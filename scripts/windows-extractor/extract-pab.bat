@echo off
REM NEX Extract PAB — runs PAB Btrieve → JSON extract.
REM Usage:  extract-pab.bat C:\ICC\NEX

setlocal

if "%~1"=="" (
    echo Usage: extract-pab.bat ^<NEX_DATA_ROOT^>
    echo Example for ICC:    extract-pab.bat C:\ICC\NEX
    echo Example for ANDROS: extract-pab.bat C:\ANDROS\NEX
    exit /b 1
)

set DATA_ROOT=%~1

if not exist "%DATA_ROOT%\YEARACT\DIALS\PAB00000.BTR" (
    echo ERROR: PAB Btrieve file not found:
    echo   %DATA_ROOT%\YEARACT\DIALS\PAB00000.BTR
    echo.
    echo Verify that --data-root points to the NEX Genesis install root
    echo ^(the dir that contains YEARACT\DIALS\^).
    exit /b 1
)

if not exist venv32\Scripts\activate.bat (
    echo ERROR: venv32 not found. Run install.bat first.
    exit /b 1
)
call venv32\Scripts\activate.bat

REM Locate run_extract.py — either in this bundle or in upstream repo
if exist "..\..\apps\nex-migration\run_extract.py" (
    set RUN_EXTRACT=..\..\apps\nex-migration\run_extract.py
    set EXTRACT_CWD=..\..\apps\nex-migration
) else if exist "nex-migration\run_extract.py" (
    set RUN_EXTRACT=nex-migration\run_extract.py
    set EXTRACT_CWD=nex-migration
) else (
    echo ERROR: run_extract.py not found.
    echo Either run from a nex-automat-src checkout, or copy
    echo apps\nex-migration\ as ".\nex-migration\".
    exit /b 1
)

mkdir output 2>NUL

echo [extract] Running PAB extraction...
echo   data-root: %DATA_ROOT%
echo   output:    %CD%\output\PAB\PAB.json
echo.

pushd %EXTRACT_CWD%
python run_extract.py --category PAB --data-root "%DATA_ROOT%" --data-dir "%CD%\..\windows-extractor\output" 2>&1
set EXTRACT_RC=%errorlevel%
popd

if %EXTRACT_RC% NEQ 0 (
    echo.
    echo [extract] FAILED with code %EXTRACT_RC%
    exit /b %EXTRACT_RC%
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo  Extract complete.
echo  Output: %CD%\output\PAB\PAB.json
echo.
echo  Next: transfer to ANDROS:
echo    scp output\PAB\PAB.json andros@100.107.134.104:/opt/customers/^<slug^>/migration/PAB/
echo.
echo  Then trigger /api/migration/run from NEX Manager UI.
echo ═══════════════════════════════════════════════════════════════
endlocal
