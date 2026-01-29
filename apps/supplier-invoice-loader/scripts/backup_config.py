#!/usr/bin/env python3
"""Config Backup CLI - Minimal Version"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from backup.config_backup import ConfigBackup


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--config-files", nargs="+", required=True)
    parser.add_argument("--backup-dir", default="backups")
    args = parser.parse_args()

    backup = ConfigBackup(args.backup_dir)
    result = backup.create_backup([Path(f) for f in args.config_files])

    if result:
        print(f"✓ Backup created: {result}")
    else:
        print("✗ Backup failed")


if __name__ == "__main__":
    main()
