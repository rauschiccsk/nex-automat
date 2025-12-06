#!/usr/bin/env python3
"""
Script 38: Find ENTER key handling in MainWindow
Nájde kde bola implementovaná funkčnosť ENTER klávesy
"""

from pathlib import Path


def find_enter_handling():
    """Hľadá ENTER key handling v main_window.py"""

    main_window_path = Path("apps/supplier-invoice-editor/src/ui/main_window.py")

    if not main_window_path.exists():
        print(f"❌ File not found: {main_window_path}")
        return

    content = main_window_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    print("=" * 80)
    print("SEARCHING FOR ENTER KEY HANDLING")
    print("=" * 80)

    # Hľadaj keyPressEvent
    print("\n1. Looking for keyPressEvent:")
    found_key_press = False
    for i, line in enumerate(lines, 1):
        if 'keyPressEvent' in line or 'keyPress' in line:
            found_key_press = True
            print(f"   {i:4d}: {line.strip()}")

    if not found_key_press:
        print("   ⚠️  No keyPressEvent found")

    # Hľadaj Qt.Key_Return alebo Qt.Key_Enter
    print("\n2. Looking for Key_Return or Key_Enter:")
    found_enter = False
    for i, line in enumerate(lines, 1):
        if 'Key_Return' in line or 'Key_Enter' in line:
            found_enter = True
            print(f"   {i:4d}: {line.strip()}")
            # Zobraz okolie
            for j in range(max(0, i - 3), min(len(lines), i + 3)):
                print(f"        {j + 1:4d}: {lines[j]}")

    if not found_enter:
        print("   ⚠️  No Key_Return or Key_Enter found")

    # Hľadaj activated signal
    print("\n3. Looking for activated signal:")
    for i, line in enumerate(lines, 1):
        if 'activated' in line.lower() and 'connect' in line:
            print(f"   {i:4d}: {line.strip()}")

    # Hľadaj _on_invoice_activated
    print("\n4. Looking for _on_invoice_activated connections:")
    for i, line in enumerate(lines, 1):
        if '_on_invoice_activated' in line and 'connect' in line:
            print(f"   {i:4d}: {line.strip()}")


if __name__ == "__main__":
    find_enter_handling()