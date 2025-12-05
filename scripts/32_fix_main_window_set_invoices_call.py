r"""
Script 32: Oprava volania set_invoices na update_invoices v main_window.py.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/main_window.py"


def main():
    """Opraví volanie set_invoices."""
    print(f"Upravujem: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')

    # Skontroluj či už je opravené
    if 'self.invoice_list.update_invoices(invoices)' in content:
        print("✅ Už je opravené - volá sa update_invoices()")
        return

    # Nahraď set_invoices za update_invoices
    if 'self.invoice_list.set_invoices(invoices)' in content:
        content = content.replace(
            'self.invoice_list.set_invoices(invoices)',
            'self.invoice_list.update_invoices(invoices)'
        )

        # Zapíš späť
        TARGET_FILE.write_text(content, encoding='utf-8')

        print("✅ Súbor upravený: {TARGET_FILE}")
        print("   Zmenené: set_invoices → update_invoices")
        print("\nTeraz spusti aplikáciu!")
    else:
        print("⚠️  Nenašiel som volanie set_invoices v main_window.py")
        print("Možno je to už inak pomenované?")


if __name__ == "__main__":
    main()