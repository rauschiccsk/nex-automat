#!/usr/bin/env python3
"""
Script 39: Analyze current postgres_client.py
Show how it gets connection parameters
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
POSTGRES_CLIENT = PROJECT_ROOT / "apps" / "supplier-invoice-editor" / "src" / "database" / "postgres_client.py"


def main():
    """Analyze postgres_client"""
    print("=" * 60)
    print("Analyzing postgres_client.py")
    print("=" * 60)

    if not POSTGRES_CLIENT.exists():
        print(f"❌ File not found: {POSTGRES_CLIENT}")
        return False

    content = POSTGRES_CLIENT.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Show __init__ and connection params logic
    in_init = False
    in_get_params = False

    print("\n📋 PostgresClient initialization and connection logic:\n")

    for i, line in enumerate(lines, 1):
        if 'def __init__' in line:
            in_init = True
        elif 'def _get_connection_params' in line or 'self.conn_params' in line:
            in_get_params = True
        elif (in_init or in_get_params) and line.strip().startswith('def ') and '__init__' not in line:
            in_init = False
            in_get_params = False

        if in_init or in_get_params or 'conn_params' in line:
            print(f"{i:4d}: {line}")

    print("\n" + "=" * 60)
    return True


if __name__ == "__main__":
    main()