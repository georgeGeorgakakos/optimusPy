# OptimusDB Python Client - Push ALL Files to GitHub
# Single comprehensive script - pushes everything in current directory
# Repository: https://github.com/georgeGeorgakakos/optimusPy

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  OptimusDB - Push ALL Files to GitHub" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$REPO_URL = "https://github.com/georgeGeorgakakos/optimusPy.git"
$BRANCH = "main"

# Check if git is installed
Write-Host "[1/7] Checking Git installation..." -ForegroundColor Yellow
try {
    $gitVersion = git --version 2>&1
    Write-Host "      ✓ Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "      ✗ Git is not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "Or install GitHub Desktop: https://desktop.github.com/" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Initialize git repository if needed
Write-Host ""
Write-Host "[2/7] Checking Git repository..." -ForegroundColor Yellow

if (-not (Test-Path ".git")) {
    Write-Host "      Git repository not found. Initializing..." -ForegroundColor Yellow
    git init
    git remote add origin $REPO_URL
    Write-Host "      ✓ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "      ✓ Git repository exists" -ForegroundColor Green

    # Check if remote exists
    $remoteUrl = git remote get-url origin 2>$null
    if ($remoteUrl -ne $REPO_URL) {
        Write-Host "      Updating remote URL..." -ForegroundColor Yellow
        git remote remove origin 2>$null
        git remote add origin $REPO_URL
        Write-Host "      ✓ Remote URL updated" -ForegroundColor Green
    }
}

# Configure git user if needed
Write-Host ""
Write-Host "[3/7] Checking Git configuration..." -ForegroundColor Yellow

$userName = git config user.name 2>$null
$userEmail = git config user.email 2>$null

if (-not $userName) {
    Write-Host "      Git user name not configured" -ForegroundColor Yellow
    $inputName = Read-Host "      Enter your Git user name (e.g., George Georgakakos)"
    git config user.name "$inputName"
    Write-Host "      ✓ User name configured: $inputName" -ForegroundColor Green
} else {
    Write-Host "      ✓ User name: $userName" -ForegroundColor Green
}

if (-not $userEmail) {
    Write-Host "      Git email not configured" -ForegroundColor Yellow
    $inputEmail = Read-Host "      Enter your Git email"
    git config user.email "$inputEmail"
    Write-Host "      ✓ Email configured: $inputEmail" -ForegroundColor Green
} else {
    Write-Host "      ✓ Email: $userEmail" -ForegroundColor Green
}

# Switch to main branch
Write-Host ""
Write-Host "[4/7] Setting up branch..." -ForegroundColor Yellow

$currentBranch = git rev-parse --abbrev-ref HEAD 2>$null
if ($currentBranch -ne $BRANCH) {
    try {
        git checkout $BRANCH 2>$null
        Write-Host "      ✓ Switched to $BRANCH branch" -ForegroundColor Green
    } catch {
        git checkout -b $BRANCH 2>$null
        Write-Host "      ✓ Created and switched to $BRANCH branch" -ForegroundColor Green
    }
} else {
    Write-Host "      ✓ Already on $BRANCH branch" -ForegroundColor Green
}

# Stage ALL files
Write-Host ""
Write-Host "[5/7] Staging ALL files..." -ForegroundColor Yellow

# Create .gitignore if it doesn't exist
if (-not (Test-Path ".gitignore")) {
    Write-Host "      Creating .gitignore..." -ForegroundColor Yellow
    @"
# Python
__pycache__/
*.py[cod]
*`$py.class
*.so
.Python
build/
dist/
*.egg-info/
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*~
.DS_Store

# Logs
*.log
logs/

# OS
Thumbs.db

# Backup
*.bak
*.backup
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
    Write-Host "      ✓ Created .gitignore" -ForegroundColor Green
}

git add .

# Show what will be committed
Write-Host ""
Write-Host "      Files to be committed:" -ForegroundColor Cyan
$status = git status --short
if ($status) {
    $status | ForEach-Object { Write-Host "        $_" -ForegroundColor White }
    $fileCount = ($status | Measure-Object).Count
    Write-Host ""
    Write-Host "      ✓ Staged $fileCount file(s)" -ForegroundColor Green
} else {
    Write-Host "        (no changes detected)" -ForegroundColor Yellow
}

# Commit changes
Write-Host ""
Write-Host "[6/7] Committing changes..." -ForegroundColor Yellow

if ($status) {
    Write-Host "      Enter commit message (or press Enter for default):" -ForegroundColor Cyan
    $commitMessage = Read-Host "      "

    if ([string]::IsNullOrWhiteSpace($commitMessage)) {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        $commitMessage = "Update OptimusDB Python Client - $timestamp"
    }

    try {
        git commit -m "$commitMessage"
        Write-Host "      ✓ Changes committed: $commitMessage" -ForegroundColor Green
    } catch {
        Write-Host "      ✗ Commit failed" -ForegroundColor Red
        Write-Host "      Error: $_" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "      ⚠ No changes to commit (working tree clean)" -ForegroundColor Yellow
    Write-Host ""

    $pushAnyway = Read-Host "      Push anyway? (y/n)"
    if ($pushAnyway -ne "y") {
        Write-Host ""
        Write-Host "Cancelled by user" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 0
    }
}

# Push to GitHub
Write-Host ""
Write-Host "[7/7] Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "      Repository: $REPO_URL" -ForegroundColor Cyan
Write-Host "      Branch: $BRANCH" -ForegroundColor Cyan
Write-Host ""

try {
    # Try to pull first (in case of remote changes)
    Write-Host "      Checking for remote changes..." -ForegroundColor Yellow
    git pull origin $BRANCH --rebase 2>$null

    # Push
    Write-Host "      Pushing to remote..." -ForegroundColor Yellow
    git push -u origin $BRANCH

    Write-Host ""
    Write-Host "============================================" -ForegroundColor Green
    Write-Host "  ✓ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Repository URL:" -ForegroundColor Cyan
    Write-Host "https://github.com/georgeGeorgakakos/optimusPy" -ForegroundColor White
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Visit the URL above to view your repository" -ForegroundColor White
    Write-Host "  2. Verify all files are present" -ForegroundColor White
    Write-Host "  3. Add repository description in Settings" -ForegroundColor White
    Write-Host "  4. Share with your team!" -ForegroundColor White
    Write-Host ""

} catch {
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Red
    Write-Host "  ✗ Push failed!" -ForegroundColor Red
    Write-Host "============================================" -ForegroundColor Red
    Write-Host ""

    $errorMessage = $_.Exception.Message

    # Check for common errors and provide solutions
    if ($errorMessage -like "*authentication*" -or $errorMessage -like "*403*" -or $errorMessage -like "*401*") {
        Write-Host "Authentication Failed!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Solutions:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Option 1 - GitHub Desktop (EASIEST):" -ForegroundColor Cyan
        Write-Host "  1. Install GitHub Desktop: https://desktop.github.com/" -ForegroundColor White
        Write-Host "  2. Sign in to your GitHub account" -ForegroundColor White
        Write-Host "  3. Run this script again" -ForegroundColor White
        Write-Host ""
        Write-Host "Option 2 - Personal Access Token:" -ForegroundColor Cyan
        Write-Host "  1. Go to: https://github.com/settings/tokens" -ForegroundColor White
        Write-Host "  2. Click 'Generate new token' -> 'Classic'" -ForegroundColor White
        Write-Host "  3. Select scope: 'repo' (full control)" -ForegroundColor White
        Write-Host "  4. Generate and copy the token" -ForegroundColor White
        Write-Host "  5. Use token as password when Git asks" -ForegroundColor White
        Write-Host ""
        Write-Host "Option 3 - Configure Git Credentials:" -ForegroundColor Cyan
        Write-Host "  git config --global credential.helper wincred" -ForegroundColor White
        Write-Host ""

    } elseif ($errorMessage -like "*repository not found*" -or $errorMessage -like "*404*") {
        Write-Host "Repository Not Found!" -ForegroundColor Red
        Write-Host ""
        Write-Host "The repository doesn't exist yet. Create it:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  1. Go to: https://github.com/new" -ForegroundColor White
        Write-Host "  2. Repository name: optimusPy" -ForegroundColor White
        Write-Host "  3. Description: OptimusDB Python Client" -ForegroundColor White
        Write-Host "  4. Choose Public or Private" -ForegroundColor White
        Write-Host "  5. DON'T add README, .gitignore, or license" -ForegroundColor White
        Write-Host "  6. Click 'Create repository'" -ForegroundColor White
        Write-Host "  7. Run this script again" -ForegroundColor White
        Write-Host ""

    } elseif ($errorMessage -like "*rejected*" -or $errorMessage -like "*non-fast-forward*") {
        Write-Host "Push Rejected - Remote has changes!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Solution:" -ForegroundColor Yellow
        Write-Host "  git pull origin $BRANCH --rebase" -ForegroundColor White
        Write-Host "  Then run this script again" -ForegroundColor White
        Write-Host ""

    } else {
        Write-Host "Error details:" -ForegroundColor Red
        Write-Host $errorMessage -ForegroundColor White
        Write-Host ""
        Write-Host "General solutions:" -ForegroundColor Yellow
        Write-Host "  1. Check your internet connection" -ForegroundColor White
        Write-Host "  2. Verify repository exists: https://github.com/georgeGeorgakakos/optimusPy" -ForegroundColor White
        Write-Host "  3. Check Git configuration: git config --list" -ForegroundColor White
        Write-Host "  4. Try using GitHub Desktop: https://desktop.github.com/" -ForegroundColor White
        Write-Host ""
    }

    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Read-Host "Press Enter to exit"