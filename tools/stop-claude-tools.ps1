# Claude Tools - Stop Script (nex-automat)
# Zastavi vsetky beziace Claude Tools procesy

param(
    [switch]$Force,
    [switch]$Verbose
)

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "STOP CLAUDE TOOLS (nex-automat)" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Najdi vsetky Claude Tools procesy
$Patterns = @(
    "*artifact-server*",
    "*claude-hotkeys*",
    "*claude-chat-loader*",
    "*session-notes-manager*"
)

$FoundProcesses = @()

foreach ($Pattern in $Patterns) {
    $Processes = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
        $_.CommandLine -like $Pattern
    }

    if ($Processes) {
        $FoundProcesses += $Processes
    }
}

if ($FoundProcesses.Count -eq 0) {
    Write-Host "Ziadne Claude Tools procesy nebezia" -ForegroundColor Yellow
    Write-Host ""
    exit 0
}

# Zobraz najdene procesy
Write-Host "Najdene procesy:" -ForegroundColor Yellow
foreach ($Process in $FoundProcesses) {
    $CommandSnippet = if ($Process.CommandLine) {
        $Process.CommandLine.Substring(0, [Math]::Min(50, $Process.CommandLine.Length))
    } else {
        "N/A"
    }

    Write-Host "  PID $($Process.Id): $CommandSnippet..." -ForegroundColor Gray
}

Write-Host ""

# Potvrdenie ak nie je Force
if (-not $Force) {
    $Confirm = Read-Host "Zastavit vsetky tieto procesy? (y/n)"
    if ($Confirm -ne 'y' -and $Confirm -ne 'Y') {
        Write-Host "Zrusene" -ForegroundColor Red
        exit 1
    }
}

# Zastavit procesy
$StoppedCount = 0
$FailedCount = 0

foreach ($Process in $FoundProcesses) {
    try {
        Write-Host "Zastavujem PID $($Process.Id)..." -ForegroundColor Gray

        Stop-Process -Id $Process.Id -Force -ErrorAction Stop
        $StoppedCount++

        Write-Host "  Zastaveny PID $($Process.Id)" -ForegroundColor Green

    } catch {
        $FailedCount++
        Write-Host "  Chyba pri zastaveni PID $($Process.Id): $_" -ForegroundColor Red
    }
}

# Summary
Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "VYSLEDOK:" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "  Zastavene: $StoppedCount" -ForegroundColor Green
if ($FailedCount -gt 0) {
    Write-Host "  Chyby: $FailedCount" -ForegroundColor Red
}
Write-Host ""

# Overenie
Start-Sleep -Seconds 1

$RemainingProcesses = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    foreach ($Pattern in $Patterns) {
        if ($_.CommandLine -like $Pattern) {
            return $true
        }
    }
    return $false
}

if ($RemainingProcesses) {
    Write-Host "Niektore procesy este stale bezia:" -ForegroundColor Yellow
    foreach ($Process in $RemainingProcesses) {
        Write-Host "  PID $($Process.Id)" -ForegroundColor Gray
    }
    Write-Host ""
    Write-Host "Pouzi -Force pre nasilne zastavenie" -ForegroundColor Yellow
} else {
    Write-Host "Vsetky Claude Tools procesy zastavene" -ForegroundColor Green
}

Write-Host ""
