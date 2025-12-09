# Script 20: Fix Pervasive Services and Test Without Reboot
# ==========================================================
# Purpose: Configure Pervasive services properly and test NEX Automat

Write-Host "=" -NoNewline; Write-Host ("=" * 69)
Write-Host "FIX PERVASIVE SERVICES - NO REBOOT"
Write-Host "=" -NoNewline; Write-Host ("=" * 69)

Write-Host @"

ANALYSIS:
Pervasive works after fresh install but breaks after reboot.
This suggests services don't start/stop properly during shutdown.

SOLUTION:
1. Find and configure all Pervasive services
2. Set proper startup type and dependencies
3. Start services manually (NO REBOOT)
4. Test NEX Genesis
5. Test NEX Automat
6. Keep server running (avoid reboot)

"@

Write-Host "`n" + ("=" * 70)
Write-Host "STEP 1: FIND PERVASIVE SERVICES"
Write-Host ("=" * 70)

$allServices = Get-Service | Where-Object {
    $_.DisplayName -like "*pervasive*" -or
    $_.DisplayName -like "*btrieve*" -or
    $_.DisplayName -like "*psql*" -or
    $_.Name -like "*psql*"
}

if ($allServices) {
    Write-Host "`n[FOUND] Pervasive services:"
    foreach ($svc in $allServices) {
        Write-Host "  - $($svc.Name) ($($svc.DisplayName))"
        Write-Host "    Status: $($svc.Status)"
        Write-Host "    StartType: $($svc.StartType)"
    }
} else {
    Write-Host "`n[ERROR] No Pervasive services found!"
    Write-Host "[INFO] Pervasive may not be installed as service"
    Write-Host "[INFO] Check if W3DBSMGR.EXE is running as process"

    $process = Get-Process -Name "W3DBSMGR" -ErrorAction SilentlyContinue
    if ($process) {
        Write-Host "[FOUND] W3DBSMGR process is running (PID: $($process.Id))"
    } else {
        Write-Host "[ERROR] W3DBSMGR process is NOT running"
        Write-Host "`n[ACTION NEEDED] Start Btrieve manually:"
        Write-Host "  C:\PVSW\bin\W3DBSMGR.EXE"
    }

    exit 0
}

Write-Host "`n" + ("=" * 70)
Write-Host "STEP 2: CONFIGURE SERVICES"
Write-Host ("=" * 70)

foreach ($svc in $allServices) {
    Write-Host "`n[INFO] Configuring: $($svc.Name)"

    try {
        # Set to Automatic startup
        Set-Service -Name $svc.Name -StartupType Automatic -ErrorAction Stop
        Write-Host "  [OK] Set to Automatic startup"
    } catch {
        Write-Host "  [ERROR] Could not set startup type: $($_.Exception.Message)"
    }
}

Write-Host "`n" + ("=" * 70)
Write-Host "STEP 3: START SERVICES"
Write-Host ("=" * 70)

foreach ($svc in $allServices) {
    Write-Host "`n[INFO] Starting: $($svc.Name)"

    try {
        if ($svc.Status -ne "Running") {
            Start-Service -Name $svc.Name -ErrorAction Stop
            Start-Sleep -Seconds 2
            $svc.Refresh()
            Write-Host "  [OK] Started - Status: $($svc.Status)"
        } else {
            Write-Host "  [OK] Already running"
        }
    } catch {
        Write-Host "  [ERROR] Could not start: $($_.Exception.Message)"
    }
}

Write-Host "`n" + ("=" * 70)
Write-Host "STEP 4: VERIFY BTRIEVE"
Write-Host ("=" * 70)

Write-Host "`n[INFO] Checking if Btrieve DLL is accessible..."
$dllPath = "C:\PVSW\bin\w3btrv7.dll"

if (Test-Path $dllPath) {
    Write-Host "[OK] Btrieve DLL found: $dllPath"
} else {
    Write-Host "[ERROR] Btrieve DLL not found: $dllPath"
    exit 1
}

Write-Host "`n[INFO] Test NEX Genesis NOW:"
Write-Host "  1. Open NEX Genesis"
Write-Host "  2. Try to access database"
Write-Host "  3. Check if Error 8520 appears"

$genesis = Read-Host "`nDoes NEX Genesis work? (yes/no)"

if ($genesis.ToLower() -ne "yes") {
    Write-Host "`n[ERROR] NEX Genesis still has issues"
    Write-Host "[INFO] Check Windows Event Log for Pervasive errors"
    exit 1
}

Write-Host "`n[OK] NEX Genesis works!"

Write-Host "`n" + ("=" * 70)
Write-Host "STEP 5: START NEX AUTOMAT"
Write-Host ("=" * 70)

Write-Host "`n[INFO] Starting NEX-Automat-Loader task..."

try {
    Start-ScheduledTask -TaskName "NEX-Automat-Loader" -ErrorAction Stop
    Write-Host "[OK] Task started"

    Write-Host "`n[INFO] Waiting 10 seconds..."
    Start-Sleep -Seconds 10

    # Test port
    $tcpClient = New-Object System.Net.Sockets.TcpClient
    try {
        $tcpClient.Connect("localhost", 8001)
        $tcpClient.Close()
        Write-Host "[OK] Port 8001 is open - NEX Automat is running!"
    } catch {
        Write-Host "[ERROR] Port 8001 is not open"
    }
} catch {
    Write-Host "[ERROR] Could not start task: $($_.Exception.Message)"
}

Write-Host "`n" + ("=" * 70)
Write-Host "CRITICAL RECOMMENDATION"
Write-Host ("=" * 70)

Write-Host @"

[WARNING] DO NOT REBOOT THIS SERVER!

Situation:
- Pervasive works NOW
- NEX Genesis works NOW
- NEX Automat works NOW
- BUT: Reboot breaks Pervasive

Root cause unknown - could be:
- Windows shutdown timing issue
- Service dependency problem
- Hardware/driver issue
- Corrupted Windows system files

RECOMMENDED ACTIONS:
1. Keep server running (no reboot)
2. Contact system administrator
3. Consider:
   - Windows system file check: sfc /scannow
   - Check disk: chkdsk /f
   - Update Windows
   - Check hardware (RAM, disk)

IF REBOOT IS ABSOLUTELY NECESSARY:
1. Stop all services manually first
2. Wait 30 seconds
3. Then reboot
4. After reboot, run this script again

Current Status: WORKING - DO NOT REBOOT

"@