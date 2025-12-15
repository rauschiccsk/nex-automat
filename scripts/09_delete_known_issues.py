#!/usr/bin/env python3
"""
Delete KNOWN_ISSUES.md-old - obsolete document.

DECISION: DELETE (not archive)

REASONS:
1. Extremely outdated (22.11.2025 vs today 15.12.2025)
2. All issues already fixed (pdfplumber, pg8000, env vars)
3. Pre-deployment checklist outdated (doesn't reflect v2.4)
4. No practical value - all info in current docs
5. Better documentation exists in SESSION_NOTES, PROJECT_ARCHIVE

ALTERNATIVE: If you want to keep for history, use script 08 pattern (archive)

USAGE:
    python scripts/09_delete_known_issues.py
"""

from pathlib import Path


def main():
    print("=" * 80)
    print("DELETE KNOWN_ISSUES.md-old")
    print("=" * 80)

    # Path
    file_to_delete = Path("docs/deployment/KNOWN_ISSUES.md-old")

    # Check if exists
    if not file_to_delete.exists():
        print(f"\n❌ ERROR: {file_to_delete} not found!")
        return

    print(f"\n📂 File: {file_to_delete}")

    # Read for info
    content = file_to_delete.read_text(encoding='utf-8')
    print(f"   Size: {len(content):,} bytes")
    print(f"   Lines: {len(content.splitlines()):,}")

    # Show reason
    print("\n📋 Deletion Reason:")
    print("   - Extremely outdated (22.11.2025, v2.0)")
    print("   - All 4 critical issues fixed")
    print("   - Pre-deployment checklist obsolete")
    print("   - No practical value")

    # Confirm
    response = input("\n⚠️  Confirm deletion? (yes/no): ").strip().lower()

    if response not in ['yes', 'y']:
        print("\n❌ Deletion cancelled.")
        return

    # Delete
    print("\n🗑️  Deleting file...")
    file_to_delete.unlink()
    print(f"   ✅ Deleted: {file_to_delete}")

    print("\n" + "=" * 80)
    print("✅ DONE!")
    print("=" * 80)

    # Count remaining
    remaining = list(Path("docs").rglob("*.md-old"))
    print(f"\n📂 Remaining .md-old files: {len(remaining)}")

    print("\n💡 Next file to process:")
    print("   - MAGERSTAV_DEPLOYMET_SUMMARY.md-old (4.5 KB)")
    print("   OR")
    print("   - GO_LIVE_CHECKLIST.md-old (6.3 KB)")


if __name__ == "__main__":
    main()