"""
Migration script: Copy models from nex-genesis-server to nex-shared
Source: C:/Development/nex-genesis-server/src/models/
Target: C:/Development/nex-automat/packages/nex-shared/models/
"""

import shutil
from pathlib import Path

# Paths
SOURCE_DIR = Path("C:/Development/nex-genesis-server/src/models")
TARGET_DIR = Path("C:/Development/nex-automat/packages/nex-shared/models")

# Files to migrate
FILES_TO_MIGRATE = [
    "gscat.py",
    "barcode.py",
    "pab.py",
    "mglst.py"
]


def main():
    print("=" * 60)
    print("MIGRATION: Models from nex-genesis-server to nex-shared")
    print("=" * 60)

    # Check source directory
    if not SOURCE_DIR.exists():
        print(f"❌ ERROR: Source directory not found: {SOURCE_DIR}")
        return False

    # Check target directory
    if not TARGET_DIR.exists():
        print(f"❌ ERROR: Target directory not found: {TARGET_DIR}")
        return False

    print(f"\n✅ Source: {SOURCE_DIR}")
    print(f"✅ Target: {TARGET_DIR}")

    # Migrate files
    success_count = 0
    error_count = 0

    print(f"\n📋 Migrating {len(FILES_TO_MIGRATE)} files:")
    print("-" * 60)

    for filename in FILES_TO_MIGRATE:
        source_file = SOURCE_DIR / filename
        target_file = TARGET_DIR / filename

        if not source_file.exists():
            print(f"❌ {filename:<20} - Source not found")
            error_count += 1
            continue

        try:
            # Copy file
            shutil.copy2(source_file, target_file)

            # Get file size
            size = target_file.stat().st_size

            print(f"✅ {filename:<20} - Copied ({size:,} bytes)")
            success_count += 1

        except Exception as e:
            print(f"❌ {filename:<20} - Error: {e}")
            error_count += 1

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"  ✅ Success: {success_count}")
    print(f"  ❌ Failed:  {error_count}")
    print(f"  📊 Total:   {len(FILES_TO_MIGRATE)}")
    print("=" * 60)

    # List target directory
    if success_count > 0:
        print(f"\n📁 Target directory contents:")
        print(f"   {TARGET_DIR}")
        for file in sorted(TARGET_DIR.glob("*.py")):
            size = file.stat().st_size
            print(f"   - {file.name:<20} ({size:,} bytes)")

    return error_count == 0


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)