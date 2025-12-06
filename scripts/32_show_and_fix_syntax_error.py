#!/usr/bin/env python3
"""
Script 32: Show and fix syntax error around line 214
Zobrazí a opraví syntax chybu
"""

from pathlib import Path


def show_and_fix():
    """Zobrazí problematickú oblasť a opraví syntax"""

    window_path = Path("apps/supplier-invoice-editor/src/ui/invoice_detail_window.py")

    if not window_path.exists():
        print(f"❌ File not found: {window_path}")
        return False

    content = window_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    print("=" * 80)
    print("LINES AROUND 214 (200-220)")
    print("=" * 80)

    for i in range(199, min(221, len(lines))):
        marker = ">>>" if i == 213 else "   "
        print(f"{marker} {i + 1:4d}: {lines[i]}")

    # Hľadaj problematický blok s accept()
    print("\n" + "=" * 80)
    print("SEARCHING FOR PROBLEMATIC accept() REPLACEMENT")
    print("=" * 80)

    for i, line in enumerate(lines):
        if 'self.invoice_saved.emit' in line:
            print(f"\nFound at line {i + 1}:")
            for j in range(max(0, i - 5), min(len(lines), i + 10)):
                marker = ">>>" if j == i else "   "
                print(f"{marker} {j + 1:4d}: {lines[j]}")

    # Opraviť: Hľadaj a oprav zlé odsadenie
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]

        # Ak nájdeme self.invoice_saved.emit na samostatnom riadku
        if 'self.invoice_saved.emit(self.invoice_id)' in line and 'self.close()' in line:
            # Rozdelíme na dva riadky so správnym odsadením
            indent = len(line) - len(line.lstrip())
            new_lines.append(' ' * indent + 'self.invoice_saved.emit(self.invoice_id)')
            new_lines.append(' ' * indent + 'self.close()')
        else:
            new_lines.append(line)

        i += 1

    content = '\n'.join(new_lines)
    window_path.write_text(content, encoding='utf-8')

    print("\n✅ Fixed indentation for emit + close()")

    return True


if __name__ == "__main__":
    success = show_and_fix()
    if success:
        print("\n" + "=" * 80)
        print("TEST AGAIN")
        print("=" * 80)
        print("cd apps/supplier-invoice-editor")
        print("python main.py")