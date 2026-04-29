"""
Pipeline — Main orchestrator that ties all RAG components together.

Flow: User Query → Pre-Retrieval → Retrieval → Post-Retrieval → Generation → Answer
"""

from typing import Optional
from rag.pre_retrieval import pre_retrieve
from rag.retriever import AdvancedRetriever
from rag.post_retrieval import compress_chunks
from rag.generator import generate_answer
from rag.indexer import SimpleBM25Encoder


class OlistRAGPipeline:
    """
    Complete Advanced RAG Pipeline for the Olist project.

    Usage:
        pipeline = OlistRAGPipeline(bm25_encoder=fitted_bm25)
        answer = pipeline.query("Why does the churn model fail?")
    """

    def __init__(self, bm25_encoder: Optional[SimpleBM25Encoder] = None):
        self.retriever = AdvancedRetriever(bm25_encoder=bm25_encoder)

    def query(self, user_query: str) -> str:
        """
        Run the full RAG pipeline on a user query.

        Steps:
        1. PRE-RETRIEVAL: Rewrite → Multi-Query → Route
        2. RETRIEVAL: Hybrid Search → MMR → Re-Rank
        3. POST-RETRIEVAL: Contextual Compression
        4. AUGMENTATION: Prompt Engineering → Generate
        """
        print("=" * 70)
        print(f"🧠 OLIST RAG PIPELINE")
        print(f"   Query: '{user_query}'")
        print("=" * 70)

        # Step 1: Pre-Retrieval
        rewritten, all_queries, namespaces = pre_retrieve(user_query)

        # Step 2: Retrieval
        chunks = self.retriever.retrieve(
            queries=all_queries,
            namespaces=namespaces,
            primary_query=rewritten,
        )

        # Step 3: Post-Retrieval (Contextual Compression)
        compressed = compress_chunks(rewritten, chunks)

        # Step 4: Generation
        answer = generate_answer(
            query=rewritten,
            chunks=compressed,
            original_query=user_query,
        )

        print("\n" + "=" * 70)
        print("💬 FINAL ANSWER:")
        print("=" * 70)
        print(answer)

        return answer
