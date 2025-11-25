# Script: create_branches.ps1
# Purpose: Create branching strategy for NEX Automat v2.0 production
# Branches: main (production), develop (features), hotfix_v2.0 (bugfixes)

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "NEX Automat v2.0 - Branching Strategy" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (!(Test-Path ".git")) {
    Write-Host "ERROR: Not in a git repository!" -ForegroundColor Red
    exit 1
}

Write-Host "Step 1: Updating main branch..." -ForegroundColor Yellow
git checkout main
git pull origin main

Write-Host ""
Write-Host "Step 2: Creating tag v2.0.0..." -ForegroundColor Yellow
git tag v2.0.0
Write-Host "✓ Tag v2.0.0 created" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Creating develop branch..." -ForegroundColor Yellow
git checkout -b develop
git push -u origin develop
Write-Host "✓ Branch 'develop' created and pushed" -ForegroundColor Green

Write-Host ""
Write-Host "Step 4: Creating hotfix_v2.0 branch..." -ForegroundColor Yellow
git checkout main
git checkout -b hotfix_v2.0
git push -u origin hotfix_v2.0
Write-Host "✓ Branch 'hotfix_v2.0' created and pushed" -ForegroundColor Green

Write-Host ""
Write-Host "Step 5: Pushing tags..." -ForegroundColor Yellow
git push --tags
Write-Host "✓ Tags pushed" -ForegroundColor Green

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "SUCCESS: Branching strategy created!" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Branches created:" -ForegroundColor White
Write-Host "  - main          (production, tagged v2.0.0)" -ForegroundColor White
Write-Host "  - develop       (feature development)" -ForegroundColor White
Write-Host "  - hotfix_v2.0   (bug fixes for v2.0.x)" -ForegroundColor White
Write-Host ""
Write-Host "Current branch: hotfix_v2.0" -ForegroundColor White
Write-Host ""
Write-Host "Workflow:" -ForegroundColor White
Write-Host "  - New features  → develop → main (at release)" -ForegroundColor White
Write-Host "  - Bug fixes     → hotfix_v2.0 → main (immediate) + merge to develop" -ForegroundColor White
Write-Host ""