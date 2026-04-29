"""
Pre-Retrieval Module — Query Enhancement before searching.

Three techniques to improve retrieval quality BEFORE hitting the vector store:

1. QUERY REWRITING — LLM reformulates vague/informal queries into precise ones
   Why? Users type messy queries like "why model bad?" but the indexed documents
   use precise language like "churn prediction model accuracy".

2. MULTI-QUERY GENERATION — Creates 3-4 alternative phrasings
   Why? A single query might miss relevant documents. Multiple perspectives
   capture different angles. Results are merged and deduplicated.

3. DOMAIN-AWARE ROUTING — Routes query to the right Pinecone namespace(s)
   Why? Searching all namespaces wastes time and returns irrelevant results.
   A query about "revenue" shouldn't search the "methodology" namespace.
"""

import json
from typing import List, Tuple

import ollama

from rag.config import LLM_MODEL, LLM_TEMPERATURE, NUM_GENERATED_QUERIES, NAMESPACES


# =============================================================================
# 1. QUERY REWRITING
# =============================================================================

def rewrite_query(original_query: str) -> str:
    """
    Use LLM to reformulate a vague/informal query into a precise, searchable query.

    Example:
        Input:  "why model bad?"
        Output: "Why does the churn prediction logistic regression model have low accuracy
                 in the Olist e-commerce analysis?"
    """
    prompt = f"""You are a data analytics search assistant for the Olist E-Commerce Analytics project.

The project analyzes 100K+ e-commerce orders and covers:
- Revenue analysis (monthly trends)
- Customer retention (97% single-purchase rate)
- Churn prediction (logistic regression, data leakage)
- Statistical hypothesis testing (t-tests, Mann-Whitney U)
- A/B testing (post-purchase discount experiment)
- Business recommendations

Rewrite the following user query to be clear, specific, and searchable.
Add relevant domain terms if the query is vague.
Return ONLY the rewritten query, nothing else.

User query: "{original_query}"

Rewritten query:"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.0, "num_ctx": 1024},
    )

    rewritten = response["message"]["content"].strip().strip('"')
    print(f"  🔄 Query Rewritten: '{original_query}' → '{rewritten}'")
    return rewritten


# =============================================================================
# 2. MULTI-QUERY GENERATION
# =============================================================================

def generate_multi_queries(query: str, n: int = NUM_GENERATED_QUERIES) -> List[str]:
    """
    Generate multiple semantically different queries from the original.

    This captures different angles of the same question.

    Example:
        Input: "Why does the churn model fail?"
        Output: [
            "What is the accuracy of the churn prediction model?",
            "What causes data leakage in churn feature engineering?",
            "Are there statistical differences between churned and active customers?"
        ]
    """
    prompt = f"""You are a data analytics search assistant for the Olist E-Commerce project.

Generate exactly {n} different search queries that would help answer the user's question.
Each query should approach the question from a different angle.
Return ONLY the queries, one per line, numbered 1-{n}.

The project covers: revenue analysis, customer retention (97% churn), churn prediction
(logistic regression, data leakage), statistical tests (t-test, Mann-Whitney), 
A/B testing (discount incentives), and business recommendations.

User's question: "{query}"

Alternative queries:"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.3, "num_ctx": 1024},
    )

    raw = response["message"]["content"].strip()

    # Parse numbered lines
    queries = []
    for line in raw.split("\n"):
        line = line.strip()
        if not line:
            continue
        # Remove numbering like "1.", "1)", "1:"
        cleaned = line.lstrip("0123456789").lstrip(".):-").strip()
        if cleaned:
            queries.append(cleaned)

    queries = queries[:n]  # Cap at n
    print(f"  📝 Multi-Query Generated: {len(queries)} variants")
    for i, q in enumerate(queries):
        print(f"     {i + 1}. {q}")

    return queries


# =============================================================================
# 3. DOMAIN-AWARE ROUTING
# =============================================================================

