#!/usr/bin/env python3
"""
Script 36: Create simple hardcoded config for testing
Quick workaround to get database working
"""

from pathlib import Path

# Target file - absolute path
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_FILE = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "config.py"

# Simple hardcoded config
CONFIG_CONTENT = '''"""
Configuration for Supplier Invoice Editor
TEMPORARY: Hardcoded for testing
"""

import os


class Config:
    """Simple configuration class with hardcoded database parameters"""

    def __init__(self):
        """Initialize config with database connection parameters"""
        # Hardcoded defaults that work
        password = os.getenv('POSTGRES_PASSWORD', '')

        self._config = {
            # PostgreSQL connection parameters - HARDCODED
            'host': 'localhost',
            'port': 5432,
            'database': 'supplier_invoice_editor',
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
    """Create simple hardcoded config"""
    print("=" * 60)
    print("Creating simple hardcoded config")
    print("=" * 60)

    # Write config file
    CONFIG_FILE.write_text(CONFIG_CONTENT, encoding='utf-8')
    print(f"\n✅ Created: {CONFIG_FILE}")

    # Verify syntax
    try:
        compile(CONFIG_CONTENT, str(CONFIG_FILE), 'exec')
        print("✅ Python syntax valid")
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False

    print("\n📋 Hardcoded config:")
    print("   host     = 'localhost'")
    print("   port     = 5432")
    print("   database = 'supplier_invoice_editor'")
    print("   user     = 'postgres'")
    print("   password = from $env:POSTGRES_PASSWORD")

    print("\n" + "=" * 60)
    print("ÚSPECH: Simple config created")
    print("=" * 60)
    print("\nNext step: Test if database connects")
    print("cd apps/supplier-invoice-editor")
    print("python main.py")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)