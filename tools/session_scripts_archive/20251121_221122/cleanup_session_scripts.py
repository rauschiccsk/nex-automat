#!/usr/bin/env python3
"""
Cleanup Session Scripts - Remove temporary utility scripts from project root
Archives helper scripts created during development session
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

BASE_PATH = Path(r"C:\Development\nex-automat")
ARCHIVE_DIR = BASE_PATH / "tools" / "session_scripts_archive"

# Scripts to archive (created during session, not needed in production)
TEMP_SCRIPTS = [
    "create_test_config.py",
    "update_production_paths.py",
    "fix_all_config_scripts.py",
    "fix_config_errors.py",
    "final_config_fix.py",
    "fix_validator_env_vars.py",
    "fix_missing_os_import.py",
    "fix_env_vars_in_config.py",
    "auto_deploy_service_scripts.py",
    "complete_deploy_to_production.py",
    "update_gitignore.py",
    "deploy_config_tools.py",
    "cleanup_session_scripts.py",  # This script itself
]

# Backup files to remove
BACKUP_PATTERNS = [
    "*.backup",
    "*.backup2",
    "*.old",
    "*.bak",
]

def create_archive_dir():
    """Create archive directory with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = ARCHIVE_DIR / timestamp
    archive_path.mkdir(parents=True, exist_ok=True)
    return archive_path

def archive_file(filepath: Path, archive_path: Path) -> bool:
    """Archive a single file"""
    if not filepath.exists():
        return False

    try:
        dest = archive_path / filepath.name
        shutil.move(str(filepath), str(dest))
        return True
    except Exception as e:
        print(f"  ❌ Error archiving {filepath.name}: {e}")
        return False

def remove_backups():
    """Remove backup files"""
    print("\nRemoving backup files...")
    removed = 0

    for pattern in BACKUP_PATTERNS:
        for filepath in BASE_PATH.rglob(pattern):
            # Skip files in .git, venv, etc.
            if any(part.startswith('.') or part in ['venv', 'venv32', 'node_modules']
                   for part in filepath.parts):
                continue

            try:
                filepath.unlink()
                print(f"  ✅ Removed: {filepath.name}")
                removed += 1
            except Exception as e:
                print(f"  ❌ Error removing {filepath.name}: {e}")

    return removed

def main():
    print("=" * 70)
    print("CLEANUP SESSION SCRIPTS")
    print("=" * 70)
    print()
    print("This will archive temporary utility scripts to:")
    print(f"  {ARCHIVE_DIR}")
    print()
    print("Scripts to archive:")
    for script in TEMP_SCRIPTS:
        filepath = BASE_PATH / script
        status = "✅" if filepath.exists() else "⚠️  (not found)"
        print(f"  {status} {script}")

    print()
    response = input("Continue? (y/N): ").strip().lower()
    if response != 'y':
        print("Cancelled")
        return

    # Create archive directory
    print("\nCreating archive...")
    archive_path = create_archive_dir()
    print(f"  ✅ Created: {archive_path}")

    # Archive scripts
    print("\nArchiving scripts...")
    archived = 0
    for script in TEMP_SCRIPTS:
        filepath = BASE_PATH / script
        if archive_file(filepath, archive_path):
            print(f"  ✅ Archived: {script}")
            archived += 1
        elif filepath.exists():
            print(f"  ⚠️  Exists but not archived: {script}")

    # Remove backups
    removed = remove_backups()

    # Summary
    print()
    print("=" * 70)
    print("✅ CLEANUP COMPLETE")
    print("=" * 70)
    print()
    print(f"Archived: {archived} scripts")
    print(f"Removed:  {removed} backup files")
    print(f"Location: {archive_path}")
    print()
    print("Production scripts remain in:")
    print("  scripts/create_production_config.py")
    print("  scripts/validate_config.py")
    print("  scripts/test_database_connection.py")
    print("  scripts/install_nssm.py")
    print("  scripts/create_windows_service.py")
    print("  scripts/manage_service.py")
    print("  scripts/deploy_to_production.py")
    print()
    print("Ready for Git commit!")
    print()

if __name__ == "__main__":
    main()