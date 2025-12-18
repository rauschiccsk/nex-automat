"""
Fix get_invoice_items query in invoice_repository.py.
"""

from pathlib import Path
import re

REPOSITORY_FILE = Path("apps/supplier-invoice-staging/database/repositories/invoice_repository.py")

NEW_METHOD = '''    def get_invoice_items(self, invoice_head_id: int) -> List[Dict[str, Any]]:
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


def main():
    if not REPOSITORY_FILE.exists():
        print(f"ERROR: {REPOSITORY_FILE} not found!")
        return

    content = REPOSITORY_FILE.read_text(encoding="utf-8")

    # Find and replace the entire get_invoice_items method
    pattern = r'    def get_invoice_items\(self, invoice_head_id: int\).*?return \[dict\(row\) for row in rows\]'

    # Try to find method boundaries
    start_marker = "    def get_invoice_items(self, invoice_head_id: int)"
    end_marker = "    def update_item_pricing"

    if start_marker in content and end_marker in content:
        start_idx = content.index(start_marker)
        end_idx = content.index(end_marker)

        old_method = content[start_idx:end_idx]
        content = content[:start_idx] + NEW_METHOD + "\n\n" + content[end_idx:]

        REPOSITORY_FILE.write_text(content, encoding="utf-8")
        print(f"Updated get_invoice_items method")
        print(f"Saved: {REPOSITORY_FILE}")
    else:
        print("Could not find method boundaries")
        print(f"start_marker found: {start_marker in content}")
        print(f"end_marker found: {end_marker in content}")


if __name__ == "__main__":
    main()