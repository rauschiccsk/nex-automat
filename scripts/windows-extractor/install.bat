@echo off
REM NEX Extract — one-time install on Windows
REM Creates 32-bit venv, installs dependencies, verifies Btrieve DLL.

setlocal

REM ─────────────────────────────────────────────────────────────
REM 1. Sanity check: must be 32-bit Python 3.11+
REM ─────────────────────────────────────────────────────────────
where python >NUL 2>&1
if errorlevel 1 (
    echo ERROR: python not found in PATH.
    echo Install Python 3.11 32-bit from https://www.python.org/downloads/
    echo and tick "Add to PATH" during setup.
    exit /b 1
)

for /f "tokens=*" %%v in ('python -c "import sys; print(sys.version_info[0]*100+sys.version_info[1])"') do set PYVER=%%v
if %PYVER% LSS 311 (
    echo ERROR: Python 3.11+ required, found:
    python --version
    exit /b 1
)

for /f "tokens=*" %%b in ('python -c "import struct; print(struct.calcsize('P')*8)"') do set PYBITS=%%b
if not "%PYBITS%"=="32" (
    echo ERROR: 32-bit Python required, found %PYBITS%-bit.
    echo Btrieve DLL is 32-bit and Python must match for ctypes to work.
    echo Reinstall from https://www.python.org/downloads/release/python-3110/
    echo and pick "Windows installer (32-bit)".
    exit /b 1
)

echo [install] Python 3.11 32-bit OK.

REM ─────────────────────────────────────────────────────────────
REM 2. Create venv32
REM ─────────────────────────────────────────────────────────────
if not exist venv32 (
    echo [install] Creating venv32...
    python -m venv venv32
)
call venv32\Scripts\activate.bat

REM ─────────────────────────────────────────────────────────────
REM 3. Install requirements
REM ─────────────────────────────────────────────────────────────
echo [install] Installing dependencies...
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt --quiet

REM nexdata is a path-installable package — needs the source tree.
REM If user copied this windows-extractor/ as a standalone bundle, nexdata
REM should be at ..\..\packages\nexdata. If not, we need to ship a copy.
if exist "..\..\packages\nexdata" (
    echo [install] Installing nexdata from local source...
    python -m pip install -e "..\..\packages\nexdata" --quiet
) else if exist "nexdata" (
    echo [install] Installing bundled nexdata...
    python -m pip install -e "nexdata" --quiet
) else (
    echo ERROR: nexdata package not found.
    echo Either run from a full nex-automat-src checkout, or copy
    echo packages\nexdata\ next to this script.
    exit /b 1
)

REM ─────────────────────────────────────────────────────────────
REM 4. Verify Btrieve DLL is reachable
REM ─────────────────────────────────────────────────────────────
echo [install] Checking Btrieve DLL reachability...
python -c "import ctypes; ctypes.WinDLL('w3btrv7.dll')" 2>NUL
if errorlevel 1 (
    python -c "import ctypes; ctypes.WinDLL('wbtrv32.dll')" 2>NUL
    if errorlevel 1 (
        echo WARNING: Neither w3btrv7.dll nor wbtrv32.dll loadable from current PATH.
        echo Extract will fail at runtime. NEX Genesis must be installed and its
        echo Btrieve runtime registered ^(usually in C:\Windows\SysWOW64\^).
        echo.
        echo Continue anyway? Press Ctrl+C to abort, or:
        pause
    ) else (
        echo [install] wbtrv32.dll OK.
    )
) else (
    echo [install] w3btrv7.dll OK.
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo  Installation complete.
echo  Next: run extract-pab.bat ^<DATA_ROOT^>
echo  Example: extract-pab.bat C:\ICC\NEX
echo ═══════════════════════════════════════════════════════════════
endlocal
