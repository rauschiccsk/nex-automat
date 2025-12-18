"""
Update main_window.py to use real database queries instead of test data.
"""

from pathlib import Path

TARGET_FILE = Path("apps/supplier-invoice-staging/ui/main_window.py")

# New import to add
NEW_IMPORT = "from database.repositories import InvoiceRepository"

# Old _load_test_data method
OLD_LOAD_TEST_DATA = '''    def _load_test_data(self):
        self._data = [
            {"id": 1, "supplier_name": "METRO", "invoice_number": "F2024-001", 
             "invoice_date": "2024-12-15", "total_amount": 1250.50, "currency": "EUR",
             "status": "pending", "item_count": 15, "match_percent": 45.0},
            {"id": 2, "supplier_name": "MAKRO", "invoice_number": "F2024-002",
             "invoice_date": "2024-12-14", "total_amount": 890.00, "currency": "EUR",
             "status": "matched", "item_count": 8, "match_percent": 100.0},
            {"id": 3, "supplier_name": "LIDL", "invoice_number": "F2024-003",
             "invoice_date": "2024-12-13", "total_amount": 2100.75, "currency": "EUR",
             "status": "processing", "item_count": 22, "match_percent": 68.0},
            {"id": 4, "supplier_name": "TESCO", "invoice_number": "F2024-004",
             "invoice_date": "2024-12-12", "total_amount": 550.25, "currency": "EUR",
             "status": "pending", "item_count": 5, "match_percent": 20.0},
            {"id": 5, "supplier_name": "BILLA", "invoice_number": "F2024-005",
             "invoice_date": "2024-12-11", "total_amount": 1800.00, "currency": "EUR",
             "status": "matched", "item_count": 12, "match_percent": 100.0},
        ]
        self._filtered_data = self._data.copy()
        self._populate_model()
        self.grid.select_initial_row()'''

# New _load_data method
NEW_LOAD_DATA = '''    def _load_data(self):
        """Load invoice heads from database."""
        try:
            self._data = self.repository.get_invoice_heads()
            self._filtered_data = self._data.copy()
            self._populate_model()
            self.grid.select_initial_row()
            self.status_label.setText(f"Načítaných {len(self._data)} faktúr")
        except Exception as e:
            self._data = []
            self._filtered_data = []
            self._populate_model()
            self.status_label.setText(f"Chyba: {e}")'''

# Old __init__ section to update (add repository)
OLD_INIT = '''        self.settings = settings
        self._data = []
        self._filtered_data = []
        self._items_windows = {}'''

NEW_INIT = '''        self.settings = settings
        self.repository = InvoiceRepository(settings)
        self._data = []
        self._filtered_data = []
        self._items_windows = {}'''

# Old method call
OLD_CALL = "self._load_test_data()"
NEW_CALL = "self._load_data()"


def main():
    if not TARGET_FILE.exists():
        print(f"ERROR: {TARGET_FILE} not found!")
        return

    content = TARGET_FILE.read_text(encoding="utf-8")
    original = content

    # 1. Add import
    if NEW_IMPORT not in content:
        # Find last import line in the import block
        import_marker = "from config.settings import Settings"
        if import_marker in content:
            content = content.replace(
                import_marker,
                f"{import_marker}\n{NEW_IMPORT}"
            )
            print(f"Added import: {NEW_IMPORT}")

    # 2. Add repository to __init__
    if OLD_INIT in content:
        content = content.replace(OLD_INIT, NEW_INIT)
        print("Updated __init__ - added repository")

    # 3. Replace _load_test_data with _load_data
    if OLD_LOAD_TEST_DATA in content:
        content = content.replace(OLD_LOAD_TEST_DATA, NEW_LOAD_DATA)
        print("Replaced _load_test_data() with _load_data()")

    # 4. Update method calls
    content = content.replace(OLD_CALL, NEW_CALL)
    print("Updated method calls")

    if content != original:
        # Backup
        backup = TARGET_FILE.with_suffix(".py.bak")
        backup.write_text(original, encoding="utf-8")
        print(f"Backup: {backup}")

        # Save
        TARGET_FILE.write_text(content, encoding="utf-8")
        print(f"Updated: {TARGET_FILE}")
    else:
        print("No changes needed")


if __name__ == "__main__":
    main()