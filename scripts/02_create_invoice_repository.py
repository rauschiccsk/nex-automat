"""
Create invoice_repository.py in supplier-invoice-staging app.
"""

from pathlib import Path

TARGET_DIR = Path("apps/supplier-invoice-staging/database/repositories")
TARGET_FILE = TARGET_DIR / "invoice_repository.py"
INIT_FILE = TARGET_DIR / "__init__.py"

REPOSITORY_CODE = '''\
"""Invoice Repository - Database access for supplier invoices"""
from typing import List, Dict, Any, Optional
from contextlib import contextmanager
import psycopg2
from psycopg2.extras import RealDictCursor

from config.settings import Settings


class InvoiceRepository:
    """Repository for supplier invoice database operations."""

    def __init__(self, settings: Settings):
        self.settings = settings

    @contextmanager
    def _get_cursor(self):
        """Context manager for database cursor."""
        conn = None
        try:
            db = self.settings.database
            conn = psycopg2.connect(
                host=db.host,
                port=db.port,
                database=db.database,
                user=db.user,
                password=db.password
            )
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            yield cursor
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()

    def get_invoice_heads(self) -> List[Dict[str, Any]]:
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
            return [dict(row) for row in rows]

    def get_invoice_items(self, invoice_head_id: int) -> List[Dict[str, Any]]:
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
                item["in_nex"] = item.get("nex_product_id") is not None
                item["margin_percent"] = 0.0
                item["selling_price_excl_vat"] = 0.0
                item["selling_price_incl_vat"] = 0.0
                result.append(item)

            return result

    def update_item_pricing(self, item_id: int, margin_percent: float, 
                           selling_price_excl_vat: float, selling_price_incl_vat: float) -> bool:
        """Update pricing for single item."""
        query = """
            UPDATE supplier_invoice_items
            SET edited_unit_price = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        try:
            with self._get_cursor() as cur:
                cur.execute(query, (selling_price_excl_vat, item_id))
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error updating item {item_id}: {e}")
            return False

    def save_items_batch(self, items: List[Dict[str, Any]]) -> int:
        """Save multiple items at once. Returns count of updated items."""
        query = """
            UPDATE supplier_invoice_items
            SET edited_unit_price = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        updated = 0
        try:
            with self._get_cursor() as cur:
                for item in items:
                    if item.get("margin_percent", 0) > 0:
                        cur.execute(query, (
                            item.get("selling_price_excl_vat", 0),
                            item["id"]
                        ))
                        updated += cur.rowcount
            return updated
        except Exception as e:
            print(f"Error saving items batch: {e}")
            return 0

    def test_connection(self) -> tuple[bool, str]:
        """Test database connection. Returns (success, message)."""
        try:
            with self._get_cursor() as cur:
                cur.execute("SELECT 1")
                return True, "Connection OK"
        except Exception as e:
            return False, str(e)
'''

INIT_CODE = '''\
"""Database repositories"""
from .invoice_repository import InvoiceRepository

__all__ = ["InvoiceRepository"]
'''


def main():
    # Create directory if needed
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Directory: {TARGET_DIR}")

    # Create __init__.py
    INIT_FILE.write_text(INIT_CODE, encoding="utf-8")
    print(f"Created: {INIT_FILE}")

    # Create repository
    TARGET_FILE.write_text(REPOSITORY_CODE, encoding="utf-8")
    print(f"Created: {TARGET_FILE}")

    print("Done!")


if __name__ == "__main__":
    main()