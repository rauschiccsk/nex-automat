"""
Staging Client - INSERT operations for invoice processing.
Replaces PostgresStagingClient from nex-shared.
"""

import logging
from typing import Any

import pg8000.native

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
        config: dict[str, Any] | None = None,
    ):
        """
        Initialize staging client.

        Args:
            host, port, database, user, password: Connection parameters
            config: Alternative - dict with connection parameters
        """
        if config:
            self._host = config.get("host", "localhost")
            self._port = config.get("port", 5432)
            self._database = config.get("database", "supplier_invoice_staging")
            self._user = config.get("user", "postgres")
            self._password = config.get("password", "")
        else:
            self._host = host
            self._port = port
            self._database = database
            self._user = user
            self._password = password

        self.db = DatabaseConnection(
            host=self._host,
            port=self._port,
            database=self._database,
            user=self._user,
            password=self._password,
        )
        self._conn: pg8000.native.Connection | None = None

    def __enter__(self):
        """Context manager entry - establish connection."""
        self._conn = pg8000.native.Connection(
            host=self._host,
            port=self._port,
            database=self._database,
            user=self._user,
            password=self._password,
        )
        logger.debug("Database connection established")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close connection."""
        if self._conn:
            if exc_type is not None:
                logger.error(f"Transaction error: {exc_val}")
            self._conn.close()
            self._conn = None
        return False

    def _run(self, query: str, params: tuple = None):
        """Execute query with parameter conversion.

        pg8000.native uses named parameters (:name) with **kwargs,
        not positional parameters ($1) with list.
        """
        if params:
            converted_query = query
            param_dict = {}
            for i, value in enumerate(params):
                placeholder = f":p{i}"
                converted_query = converted_query.replace("%s", placeholder, 1)
                param_dict[f"p{i}"] = value
            return self._conn.run(converted_query, **param_dict)
        return self._conn.run(query)

    def check_duplicate_invoice(self, supplier_ico: str, invoice_number: str) -> bool:
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

        result = self._run(
            """
            SELECT COUNT(*) 
            FROM supplier_invoice_heads 
            WHERE xml_supplier_ico = %s 
              AND xml_invoice_number = %s
        """,
            (supplier_ico, invoice_number),
        )

        count = result[0][0] if result else 0

        if count > 0:
            logger.info(f"Duplicate invoice found: {supplier_ico}/{invoice_number}")

        return count > 0

    def insert_invoice_with_items(
        self,
        invoice_data: dict[str, Any],
        items_data: list[dict[str, Any]],
        isdoc_xml: str | None = None,
    ) -> int | None:
        """
        Insert invoice with items into staging database.

        Args:
            invoice_data: Invoice header data dict
            items_data: List of item dicts
            isdoc_xml: Optional ISDOC XML string (not stored)

        Returns:
            Invoice ID if successful, None otherwise
        """
        if not self._conn:
            raise RuntimeError("Not in context manager")

        try:
            result = self._run(
                """
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
            """,
                (
                    invoice_data.get("supplier_ico"),
                    invoice_data.get("supplier_name"),
                    invoice_data.get("supplier_dic"),
                    invoice_data.get("invoice_number"),
                    invoice_data.get("invoice_date"),
                    invoice_data.get("due_date"),
                    invoice_data.get("total_amount"),
                    invoice_data.get("total_vat"),
                    invoice_data.get("total_without_vat"),
                    invoice_data.get("currency", "EUR"),
                    invoice_data.get("file_basename"),
                    invoice_data.get("file_status", "received"),
                    invoice_data.get("pdf_file_path"),
                    invoice_data.get("xml_file_path"),
                    "pending",
                    len(items_data),
                ),
            )

            # pg8000.native.run() may return empty list for INSERT RETURNING
            if not result or len(result) == 0:
                raise RuntimeError("INSERT RETURNING failed - no result returned")
            invoice_id = result[0][0]
            logger.info(f"Inserted invoice: id={invoice_id}")

            for item in items_data:
                self._run(
                    """
                    INSERT INTO supplier_invoice_items (
                        head_id,
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
                """,
                    (
                        invoice_id,
                        item.get("line_number"),
                        item.get("name"),
                        item.get("quantity"),
                        item.get("unit"),
                        item.get("price_per_unit"),
                        item.get("ean"),
                        item.get("vat_rate"),
                    ),
                )

            logger.info(f"Inserted {len(items_data)} items for invoice {invoice_id}")
            return invoice_id

        except Exception:
            logger.exception("Failed to insert invoice with items")
            raise

    def update_file_status(
        self,
        invoice_id: int,
        file_status: str,
        pdf_file_path: str | None = None,
        xml_file_path: str | None = None,
    ) -> bool:
        """Update file status and paths for an invoice."""
        if not self._conn:
            raise RuntimeError("Not in context manager")

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

        self._run(query, tuple(params))
        success = self._conn.row_count > 0

        if success:
            logger.info(
                f"Updated file_status to '{file_status}' for invoice {invoice_id}"
            )

        return success

    def get_enrichment_stats(self, invoice_id: int | None = None) -> dict:
        """Get enrichment statistics."""
        if not self._conn:
            raise RuntimeError("Not in context manager")

        if invoice_id:
            result = self._run(
                """
                SELECT 
                    COUNT(*) FILTER (WHERE matched = TRUE) as matched,
                    COUNT(*) FILTER (WHERE matched = FALSE OR matched IS NULL) as not_matched,
                    COUNT(*) as total
                FROM supplier_invoice_items
                WHERE head_id = %s
            """,
                (invoice_id,),
            )
        else:
            result = self._run("""
                SELECT 
                    COUNT(*) FILTER (WHERE matched = TRUE) as matched,
                    COUNT(*) FILTER (WHERE matched = FALSE OR matched IS NULL) as not_matched,
                    COUNT(*) as total
                FROM supplier_invoice_items
            """)

        row = result[0] if result else (0, 0, 0)

        return {
            "matched": row[0] or 0,
            "not_matched": row[1] or 0,
            "total": row[2] or 0,
        }

    def test_connection(self) -> tuple:
        """Test database connection."""
        return self.db.test_connection()
