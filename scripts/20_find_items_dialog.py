#!/usr/bin/env python3
"""
Script 20: Find items dialog/window
Nájde dialóg/okno ktoré zobrazuje položky faktúry
"""

from pathlib import Path
import os


def find_items_dialog():
    """Nájde všetky dialógy/okná v supplier-invoice-editor"""

    app_dir = Path("apps/supplier-invoice-editor/src/ui")

    if not app_dir.exists():
        print(f"❌ Directory not found: {app_dir}")
        return

    print("=" * 80)
    print("ALL UI FILES IN supplier-invoice-editor")
    print("=" * 80)

    py_files = list(app_dir.glob("*.py"))

    for py_file in sorted(py_files):
        if py_file.name == "__init__.py":
            continue

        content = py_file.read_text(encoding='utf-8')

        # Hľadaj class definície
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if 'class ' in line and ('Dialog' in line or 'Window' in line):
                print(f"\n📄 {py_file.name}")
                print(f"   {i:4d}: {line.strip()}")

                # Zobraz či dedí z BaseWindow
                if 'BaseWindow' in line:
                    print(f"        ✅ Inherits from BaseWindow")
                elif 'QDialog' in line:
                    print(f"        ⚠️  Inherits from QDialog (not BaseWindow)")
                elif 'QMainWindow' in line:
                    print(f"        ⚠️  Inherits from QMainWindow (not BaseWindow)")

    # Hľadaj "items" v názvoch tried a súborov
    print("\n" + "=" * 80)
    print("SEARCHING FOR 'items' RELATED FILES")
    print("=" * 80)

    for py_file in sorted(py_files):
        if 'item' in py_file.name.lower():
            print(f"\n📄 {py_file.name}")
            content = py_file.read_text(encoding='utf-8')
            lines = content.split('\n')

            # Zobraz class definíciu
            for i, line in enumerate(lines, 1):
                if 'class ' in line:
                    print(f"   {i:4d}: {line.strip()}")

                    # Zobraz ±3 riadky okolo
                    for j in range(max(0, i - 1), min(len(lines), i + 3)):
                        if j != i - 1:
                            print(f"        {j + 1:4d}: {lines[j].strip()}")


if __name__ == "__main__":
    find_items_dialog()