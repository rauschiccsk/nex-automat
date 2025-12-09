# Script 14: Fix Winsock (MUST RUN AS ADMINISTRATOR)
# ===================================================
# Purpose: Reset Windows Sockets to fix WinError 10106
# WARNING: Server MUST be rebooted after this!

Write-Host "=" -NoNewline; Write-Host ("=" * 69)
Write-Host "WINDOWS SOCKETS (WINSOCK) RESET"
Write-Host "=" -NoNewline; Write-Host ("=" * 69)

Write-Host "`n[WARNING] This will reset Windows Sockets configuration"
Write-Host "[WARNING] Server MUST be rebooted after this operation"
Write-Host "[WARNING] Schedule downtime before proceeding"

$response = Read-Host "`nProceed with Winsock reset? (yes/no)"

if ($response -ne "yes") {
    Write-Host "`n[CANCELLED] Winsock reset cancelled by user"
    exit
}

Write-Host "`n" + ("=" * 70)
Write-Host "STEP 1: BACKUP CURRENT CONFIGURATION"
Write-Host ("=" * 70)

$backupDir = "C:\Deployment\nex-automat\logs\winsock-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null

Write-Host "`n[INFO] Backing up current configuration to: $backupDir"

# Export current Winsock catalog
netsh winsock show catalog > "$backupDir\winsock-catalog-before.txt"
netsh int ip show config > "$backupDir\ip-config-before.txt"
ipconfig /all > "$backupDir\ipconfig-before.txt"

Write-Host "[OK] Backup complete"

Write-Host "`n" + ("=" * 70)
Write-Host "STEP 2: RESET WINSOCK"
Write-Host ("=" * 70)

Write-Host "`n[INFO] Resetting Winsock catalog..."
$result = netsh winsock reset 2>&1
Write-Host $result

Write-Host "`n[INFO] Resetting TCP/IP stack..."
$result = netsh int ip reset 2>&1
Write-Host $result

Write-Host "`n[OK] Winsock reset complete"

Write-Host "`n" + ("=" * 70)
Write-Host "STEP 3: REBOOT REQUIRED"
Write-Host ("=" * 70)

Write-Host "`n[CRITICAL] Server MUST be rebooted for changes to take effect"
Write-Host "[INFO] After reboot, test service startup"

$reboot = Read-Host "`nReboot server NOW? (yes/no)"

if ($reboot -eq "yes") {
    Write-Host "`n[INFO] Rebooting server in 60 seconds..."
    Write-Host "[INFO] Press CTRL+C to cancel"
    shutdown /r /t 60 /c "Rebooting to apply Winsock reset for NEX Automat service"
} else {
    Write-Host "`n[INFO] Manual reboot required before service will work"
    Write-Host "[INFO] Run: shutdown /r /t 0"
}

Write-Host "`n" + ("=" * 70)
Write-Host "AFTER REBOOT - TEST PROCEDURE"
Write-Host ("=" * 70)
Write-Host @"

1. Verify Winsock is working:
   python scripts\03_check_btrieve_client.py

2. Start service:
   net start "NEX-Automat-Loader"

3. Check service status:
   sc query "NEX-Automat-Loader"

4. Test API:
   Open browser: http://localhost:8001/health

If still fails:
- Check if antivirus/firewall is blocking Winsock
- Check Windows Event Log for Winsock errors
- Consider contacting system administrator
"@