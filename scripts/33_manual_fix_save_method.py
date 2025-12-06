#!/usr/bin/env python3
"""
Script 33: Manual fix of _save_invoice method
Manuálne opraví _save_invoice metódu s correct indentation
"""

from pathlib import Path


def manual_fix():
    """Manuálne opraví _save_invoice metódu"""

    window_path = Path("apps/supplier-invoice-editor/src/ui/invoice_detail_window.py")

    if not window_path.exists():
        print(f"❌ File not found: {window_path}")
        return False

    content = window_path.read_text(encoding='utf-8')

    # Problematický blok
    old_block = """            if success:
                self.logger.info("Invoice saved successfully")
                QMessageBox.information(
                    self,
                    "Úspech",
                    "Faktúra bola úspešne uložená."
                )

                # Emit signal and close
                self.invoice_saved.emit(self.invoice_id)
                self.invoice_saved.emit(self.invoice_id)
            self.close()
            else:"""

    # Správny blok
    new_block = """            if success:
                self.logger.info("Invoice saved successfully")
                QMessageBox.information(
                    self,
                    "Úspech",
                    "Faktúra bola úspešne uložená."
                )

                # Emit signal and close
                self.invoice_saved.emit(self.invoice_id)
                self.close()
            else:"""

    if old_block in content:
        content = content.replace(old_block, new_block)

        window_path.write_text(content, encoding='utf-8')

        print("=" * 80)
        print("FIXED _save_invoice METHOD")
        print("=" * 80)
        print("✅ Removed duplicate self.invoice_saved.emit()")
        print("✅ Fixed self.close() indentation")
        print("✅ Fixed else: syntax")

        return True
    else:
        print("❌ Pattern not found - manual editing needed")
        return False


if __name__ == "__main__":
    success = manual_fix()
    if success:
        print("\n" + "=" * 80)
        print("TEST AGAIN")
        print("=" * 80)
        print("cd apps/supplier-invoice-editor")
        print("python main.py")