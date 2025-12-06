#!/usr/bin/env python3
"""
Script 08: Fix nex-shared database/__init__.py imports
Change to relative imports for proper package structure
"""

from pathlib import Path

# Target file
DB_INIT = Path("packages/nex-shared/database/__init__.py")

# Correct content with relative imports
DB_INIT_CONTENT = '''"""
Database components for nex-shared package
"""

from .window_settings_db import WindowSettingsDB

__all__ = ['WindowSettingsDB']
'''


def main():
    """Fix database/__init__.py in nex-shared package"""
    print("=" * 60)
    print("Fixing nex-shared/database/__init__.py imports")
    print("=" * 60)

    if not DB_INIT.exists():
        print(f"❌ ERROR: File not found: {DB_INIT}")
        return False

    # Read current content
    current = DB_INIT.read_text(encoding='utf-8')
    print(f"\n📝 Current content:")
    print(current)
    print(f"\n📝 Current file size: {len(current)} chars")

    # Write correct content with relative imports
    DB_INIT.write_text(DB_INIT_CONTENT, encoding='utf-8')
    print(f"\n✅ Fixed: {DB_INIT}")

    # Verify
    new_content = DB_INIT.read_text(encoding='utf-8')
    print(f"✅ New file size: {len(new_content)} chars")

    # Check syntax
    try:
        compile(new_content, str(DB_INIT), 'exec')
        print("✅ Python syntax valid")
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False

    # Verify relative imports
    if 'from .window_settings_db import' in new_content:
        print("✅ Using relative imports (.window_settings_db)")

    print("\n" + "=" * 60)
    print("ÚSPECH: nex-shared database/__init__.py fixed")
    print("=" * 60)
    print("\nNext step: Test application")
    print("cd apps/supplier-invoice-editor")
    print("python main.py")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)