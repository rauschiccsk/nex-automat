"""
Staging Client - INSERT operations for invoice processing.
Replaces PostgresStagingClient from nex-shared.
"""
import logging
from typing import Optional, Dict, List, Any
from decimal import Decimal

from nex_staging.connection import DatabaseConnection

logger = logging.getLogger(__name__)


class StagingClient:
    """
    PostgreSQL client for invoice staging INSERT operations.
    Used by supplier-invoice-loader for saving new invoices.

    Usage:
        from nex_staging import StagingClient

        with StagingClient(host='localhost', database='supplier_invoice_staging', 
                          user='postgres', password='...') as client:
            is_dup = client.check_duplicate_invoice(ico, number)
            invoice_id = client.insert_invoice_with_items(invoice_data, items_data, xml)
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        database: str = "supplier_invoice_staging",
        user: str = "postgres",
        password: str = "",
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize staging client.

        Args:
            host, port, database, user, password: Connection parameters
            config: Alternative - dict with connection parameters
        """
        if config:
            self.db = DatabaseConnection(
                host=config.get('host', 'localhost'),
                port=config.get('port', 5432),
                database=config.get('database', 'supplier_invoice_staging'),
                user=config.get('user', 'postgres'),
                password=config.get('password', ''),
            )
        else:
            self.db = DatabaseConnection(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password,
            )
        self._conn = None
        self._cursor = None

    def __enter__(self):
        """Context manager entry - establish connection."""
        import psycopg2
        from psycopg2.extras import RealDictCursor

        self._conn = psycopg2.connect(
            host=self.db.config.host,
            port=self.db.config.port,
            database=self.db.config.database,
            user=self.db.config.user,
            password=self.db.config.password,
        )
        logger.debug("Database connection established")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - commit/rollback and close."""
        if self._conn:
            if exc_type is not None:
                self._conn.rollback()
                logger.error(f"Transaction rolled back: {exc_val}")
            else:
                self._conn.commit()
                logger.debug("Transaction committed")
            self._conn.close()
            self._conn = None
        return False

    def check_duplicate_invoice(
        self,
        supplier_ico: str,
        invoice_number: str
    ) -> bool:
        """
        Check if invoice already exists in staging database.

        Args:
            supplier_ico: Supplier ICO (tax ID)
            invoice_number: Invoice number

        Returns:
            True if invoice exists, False otherwise
        """
        if not self._conn:
            raise RuntimeError("Not in context manager")

        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) 
            FROM supplier_invoice_heads 
            WHERE xml_supplier_ico = %s 
              AND xml_invoice_number = %s
        """, (supplier_ico, invoice_number))

        count = cursor.fetchone()[0]
        cursor.close()

        if count > 0:
            logger.info(f"Duplicate invoice found: {supplier_ico}/{invoice_number}")

        return count > 0

    def insert_invoice_with_items(
        self,
        invoice_data: Dict[str, Any],
        items_data: List[Dict[str, Any]],
        isdoc_xml: Optional[str] = None
    ) -> Optional[int]:
        """
        Insert invoice with items into staging database.

        Args:
            invoice_data: Invoice header data dict with keys:
                - supplier_ico (required)
                - supplier_name
                - supplier_dic
                - invoice_number (required)
                - invoice_date (required)
                - due_date
                - total_amount (required)
                - total_vat
                - total_without_vat
                - currency (default: EUR)
                - file_basename
                - file_status
                - pdf_file_path
                - xml_file_path

            items_data: List of item dicts with keys:
                - line_number (required)
                - name (required)
                - quantity (required)
                - unit
                - price_per_unit (required)
                - ean
                - vat_rate

            isdoc_xml: Optional ISDOC XML string (not stored, kept for compatibility)

        Returns:
            Invoice ID if successful, None otherwise
        """
        if not self._conn:
            raise RuntimeError("Not in context manager")

        try:
            cursor = self._conn.cursor()

            # Insert invoice header into supplier_invoice_heads
            cursor.execute("""
                INSERT INTO supplier_invoice_heads (
                    xml_supplier_ico,
                    xml_supplier_name,
                    xml_supplier_dic,
                    xml_invoice_number,
                    xml_issue_date,
                    xml_due_date,
                    xml_total_with_vat,
                    xml_total_vat,
                    xml_total_without_vat,
                    xml_currency,
                    file_basename,
                    file_status,
                    pdf_file_path,
                    xml_file_path,
                    status,
                    item_count
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                RETURNING id
            """, (
                invoice_data.get('supplier_ico'),
                invoice_data.get('supplier_name'),
                invoice_data.get('supplier_dic'),
                invoice_data.get('invoice_number'),
                invoice_data.get('invoice_date'),
                invoice_data.get('due_date'),
                invoice_data.get('total_amount'),
                invoice_data.get('total_vat'),
                invoice_data.get('total_without_vat'),
                invoice_data.get('currency', 'EUR'),
                invoice_data.get('file_basename'),
                invoice_data.get('file_status', 'received'),
                invoice_data.get('pdf_file_path'),
                invoice_data.get('xml_file_path'),
                'pending',
                len(items_data)
            ))

            invoice_id = cursor.fetchone()[0]
            logger.info(f"Inserted invoice: id={invoice_id}")

            # Insert invoice items into supplier_invoice_items
            for item in items_data:
                cursor.execute("""
                    INSERT INTO supplier_invoice_items (
                        invoice_head_id,
                        xml_line_number,
                        xml_product_name,
                        xml_quantity,
                        xml_unit,
                        xml_unit_price,
                        xml_ean,
                        xml_vat_rate
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """, (
                    invoice_id,
                    item.get('line_number'),
                    item.get('name'),
                    item.get('quantity'),
                    item.get('unit'),
                    item.get('price_per_unit'),
                    item.get('ean'),
                    item.get('vat_rate')
                ))

            cursor.close()
            logger.info(f"Inserted {len(items_data)} items for invoice {invoice_id}")

            return invoice_id

        except Exception as e:
            logger.exception("Failed to insert invoice with items")
            raise

    def update_file_status(
        self,
        invoice_id: int,
        file_status: str,
        pdf_file_path: Optional[str] = None,
        xml_file_path: Optional[str] = None,
    ) -> bool:
        """
        Update file status and paths for an invoice.

        Args:
            invoice_id: Invoice head ID
            file_status: New status ('received', 'staged', 'archived')
            pdf_file_path: Optional new PDF path
            xml_file_path: Optional new XML path

        Returns:
            True if updated successfully
        """
        if not self._conn:
            raise RuntimeError("Not in context manager")

        cursor = self._conn.cursor()

        query = """
            UPDATE supplier_invoice_heads
            SET file_status = %s,
                updated_at = CURRENT_TIMESTAMP
        """
        params = [file_status]

        if pdf_file_path is not None:
            query += ", pdf_file_path = %s"
            params.append(pdf_file_path)

        if xml_file_path is not None:
            query += ", xml_file_path = %s"
            params.append(xml_file_path)

        query += " WHERE id = %s"
        params.append(invoice_id)

        cursor.execute(query, params)
        success = cursor.rowcount > 0
        cursor.close()

        if success:
            logger.info(f"Updated file_status to '{file_status}' for invoice {invoice_id}")

        return success

    def get_enrichment_stats(self, invoice_id: Optional[int] = None) -> Dict:
        """
        Get enrichment statistics.

        Args:
            invoice_id: Optional invoice ID to filter by

        Returns:
            Dictionary with enrichment statistics
        """
        if not self._conn:
            raise RuntimeError("Not in context manager")

        cursor = self._conn.cursor()

        if invoice_id:
            cursor.execute("""
                SELECT 
                    COUNT(*) FILTER (WHERE matched = TRUE) as matched,
                    COUNT(*) FILTER (WHERE matched = FALSE OR matched IS NULL) as not_matched,
                    COUNT(*) as total
                FROM supplier_invoice_items
                WHERE invoice_head_id = %s
            """, (invoice_id,))
        else:
            cursor.execute("""
                SELECT 
                    COUNT(*) FILTER (WHERE matched = TRUE) as matched,
                    COUNT(*) FILTER (WHERE matched = FALSE OR matched IS NULL) as not_matched,
                    COUNT(*) as total
                FROM supplier_invoice_items
            """)

        row = cursor.fetchone()
        cursor.close()

        return {
            'matched': row[0] or 0,
            'not_matched': row[1] or 0,
            'total': row[2] or 0
        }

    def test_connection(self) -> tuple:
        """Test database connection."""
        return self.db.test_connection()
