#!/usr/bin/env python3
"""
Script 43: Show WindowSettingsDB content
Display file to find where db_dir is defined
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
WINDOW_SETTINGS_DB = PROJECT_ROOT / "packages" / "nex-shared" / "database" / "window_settings_db.py"


def main():
    """Show file content"""
    print("=" * 60)
    print("Showing WindowSettingsDB content")
    print("=" * 60)

    if not WINDOW_SETTINGS_DB.exists():
        print(f"❌ File not found: {WINDOW_SETTINGS_DB}")
        return False

    content = WINDOW_SETTINGS_DB.read_text(encoding='utf-8')
    lines = content.split('\n')

    print(f"\n📄 File: {WINDOW_SETTINGS_DB}")
    print(f"   Lines: {len(lines)}\n")

    # Show file content
    for i, line in enumerate(lines, 1):
        print(f"{i:3d}: {line}")

    print("\n" + "=" * 60)

    return True


if __name__ == "__main__":
    main()