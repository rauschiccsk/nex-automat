#!/usr/bin/env python3
"""
Script 01: Create setup.py for nex-shared package
Creates proper Python package setup with namespace mapping
"""

from pathlib import Path

# Target location
SETUP_PATH = Path("packages/nex-shared/setup.py")

# Setup.py content
SETUP_CONTENT = '''"""
nex-shared package setup
Shared components for NEX Automat applications
"""

from setuptools import setup, find_packages

setup(
    name="nex-shared",
    version="1.0.0",
    description="Shared components for NEX Automat applications",
    author="ICC Komárno",
    python_requires=">=3.8",

    # Map nex_shared namespace to current directory (FLAT structure)
    package_dir={'nex_shared': '.'},

    # Define packages with nex_shared namespace
    packages=[
        'nex_shared.ui',
        'nex_shared.database',
    ],

    # Include package data
    package_data={
        'nex_shared.ui': ['*.py'],
        'nex_shared.database': ['*.py'],
    },

    # Dependencies
    install_requires=[
        'PyQt5>=5.15.0',
    ],

    # Development dependencies
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-qt>=4.0.0',
        ],
    },

    # Project URLs
    url="https://github.com/rauschiccsk/nex-automat",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
'''


def main():
    """Create setup.py file"""
    print("=" * 60)
    print("Creating setup.py for nex-shared package")
    print("=" * 60)

    # Verify target directory exists
    package_dir = SETUP_PATH.parent
    if not package_dir.exists():
        print(f"❌ ERROR: Package directory not found: {package_dir}")
        return False

    # Verify required subdirectories exist
    ui_dir = package_dir / "ui"
    db_dir = package_dir / "database"

    if not ui_dir.exists():
        print(f"❌ ERROR: UI directory not found: {ui_dir}")
        return False

    if not db_dir.exists():
        print(f"❌ ERROR: Database directory not found: {db_dir}")
        return False

    print(f"\n✅ Package directory verified: {package_dir}")
    print(f"✅ UI directory exists: {ui_dir}")
    print(f"✅ Database directory exists: {db_dir}")

    # Create setup.py
    SETUP_PATH.write_text(SETUP_CONTENT, encoding='utf-8')
    print(f"\n✅ Created: {SETUP_PATH}")

    # Verify content
    content = SETUP_PATH.read_text(encoding='utf-8')
    if "package_dir={'nex_shared': '.'}" in content:
        print("✅ Namespace mapping configured correctly")

    if "nex_shared.ui" in content and "nex_shared.database" in content:
        print("✅ Packages defined correctly")

    print("\n" + "=" * 60)
    print("ÚSPECH: setup.py vytvorený")
    print("=" * 60)
    print("\nNext step: pip install -e packages/nex-shared")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)