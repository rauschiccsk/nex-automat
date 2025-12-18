"""
Update invoice_items_window.py to use real database queries instead of test data.
"""

from pathlib import Path

TARGET_FILE = Path("apps/supplier-invoice-staging/ui/invoice_items_window.py")

# New import to add
NEW_IMPORT = "from database.repositories import InvoiceRepository"

# Old import line to find
IMPORT_MARKER = "from config.settings import Settings"

# Old __init__ params section
OLD_INIT = '''    def __init__(self, invoice: dict, settings: Settings, parent=None):
        self.invoice = invoice
        self.settings = settings
        self._data: List[Dict[str, Any]] = []
        self._filtered_data: List[Dict[str, Any]] = []'''

NEW_INIT = '''    def __init__(self, invoice: dict, settings: Settings, repository: InvoiceRepository, parent=None):
        self.invoice = invoice
        self.settings = settings
        self.repository = repository
        self._data: List[Dict[str, Any]] = []
        self._filtered_data: List[Dict[str, Any]] = []'''

# Old _load_test_items method
OLD_LOAD_TEST_ITEMS = '''    def _load_test_items(self):
        self._data = [
            {"id": 1, "line_number": 1, "xml_ean": "8590123456789", "xml_name": "Mlieko 1L",
             "nex_product_name": "Mlieko polotucne 1L", "xml_quantity": 10, "xml_unit": "ks",
             "xml_unit_price": 1.20, "xml_vat_rate": 20.0, "margin_percent": 0.0,
             "selling_price_excl_vat": 0.0, "selling_price_incl_vat": 0.0,
             "in_nex": True, "matched_by": "ean", "item_status": "matched"},
            {"id": 2, "line_number": 2, "xml_ean": "8590123456790", "xml_name": "Chlieb",
             "nex_product_name": "", "xml_quantity": 5, "xml_unit": "ks",
             "xml_unit_price": 2.50, "xml_vat_rate": 20.0, "margin_percent": 0.0,
             "selling_price_excl_vat": 0.0, "selling_price_incl_vat": 0.0,
             "in_nex": False, "matched_by": "", "item_status": "pending"},
            {"id": 3, "line_number": 3, "xml_ean": "8590123456791", "xml_name": "Maslo 250g",
             "nex_product_name": "Maslo 82% 250g", "xml_quantity": 20, "xml_unit": "ks",
             "xml_unit_price": 3.80, "xml_vat_rate": 20.0, "margin_percent": 25.0,
             "selling_price_excl_vat": 4.75, "selling_price_incl_vat": 5.70,
             "in_nex": True, "matched_by": "ean", "item_status": "priced"},
            {"id": 4, "line_number": 4, "xml_ean": "8590123456792", "xml_name": "Jogurt biely",
             "nex_product_name": "Jogurt biely 150g", "xml_quantity": 30, "xml_unit": "ks",
             "xml_unit_price": 0.65, "xml_vat_rate": 20.0, "margin_percent": 0.0,
             "selling_price_excl_vat": 0.0, "selling_price_incl_vat": 0.0,
             "in_nex": True, "matched_by": "name", "item_status": "matched"},
            {"id": 5, "line_number": 5, "xml_ean": "8590123456793", "xml_name": "Syry Edamsky",
             "nex_product_name": "", "xml_quantity": 8, "xml_unit": "ks",
             "xml_unit_price": 4.20, "xml_vat_rate": 20.0, "margin_percent": 0.0,
             "selling_price_excl_vat": 0.0, "selling_price_incl_vat": 0.0,
             "in_nex": False, "matched_by": "", "item_status": "pending"},
        ]
        self._filtered_data = self._data.copy()
        self._populate_model()
        self.grid.select_initial_row()
        self.grid.table_view.setFocus()'''

# New _load_items method
NEW_LOAD_ITEMS = '''    def _load_items(self):
        """Load invoice items from database."""
        try:
            self._data = self.repository.get_invoice_items(self.invoice["id"])
            self._filtered_data = self._data.copy()
            self._populate_model()
            self.grid.select_initial_row()
            self.grid.table_view.setFocus()
        except Exception as e:
            self._data = []
            self._filtered_data = []
            self._populate_model()
            self.status_label.setText(f"Chyba: {e}")'''

# Old _save_items method
OLD_SAVE_ITEMS = '''    def _save_items(self):
        modified = [i for i in self._data if (i.get("margin_percent") or 0) > 0]
        print(f"Saving {len(modified)} modified items...")
        self.status_label.setText(f"Ulozene {len(modified)} poloziek")'''

# New _save_items method
NEW_SAVE_ITEMS = '''    def _save_items(self):
        """Save modified items to database."""
        modified = [i for i in self._data if (i.get("margin_percent") or 0) > 0]
        if not modified:
            self.status_label.setText("Žiadne položky na uloženie")
            return

        try:
            count = self.repository.save_items_batch(modified)
            self.status_label.setText(f"Uložených {count} položiek")
        except Exception as e:
            self.status_label.setText(f"Chyba pri ukladaní: {e}")'''

# Method call replacements
OLD_CALL = "self._load_test_items()"
NEW_CALL = "self._load_items()"


def main():
    if not TARGET_FILE.exists():
        print(f"ERROR: {TARGET_FILE} not found!")
        return

    content = TARGET_FILE.read_text(encoding="utf-8")
    original = content

    # 1. Add import
    if NEW_IMPORT not in content:
        if IMPORT_MARKER in content:
            content = content.replace(
                IMPORT_MARKER,
                f"{IMPORT_MARKER}\n{NEW_IMPORT}"
            )
            print(f"Added import: {NEW_IMPORT}")

    # 2. Update __init__ signature to accept repository
    if OLD_INIT in content:
        content = content.replace(OLD_INIT, NEW_INIT)
        print("Updated __init__ - added repository parameter")

    # 3. Replace _load_test_items with _load_items
    if OLD_LOAD_TEST_ITEMS in content:
        content = content.replace(OLD_LOAD_TEST_ITEMS, NEW_LOAD_ITEMS)
        print("Replaced _load_test_items() with _load_items()")

    # 4. Replace _save_items
    if OLD_SAVE_ITEMS in content:
        content = content.replace(OLD_SAVE_ITEMS, NEW_SAVE_ITEMS)
        print("Updated _save_items() to use repository")

    # 5. Update method calls
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