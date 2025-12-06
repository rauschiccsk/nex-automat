#!/usr/bin/env python3
"""
Script 21: Analyze InvoiceDetailWindow
Zobrazí __init__ a hľadá grid settings použitie
"""

from pathlib import Path


def analyze_detail_window():
    """Analyzuje InvoiceDetailWindow"""

    window_path = Path("apps/supplier-invoice-editor/src/ui/invoice_detail_window.py")

    if not window_path.exists():
        print(f"❌ File not found: {window_path}")
        return

    content = window_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    print("=" * 80)
    print("InvoiceDetailWindow CLASS DEFINITION")
    print("=" * 80)

    # Zobraz class definíciu a imports
    for i, line in enumerate(lines[:30], 1):
        print(f"{i:4d}: {line}")

    print("\n" + "=" * 80)
    print("SEARCHING FOR 'grid' REFERENCES")
    print("=" * 80)

    for i, line in enumerate(lines, 1):
        if 'grid' in line.lower():
            print(f"{i:4d}: {line}")

    print("\n" + "=" * 80)
    print("SEARCHING FOR 'closeEvent' METHOD")
    print("=" * 80)

    in_close = False
    for i, line in enumerate(lines, 1):
        if 'def closeEvent' in line:
            in_close = True
            # Zobraz closeEvent metódu
            indent_level = len(line) - len(line.lstrip())
            print(f"{i:4d}: {line}")

            for j in range(i, min(i + 20, len(lines))):
                current_indent = len(lines[j]) - len(lines[j].lstrip())
                if lines[j].strip() and current_indent <= indent_level and j > i:
                    break
                print(f"{j + 1:4d}: {lines[j]}")
            break

    if not in_close:
        print("⚠️  No closeEvent method found")


if __name__ == "__main__":
    analyze_detail_window()