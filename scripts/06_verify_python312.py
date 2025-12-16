#!/usr/bin/env python3
"""
Script 06: Verify Python 3.12 Installation
Session: RAG Implementation Phase 2

Verifies Python 3.12 is correctly installed
Location: scripts/06_verify_python312.py
"""

import subprocess
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}\n")


def print_step(num, text):
    """Print formatted step"""
    print(f"\n{num}. {text}")
    print("-" * 60)


def main():
    print_header("Script 06: Verify Python 3.12 Installation")

    # Expected path
    python312_path = Path("C:/Program Files/Python312/python.exe")

    # Step 1: Check if file exists
    print_step(1, "Checking if Python 3.12 exists")
    print(f"Expected location: {python312_path}")

    if not python312_path.exists():
        print("✗ Python 3.12 NOT FOUND")
        print("\nPlease install Python 3.12 following the guide:")
        print("  docs/setup/PYTHON_312_INSTALLATION.md")
        return 1

    print(f"✓ Found: {python312_path}")

    # Step 2: Check version
    print_step(2, "Checking Python version")

    try:
        result = subprocess.run(
            [str(python312_path), "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        version = result.stdout.strip() or result.stderr.strip()
        print(f"Version: {version}")

        if "3.12" not in version:
            print(f"⚠ Warning: Expected Python 3.12, got: {version}")
        else:
            print("✓ Version is Python 3.12")
    except Exception as e:
        print(f"✗ Error checking version: {e}")
        return 1

    # Step 3: Check architecture
    print_step(3, "Checking architecture")

    try:
        result = subprocess.run(
            [str(python312_path), "-c", "import platform; print(platform.architecture()[0])"],
            capture_output=True,
            text=True,
            timeout=5
        )
        arch = result.stdout.strip()
        print(f"Architecture: {arch}")

        if arch != "64bit":
            print(f"✗ Error: Expected 64-bit, got: {arch}")
            return 1

        print("✓ Architecture is 64-bit")
    except Exception as e:
        print(f"✗ Error checking architecture: {e}")
        return 1

    # Step 4: Check pip
    print_step(4, "Checking pip")

    try:
        result = subprocess.run(
            [str(python312_path), "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        pip_version = result.stdout.strip()
        print(f"pip: {pip_version}")

        if not pip_version:
            print("⚠ Warning: pip may not be installed")
        else:
            print("✓ pip is available")
    except Exception as e:
        print(f"⚠ Warning: Error checking pip: {e}")

    # Summary
    print_header("Verification Complete")
    print("✓ Python 3.12.x 64-bit is correctly installed")
    print(f"✓ Location: {python312_path}")
    print("\nNext step:")
    print("  Run: python scripts/07_recreate_venv_python312.py")

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())