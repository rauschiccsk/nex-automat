#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cleanup NEX Automat Monorepo
Remove backup files, temporary files, and old migration scripts
"""

from pathlib import Path
import os

MONOREPO_ROOT = Path("C:/Development/nex-automat")

# Patterns to remove
BACKUP_PATTERNS = [
    "*.backup",
    "*.backup[0-9]",
    "*.backup2",
    "*.bak",
    "*.old",
]

TEMP_PATTERNS = [
    "*.tmp",
    "*.temp",
    "*~",
]

# Old migration scripts to archive
MIGRATION_SCRIPTS = [
    "setup_nex_automat_monorepo.py",
    "copy_projects_to_monorepo.py",
    "create_invoice_shared.py",
    "update_all_imports.py",
    "fix_workspace_dependencies.py",
    "fix_root_pyproject.py",
    "fix_hatch_build_config.py",
    "fix_extraction_test.py",
    "fix_all_broken_tests.py",
    "add_missing_dependencies.py",
    "fix_monitoring_optional_psutil.py",
    "fix_conftest_metrics.py",
    "fix_import_and_monitoring_errors.py",
    "fix_remaining_test_errors.py",
    "fix_monitoring_tests.py",
    "fix_final_api_tests.py",
]

# Test script to remove
TEST_SCRIPTS = [
    "create_editor_tests.py",
]


def find_files_by_patterns(root: Path, patterns: list[str]) -> list[Path]:
    """Find files matching patterns"""
    found = []
    for pattern in patterns:
        found.extend(root.rglob(pattern))
    return found


def main():
    """Main cleanup execution"""
    print("=" * 70)
    print("CLEANUP NEX AUTOMAT MONOREPO")
    print("=" * 70)
    print()

    stats = {
        'backup_files': 0,
        'temp_files': 0,
        'migration_scripts': 0,
        'test_scripts': 0,
        'total_size': 0,
    }

    # 1. Find backup files
    print("1️⃣ Searching for backup files...")
    backup_files = find_files_by_patterns(MONOREPO_ROOT, BACKUP_PATTERNS)

    if backup_files:
        print(f"   Found {len(backup_files)} backup files:")
        for f in backup_files:
            size = f.stat().st_size
            stats['total_size'] += size
            rel_path = f.relative_to(MONOREPO_ROOT)
            print(f"   - {rel_path} ({size:,} bytes)")
        stats['backup_files'] = len(backup_files)
    else:
        print("   ✅ No backup files found")
    print()

    # 2. Find temp files
    print("2️⃣ Searching for temp files...")
    temp_files = find_files_by_patterns(MONOREPO_ROOT, TEMP_PATTERNS)

    if temp_files:
        print(f"   Found {len(temp_files)} temp files:")
        for f in temp_files:
            size = f.stat().st_size
            stats['total_size'] += size
            rel_path = f.relative_to(MONOREPO_ROOT)
            print(f"   - {rel_path} ({size:,} bytes)")
        stats['temp_files'] = len(temp_files)
    else:
        print("   ✅ No temp files found")
    print()

    # 3. Find migration scripts
    print("3️⃣ Checking migration scripts...")
    migration_found = []
    for script in MIGRATION_SCRIPTS:
        script_path = MONOREPO_ROOT / script
        if script_path.exists():
            migration_found.append(script_path)

    if migration_found:
        print(f"   Found {len(migration_found)} migration scripts:")
        for f in migration_found:
            size = f.stat().st_size
            stats['total_size'] += size
            print(f"   - {f.name} ({size:,} bytes)")
        stats['migration_scripts'] = len(migration_found)
    else:
        print("   ✅ No migration scripts found")
    print()

    # 4. Find test creation scripts
    print("4️⃣ Checking test scripts...")
    test_found = []
    for script in TEST_SCRIPTS:
        script_path = MONOREPO_ROOT / script
        if script_path.exists():
            test_found.append(script_path)

    if test_found:
        print(f"   Found {len(test_found)} test scripts:")
        for f in test_found:
            size = f.stat().st_size
            stats['total_size'] += size
            print(f"   - {f.name} ({size:,} bytes)")
        stats['test_scripts'] = len(test_found)
    else:
        print("   ✅ No test scripts found")
    print()

    # Summary
    total_files = (
            stats['backup_files'] +
            stats['temp_files'] +
            stats['migration_scripts'] +
            stats['test_scripts']
    )

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Backup files:       {stats['backup_files']:>6}")
    print(f"Temp files:         {stats['temp_files']:>6}")
    print(f"Migration scripts:  {stats['migration_scripts']:>6}")
    print(f"Test scripts:       {stats['test_scripts']:>6}")
    print("-" * 70)
    print(f"Total files:        {total_files:>6}")
    print(f"Total size:         {stats['total_size']:>6,} bytes ({stats['total_size'] / 1024:.1f} KB)")
    print()

    if total_files == 0:
        print("✅ Nothing to cleanup - monorepo is clean!")
        print("=" * 70)
        return

    # Confirm deletion
    print("=" * 70)
    print("ACTION REQUIRED")
    print("=" * 70)
    print()
    response = input("Delete these files? [y/N]: ").strip().lower()

    if response != 'y':
        print("❌ Cleanup cancelled")
        print("=" * 70)
        return

    # Archive migration scripts instead of deleting
    archive_dir = MONOREPO_ROOT / "tools" / "migration_scripts"
    archive_dir.mkdir(parents=True, exist_ok=True)

    # Delete backup and temp files
    deleted = 0
    archived = 0

    print()
    print("🗑️ Deleting files...")

    for f in backup_files + temp_files + test_found:
        try:
            f.unlink()
            deleted += 1
            print(f"   ✅ Deleted: {f.relative_to(MONOREPO_ROOT)}")
        except Exception as e:
            print(f"   ❌ Failed to delete {f.name}: {e}")

    # Archive migration scripts
    if migration_found:
        print()
        print("📦 Archiving migration scripts...")
        for f in migration_found:
            try:
                dest = archive_dir / f.name
                f.rename(dest)
                archived += 1
                print(f"   ✅ Archived: {f.name} → tools/migration_scripts/")
            except Exception as e:
                print(f"   ❌ Failed to archive {f.name}: {e}")

    print()
    print("=" * 70)
    print("CLEANUP COMPLETE!")
    print("=" * 70)
    print(f"✅ {deleted} files deleted")
    print(f"📦 {archived} scripts archived")
    print(f"💾 {stats['total_size']:,} bytes freed")
    print()
    print(f"Archived scripts location: tools/migration_scripts/")
    print("=" * 70)


if __name__ == "__main__":
    main()