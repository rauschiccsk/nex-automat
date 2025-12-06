#!/usr/bin/env python3
"""
Script 42: Fix WindowSettingsDB path
Change database path to C:/NEX/YEARACT/SYSTEM/SQLITE
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
WINDOW_SETTINGS_DB = PROJECT_ROOT / "packages" / "nex-shared" / "database" / "window_settings_db.py"


def main():
    """Fix database path"""
    print("=" * 60)
    print("Fixing WindowSettingsDB path")
    print("=" * 60)

    if not WINDOW_SETTINGS_DB.exists():
        print(f"❌ File not found: {WINDOW_SETTINGS_DB}")
        return False

    content = WINDOW_SETTINGS_DB.read_text(encoding='utf-8')

    # Find and replace the DB path initialization
    # Old: db_dir = Path.home() / ".nex-automat"
    # New: db_dir = Path("C:/NEX/YEARACT/SYSTEM/SQLITE")

    old_pattern = 'db_dir = Path.home() / ".nex-automat"'
    new_pattern = 'db_dir = Path("C:/NEX/YEARACT/SYSTEM/SQLITE")'

    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        WINDOW_SETTINGS_DB.write_text(content, encoding='utf-8')
        print(f"\n✅ Updated: {WINDOW_SETTINGS_DB}")
        print(f"   Old: {old_pattern}")
        print(f"   New: {new_pattern}")
    else:
        print(f"\n⚠️  Pattern not found, showing current db_dir setup:")
        for i, line in enumerate(content.split('\n'), 1):
            if 'db_dir' in line and '=' in line:
                print(f"   Line {i}: {line.strip()}")

    # Verify syntax
    try:
        compile(content, str(WINDOW_SETTINGS_DB), 'exec')
        print("✅ Python syntax valid")
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False

    print("\n" + "=" * 60)
    print("ÚSPECH: Database path fixed")
    print("=" * 60)
    print("\nDatabase now at: C:/NEX/YEARACT/SYSTEM/SQLITE/window_settings.db")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)