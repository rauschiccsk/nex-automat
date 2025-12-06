#!/usr/bin/env python3
"""
Script 43: Fix ENTER handling to use correct method
Opraví ENTER handling aby používal get_selected_invoice_id()
"""

from pathlib import Path


def fix_enter_method():
    """Opraví metódu pre získanie vybranej faktúry"""

    main_window_path = Path("apps/supplier-invoice-editor/src/ui/main_window.py")

    if not main_window_path.exists():
        print(f"❌ File not found: {main_window_path}")
        return False

    content = main_window_path.read_text(encoding='utf-8')

    print("=" * 80)
    print("FIXING ENTER HANDLING")
    print("=" * 80)

    # Zlý kód
    old_code = """        # Open invoice detail on Enter/Return
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            # Get current selection
            if hasattr(self, 'invoice_list') and self.invoice_list:
                current_index = self.invoice_list.get_current_index()
                if current_index is not None:
                    invoice_id = self.invoice_list.get_invoice_id_at_index(current_index)
                    if invoice_id:
                        self._on_invoice_activated(invoice_id)
                        event.accept()
                        return"""

    # Správny kód
    new_code = """        # Open invoice detail on Enter/Return
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            # Get currently selected invoice
            if hasattr(self, 'invoice_list') and self.invoice_list:
                invoice_id = self.invoice_list.get_selected_invoice_id()
                if invoice_id:
                    self._on_invoice_activated(invoice_id)
                    event.accept()
                    return"""

    if old_code in content:
        content = content.replace(old_code, new_code)

        main_window_path.write_text(content, encoding='utf-8')

        print("✅ Fixed ENTER handling")
        print("\n📝 CHANGES:")
        print("   OLD: get_current_index() + get_invoice_id_at_index()")
        print("   NEW: get_selected_invoice_id()")
        print("\n   Using existing InvoiceListWidget method ✅")

        return True
    else:
        print("❌ Pattern not found")
        return False


if __name__ == "__main__":
    success = fix_enter_method()
    if success:
        print("\n" + "=" * 80)
        print("FINAL TEST")
        print("=" * 80)
        print("cd apps/supplier-invoice-editor")
        print("python main.py")
        print("\n1. Vyber faktúru")
        print("2. Stlač ENTER")
        print("3. Detail by sa mal otvoriť! ✅")