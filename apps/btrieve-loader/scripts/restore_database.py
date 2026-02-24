"""
Database Restore CLI Wrapper
Command-line interface for database restoration

Author: Zoltán Rausch, ICC Komárno
Date: 2025-11-21
"""

import argparse
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from backup.database_restore import DatabaseRestore


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Restore PostgreSQL database from backup"
    )

    parser.add_argument(
        "--config", default="config/config.yaml", help="Path to configuration file"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # List command
    list_parser = subparsers.add_parser("list", help="List available backups")
    list_parser.add_argument(
        "--type",
        choices=["daily", "weekly", "all"],
        default="all",
        help="Type of backups to list",
    )

    # Info command
    info_parser = subparsers.add_parser("info", help="Get restore point information")
    info_parser.add_argument("backup_path", help="Path to backup file")

    # Verify command
    verify_parser = subparsers.add_parser("verify", help="Verify backup integrity")
    verify_parser.add_argument("backup_path", help="Path to backup file")

    # Restore command
    restore_parser = subparsers.add_parser("restore", help="Restore database")
    restore_parser.add_argument("backup_path", help="Path to backup file")
    restore_parser.add_argument(
        "--drop", action="store_true", help="Drop existing database before restore"
    )
    restore_parser.add_argument(
        "--no-verify", action="store_true", help="Skip backup verification"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        restore = DatabaseRestore(args.config)

        if args.command == "list":
            backups = restore.list_backups(args.type)

            if not backups:
                print(f"No backups found (type: {args.type})")
                return 0

            print(f"\nAvailable backups ({len(backups)}):\n")
            for backup in backups:
                print(f"  {backup['name']}")
                print(f"    Type: {backup['type']}")
                print(f"    Size: {backup['size'] / 1024 / 1024:.2f} MB")
                print(
                    f"    Modified: {backup['modified'].strftime('%Y-%m-%d %H:%M:%S')}"
                )
                print(f"    Checksum: {'Yes' if backup['has_checksum'] else 'No'}")
                print()

        elif args.command == "info":
            info = restore.get_restore_point_info(args.backup_path)

            if "error" in info:
                print(f"Error: {info['error']}")
                return 1

            print("\nRestore Point Information:\n")
            print(f"  Name: {info['name']}")
            print(f"  Path: {info['path']}")
            print(f"  Timestamp: {info['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  Size: {info['size_mb']} MB ({info['size_bytes']} bytes)")
            print(f"  Verified: {'Yes' if info['verified'] else 'No'}")
            print(f"  Message: {info['verification_message']}")
            print()

        elif args.command == "verify":
            success, message = restore.verify_backup(args.backup_path)

            if success:
                print(f"✓ {message}")
                return 0
            else:
                print(f"✗ {message}")
                return 1

        elif args.command == "restore":
            print(f"\nRestoring database from: {args.backup_path}")

            if args.drop:
                print("⚠ WARNING: Existing database will be dropped!")
                response = input("Continue? (yes/no): ")
                if response.lower() != "yes":
                    print("Restore cancelled")
                    return 0

            success, message = restore.restore_database(
                args.backup_path,
                drop_existing=args.drop,
                verify_first=not args.no_verify,
            )

            if success:
                print(f"✓ {message}")
                return 0
            else:
                print(f"✗ {message}")
                return 1

        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
