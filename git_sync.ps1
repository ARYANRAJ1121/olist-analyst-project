param(
    [string]$Email = $(Read-Host "Enter your exact GitHub email address (this fixes the green squares)"),
    [string]$Name = "Aryan Raj"
)

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "🚀 Starting Git Configuration & History Rewrite" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# 1. Set Git Configuration
Write-Host "`n[1/4] Setting Git Identity..." -ForegroundColor Yellow
git config --global user.email "$Email"
git config --global user.name "$Name"
Write-Host "✅ Git identity set to: $Name ($Email)" -ForegroundColor Green

# 2. Reset the previous bulk commit but KEEP the changes
Write-Host "`n[2/4] Undoing the previous bulk commit..." -ForegroundColor Yellow
git reset --soft HEAD~1
Write-Host "✅ Previous commit undone. Changes are ready to be re-committed." -ForegroundColor Green

# 3. Commit files individually with specific messages
Write-Host "`n[3/4] Committing files individually..." -ForegroundColor Yellow

# Unstage everything first
git reset HEAD .

# Commit SQL files
$sqlFiles = Get-ChildItem -Path "sql" -Filter "*.sql"
foreach ($file in $sqlFiles) {
    git add "sql/$($file.Name)"
    git commit -m "feat(sql): add block annotations to $($file.Name)"
}

# Commit RAG Pipeline modules
$ragFiles = Get-ChildItem -Path "rag" -Filter "*.py"
foreach ($file in $ragFiles) {
    git add "rag/$($file.Name)"
    git commit -m "feat(rag): implement $($file.Name) for AI assistant"
}

# Commit App Dashboard
git add app.py
git commit -m "feat(dashboard): integrate Ask AI chatbot interface into app.py"

# Commit Requirements
if (Test-Path "requirements_rag.txt") {
    git add requirements_rag.txt
    git commit -m "chore(deps): add requirements_rag.txt for AI pipeline"
}

# Commit Setup Scripts
$scriptFiles = Get-ChildItem -Path "scripts" -Filter "*.py"
foreach ($file in $scriptFiles) {
    git add "scripts/$($file.Name)"
    git commit -m "feat(scripts): update $($file.Name) configuration"
}

# Commit the new README
git add README.md
git commit -m "docs(readme): rewrite README with ultimate business and technical structure"

# Commit any remaining files
git add .
$status = git status --porcelain
if ($status) {
    git commit -m "chore: update miscellaneous project files"
}

Write-Host "✅ All files committed individually!" -ForegroundColor Green

# 4. Force Push to GitHub
Write-Host "`n[4/4] Pushing to GitHub (Force push to overwrite history)..." -ForegroundColor Yellow
git push --force origin main

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "🎉 SUCCESS! Your GitHub profile should now show the green squares." -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
