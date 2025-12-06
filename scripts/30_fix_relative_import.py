#!/usr/bin/env python3
"""
Script 30: Fix relative import in invoice_detail_window.py
Opraví relatívny import z ... na ..
"""

from pathlib import Path


def fix_relative_import():
    """Opraví relatívny import"""

    window_path = Path("apps/supplier-invoice-editor/src/ui/invoice_detail_window.py")

    if not window_path.exists():
        print(f"❌ File not found: {window_path}")
        return False

    content = window_path.read_text(encoding='utf-8')

    print("=" * 80)
    print("FIXING RELATIVE IMPORT")
    print("=" * 80)

    # Oprav import
    old_import = "from ...utils.constants import WINDOW_INVOICE_DETAIL"
    new_import = "from ..utils.constants import WINDOW_INVOICE_DETAIL"

    if old_import in content:
        content = content.replace(old_import, new_import)
        print(f"✅ Fixed import:")
        print(f"   OLD: {old_import}")
        print(f"   NEW: {new_import}")
        print(f"\n   Explanation:")
        print(f"   File location: src/ui/invoice_detail_window.py")
        print(f"   .. = go up to src/")
        print(f"   ..utils = src/utils ✅")
    else:
        print("⚠️  Pattern not found")
        return False

    # Ulož súbor
    window_path.write_text(content, encoding='utf-8')

    return True


if __name__ == "__main__":
    success = fix_relative_import()
    if success:
        print("\n" + "=" * 80)
        print("TEST AGAIN")
        print("=" * 80)
        print("cd apps/supplier-invoice-editor")
        print("python main.py")