"""
Indexer — Embeds documents and upserts into Pinecone with hybrid vectors.

This module handles:
1. Generating dense embeddings via Ollama (nomic-embed-text)
2. Generating sparse vectors via BM25 for keyword matching
3. Upserting both into Pinecone for hybrid search
4. Creating the Pinecone index if it doesn't exist

WHY HYBRID?
- Dense embeddings capture semantic meaning ("customer dropout" ≈ "churn")
- Sparse/BM25 captures exact keywords ("ROC-AUC", "p-value", "97%")
- Together they give best-of-both-worlds retrieval
"""

import hashlib
import math
import re
from collections import Counter
from typing import List, Dict, Any, Tuple

import ollama
from pinecone import Pinecone, ServerlessSpec

from rag.config import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    PINECONE_CLOUD,
    PINECONE_REGION,
    PINECONE_METRIC,
    EMBEDDING_DIMENSION,
    EMBEDDING_MODEL,
)
from rag.document_loader import Document


# =============================================================================
# BM25 SPARSE ENCODER (lightweight, no external dependency)
# =============================================================================

class SimpleBM25Encoder:
    """
    A lightweight BM25 sparse vector encoder.

    We implement BM25 from scratch instead of using pinecone-text because:
    1. Fewer dependencies
    2. Full control over tokenization
    3. Easy to understand and explain in interviews

    BM25 scores how important a word is to a document relative to a corpus.
    """

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1  # Term frequency saturation parameter
        self.b = b      # Length normalization parameter
        self.vocab = {}  # word -> index mapping
        self.idf = {}    # word -> IDF score
        self.avg_doc_len = 0
        self.fitted = False

    def _tokenize(self, text: str) -> List[str]:
        """Simple whitespace + punctuation tokenizer."""
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens

    def fit(self, corpus: List[str]):
        """
        Fit BM25 on a corpus of documents.

        Calculates IDF (Inverse Document Frequency) for each word.
        IDF measures how rare/important a word is across all documents.
        """
        n_docs = len(corpus)
        doc_freq = Counter()  # How many documents contain each word
        total_len = 0
        word_set = set()

        for doc in corpus:
            tokens = self._tokenize(doc)
            total_len += len(tokens)
            unique_tokens = set(tokens)
            for token in unique_tokens:
                doc_freq[token] += 1
                word_set.add(token)

        self.avg_doc_len = total_len / max(n_docs, 1)

        # Build vocabulary mapping
        self.vocab = {word: idx for idx, word in enumerate(sorted(word_set))}

        # Calculate IDF for each word
        # IDF = log((N - df + 0.5) / (df + 0.5) + 1)
        for word, df in doc_freq.items():
            self.idf[word] = math.log((n_docs - df + 0.5) / (df + 0.5) + 1)

        self.fitted = True
        print(f"  BM25 fitted on {n_docs} documents, vocabulary size: {len(self.vocab)}")

    def encode(self, text: str) -> Dict[str, List]:
        """
        Encode a text into a Pinecone-compatible sparse vector.

        Returns: {"indices": [int, ...], "values": [float, ...]}
        """
        if not self.fitted:
            raise RuntimeError("BM25 encoder not fitted. Call fit() first.")

        tokens = self._tokenize(text)
        doc_len = len(tokens)
        tf_map = Counter(tokens)

        indices = []
        values = []

        for word, tf in tf_map.items():
            if word not in self.vocab or word not in self.idf:
                continue

            # BM25 score for this term
            idf = self.idf[word]
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / max(self.avg_doc_len, 1))
            score = idf * (numerator / denominator)

            if score > 0:
                indices.append(self.vocab[word])
                values.append(round(score, 4))

        return {"indices": indices, "values": values}


# =============================================================================
# EMBEDDING FUNCTIONS
# =============================================================================

def get_embedding(text: str) -> List[float]:
    """
    Get dense embedding for a single text using Ollama nomic-embed-text.

    nomic-embed-text produces 768-dimensional embeddings.
    """
    response = ollama.embeddings(model=EMBEDDING_MODEL, prompt=text)
    return response["embedding"]


