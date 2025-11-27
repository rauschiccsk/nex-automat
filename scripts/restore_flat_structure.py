"""
Restore FLAT structure for nex-shared package
Move everything from nex_shared/ back to root
"""

import shutil
from pathlib import Path

BASE_DIR = Path("packages/nex-shared")
NEX_SHARED_DIR = BASE_DIR / "nex_shared"
PYPROJECT = BASE_DIR / "pyproject.toml"


def restore_flat_structure():
    print("=" * 60)
    print("RESTORE: Flat structure for nex-shared")
    print("=" * 60)

    if not NEX_SHARED_DIR.exists():
        print(f"✅ Already flat structure")
        return True

    # Get all items in nex_shared/
    items = list(NEX_SHARED_DIR.iterdir())

    print(f"\n📋 Moving {len(items)} items from nex_shared/ to root:")
    print("-" * 60)

    moved = 0
    for item in items:
        target = BASE_DIR / item.name

        # Skip if target exists
        if target.exists():
            print(f"⚠️  {item.name:<20} - Already exists in root, skipping")
            continue

        try:
            shutil.move(str(item), str(target))
            print(f"✅ {item.name:<20} - Moved to root")
            moved += 1
        except Exception as e:
            print(f"❌ {item.name:<20} - Error: {e}")

    # Remove empty nex_shared/ directory
    if NEX_SHARED_DIR.exists() and not list(NEX_SHARED_DIR.iterdir()):
        NEX_SHARED_DIR.rmdir()
        print(f"\n🗑️  Removed empty: nex_shared/")

    # Fix pyproject.toml
    print(f"\n📄 Fixing: {PYPROJECT}")
    print("-" * 60)

    if not PYPROJECT.exists():
        print("❌ pyproject.toml not found")
        return False

    # Read pyproject.toml
    with open(PYPROJECT, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace packages line
    if 'packages = ["nex_shared"]' in content:
        content = content.replace(
            'packages = ["nex_shared"]',
            'packages = ["."]'
        )

        with open(PYPROJECT, "w", encoding="utf-8") as f:
            f.write(content)

        print('✅ Changed: packages = ["nex_shared"] → packages = ["."]')
    else:
        print('✅ pyproject.toml already correct')

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"  ✅ Items moved: {moved}")
    print("=" * 60)

    # Show structure
    print(f"\n📁 Correct FLAT structure:")
    print(f"   packages/nex-shared/")
    print(f"   ├── models/           ← PRIAMO tu")
    print(f"   ├── btrieve/")
    print(f"   ├── repositories/")
    print(f"   ├── __init__.py")
    print(f"   ├── pyproject.toml")
    print(f"   └── README.md")

    print("\n📝 Next step:")
    print("   pip install -e packages/nex-shared")

    return True


if __name__ == "__main__":
    success = restore_flat_structure()
    exit(0 if success else 1)