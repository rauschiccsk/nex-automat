#!/usr/bin/env python3
"""
Download and install NSSM (Non-Sucking Service Manager)
"""

import os
import sys
import urllib.request
import zipfile
import shutil
from pathlib import Path

NSSM_VERSION = "2.24"
NSSM_URL = f"https://nssm.cc/release/nssm-{NSSM_VERSION}.zip"
TOOLS_DIR = Path(r"C:\Deployment\nex-automat\tools")
NSSM_DIR = TOOLS_DIR / "nssm"

def download_nssm():
    """Download NSSM"""
    print("Downloading NSSM...")

    TOOLS_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = TOOLS_DIR / f"nssm-{NSSM_VERSION}.zip"

    if zip_path.exists():
        print(f"  ✅ Already downloaded: {zip_path}")
        return zip_path

    try:
        print(f"  Downloading from: {NSSM_URL}")
        urllib.request.urlretrieve(NSSM_URL, zip_path)
        print(f"  ✅ Downloaded to: {zip_path}")
        return zip_path
    except Exception as e:
        print(f"  ❌ Download failed: {e}")
        print("\n  Manual download:")
        print(f"    1. Download from: {NSSM_URL}")
        print(f"    2. Save to: {zip_path}")
        print(f"    3. Run this script again")
        return None

def extract_nssm(zip_path: Path):
    """Extract NSSM"""
    print("\nExtracting NSSM...")

    if NSSM_DIR.exists():
        print(f"  ✅ Already extracted: {NSSM_DIR}")
        return True

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(TOOLS_DIR)

        extracted = TOOLS_DIR / f"nssm-{NSSM_VERSION}"
        if extracted.exists():
            extracted.rename(NSSM_DIR)

        print(f"  ✅ Extracted to: {NSSM_DIR}")
        return True
    except Exception as e:
        print(f"  ❌ Extraction failed: {e}")
        return False

def get_nssm_exe():
    """Get NSSM executable path"""
    nssm_exe = NSSM_DIR / "win32" / "nssm.exe"
    if nssm_exe.exists():
        return nssm_exe

    nssm_exe_64 = NSSM_DIR / "win64" / "nssm.exe"
    if nssm_exe_64.exists():
        return nssm_exe_64

    return None

def verify_installation():
    """Verify NSSM installation"""
    print("\nVerifying installation...")

    nssm_exe = get_nssm_exe()

    if not nssm_exe:
        print("  ❌ NSSM executable not found")
        return False

    print(f"  ✅ NSSM executable: {nssm_exe}")

    try:
        import subprocess
        result = subprocess.run(
            [str(nssm_exe), "version"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            print(f"  ✅ NSSM version: {result.stdout.strip()}")
            return True
        else:
            print(f"  ❌ NSSM test failed")
            return False
    except Exception as e:
        print(f"  ❌ NSSM test error: {e}")
        return False

def main():
    print("=" * 70)
    print("NSSM INSTALLATION")
    print("=" * 70)
    print()

    zip_path = download_nssm()
    if not zip_path:
        sys.exit(1)

    if not extract_nssm(zip_path):
        sys.exit(1)

    if not verify_installation():
        sys.exit(1)

    print()
    print("=" * 70)
    print("✅ NSSM INSTALLATION COMPLETE")
    print("=" * 70)
    print()
    print(f"NSSM Location: {get_nssm_exe()}")
    print()
    print("Next: python scripts/create_windows_service.py")
    print()

if __name__ == "__main__":
    main()
