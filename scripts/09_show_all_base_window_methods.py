#!/usr/bin/env python3
"""
Script 09: Show all methods in BaseWindow class
Zobrazí všetky metódy v BaseWindow
"""

from pathlib import Path


def show_all_methods():
    """Zobrazí všetky metódy BaseWindow triedy"""

    base_window_path = Path("packages/nex-shared/ui/base_window.py")

    if not base_window_path.exists():
        print(f"❌ File not found: {base_window_path}")
        return

    content = base_window_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    print("=" * 80)
    print("ALL METHODS IN BaseWindow")
    print("=" * 80)

    in_class = False
    methods = []

    for i, line in enumerate(lines, 1):
        # Začiatok BaseWindow triedy
        if 'class BaseWindow' in line:
            in_class = True
            print(f"{i:4d}: {line}")
            continue

        # Koniec triedy
        if in_class and line.strip() and not line[0].isspace() and 'class ' in line:
            break

        # Metódy triedy
        if in_class and 'def ' in line:
            methods.append((i, line.strip()))
            print(f"{i:4d}: {line}")

    print("=" * 80)
    print(f"\n📊 Total methods found: {len(methods)}")
    print("\n🔍 Looking for load/restore/init methods:")

    for i, method in methods:
        if any(keyword in method.lower() for keyword in ['load', 'restore', 'init', '__init__']):
            print(f"  {i:4d}: {method}")

    # Hľadaj kde sa volá self._db.load()
    print("\n🔍 Searching for self._db.load() calls:")
    for i, line in enumerate(lines, 1):
        if 'self._db.load' in line:
            print(f"  {i:4d}: {line}")


if __name__ == "__main__":
    show_all_methods()