"""
Configuration for Olist Advanced RAG Pipeline.

This module stores all configuration constants: API keys (via env vars),
model names, Pinecone settings, chunking parameters, and retrieval tuning.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# API KEYS (loaded from environment variables or .env file)
# =============================================================================
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")

# =============================================================================
# PINECONE SETTINGS
# =============================================================================
PINECONE_INDEX_NAME = "olist-rag"
PINECONE_CLOUD = "aws"
PINECONE_REGION = "us-east-1"
EMBEDDING_DIMENSION = 768  # nomic-embed-text output dimension
PINECONE_METRIC = "dotproduct"  # Required for hybrid search

# Namespaces for domain-aware routing
NAMESPACES = {
    "revenue": "revenue",
    "retention": "retention",
    "churn": "churn",
    "ab_test": "ab_test",
    "methodology": "methodology",
    "general": "general",
}

# =============================================================================
# OLLAMA SETTINGS
# =============================================================================
OLLAMA_BASE_URL = "http://localhost:11434"
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3"
LLM_TEMPERATURE = 0.1  # Low temperature for factual, grounded answers
LLM_NUM_CTX = 4096  # Context window size

# =============================================================================
# CHUNKING SETTINGS
# =============================================================================
CHUNK_SIZE = 500  # Characters per chunk
CHUNK_OVERLAP = 100  # Overlap between consecutive chunks
# Separators ordered by priority (try to split on these first)
CHUNK_SEPARATORS = ["\n\n", "\n", ". ", ", ", " "]

# =============================================================================
# RETRIEVAL SETTINGS
# =============================================================================
# Hybrid search weighting: 0.0 = pure sparse (BM25), 1.0 = pure dense (semantic)
HYBRID_ALPHA = 0.6  # Favor semantic slightly, but keep keyword relevance

# How many candidates to fetch from Pinecone before re-ranking
INITIAL_TOP_K = 20

# How many results to keep after MMR diversity filtering
MMR_TOP_K = 10

# MMR lambda: 0.0 = max diversity, 1.0 = max relevance
MMR_LAMBDA = 0.7

# How many results to keep after cross-encoder re-ranking
RERANK_TOP_K = 5

# Cross-encoder model for re-ranking
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# =============================================================================
# MULTI-QUERY SETTINGS
# =============================================================================
NUM_GENERATED_QUERIES = 3  # Number of alternative queries to generate

# =============================================================================
# FILE PATHS (relative to project root)
# =============================================================================
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
SQL_DIR = os.path.join(PROJECT_ROOT, "sql")
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")

# Files to index
INDEX_FILES = {
    "general": [
        os.path.join(PROJECT_ROOT, "README.md"),
        os.path.join(PROJECT_ROOT, "business_recommendations.md"),
    ],
    "revenue": [
        os.path.join(OUTPUT_DIR, "monthly_revenue.csv"),
    ],
    "retention": [
        os.path.join(OUTPUT_DIR, "retention_metrics.csv"),
    ],
    "churn": [
        os.path.join(OUTPUT_DIR, "churn_features_v2.csv"),
        os.path.join(OUTPUT_DIR, "churn_statistical_tests.csv"),
        os.path.join(OUTPUT_DIR, "logistic_regression_coefficients_v2.csv"),
    ],
    "ab_test": [
        os.path.join(OUTPUT_DIR, "ab_test_second_purchase_results.csv"),
    ],
    "methodology": [
        os.path.join(SQL_DIR, "schema.sql"),
        os.path.join(SQL_DIR, "revenue_analysis.sql"),
        os.path.join(SQL_DIR, "retention_metrics.sql"),
        os.path.join(SQL_DIR, "churn_definition.sql"),
        os.path.join(SQL_DIR, "churn_features.sql"),
        os.path.join(SQL_DIR, "churn_statistical_analysis.sql"),
        os.path.join(SQL_DIR, "customer_revenue_decomposition.sql"),
        os.path.join(SCRIPTS_DIR, "run_analysis.py"),
        os.path.join(SCRIPTS_DIR, "run_retention_analysis.py"),
        os.path.join(SCRIPTS_DIR, "run_churn_feature_extraction_v2.py"),
        os.path.join(SCRIPTS_DIR, "run_churn_logistic_regression_v2.py"),
        os.path.join(SCRIPTS_DIR, "run_churn_statistical_tests.py"),
        os.path.join(SCRIPTS_DIR, "run_ab_test_retention.py"),
        os.path.join(SCRIPTS_DIR, "run_visualizations.py"),
    ],
}
