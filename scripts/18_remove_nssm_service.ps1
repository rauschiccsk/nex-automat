# Script 18: Remove NSSM Service
# ================================
# Purpose: Remove old NSSM service that doesn't work

Write-Host "=" -NoNewline; Write-Host ("=" * 69)
Write-Host "REMOVE NSSM SERVICE"
Write-Host "=" -NoNewline; Write-Host ("=" * 69)

$serviceName = "NEX-Automat-Loader"

# Check if service exists
$service = Get-Service -Name $serviceName -ErrorAction SilentlyContinue

if (-not $service) {
    Write-Host "`n[INFO] Service '$serviceName' not found - already removed"
    exit 0
}

Write-Host "`n[INFO] Found service: $serviceName"
Write-Host "[INFO] Status: $($service.Status)"

# Stop service if running
if ($service.Status -eq "Running" -or $service.Status -eq "Paused") {
    Write-Host "`n[INFO] Stopping service..."
    try {
        Stop-Service -Name $serviceName -Force -ErrorAction Stop
        Start-Sleep -Seconds 2
        Write-Host "[OK] Service stopped"
    } catch {
        Write-Host "[WARNING] Could not stop service: $($_.Exception.Message)"
    }
}

# Remove service using sc.exe
Write-Host "`n[INFO] Removing service with sc.exe..."
$result = sc.exe delete $serviceName 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Service removed successfully"
} else {
    Write-Host "[ERROR] Failed to remove service: $result"
    exit 1
}

Write-Host "`n" + ("=" * 70)
Write-Host "VERIFICATION"
Write-Host ("=" * 70)

Start-Sleep -Seconds 2

$serviceCheck = Get-Service -Name $serviceName -ErrorAction SilentlyContinue

if (-not $serviceCheck) {
    Write-Host "`n[OK] Service successfully removed"
} else {
    Write-Host "`n[WARNING] Service still exists - may require reboot"
}

Write-Host "`n[SUCCESS] NSSM service cleanup complete"
Write-Host "[INFO] NEX Automat now runs via Task Scheduler"