# Script 19: Restore Winsock from Backup (EMERGENCY)
# ===================================================
# Purpose: Restore Winsock to state before reset to fix Btrieve

Write-Host "=" -NoNewline; Write-Host ("=" * 69)
Write-Host "EMERGENCY: RESTORE WINSOCK FROM BACKUP"
Write-Host "=" -NoNewline; Write-Host ("=" * 69)

Write-Host @"

CRITICAL ISSUE:
Winsock reset broke Btrieve SRDE engine initialization.
Error 8520 persists after reboot.

SOLUTION:
We need to restore Winsock to its original state using System Restore
or reinstall Pervasive PSQL to rebuild Btrieve components.

"@

Write-Host "`n" + ("=" * 70)
Write-Host "OPTION 1: SYSTEM RESTORE (RECOMMENDED)"
Write-Host ("=" * 70)

Write-Host @"

Windows System Restore can rollback Winsock changes:

1. Open System Restore:
   rstrui.exe

2. Select restore point BEFORE today (before Winsock reset)

3. Follow wizard to restore

4. System will reboot

5. After reboot, verify:
   - NEX Genesis works
   - No Btrieve errors

"@

Write-Host "`n" + ("=" * 70)
Write-Host "OPTION 2: REINSTALL PERVASIVE COMPONENTS"
Write-Host ("=" * 70)

Write-Host @"

Reinstall Pervasive Btrieve components:

1. Find Pervasive installation media/setup
2. Run repair/reinstall
3. Reboot
4. Verify Btrieve works

"@

Write-Host "`n" + ("=" * 70)
Write-Host "OPTION 3: MANUAL WINSOCK FIX"
Write-Host ("=" * 70)

Write-Host @"

Try to register Btrieve DLLs manually:

1. Open CMD as Administrator
2. Run:
   cd C:\PVSW\bin
   regsvr32 w3btrv7.dll

3. Reboot
4. Test

"@

Write-Host "`n" + ("=" * 70)
Write-Host "RECOMMENDED ACTION"
Write-Host ("=" * 70)

Write-Host @"

IMMEDIATE: Try OPTION 3 first (quickest)
If fails: Use OPTION 1 (System Restore)
Last resort: OPTION 2 (Reinstall Pervasive)

"@

$action = Read-Host "`nWhat would you like to try? (regsvr32/restore/reinstall/cancel)"

switch ($action.ToLower()) {
    "regsvr32" {
        Write-Host "`n[INFO] Attempting to register Btrieve DLL..."

        $dllPath = "C:\PVSW\bin\w3btrv7.dll"

        if (Test-Path $dllPath) {
            Write-Host "[INFO] Running: regsvr32 `"$dllPath`""

            $result = Start-Process -FilePath "regsvr32.exe" `
                -ArgumentList "/s `"$dllPath`"" `
                -Wait -PassThru -NoNewWindow

            if ($result.ExitCode -eq 0) {
                Write-Host "[OK] DLL registered successfully"
                Write-Host "`n[INFO] Reboot required: shutdown /r /t 60"
            } else {
                Write-Host "[ERROR] DLL registration failed"
                Write-Host "[INFO] Try System Restore instead"
            }
        } else {
            Write-Host "[ERROR] DLL not found: $dllPath"
        }
    }

    "restore" {
        Write-Host "`n[INFO] Opening System Restore..."
        Start-Process "rstrui.exe"
        Write-Host "[INFO] Follow the wizard to restore to point before today"
    }

    "reinstall" {
        Write-Host "`n[INFO] You need to:"
        Write-Host "1. Locate Pervasive PSQL installation media"
        Write-Host "2. Run setup and select Repair/Modify"
        Write-Host "3. Reinstall Btrieve components"
        Write-Host "4. Reboot server"
    }

    "cancel" {
        Write-Host "`n[INFO] No action taken"
        Write-Host "[WARNING] Btrieve will remain broken until fixed"
    }

    default {
        Write-Host "`n[INFO] Invalid choice"
    }
}

Write-Host "`n[IMPORTANT] NEX Automat Task Scheduler will work once Btrieve is fixed"