# OptimusDB Python Client - Quick Push to GitHub
# Usage: .\gitPush.ps1
# Usage: .\gitPush.ps1 -m "Your commit message"

param(
    [Alias("m")]
    [string]$Message
)

$ErrorActionPreference = "Stop"
$BRANCH = "main"

# Default commit message with timestamp
if (-not $Message) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    $Message = "Update OptimusDB client - $timestamp"
}

Write-Host ""
Write-Host "  optimusPy - Git Push" -ForegroundColor Cyan
Write-Host "  ────────────────────" -ForegroundColor DarkGray

# Stage all changes
git add .

# Check if there's anything to commit
$status = git status --porcelain
if (-not $status) {
    # Check if there are unpushed commits
    $unpushed = git log "origin/$BRANCH..$BRANCH" --oneline 2>$null
    if ($unpushed) {
        Write-Host "  No new changes, but $($unpushed.Count) unpushed commit(s)" -ForegroundColor Yellow
    } else {
        Write-Host "  Nothing to commit or push — working tree clean" -ForegroundColor Green
        Write-Host ""
        exit 0
    }
} else {
    $fileCount = ($status | Measure-Object).Count
    Write-Host ""
    $status | ForEach-Object { Write-Host "    $_" -ForegroundColor White }
    Write-Host ""

    # Commit
    git commit -m "$Message" | Out-Null
    Write-Host "  Committed ($fileCount file(s)): $Message" -ForegroundColor Green
}

# Push
Write-Host "  Pushing to origin/$BRANCH..." -ForegroundColor Yellow
try {
    git push -u origin $BRANCH 2>&1 | Out-Null
    Write-Host "  Pushed successfully" -ForegroundColor Green
    Write-Host ""
    Write-Host "  https://github.com/georgeGeorgakakos/optimusPy" -ForegroundColor DarkGray
    Write-Host ""
} catch {
    Write-Host ""
    Write-Host "  Push failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Try manually:" -ForegroundColor Yellow
    Write-Host "    git pull origin $BRANCH --rebase" -ForegroundColor White
    Write-Host "    git push -u origin $BRANCH" -ForegroundColor White
    Write-Host ""
    exit 1
}