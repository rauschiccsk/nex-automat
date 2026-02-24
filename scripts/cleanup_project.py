"""
Cleanup NEX Automat Project
Odstráni nepotrebné súbory a priečinky
"""

import shutil
from pathlib import Path


def remove_dir(path: Path, description: str):
    """Odstráň priečinok"""
    if path.exists():
        shutil.rmtree(path)
        print(
            f"✅ Removed: {path.relative_to(Path('C:/Development/nex-automat'))} - {description}"
        )
        return True
    return False


def remove_file(path: Path, description: str):
    """Odstráň súbor"""
    if path.exists():
        path.unlink()
        print(
            f"✅ Removed: {path.relative_to(Path('C:/Development/nex-automat'))} - {description}"
        )
        return True
    return False


def cleanup_nex_shared():
    """Vyčisti nex-shared package"""
    print("=" * 80)
    print("CLEANING NEX-SHARED PACKAGE")
    print("=" * 80)
    print()

    base = Path("C:/Development/nex-automat/packages/nex-shared/nex_shared")

    # Remove unnecessary directories
    removed = 0
    removed += remove_dir(base / "auth", "Auth module (not needed)")
    removed += remove_dir(base / "database", "Database module (not needed)")
    removed += remove_dir(base / "monitoring", "Monitoring module (not needed)")

    if removed == 0:
        print("✓ No unnecessary directories found")

    print()


def cleanup_scripts():
    """Vyčisti obsolete skripty"""
    print("=" * 80)
    print("CLEANING OBSOLETE SCRIPTS")
    print("=" * 80)
    print()

    base = Path("C:/Development/nex-automat/scripts")

    # Obsolete scripts (replaced by better versions)
    obsolete = [
        ("setup_nex_shared_package.py", "Replaced by create_nex_shared_files.py"),
        ("install_nex_shared.py", "Replaced by reinstall_nex_shared.py"),
        ("diagnose_nex_shared.py", "Replaced by diagnose_site_packages.py"),
        ("fix_nex_shared_files.py", "Temporary fix script (obsolete)"),
    ]

    removed = 0
    for filename, reason in obsolete:
        removed += remove_file(base / filename, reason)

    if removed == 0:
        print("✓ No obsolete scripts found")

    print()


def cleanup_temp_files():
    """Vyčisti temporary súbory"""
    print("=" * 80)
    print("CLEANING TEMPORARY FILES")
    print("=" * 80)
    print()

    base = Path("C:/Development/nex-automat")

    # Patterns to clean
    patterns = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/.pytest_cache",
        "**/.coverage",
    ]

    removed = 0
    for pattern in patterns:
        for path in base.glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                removed += 1
            elif path.is_file():
                path.unlink()
                removed += 1

    if removed > 0:
        print(f"✅ Removed {removed} temporary files/directories")
    else:
        print("✓ No temporary files found")

    print()


def cleanup_backup_files():
    """Vyčisti backup súbory"""
    print("=" * 80)
    print("CLEANING BACKUP FILES")
    print("=" * 80)
    print()

    base = Path("C:/Development/nex-automat")

    # Backup patterns
    patterns = [
        "**/*.bak",
        "**/*~",
        "**/*.tmp",
    ]

    removed = 0
    for pattern in patterns:
        for path in base.glob(pattern):
            if path.is_file():
                path.unlink()
                print(f"✅ Removed: {path.relative_to(base)}")
                removed += 1

    if removed == 0:
        print("✓ No backup files found")

    print()


def show_current_structure():
    """Zobraz aktuálnu štruktúru nex-shared"""
    print("=" * 80)
    print("CURRENT NEX-SHARED STRUCTURE")
    print("=" * 80)
    print()

    base = Path("C:/Development/nex-automat/packages/nex-shared/nex_shared")

    if not base.exists():
        print("❌ nex_shared directory not found!")
        return

    def print_tree(path: Path, prefix: str = ""):
        """Rekurzívne vypíš strom"""
        items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))

        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            connector = "└── " if is_last else "├── "
            print(f"{prefix}{connector}{item.name}")

            if item.is_dir() and item.name != "__pycache__":
                extension = "    " if is_last else "│   "
                print_tree(item, prefix + extension)

    print("nex_shared/")
    print_tree(base, "")
    print()


def show_scripts_structure():
    """Zobraz aktuálnu štruktúru scripts"""
    print("=" * 80)
    print("CURRENT SCRIPTS STRUCTURE")
    print("=" * 80)
    print()

    base = Path("C:/Development/nex-automat/scripts")

    if not base.exists():
        print("❌ scripts directory not found!")
        return

    scripts = sorted([f for f in base.glob("*.py") if f.is_file()])

    for script in scripts:
        size = script.stat().st_size
        print(f"  {script.name:<40} ({size:>6} bytes)")

    print()


def main():
    """Main execution"""

    print("=" * 80)
    print("NEX AUTOMAT PROJECT CLEANUP")
    print("=" * 80)
    print()

    # Run cleanups
    cleanup_nex_shared()
    cleanup_scripts()
    cleanup_temp_files()
    cleanup_backup_files()

    # Show results
    show_current_structure()
    show_scripts_structure()

    print("=" * 80)
    print("✅ CLEANUP COMPLETE")
    print("=" * 80)
    print()
    print("Project is now clean and ready.")
    print()


if __name__ == "__main__":
    main()
