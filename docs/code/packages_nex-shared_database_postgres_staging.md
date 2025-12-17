# postgres_staging.py

**Path:** `packages\nex-shared\database\postgres_staging.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

NEX Shared - PostgreSQL Staging Client
Database client for invoice staging operations.

---

## Classes

### PostgresStagingClient

PostgreSQL client for invoice staging operations.

Usage:
    config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'invoice_staging',
        'user': 'postgres',
        'password': 'secret'
    }

    with PostgresStagingClient(config) as client:
        is_dup = client.check_duplicate_invoice(ico, number)
        invoice_id = client.insert_invoice_with_items(invoice_data, items_data, xml)

**Methods:**

#### `__init__(self, config)`

Initialize PostgreSQL staging client.

Args:
    config: Connection configuration dict with keys:
            host, port, database, user, password

#### `__enter__(self)`

Context manager entry - establish connection.

#### `__exit__(self, exc_type, exc_val, exc_tb)`

Context manager exit - close connection.

#### `check_duplicate_invoice(self, supplier_ico, invoice_number)`

Check if invoice already exists in staging database.

Args:
    supplier_ico: Supplier ICO (tax ID)
    invoice_number: Invoice number

Returns:
    True if invoice exists, False otherwise

#### `insert_invoice_with_items(self, invoice_data, items_data, isdoc_xml)`

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

    items_data: List of item dicts with keys:
        - line_number (required)
        - name (required)
        - quantity (required)
        - unit
        - price_per_unit (required)
        - ean
        - vat_rate

    isdoc_xml: Optional ISDOC XML string

Returns:
    Invoice ID if successful, None otherwise

#### `get_pending_enrichment_items(self, invoice_id, limit)`

Get items WHERE in_nex IS NULL OR in_nex = FALSE

Args:
    invoice_id: Optional invoice ID to filter by
    limit: Maximum number of items to return

Returns:
    List of items with original and edited data

#### `update_nex_enrichment(self, item_id, gscat_record, matched_by)`

Update item with NEX Genesis data

Args:
    item_id: Item ID to update
    gscat_record: GSCATRecord from nexdata with product data
    matched_by: Method used for matching ('ean', 'name', 'manual')

Returns:
    True if update successful

#### `mark_no_match(self, item_id, reason)`

Mark item as not found in NEX Genesis

Args:
    item_id: Item ID to mark
    reason: Reason for no match

Returns:
    True if update successful

#### `get_enrichment_stats(self, invoice_id)`

Get enrichment statistics

Args:
    invoice_id: Optional invoice ID to filter by

Returns:
    Dictionary with enrichment statistics

---
