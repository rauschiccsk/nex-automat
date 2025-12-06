#!/usr/bin/env python3
"""
Script 28: Fix to use existing WINDOW_INVOICE_DETAIL constant
Opraví aby používal existujúcu konštantu namiesto novej
"""

from pathlib import Path


def fix_constant_usage():
    """Opraví použitie konštanty"""

    # 1. Odstráň novú WINDOW_DETAIL konštantu z constants.py
    constants_path = Path("apps/supplier-invoice-editor/src/utils/constants.py")

    if constants_path.exists():
        content = constants_path.read_text(encoding='utf-8')
        lines = content.split('\n')

        # Odstráň WINDOW_DETAIL = "sie_detail_window"
        new_lines = [line for line in lines if 'WINDOW_DETAIL = "sie_detail_window"' not in line]

        constants_path.write_text('\n'.join(new_lines), encoding='utf-8')
        print("✅ Removed duplicate WINDOW_DETAIL constant")

    # 2. Oprav invoice_detail_window.py aby používal WINDOW_INVOICE_DETAIL
    window_path = Path("apps/supplier-invoice-editor/src/ui/invoice_detail_window.py")

    if not window_path.exists():
        print(f"❌ File not found: {window_path}")
        return False

    content = window_path.read_text(encoding='utf-8')

    # Zmení import
    old_import = "from ...utils.constants import WINDOW_DETAIL"
    new_import = "from ...utils.constants import WINDOW_INVOICE_DETAIL"

    if old_import in content:
        content = content.replace(old_import, new_import)
        print("✅ Updated import to use WINDOW_INVOICE_DETAIL")

    # Zmení použitie v __init__
    old_usage = "window_name=WINDOW_DETAIL,"
    new_usage = "window_name=WINDOW_INVOICE_DETAIL,"

    if old_usage in content:
        content = content.replace(old_usage, new_usage)
        print("✅ Updated __init__ to use WINDOW_INVOICE_DETAIL")

    # Ulož súbor
    window_path.write_text(content, encoding='utf-8')

    print("\n📝 CHANGES:")
    print("  - Using existing constant: WINDOW_INVOICE_DETAIL")
    print("  - Removed duplicate: WINDOW_DETAIL")

    return True


if __name__ == "__main__":
    success = fix_constant_usage()
    if success:
        print("\n" + "=" * 80)
        print("FINAL TEST")
        print("=" * 80)
        print("cd apps/supplier-invoice-editor")
        print("python main.py")
        print("\n1. Otvor faktúru (double-click)")
        print("2. Zmeň veľkosť detail okna")
        print("3. Zavri detail")
        print("4. Otvor inú faktúru")
        print("5. Veľkosť by mala byť ZAPAMÄTANÁ! ✅")