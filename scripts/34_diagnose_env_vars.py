#!/usr/bin/env python3
"""
Script 34: Diagnose environment variables
Check if POSTGRES_* env vars are set and accessible
"""

import os


def main():
    """Check environment variables"""
    print("=" * 60)
    print("Checking POSTGRES_* environment variables")
    print("=" * 60)

    env_vars = [
        'POSTGRES_HOST',
        'POSTGRES_PORT',
        'POSTGRES_DB',
        'POSTGRES_USER',
        'POSTGRES_PASSWORD'
    ]

    print("\n📋 Environment variables:")
    for var in env_vars:
        value = os.getenv(var)
        if value:
            if 'PASSWORD' in var:
                # Mask password
                masked = '*' * len(value) if value else '(empty)'
                print(f"   ✅ {var:20s} = {masked}")
            else:
                print(f"   ✅ {var:20s} = {value}")
        else:
            print(f"   ❌ {var:20s} = NOT SET")

    # Test Config class
    print("\n📋 Testing Config class:")
    try:
        import sys
        from pathlib import Path

        # Add src to path
        src_path = Path(__file__).parent.parent / "apps" / "supplier-invoice-editor" / "src"
        sys.path.insert(0, str(src_path))

        from config import Config

        config = Config()

        print(f"   host     = {config.get('host')}")
        print(f"   port     = {config.get('port')}")
        print(f"   database = {config.get('database')}")
        print(f"   user     = {config.get('user')}")

        password = config.get('password')
        if password:
            print(f"   password = {'*' * len(password)}")
        else:
            print(f"   password = (empty)")

    except Exception as e:
        print(f"   ❌ Error: {e}")

    print("\n" + "=" * 60)
    print("DIAGNOSIS COMPLETE")
    print("=" * 60)

    return True


if __name__ == "__main__":
    main()