@echo off
REM Launcher for migration-tool.pyw — activates venv32 and runs without console window.
REM Double-click this .bat to open the Migration Tool GUI.

setlocal
cd /d "%~dp0"

if not exist venv32\Scripts\pythonw.exe (
    echo ERROR: venv32 not found. Run install.bat first.
    pause
    exit /b 1
)

REM Use pythonw.exe (no console) — keeps GUI clean
start "" "%~dp0venv32\Scripts\pythonw.exe" "%~dp0migration-tool.pyw"
endlocal
