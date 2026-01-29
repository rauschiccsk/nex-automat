#!/usr/bin/env python3
"""
Cleanup Project - Remove Temporary Setup Files
===============================================
Removes one-time setup scripts that are no longer needed

Session: 2 - Cleanup after PRIORITY 2 completion
"""

from pathlib import Path


def confirm_deletion(file_path: Path) -> bool:
    """Ask user to confirm file deletion"""
    print(f"\n📄 File: {file_path}")
    if file_path.exists():
        size = file_path.stat().st_size
        print(f"   Size: {size} bytes")
        response = input("   Delete? (y/n): ").strip().lower()
        return response == "y"
    else:
        print("   ⏭️  File not found (already deleted?)")
        return False


def delete_file(file_path: Path) -> bool:
    """Delete file safely"""
    try:
        if file_path.exists():
            file_path.unlink()
            print(f"   ✅ Deleted: {file_path.name}")
            return True
        else:
            print(f"   ⏭️  Not found: {file_path.name}")
            return False
    except Exception as e:
        print(f"   ❌ Error deleting {file_path.name}: {e}")
        return False


def main():
    """Main cleanup process"""
    print("=" * 60)
    print("INVOICE EDITOR - PROJECT CLEANUP")
    print("=" * 60)
    print("\nRemoving temporary setup scripts...")
    print("These files were used once during initial setup.")

    # Files to delete
    files_to_delete = [
        Path("scripts/copy_btrieve_components.py"),
        Path("scripts/fix_imports.py"),
        Path("install_dependencies.py"),
        Path("tests/test_imports.py"),
    ]

    deleted_count = 0
    skipped_count = 0

    print("\n" + "=" * 60)
    print("FILES TO REMOVE")
    print("=" * 60)

    for file_path in files_to_delete:
        if confirm_deletion(file_path):
            if delete_file(file_path):
                deleted_count += 1
        else:
            print(f"   ⏭️  Skipped: {file_path.name}")
            skipped_count += 1

    # Check if scripts/ directory is empty
    scripts_dir = Path("scripts")
    if scripts_dir.exists() and not any(scripts_dir.iterdir()):
        print("\n📁 Directory 'scripts/' is empty")
        response = input("   Remove empty directory? (y/n): ").strip().lower()
        if response == "y":
            scripts_dir.rmdir()
            print("   ✅ Removed: scripts/")

    # Summary
    print("\n" + "=" * 60)
    print("CLEANUP SUMMARY")
    print("=" * 60)
    print(f"✅ Deleted: {deleted_count} files")
    print(f"⏭️  Skipped: {skipped_count} files")

    # Show remaining project structure
    print("\n" + "=" * 60)
    print("CLEAN PROJECT STRUCTURE")
    print("=" * 60)
    print("""
supplier-invoice-editor/
├── config/
│   └── config.yaml              ✅ Configuration
├── database/
│   └── schemas/
│       └── 001_initial_schema.sql  ✅ PostgreSQL schema
├── docs/                        ✅ Documentation
├── logs/                        ✅ Application logs
├── src/
│   ├── __init__.py
│   ├── btrieve/                 ✅ Btrieve client
│   ├── models/                  ✅ Data models
│   ├── database/                (next: PostgreSQL client)
│   ├── business/                (future: Business logic)
│   ├── ui/                      (future: Qt5 UI)
│   └── utils/                   ✅ Utilities
├── tests/                       ✅ Test suite
├── main.py                      (future: Entry point)
└── requirements.txt             ✅ Dependencies
    """)

    print("=" * 60)
    print("✅ CLEANUP COMPLETE!")
    print("=" * 60)
    print("\nProject is now clean and ready for development.")
    print("Next: PRIORITY 3 - PostgreSQL Connection Module")


if __name__ == "__main__":
    main()
