r"""
Script 30: Skontroluje aké public metódy má InvoiceListWidget.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/widgets/invoice_list_widget.py"


def main():
    """Skontroluje public metódy InvoiceListWidget."""
    print(f"Analyzujem: {TARGET_FILE}")
    print("=" * 70)

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.splitlines()

    # Nájdi InvoiceListWidget triedu
    in_widget = False
    widget_start = 0

    for i, line in enumerate(lines, 1):
        if 'class InvoiceListWidget' in line:
            in_widget = True
            widget_start = i
            print(f"InvoiceListWidget trieda začína na riadku {i}\n")
            break

    if not in_widget:
        print("❌ InvoiceListWidget trieda nenájdená!")
        return

    # Nájdi všetky public metódy (nezačínajú na _)
    print("PUBLIC METÓDY:")
    print("-" * 70)

    for i, line in enumerate(lines, 1):
        if i > widget_start:
            # Koniec triedy
            if line.strip() and not line.startswith('    ') and not line.startswith('\t'):
                break

            # Public metóda
            if '    def ' in line and not '    def _' in line:
                # Zobraz 3 riadky pre docstring
                print(f"  {i:4d}: {line.strip()}")
                if i < len(lines) - 2:
                    for j in range(1, 3):
                        if i + j < len(lines) and '"""' in lines[i + j]:
                            print(f"       {lines[i + j].strip()}")
                print()

    # Skontroluj InvoiceListModel metódy
    print("\n" + "=" * 70)
    print("INVOICELISTMODEL METÓDY:")
    print("-" * 70)

    in_model = False
    for i, line in enumerate(lines, 1):
        if 'class InvoiceListModel' in line:
            in_model = True
            print(f"InvoiceListModel trieda začína na riadku {i}\n")

        if in_model:
            # Koniec triedy
            if line.strip().startswith('class ') and i > 10:
                break

            # Public metóda
            if '    def ' in line and not '    def _' in line:
                print(f"  {i:4d}: {line.strip()}")

    # Odporúčanie
    print("\n" + "=" * 70)
    print("RIEŠENIE:")
    print("=" * 70)
    print("\nInvoiceListWidget by mal mať metódu ako:")
    print("  def update_invoices(self, invoices):")
    print("      self.model.set_invoices(invoices)")
    print("\nAlebo main_window.py by mal volať:")
    print("  self.invoice_list.model.set_invoices(invoices)")


if __name__ == "__main__":
    main()