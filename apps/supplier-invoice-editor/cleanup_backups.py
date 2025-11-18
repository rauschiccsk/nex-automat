#!/usr/bin/env python3
"""
Cleanup Backup Files
Removes all *.backup and *.backup2 files from project
"""

from pathlib import Path


def find_backup_files():
    """Find all backup files in project"""
    backup_files = []

    # Search in root and subdirectories
    for pattern in ['*.backup', '*.backup2']:
        backup_files.extend(Path('.').rglob(pattern))

    return backup_files


def main():
    """Main cleanup function"""
    print("=" * 60)
    print("BACKUP FILES CLEANUP")
    print("=" * 60)

    # Find backups
    backup_files = find_backup_files()

    if not backup_files:
        print("\n✓ No backup files found - already clean!")
        return 0

    # List files
    print(f"\nFound {len(backup_files)} backup files:")
    for backup_file in backup_files:
        print(f"  • {backup_file}")

    # Confirm deletion
    print(f"\n⚠️  This will DELETE {len(backup_files)} files!")
    response = input("Continue? (yes/no): ").strip().lower()

    if response not in ['yes', 'y']:
        print("\n✗ Cleanup cancelled")
        return 0

    # Delete files
    print("\nDeleting backup files...")
    deleted_count = 0

    for backup_file in backup_files:
        try:
            backup_file.unlink()
            print(f"  ✓ Deleted: {backup_file}")
            deleted_count += 1
        except Exception as e:
            print(f"  ✗ Failed to delete {backup_file}: {e}")

    # Summary
    print("\n" + "=" * 60)
    print(f"CLEANUP COMPLETE: {deleted_count}/{len(backup_files)} files deleted")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    exit(main())