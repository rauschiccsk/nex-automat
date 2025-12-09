# Script 16: Check Winsock Backup and Options
# =============================================
# Purpose: Check if we can restore or if we need different approach

Write-Host "=" -NoNewline; Write-Host ("=" * 69)
Write-Host "WINSOCK BACKUP CHECK AND OPTIONS"
Write-Host "=" -NoNewline; Write-Host ("=" * 69)

Write-Host "`n[INFO] Checking for Winsock backup..."

$backupDir = "C:\Deployment\nex-automat\logs"
$backups = Get-ChildItem -Path $backupDir -Directory -Filter "winsock-backup-*" -ErrorAction SilentlyContinue

if ($backups) {
    Write-Host "`n[FOUND] Winsock backup(s):"
    foreach ($backup in $backups) {
        Write-Host "  - $($backup.Name)"
        $files = Get-ChildItem -Path $backup.FullName -File
        foreach ($file in $files) {
            Write-Host "    * $($file.Name)"
        }
    }
} else {
    Write-Host "`n[WARNING] No Winsock backup found"
}

Write-Host "`n" + ("=" * 70)
Write-Host "CURRENT SITUATION"
Write-Host ("=" * 70)

Write-Host @"

Problem: Winsock reset broke Btrieve SRDE engine
Error: W3DBSMGR Error 8520 - timeout during SRDE initialization

This means:
1. Winsock reset changed network stack
2. Btrieve cannot communicate properly
3. NEX Genesis cannot access database

"@

Write-Host "`n" + ("=" * 70)
Write-Host "SOLUTION OPTIONS"
Write-Host ("=" * 70)

Write-Host @"

OPTION 1: Full Server Reboot (RECOMMENDED)
-------------------------------------------
Sometimes a full reboot fixes Btrieve initialization issues.

Command: shutdown /r /t 0

After reboot:
- Btrieve should reinitialize properly
- Test NEX Genesis access to database
- If works, try NEX-Automat service again


OPTION 2: Run NEX-Automat WITHOUT Service (WORKAROUND)
-------------------------------------------------------
Since service account has Winsock issues, run as console app:

1. Create startup script in Task Scheduler:
   - Run at system startup
   - Run as specific user account (not SYSTEM)
   - Command: C:\Deployment\nex-automat\venv32\Scripts\python.exe
   - Arguments: C:\Deployment\nex-automat\apps\supplier-invoice-loader\main.py
   - Start in: C:\Deployment\nex-automat\apps\supplier-invoice-loader

2. Or run manually in console window (for testing):
   cd C:\Deployment\nex-automat\apps\supplier-invoice-loader
   C:\Deployment\nex-automat\venv32\Scripts\python.exe main.py


OPTION 3: Investigate Root Cause
---------------------------------
The WinError 10106 is unusual and suggests:
- Corrupted Windows Sockets installation
- Antivirus/firewall interference
- Missing Windows updates
- System file corruption

Check:
1. Windows Update status
2. Antivirus logs
3. System file integrity: sfc /scannow


RECOMMENDED ACTION NOW:
-----------------------
1. Full server reboot: shutdown /r /t 0
2. After reboot, test NEX Genesis first
3. If NEX Genesis works, test NEX-Automat service
4. If service still fails, run as console app (Option 2)

"@

$action = Read-Host "`nWhat would you like to do? (reboot/console/cancel)"

switch ($action.ToLower()) {
    "reboot" {
        Write-Host "`n[INFO] Rebooting server in 60 seconds..."
        Write-Host "[INFO] Press CTRL+C to cancel"
        shutdown /r /t 60 /c "Reboot to fix Btrieve SRDE after Winsock reset"
    }
    "console" {
        Write-Host "`n[INFO] To run as console application:"
        Write-Host "cd C:\Deployment\nex-automat\apps\supplier-invoice-loader"
        Write-Host "C:\Deployment\nex-automat\venv32\Scripts\python.exe main.py"
        Write-Host "`n[INFO] Keep the window open - press CTRL+C to stop"
    }
    "cancel" {
        Write-Host "`n[INFO] No action taken"
    }
    default {
        Write-Host "`n[INFO] Invalid choice, no action taken"
    }
}