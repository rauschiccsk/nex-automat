"""
Configuration for Supplier Invoice Editor
"""

import os
from nex_config.database import DB_NAME_STAGING, DB_PORT


class Config:
    """Configuration class compatible with postgres_client expectations"""

    def __init__(self):
        """Initialize config with database connection parameters"""
        password = os.getenv("POSTGRES_PASSWORD", "")

        # Primary config - flat structure for direct access
        self._config = {
            "host": "localhost",
            "port": DB_PORT,
            "database": os.getenv("STAGING_DB_NAME", DB_NAME_STAGING),
            "user": "postgres",
            "password": password,
        }

        # Also provide nested structure for compatibility
        self._config["database.postgres"] = {
            "host": "localhost",
            "port": DB_PORT,
            "database": os.getenv("STAGING_DB_NAME", DB_NAME_STAGING),
            "user": "postgres",
            "password": password,
        }

        self._config["postgresql"] = {
            "host": "localhost",
            "port": DB_PORT,
            "database": os.getenv("STAGING_DB_NAME", DB_NAME_STAGING),
            "user": "postgres",
            "password": password,
        }

    def get(self, key, default=None):
        """
        Get configuration value

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return self._config.get(key, default)

    def __contains__(self, key):
        """Support 'in' operator for postgres_client compatibility"""
        return key in self._config
