# Script 17: Create Task Scheduler Task for NEX Automat
# =======================================================
# Purpose: Create Windows Task Scheduler task to run NEX Automat as console app

Write-Host "=" -NoNewline; Write-Host ("=" * 69)
Write-Host "CREATE TASK SCHEDULER TASK - NEX AUTOMAT LOADER"
Write-Host "=" -NoNewline; Write-Host ("=" * 69)

$taskName = "NEX-Automat-Loader"
$pythonExe = "C:\Deployment\nex-automat\venv32\Scripts\python.exe"
$mainPy = "C:\Deployment\nex-automat\apps\supplier-invoice-loader\main.py"
$workingDir = "C:\Deployment\nex-automat\apps\supplier-invoice-loader"

Write-Host "`n[INFO] Task Configuration:"
Write-Host "  Name: $taskName"
Write-Host "  Python: $pythonExe"
Write-Host "  Script: $mainPy"
Write-Host "  Working Directory: $workingDir"

# Check if files exist
if (-not (Test-Path $pythonExe)) {
    Write-Host "`n[ERROR] Python executable not found: $pythonExe"
    exit 1
}

if (-not (Test-Path $mainPy)) {
    Write-Host "`n[ERROR] Main script not found: $mainPy"
    exit 1
}

Write-Host "`n[OK] All files verified"

# Step 1: Remove existing NSSM service
Write-Host "`n" + ("=" * 70)
Write-Host "STEP 1: REMOVE NSSM SERVICE"
Write-Host ("=" * 70)

$service = Get-Service -Name $taskName -ErrorAction SilentlyContinue
if ($service) {
    Write-Host "`n[INFO] Stopping and removing NSSM service..."

    try {
        Stop-Service -Name $taskName -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2

        & nssm remove $taskName confirm
        Write-Host "[OK] NSSM service removed"
    } catch {
        Write-Host "[WARNING] Could not remove NSSM service: $($_.Exception.Message)"
    }
} else {
    Write-Host "`n[INFO] No NSSM service found to remove"
}

# Step 2: Get current user
Write-Host "`n" + ("=" * 70)
Write-Host "STEP 2: USER ACCOUNT"
Write-Host ("=" * 70)

$currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
Write-Host "`n[INFO] Current user: $currentUser"

$user = Read-Host "`nRun task as current user '$currentUser'? (yes to use current, or enter domain\username)"

if ($user -eq "yes" -or $user -eq "") {
    $user = $currentUser
}

Write-Host "[INFO] Task will run as: $user"

# Step 3: Create Task Scheduler task
Write-Host "`n" + ("=" * 70)
Write-Host "STEP 3: CREATE TASK SCHEDULER TASK"
Write-Host ("=" * 70)

# Remove existing task if exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "`n[INFO] Removing existing task..."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "[OK] Existing task removed"
}

Write-Host "`n[INFO] Creating new scheduled task..."

# Create action
$action = New-ScheduledTaskAction `
    -Execute $pythonExe `
    -Argument "`"$mainPy`"" `
    -WorkingDirectory $workingDir

# Create trigger (at system startup)
$trigger = New-ScheduledTaskTrigger -AtStartup

# Create settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -ExecutionTimeLimit (New-TimeSpan -Days 0)

# Create principal (user to run as)
$principal = New-ScheduledTaskPrincipal `
    -UserId $user `
    -LogonType Interactive `
    -RunLevel Highest

# Register task
try {
    Register-ScheduledTask `
        -TaskName $taskName `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Principal $principal `
        -Description "NEX Automat Supplier Invoice Loader - Runs at system startup" `
        -ErrorAction Stop

    Write-Host "[OK] Task created successfully"
} catch {
    Write-Host "[ERROR] Failed to create task: $($_.Exception.Message)"
    exit 1
}

# Step 4: Test task
Write-Host "`n" + ("=" * 70)
Write-Host "STEP 4: TEST TASK"
Write-Host ("=" * 70)

Write-Host "`n[INFO] Starting task manually for testing..."

try {
    Start-ScheduledTask -TaskName $taskName
    Write-Host "[OK] Task started"

    Write-Host "`n[INFO] Waiting 10 seconds for application to start..."
    Start-Sleep -Seconds 10

    # Test if port is open
    Write-Host "[INFO] Testing port 8001..."
    $tcpClient = New-Object System.Net.Sockets.TcpClient
    try {
        $tcpClient.Connect("localhost", 8001)
        $tcpClient.Close()
        Write-Host "[OK] Port 8001 is open - Application is running!"
    } catch {
        Write-Host "[WARNING] Port 8001 is not open yet"
        Write-Host "[INFO] Check task status: Get-ScheduledTask -TaskName '$taskName'"
    }
} catch {
    Write-Host "[ERROR] Failed to start task: $($_.Exception.Message)"
}

# Step 5: Summary
Write-Host "`n" + ("=" * 70)
Write-Host "SETUP COMPLETE"
Write-Host ("=" * 70)

Write-Host @"

Task Scheduler Configuration:
- Name: $taskName
- Trigger: At system startup
- User: $user
- Action: Run Python application
- Auto-restart: Yes (3 attempts, 1 minute interval)

Management Commands:
--------------------
View task:
  Get-ScheduledTask -TaskName "$taskName" | Format-List *

Start task manually:
  Start-ScheduledTask -TaskName "$taskName"

Stop task:
  Stop-ScheduledTask -TaskName "$taskName"

Remove task:
  Unregister-ScheduledTask -TaskName "$taskName"

View task history:
  Get-ScheduledTask -TaskName "$taskName" | Get-ScheduledTaskInfo

Logs:
-----
Application logs still in:
  C:\Deployment\nex-automat\logs\

Next Steps:
-----------
1. Test API: http://localhost:8001/docs
2. Upload test invoice to verify functionality
3. Monitor application stability
4. After confirming it works, reboot server to test startup

"@

Write-Host "`n[SUCCESS] NEX Automat is now configured to run at system startup"