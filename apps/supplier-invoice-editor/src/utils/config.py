# src/utils/config.py
"""Configuration Loader for Invoice Editor"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """Configuration manager for Invoice Editor"""

    def __init__(self, config_path: Optional[Path] = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"

        self.config_path = config_path
        self._config: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f)

        self._expand_env_vars(self._config)

    def _expand_env_vars(self, config: Dict[str, Any]) -> None:
        """Expand environment variables"""
        for key, value in config.items():
            if isinstance(value, dict):
                self._expand_env_vars(value)
            elif isinstance(value, str):
                if value.startswith('${ENV:') and value.endswith('}'):
                    env_var = value[6:-1]
                    config[key] = os.environ.get(env_var, value)

    def get(self, key_path: str, default: Any = None) -> Any:
        """Get config value by dot-notation path"""
        keys = key_path.split('.')
        value = self._config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def get_postgres_config(self) -> Dict[str, Any]:
        """Get PostgreSQL configuration"""
        return self._config.get('database', {}).get('postgres', {})

    def get_nex_genesis_config(self) -> Dict[str, Any]:
        """Get NEX Genesis configuration"""
        return self._config.get('database', {}).get('nex_genesis', {})

    @property
    def nex_root_path(self) -> Path:
        """Get NEX Genesis root path"""
        return Path(self.get('database.nex_genesis.root_path', 'C:\\NEX'))

    @property
    def nex_stores_path(self) -> Path:
        """Get NEX Genesis stores path"""
        return Path(self.get('database.nex_genesis.stores_path', 'C:\\NEX\\YEARACT\\STORES'))


# Singleton instance
_config_instance: Optional[Config] = None


def load_config(config_path: Optional[Path] = None) -> Config:
    """Load configuration (singleton pattern)"""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_path)
    return _config_instance


def get_config() -> Config:
    """Get config singleton instance"""
    if _config_instance is None:
        raise RuntimeError("Config not loaded. Call load_config() first.")
    return _config_instance
