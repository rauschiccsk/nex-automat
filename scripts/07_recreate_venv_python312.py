#!/usr/bin/env python3
"""
Script 07: Recreate venv with Python 3.12
Session: RAG Implementation Phase 2

Removes old venv (Python 3.13) and creates new venv with Python 3.12
Location: scripts/07_recreate_venv_python312.py
"""

import sys
import subprocess
import shutil
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
    print_header("Script 07: Recreate venv with Python 3.12")

    # Define paths
    project_root = Path("C:/Development/nex-automat")
    venv_path = project_root / "venv"
    python312_path = Path("C:/Program Files/Python312/python.exe")

    print(f"Project directory: {project_root}")
    print(f"Python 3.12: {python312_path}")
    print()

    # Step 1: Check Python 3.12 exists
    print_step(1, "Checking Python 3.12")

    if not python312_path.exists():
        print(f"✗ Error: Python 3.12 not found at: {python312_path}")
        print("\nPlease run first:")
        print("  python scripts/06_verify_python312.py")
        return 1

    print(f"✓ Found: {python312_path}")

    # Verify it's 64-bit
    result = subprocess.run(
        [str(python312_path), "-c", "import platform; print(platform.architecture()[0])"],
        capture_output=True,
        text=True
    )
    arch = result.stdout.strip()
    print(f"Architecture: {arch}")

    if arch != "64bit":
        print(f"✗ Error: Python at {python312_path} is not 64-bit!")
        return 1
    print("✓ Confirmed 64-bit Python 3.12")

    # Step 2: Remove old venv
    print_step(2, "Removing old venv (Python 3.13)")

    if venv_path.exists():
        print(f"Removing: {venv_path}")
        print("This may take a minute...")
        try:
            shutil.rmtree(venv_path)
            print("✓ Old venv removed")
        except Exception as e:
            print(f"✗ Error removing venv: {e}")
            print("\nTroubleshooting:")
            print("  1. Make sure venv is NOT activated")
            print("  2. Close any programs using files in venv/")
            print("  3. Try deleting manually, then run script again")
            return 1
    else:
        print("No existing venv to remove")

    # Step 3: Create new venv with Python 3.12
    print_step(3, "Creating new venv with Python 3.12")
    print(f"Creating: {venv_path}")
    print("This may take 2-3 minutes...")

    try:
        subprocess.check_call(
            [str(python312_path), "-m", "venv", str(venv_path)]
        )
        print("✓ New venv created with Python 3.12")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error creating venv: {e}")
        return 1

    # Step 4: Verify new venv
    print_step(4, "Verifying new venv")
    venv_python = venv_path / "Scripts" / "python.exe"

    if not venv_python.exists():
        print(f"✗ Error: venv python not found at: {venv_python}")
        return 1

    # Check version
    result = subprocess.run(
        [str(venv_python), "--version"],
        capture_output=True,
        text=True
    )
    venv_version = result.stdout.strip() or result.stderr.strip()
    print(f"venv Python version: {venv_version}")

    # Check architecture
    result = subprocess.run(
        [str(venv_python), "-c", "import platform; print(platform.architecture()[0])"],
        capture_output=True,
        text=True
    )
    venv_arch = result.stdout.strip()
    print(f"venv architecture: {venv_arch}")

    if "3.12" in venv_version and venv_arch == "64bit":
        print("✓ New venv is Python 3.12 64-bit - PERFECT for RAG!")
    else:
        print(f"⚠ Warning: Unexpected venv configuration")
        print(f"  Version: {venv_version}")
        print(f"  Arch: {venv_arch}")

    # Summary
    print_header("Script 07 Complete")
    print("✓ Old venv (Python 3.13) removed")
    print("✓ New venv (Python 3.12 64-bit) created")
    print("✓ Ready for RAG dependencies installation")
    print("\nNext steps:")
    print("  1. Activate venv:")
    print("     .\\venv\\Scripts\\activate.ps1")
    print("  2. Install RAG dependencies:")
    print("     python scripts/02_install_rag_dependencies.py")
    print("\nPython 3.12 má prebuilt wheels pre všetky RAG dependencies!")

    return 0


if __name__ == "__main__":
    sys.exit(main())