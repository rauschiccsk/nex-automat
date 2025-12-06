#!/usr/bin/env python3
"""
Script 38: Fix database name to invoice_staging
Correct database name based on actual PostgreSQL setup
"""

from pathlib import Path

# Target file - absolute path
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_FILE = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "config.py"

# Config with correct database name
CONFIG_CONTENT = '''"""
Configuration for Supplier Invoice Editor
"""

import os


class Config:
    """Simple configuration class with database parameters"""

    def __init__(self):
        """Initialize config with database connection parameters"""
        password = os.getenv('POSTGRES_PASSWORD', '')

        self._config = {
            # PostgreSQL connection parameters
            'host': 'localhost',
            'port': 5432,
            'database': 'invoice_staging',  # CORRECT database name
            'user': 'postgres',
            'password': password,

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
    """Fix database name"""
    print("=" * 60)
    print("Fixing database name to invoice_staging")
    print("=" * 60)

    # Write config file
    CONFIG_FILE.write_text(CONFIG_CONTENT, encoding='utf-8')
    print(f"\n✅ Updated: {CONFIG_FILE}")

    # Verify syntax
    try:
        compile(CONFIG_CONTENT, str(CONFIG_FILE), 'exec')
        print("✅ Python syntax valid")
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False

    print("\n📋 Corrected config:")
    print("   host     = 'localhost'")
    print("   port     = 5432")
    print("   database = 'invoice_staging' ✅ CORRECT")
    print("   user     = 'postgres'")
    print("   password = from $env:POSTGRES_PASSWORD")

    print("\n" + "=" * 60)
    print("ÚSPECH: Database name fixed")
    print("=" * 60)
    print("\nNext step: Test application")
    print("cd apps/supplier-invoice-editor")
    print("python main.py")
    print("\nShould now connect to invoice_staging database!")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)