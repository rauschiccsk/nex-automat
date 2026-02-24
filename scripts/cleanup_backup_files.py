"""
Script to find and remove all .backup files from the project.
Shows list of files before deletion and asks for confirmation.
"""

from pathlib import Path

# Paths
BASE_DIR = Path(r"C:\Development\nex-automat")

# Patterns to find
BACKUP_PATTERNS = [
    "*.backup",
    "*.backup_*",
    "*.backup[0-9]*",
    "*_backup",
    "*.before_*",
    "*.broken",
]


def find_backup_files(base_path: Path) -> list[Path]:
    """
    Find all backup files in the project.

    Returns:
        List of Path objects for backup files
    """
    backup_files = []

    for pattern in BACKUP_PATTERNS:
        # Find files matching pattern
        found = list(base_path.rglob(pattern))
        backup_files.extend(found)

    # Remove duplicates and sort
    backup_files = sorted(set(backup_files))

    return backup_files


def format_size(size: int) -> str:
    """Format file size in human-readable format."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"


def main():
    print("=" * 70)
    print("CLEANUP BACKUP FILES")
    print("=" * 70)
    print()

    print(f"Searching for backup files in: {BASE_DIR}")
    print(f"Patterns: {', '.join(BACKUP_PATTERNS)}")
    print()

    # Find backup files
    backup_files = find_backup_files(BASE_DIR)

    if not backup_files:
        print("✅ No backup files found!")
        return

    # Show statistics
    total_size = sum(f.stat().st_size for f in backup_files if f.exists())

    print(f"Found {len(backup_files)} backup files")
    print(f"Total size: {format_size(total_size)}")
    print()

    # Group by directory
    by_dir = {}
    for f in backup_files:
        dir_name = str(f.parent.relative_to(BASE_DIR))
        if dir_name not in by_dir:
            by_dir[dir_name] = []
        by_dir[dir_name].append(f)

    # Show files grouped by directory
    print("Files by directory:")
    print("-" * 70)
    for dir_name in sorted(by_dir.keys()):
        files = by_dir[dir_name]
        dir_size = sum(f.stat().st_size for f in files if f.exists())
        print(f"\n📁 {dir_name}/ ({len(files)} files, {format_size(dir_size)})")

        for f in sorted(files):
            size = f.stat().st_size if f.exists() else 0
            print(f"   - {f.name} ({format_size(size)})")

    print()
    print("=" * 70)

    # Ask for confirmation
    response = (
        input(f"\nDelete all {len(backup_files)} backup files? (yes/no): ")
        .strip()
        .lower()
    )

    if response != "yes":
        print("\n❌ Cancelled - no files deleted")
        return

    # Delete files
    print()
    print("Deleting files...")
    deleted_count = 0
    deleted_size = 0

    for f in backup_files:
        try:
            if f.exists():
                size = f.stat().st_size
                f.unlink()
                deleted_count += 1
                deleted_size += size
                print(f"   ✅ Deleted: {f.relative_to(BASE_DIR)}")
        except Exception as e:
            print(f"   ❌ Error deleting {f.name}: {e}")

    print()
    print("=" * 70)
    print("✅ CLEANUP COMPLETE")
    print(f"   Deleted: {deleted_count} files")
    print(f"   Freed space: {format_size(deleted_size)}")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Review changes: git status")
    print("2. Commit: git add -A && git commit -m 'Remove backup files'")
    print("3. Push: git push origin develop")


if __name__ == "__main__":
    main()
