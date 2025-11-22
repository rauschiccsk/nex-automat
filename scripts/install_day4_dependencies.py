"""
Install DAY 4 Missing Dependencies
Installs all dependencies discovered missing during DAY 4 testing
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Install DAY 4 critical dependencies"""

    print("=" * 80)
    print("INSTALLING DAY 4 DEPENDENCIES")
    print("=" * 80)
    print()

    # DAY 4 critical packages
    packages = [
        "pdfplumber>=0.11.8",
        "pytesseract>=0.3.13",
        "pdf2image>=1.17.0",
        "pg8000>=1.31.5"
    ]

    print(f"Installing {len(packages)} packages...")
    print()

    for i, package in enumerate(packages, 1):
        print(f"[{i}/{len(packages)}] Installing {package}...")

        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                capture_output=True,
                text=True,
                check=True
            )

            print(f"  [OK] {package.split('>=')[0]} installed")

        except subprocess.CalledProcessError as e:
            print(f"  [ERROR] Failed to install {package}")
            print(f"  {e.stderr}")
            return 1

    print()
    print("=" * 80)
    print("ALL DAY 4 DEPENDENCIES INSTALLED")
    print("=" * 80)
    print()
    print("Verification:")
    print("  python scripts/prepare_deployment.py")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())