def get_embeddings_batch(texts: List[str], batch_size: int = 32) -> List[List[float]]:
    """
    Get embeddings for multiple texts in batches.

    Ollama processes one at a time, so we batch for progress tracking only.
    """
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        for text in batch:
            emb = get_embedding(text)
            all_embeddings.append(emb)
        print(f"    Embedded {min(i + batch_size, len(texts))}/{len(texts)}")
    return all_embeddings


# =============================================================================
# PINECONE INDEXER
# =============================================================================

class PineconeIndexer:
    """
    Handles creating the Pinecone index and upserting documents
    with both dense and sparse vectors for hybrid search.
    """

    def __init__(self):
        if not PINECONE_API_KEY:
            raise ValueError(
                "PINECONE_API_KEY not set! "
                "Set it in your .env file or as an environment variable."
            )
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.bm25 = SimpleBM25Encoder()

    def create_index(self):
        """Create Pinecone index if it doesn't exist."""
        existing = self.pc.list_indexes().names()

        if PINECONE_INDEX_NAME in existing:
            print(f"✅ Index '{PINECONE_INDEX_NAME}' already exists.")
        else:
            print(f"🔨 Creating index '{PINECONE_INDEX_NAME}'...")
            self.pc.create_index(
                name=PINECONE_INDEX_NAME,
                dimension=EMBEDDING_DIMENSION,
                metric=PINECONE_METRIC,
                spec=ServerlessSpec(
                    cloud=PINECONE_CLOUD,
                    region=PINECONE_REGION,
                ),
            )
            print(f"✅ Index '{PINECONE_INDEX_NAME}' created.")

        self.index = self.pc.Index(PINECONE_INDEX_NAME)

    def _make_id(self, namespace: str, content: str) -> str:
        """Generate a deterministic ID for a document chunk."""
        hash_input = f"{namespace}:{content[:200]}"
        return hashlib.md5(hash_input.encode()).hexdigest()

    def index_documents(self, docs_by_namespace: Dict[str, List[Document]]):
        """
        Index all documents into Pinecone with hybrid vectors.

        Steps:
        1. Fit BM25 on all document contents (corpus-level statistics)
        2. For each document: generate dense embedding + sparse BM25 vector
        3. Upsert to Pinecone with metadata in the correct namespace
        """
        # Step 1: Fit BM25 on entire corpus
        print("\n📊 Fitting BM25 encoder on corpus...")
        all_contents = []
        for docs in docs_by_namespace.values():
            for doc in docs:
                all_contents.append(doc.content)
        self.bm25.fit(all_contents)

        # Step 2: Embed and upsert per namespace
        for namespace, docs in docs_by_namespace.items():
            if not docs:
                continue

            print(f"\n📤 Indexing namespace '{namespace}' ({len(docs)} chunks)...")

            vectors_to_upsert = []
            for i, doc in enumerate(docs):
                # Dense embedding
                dense = get_embedding(doc.content[:2000])  # Cap length for embedding

                # Sparse BM25 vector
                sparse = self.bm25.encode(doc.content)

                # Build vector record
                vec_id = self._make_id(namespace, doc.content)
                vectors_to_upsert.append({
                    "id": vec_id,
                    "values": dense,
                    "sparse_values": sparse,
                    "metadata": {
                        **doc.metadata,
                        "text": doc.content[:4000],  # Store text in metadata (Pinecone limit ~40KB)
                    }
                })

                if (i + 1) % 5 == 0 or (i + 1) == len(docs):
                    print(f"    Processed {i + 1}/{len(docs)}")

            # Upsert in batches of 50
            batch_size = 50
            for i in range(0, len(vectors_to_upsert), batch_size):
                batch = vectors_to_upsert[i:i + batch_size]
                self.index.upsert(vectors=batch, namespace=namespace)
            
            print(f"  ✅ Upserted {len(vectors_to_upsert)} vectors to '{namespace}'")

        print("\n🎉 Indexing complete!")
        print(self.index.describe_index_stats())

    def delete_all(self):
        """Delete all vectors from the index (for re-indexing)."""
        print("🗑️ Deleting all vectors...")
        for ns in ["revenue", "retention", "churn", "ab_test", "methodology", "general"]:
            try:
                self.index.delete(delete_all=True, namespace=ns)
            except Exception:
                pass
        print("✅ All vectors deleted.")
