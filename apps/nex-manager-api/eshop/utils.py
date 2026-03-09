"""ESHOP utility functions — order number generation."""

from datetime import datetime


def generate_order_number(tenant_id: int, brand_name: str, conn) -> str:
    """Generate unique order number in format PREFIX-YEAR-NNNNN.

    Uses advisory lock to prevent race conditions.

    Args:
        tenant_id: Tenant ID for isolation.
        brand_name: Brand name for prefix (first 2 chars uppercase).
        conn: Database connection (pg8000).

    Returns:
        Order number string, e.g. 'EM-2026-00001'.
    """
    prefix = brand_name[:2].upper()
    year = datetime.now().year

    cur = conn.cursor()

    # Advisory lock using tenant_id + year as key to prevent race conditions
    lock_key = tenant_id * 10000 + year
    cur.execute("SELECT pg_advisory_xact_lock(%s)", (lock_key,))

    # Find max sequence for this tenant + year
    pattern = f"{prefix}-{year}-%"
    cur.execute(
        "SELECT MAX(order_number) FROM eshop_orders "
        "WHERE tenant_id = %s AND order_number LIKE %s",
        (tenant_id, pattern),
    )
    row = cur.fetchone()
    max_number = row[0] if row else None

    if max_number:
        # Parse sequence from e.g. 'EM-2026-00042'
        parts = max_number.split("-")
        seq = int(parts[-1]) + 1
    else:
        seq = 1

    return f"{prefix}-{year}-{seq:05d}"
