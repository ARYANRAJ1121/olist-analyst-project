"""
Test script — Index documents and run a sample query.

Run this ONCE to:
1. Load all project files
2. Index them into Pinecone (with hybrid vectors)
3. Test the full RAG pipeline with a sample question
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.config import INDEX_FILES
from rag.document_loader import DocumentLoader
from rag.indexer import PineconeIndexer
from rag.pipeline import OlistRAGPipeline


def main():
    # ===================== STEP 1: Load Documents =====================
    print("=" * 60)
    print("STEP 1: Loading project documents")
    print("=" * 60)

    loader = DocumentLoader()
    docs_by_namespace = loader.load_all(INDEX_FILES)

    total = sum(len(docs) for docs in docs_by_namespace.values())
    print(f"\n📚 Total chunks loaded: {total}")

    # ===================== STEP 2: Index into Pinecone =====================
    print("\n" + "=" * 60)
    print("STEP 2: Indexing into Pinecone (hybrid: dense + BM25)")
    print("=" * 60)

    indexer = PineconeIndexer()
    indexer.create_index()
    indexer.index_documents(docs_by_namespace)

    # ===================== STEP 3: Test Query =====================
    print("\n" + "=" * 60)
    print("STEP 3: Testing RAG Pipeline")
    print("=" * 60)

    pipeline = OlistRAGPipeline(bm25_encoder=indexer.bm25)

    test_questions = [
        "What is the customer retention rate?",
    ]

    for q in test_questions:
        print(f"\n{'=' * 60}")
        answer = pipeline.query(q)
        print(f"\n{'=' * 60}\n")


if __name__ == "__main__":
    main()