# Keyword-to-namespace mapping rules
ROUTING_RULES = {
    "revenue": [
        "revenue", "sales", "monthly", "income", "money earned",
        "growth", "trend", "seasonal", "quarter", "Q4",
    ],
    "retention": [
        "retention", "repeat", "comeback", "return", "loyal",
        "one-time", "single purchase", "customer lifetime",
    ],
    "churn": [
        "churn", "predict", "model", "logistic regression",
        "accuracy", "leakage", "feature", "coefficient",
        "ROC", "AUC", "classification", "machine learning",
        "statistical test", "t-test", "mann-whitney", "p-value",
        "hypothesis", "significant",
    ],
    "ab_test": [
        "a/b test", "ab test", "experiment", "control group",
        "treatment", "discount", "incentive", "conversion",
        "z-test", "z-score", "lift", "ROI",
    ],
    "methodology": [
        "how", "code", "script", "sql", "query", "python",
        "pipeline", "implement", "process", "step",
        "duckdb", "join", "CTE", "function",
    ],
    "general": [
        "what is", "overview", "summary", "explain", "project",
        "recommend", "business", "strategy", "action",
        "insight", "finding", "conclusion",
    ],
}


def route_query(query: str) -> List[str]:
    """
    Determine which Pinecone namespace(s) to search based on query content.

    Uses keyword matching with a fallback to LLM classification.
    Returns 1-3 namespaces to search (more specific = fewer namespaces).

    Why keyword-first?
    - Fast (no LLM call needed)
    - Deterministic (same query → same routing)
    - LLM fallback handles ambiguous cases
    """
    query_lower = query.lower()

    # Score each namespace based on keyword matches
    scores = {}
    for namespace, keywords in ROUTING_RULES.items():
        score = sum(1 for kw in keywords if kw in query_lower)
        if score > 0:
            scores[namespace] = score

    if scores:
        # Sort by score descending, take top 2
        sorted_ns = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        selected = [ns for ns, _ in sorted_ns[:2]]

        # Always include 'general' if not already there (has broad context)
        if "general" not in selected and len(selected) < 3:
            selected.append("general")

        print(f"  🗂️ Routed to namespaces: {selected} (keyword-based)")
        return selected

    # Fallback: LLM-based classification
    return _llm_route_query(query)


def _llm_route_query(query: str) -> List[str]:
    """
    Fallback: Use LLM to classify the query into namespace(s).
    Only called when keyword matching finds nothing.
    """
    namespace_list = ", ".join(NAMESPACES.keys())
    prompt = f"""Classify this question into 1-2 categories from: [{namespace_list}]

Categories:
- revenue: questions about sales, income, monthly trends
- retention: questions about repeat customers, customer loyalty
- churn: questions about churn prediction, model performance, statistical tests
- ab_test: questions about A/B testing, experiments, discounts
- methodology: questions about code, SQL, how things were implemented
- general: broad questions about the project, recommendations

Question: "{query}"

Return ONLY the category names, comma-separated:"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.0, "num_ctx": 512},
    )

    raw = response["message"]["content"].strip().lower()
    namespaces = [ns.strip() for ns in raw.split(",") if ns.strip() in NAMESPACES]

    if not namespaces:
        namespaces = ["general"]

    # Always include general for context
    if "general" not in namespaces:
        namespaces.append("general")

    print(f"  🗂️ Routed to namespaces: {namespaces} (LLM-based)")
    return namespaces


# =============================================================================
# COMBINED PRE-RETRIEVAL STEP
# =============================================================================

def pre_retrieve(original_query: str) -> Tuple[str, List[str], List[str]]:
    """
    Run the full pre-retrieval pipeline:
    1. Rewrite the query
    2. Generate multi-queries
    3. Route to namespaces

    Returns:
        Tuple of (rewritten_query, all_queries, target_namespaces)
    """
    print("\n🔧 PRE-RETRIEVAL PIPELINE")
    print(f"  Original query: '{original_query}'")

    # Step 1: Rewrite
    rewritten = rewrite_query(original_query)

    # Step 2: Multi-query
    multi_queries = generate_multi_queries(rewritten)

    # Combine: rewritten query + multi-queries (no duplicates)
    all_queries = [rewritten] + [q for q in multi_queries if q != rewritten]

    # Step 3: Route (use rewritten query for routing)
    namespaces = route_query(rewritten)

    return rewritten, all_queries, namespaces
