#!/usr/bin/env python3
"""
Script 23: Analyze grid_settings.py module
Nájde kde je chyba "Chyba pri ukladaní grid settings"
"""

from pathlib import Path


def analyze_grid_settings():
    """Analyzuje grid_settings.py"""

    grid_settings_path = Path("apps/supplier-invoice-editor/src/utils/grid_settings.py")

    if not grid_settings_path.exists():
        print(f"❌ File not found: {grid_settings_path}")
        return

    content = grid_settings_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    print("=" * 80)
    print("SEARCHING FOR ERROR MESSAGE")
    print("=" * 80)

    error_found = False
    for i, line in enumerate(lines, 1):
        if 'Chyba pri ukladaní grid settings' in line:
            error_found = True
            print(f"\n✓ Found at line {i}:")
            # Zobraz celú funkciu
            start = max(0, i - 20)
            end = min(len(lines), i + 10)

            for j in range(start, end):
                marker = ">>>" if j == i - 1 else "   "
                print(f"{marker} {j + 1:4d}: {lines[j]}")

    if not error_found:
        print("❌ Error message not found in grid_settings.py")
        return

    # Zobraz save_grid_settings funkciu
    print("\n" + "=" * 80)
    print("save_grid_settings() FUNCTION")
    print("=" * 80)

    in_function = False
    indent_level = None

    for i, line in enumerate(lines, 1):
        if 'def save_grid_settings' in line:
            in_function = True
            indent_level = len(line) - len(line.lstrip())
            print(f"{i:4d}: {line}")
            continue

        if in_function:
            current_indent = len(line) - len(line.lstrip())
            if line.strip() and current_indent <= indent_level and 'def ' in line:
                break
            print(f"{i:4d}: {line}")


if __name__ == "__main__":
    analyze_grid_settings()