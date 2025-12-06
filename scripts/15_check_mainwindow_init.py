#!/usr/bin/env python3
"""
Script 15: Check MainWindow.__init__()
Overí, kde MainWindow volá super().__init__() a aké parametre použije
"""

from pathlib import Path


def check_mainwindow():
    """Zobrazí MainWindow.__init__() a hľadá default_size"""

    mainwindow_path = Path("apps/supplier-invoice-editor/src/ui/main_window.py")

    if not mainwindow_path.exists():
        print(f"❌ File not found: {mainwindow_path}")
        return

    content = mainwindow_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    print("=" * 80)
    print("MainWindow CLASS")
    print("=" * 80)

    in_init = False
    indent_level = None

    for i, line in enumerate(lines, 1):
        # Zobraz class definíciu
        if 'class MainWindow' in line:
            print(f"{i:4d}: {line}")
            continue

        # Zobraz __init__ metódu
        if 'def __init__' in line:
            in_init = True
            indent_level = len(line) - len(line.lstrip())
            print(f"{i:4d}: {line}")
            continue

        if in_init:
            current_indent = len(line) - len(line.lstrip())

            # Koniec __init__
            if line.strip() and current_indent <= indent_level and 'def ' in line:
                break

            print(f"{i:4d}: {line}")

    print("=" * 80)

    # Analýza
    print("\n📊 ANALYSIS:")

    # Hľadaj super().__init__() volanie
    for i, line in enumerate(lines, 1):
        if 'super().__init__' in line:
            print(f"\n✓ super().__init__() call at line {i}:")
            # Zobraz 5 riadkov okolo
            for j in range(max(0, i - 2), min(len(lines), i + 8)):
                print(f"  {j + 1:4d}: {lines[j]}")
            break

    # Hľadaj default_size parameter
    if 'default_size' in content:
        print("\n✓ default_size found:")
        for i, line in enumerate(lines, 1):
            if 'default_size' in line:
                print(f"  {i:4d}: {line}")
    else:
        print("\n⚠️  No default_size parameter found")
        print("   → Using BaseWindow default (800, 600)?")

    # Hľadaj resize() volania
    print("\n🔍 Searching for resize() or setGeometry() calls:")
    for i, line in enumerate(lines, 1):
        if 'resize(' in line or 'setGeometry(' in line:
            print(f"  {i:4d}: {line.strip()}")


if __name__ == "__main__":
    check_mainwindow()