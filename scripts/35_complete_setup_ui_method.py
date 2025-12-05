r"""
Script 35: Doplnenie chýbajúcej časti _setup_ui metódy.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/widgets/invoice_list_widget.py"

# Chýbajúca časť _setup_ui
MISSING_PART = """
        # Create quick search container with search input
        self.quick_search_container = QuickSearchContainer(self.table_view, self)
        layout.addWidget(self.quick_search_container)

        # Create search controller
        self.search_controller = QuickSearchController(self.table_view, self.quick_search_container)

        # Connect selection change signal
        selection_model = self.table_view.selectionModel()
        selection_model.currentRowChanged.connect(self._on_selection_changed)

        # Connect double-click signal
        self.table_view.doubleClicked.connect(self._on_double_clicked)

        self.logger.info("Invoice list widget UI setup complete (with quick search)")
"""


def main():
    """Doplní chýbajúcu časť _setup_ui."""
    print(f"Upravujem: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.splitlines()

    # Nájdi koniec _setup_ui (riadok 186)
    insert_line = 0
    for i, line in enumerate(lines):
        if i > 183 and 'header.sectionMoved.connect' in line:
            insert_line = i + 1
            break

    if insert_line == 0:
        print("❌ Nepodarilo sa nájsť koniec _setup_ui!")
        return

    print(f"✅ Vkladám chýbajúcu časť za riadok {insert_line + 1}")

    # Pridaj chýbajúcu časť
    lines.insert(insert_line, MISSING_PART)

    # Zapíš späť
    content = '\n'.join(lines)
    TARGET_FILE.write_text(content, encoding='utf-8')

    print(f"\n✅ Súbor upravený: {TARGET_FILE}")
    print(f"   Nové riadky: {len(lines)}")
    print("\nDoplnené:")
    print("  ✅ QuickSearchContainer - vytvorenie quick search widgetu")
    print("  ✅ layout.addWidget(quick_search_container) - pridanie do layoutu")
    print("  ✅ QuickSearchController - vytvorenie controllera")
    print("  ✅ Pripojenie signálov (selection, doubleClick)")
    print("\nTeraz spusti aplikáciu znova!")


if __name__ == "__main__":
    main()