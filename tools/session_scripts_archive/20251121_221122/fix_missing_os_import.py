#!/usr/bin/env python3
"""
Add missing 'os' import to test_database_connection.py
"""

from pathlib import Path

BASE_PATH = Path(r"C:\Development\nex-automat")
TEST_DB_PATH = BASE_PATH / "scripts" / "test_database_connection.py"


def fix_imports():
    """Add os import if missing"""

    with open(TEST_DB_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if os is imported
    if 'import os' not in content:
        # Find import section and add os
        old_imports = '''import sys
import asyncio
import asyncpg
import yaml
from pathlib import Path
from datetime import datetime'''

        new_imports = '''import os
import sys
import asyncio
import asyncpg
import yaml
from pathlib import Path
from datetime import datetime'''

        if old_imports in content:
            content = content.replace(old_imports, new_imports)

            with open(TEST_DB_PATH, 'w', encoding='utf-8') as f:
                f.write(content)

            print("✅ Added 'import os' to test_database_connection.py")
            return True

    print("✅ 'import os' already present")
    return False


def main():
    print("=" * 70)
    print("FIX MISSING IMPORT")
    print("=" * 70)
    print()

    fix_imports()

    print()
    print("Now run:")
    print("  python scripts/test_database_connection.py")
    print()


if __name__ == "__main__":
    main()