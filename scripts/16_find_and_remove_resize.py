#!/usr/bin/env python3
"""
Script 16: Find and remove resize(1400, 900) call
Nájde a odstráni resize() volanie ktoré prepisuje načítané rozmery
"""

from pathlib import Path


def find_and_remove_resize():
    """Nájde a odstráni resize(1400, 900) z MainWindow"""

    mainwindow_path = Path("apps/supplier-invoice-editor/src/ui/main_window.py")

    if not mainwindow_path.exists():
        print(f"❌ File not found: {mainwindow_path}")
        return False

    content = mainwindow_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Nájdi všetky resize() volania
    print("=" * 80)
    print("ALL resize() AND setGeometry() CALLS IN MainWindow")
    print("=" * 80)

    resize_lines = []
    for i, line in enumerate(lines, 1):
        if 'resize(' in line or 'setGeometry(' in line:
            resize_lines.append((i, line))
            print(f"{i:4d}: {line}")

    if not resize_lines:
        print("No resize() or setGeometry() calls found!")
        return False

    print("\n" + "=" * 80)
    print("REMOVING resize(1400, 900) calls")
    print("=" * 80)

    # Odstráň resize(1400, 900) riadky
    new_lines = []
    removed_count = 0

    for i, line in enumerate(lines):
        # Kontroluj či riadok obsahuje resize(1400, 900)
        if 'resize(1400, 900)' in line or 'resize(1400,900)' in line:
            print(f"❌ REMOVING line {i + 1}: {line.strip()}")
            removed_count += 1
            # Pridaj komentár namiesto odstránenia
            indent = len(line) - len(line.lstrip())
            new_lines.append(' ' * indent + '# REMOVED: resize(1400, 900) - BaseWindow handles size from DB')
        else:
            new_lines.append(line)

    if removed_count == 0:
        print("⚠️  No resize(1400, 900) calls found to remove")
        print("   Looking for similar patterns...")

        # Hľadaj iné resize patterns
        for i, line in enumerate(lines, 1):
            if 'resize(' in line.lower():
                print(f"  Found: {i:4d}: {line.strip()}")

        return False

    # Ulož súbor
    content = '\n'.join(new_lines)
    mainwindow_path.write_text(content, encoding='utf-8')

    print(f"\n✅ Removed {removed_count} resize(1400, 900) call(s)")
    print("\n📝 Changes:")
    print("  - resize(1400, 900) replaced with comment")
    print("  - BaseWindow now fully controls window size from DB")

    return True


if __name__ == "__main__":
    success = find_and_remove_resize()
    if success:
        print("\n" + "=" * 80)
        print("NEXT: Test the fix")
        print("=" * 80)
        print("cd apps/supplier-invoice-editor")
        print("python main.py")
        print("\n1. Zmeň veľkosť okna")
        print("2. Zavri aplikáciu")
        print("3. Otvor znova → rozmery by mali byť ZACHOVANÉ! ✅")