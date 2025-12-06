#!/usr/bin/env python3
"""
Script 22: Diagnose _get_connection_params method
Find what config keys PostgresClient needs
"""

from pathlib import Path
import re

# Target file
POSTGRES_CLIENT = Path("apps/supplier-invoice-editor/src/database/postgres_client.py")


def find_get_connection_params():
    """Find _get_connection_params method"""
    if not POSTGRES_CLIENT.exists():
        print(f"❌ ERROR: File not found: {POSTGRES_CLIENT}")
        return False

    content = POSTGRES_CLIENT.read_text(encoding='utf-8')

    # Find _get_connection_params method
    pattern = r'def _get_connection_params\(self\):.*?(?=\n    def |\Z)'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        print("\n📝 _get_connection_params method:")
        lines = match.group(0).split('\n')
        for i, line in enumerate(lines, 1):
            print(f"   {i:3d}: {line}")
    else:
        print("\n⚠️  _get_connection_params method not found")

    # Find all config.get calls
    config_calls = re.findall(r'self\.config\.get\([^)]+\)', content)
    if config_calls:
        print(f"\n📋 Found {len(config_calls)} config.get() calls:")
        for call in config_calls:
            print(f"   - {call}")

    return True


def main():
    """Diagnose connection params"""
    print("=" * 60)
    print("Diagnosing connection parameters")
    print("=" * 60)

    find_get_connection_params()

    print("\n" + "=" * 60)
    print("DIAGNOSIS COMPLETE")
    print("=" * 60)

    return True


if __name__ == "__main__":
    main()