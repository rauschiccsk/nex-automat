#!/usr/bin/env python3
"""
Script 25: Delete obsolete INDEX.md-old (database)
Reason: Replaced by docs/database/00_DATABASE_INDEX.md
"""

from pathlib import Path


def main():
    """Delete obsolete database index."""

    # Target file
    old_index = Path(r"C:\Development\nex-automat\docs\architecture\database\INDEX.md-old")

    print("=" * 70)
    print("Script 25: Delete Obsolete Database Index")
    print("=" * 70)

    # Check if exists
    if not old_index.exists():
        print(f"\n❌ File not found: {old_index}")
        return False

    print(f"\n📄 File to delete:")
    print(f"   {old_index}")
    print(f"   Size: {old_index.stat().st_size:,} bytes")

    # Confirm
    print(f"\n⚠️  Reason: Replaced by docs/database/00_DATABASE_INDEX.md")
    print(f"   - Obsolete after Batch 4 systematic reorganization")
    print(f"   - Contains outdated progress statistics")
    print(f"   - References relocated documents")

    # Delete
    try:
        old_index.unlink()
        print(f"\n✅ File deleted successfully")
        return True
    except Exception as e:
        print(f"\n❌ Error deleting file: {e}")
        return False


if __name__ == "__main__":
    success = main()
    print("\n" + "=" * 70)
    if success:
        print("✅ Migration complete - INDEX.md-old deleted")
        print("\nNext steps:")
        print("1. Update docs.json manifest")
        print("2. Continue with next .md-old file")
    else:
        print("❌ Migration failed")
    print("=" * 70)