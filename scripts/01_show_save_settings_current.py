#!/usr/bin/env python3
"""
Script 01: Show current _save_settings() implementation
Overí, či sú zmeny z predchádzajúcej session skutočne aplikované
"""

from pathlib import Path


def show_save_settings():
    """Zobrazí aktuálnu implementáciu _save_settings() metódy"""
    base_window_path = Path("packages/nex-shared/ui/base_window.py")

    if not base_window_path.exists():
        print(f"❌ File not found: {base_window_path}")
        return

    content = base_window_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Nájdi _save_settings metódu
    in_method = False
    method_lines = []
    indent_level = None

    for i, line in enumerate(lines, 1):
        if 'def _save_settings(self)' in line:
            in_method = True
            indent_level = len(line) - len(line.lstrip())
            method_lines.append(f"{i:4d}: {line}")
            continue

        if in_method:
            current_indent = len(line) - len(line.lstrip())

            # Koniec metódy - ďalšia metóda alebo koniec class
            if line.strip() and current_indent <= indent_level:
                break

            method_lines.append(f"{i:4d}: {line}")

    if method_lines:
        print("=" * 80)
        print("CURRENT _save_settings() METHOD")
        print("=" * 80)
        for line in method_lines:
            print(line)
        print("=" * 80)

        # Analýza kľúčových bodov
        code = '\n'.join(method_lines)
        print("\n📊 ANALYSIS:")
        print(f"✓ Total lines: {len(method_lines)}")
        print(f"✓ Contains validation check: {'validate_position' in code}")
        print(f"✓ Contains 'ALWAYS save' logic: {'ALWAYS' in code or 'always' in code}")
        print(f"✓ Saves unconditionally: {'.save(' in code and 'if' not in code.split('.save(')[0].split('\n')[-1]}")

    else:
        print("❌ Method _save_settings() not found!")


if __name__ == "__main__":
    show_save_settings()