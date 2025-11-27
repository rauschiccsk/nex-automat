"""
Fix repository files - correct model import names
"""

from pathlib import Path

REPOS_DIR = Path("packages/nexdata/nexdata/repositories")


def fix_repository_file(filepath: Path) -> bool:
    """Fix imports in repository file"""

    if not filepath.exists():
        return False

    # Read file
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Fix BARCODERecord → BarcodeRecord
    content = content.replace("BARCODERecord", "BarcodeRecord")

    # Write if changed
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True

    return False


def fix_all_repositories():
    print("=" * 60)
    print("FIX: Repository model imports")
    print("=" * 60)

    if not REPOS_DIR.exists():
        print(f"❌ Directory not found: {REPOS_DIR}")
        return False

    print(f"\n📁 Scanning: {REPOS_DIR}")
    print("-" * 60)

    # Files to fix
    files_to_fix = [
        REPOS_DIR / "barcode_repository.py"
    ]

    fixed_count = 0

    for filepath in files_to_fix:
        if not filepath.exists():
            print(f"⚠️  {filepath.name} - Not found")
            continue

        if fix_repository_file(filepath):
            print(f"✅ {filepath.name} - Fixed")
            fixed_count += 1
        else:
            print(f"✅ {filepath.name} - No changes needed")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"  ✅ Fixed: {fixed_count}")
    print("=" * 60)

    print("\n📋 Fixed:")
    print("   - BARCODERecord → BarcodeRecord")

    print("\n📝 Next step:")
    print('   python -c "from nexdata import *"')

    return True


if __name__ == "__main__":
    success = fix_all_repositories()
    exit(0 if success else 1)