#!/usr/bin/env python3
"""
Script 08: Show _load_settings() method
Zobrazí implementáciu _load_settings() v base_window.py
"""

from pathlib import Path


def show_load_settings():
    """Zobrazí _load_settings() metódu"""

    base_window_path = Path("packages/nex-shared/ui/base_window.py")

    if not base_window_path.exists():
        print(f"❌ File not found: {base_window_path}")
        return

    content = base_window_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Nájdi _load_settings metódu
    in_method = False
    method_lines = []
    indent_level = None

    for i, line in enumerate(lines, 1):
        if 'def _load_settings(self)' in line:
            in_method = True
            indent_level = len(line) - len(line.lstrip())
            method_lines.append(f"{i:4d}: {line}")
            continue

        if in_method:
            current_indent = len(line) - len(line.lstrip())

            # Koniec metódy
            if line.strip() and current_indent <= indent_level:
                break

            method_lines.append(f"{i:4d}: {line}")

    if method_lines:
        print("=" * 80)
        print("CURRENT _load_settings() METHOD")
        print("=" * 80)
        for line in method_lines:
            print(line)
        print("=" * 80)

        # Analýza
        code = '\n'.join(method_lines)
        print("\n📊 ANALYSIS:")
        print(f"✓ Total lines: {len(method_lines)}")
        print(f"✓ Calls self._db.load(): {'self._db.load' in code}")
        print(f"✓ Sets geometry: {'setGeometry' in code or 'resize' in code}")
        print(f"✓ Has DEBUG logging: {'print(f\"🔍' in code or 'DEBUG' in code}")

        if 'resize' in code:
            print("  → Uses resize() method")
        if 'setGeometry' in code:
            print("  → Uses setGeometry() method")

    else:
        print("❌ Method _load_settings() not found!")


if __name__ == "__main__":
    show_load_settings()