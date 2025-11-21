# NEX Automat - Task Scheduler Setup
# Creates scheduled tasks for automated database backups
# Author: Zoltan Rausch, ICC Komarno
# Date: 2025-11-21

$ErrorActionPreference = "Stop"

# Configuration
$ProjectRoot = "C:\Development\nex-automat\apps\supplier-invoice-loader"
$PythonExe = "C:\Development\nex-automat\venv32\Scripts\python.exe"
$BackupWrapper = "$ProjectRoot\scripts\backup_wrapper.py"
$LogDir = "$ProjectRoot\logs"

Write-Host "======================================================================"
Write-Host "NEX Automat - Task Scheduler Setup"
Write-Host "======================================================================"

# Create logs directory
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
    Write-Host ""
    Write-Host "[OK] Created logs directory: $LogDir"
}

# Task 1: Daily Backup
Write-Host ""
Write-Host "1. Creating Daily Backup Task..."

$DailyAction = New-ScheduledTaskAction `
    -Execute $PythonExe `
    -Argument "$BackupWrapper --type daily" `
    -WorkingDirectory $ProjectRoot

$DailyTrigger = New-ScheduledTaskTrigger `
    -Daily `
    -At "02:00AM"

$DailySettings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2) `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 5) `
    -StartWhenAvailable

$DailyPrincipal = New-ScheduledTaskPrincipal `
    -UserId "SYSTEM" `
    -RunLevel Highest

try {
    Unregister-ScheduledTask -TaskName "NEX-Automat-Backup-Daily" -Confirm:$false -ErrorAction SilentlyContinue
    Register-ScheduledTask `
        -TaskName "NEX-Automat-Backup-Daily" `
        -Description "Daily database backup for NEX Automat at 02:00 AM" `
        -Action $DailyAction `
        -Trigger $DailyTrigger `
        -Settings $DailySettings `
        -Principal $DailyPrincipal | Out-Null

    Write-Host "   [OK] Daily backup task created (02:00 AM)"
} catch {
    Write-Host "   [ERROR] Failed to create daily backup task: $_" -ForegroundColor Red
    exit 1
}

# Task 2: Weekly Backup
Write-Host ""
Write-Host "2. Creating Weekly Backup Task..."

$WeeklyAction = New-ScheduledTaskAction `
    -Execute $PythonExe `
    -Argument "$BackupWrapper --type weekly" `
    -WorkingDirectory $ProjectRoot

$WeeklyTrigger = New-ScheduledTaskTrigger `
    -Weekly `
    -DaysOfWeek Sunday `
    -At "02:00AM"

$WeeklySettings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2) `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 5) `
    -StartWhenAvailable

$WeeklyPrincipal = New-ScheduledTaskPrincipal `
    -UserId "SYSTEM" `
    -RunLevel Highest

try {
    Unregister-ScheduledTask -TaskName "NEX-Automat-Backup-Weekly" -Confirm:$false -ErrorAction SilentlyContinue
    Register-ScheduledTask `
        -TaskName "NEX-Automat-Backup-Weekly" `
        -Description "Weekly database backup for NEX Automat every Sunday at 02:00 AM" `
        -Action $WeeklyAction `
        -Trigger $WeeklyTrigger `
        -Settings $WeeklySettings `
        -Principal $WeeklyPrincipal | Out-Null

    Write-Host "   [OK] Weekly backup task created (Sunday 02:00 AM)"
} catch {
    Write-Host "   [ERROR] Failed to create weekly backup task: $_" -ForegroundColor Red
    exit 1
}

# Verify tasks
Write-Host ""
Write-Host "3. Verifying scheduled tasks..."

$DailyTask = Get-ScheduledTask -TaskName "NEX-Automat-Backup-Daily" -ErrorAction SilentlyContinue
$WeeklyTask = Get-ScheduledTask -TaskName "NEX-Automat-Backup-Weekly" -ErrorAction SilentlyContinue

if ($DailyTask -and $WeeklyTask) {
    Write-Host "   [OK] Both tasks verified and ready"

    Write-Host ""
    Write-Host "======================================================================"
    Write-Host "[SUCCESS] Task Scheduler Setup Complete!"
    Write-Host "======================================================================"

    Write-Host ""
    Write-Host "Scheduled Tasks:"
    Write-Host "  - NEX-Automat-Backup-Daily  : Every day at 02:00 AM"
    Write-Host "  - NEX-Automat-Backup-Weekly : Every Sunday at 02:00 AM"

    Write-Host ""
    Write-Host "Manage tasks:"
    Write-Host "  Get-ScheduledTask -TaskName 'NEX-Automat-Backup-*'"
    Write-Host "  Start-ScheduledTask -TaskName 'NEX-Automat-Backup-Daily'"
    Write-Host "  Disable-ScheduledTask -TaskName 'NEX-Automat-Backup-Daily'"
    Write-Host "  Enable-ScheduledTask -TaskName 'NEX-Automat-Backup-Daily'"

    Write-Host ""
    Write-Host "View logs:"
    Write-Host "  Get-Content $LogDir\backup_daily_YYYYMMDD.log"
    Write-Host "  Get-Content $LogDir\backup_weekly_YYYYMMDD.log"

} else {
    Write-Host "   [ERROR] Task verification failed" -ForegroundColor Red
    exit 1
}
