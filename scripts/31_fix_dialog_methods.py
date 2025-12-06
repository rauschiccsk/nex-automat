#!/usr/bin/env python3
"""
Script 31: Fix QDialog methods (accept/reject) to QMainWindow (close)
Zmení accept() a reject() na close() pretože BaseWindow nie je QDialog
"""

from pathlib import Path

def fix_dialog_methods():
    """Opraví QDialog metódy na QMainWindow"""

    window_path = Path("apps/supplier-invoice-editor/src/ui/invoice_detail_window.py")

    if not window_path.exists():
        print(f"❌ File not found: {window_path}")
        return False

    content = window_path.read_text(encoding='utf-8')

    print("=" * 80)
    print("FIXING QDialog METHODS")
    print("=" * 80)

    changes = []

    # 1. Zmeniť self.reject() na self.close()
    if 'self.reject()' in content:
        content = content.replace('self.reject()', 'self.close()')
        changes.append("self.reject() → self.close()")

    # 2. Zmeniť self.accept() na self.close() + emit signal
    if 'self.accept()' in content:
        # Nájdi accept() a nahraď s emitovaním signálu
        content = content.replace(
            'self.accept()',
            'self.invoice_saved.emit(self.invoice_id)\n            self.close()'
        )
        changes.append("self.accept() → emit signal + self.close()")

    if changes:
        for change in changes:
            print(f"✅ {change}")

        # Ulož súbor
        window_path.write_text(content, encoding='utf-8')

        print("\n📝 EXPLANATION:")
        print("  - QDialog has: accept(), reject()")
        print("  - QMainWindow has: close()")
        print("  - BaseWindow inherits from QMainWindow")
        print("  - Signal invoice_saved is emitted before close()")

        return True
    else:
        print("⚠️  No accept() or reject() calls found")
        return False

if __name__ == "__main__":
    success = fix_dialog_methods()
    if success:
        print("\n" + "=" * 80)
        print("TEST AGAIN")
        print("=" * 80)
        print("cd apps/supplier-invoice-editor")
        print("python main.py")