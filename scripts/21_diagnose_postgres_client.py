#!/usr/bin/env python3
"""
Script 21: Diagnose PostgresClient initialization
Find what PostgresClient expects
"""

from pathlib import Path
import re

# Target files
POSTGRES_CLIENT = Path("apps/supplier-invoice-editor/src/database/postgres_client.py")


def find_postgres_init():
    """Find PostgresClient.__init__ signature"""
    if not POSTGRES_CLIENT.exists():
        print(f"❌ ERROR: File not found: {POSTGRES_CLIENT}")
        return False

    content = POSTGRES_CLIENT.read_text(encoding='utf-8')

    # Find __init__ method
    pattern = r'def __init__\(self[^)]*\):.*?(?=\n    def |\Z)'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        print("\n📝 PostgresClient.__init__ method:")
        lines = match.group(0).split('\n')
        for i, line in enumerate(lines[:30], 1):
            print(f"   {i:3d}: {line}")
        if len(lines) > 30:
            print(f"   ... and {len(lines) - 30} more lines")
    else:
        print("\n⚠️  __init__ method not found")

    # Find all self.config usages
    config_usages = re.findall(r'self\.config\.[a-zA-Z_][a-zA-Z0-9_.]*', content)
    if config_usages:
        print(f"\n📋 PostgresClient uses config attributes:")
        for usage in sorted(set(config_usages)):
            print(f"   - {usage}")

    return True


def main():
    """Diagnose PostgresClient"""
    print("=" * 60)
    print("Diagnosing PostgresClient initialization")
    print("=" * 60)

    find_postgres_init()

    print("\n" + "=" * 60)
    print("DIAGNOSIS COMPLETE")
    print("=" * 60)

    return True


if __name__ == "__main__":
    main()