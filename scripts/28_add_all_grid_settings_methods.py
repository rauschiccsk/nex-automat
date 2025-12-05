r"""
Script 28: Pridanie všetkých grid settings metód do invoice_list_widget.py.
"""

from pathlib import Path

# Cesta k projektu
PROJECT_ROOT = Path("C:/Development/nex-automat")
TARGET_FILE = PROJECT_ROOT / "apps/supplier-invoice-editor/src/ui/widgets/invoice_list_widget.py"

# Všetky metódy na pridanie
ALL_METHODS = '''
    def _load_grid_settings(self):
        """Načíta a aplikuje uložené nastavenia gridu."""
        # Načítaj column settings
        column_settings = load_column_settings(
            window_name=WINDOW_MAIN,
            grid_name=GRID_INVOICE_LIST
        )

        if column_settings:
            self.logger.info(f"Loading grid settings: {len(column_settings)} columns")

            header = self.table_view.horizontalHeader()

            # Aplikuj nastavenia na stĺpce
            for col_setting in column_settings:
                col_name = col_setting['column_name']

                # Nájdi index stĺpca podľa názvu
                col_index = None
                for idx, (display_name, field_name) in enumerate(self.COLUMNS):
                    if field_name == col_name:
                        col_index = idx
                        break

                if col_index is not None:
                    # Aplikuj šírku
                    if col_setting.get('width'):
                        header.resizeSection(col_index, col_setting['width'])

                    # Aplikuj viditeľnosť
                    if not col_setting.get('visible', True):
                        self.table_view.hideColumn(col_index)

                    # Aplikuj visual_index (poradie po drag-and-drop)
                    if col_setting.get('visual_index') is not None:
                        header.moveSection(header.visualIndex(col_index), col_setting['visual_index'])

        # Načítaj grid-level settings (aktívny stĺpec)
        grid_settings = load_grid_settings(
            window_name=WINDOW_MAIN,
            grid_name=GRID_INVOICE_LIST
        )

        if grid_settings and grid_settings.get('active_column_index') is not None:
            # Nastav aktívny stĺpec v QuickSearchController
            active_col = grid_settings['active_column_index']
            if hasattr(self, 'search_controller') and self.search_controller:
                self.search_controller.set_active_column(active_col)
                self.logger.info(f"Restored active column: {active_col}")

    def _save_grid_settings(self):
        """Uloží aktuálne nastavenia gridu."""
        header = self.table_view.horizontalHeader()

        # Zozbieraj nastavenia všetkých stĺpcov
        columns = []
        for idx, (display_name, field_name) in enumerate(self.COLUMNS):
            columns.append({
                'column_name': field_name,
                'width': header.sectionSize(idx),
                'visual_index': header.visualIndex(idx),
                'visible': not self.table_view.isColumnHidden(idx)
            })

        # Ulož column settings
        save_column_settings(
            window_name=WINDOW_MAIN,
            grid_name=GRID_INVOICE_LIST,
            columns=columns
        )

        # Ulož active column z QuickSearchController
        if hasattr(self, 'search_controller') and self.search_controller:
            active_col = self.search_controller.get_active_column()
            save_grid_settings(
                window_name=WINDOW_MAIN,
                grid_name=GRID_INVOICE_LIST,
                active_column_index=active_col
            )

    def _on_column_resized(self, logical_index, old_size, new_size):
        """Handler pre zmenu šírky stĺpca."""
        self._save_grid_settings()

    def _on_column_moved(self, logical_index, old_visual_index, new_visual_index):
        """Handler pre presunutie stĺpca."""
        self._save_grid_settings()
'''


def main():
    """Pridá všetky grid settings metódy."""
    print(f"Upravujem: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        print(f"❌ Súbor neexistuje: {TARGET_FILE}")
        return

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.splitlines()

    # Nájdi koniec InvoiceListWidget triedy
    widget_end = 0

    for i, line in enumerate(lines):
        if line.strip() and not line.startswith('    ') and not line.startswith('\t'):
            # Možno koniec triedy
            if i > 130:  # Widget začína okolo riadku 124
                widget_end = i
                break

    if widget_end == 0:
        widget_end = len(lines)

    print(f"✅ Vkladám metódy na riadok {widget_end + 1}")

    # Vlož metódy
    lines.insert(widget_end, ALL_METHODS)

    # Zapíš späť
    content = '\n'.join(lines)
    TARGET_FILE.write_text(content, encoding='utf-8')

    print(f"\n✅ Súbor upravený: {TARGET_FILE}")
    print(f"   Nové riadky: {len(lines)}")
    print("\nPridané metódy:")
    print("  ✅ _load_grid_settings() - načíta a aplikuje nastavenia")
    print("  ✅ _save_grid_settings() - uloží aktuálne nastavenia")
    print("  ✅ _on_column_resized() - handler pre zmenu šírky")
    print("  ✅ _on_column_moved() - handler pre presun stĺpca")
    print("\nTeraz spusti aplikáciu znova!")


if __name__ == "__main__":
    main()