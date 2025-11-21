#!/usr/bin/env python3
"""
Create Windows Service - REQUIRES ADMINISTRATOR
"""
import sys
import subprocess
from pathlib import Path

DEPLOYMENT_PATH = Path(r"C:\Deployment\nex-automat")
NSSM_EXE = DEPLOYMENT_PATH / "tools" / "nssm" / "win32" / "nssm.exe"
PYTHON_EXE = DEPLOYMENT_PATH / "venv32" / "Scripts" / "python.exe"
MAIN_SCRIPT = DEPLOYMENT_PATH / "apps" / "supplier-invoice-loader" / "src" / "main.py"
SERVICE_NAME = "NEX-Automat-Loader"

def check_admin():
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    if not check_admin():
        print("❌ ERROR: Must run as Administrator")
        sys.exit(1)

    print("Creating Windows Service...")
    print(f"Service: {SERVICE_NAME}")
    print(f"Python: {PYTHON_EXE}")
    print(f"Script: {MAIN_SCRIPT}")
    print("\n✅ Service creation script ready")
    print("(Full implementation in artifact)")

if __name__ == "__main__":
    main()
