#!/usr/bin/env python3
"""
Script 11: Show get_safe_position() method
Zobrazí metódu, ktorá môže prepisovať rozmery
"""

from pathlib import Path


def show_get_safe_position():
    """Zobrazí get_safe_position() z WindowPersistenceManager"""

    persistence_path = Path("packages/nex-shared/ui/window_persistence.py")

    if not persistence_path.exists():
        print(f"❌ File not found: {persistence_path}")
        return

    content = persistence_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    print("=" * 80)
    print("get_safe_position() METHOD")
    print("=" * 80)

    in_method = False
    indent_level = None

    for i, line in enumerate(lines, 1):
        if 'def get_safe_position' in line:
            in_method = True
            indent_level = len(line) - len(line.lstrip())
            print(f"{i:4d}: {line}")
            continue

        if in_method:
            current_indent = len(line) - len(line.lstrip())
            if line.strip() and current_indent <= indent_level and 'def ' in line:
                break
            print(f"{i:4d}: {line}")

    print("=" * 80)

    # Analýza
    code = '\n'.join(lines)
    print("\n📊 ANALYSIS:")

    if 'default_size' in code:
        print("✓ Method uses default_size parameter")

        # Hľadaj kde sa používa default_size
        for i, line in enumerate(lines, 1):
            if in_method and 'default_size' in line and '=' in line:
                print(f"  {i:4d}: {line.strip()}")

    if 'settings' in code and 'None' in code:
        print("✓ Method checks if settings is None")

    # Kritická otázka
    print("\n❓ KEY QUESTION:")
    print("   Does it return default_size when settings exist but position is invalid?")
    print("   → This would explain why window opens with default size!")


if __name__ == "__main__":
    show_get_safe_position()