"""Partner catalog versioning utility functions.

Provides sync functions for querying partner version history.
Uses pg8000 cursor (synchronous) — consistent with the rest of the codebase.
"""

_HISTORY_COLUMNS = (
    "history_id, partner_id, modify_id, "
    "partner_code, partner_name, reg_name, "
    "company_id, tax_id, vat_id, is_vat_payer, "
    "is_supplier, is_customer, "
    "street, city, zip_code, country_code, "
    "partner_class, "
    "valid_from, valid_to, changed_by"
)


def _row_to_dict(row: tuple) -> dict:
    """Map a history row tuple to a dict."""
    keys = [
        "history_id",
        "partner_id",
        "modify_id",
        "partner_code",
        "partner_name",
        "reg_name",
        "company_id",
        "tax_id",
        "vat_id",
        "is_vat_payer",
        "is_supplier",
        "is_customer",
        "street",
        "city",
        "zip_code",
        "country_code",
        "partner_class",
        "valid_from",
        "valid_to",
        "changed_by",
    ]
    return dict(zip(keys, row))


def get_partner_at_version(conn, partner_id: int, modify_id: int) -> dict | None:
    """Získaj partnera v konkrétnej verzii z history tabuľky.

    Args:
        conn: pg8000 database connection
        partner_id: Partner ID
        modify_id: Version number

    Returns:
        dict with version data or None if not found
    """
    cur = conn.cursor()
    cur.execute(
        f"SELECT {_HISTORY_COLUMNS} FROM partner_catalog_history "
        "WHERE partner_id = %s AND modify_id = %s",
        (partner_id, modify_id),
    )
    row = cur.fetchone()
    if not row:
        return None
    return _row_to_dict(row)


def get_current_partner_version(conn, partner_id: int) -> dict | None:
    """Získaj aktuálnu verziu partnera (valid_to IS NULL).

    Args:
        conn: pg8000 database connection
        partner_id: Partner ID

    Returns:
        dict with current version data or None if not found
    """
    cur = conn.cursor()
    cur.execute(
        f"SELECT {_HISTORY_COLUMNS} FROM partner_catalog_history "
        "WHERE partner_id = %s AND valid_to IS NULL",
        (partner_id,),
    )
    row = cur.fetchone()
    if not row:
        return None
    return _row_to_dict(row)
