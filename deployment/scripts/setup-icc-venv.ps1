# setup-icc-venv.ps1
# ICC VM - Virtual Environment Setup Script
# Usage: .\setup-icc-venv.ps1

$ErrorActionPreference = "Stop"

# Configuration
$PROJECT_ROOT = "C:\ICC\nex-automat"
$PYTHON_64 = "C:\Python311-64\python.exe"
$PYTHON_32 = "C:\Python311-32\python.exe"

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  ICC - Virtual Environment Setup" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check current directory
Write-Host "[1/6] Checking working directory..." -ForegroundColor Yellow

$currentPath = (Get-Location).Path
if ($currentPath -ne $PROJECT_ROOT) {
    Write-Host "  ERROR: Must run from $PROJECT_ROOT" -ForegroundColor Red
    Write-Host "  Current: $currentPath" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Run: cd $PROJECT_ROOT" -ForegroundColor Yellow
    exit 1
}
Write-Host "  OK: $currentPath" -ForegroundColor Green

# Step 2: Check Python installations
Write-Host "[2/6] Checking Python installations..." -ForegroundColor Yellow

if (-not (Test-Path $PYTHON_64)) {
    Write-Host "  ERROR: Python 64-bit not found at $PYTHON_64" -ForegroundColor Red
    exit 1
}
$py64Version = & $PYTHON_64 --version 2>&1
Write-Host "  64-bit: $py64Version" -ForegroundColor Green

if (-not (Test-Path $PYTHON_32)) {
    Write-Host "  ERROR: Python 32-bit not found at $PYTHON_32" -ForegroundColor Red
    exit 1
}
$py32Version = & $PYTHON_32 --version 2>&1
Write-Host "  32-bit: $py32Version" -ForegroundColor Green

# Step 3: Create 64-bit venv
Write-Host "[3/6] Creating 64-bit virtual environment..." -ForegroundColor Yellow

if (Test-Path "venv") {
    Write-Host "  Removing existing venv..." -ForegroundColor Gray
    Remove-Item -Recurse -Force "venv"
}

try {
    & $PYTHON_64 -m venv venv
    Write-Host "  Created: venv\" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Failed to create venv" -ForegroundColor Red
    Write-Host "  $_" -ForegroundColor Red
    exit 1
}

# Step 4: Create 32-bit venv
Write-Host "[4/6] Creating 32-bit virtual environment..." -ForegroundColor Yellow

if (Test-Path "venv32") {
    Write-Host "  Removing existing venv32..." -ForegroundColor Gray
    Remove-Item -Recurse -Force "venv32"
}

try {
    & $PYTHON_32 -m venv venv32
    Write-Host "  Created: venv32\" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Failed to create venv32" -ForegroundColor Red
    Write-Host "  $_" -ForegroundColor Red
    exit 1
}

# Step 5: Install 64-bit requirements
Write-Host "[5/6] Installing 64-bit requirements..." -ForegroundColor Yellow

$venvPip = ".\venv\Scripts\pip.exe"
$requirementsFile = "requirements.txt"

if (-not (Test-Path $requirementsFile)) {
    Write-Host "  WARNING: $requirementsFile not found, skipping..." -ForegroundColor Yellow
} else {
    try {
        Write-Host "  Installing from $requirementsFile..." -ForegroundColor Gray
        & $venvPip install --upgrade pip -q
        & $venvPip install -r $requirementsFile
        if ($LASTEXITCODE -ne 0) { throw "pip install failed" }
        Write-Host "  Installed 64-bit dependencies" -ForegroundColor Green
    } catch {
        Write-Host "  ERROR: Failed to install 64-bit requirements" -ForegroundColor Red
        Write-Host "  $_" -ForegroundColor Red
        exit 1
    }
}

# Step 6: Install 32-bit requirements (supplier-invoice-loader)
Write-Host "[6/6] Installing 32-bit requirements..." -ForegroundColor Yellow

$venv32Pip = ".\venv32\Scripts\pip.exe"
$requirements32File = "apps\supplier-invoice-loader\requirements.txt"

if (-not (Test-Path $requirements32File)) {
    Write-Host "  WARNING: $requirements32File not found, skipping..." -ForegroundColor Yellow
} else {
    try {
        Write-Host "  Installing from $requirements32File..." -ForegroundColor Gray
        & $venv32Pip install --upgrade pip -q
        & $venv32Pip install -r $requirements32File
        if ($LASTEXITCODE -ne 0) { throw "pip install failed" }
        Write-Host "  Installed 32-bit dependencies" -ForegroundColor Green
    } catch {
        Write-Host "  ERROR: Failed to install 32-bit requirements" -ForegroundColor Red
        Write-Host "  $_" -ForegroundColor Red
        exit 1
    }
}

# Success
Write-Host ""
Write-Host "=============================================" -ForegroundColor Green
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Virtual environments created:" -ForegroundColor White
Write-Host "    venv\    - 64-bit (general purpose)" -ForegroundColor Gray
Write-Host "    venv32\  - 32-bit (Btrieve/NEX Genesis)" -ForegroundColor Gray
Write-Host ""
Write-Host "  Activation:" -ForegroundColor White
Write-Host "    64-bit: .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "    32-bit: .\venv32\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host ""
