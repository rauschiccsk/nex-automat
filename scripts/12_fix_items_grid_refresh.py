"""
Fix: Refresh grid view after populating model in InvoiceItemsWindow.
"""
import os

TARGET_FILE = r"apps\supplier-invoice-staging\ui\invoice_items_window.py"

OLD_POPULATE = '''    def _populate_model(self):
        self.model.blockSignals(True)
        self.model.removeRows(0, self.model.rowCount())

        for row_data in self._filtered_data:
            row_items = []
            for col_key, _, _, _, editable in self.COLUMNS:
                value = row_data.get(col_key, "")
                if isinstance(value, float):
                    value = f"{value:.2f}"
                item = QStandardItem(str(value) if value is not None else "")
                item.setEditable(editable)
                row_items.append(item)
            self.model.appendRow(row_items)

        self.model.blockSignals(False)
        self._update_status()'''

NEW_POPULATE = '''    def _populate_model(self):
        self.model.blockSignals(True)
        self.model.removeRows(0, self.model.rowCount())

        for row_data in self._filtered_data:
            row_items = []
            for col_key, _, _, _, editable in self.COLUMNS:
                value = row_data.get(col_key, "")
                if isinstance(value, float):
                    value = f"{value:.2f}"
                item = QStandardItem(str(value) if value is not None else "")
                item.setEditable(editable)
                row_items.append(item)
            self.model.appendRow(row_items)

        self.model.blockSignals(False)

        # Force view refresh
        self.grid.table_view.viewport().update()

        self._update_status()'''


def main():
    if not os.path.exists(TARGET_FILE):
        print(f"ERROR: File not found: {TARGET_FILE}")
        return False

    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    if OLD_POPULATE not in content:
        print("ERROR: OLD_POPULATE not found")
        return False

    content = content.replace(OLD_POPULATE, NEW_POPULATE)

    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"SUCCESS: Updated {TARGET_FILE}")
    print("- Added viewport update after populate")
    return True


if __name__ == "__main__":
    main()