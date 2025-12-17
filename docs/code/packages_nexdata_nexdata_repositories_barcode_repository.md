# barcode_repository.py

**Path:** `packages\nexdata\nexdata\repositories\barcode_repository.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Repository for BARCODE (Čiarové kódy)

---

## Classes

### BARCODERepository(Unknown)

Repository for accessing BARCODE records (Čiarové kódy)

**Methods:**

#### `table_name(self)`

Get table file path

#### `from_bytes(self, data)`

Convert bytes to BarcodeRecord

#### `to_bytes(self, record)`

Convert record to bytes

#### `get_by_barcode(self, barcode)`

Get BARCODE record by barcode

Args:
    barcode: Barcode string

Returns:
    BarcodeRecord if found, None otherwise

#### `get_by_product_code(self, product_code)`

Get all barcodes for product code

Args:
    product_code: Product code

Returns:
    List of barcode records

#### `find_by_barcode(self, barcode)`

Find barcode record by barcode string - LIVE query

Args:
    barcode: Barcode string to search for
    
Returns:
    BarcodeRecord if found, None otherwise

---
