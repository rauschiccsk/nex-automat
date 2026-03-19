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

    # Advisory lock using prefix hash + year as key to prevent race conditions
    # Global lock per prefix+year — matches UNIQUE constraint scope
    lock_key = hash(prefix) % 2_000_000_000 + year
    cur.execute("SELECT pg_advisory_xact_lock(%s)", (lock_key,))

    # Find max sequence globally for this prefix + year (not per-tenant)
    pattern = f"{prefix}-{year}-%"
    cur.execute(
        "SELECT MAX(order_number) FROM eshop_orders WHERE order_number LIKE %s",
        (pattern,),
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
