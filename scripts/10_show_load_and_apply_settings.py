#!/usr/bin/env python3
"""
Script 10: Show _load_and_apply_settings() method
Zobrazí implementáciu metódy, ktorá načítava nastavenia z DB
"""

from pathlib import Path


def show_method():
    """Zobrazí _load_and_apply_settings() a __init__"""

    base_window_path = Path("packages/nex-shared/ui/base_window.py")

    if not base_window_path.exists():
        print(f"❌ File not found: {base_window_path}")
        return

    content = base_window_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    # 1. Zobraz __init__ metódu
    print("=" * 80)
    print("__init__ METHOD")
    print("=" * 80)

    in_init = False
    indent_level = None

    for i, line in enumerate(lines, 1):
        if 'def __init__(self,' in line and 'BaseWindow' not in line:
            in_init = True
            indent_level = len(line) - len(line.lstrip())
            print(f"{i:4d}: {line}")
            continue

        if in_init:
            current_indent = len(line) - len(line.lstrip())
            if line.strip() and current_indent <= indent_level and 'def ' in line:
                break
            print(f"{i:4d}: {line}")

    # 2. Zobraz _load_and_apply_settings metódu
    print("\n" + "=" * 80)
    print("_load_and_apply_settings() METHOD")
    print("=" * 80)

    in_method = False
    indent_level = None

    for i, line in enumerate(lines, 1):
        if 'def _load_and_apply_settings(self)' in line:
            in_method = True
            indent_level = len(line) - len(line.lstrip())
            print(f"{i:4d}: {line}")
            continue

        if in_method:
            current_indent = len(line) - len(line.lstrip())
            if line.strip() and current_indent <= indent_level:
                break
            print(f"{i:4d}: {line}")

    print("=" * 80)

    # Analýza
    print("\n📊 ANALYSIS:")
    if '_load_and_apply_settings' in content:
        # Kde sa volá?
        init_calls_load = False
        for i, line in enumerate(lines, 1):
            if 'def __init__' in line and 'BaseWindow' not in line:
                # Skontroluj nasledujúcich 50 riadkov
                for j in range(i, min(i + 50, len(lines))):
                    if '_load_and_apply_settings' in lines[j]:
                        print(f"✓ __init__ calls _load_and_apply_settings() at line {j + 1}")
                        init_calls_load = True
                        break
                break

        if not init_calls_load:
            print("❌ __init__ DOES NOT call _load_and_apply_settings()!")
            print("   → This is the BUG! Settings are never loaded!")


if __name__ == "__main__":
    show_method()