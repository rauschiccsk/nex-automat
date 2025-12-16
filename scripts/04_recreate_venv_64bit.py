#!/usr/bin/env python3
"""
Script 04: Recreate venv with 64-bit Python
Session: RAG Implementation Phase 2

Removes old 32-bit venv and creates new 64-bit venv
Location: scripts/04_recreate_venv_64bit.py
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
    print_header("Script 04: Recreate venv with 64-bit Python")

    # Define paths
    project_root = Path("C:/Development/nex-automat")
    venv_path = project_root / "venv"
    python64_path = Path("C:/Program Files/Python313/python.exe")

    print(f"Project directory: {project_root}")
    print(f"64-bit Python: {python64_path}")
    print()

    # Step 1: Check 64-bit Python exists
    print_step(1, "Checking 64-bit Python")
    if not python64_path.exists():
        print(f"✗ Error: 64-bit Python not found at: {python64_path}")
        return 1
    print(f"✓ Found: {python64_path}")

    # Verify it's 64-bit
    result = subprocess.run(
        [str(python64_path), "-c", "import platform; print(platform.architecture()[0])"],
        capture_output=True,
        text=True
    )
    arch = result.stdout.strip()
    print(f"Architecture: {arch}")

    if arch != "64bit":
        print(f"✗ Error: Python at {python64_path} is not 64-bit!")
        return 1
    print("✓ Confirmed 64-bit Python")

    # Step 2: Remove old venv
    print_step(2, "Removing old 32-bit venv")
    if venv_path.exists():
        print(f"Removing: {venv_path}")
        try:
            shutil.rmtree(venv_path)
            print("✓ Old venv removed")
        except Exception as e:
            print(f"✗ Error removing venv: {e}")
            print("\nTry manually:")
            print(f"  1. Deactivate venv if active")
            print(f"  2. Delete folder: {venv_path}")
            return 1
    else:
        print("No existing venv to remove")

    # Step 3: Create new venv with 64-bit Python
    print_step(3, "Creating new venv with 64-bit Python")
    print(f"Creating: {venv_path}")
    print("This may take a minute...")

    try:
        subprocess.check_call(
            [str(python64_path), "-m", "venv", str(venv_path)]
        )
        print("✓ New 64-bit venv created")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error creating venv: {e}")
        return 1

    # Step 4: Verify new venv
    print_step(4, "Verifying new venv")
    venv_python = venv_path / "Scripts" / "python.exe"

    if not venv_python.exists():
        print(f"✗ Error: venv python not found at: {venv_python}")
        return 1

    result = subprocess.run(
        [str(venv_python), "-c", "import platform; print(platform.architecture()[0])"],
        capture_output=True,
        text=True
    )
    venv_arch = result.stdout.strip()
    print(f"New venv architecture: {venv_arch}")

    if venv_arch == "64bit":
        print("✓ New venv is 64-bit - READY for RAG!")
    else:
        print(f"✗ Error: New venv is still {venv_arch}")
        return 1

    # Summary
    print_header("Script 04 Complete")
    print("✓ Old 32-bit venv removed")
    print("✓ New 64-bit venv created")
    print("✓ Ready for RAG dependencies")
    print("\nNext steps:")
    print("  1. Activate venv: .\\venv\\Scripts\\activate.ps1")
    print("  2. Install RAG dependencies: python scripts/02_install_rag_dependencies.py")

    return 0


if __name__ == "__main__":
    sys.exit(main())