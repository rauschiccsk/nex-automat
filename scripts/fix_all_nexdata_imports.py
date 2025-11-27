"""
Fix all imports: nex_shared → nexdata
"""

from pathlib import Path

NEXDATA_DIR = Path("packages/nexdata/nexdata")


def fix_imports_in_file(filepath: Path) -> bool:
    """Fix imports in single file"""

    if not filepath.exists():
        return False

    # Read file
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if needs fixing
    if "nex_shared" not in content:
        return False

    # Replace all occurrences
    original = content
    content = content.replace("from nex_shared.", "from nexdata.")
    content = content.replace("import nex_shared", "import nexdata")

    # Only write if changed
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True

    return False


def fix_all_imports():
    print("=" * 60)
    print("FIX: All imports nex_shared → nexdata")
    print("=" * 60)

    if not NEXDATA_DIR.exists():
        print(f"❌ Directory not found: {NEXDATA_DIR}")
        return False

    print(f"\n📁 Scanning: {NEXDATA_DIR}")
    print("-" * 60)

    # Find all Python files
    py_files = list(NEXDATA_DIR.rglob("*.py"))

    print(f"Found {len(py_files)} Python files\n")

    fixed_count = 0
    skipped_count = 0

    for filepath in py_files:
        relative_path = filepath.relative_to(NEXDATA_DIR)

        if fix_imports_in_file(filepath):
            print(f"✅ {relative_path}")
            fixed_count += 1
        else:
            skipped_count += 1

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"  ✅ Fixed:   {fixed_count}")
    print(f"  ⚪ Skipped: {skipped_count}")
    print(f"  📊 Total:   {len(py_files)}")
    print("=" * 60)

    if fixed_count > 0:
        print("\n📝 Next step:")
        print("   pip install -e packages/nexdata")
        print('   python -c "from nexdata import *"')

    return True


if __name__ == "__main__":
    success = fix_all_imports()
    exit(0 if success else 1)