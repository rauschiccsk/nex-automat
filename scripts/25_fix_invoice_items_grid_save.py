#!/usr/bin/env python3
"""
Script 25: Fix save_grid_settings call in invoice_items_grid.py
Opraví zlé volanie s dict namiesto int
"""

from pathlib import Path


def fix_grid_save():
    """Opraví save_grid_settings() volanie"""

    grid_path = Path("apps/supplier-invoice-editor/src/ui/widgets/invoice_items_grid.py")

    if not grid_path.exists():
        print(f"❌ File not found: {grid_path}")
        return False

    content = grid_path.read_text(encoding='utf-8')

    print("=" * 80)
    print("FIXING save_grid_settings() CALL")
    print("=" * 80)

    # Zlé volanie
    old_call = "save_grid_settings(WINDOW_MAIN, GRID_INVOICE_ITEMS, {'active_column': None})"

    # Správne volanie - použiť None alebo -1 pre "no active column"
    new_call = "save_grid_settings(WINDOW_MAIN, GRID_INVOICE_ITEMS, -1)  # -1 = no active column"

    if old_call in content:
        content = content.replace(old_call, new_call)

        grid_path.write_text(content, encoding='utf-8')

        print("✅ Fixed save_grid_settings() call")
        print(f"\n📝 Changed:")
        print(f"   OLD: {old_call}")
        print(f"   NEW: {new_call}")
        print(f"\n   Explanation: Changed dict to int (-1 represents 'no active column')")

        return True
    else:
        print("❌ Pattern not found - might be already fixed")
        return False


if __name__ == "__main__":
    success = fix_grid_save()
    if success:
        print("\n" + "=" * 80)
        print("NEXT: Test the fix")
        print("=" * 80)
        print("cd apps/supplier-invoice-editor")
        print("python main.py")
        print("\n1. Otvor faktúru (klikni na riadok)")
        print("2. Pozri položky faktúry")
        print("3. Zatvor okno")
        print("4. Chyba 'type dict is not supported' by nemala byť! ✅")