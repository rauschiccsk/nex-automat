# gscat_repository.py

**Path:** `packages\nexdata\nexdata\repositories\gscat_repository.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Repository for GSCAT (Katalóg)

---

## Classes

### GSCATRepository(Unknown)

Repository for accessing GSCAT records (Katalóg)

**Methods:**

#### `table_name(self)`

Get table file path

#### `from_bytes(self, data)`

Convert bytes to GSCATRecord

#### `to_bytes(self, record)`

Convert record to bytes

#### `get_by_code(self, code)`

Get GSCAT record by product code

Args:
    code: Product code

Returns:
    GSCATRecord if found, None otherwise

#### `search_by_name(self, search_term, limit)`

Search products by name

Args:
    search_term: Search term

Returns:
    List of matching records

#### `find_by_barcode(self, barcode)`

Find product by primary barcode in GSCAT - LIVE query

Most products (95%) have only one barcode stored in GSCAT.
This is faster than searching BARCODE table.

Args:
    barcode: Barcode string to search for

Returns:
    GSCATRecord if found, None otherwise

---
