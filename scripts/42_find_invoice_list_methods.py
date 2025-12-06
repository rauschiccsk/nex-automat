#!/usr/bin/env python3
"""
Script 42: Find methods in InvoiceListWidget
Nájde metódy pre získanie vybranej faktúry
"""

from pathlib import Path


def find_methods():
    """Nájde metódy v InvoiceListWidget"""

    widget_path = Path("apps/supplier-invoice-editor/src/ui/widgets/invoice_list_widget.py")

    if not widget_path.exists():
        print(f"❌ File not found: {widget_path}")
        return

    content = widget_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    print("=" * 80)
    print("ALL METHODS IN InvoiceListWidget")
    print("=" * 80)

    for i, line in enumerate(lines, 1):
        if '    def ' in line:
            print(f"{i:4d}: {line.strip()}")

    # Hľadaj metódy pre selection/current
    print("\n" + "=" * 80)
    print("METHODS WITH 'current' OR 'selected' OR 'index'")
    print("=" * 80)

    for i, line in enumerate(lines, 1):
        if '    def ' in line:
            if any(keyword in line.lower() for keyword in ['current', 'selected', 'index', 'get']):
                print(f"{i:4d}: {line.strip()}")

    # Hľadaj invoice_activated signal emission
    print("\n" + "=" * 80)
    print("SEARCHING FOR invoice_activated.emit()")
    print("=" * 80)

    for i, line in enumerate(lines, 1):
        if 'invoice_activated.emit' in line:
            print(f"\nFound at line {i}:")
            for j in range(max(0, i - 10), min(len(lines), i + 5)):
                marker = ">>>" if j == i - 1 else "   "
                print(f"{marker} {j + 1:4d}: {lines[j]}")


if __name__ == "__main__":
    find_methods()