"""
PostgreSQL Activities for ANDROS Invoice Worker.

Temporal activities for saving invoice data to PostgreSQL database.
Tables: supplier_invoice_heads, supplier_invoice_items
"""

import logging
import os
from datetime import datetime
from typing import Any, Dict, Optional

import asyncpg
from temporalio import activity

logger = logging.getLogger(__name__)


async def get_db_connection() -> asyncpg.Connection:
    """Create PostgreSQL database connection."""
    return await asyncpg.connect(
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=int(os.environ.get("POSTGRES_PORT", "5432")),
        database=os.environ.get("POSTGRES_DB", "nex_invoices"),
        user=os.environ.get("POSTGRES_USER", "postgres"),
        password=os.environ.get("POSTGRES_PASSWORD", ""),
    )


@activity.defn
async def save_invoice_to_postgres_activity(
    invoice_data: Dict[str, Any],
    supplier_id: str,
    customer_code: str = "ANDROS",
) -> Dict[str, Any]:
    """
    Save invoice header and items to PostgreSQL.

    Args:
        invoice_data: UnifiedInvoice data as dictionary
        supplier_id: Supplier identifier (e.g., "marso")
        customer_code: Customer code (default: "ANDROS")

    Returns:
        Dictionary with head_id, item_count, and status
    """
    invoice_number = invoice_data.get("invoice_number", "unknown")
    activity.logger.info(f"Saving invoice {invoice_number} to PostgreSQL")

    supplier_code = supplier_id.upper()
    conn = None

    try:
        conn = await get_db_connection()

        # Start transaction
        async with conn.transaction():
            # Insert invoice header
            head_id = await _insert_invoice_head(
                conn,
                invoice_data,
                customer_code,
                supplier_code,
            )

            # Insert invoice items
            items = invoice_data.get("items", [])
            item_count = 0
            for item in items:
                await _insert_invoice_item(conn, head_id, item)
                item_count += 1

        activity.logger.info(
            f"Invoice {invoice_number} saved: head_id={head_id}, items={item_count}"
        )

        return {
            "status": "success",
            "head_id": head_id,
            "invoice_number": invoice_number,
            "item_count": item_count,
            "customer_code": customer_code,
            "supplier_code": supplier_code,
        }

    except Exception as e:
        activity.logger.error(f"Failed to save invoice {invoice_number}: {e}")
        raise

    finally:
        if conn:
            await conn.close()


async def _insert_invoice_head(
    conn: asyncpg.Connection,
    invoice_data: Dict[str, Any],
    customer_code: str,
    supplier_code: str,
) -> int:
    """
    Insert invoice header into supplier_invoice_heads table.

    Returns:
        Generated head_id
    """
    # Parse dates
    invoice_date = _parse_datetime(invoice_data.get("invoice_date"))
    due_date = _parse_datetime(invoice_data.get("due_date"))
    delivery_date = _parse_datetime(invoice_data.get("delivery_date"))
    fetched_at = _parse_datetime(invoice_data.get("fetched_at")) or datetime.now()

    sql = """
        INSERT INTO supplier_invoice_heads (
            customer_code,
            supplier_code,
            supplier_id,
            supplier_name,
            invoice_number,
            external_invoice_id,
            invoice_date,
            due_date,
            delivery_date,
            total_without_vat,
            total_vat,
            total_with_vat,
            currency,
            source_type,
            status,
            supplier_ico,
            supplier_dic,
            supplier_ic_dph,
            fetched_at,
            created_at
        ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10,
            $11, $12, $13, $14, $15, $16, $17, $18, $19, NOW()
        )
        RETURNING id
    """

    head_id = await conn.fetchval(
        sql,
        customer_code,
        supplier_code,
        invoice_data.get("supplier_id", ""),
        invoice_data.get("supplier_name", ""),
        invoice_data.get("invoice_number", ""),
        invoice_data.get("external_invoice_id", ""),
        invoice_date,
        due_date,
        delivery_date,
        float(invoice_data.get("total_without_vat", 0)),
        float(invoice_data.get("total_vat", 0)),
        float(invoice_data.get("total_with_vat", 0)),
        invoice_data.get("currency", "EUR"),
        invoice_data.get("source_type", "api"),
        invoice_data.get("status", "pending"),
        invoice_data.get("supplier_ico"),
        invoice_data.get("supplier_dic"),
        invoice_data.get("supplier_ic_dph"),
        fetched_at,
    )

    return head_id


async def _insert_invoice_item(
    conn: asyncpg.Connection,
    head_id: int,
    item: Dict[str, Any],
) -> int:
    """
    Insert invoice item into supplier_invoice_items table.

    Returns:
        Generated item_id
    """
    sql = """
        INSERT INTO supplier_invoice_items (
            head_id,
            line_number,
            product_code,
            product_code_type,
            product_name,
            quantity,
            unit,
            unit_price,
            total_price,
            vat_rate,
            vat_amount,
            ean,
            supplier_product_code,
            nex_product_id,
            nex_product_code,
            match_confidence,
            created_at
        ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10,
            $11, $12, $13, $14, $15, $16, NOW()
        )
        RETURNING id
    """

    item_id = await conn.fetchval(
        sql,
        head_id,
        int(item.get("line_number", 0)),
        item.get("product_code", ""),
        item.get("product_code_type", ""),
        item.get("product_name", ""),
        float(item.get("quantity", 0)),
        item.get("unit", "PCE"),
        float(item.get("unit_price", 0)),
        float(item.get("total_price", 0)),
        float(item.get("vat_rate", 0)),
        float(item.get("vat_amount", 0)),
        item.get("ean"),
        item.get("supplier_product_code"),
        item.get("nex_product_id"),
        item.get("nex_product_code"),
        item.get("match_confidence"),
    )

    return item_id


def _parse_datetime(value: Any) -> Optional[datetime]:
    """Parse datetime from various formats."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        # Try ISO format
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            pass
        # Try common formats
        for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%Y.%m.%d"]:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
    return None


@activity.defn
async def check_invoice_exists_activity(
    invoice_number: str,
    supplier_code: str,
    customer_code: str = "ANDROS",
) -> bool:
    """
    Check if invoice already exists in database.

    Args:
        invoice_number: Invoice number to check
        supplier_code: Supplier code
        customer_code: Customer code

    Returns:
        True if invoice exists
    """
    conn = None
    try:
        conn = await get_db_connection()

        sql = """
            SELECT EXISTS(
                SELECT 1 FROM supplier_invoice_heads
                WHERE customer_code = $1
                  AND supplier_code = $2
                  AND invoice_number = $3
            )
        """

        exists = await conn.fetchval(sql, customer_code, supplier_code, invoice_number)
        return bool(exists)

    finally:
        if conn:
            await conn.close()


@activity.defn
async def update_invoice_status_activity(
    head_id: int,
    status: str,
) -> bool:
    """
    Update invoice status in database.

    Args:
        head_id: Invoice header ID
        status: New status value

    Returns:
        True if updated successfully
    """
    conn = None
    try:
        conn = await get_db_connection()

        sql = """
            UPDATE supplier_invoice_heads
            SET status = $1, updated_at = NOW()
            WHERE id = $2
        """

        result = await conn.execute(sql, status, head_id)
        return "UPDATE 1" in result

    finally:
        if conn:
            await conn.close()
