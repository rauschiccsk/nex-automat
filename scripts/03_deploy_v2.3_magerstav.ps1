# ============================================================================
# Deployment Script v2.3 - Magerstav
# Deploy nex-automat v2.3 with nex-shared migration
# ============================================================================

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "DEPLOYMENT v2.3 - MAGERSTAV" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan

$DeploymentPath = "C:\Deployment\nex-automat"
$ServiceName = "NEXAutomat"

# ============================================================================
# 1. CHECK PREREQUISITES
# ============================================================================
Write-Host "`n[1/6] Checking prerequisites..." -ForegroundColor Yellow

if (-not (Test-Path $DeploymentPath)) {
    Write-Host "ERROR: Deployment path not found: $DeploymentPath" -ForegroundColor Red
    exit 1
}

# ============================================================================
# 2. STOP SERVICE
# ============================================================================
Write-Host "`n[2/6] Stopping service: $ServiceName..." -ForegroundColor Yellow

$service = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
if ($service) {
    if ($service.Status -eq "Running") {
        Stop-Service -Name $ServiceName -Force
        Start-Sleep -Seconds 3
        Write-Host "   Service stopped" -ForegroundColor Green
    } else {
        Write-Host "   Service already stopped" -ForegroundColor Green
    }
} else {
    Write-Host "   WARNING: Service not found" -ForegroundColor Yellow
}

# ============================================================================
# 3. PULL LATEST CODE
# ============================================================================
Write-Host "`n[3/6] Pulling latest code from main..." -ForegroundColor Yellow

Set-Location $DeploymentPath

# Checkout main and pull
git checkout main
git pull origin main

$currentTag = git describe --tags --abbrev=0
Write-Host "   Current version: $currentTag" -ForegroundColor Green

# ============================================================================
# 4. REINSTALL NEX-SHARED
# ============================================================================
Write-Host "`n[4/6] Reinstalling nex-shared package..." -ForegroundColor Yellow

Set-Location "$DeploymentPath\packages\nex-shared"

# Activate venv (assuming venv32 in deployment)
& "$DeploymentPath\venv32\Scripts\Activate.ps1"

# Reinstall nex-shared
pip install -e .

if ($LASTEXITCODE -eq 0) {
    Write-Host "   nex-shared installed successfully" -ForegroundColor Green
} else {
    Write-Host "   ERROR: Failed to install nex-shared" -ForegroundColor Red
    exit 1
}

# ============================================================================
# 5. VERIFY INSTALLATION
# ============================================================================
Write-Host "`n[5/6] Verifying installation..." -ForegroundColor Yellow

Set-Location "$DeploymentPath\apps\supplier-invoice-loader"

# Test import
python -c "from nex_shared.utils import clean_string; from nex_shared.database import PostgresStagingClient; print('Imports OK')"

if ($LASTEXITCODE -eq 0) {
    Write-Host "   Imports verified successfully" -ForegroundColor Green
} else {
    Write-Host "   ERROR: Import verification failed" -ForegroundColor Red
    exit 1
}

# ============================================================================
# 6. START SERVICE
# ============================================================================
Write-Host "`n[6/6] Starting service: $ServiceName..." -ForegroundColor Yellow

Start-Service -Name $ServiceName
Start-Sleep -Seconds 5

$service = Get-Service -Name $ServiceName
if ($service.Status -eq "Running") {
    Write-Host "   Service started successfully" -ForegroundColor Green
} else {
    Write-Host "   ERROR: Service failed to start" -ForegroundColor Red
    Write-Host "   Check logs in: $DeploymentPath\apps\supplier-invoice-loader\logs" -ForegroundColor Yellow
    exit 1
}

# ============================================================================
# 7. HEALTH CHECK
# ============================================================================
Write-Host "`n[7/7] Testing API health..." -ForegroundColor Yellow

Start-Sleep -Seconds 3

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "   API health check: OK" -ForegroundColor Green
        Write-Host "   Response: $($response.Content)" -ForegroundColor Gray
    } else {
        Write-Host "   WARNING: Unexpected status code: $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ERROR: API health check failed" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)" -ForegroundColor Red
}

# ============================================================================
# SUMMARY
# ============================================================================
Write-Host "`n" + "=" * 80 -ForegroundColor Cyan
Write-Host "DEPLOYMENT COMPLETE" -ForegroundColor Green
Write-Host "=" * 80 -ForegroundColor Cyan

Write-Host "`nDeployment Details:" -ForegroundColor White
Write-Host "  Version: v2.3" -ForegroundColor Gray
Write-Host "  Location: $DeploymentPath" -ForegroundColor Gray
Write-Host "  Service: $ServiceName (Running)" -ForegroundColor Gray
Write-Host "  API: http://localhost:8000" -ForegroundColor Gray
Write-Host "  Health: http://localhost:8000/health" -ForegroundColor Gray

Write-Host "`nChanges in v2.3:" -ForegroundColor White
Write-Host "  - Migrated invoice-shared to nex-shared" -ForegroundColor Gray
Write-Host "  - Added clean_string to nex-shared/utils" -ForegroundColor Gray
Write-Host "  - Added PostgresStagingClient to nex-shared/database" -ForegroundColor Gray
Write-Host "  - Updated supplier-invoice-loader imports" -ForegroundColor Gray

Write-Host "`n" + "=" * 80 -ForegroundColor Cyan