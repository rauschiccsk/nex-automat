"""Invoice Repository - Database access for supplier invoices."""

from typing import List, Dict, Any, Optional

from nex_staging.connection import DatabaseConnection
from nex_staging.models import InvoiceHead, InvoiceItem, FileStatus


class InvoiceRepository:
    """Repository for supplier invoice database operations."""

    def __init__(self, db: DatabaseConnection):
        self.db = db

    def get_invoice_heads(
        self, 
        file_status: Optional[FileStatus] = None,
        limit: Optional[int] = None,
    ) -> List[InvoiceHead]:
        """Get invoice heads with optional filtering.

        Args:
            file_status: Filter by file status (received/staged/archived)
            limit: Maximum number of records to return

        Returns:
            List of InvoiceHead models
        """
        query = """
            SELECT 
                id,
                xml_invoice_number,
                xml_variable_symbol,
                xml_issue_date,
                xml_tax_point_date,
                xml_due_date,
                xml_currency,
                xml_supplier_ico,
                xml_supplier_name,
                xml_supplier_dic,
                xml_supplier_ic_dph,
                xml_iban,
                xml_swift,
                xml_total_without_vat,
                xml_total_vat,
                xml_total_with_vat,
                nex_supplier_id,
                nex_supplier_modify_id,
                nex_iban,
                nex_swift,
                nex_stock_id,
                nex_book_num,
                nex_payment_method_id,
                nex_price_list_id,
                nex_document_id,
                nex_invoice_doc_id,
                nex_delivery_doc_id,
                status,
                file_status,
                pdf_file_path,
                xml_file_path,
                file_basename,
                item_count,
                items_matched,
                match_percent,
                validation_status,
                validation_errors,
                created_at,
                updated_at,
                processed_at,
                imported_at
            FROM supplier_invoice_heads
            WHERE 1=1
        """
        params: List[Any] = []

        if file_status:
            query += " AND file_status = %s"
            params.append(file_status.value)

        query += " ORDER BY xml_issue_date DESC, id DESC"

        if limit:
            query += " LIMIT %s"
            params.append(limit)

        with self.db.get_cursor() as cur:
            cur.execute(query, params if params else None)
            rows = cur.fetchall()
            return [InvoiceHead(**dict(row)) for row in rows]

    def get_invoice_heads_dict(self) -> List[Dict[str, Any]]:
        """Get invoice heads as dictionaries (for grid compatibility)."""
        heads = self.get_invoice_heads()
        return [h.model_dump() for h in heads]

    def get_invoice_items(self, invoice_head_id: int) -> List[InvoiceItem]:
        """Get items for specific invoice.

        Args:
            invoice_head_id: ID of the invoice head

        Returns:
            List of InvoiceItem models
        """
        query = """
            SELECT 
                id,
                invoice_head_id,
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
                edited_unit_price,
                validation_status,
                created_at,
                updated_at
            FROM supplier_invoice_items
            WHERE invoice_head_id = %s
            ORDER BY xml_line_number
        """
        with self.db.get_cursor() as cur:
            cur.execute(query, (invoice_head_id,))
            rows = cur.fetchall()
            return [InvoiceItem(**dict(row)) for row in rows]

    def get_invoice_items_dict(self, invoice_head_id: int) -> List[Dict[str, Any]]:
        """Get invoice items as dictionaries (for grid compatibility)."""
        items = self.get_invoice_items(invoice_head_id)
        return [i.model_dump() for i in items]

    def update_file_status(
        self, 
        invoice_id: int, 
        file_status: FileStatus,
        pdf_file_path: Optional[str] = None,
        xml_file_path: Optional[str] = None,
    ) -> bool:
        """Update file status and paths for an invoice.

        Args:
            invoice_id: Invoice head ID
            file_status: New file status
            pdf_file_path: Optional new PDF path
            xml_file_path: Optional new XML path

        Returns:
            True if updated successfully
        """
        query = """
            UPDATE supplier_invoice_heads
            SET file_status = %s,
                updated_at = CURRENT_TIMESTAMP
        """
        params: List[Any] = [file_status.value]

        if pdf_file_path is not None:
            query += ", pdf_file_path = %s"
            params.append(pdf_file_path)

        if xml_file_path is not None:
            query += ", xml_file_path = %s"
            params.append(xml_file_path)

        query += " WHERE id = %s"
        params.append(invoice_id)

        try:
            with self.db.get_cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error updating invoice {invoice_id}: {e}")
            return False

    def update_item_pricing(
        self, 
        item_id: int, 
        selling_price_excl_vat: float,
    ) -> bool:
        """Update pricing for single item.

        Args:
            item_id: Item ID
            selling_price_excl_vat: New selling price

        Returns:
            True if updated successfully
        """
        query = """
            UPDATE supplier_invoice_items
            SET edited_unit_price = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        try:
            with self.db.get_cursor() as cur:
                cur.execute(query, (selling_price_excl_vat, item_id))
                return cur.rowcount > 0
        except Exception as e:
            print(f"Error updating item {item_id}: {e}")
            return False

    def save_items_batch(self, items: List[Dict[str, Any]]) -> int:
        """Save multiple items at once.

        Args:
            items: List of item dicts with 'id' and 'selling_price_excl_vat'

        Returns:
            Count of updated items
        """
        query = """
            UPDATE supplier_invoice_items
            SET edited_unit_price = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        updated = 0
        try:
            with self.db.get_cursor() as cur:
                for item in items:
                    if item.get("selling_price_excl_vat"):
                        cur.execute(query, (
                            item["selling_price_excl_vat"],
                            item["id"]
                        ))
                        updated += cur.rowcount
            return updated
        except Exception as e:
            print(f"Error saving items batch: {e}")
            return 0

    def test_connection(self) -> tuple[bool, str]:
        """Test database connection."""
        return self.db.test_connection()
