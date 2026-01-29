"""Invoice Repository - Database access for supplier invoices"""

from contextlib import contextmanager
from typing import Any

import psycopg2
from config.settings import Settings
from psycopg2.extras import RealDictCursor


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
                host=db.host, port=db.port, database=db.database, user=db.user, password=db.password
            )
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            yield cursor
            conn.commit()
        except Exception:
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()

    def get_invoice_heads(self) -> list[dict[str, Any]]:
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
            return [dict(row) for row in rows]

    def get_invoice_items(self, invoice_head_id: int) -> list[dict[str, Any]]:
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
            WHERE head_id = %s
            ORDER BY xml_line_number
        """
        with self._get_cursor() as cur:
            cur.execute(query, (invoice_head_id,))
            rows = cur.fetchall()
            return [dict(row) for row in rows]

    def update_item_pricing(
        self, item_id: int, margin_percent: float, selling_price_excl_vat: float, selling_price_incl_vat: float
    ) -> bool:
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

    def save_items_batch(self, items: list[dict[str, Any]]) -> int:
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
                        cur.execute(query, (item.get("selling_price_excl_vat", 0), item["id"]))
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
