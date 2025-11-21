#!/usr/bin/env python3
"""
COMPLETE: Deploy to Production Script
Replaces the placeholder version in scripts/deploy_to_production.py
"""

from pathlib import Path

BASE_PATH = Path(r"C:\Development\nex-automat")
TARGET_SCRIPT = BASE_PATH / "scripts" / "deploy_to_production.py"

FULL_SCRIPT = r'''#!/usr/bin/env python3
"""
Deploy NEX Automat from Development to Production
Copies project from C:\Development to C:\Deployment
"""

import shutil
import sys
from pathlib import Path

DEV_PATH = Path(r"C:\Development\nex-automat")
PROD_PATH = Path(r"C:\Deployment\nex-automat")

COPY_DIRS = ["apps", "packages", "docs", "scripts", "tools"]
COPY_FILES = ["pyproject.toml", "README.md"]

EXCLUDE_DIRS = {"__pycache__", ".pytest_cache", ".git", "venv", "venv32", 
                ".venv", "node_modules", "dist", "build", "*.egg-info"}

EXCLUDE_FILES = {"*.pyc", "*.pyo", "*.pyd", ".DS_Store", "Thumbs.db", 
                 "*.log", "*.backup", "*.backup2"}

def should_exclude(path: Path) -> bool:
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
        if part.startswith('.') and part not in ['.gitignore']:
            return True

    for pattern in EXCLUDE_FILES:
        if path.match(pattern):
            return True

    return False

def copy_directory(src: Path, dst: Path, description: str = ""):
    if not src.exists():
        print(f"  ⚠️  Source not found: {src}")
        return False

    print(f"  Copying {description or src.name}...")

    try:
        dst.mkdir(parents=True, exist_ok=True)

        copied = 0
        skipped = 0

        for item in src.rglob('*'):
            if should_exclude(item):
                skipped += 1
                continue

            rel_path = item.relative_to(src)
            dst_item = dst / rel_path

            if item.is_file():
                dst_item.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dst_item)
                copied += 1
            elif item.is_dir():
                dst_item.mkdir(parents=True, exist_ok=True)

        print(f"    ✅ Copied {copied} files (skipped {skipped})")
        return True

    except Exception as e:
        print(f"    ❌ Error: {e}")
        return False

def copy_file(src: Path, dst: Path):
    if not src.exists():
        print(f"  ⚠️  File not found: {src}")
        return False

    print(f"  Copying {src.name}...")

    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"    ✅ Copied")
        return True
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return False

def create_venv():
    print("\nCreating production virtual environment...")

    venv_path = PROD_PATH / "venv32"

    if venv_path.exists():
        print(f"  ✅ Virtual environment already exists")
        return True

    try:
        import subprocess

        python_cmd = "py"
        args = ["-3.13-32"]

        result = subprocess.run(
            [python_cmd] + args + ["-m", "venv", str(venv_path)],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"  ✅ Created venv32")
            return True
        else:
            print(f"  ❌ Failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def install_dependencies():
    print("\nInstalling dependencies...")

    venv_python = PROD_PATH / "venv32" / "Scripts" / "python.exe"

    if not venv_python.exists():
        print(f"  ❌ Python not found")
        return False

    try:
        import subprocess

        print("  Upgrading pip...")
        subprocess.run(
            [str(venv_python), "-m", "pip", "install", "--upgrade", "pip"],
            capture_output=True
        )

        packages = [
            str(PROD_PATH / "packages" / "invoice-shared"),
            str(PROD_PATH / "packages" / "nex-shared"),
            str(PROD_PATH / "apps" / "supplier-invoice-loader"),
        ]

        for package in packages:
            package_path = Path(package)
            if package_path.exists():
                print(f"  Installing {package_path.name}...")
                result = subprocess.run(
                    [str(venv_python), "-m", "pip", "install", "-e", package],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    print(f"    ✅ Installed")
                else:
                    print(f"    ❌ Failed")
                    return False

        return True

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def verify_deployment():
    print("\nVerifying deployment...")

    checks = [
        (PROD_PATH / "apps" / "supplier-invoice-loader", "Application"),
        (PROD_PATH / "packages" / "invoice-shared", "Shared package"),
        (PROD_PATH / "scripts", "Scripts"),
        (PROD_PATH / "venv32", "Virtual environment"),
        (PROD_PATH / "venv32" / "Scripts" / "python.exe", "Python executable"),
    ]

    all_ok = True
    for path, name in checks:
        if path.exists():
            print(f"  ✅ {name}")
        else:
            print(f"  ❌ {name} missing")
            all_ok = False

    return all_ok

def main():
    print("=" * 70)
    print("DEPLOY TO PRODUCTION")
    print("=" * 70)
    print()
    print(f"Source:      {DEV_PATH}")
    print(f"Destination: {PROD_PATH}")
    print()

    response = input("Continue? (y/N): ").strip().lower()
    if response != 'y':
        print("Cancelled")
        sys.exit(0)

    print()
    print("Copying directories...")
    for dir_name in COPY_DIRS:
        copy_directory(DEV_PATH / dir_name, PROD_PATH / dir_name, dir_name)

    print("\nCopying files...")
    for file_name in COPY_FILES:
        copy_file(DEV_PATH / file_name, PROD_PATH / file_name)

    if not create_venv():
        print("\n❌ Failed to create virtual environment")
        sys.exit(1)

    if not install_dependencies():
        print("\n❌ Failed to install dependencies")
        sys.exit(1)

    if not verify_deployment():
        print("\n❌ Deployment verification failed")
        sys.exit(1)

    print()
    print("=" * 70)
    print("✅ DEPLOYMENT COMPLETE")
    print("=" * 70)
    print()
    print("Next: python scripts/install_nssm.py (in C:\\Deployment\\nex-automat)")
    print()

if __name__ == "__main__":
    main()
'''


def main():
    print("=" * 70)
    print("INSTALL COMPLETE deploy_to_production.py")
    print("=" * 70)
    print()

    # Backup existing
    if TARGET_SCRIPT.exists():
        backup = TARGET_SCRIPT.with_suffix('.py.old')
        import shutil
        shutil.copy2(TARGET_SCRIPT, backup)
        print(f"✅ Backed up to: {backup.name}")

    # Write new script
    with open(TARGET_SCRIPT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(FULL_SCRIPT)

    print(f"✅ Created: {TARGET_SCRIPT}")
    print()
    print("=" * 70)
    print("✅ READY FOR DEPLOYMENT")
    print("=" * 70)
    print()
    print("Run deployment:")
    print("  python scripts/deploy_to_production.py")
    print()


if __name__ == "__main__":
    main()