"""
Fix nex-shared package structure
Move everything into nex_shared/ subfolder
"""

import shutil
from pathlib import Path

BASE_DIR = Path("packages/nex-shared")
NEX_SHARED_DIR = BASE_DIR / "nex_shared"

# Folders to move
FOLDERS = [
    "models",
    "btrieve",
    "repositories",
    "auth",
    "database",
    "monitoring",
    "utils"
]

# Files to move
FILES = [
    "__init__.py"
]


def fix_structure():
    print("=" * 60)
    print("FIX: nex-shared package structure")
    print("=" * 60)

    if not BASE_DIR.exists():
        print(f"❌ Base directory not found: {BASE_DIR}")
        return False

    # Create nex_shared directory
    print(f"\n📁 Creating: {NEX_SHARED_DIR}")
    NEX_SHARED_DIR.mkdir(exist_ok=True)
    print("✅ Created")

    # Move folders
    print(f"\n📋 Moving {len(FOLDERS)} folders:")
    print("-" * 60)

    moved_folders = 0
    for folder in FOLDERS:
        source = BASE_DIR / folder
        target = NEX_SHARED_DIR / folder

        if not source.exists():
            print(f"⚠️  {folder:<20} - Not found, skipping")
            continue

        if target.exists():
            print(f"⚠️  {folder:<20} - Already exists, skipping")
            continue

        try:
            shutil.move(str(source), str(target))
            print(f"✅ {folder:<20} - Moved")
            moved_folders += 1
        except Exception as e:
            print(f"❌ {folder:<20} - Error: {e}")

    # Move files
    print(f"\n📋 Moving {len(FILES)} files:")
    print("-" * 60)

    moved_files = 0
    for file in FILES:
        source = BASE_DIR / file
        target = NEX_SHARED_DIR / file

        if not source.exists():
            print(f"⚠️  {file:<20} - Not found, skipping")
            continue

        if target.exists():
            print(f"⚠️  {file:<20} - Already exists, skipping")
            continue

        try:
            shutil.move(str(source), str(target))
            print(f"✅ {file:<20} - Moved")
            moved_files += 1
        except Exception as e:
            print(f"❌ {file:<20} - Error: {e}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"  ✅ Folders moved: {moved_folders}")
    print(f"  ✅ Files moved:   {moved_files}")
    print("=" * 60)

    # Show new structure
    print(f"\n📁 New structure:")
    print(f"   {BASE_DIR}/")
    print(f"   ├── nex_shared/")
    print(f"   │   ├── __init__.py")
    print(f"   │   ├── models/")
    print(f"   │   ├── btrieve/")
    print(f"   │   ├── repositories/")
    print(f"   │   └── ...")
    print(f"   ├── pyproject.toml")
    print(f"   └── README.md")

    print("\n📝 Next step:")
    print("   pip install -e packages/nex-shared")

    return True


if __name__ == "__main__":
    success = fix_structure()
    exit(0 if success else 1)