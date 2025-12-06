#!/usr/bin/env python3
"""
Script 40: Fix Config to work with postgres_client logic
Config must work as dict-like object with direct key access
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_FILE = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "config.py"

# Fixed Config that works with postgres_client
CONFIG_CONTENT = '''"""
Configuration for Supplier Invoice Editor
"""

import os


class Config:
    """Configuration class compatible with postgres_client expectations"""

    def __init__(self):
        """Initialize config with database connection parameters"""
        password = os.getenv('POSTGRES_PASSWORD', '')

        # Primary config - flat structure for direct access
        self._config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'invoice_staging',
            'user': 'postgres',
            'password': password,
        }

        # Also provide nested structure for compatibility
        self._config['database.postgres'] = {
            'host': 'localhost',
            'port': 5432,
            'database': 'invoice_staging',
            'user': 'postgres',
            'password': password,
        }

        self._config['postgresql'] = {
            'host': 'localhost',
            'port': 5432,
            'database': 'invoice_staging',
            'user': 'postgres',
            'password': password,
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
'''


def main():
    """Fix Config class"""
    print("=" * 60)
    print("Fixing Config for postgres_client compatibility")
    print("=" * 60)

    CONFIG_FILE.write_text(CONFIG_CONTENT, encoding='utf-8')
    print(f"\n✅ Updated: {CONFIG_FILE}")

    try:
        compile(CONFIG_CONTENT, str(CONFIG_FILE), 'exec')
        print("✅ Python syntax valid")
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False

    print("\n📋 Config now provides:")
    print("   Direct access: config.get('host'), config.get('database'), etc.")
    print("   Nested access: config.get('database.postgres'), config.get('postgresql')")
    print("   All point to: invoice_staging with POSTGRES_PASSWORD")

    print("\n" + "=" * 60)
    print("ÚSPECH: Config fixed")
    print("=" * 60)
    print("\nNext step: Test application")
    print("cd apps/supplier-invoice-editor")
    print("python main.py")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)