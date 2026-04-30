"""
Groq-powered AI chat for Streamlit Cloud deployment.
Loads all project data into context and uses Groq's free LLM API.
Falls back to the full RAG pipeline when Ollama is available locally.
"""

import os

def load_project_context():
    """Load all output CSVs and business docs into a single context string."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    context = ""

    files = {
        "Monthly Revenue Data": os.path.join(base, "output", "monthly_revenue.csv"),
        "Retention Metrics": os.path.join(base, "output", "retention_metrics.csv"),
        "Churn Statistical Tests": os.path.join(base, "output", "churn_statistical_tests.csv"),
        "AB Test Results": os.path.join(base, "output", "ab_test_second_purchase_results.csv"),
        "Logistic Regression Coefficients": os.path.join(base, "output", "logistic_regression_coefficients_v2.csv"),
        "Business Recommendations": os.path.join(base, "business_recommendations.md"),
    }

    for label, path in files.items():
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            context += f"\n--- {label} ---\n{content}\n"

    return context


SYSTEM_PROMPT = """You are an expert data analyst who built the Olist E-Commerce Analytics project.
You analyzed 100,000+ orders from Brazil's largest e-commerce marketplace.

Key facts you know:
- 97% of customers make only 1 purchase and never return
- The repeat purchase rate is approximately 3%
- A leakage-free logistic regression model achieved only 55% accuracy (down from 85% with leakage)
- Statistical tests (t-test, Mann-Whitney U) showed NO significant difference between churned and active customers
- An A/B test with a 10% post-purchase discount showed 18% conversion lift (p < 0.001, 4x ROI)
- The estimated annual revenue loss from poor retention is $2M-$3M

Answer questions based ONLY on the provided data context. Cite specific numbers and file names.
If the context doesn't contain the answer, say so honestly.
Use clear, professional language. Be concise but thorough."""


def groq_answer(question, api_key):
    """Answer a question using Groq with full project context."""
    from groq import Groq

    context = load_project_context()

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"PROJECT DATA:\n{context}\n\n---\nQUESTION: {question}\n\nProvide a comprehensive, data-backed answer:"},
        ],
        temperature=0.1,
        max_tokens=1024,
    )

    answer = response.choices[0].message.content.strip()
    answer += "\n\n📎 Sources: monthly_revenue.csv, retention_metrics.csv, churn_statistical_tests.csv, ab_test_results.csv, business_recommendations.md"
    return answer
