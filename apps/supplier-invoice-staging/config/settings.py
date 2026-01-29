"""Configuration"""

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    database: str = "supplier_invoice_staging"
    user: str = "postgres"
    password: str = ""


@dataclass
class Settings:
    app_root: Path = field(default_factory=lambda: Path(__file__).parent.parent)
    config_file: Path = field(default_factory=lambda: Path(__file__).parent / "config.yaml")
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    default_margin_percent: float = 25.0
    default_vat_rate: float = 20.0

    def __post_init__(self):
        self._load_from_yaml()
        self._load_from_env()

    def _load_from_yaml(self):
        if self.config_file.exists():
            with open(self.config_file, encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
            db = config.get("database", {})
            self.database.host = db.get("host", self.database.host)
            self.database.port = db.get("port", self.database.port)
            self.database.database = db.get("database", self.database.database)
            self.database.user = db.get("user", self.database.user)
            self.database.password = db.get("password", self.database.password)
            ui = config.get("ui", {})
            self.default_margin_percent = ui.get("default_margin_percent", self.default_margin_percent)
            self.default_vat_rate = ui.get("default_vat_rate", self.default_vat_rate)

    def _load_from_env(self):
        if pw := os.environ.get("POSTGRES_PASSWORD"):
            self.database.password = pw

    def get_settings_db_path(self) -> Path:
        return self.app_root / "data" / "settings.db"
