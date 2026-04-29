"""
Generator — Prompt Engineering + LLM Answer Generation.
"""

from typing import List
import ollama

from rag.config import LLM_MODEL, LLM_TEMPERATURE, LLM_NUM_CTX
from rag.retriever import RetrievedChunk


SYSTEM_PROMPT = """You are an expert data analyst who built the Olist E-Commerce Analytics project.
Answer questions based ONLY on the provided context. Cite specific numbers and file names.
If the context doesn't contain the answer, say so. Use clear, professional language."""


def generate_answer(query: str, chunks: List[RetrievedChunk], original_query: str = None) -> str:
    """Generate a final answer using the LLM with compressed context."""
    print("\n✨ AUGMENTATION: Generating Answer")

    if not chunks:
        return "I couldn't find relevant information. Try asking about revenue, retention, churn, A/B testing, or methodology."

    context_parts = []
    for chunk in chunks:
        source = chunk.metadata.get("source", "unknown")
        context_parts.append(f"--- Source: {source} ---\n{chunk.text}")

    context = "\n\n".join(context_parts)

    user_message = f"""CONTEXT FROM PROJECT FILES:
{context}

---
QUESTION: {query}

Provide a comprehensive answer based on the context above."""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        options={"temperature": LLM_TEMPERATURE, "num_ctx": LLM_NUM_CTX},
    )

    answer = response["message"]["content"].strip()
    sources = list(set(chunk.metadata.get("source", "unknown") for chunk in chunks))
    answer += f"\n\n📎 Sources: {', '.join(sources)}"
    print(f"  ✅ Answer generated ({len(answer)} chars)")
    return answer
