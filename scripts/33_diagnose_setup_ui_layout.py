r"""
Script 33: Diagnostika _setup_ui - prečo sa grid nezobrazuje.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/widgets/invoice_list_widget.py"


def main():
    """Analyzuje _setup_ui metódu."""
    print(f"Analyzujem: {TARGET_FILE}")
    print("=" * 70)

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.splitlines()

    # Nájdi _setup_ui metódu
    print("\n_SETUP_UI METÓDA:")
    print("-" * 70)

    in_setup_ui = False
    setup_ui_start = 0

    for i, line in enumerate(lines, 1):
        if 'def _setup_ui(self):' in line and i > 140:
            in_setup_ui = True
            setup_ui_start = i
            print(f"Začína na riadku {i}\n")
            break

    if not in_setup_ui:
        print("❌ _setup_ui metóda nenájdená!")
        return

    # Zobraz celú metódu (do ďalšej metódy)
    for i in range(setup_ui_start - 1, len(lines)):
        line = lines[i]

        # Koniec metódy
        if i > setup_ui_start and line.strip().startswith('def '):
            break

        print(f"  {i + 1:4d}: {line}")

    # Kontrola kľúčových častí
    print("\n" + "=" * 70)
    print("KONTROLA:")
    print("=" * 70)

    has_layout = 'layout = QVBoxLayout' in content
    has_set_layout = 'self.setLayout(layout)' in content
    has_table_view = 'self.table_view = QTableView()' in content
    has_model = 'self.model = InvoiceListModel' in content
    has_add_widget = 'layout.addWidget' in content

    print(f"\n  {'✅' if has_layout else '❌'} layout = QVBoxLayout()")
    print(f"  {'✅' if has_table_view else '❌'} self.table_view = QTableView()")
    print(f"  {'✅' if has_model else '❌'} self.model = InvoiceListModel()")
    print(f"  {'✅' if has_add_widget else '❌'} layout.addWidget(...)")
    print(f"  {'✅' if has_set_layout else '❌'} self.setLayout(layout)")

    # Hľadaj pridávanie widgetov do layoutu
    print("\n" + "=" * 70)
    print("PRIDÁVANIE WIDGETOV DO LAYOUTU:")
    print("=" * 70)

    found_add_widget = False
    for i, line in enumerate(lines, 1):
        if i > setup_ui_start and 'layout.addWidget' in line:
            print(f"  {i:4d}: {line.strip()}")
            found_add_widget = True

    if not found_add_widget:
        print("  ❌ Žiadne layout.addWidget() volania!")
        print("\n⚠️  PROBLÉM: Widgety nie sú pridané do layoutu!")

    # Záver
    print("\n" + "=" * 70)
    print("ZÁVER:")
    print("=" * 70)

    if not has_add_widget:
        print("\n❌ CHÝBA: layout.addWidget(self.table_view) alebo podobné")
        print("\nMusíme pridať do _setup_ui:")
        print("  layout.addWidget(self.table_view)")
        print("  # alebo")
        print("  layout.addWidget(self.quick_search_container)")


if __name__ == "__main__":
    main()