"""
Retriever — Hybrid Search, MMR, and Re-Ranking.

Three techniques applied DURING retrieval:

1. HYBRID SEARCH — Combines dense (semantic) + sparse (BM25 keyword) search
   Why? "ROC-AUC" as a keyword won't match semantically, but BM25 catches it.
   "model performance" semantically matches "accuracy" but keywords wouldn't.

2. MMR (Maximal Marginal Relevance) — Diversifies results
   Why? Without MMR, you might get 5 chunks all saying the same thing.
   MMR balances relevance and diversity to get broader coverage.

3. RE-RANKING (Cross-Encoder) — Re-scores the shortlist for precision
   Why? Bi-encoder retrieval is fast but approximate. Cross-encoders are
   slow but much more accurate. We use them only on the top-K shortlist.
"""

import numpy as np
from typing import List, Dict, Any, Tuple

from pinecone import Pinecone
from sentence_transformers import CrossEncoder

from rag.config import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    INITIAL_TOP_K,
    MMR_TOP_K,
    MMR_LAMBDA,
    RERANK_TOP_K,
    RERANKER_MODEL,
    HYBRID_ALPHA,
    EMBEDDING_MODEL,
)
from rag.indexer import get_embedding, SimpleBM25Encoder


class RetrievedChunk:
    """Represents a single retrieved chunk with score and metadata."""

    def __init__(self, text: str, score: float, metadata: Dict[str, Any]):
        self.text = text
        self.score = score
        self.metadata = metadata

    def __repr__(self):
        source = self.metadata.get("source", "?")
        return f"Chunk(source={source}, score={self.score:.3f}, len={len(self.text)})"


