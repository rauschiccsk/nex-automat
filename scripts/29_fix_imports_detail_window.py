#!/usr/bin/env python3
"""
Script 29: Fix imports in invoice_detail_window.py
Opraví importy aby BaseWindow bol správne importovaný
"""

from pathlib import Path


def fix_imports():
    """Opraví importy v invoice_detail_window.py"""

    window_path = Path("apps/supplier-invoice-editor/src/ui/invoice_detail_window.py")

    if not window_path.exists():
        print(f"❌ File not found: {window_path}")
        return False

    content = window_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    print("=" * 80)
    print("CURRENT IMPORTS (first 20 lines)")
    print("=" * 80)

    for i in range(min(20, len(lines))):
        print(f"{i + 1:4d}: {lines[i]}")

    # Nájdi riadok s from .widgets.invoice_items_grid import
    insert_line = None
    for i, line in enumerate(lines):
        if 'from .widgets.invoice_items_grid import' in line:
            insert_line = i + 1
            break

    if insert_line is None:
        # Ak nenájde, vlož po PyQt5 importoch
        for i, line in enumerate(lines):
            if 'from decimal import' in line:
                insert_line = i + 1
                break

    # Skontroluj či už import existuje
    has_basewindow = any('from nex_shared.ui import BaseWindow' in line for line in lines)
    has_constant = any('from ...utils.constants import WINDOW_INVOICE_DETAIL' in line for line in lines)

    if not has_basewindow:
        lines.insert(insert_line, 'from nex_shared.ui import BaseWindow')
        print(f"\n✅ Added: from nex_shared.ui import BaseWindow at line {insert_line + 1}")
    else:
        print(f"\n✓ BaseWindow import already exists")

    if not has_constant:
        lines.insert(insert_line + 1, 'from ...utils.constants import WINDOW_INVOICE_DETAIL')
        print(f"✅ Added: from ...utils.constants import WINDOW_INVOICE_DETAIL at line {insert_line + 2}")
    else:
        print(f"✓ WINDOW_INVOICE_DETAIL import already exists")

    # Ulož súbor
    content = '\n'.join(lines)
    window_path.write_text(content, encoding='utf-8')

    print("\n" + "=" * 80)
    print("UPDATED IMPORTS (first 20 lines)")
    print("=" * 80)

    new_lines = content.split('\n')
    for i in range(min(20, len(new_lines))):
        print(f"{i + 1:4d}: {new_lines[i]}")

    return True


if __name__ == "__main__":
    success = fix_imports()
    if success:
        print("\n" + "=" * 80)
        print("TEST AGAIN")
        print("=" * 80)
        print("cd apps/supplier-invoice-editor")
        print("python main.py")