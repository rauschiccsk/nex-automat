#!/usr/bin/env python3
"""
Script 23: Create Config class for supplier-invoice-editor
Simple config class with database connection parameters
"""

from pathlib import Path

# Target file
CONFIG_FILE = Path("apps/supplier-invoice-editor/src/config.py")

# Config class content
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
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', '5432')),
            'database': os.getenv('DB_NAME', 'supplier_invoice_editor'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', ''),

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
    """Create Config class"""
    print("=" * 60)
    print("Creating Config class")
    print("=" * 60)

    # Ensure parent directory exists
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

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

    print("\n📋 Config provides:")
    print("   - host (default: localhost)")
    print("   - port (default: 5432)")
    print("   - database (default: supplier_invoice_editor)")
    print("   - user (default: postgres)")
    print("   - password (default: '')")
    print("\n💡 Use environment variables to override:")
    print("   DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD")

    print("\n" + "=" * 60)
    print("ÚSPECH: Config class created")
    print("=" * 60)
    print("\nNext step: Update main.py to use Config")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)