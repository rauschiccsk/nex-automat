#!/usr/bin/env python3
"""
Database Backup Script - CLI Wrapper
Automated PostgreSQL backup with rotation, compression, and verification.
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from backup.database_backup import DatabaseBackup, load_config


def main():
    """Main entry point for backup script."""
    parser = argparse.ArgumentParser(description="Database backup utility")
    parser.add_argument("--config", required=True, help="Path to configuration file")
    parser.add_argument(
        "--type", choices=["daily", "weekly"], default="daily", help="Backup type"
    )
    parser.add_argument("--backup-dir", default="backups", help="Backup directory")
    parser.add_argument("--verify", help="Verify existing backup file")
    parser.add_argument("--list", action="store_true", help="List all backups")
    parser.add_argument("--rotate", action="store_true", help="Rotate old backups only")

    args = parser.parse_args()

    try:
        config = load_config(args.config)
        db_config = config.get("database", {}).get("postgres", {})
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)

    backup_manager = DatabaseBackup(
        backup_dir=args.backup_dir,
        db_config=db_config,
        retention_days=7,
        retention_weeks=4,
    )

    if args.verify:
        backup_file = Path(args.verify)
        if backup_manager._verify_backup(backup_file):
            print(f"✓ Backup verified: {backup_file}")
            sys.exit(0)
        else:
            print(f"✗ Verification failed: {backup_file}")
            sys.exit(1)

    elif args.list:
        backups = backup_manager.list_backups()
        print("\n=== Daily Backups ===")
        for backup in backups["daily"]:
            print(f"  {backup['filename']} - {backup['size']:,} bytes")
        print("\n=== Weekly Backups ===")
        for backup in backups["weekly"]:
            print(f"  {backup['filename']} - {backup['size']:,} bytes")
        sys.exit(0)

    elif args.rotate:
        daily_removed, weekly_removed = backup_manager.rotate_backups()
        print(
            f"Rotation complete: {daily_removed} daily, {weekly_removed} weekly removed"
        )
        sys.exit(0)

    else:
        backup_file = backup_manager.create_backup(backup_type=args.type)
        if backup_file:
            backup_manager.rotate_backups()
            print(f"✓ Backup successful: {backup_file}")
            sys.exit(0)
        else:
            print("✗ Backup failed")
            sys.exit(1)


if __name__ == "__main__":
    main()
