# Run unit tests for supplier-invoice-loader

import subprocess
import sys
from pathlib import Path

DEV_ROOT = Path(r"C:\Development\nex-automat")
LOADER_APP = DEV_ROOT / "apps" / "supplier-invoice-loader"

print("=" * 70)
print("RUNNING UNIT TESTS - SUPPLIER-INVOICE-LOADER")
print("=" * 70)
print(f"Location: {LOADER_APP}")
print("=" * 70)

# Change to app directory
import os
os.chdir(LOADER_APP)

print(f"\nWorking directory: {os.getcwd()}\n")

# Run pytest with verbose output
cmd = [
    sys.executable,
    "-m", "pytest",
    "tests/",
    "-v",
    "--tb=short",
    "--color=yes"
]

print(f"Command: {' '.join(cmd)}\n")
print("=" * 70)

result = subprocess.run(cmd, capture_output=False)

print("\n" + "=" * 70)
if result.returncode == 0:
    print("✅ ALL TESTS PASSED")
else:
    print(f"❌ TESTS FAILED (exit code: {result.returncode})")
print("=" * 70)

sys.exit(result.returncode)