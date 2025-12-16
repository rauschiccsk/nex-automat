#!/usr/bin/env python3
"""
Script 05: Find installed Python versions
Session: RAG Implementation Phase 2

Searches for installed Python versions on the system
Location: scripts/05_find_python_versions.py
"""

import os
import subprocess
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}\n")


def check_python_executable(python_path):
    """Check Python version for given executable"""
    try:
        result = subprocess.run(
            [str(python_path), "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        version = result.stdout.strip() or result.stderr.strip()

        # Get architecture
        result_arch = subprocess.run(
            [str(python_path), "-c", "import platform; print(platform.architecture()[0])"],
            capture_output=True,
            text=True,
            timeout=5
        )
        arch = result_arch.stdout.strip()

        return version, arch
    except:
        return None, None


def main():
    print_header("Find Installed Python Versions")

    # Common Python installation paths
    search_paths = [
        Path("C:/Program Files/Python*"),
        Path("C:/Program Files (x86)/Python*"),
        Path("C:/Python*"),
        Path("C:/Users") / os.getenv("USERNAME", "") / "AppData/Local/Programs/Python/Python*"
    ]

    found_pythons = []

    print("Searching for Python installations...\n")

    # Search in common paths
    for pattern in search_paths:
        parent = pattern.parent
        glob_pattern = pattern.name

        if not parent.exists():
            continue

        for path in parent.glob(glob_pattern):
            python_exe = path / "python.exe"
            if python_exe.exists():
                version, arch = check_python_executable(python_exe)
                if version:
                    found_pythons.append((python_exe, version, arch))

    # Display results
    if not found_pythons:
        print("✗ No Python installations found")
        return 1

    print(f"Found {len(found_pythons)} Python installation(s):\n")

    python312_64bit = None

    for i, (path, version, arch) in enumerate(found_pythons, 1):
        print(f"{i}. {path}")
        print(f"   Version: {version}")
        print(f"   Architecture: {arch}")

        # Check if this is Python 3.12 64-bit
        if "3.12" in version and arch == "64bit":
            python312_64bit = path
            print("   ✓ RECOMMENDED for RAG (Python 3.12 64-bit)")
        elif "3.11" in version and arch == "64bit":
            if not python312_64bit:
                python312_64bit = path
            print("   ✓ ACCEPTABLE for RAG (Python 3.11 64-bit)")
        elif arch == "32bit":
            print("   ⚠ 32-bit (not suitable for RAG)")

        print()

    # Recommendation
    print_header("Recommendation")

    if python312_64bit:
        print(f"✓ Use Python 3.12/3.11 64-bit for RAG:")
        print(f"  {python312_64bit}")
        print("\nNext steps:")
        print(f"  1. Recreate venv with this Python")
        print(f"  2. Script will be generated automatically")
    else:
        print("✗ Python 3.12 64-bit not found")
        print("\nRecommendation:")
        print("  1. Download Python 3.12 64-bit from:")
        print("     https://www.python.org/downloads/release/python-3120/")
        print("  2. Install to: C:\\Program Files\\Python312\\")
        print("  3. Run this script again")

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
    sys.exit(main())