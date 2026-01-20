# install-services-andros.ps1
# ANDROS VM - Windows Services Installation via NSSM
# Run as Administrator!
# Usage: .\install-services-andros.ps1

$ErrorActionPreference = "Stop"

# Configuration
$PROJECT_ROOT = "C:\ANDROS\nex-automat"
$NSSM = "$PROJECT_ROOT\tools\nssm\win64\nssm.exe"
$PYTHON_64 = "$PROJECT_ROOT\venv\Scripts\python.exe"
$PYTHON_32 = "$PROJECT_ROOT\venv32\Scripts\python.exe"
$LOG_DIR = "$PROJECT_ROOT\logs\services"

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  ANDROS - Windows Services Installation" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Check Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    exit 1
}

# Check NSSM
if (-not (Test-Path $NSSM)) {
    Write-Host "ERROR: NSSM not found at $NSSM" -ForegroundColor Red
    exit 1
}
Write-Host "NSSM: $NSSM" -ForegroundColor Green

# Check Python
if (-not (Test-Path $PYTHON_64)) {
    Write-Host "ERROR: Python 64-bit venv not found at $PYTHON_64" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path $PYTHON_32)) {
    Write-Host "ERROR: Python 32-bit venv not found at $PYTHON_32" -ForegroundColor Red
    exit 1
}
Write-Host "Python 64-bit: $PYTHON_64" -ForegroundColor Green
Write-Host "Python 32-bit: $PYTHON_32" -ForegroundColor Green

# Create log directory
if (-not (Test-Path $LOG_DIR)) {
    New-Item -ItemType Directory -Path $LOG_DIR -Force | Out-Null
    Write-Host "Created log directory: $LOG_DIR" -ForegroundColor Green
}

Write-Host ""

# Function to install service
function Install-NSSMService {
    param(
        [string]$ServiceName,
        [string]$Python,
        [string]$Arguments,
        [string]$WorkDir
    )

    Write-Host "Installing: $ServiceName" -ForegroundColor Yellow

    # Remove if exists
    $existingService = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
    if ($existingService) {
        Write-Host "  Removing existing service..." -ForegroundColor Gray
        & $NSSM stop $ServiceName 2>$null
        & $NSSM remove $ServiceName confirm
    }

    # Install service
    Write-Host "  Python: $Python" -ForegroundColor Gray
    Write-Host "  Args: $Arguments" -ForegroundColor Gray
    Write-Host "  WorkDir: $WorkDir" -ForegroundColor Gray

    & $NSSM install $ServiceName $Python
    if ($LASTEXITCODE -ne 0) { throw "Failed to install $ServiceName" }

    # Configure service
    & $NSSM set $ServiceName AppParameters $Arguments
    & $NSSM set $ServiceName AppDirectory $WorkDir
    & $NSSM set $ServiceName Start SERVICE_AUTO_START
    & $NSSM set $ServiceName AppStdout "$LOG_DIR\$ServiceName-stdout.log"
    & $NSSM set $ServiceName AppStderr "$LOG_DIR\$ServiceName-stderr.log"
    & $NSSM set $ServiceName AppStdoutCreationDisposition 4
    & $NSSM set $ServiceName AppStderrCreationDisposition 4
    & $NSSM set $ServiceName AppRotateFiles 1
    & $NSSM set $ServiceName AppRotateBytes 10485760

    Write-Host "  Installed: $ServiceName" -ForegroundColor Green
    Write-Host ""
}

# Service 1: NEX-Invoice-Worker-ANDROS
Install-NSSMService `
    -ServiceName "NEX-Invoice-Worker-ANDROS" `
    -Python $PYTHON_64 `
    -Arguments "-m workers.main_worker" `
    -WorkDir "$PROJECT_ROOT\apps\supplier-invoice-worker"

# Service 2: NEX-Polling-Scheduler-ANDROS
Install-NSSMService `
    -ServiceName "NEX-Polling-Scheduler-ANDROS" `
    -Python $PYTHON_64 `
    -Arguments "-m scheduler.polling_scheduler" `
    -WorkDir "$PROJECT_ROOT\apps\supplier-invoice-worker"

# Service 3: NEX-Automat-Loader-ANDROS
Install-NSSMService `
    -ServiceName "NEX-Automat-Loader-ANDROS" `
    -Python $PYTHON_32 `
    -Arguments "-m uvicorn main:app --host 0.0.0.0 --port 8001" `
    -WorkDir "$PROJECT_ROOT\apps\supplier-invoice-loader"

# Summary
Write-Host "=============================================" -ForegroundColor Green
Write-Host "  Installation Complete!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Services installed:" -ForegroundColor White
Write-Host "    - NEX-Invoice-Worker-ANDROS" -ForegroundColor Gray
Write-Host "    - NEX-Polling-Scheduler-ANDROS" -ForegroundColor Gray
Write-Host "    - NEX-Automat-Loader-ANDROS" -ForegroundColor Gray
Write-Host ""
Write-Host "  Log directory: $LOG_DIR" -ForegroundColor White
Write-Host ""
Write-Host "  Commands:" -ForegroundColor White
Write-Host "    Start all:  Get-Service NEX-*-ANDROS | Start-Service" -ForegroundColor Gray
Write-Host "    Stop all:   Get-Service NEX-*-ANDROS | Stop-Service" -ForegroundColor Gray
Write-Host "    Status:     Get-Service NEX-*-ANDROS" -ForegroundColor Gray
Write-Host ""
