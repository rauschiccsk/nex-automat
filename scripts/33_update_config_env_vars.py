#!/usr/bin/env python3
"""
Script 33: Update Config to use POSTGRES_* environment variables
Match the environment variables user already has
"""

from pathlib import Path

# Target file - absolute path from script location
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_FILE = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "config.py"

# Updated Config class content
CONFIG_CONTENT = '''"""
Configuration for Supplier Invoice Editor
"""

import os


class Config:
    """Simple configuration class with database parameters"""

    def __init__(self):
        """Initialize config with database connection parameters"""
        self._config = {
            # PostgreSQL connection parameters
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': int(os.getenv('POSTGRES_PORT', '5432')),
            'database': os.getenv('POSTGRES_DB', 'supplier_invoice_editor'),
            'user': os.getenv('POSTGRES_USER', 'postgres'),
            'password': os.getenv('POSTGRES_PASSWORD', ''),

            # Nested config structures (for compatibility)
            'database.postgres': {},
            'postgresql': {},
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
'''


def main():
    """Update Config class"""
    print("=" * 60)
    print("Updating Config to use POSTGRES_* env vars")
    print("=" * 60)

    # Write updated config file
    CONFIG_FILE.write_text(CONFIG_CONTENT, encoding='utf-8')
    print(f"\n✅ Updated: {CONFIG_FILE}")

    # Verify syntax
    try:
        compile(CONFIG_CONTENT, str(CONFIG_FILE), 'exec')
        print("✅ Python syntax valid")
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False

    print("\n📋 Config now reads:")
    print("   - POSTGRES_HOST (default: localhost)")
    print("   - POSTGRES_PORT (default: 5432)")
    print("   - POSTGRES_DB (default: supplier_invoice_editor)")
    print("   - POSTGRES_USER (default: postgres)")
    print("   - POSTGRES_PASSWORD (default: '')")

    print("\n" + "=" * 60)
    print("ÚSPECH: Config updated")
    print("=" * 60)
    print("\nNext step: Test application")
    print("cd apps/supplier-invoice-editor")
    print("python main.py")
    print("\nShould now connect to database using $env:POSTGRES_PASSWORD")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)