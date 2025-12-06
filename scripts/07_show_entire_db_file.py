#!/usr/bin/env python3
"""
Script 07: Show entire window_settings_db.py
Zobrazí celý súbor pre analýzu
"""

from pathlib import Path


def show_db_file():
    """Zobrazí celý window_settings_db.py"""

    db_file = Path("packages/nex-shared/database/window_settings_db.py")

    if not db_file.exists():
        print(f"❌ File not found: {db_file}")
        return

    content = db_file.read_text(encoding='utf-8')
    lines = content.split('\n')

    print("=" * 80)
    print(f"FILE: {db_file}")
    print(f"Lines: {len(lines)}")
    print("=" * 80)

    for i, line in enumerate(lines, 1):
        print(f"{i:4d}: {line}")

    print("=" * 80)

    # Analýza metód
    print("\n📊 METHODS FOUND:")
    for i, line in enumerate(lines, 1):
        if 'def ' in line and 'self' in line:
            print(f"  {i:4d}: {line.strip()}")


if __name__ == "__main__":
    show_db_file()