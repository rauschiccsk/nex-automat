# Script 15: Restart Pervasive PSQL Services
# ============================================
# Purpose: Restart Pervasive services after Winsock reset

Write-Host "=" -NoNewline; Write-Host ("=" * 69)
Write-Host "RESTART PERVASIVE PSQL SERVICES"
Write-Host "=" -NoNewline; Write-Host ("=" * 69)

# Common Pervasive service names
$pervasiveServices = @(
    "PSQL",
    "PervasiveSQL",
    "Btrieve",
    "SRDE",
    "W3DBSMGR"
)

Write-Host "`n[INFO] Searching for Pervasive services..."

$foundServices = @()
foreach ($serviceName in $pervasiveServices) {
    $service = Get-Service -Name "*$serviceName*" -ErrorAction SilentlyContinue
    if ($service) {
        $foundServices += $service
        Write-Host "[FOUND] $($service.Name) - Status: $($service.Status)"
    }
}

if ($foundServices.Count -eq 0) {
    Write-Host "`n[WARNING] No Pervasive services found"
    Write-Host "[INFO] Checking for all services with 'pervasive' or 'btrieve'..."

    $allServices = Get-Service | Where-Object {
        $_.DisplayName -like "*pervasive*" -or
        $_.DisplayName -like "*btrieve*" -or
        $_.DisplayName -like "*psql*"
    }

    if ($allServices) {
        Write-Host "`n[FOUND] Related services:"
        foreach ($svc in $allServices) {
            Write-Host "  - $($svc.Name) ($($svc.DisplayName)) - Status: $($svc.Status)"
            $foundServices += $svc
        }
    } else {
        Write-Host "[ERROR] No Pervasive/Btrieve services found on this system"
        exit 1
    }
}

Write-Host "`n" + ("=" * 70)
Write-Host "RESTARTING SERVICES"
Write-Host ("=" * 70)

foreach ($service in $foundServices) {
    Write-Host "`n[INFO] Processing: $($service.Name)"

    try {
        if ($service.Status -eq "Running") {
            Write-Host "  Stopping service..."
            Stop-Service -Name $service.Name -Force -ErrorAction Stop
            Start-Sleep -Seconds 2
            Write-Host "  [OK] Stopped"
        }

        Write-Host "  Starting service..."
        Start-Service -Name $service.Name -ErrorAction Stop
        Start-Sleep -Seconds 2

        $service.Refresh()
        Write-Host "  [OK] Started - Status: $($service.Status)"

    } catch {
        Write-Host "  [ERROR] Failed: $($_.Exception.Message)"
    }
}

Write-Host "`n" + ("=" * 70)
Write-Host "VERIFICATION"
Write-Host ("=" * 70)

Write-Host "`n[INFO] Current service status:"
foreach ($service in $foundServices) {
    $service.Refresh()
    $status = if ($service.Status -eq "Running") { "[OK]" } else { "[ERROR]" }
    Write-Host "$status $($service.Name): $($service.Status)"
}

Write-Host "`n" + ("=" * 70)
Write-Host "TEST BTRIEVE CONNECTION"
Write-Host ("=" * 70)

Write-Host "`n[INFO] Testing if Btrieve DLL is accessible..."

$dllPath = "C:\PVSW\bin\w3btrv7.dll"
if (Test-Path $dllPath) {
    Write-Host "[OK] Btrieve DLL found: $dllPath"

    Write-Host "`n[INFO] You can now test NEX Automat service:"
    Write-Host "  1. Start NEX-Automat-Loader service:"
    Write-Host "     net start `"NEX-Automat-Loader`""
    Write-Host "`n  2. Check if it stays running:"
    Write-Host "     sc query `"NEX-Automat-Loader`""
    Write-Host "`n  3. Test API endpoint:"
    Write-Host "     http://localhost:8001/health"
} else {
    Write-Host "[ERROR] Btrieve DLL not found: $dllPath"
}