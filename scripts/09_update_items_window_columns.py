"""
Update invoice_items_window.py COLUMNS and invoice_repository.py get_invoice_items query.
"""

from pathlib import Path

# === ITEMS WINDOW UPDATE ===
ITEMS_WINDOW_FILE = Path("apps/supplier-invoice-staging/ui/invoice_items_window.py")

OLD_COLUMNS = '''    COLUMNS = [
        ("id", "ID", 50, False, False),
        ("line_number", "#", 40, True, False),
        ("xml_ean", "EAN", 120, True, False),
        ("xml_name", "Nazov (XML)", 200, True, False),
        ("nex_product_name", "Nazov (NEX)", 180, True, False),
        ("xml_quantity", "Mnozstvo", 70, True, False),
        ("xml_unit", "MJ", 50, True, False),
        ("xml_unit_price", "NC", 90, True, False),
        ("margin_percent", "Marza %", 80, True, True),
        ("selling_price_excl_vat", "PC bez DPH", 90, True, True),
        ("selling_price_incl_vat", "PC s DPH", 90, True, False),
        ("in_nex", "NEX", 50, True, False),
        ("matched_by", "Match", 60, True, False),
        ("item_status", "Stav", 70, True, False),
    ]'''

NEW_COLUMNS = '''    COLUMNS = [
        ("id", "ID", 50, True, False),
        ("xml_line_number", "#", 40, True, False),
        ("xml_seller_code", "Kod dod.", 80, True, False),
        ("xml_ean", "EAN", 120, True, False),
        ("xml_product_name", "Nazov (XML)", 200, True, False),
        ("nex_product_name", "Nazov (NEX)", 180, True, False),
        ("nex_ean", "EAN (NEX)", 120, True, False),
        ("xml_quantity", "Mnozstvo", 70, True, False),
        ("xml_unit", "MJ", 50, True, False),
        ("xml_unit_price", "JC bez DPH", 90, True, False),
        ("xml_unit_price_vat", "JC s DPH", 90, True, False),
        ("xml_total_price", "Spolu", 90, True, False),
        ("xml_vat_rate", "DPH %", 60, True, False),
        ("nex_product_id", "NEX Prod ID", 80, True, False),
        ("nex_stock_code", "Sklad kod", 80, True, False),
        ("matched", "Matched", 60, True, False),
        ("matched_by", "Match by", 70, True, False),
        ("match_confidence", "Confidence", 70, True, False),
        ("validation_status", "Stav", 70, True, False),
    ]'''

# Fix _update_row tuple unpacking
OLD_UPDATE_ROW = '''            for col, (col_key, _, _, _, _) in enumerate(self.COLUMNS):'''
NEW_UPDATE_ROW = '''            for col, (col_key, _, _, _, _) in enumerate(self.COLUMNS):'''

# Fix _populate_model tuple unpacking
OLD_POPULATE = '''            for col_key, _, _, _, editable in self.COLUMNS:'''
NEW_POPULATE = '''            for col_key, _, _, _, editable in self.COLUMNS:'''

# === REPOSITORY UPDATE ===
REPOSITORY_FILE = Path("apps/supplier-invoice-staging/database/repositories/invoice_repository.py")

OLD_ITEMS_QUERY = '''    def get_invoice_items(self, invoice_head_id: int) -> List[Dict[str, Any]]:
        """Get items for specific invoice."""
        query = """
            SELECT 
                id,
                xml_line_number as line_number,
                xml_ean,
                xml_product_name as xml_name,
                nex_product_name,
                xml_quantity,
                xml_unit,
                xml_unit_price,
                xml_vat_rate,
                COALESCE(edited_unit_price, xml_unit_price) as current_unit_price,
                nex_product_id,
                matched,
                matched_by,
                match_confidence,
                validation_status as item_status
            FROM supplier_invoice_items
            WHERE invoice_head_id = %s
            ORDER BY xml_line_number
        """
        with self._get_cursor() as cur:
            cur.execute(query, (invoice_head_id,))
            rows = cur.fetchall()

            result = []
            for row in rows:
                item = dict(row)
                # Compute display fields
                item["in_nex"] = item.get("nex_product_id") is not None
                item["margin_percent"] = 0.0
                item["selling_price_excl_vat"] = 0.0
                item["selling_price_incl_vat"] = 0.0
                result.append(item)

            return result'''

NEW_ITEMS_QUERY = '''    def get_invoice_items(self, invoice_head_id: int) -> List[Dict[str, Any]]:
        """Get items for specific invoice."""
        query = """
            SELECT 
                id,
                xml_line_number,
                xml_seller_code,
                xml_ean,
                xml_product_name,
                xml_quantity,
                xml_unit,
                xml_unit_price,
                xml_unit_price_vat,
                xml_total_price,
                xml_total_price_vat,
                xml_vat_rate,
                nex_product_id,
                nex_product_name,
                nex_ean,
                nex_stock_code,
                nex_stock_id,
                matched,
                matched_by,
                match_confidence,
                validation_status
            FROM supplier_invoice_items
            WHERE invoice_head_id = %s
            ORDER BY xml_line_number
        """
        with self._get_cursor() as cur:
            cur.execute(query, (invoice_head_id,))
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
            print(f"  Updated: {old[:60]}...")
            changed = True

    if changed:
        filepath.write_text(content, encoding="utf-8")
        print(f"Saved: {filepath}")
    else:
        print(f"No changes needed: {filepath}")

    return changed


def main():
    print("=== Updating invoice_items_window.py ===")
    update_file(ITEMS_WINDOW_FILE, [
        (OLD_COLUMNS, NEW_COLUMNS),
    ])

    print("\n=== Updating invoice_repository.py ===")
    update_file(REPOSITORY_FILE, [
        (OLD_ITEMS_QUERY, NEW_ITEMS_QUERY),
    ])

    print("\nDone!")


if __name__ == "__main__":
    main()