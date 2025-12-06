# Claude Tools - Startup Script (nex-automat)
# Spusti vsetky potrebne komponenty na pozadi

param(
    [switch]$NoHotkeys,
    [switch]$NoServer,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

# Konfiguracia
$ToolsDir = "C:\Development\nex-automat\tools"
$LogFile = Join-Path $ToolsDir "claude-tools.log"

# Funkcia pre logovanie
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")

    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogMessage = "[$Timestamp] [$Level] $Message"

    # Console
    switch ($Level) {
        "ERROR" { Write-Host $LogMessage -ForegroundColor Red }
        "WARN"  { Write-Host $LogMessage -ForegroundColor Yellow }
        "SUCCESS" { Write-Host $LogMessage -ForegroundColor Green }
        default { Write-Host $LogMessage }
    }

    # File
    Add-Content -Path $LogFile -Value $LogMessage
}

# Banner
Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "CLAUDE TOOLS - STARTUP (nex-automat)" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Kontrola adresara
if (-not (Test-Path $ToolsDir)) {
    Write-Log "Tools adresar neexistuje: $ToolsDir" "ERROR"
    exit 1
}

Set-Location $ToolsDir
Write-Log "Working directory: $ToolsDir" "INFO"

# Kontrola Python
Write-Log "Kontrolujem Python..." "INFO"
try {
    $PythonVersion = & python --version 2>&1
    Write-Log "Python: $PythonVersion" "SUCCESS"
} catch {
    Write-Log "Python nie je nainstalovany alebo nie je v PATH" "ERROR"
    exit 1
}

# Inicializuj log
"" | Out-File -FilePath $LogFile -Force
Write-Log "Claude Tools Startup (nex-automat) - Begin" "INFO"

# Tracking spustenych procesov
$StartedProcesses = @()

# 1. ARTIFACT SERVER
if (-not $NoServer) {
    Write-Host ""
    Write-Log "Spustam Artifact Server..." "INFO"

    try {
        # Kontrola ci uz nebezi
        $ExistingServer = Get-Process | Where-Object { 
            $_.CommandLine -like "*artifact-server*" 
        }

        if ($ExistingServer) {
            Write-Log "Artifact Server uz bezi (PID: $($ExistingServer.Id))" "WARN"
        } else {
            # Spusti server v novom okne
            $ServerProcess = Start-Process powershell -ArgumentList `
                "-NoExit", `
                "-Command", `
                "cd '$ToolsDir'; python artifact-server.py" `
                -PassThru `
                -WindowStyle Normal

            $StartedProcesses += @{
                Name = "Artifact Server"
                PID = $ServerProcess.Id
            }

            Write-Log "Artifact Server spusteny (PID: $($ServerProcess.Id))" "SUCCESS"
            Write-Log "   URL: http://localhost:8765" "INFO"

            # Pockaj na inicializaciu
            Start-Sleep -Seconds 2

            # Test dostupnosti
            try {
                $Response = Invoke-WebRequest -Uri "http://localhost:8765/ping" -TimeoutSec 5
                if ($Response.StatusCode -eq 200) {
                    Write-Log "Server je dostupny" "SUCCESS"
                }
            } catch {
                Write-Log "Server mozno este nie je plne pripraveny" "WARN"
            }
        }
    } catch {
        Write-Log "Chyba pri spustani servera: $_" "ERROR"
    }
}

# 2. HOTKEYS
if (-not $NoHotkeys) {
    Write-Host ""
    Write-Log "Spustam Hotkeys..." "INFO"

    try {
        # Kontrola ci uz nebezia
        $ExistingHotkeys = Get-Process python | Where-Object { 
            $_.CommandLine -like "*claude-hotkeys*" 
        }

        if ($ExistingHotkeys) {
            Write-Log "Hotkeys uz bezia (PID: $($ExistingHotkeys.Id))" "WARN"
        } else {
            # Spusti hotkeys na pozadi (bez okna)
            $HotkeyProcess = Start-Process python `
                -ArgumentList "claude-hotkeys.py" `
                -PassThru `
                -WindowStyle Hidden `
                -WorkingDirectory $ToolsDir

            $StartedProcesses += @{
                Name = "Hotkeys"
                PID = $HotkeyProcess.Id
            }

            Write-Log "Hotkeys spustene (PID: $($HotkeyProcess.Id))" "SUCCESS"
            Write-Log "   Ctrl+Alt+S - Copy Session Notes" "INFO"
            Write-Log "   Ctrl+Alt+G - Git Status" "INFO"
            Write-Log "   Ctrl+Alt+D - Deployment Info" "INFO"
            Write-Log "   Ctrl+Alt+N - New Chat Template" "INFO"
            Write-Log "   Ctrl+Alt+I - Show Info" "INFO"
        }
    } catch {
        Write-Log "Chyba pri spustani hotkeys: $_" "ERROR"
    }
}

# Summary
Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Log "STARTUP DOKONCENY (nex-automat)" "SUCCESS"
Write-Host "=" * 60 -ForegroundColor Cyan

if ($StartedProcesses.Count -gt 0) {
    Write-Host ""
    Write-Host "Spustene procesy:" -ForegroundColor Green
    foreach ($Process in $StartedProcesses) {
        Write-Host "  $($Process.Name) (PID: $($Process.PID))" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Ako zastavit:" -ForegroundColor Yellow
Write-Host "   .\stop-claude-tools.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "Ako restartovat:" -ForegroundColor Yellow  
Write-Host "   .\stop-claude-tools.ps1; .\start-claude-tools.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "Log file: $LogFile" -ForegroundColor Cyan
Write-Host ""

Write-Log "Startup script dokonceny" "INFO"
