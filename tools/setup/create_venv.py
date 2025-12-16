#!/usr/bin/env python3
"""
Virtual Environment Setup Utility
NEX Automat Project

Creates Python virtual environment for development.
Usage: python tools/setup/create_venv.py [options]
"""

import sys
import os
import venv
import shutil
import argparse
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


def check_python_version(min_version=(3, 11)):
    """Check if Python version meets minimum requirement"""
    print_step(1, "Checking Python version")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    print(f"Python version: {version_str}")

    if (version.major, version.minor) >= min_version:
        print(f"✓ Python version OK ({min_version[0]}.{min_version[1]}+)")
        return True
    else:
        print(f"⚠ Warning: Python {min_version[0]}.{min_version[1]}+ is recommended")
        return False


def create_venv_dir(project_dir, venv_name="venv", force=False):
    """Create virtual environment"""
    print_step(2, f"Creating virtual environment: {venv_name}")

    venv_path = project_dir / venv_name

    if venv_path.exists():
        print(f"⚠ {venv_name} directory already exists: {venv_path}")

        if force:
            print("Force mode: removing existing venv...")
            shutil.rmtree(venv_path)
        else:
            response = input("Do you want to recreate it? (y/n): ").strip().lower()
            if response != 'y':
                print("Using existing venv")
                return venv_path
            print("Removing existing venv...")
            shutil.rmtree(venv_path)

    print(f"Creating venv at: {venv_path}")
    venv.create(venv_path, with_pip=True)
    print(f"✓ Virtual environment '{venv_name}' created")

    return venv_path


def print_activation_instructions(venv_path):
    """Print activation instructions for current platform"""
    print_step(3, "Activation Instructions")

    venv_name = venv_path.name

    if sys.platform == "win32":
        print("To activate the virtual environment, run:")
        print(f"  .\\{venv_name}\\Scripts\\activate.ps1")
        print("\nIf you get execution policy error:")
        print(f"  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process")
        print(f"  .\\{venv_name}\\Scripts\\activate.ps1")
        print("\nOr use cmd.exe:")
        print(f"  {venv_name}\\Scripts\\activate.bat")
    else:
        print("To activate the virtual environment, run:")
        print(f"  source {venv_name}/bin/activate")

    print("\nAfter activation, verify with:")
    print("  python --version")
    print("  python -c \"import sys; print(sys.executable)\"")


def get_project_root():
    """Get project root directory"""
    # Try to find project root by looking for specific markers
    current = Path.cwd()

    # If we're already in nex-automat directory
    if current.name == "nex-automat" or (current / "init_chat").exists():
        return current

    # Try going up to find nex-automat
    for parent in current.parents:
        if parent.name == "nex-automat" or (parent / "init_chat").exists():
            return parent

    # Default to expected location
    default_path = Path("/")
    if default_path.exists():
        return default_path

    return current


def main():
    parser = argparse.ArgumentParser(
        description="Create Python virtual environment for NEX Automat project"
    )
    parser.add_argument(
        "--name",
        default="venv",
        help="Name of virtual environment directory (default: venv)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force recreate if venv exists (no prompt)"
    )
    parser.add_argument(
        "--dir",
        help="Project directory (default: auto-detect)"
    )

    args = parser.parse_args()

    print_header("Virtual Environment Setup - NEX Automat")

    # Determine project directory
    if args.dir:
        project_dir = Path(args.dir)
    else:
        project_dir = get_project_root()

    print(f"Project directory: {project_dir}")

    if not project_dir.exists():
        print(f"✗ Error: Project directory does not exist: {project_dir}")
        return 1

    # Change to project directory
    original_dir = Path.cwd()
    if Path.cwd() != project_dir:
        try:
            os.chdir(project_dir)
            print(f"✓ Changed to: {Path.cwd()}")
        except Exception as e:
            print(f"✗ Error changing directory: {e}")
            return 1

    # Step 1: Check Python version
    version_ok = check_python_version()

    # Step 2: Create venv
    venv_path = create_venv_dir(project_dir, args.name, args.force)

    # Step 3: Print activation instructions
    print_activation_instructions(venv_path)

    # Summary
    print_header("Setup Complete")
    print(f"✓ Virtual environment '{args.name}' ready at: {venv_path}")
    print("\nNext steps:")
    print(f"  1. Activate venv (see instructions above)")
    print(f"  2. Install dependencies: pip install -r requirements.txt")
    print(f"  3. Or for RAG: pip install -r requirements-rag.txt")

    return 0


if __name__ == "__main__":
    sys.exit(main())