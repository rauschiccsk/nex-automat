#!/usr/bin/env python3
"""
Script 02: Install RAG Dependencies
Session: RAG Implementation Phase 2

Installs dependencies from requirements-rag.txt
Location: scripts/02_install_rag_dependencies.py
"""

import sys
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


def check_venv():
    """Check if virtual environment is activated"""
    print_step(1, "Checking virtual environment")

    python_path = Path(sys.executable)
    print(f"Python executable: {python_path}")

    if "venv" in str(python_path):
        print("✓ Virtual environment is active")
        return True
    else:
        print("⚠ WARNING: Virtual environment does NOT appear to be active!")
        print("\nPlease activate venv first:")
        print("  .\\venv\\Scripts\\activate.ps1")
        response = input("\nContinue anyway? (y/n): ").strip().lower()
        return response == 'y'


def upgrade_pip():
    """Upgrade pip to latest version"""
    print_step(2, "Upgrading pip")

    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("✓ pip upgraded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠ Warning: pip upgrade failed: {e}")
        return False


def install_dependencies(requirements_file):
    """Install dependencies from requirements file"""
    print_step(3, f"Installing dependencies from {requirements_file}")

    if not requirements_file.exists():
        print(f"✗ Error: {requirements_file} not found!")
        return False

    print(f"Requirements file: {requirements_file}")
    print("\nThis may take several minutes (downloading ~1.5 GB)...")
    print("Installing packages...\n")

    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)]
        )
        print("\n✓ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error: Installation failed: {e}")
        return False


def verify_installation():
    """Verify key packages are installed"""
    print_step(4, "Verifying installation")

    packages = [
        "sentence_transformers",
        "asyncpg",
        "pydantic",
        "tiktoken",
        "numpy",
        "yaml"
    ]

    all_ok = True
    for package in packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - NOT FOUND")
            all_ok = False

    return all_ok


def main():
    print_header("Script 02: Install RAG Dependencies")

    # Define paths
    project_root = Path.cwd()
    requirements_file = project_root / "requirements-rag.txt"

    print(f"Project directory: {project_root}")

    # Step 1: Check venv
    if not check_venv():
        print("\n✗ Aborting installation")
        return 1

    # Step 2: Upgrade pip
    upgrade_pip()

    # Step 3: Install dependencies
    if not install_dependencies(requirements_file):
        return 1

    # Step 4: Verify installation
    if not verify_installation():
        print("\n⚠ Some packages failed to install correctly")
        return 1

    # Summary
    print_header("Script 02 Complete")
    print("✓ All RAG dependencies installed and verified")
    print("\nInstalled packages:")
    print("  - sentence-transformers (embeddings)")
    print("  - asyncpg (PostgreSQL)")
    print("  - pydantic (validation)")
    print("  - tiktoken (tokenization)")
    print("  - numpy, PyYAML, python-dotenv, tqdm")
    print("\nNext: Create RAG module structure (Step 2.3)")

    return 0


if __name__ == "__main__":
    sys.exit(main())