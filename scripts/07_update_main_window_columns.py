"""
Update main_window.py COLUMNS and invoice_repository.py query for all DB fields.
"""

from pathlib import Path

# === MAIN WINDOW UPDATE ===
MAIN_WINDOW_FILE = Path("apps/supplier-invoice-staging/ui/main_window.py")

OLD_COLUMNS = '''    COLUMNS = [
        ("id", "ID", 50, False),
        ("supplier_name", "Dodavatel", 150, True),
        ("invoice_number", "Cislo faktury", 120, True),
        ("invoice_date", "Datum", 90, True),
        ("total_amount", "Suma", 100, True),
        ("currency", "Mena", 50, True),
        ("status", "Stav", 80, True),
        ("item_count", "Poloziek", 60, True),
        ("match_percent", "Match%", 70, True),
    ]'''

NEW_COLUMNS = '''    COLUMNS = [
        ("id", "ID", 50, True),
        ("xml_invoice_number", "Cislo faktury", 100, True),
        ("xml_variable_symbol", "VS", 80, True),
        ("xml_issue_date", "Vystavena", 90, True),
        ("xml_due_date", "Splatnost", 90, True),
        ("xml_supplier_ico", "ICO", 80, True),
        ("xml_supplier_name", "Dodavatel", 180, True),
        ("xml_supplier_dic", "DIC", 100, True),
        ("xml_currency", "Mena", 50, True),
        ("xml_total_without_vat", "Bez DPH", 90, True),
        ("xml_total_vat", "DPH", 70, True),
        ("xml_total_with_vat", "S DPH", 90, True),
        ("nex_supplier_id", "NEX ID", 60, True),
        ("status", "Stav", 80, True),
        ("item_count", "Poloziek", 60, True),
        ("items_matched", "Matched", 60, True),
        ("match_percent", "Match%", 70, True),
        ("validation_status", "Validacia", 80, True),
    ]'''

# Fix _populate_model tuple unpacking (was 4 elements, now still 4)
OLD_POPULATE = '''    def _populate_model(self):
        self.model.removeRows(0, self.model.rowCount())
        for row_data in self._filtered_data:
            row_items = []
            for col_key, _, _, _ in self.COLUMNS:
                value = row_data.get(col_key, "")
                item = self.grid.create_item(value, editable=False)
                row_items.append(item)
            self.model.appendRow(row_items)
        self.title_label.setText(f"Faktury ({len(self._filtered_data)})")'''

NEW_POPULATE = '''    def _populate_model(self):
        self.model.removeRows(0, self.model.rowCount())
        for row_data in self._filtered_data:
            row_items = []
            for col_key, _, _, _ in self.COLUMNS:
                value = row_data.get(col_key, "")
                if isinstance(value, (int, float)) and col_key in ("xml_total_without_vat", "xml_total_vat", "xml_total_with_vat", "match_percent"):
                    value = f"{value:.2f}"
                item = self.grid.create_item(value, editable=False)
                row_items.append(item)
            self.model.appendRow(row_items)
        self.title_label.setText(f"Faktury ({len(self._filtered_data)})")'''

# Fix _on_row_selected to use new field names
OLD_ROW_SELECTED = '''    @Slot(int)
    def _on_row_selected(self, row: int):
        if 0 <= row < len(self._filtered_data):
            inv = self._filtered_data[row]
            self.status_label.setText(f"Faktura: {inv['invoice_number']} | {inv['supplier_name']}")'''

NEW_ROW_SELECTED = '''    @Slot(int)
    def _on_row_selected(self, row: int):
        if 0 <= row < len(self._filtered_data):
            inv = self._filtered_data[row]
            self.status_label.setText(f"Faktura: {inv['xml_invoice_number']} | {inv['xml_supplier_name']}")'''

# Fix hidden ID column (now visible)
OLD_HIDE_ID = '''        # Hide ID column
        self.grid.table_view.setColumnHidden(0, True)'''

NEW_HIDE_ID = '''        # ID column is now visible'''

# === REPOSITORY UPDATE ===
REPOSITORY_FILE = Path("apps/supplier-invoice-staging/database/repositories/invoice_repository.py")

OLD_QUERY = '''    def get_invoice_heads(self) -> List[Dict[str, Any]]:
        """Get all invoice heads for main grid."""
        query = """
            SELECT 
                id,
                xml_supplier_name as supplier_name,
                xml_invoice_number as invoice_number,
                xml_issue_date as invoice_date,
                xml_total_with_vat as total_amount,
                xml_currency as currency,
                status,
                item_count,
                match_percent
            FROM supplier_invoice_heads
            ORDER BY xml_issue_date DESC, id DESC
        """
        with self._get_cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return [dict(row) for row in rows]'''

NEW_QUERY = '''    def get_invoice_heads(self) -> List[Dict[str, Any]]:
        """Get all invoice heads for main grid."""
        query = """
            SELECT 
                id,
                xml_invoice_number,
                xml_variable_symbol,
                xml_issue_date,
                xml_due_date,
                xml_supplier_ico,
                xml_supplier_name,
                xml_supplier_dic,
                xml_currency,
                xml_total_without_vat,
                xml_total_vat,
                xml_total_with_vat,
                nex_supplier_id,
                status,
                item_count,
                items_matched,
                match_percent,
                validation_status
            FROM supplier_invoice_heads
            ORDER BY xml_issue_date DESC, id DESC
        """
        with self._get_cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return [dict(row) for row in rows]'''


def update_file(filepath: Path, replacements: list) -> bool:
    if not filepath.exists():
        print(f"ERROR: {filepath} not found!")
        return False

    content = filepath.read_text(encoding="utf-8")
    changed = False

    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"  Updated: {old[:50]}...")
            changed = True

    if changed:
        filepath.write_text(content, encoding="utf-8")
        print(f"Saved: {filepath}")
    else:
        print(f"No changes needed: {filepath}")

    return changed


def main():
    print("=== Updating main_window.py ===")
    update_file(MAIN_WINDOW_FILE, [
        (OLD_COLUMNS, NEW_COLUMNS),
        (OLD_POPULATE, NEW_POPULATE),
        (OLD_ROW_SELECTED, NEW_ROW_SELECTED),
        (OLD_HIDE_ID, NEW_HIDE_ID),
    ])

    print("\n=== Updating invoice_repository.py ===")
    update_file(REPOSITORY_FILE, [
        (OLD_QUERY, NEW_QUERY),
    ])

    print("\nDone!")


if __name__ == "__main__":
    main()