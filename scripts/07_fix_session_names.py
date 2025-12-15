#!/usr/bin/env python3
"""
Fix problematic session filenames with correct dates and better names.

PROBLEM:
- SESSION_2025-12-09_project-archive-session-2025-12-09.md (duplicate date)
- SESSION_unknown_project-archive-session-v23-migration.md (unknown date)
- SESSION_unknown_v24-phase4-deployment.md (unknown date)

SOLUTION:
- Manual rename with correct dates and descriptive names

USAGE:
    python scripts/07_fix_session_names.py
"""

from pathlib import Path


def main():
    print("=" * 80)
    print("FIX SESSION FILENAMES")
    print("=" * 80)

    sessions_dir = Path("docs/archive/sessions")

    # Define manual renames (old -> new)
    renames = [
        # Fix duplicate date (analyze content first, likely v2.4 completion)
        (
            "SESSION_2025-12-09_project-archive-session-2025-12-09.md",
            "SESSION_2025-12-09_v24-implementation-complete.md"
        ),
        # Fix unknown date for v2.3 migration (should be 2025-12-08)
        (
            "SESSION_unknown_project-archive-session-v23-migration.md",
            "SESSION_2025-12-08_v23-loader-migration.md"
        ),
        # Fix unknown date for v2.4 deployment (should be 2025-12-09)
        (
            "SESSION_unknown_v24-phase4-deployment.md",
            "SESSION_2025-12-09_v24-phase4-deployment.md"
        ),
    ]

    print("\n📝 Proposed renames:\n")
    for i, (old, new) in enumerate(renames, 1):
        old_path = sessions_dir / old
        if old_path.exists():
            print(f"{i}. {old}")
            print(f"   → {new}")
            print()
        else:
            print(f"{i}. ❌ NOT FOUND: {old}")
            print()

    response = input("Proceed with renaming? (yes/no): ").strip().lower()

    if response not in ['yes', 'y']:
        print("\n❌ Rename cancelled.")
        return

    # Perform renames
    print("\n🔄 Renaming files...")
    success = 0
    for old, new in renames:
        old_path = sessions_dir / old
        new_path = sessions_dir / new

        if not old_path.exists():
            print(f"⚠️  SKIP: {old} (not found)")
            continue

        if new_path.exists():
            print(f"❌ ERROR: {new} already exists!")
            continue

        try:
            old_path.rename(new_path)
            print(f"✅ Renamed: {new}")
            success += 1
        except Exception as e:
            print(f"❌ ERROR renaming {old}: {e}")

    print("\n" + "=" * 80)
    print(f"✅ DONE! Renamed {success}/{len(renames)} files")
    print("=" * 80)

    # List all files after rename
    print("\n📁 Final session files:\n")
    all_sessions = sorted(sessions_dir.glob("SESSION_*.md"))
    for session in all_sessions:
        print(f"   - {session.name}")


if __name__ == "__main__":
    main()