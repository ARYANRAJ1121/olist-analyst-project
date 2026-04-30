# Olist Project - Git Sync Script
# Commits each changed file individually with descriptive messages

param(
    [string]$Email = $(Read-Host "Enter your EXACT GitHub email"),
    [string]$Name = $(Read-Host "Enter your GitHub display name")
)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Olist Project - Git Sync" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Step 1: Fix git identity
Write-Host ""
Write-Host "[1/3] Setting Git identity..." -ForegroundColor Yellow
git config user.email $Email
git config user.name $Name
Write-Host ("  Done: " + $Name + " (" + $Email + ")") -ForegroundColor Green

# Step 2: Commit each changed file individually
Write-Host ""
Write-Host "[2/3] Committing changed files..." -ForegroundColor Yellow

# Commit message map
$commitMessages = @{}
$commitMessages["README.md"] = "docs: rewrite README with charts, architecture diagrams, ROI metrics"
$commitMessages["app.py"] = "feat(dashboard): integrate Ask AI chatbot with RAG pipeline"
$commitMessages["business_recommendations.md"] = "docs: add strategic business recommendations"
$commitMessages["requirements.txt"] = "chore(deps): add dashboard dependencies"
$commitMessages["requirements_rag.txt"] = "chore(deps): add RAG pipeline dependencies"
$commitMessages["requirements_dashboard.txt"] = "chore(deps): add dashboard requirements file"
$commitMessages[".gitignore"] = "chore: update gitignore with DuckDB and vscode exclusions"
$commitMessages[".vscode/settings.json"] = "config: add SQLTools PostgreSQL connection settings"
$commitMessages[".streamlit/config.toml"] = "config: add Streamlit server configuration"
$commitMessages["rag/__init__.py"] = "feat(rag): add RAG package init"
$commitMessages["rag/config.py"] = "feat(rag): add pipeline configuration for Pinecone and Ollama"
$commitMessages["rag/document_loader.py"] = "feat(rag): implement document loader with multi-format chunkers"
$commitMessages["rag/indexer.py"] = "feat(rag): implement BM25 encoder and Pinecone hybrid indexer"
$commitMessages["rag/pre_retrieval.py"] = "feat(rag): implement query rewriting and domain routing"
$commitMessages["rag/retriever.py"] = "feat(rag): implement hybrid search, MMR, cross-encoder reranking"
$commitMessages["rag/post_retrieval.py"] = "feat(rag): implement contextual compression with LLM"
$commitMessages["rag/generator.py"] = "feat(rag): implement prompt engineering and answer generation"
$commitMessages["rag/pipeline.py"] = "feat(rag): implement end-to-end RAG pipeline orchestrator"
$commitMessages["rag/test_pipeline.py"] = "feat(rag): add indexing and test script"
$commitMessages["sql/schema.sql"] = "feat(sql): add schema with SERIAL PKs and indexes"
$commitMessages["sql/revenue_analysis.sql"] = "feat(sql): add revenue analysis with block annotations"
$commitMessages["sql/retention_metrics.sql"] = "feat(sql): add retention metrics with block annotations"
$commitMessages["sql/churn_definition.sql"] = "feat(sql): add churn definition with block annotation"
$commitMessages["sql/churn_features.sql"] = "feat(sql): add churn feature engineering CTE"
$commitMessages["sql/churn_statistical_analysis.sql"] = "feat(sql): add statistical analysis queries"
$commitMessages["sql/customer_revenue_decomposition.sql"] = "feat(sql): add revenue decomposition query"
$commitMessages["sql/load_data.sql"] = "feat(sql): add PostgreSQL COPY data loading"
$commitMessages["sql/validation_checks.sql"] = "feat(sql): add data validation queries"
$commitMessages["scripts/setup_postgres.py"] = "feat(scripts): add PostgreSQL database setup and CSV loader"
$commitMessages["scripts/setup_duckdb.py"] = "feat(scripts): add DuckDB database setup script"
$commitMessages["scripts/run_analysis.py"] = "feat(scripts): update revenue analysis script"
$commitMessages["scripts/run_retention_analysis.py"] = "feat(scripts): update retention analysis script"
$commitMessages["scripts/run_churn_feature_extraction.py"] = "feat(scripts): update churn feature extraction"
$commitMessages["scripts/run_churn_feature_extraction_v2.py"] = "feat(scripts): update leakage-free feature engineering"
$commitMessages["scripts/run_churn_logistic_regression.py"] = "feat(scripts): update logistic regression script"
$commitMessages["scripts/run_churn_logistic_regression_v2.py"] = "feat(scripts): update leakage-free regression model"
$commitMessages["scripts/run_churn_statistical_tests.py"] = "feat(scripts): update statistical hypothesis testing"
$commitMessages["scripts/run_ab_test_retention.py"] = "feat(scripts): update AB test simulation script"
$commitMessages["scripts/run_visualizations.py"] = "feat(scripts): update visualization generation script"
$commitMessages["git_sync.ps1"] = "chore: add git sync automation script"

$committed = 0

# Get changed files
$changes = git status --porcelain

foreach ($line in $changes) {
    if (-not $line) { continue }
    
    $filepath = $line.Substring(3).Trim().Trim('"')
    
    # Skip unwanted files
    if ($filepath -match "\.env$") { continue }
    if ($filepath -match "rag_env/") { continue }
    if ($filepath -match "__pycache__") { continue }
    
    # Handle renames
    if ($filepath -match " -> ") {
        $filepath = ($filepath -split " -> ")[1]
    }

    # Look up commit message or generate one
    $msg = $commitMessages[$filepath]
    if (-not $msg) {
        $basename = Split-Path $filepath -Leaf
        $msg = "chore: update " + $basename
    }

    git add $filepath 2>$null
    $result = git commit -m $msg 2>&1
    $resultStr = $result | Out-String
    
    if ($resultStr -match "file changed|insertion|deletion|create mode") {
        Write-Host ("  OK: " + $filepath) -ForegroundColor Green
        $committed++
    }
}

Write-Host ""
Write-Host ("  Total commits: " + $committed) -ForegroundColor Cyan

# Step 3: Push to GitHub
Write-Host ""
Write-Host "[3/3] Pushing to GitHub..." -ForegroundColor Yellow
git push origin main --force

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Done! Check your GitHub profile." -ForegroundColor Green
Write-Host "  Green squares should appear now." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
