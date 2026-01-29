"""Configuration Backup Module - Minimal Version"""

import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional


class ConfigBackup:
    """Simple config file backup."""

    def __init__(self, backup_dir: str):
        self.backup_dir = Path(backup_dir)
        self.config_backup_dir = self.backup_dir / "config"
        self.config_backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self, config_files: list[Path]) -> Path | None:
        """Create config backup."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"config_backup_{timestamp}"
        backup_path = self.config_backup_dir / backup_name
        backup_path.mkdir(exist_ok=True)

        for config_file in config_files:
            if config_file.exists():
                shutil.copy2(config_file, backup_path / config_file.name)

        return backup_path

    def list_backups(self) -> list:
        """List all backups."""
        return sorted(self.config_backup_dir.glob("config_backup_*"), reverse=True)
