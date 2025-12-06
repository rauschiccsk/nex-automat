#!/usr/bin/env python3
"""
Script 35: Test database connection with current config
Show exactly what connection parameters are being used
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "apps" / "supplier-invoice-editor" / "src"
sys.path.insert(0, str(src_path))

from config import Config


def main():
    """Test database connection"""
    print("=" * 60)
    print("Testing database connection")
    print("=" * 60)

    # Create config
    config = Config()

    # Show connection parameters
    print("\n📋 Connection parameters:")
    print(f"   Host:     {config.get('host')}")
    print(f"   Port:     {config.get('port')}")
    print(f"   Database: {config.get('database')}")
    print(f"   User:     {config.get('user')}")

    password = config.get('password')
    if password:
        print(f"   Password: {'*' * len(password)} ({len(password)} chars)")
    else:
        print(f"   Password: (empty)")

    # Try to connect
    print("\n🔍 Testing connection...")
    try:
        import pg8000.dbapi

        conn_params = {
            'host': config.get('host'),
            'port': config.get('port'),
            'database': config.get('database'),
            'user': config.get('user'),
            'password': config.get('password'),
        }

        conn = pg8000.dbapi.connect(**conn_params)
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        print(f"   ✅ Connection successful!")
        print(f"   PostgreSQL version: {version[:50]}...")

    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        print("\n💡 Možné riešenia:")
        print("   1. Skontroluj či PostgreSQL beží")
        print("   2. Skontroluj či databáza 'supplier_invoice_editor' existuje")
        print("   3. Skontroluj credentials pre user 'postgres'")
        print("   4. Možno potrebuješ iné env vars:")
        print("      $env:POSTGRES_USER = 'tvoj_user'")
        print("      $env:POSTGRES_DB = 'tvoja_databaza'")

    print("\n" + "=" * 60)

    return True


if __name__ == "__main__":
    main()