# Script: create_desktop_shortcuts.ps1
# Purpose: Create desktop shortcuts for Markdown documentation
# Usage: Run from C:\Development\nex-automat

param(
    [string]$MarkdownViewer = ""
)

$ErrorActionPreference = "Stop"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "NEX Automat - Desktop Shortcuts Creator" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Get project root
$projectRoot = Get-Location

# Get desktop path
$desktopPath = [Environment]::GetFolderPath("Desktop")
$shortcutFolder = Join-Path $desktopPath "NEX Automat Docs"

# Create folder for shortcuts
if (!(Test-Path $shortcutFolder)) {
    New-Item -Path $shortcutFolder -ItemType Directory | Out-Null
    Write-Host "[OK] Created folder: $shortcutFolder" -ForegroundColor Green
} else {
    # Clean existing .lnk shortcuts
    Remove-Item -Path "$shortcutFolder\*.lnk" -Force -ErrorAction SilentlyContinue
    Write-Host "[OK] Cleaned existing shortcuts" -ForegroundColor Green
}

# Find Markdown Viewer
if ($MarkdownViewer -eq "") {
    Write-Host "Searching for Markdown Viewer..." -ForegroundColor Yellow

    $possiblePaths = @(
        "$env:PROGRAMFILES\MarkText\MarkText.exe",
        "$env:LOCALAPPDATA\Programs\MarkText\MarkText.exe",
        "$env:PROGRAMFILES\Markdown Viewer\Markdown Viewer.exe",
        "$env:LOCALAPPDATA\Programs\Markdown Viewer\Markdown Viewer.exe",
        "$env:PROGRAMFILES\Typora\Typora.exe"
    )

    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            $MarkdownViewer = $path
            Write-Host "[OK] Found: $path" -ForegroundColor Green
            break
        }
    }

    if ($MarkdownViewer -eq "") {
        Write-Host "[WARN] Markdown Viewer not found, using Notepad" -ForegroundColor Yellow
        $MarkdownViewer = "notepad.exe"
    }
}

Write-Host "Using viewer: $MarkdownViewer" -ForegroundColor Cyan
Write-Host ""

# Helper function to create shortcut
function Create-Shortcut {
    param(
        [string]$ShortcutPath,
        [string]$TargetPath,
        [string]$Arguments = "",
        [string]$Description = ""
    )

    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = $TargetPath

    if ($Arguments -ne "") {
        $Shortcut.Arguments = $Arguments
    }

    if ($Description -ne "") {
        $Shortcut.Description = $Description
    }

    $Shortcut.Save()
}

# Locations to search - ONLY Development
$searchLocations = @(
    @{
        Label = "Development"
        BasePath = $projectRoot
        Prefix = ""
        Folders = @("docs", "docs\deployment")
    }
)

$mdFiles = @()

# Find all .md files
Write-Host "Searching for Markdown files..." -ForegroundColor Yellow

foreach ($location in $searchLocations) {
    if (Test-Path $location.BasePath) {
        Write-Host "  Scanning: $($location.Label) [$($location.BasePath)]" -ForegroundColor Cyan

        foreach ($folder in $location.Folders) {
            $fullPath = Join-Path $location.BasePath $folder

            if (Test-Path $fullPath) {
                $files = Get-ChildItem -Path $fullPath -Filter "*.md" -File -ErrorAction SilentlyContinue

                foreach ($file in $files) {
                    # Determine display name based on folder
                    $displayName = if ($folder -eq "docs\deployment") {
                        "DEPLOY - $($file.BaseName)"
                    } else {
                        "$($file.BaseName)"
                    }

                    $mdFiles += @{
                        Name = $displayName
                        Path = $file.FullName
                        Description = "$($location.Label): $folder\$($file.Name)"
                    }

                    Write-Host "    [+] $folder\$($file.Name)" -ForegroundColor Green
                }
            }
        }

        # Also check root for .md files
        $rootFiles = Get-ChildItem -Path $location.BasePath -Filter "*.md" -File -ErrorAction SilentlyContinue
        foreach ($file in $rootFiles) {
            $mdFiles += @{
                Name = "$($file.BaseName)"
                Path = $file.FullName
                Description = "$($location.Label): $($file.Name)"
            }
            Write-Host "    [+] $($file.Name)" -ForegroundColor Green
        }
    } else {
        Write-Host "  [SKIP] $($location.Label) (path not found)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Creating shortcuts for $($mdFiles.Count) Markdown files..." -ForegroundColor Yellow

# Create shortcuts
$created = 0
foreach ($mdFile in $mdFiles) {
    $shortcutName = "$($mdFile.Name).lnk"
    $shortcutPath = Join-Path $shortcutFolder $shortcutName

    Create-Shortcut -ShortcutPath $shortcutPath `
                   -TargetPath $MarkdownViewer `
                   -Arguments "`"$($mdFile.Path)`"" `
                   -Description $mdFile.Description

    Write-Host "  [OK] $($mdFile.Name)" -ForegroundColor Green
    $created++
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "SUCCESS: $created shortcuts created!" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Location: $shortcutFolder" -ForegroundColor White
Write-Host ""

# Create README
$readmePath = Join-Path $shortcutFolder "README.txt"
$readmeContent = @"
NEX Automat v2.0 - Quick Access Documentation
=============================================

This folder contains shortcuts to all Markdown documentation files
from Development environment.

Location: C:\Development\nex-automat

PREFIX LEGEND:
--------------
DEPLOY - ... = Deployment documentation (from docs/deployment folder)
(no prefix)  = General documentation (from docs folder or root)

MARKDOWN FILES FOUND: $($mdFiles.Count)

Markdown Viewer: $MarkdownViewer

Last updated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

To refresh shortcuts, run:
  C:\Development\nex-automat\scripts\create_desktop_shortcuts.ps1
"@

Set-Content -Path $readmePath -Value $readmeContent -Encoding UTF8
Write-Host "[OK] Created README.txt" -ForegroundColor Green
Write-Host ""