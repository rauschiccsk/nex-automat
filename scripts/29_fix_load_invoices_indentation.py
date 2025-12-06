#!/usr/bin/env python3
"""
Script 29: Fix _load_invoices indentation
Fix lines that are outside try block
"""

from pathlib import Path
import re

# Target file
MAIN_WINDOW = Path("apps/supplier-invoice-editor/src/ui/main_window.py")


def fix_load_invoices():
    """Fix _load_invoices method with proper indentation"""
    if not MAIN_WINDOW.exists():
        print(f"❌ ERROR: File not found: {MAIN_WINDOW}")
        return False

    content = MAIN_WINDOW.read_text(encoding='utf-8')

    # Correct _load_invoices method
    correct_method = '''    def _load_invoices(self):
        """Load invoices from database"""
        try:
            self.statusbar.showMessage("Načítavam faktúry...")
            self.logger.info("Loading invoices...")

            invoices = self.invoice_service.get_pending_invoices()
            self.invoice_list.update_invoices(invoices)

            count = len(invoices)
            self.statusbar.showMessage(
                f"Načítaných {count} faktúr | F5: Obnoviť | Ctrl+F: Hľadať"
            )
            self.logger.info(f"Loaded {count} invoices")

        except Exception as e:
            self.logger.exception("Failed to load invoices")
            self.statusbar.showMessage("Chyba pri načítaní faktúr")
            QMessageBox.warning(
                self,
                "Chyba",
                f"Nepodarilo sa načítať faktúry:\n\n{str(e)}"
            )
'''

    # Find and replace _load_invoices method
    pattern = r'    def _load_invoices\(self\):.*?(?=\n    def |\Z)'
    content = re.sub(pattern, correct_method.rstrip(), content, flags=re.DOTALL)

    # Write fixed content
    MAIN_WINDOW.write_text(content, encoding='utf-8')

    return True


def main():
    """Fix _load_invoices indentation"""
    print("=" * 60)
    print("Fixing _load_invoices indentation")
    print("=" * 60)

    if not fix_load_invoices():
        return False

    print("\n✅ Fixed: _load_invoices indentation")
    print("   - Lines moved inside try block")
    print("   - Proper except block structure")

    # Verify syntax
    content = MAIN_WINDOW.read_text(encoding='utf-8')
    try:
        compile(content, str(MAIN_WINDOW), 'exec')
        print("✅ Python syntax valid")
    except SyntaxError as e:
        print(f"❌ Syntax error at line {e.lineno}: {e.msg}")
        if e.text:
            print(f"   {e.text.strip()}")
        return False

    print("\n" + "=" * 60)
    print("ÚSPECH: Syntax fixed")
    print("=" * 60)
    print("\nNext step: Test application")
    print("cd apps/supplier-invoice-editor")
    print("python main.py")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)