class AdvancedRetriever:
    """
    Orchestrates the three retrieval techniques:
    Hybrid Search → MMR → Re-Ranking
    """

    def __init__(self, bm25_encoder: SimpleBM25Encoder = None):
        """
        Args:
            bm25_encoder: A fitted BM25 encoder (same one used during indexing).
                         If None, only dense search is used.
        """
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index = self.pc.Index(PINECONE_INDEX_NAME)
        self.bm25 = bm25_encoder

        # Load cross-encoder for re-ranking (lazy load on first use)
        self._reranker = None

    @property
    def reranker(self):
        """Lazy-load the cross-encoder model (downloads on first use)."""
        if self._reranker is None:
            print("  📥 Loading cross-encoder re-ranker...")
            self._reranker = CrossEncoder(RERANKER_MODEL)
        return self._reranker

    # =========================================================================
    # 1. HYBRID SEARCH
    # =========================================================================

    def hybrid_search(
        self,
        query: str,
        namespaces: List[str],
        top_k: int = INITIAL_TOP_K,
    ) -> List[RetrievedChunk]:
        """
        Search Pinecone using both dense and sparse vectors.

        Dense: Captures semantic meaning (embedding similarity)
        Sparse: Captures exact keyword matches (BM25)

        The alpha parameter controls the weighting:
        - alpha = 1.0: pure dense (semantic only)
        - alpha = 0.0: pure sparse (keyword only)
        - alpha = 0.6: balanced (our default)
        """
        # Get dense embedding for the query
        dense_vector = get_embedding(query)

        # Get sparse BM25 vector for the query (if encoder is available)
        sparse_vector = None
        if self.bm25 and self.bm25.fitted:
            sparse_vector = self.bm25.encode(query)

        all_chunks = []
        seen_ids = set()

        for namespace in namespaces:
            try:
                # Build query params
                query_params = {
                    "vector": dense_vector,
                    "top_k": top_k,
                    "namespace": namespace,
                    "include_metadata": True,
                }

                # Add sparse vector for hybrid search
                if sparse_vector and sparse_vector["indices"]:
                    query_params["sparse_vector"] = sparse_vector

                results = self.index.query(**query_params)

                # Pinecone v3 returns objects, not dicts — use attribute access
                for match in results.matches:
                    if match.id in seen_ids:
                        continue
                    seen_ids.add(match.id)

                    metadata = match.metadata or {}
                    text = metadata.get("text", "")
                    if text:
                        all_chunks.append(RetrievedChunk(
                            text=text,
                            score=match.score,
                            metadata=metadata,
                        ))

            except Exception as e:
                print(f"  [WARN] Error searching namespace '{namespace}': {e}")

        # Sort by score descending
        all_chunks.sort(key=lambda c: c.score, reverse=True)
        print(f"  🔍 Hybrid Search: Retrieved {len(all_chunks)} chunks from {namespaces}")
        return all_chunks

    def multi_query_search(
        self,
        queries: List[str],
        namespaces: List[str],
        top_k: int = INITIAL_TOP_K,
    ) -> List[RetrievedChunk]:
        """
        Run hybrid search for each query and merge results.
        Deduplicates by text content (keeps highest score).
        """
        merged = {}  # text_hash -> RetrievedChunk (keep best score)

        for i, query in enumerate(queries):
            print(f"\n  📎 Searching with query {i + 1}/{len(queries)}: '{query[:80]}...'")
            results = self.hybrid_search(query, namespaces, top_k=top_k)

            for chunk in results:
                text_hash = hash(chunk.text[:200])
                if text_hash not in merged or chunk.score > merged[text_hash].score:
                    merged[text_hash] = chunk

        all_chunks = sorted(merged.values(), key=lambda c: c.score, reverse=True)
        print(f"\n  📊 Multi-Query Merge: {len(all_chunks)} unique chunks")
        return all_chunks

    # =========================================================================
    # 2. MMR (Maximal Marginal Relevance)
    # =========================================================================

    def apply_mmr(
        self,
        query: str,
        chunks: List[RetrievedChunk],
        top_k: int = MMR_TOP_K,
        lambda_param: float = MMR_LAMBDA,
    ) -> List[RetrievedChunk]:
        """
        Apply MMR to select diverse yet relevant chunks.

        MMR algorithm:
        For each candidate, score = λ * relevance - (1-λ) * max_similarity_to_selected

        This ensures we don't just pick the top-K most similar chunks
        (which might all say the same thing), but instead pick chunks
        that are both relevant AND different from each other.

        Args:
            query: The search query
            chunks: Candidate chunks from hybrid search
            top_k: Number of chunks to select
            lambda_param: Balance between relevance (1.0) and diversity (0.0)
        """
        if len(chunks) <= top_k:
            return chunks

        # Get embeddings for all chunks
        query_emb = np.array(get_embedding(query))
        chunk_embs = []
        for chunk in chunks:
            emb = np.array(get_embedding(chunk.text[:500]))
            chunk_embs.append(emb)
        chunk_embs = np.array(chunk_embs)

        # Normalize for cosine similarity
        query_norm = query_emb / (np.linalg.norm(query_emb) + 1e-8)
        chunk_norms = chunk_embs / (np.linalg.norm(chunk_embs, axis=1, keepdims=True) + 1e-8)

        # Relevance scores: similarity to query
        relevance_scores = chunk_norms @ query_norm

        # MMR selection
        selected_indices = []
        remaining_indices = list(range(len(chunks)))

        for _ in range(min(top_k, len(chunks))):
            best_idx = None
            best_score = -float("inf")

            for idx in remaining_indices:
                relevance = relevance_scores[idx]

                # Max similarity to already selected chunks
                if selected_indices:
                    selected_embs = chunk_norms[selected_indices]
                    similarities = selected_embs @ chunk_norms[idx]
                    max_sim = np.max(similarities)
                else:
                    max_sim = 0

                # MMR score
                mmr_score = lambda_param * relevance - (1 - lambda_param) * max_sim

                if mmr_score > best_score:
                    best_score = mmr_score
                    best_idx = idx

            if best_idx is not None:
                selected_indices.append(best_idx)
                remaining_indices.remove(best_idx)

        selected = [chunks[i] for i in selected_indices]
        print(f"  🎯 MMR: Selected {len(selected)} diverse chunks (λ={lambda_param})")
        return selected

    # =========================================================================
    # 3. RE-RANKING (Cross-Encoder)
    # =========================================================================

    def rerank(
        self,
        query: str,
        chunks: List[RetrievedChunk],
        top_k: int = RERANK_TOP_K,
    ) -> List[RetrievedChunk]:
        """
        Re-rank chunks using a cross-encoder model.

        WHY CROSS-ENCODER > BI-ENCODER?
        - Bi-encoder (used in initial retrieval): Encodes query and document
          separately, then computes similarity. Fast but less accurate.
        - Cross-encoder: Takes (query, document) pair together and scores them
          jointly. Much more accurate but slower.

        We use bi-encoder for initial retrieval (fast, handles 90K+ docs)
        then cross-encoder for re-ranking (accurate, only handles ~10 docs).
        """
        if not chunks:
            return []

        # Create (query, document) pairs for cross-encoder
        pairs = [(query, chunk.text[:512]) for chunk in chunks]

        # Score all pairs
        scores = self.reranker.predict(pairs)

        # Assign new scores
        for chunk, score in zip(chunks, scores):
            chunk.score = float(score)

        # Sort by new scores and take top_k
        chunks.sort(key=lambda c: c.score, reverse=True)
        reranked = chunks[:top_k]

        print(f"  🏆 Re-Ranked: Top {len(reranked)} chunks")
        for i, chunk in enumerate(reranked):
            source = chunk.metadata.get("source", "?")
            print(f"     {i + 1}. [{source}] score={chunk.score:.3f}")

        return reranked

    # =========================================================================
    # FULL RETRIEVAL PIPELINE
    # =========================================================================

    def retrieve(
        self,
        queries: List[str],
        namespaces: List[str],
        primary_query: str,
    ) -> List[RetrievedChunk]:
        """
        Full retrieval pipeline:
        Multi-Query Hybrid Search → MMR → Re-Ranking

        Args:
            queries: All queries (original + multi-query variants)
            namespaces: Target namespaces from domain routing
            primary_query: The rewritten query (used for MMR and re-ranking)

        Returns:
            Top-K re-ranked, diverse chunks
        """
        print("\n🔎 RETRIEVAL PIPELINE")

        # Step 1: Multi-query hybrid search
        candidates = self.multi_query_search(queries, namespaces)

        if not candidates:
            print("  ⚠️ No candidates found!")
            return []

        # Step 2: MMR for diversity
        diverse = self.apply_mmr(primary_query, candidates)

        # Step 3: Cross-encoder re-ranking
        final = self.rerank(primary_query, diverse)

        return final
