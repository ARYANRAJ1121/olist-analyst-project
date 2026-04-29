"""
Post-Retrieval — Contextual Compression.

After retrieval, chunks may contain a lot of irrelevant text alongside
the relevant parts. Contextual compression uses the LLM to extract
ONLY the sentences/parts that directly answer the user's question.

WHY?
- A 500-character chunk about "revenue analysis" might contain 3 sentences
  about revenue and 2 about data loading. If the user asked about revenue,
  we compress out the data loading sentences.
- This reduces token usage in the final generation step.
- It improves answer quality by removing noise.
"""

from typing import List

import ollama

from rag.config import LLM_MODEL
from rag.retriever import RetrievedChunk


def compress_chunks(
    query: str,
    chunks: List[RetrievedChunk],
) -> List[RetrievedChunk]:
    """
    Use LLM to extract only the relevant parts from each chunk.

    For each chunk, the LLM is asked:
    "Given this question, extract only the relevant information from this text."

    If a chunk has nothing relevant, it's dropped entirely.
    """
    print("\n📦 POST-RETRIEVAL: Contextual Compression")

    compressed = []

    for i, chunk in enumerate(chunks):
        prompt = f"""Extract ONLY the exact sentences containing information relevant to the question below.
If the text contains absolutely no relevant information, you MUST respond with exactly "NOT_RELEVANT" and nothing else.

Question: "{query}"

Text:
{chunk.text[:2000]}

Relevant extract:"""

        response = ollama.chat(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.0, "num_ctx": 2048},
        )

        extracted = response["message"]["content"].strip()
        
        # Filter out common negative responses that Llama 3 might generate
        bad_responses = ["not_relevant", "none", "n/a", "no", "none.", "no.", "n/a."]
        
        if extracted and extracted.lower() not in bad_responses:
            compressed.append(RetrievedChunk(
                text=extracted,
                score=chunk.score,
                metadata=chunk.metadata,
            ))
            source = chunk.metadata.get("source", "?")
            reduction = (1 - len(extracted) / max(len(chunk.text), 1)) * 100
            print(f"  ✂️ Chunk {i + 1} [{source}]: {len(chunk.text)} → {len(extracted)} chars ({reduction:.0f}% compressed)")
        else:
            source = chunk.metadata.get("source", "?")
            print(f"  🗑️ Chunk {i + 1} [{source}]: Dropped (not relevant)")

    print(f"  📊 Compression: {len(chunks)} → {len(compressed)} chunks kept")
    return compressed
