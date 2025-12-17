@echo off
REM Start RAG External Access Services
REM Run this after computer restart
REM Location: C:\Development\nex-automat\scripts\infrastructure\start-rag-services.bat

echo ============================================
echo Starting RAG External Access Services
echo ============================================
echo.

echo [1/2] Starting RAG Server...
start "RAG Server" cmd /k "cd C:\Development\nex-automat && .\venv\Scripts\Activate.ps1 && python -m tools.rag.server start"

echo Waiting 5 seconds for RAG Server to initialize...
timeout /t 5 /nobreak > nul

echo [2/2] Starting Cloudflare Tunnel...
start "Cloudflare Tunnel" cmd /k "cloudflared tunnel --config C:\Users\ZelenePC\.cloudflared\config.yml run n8n-tunnel"

echo.
echo ============================================
echo Services started!
echo ============================================
echo.
echo Verify at: https://rag-api.icc.sk/health
echo.
echo Press any key to close this window...
pause > nul