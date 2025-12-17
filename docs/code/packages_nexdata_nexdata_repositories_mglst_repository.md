# mglst_repository.py

**Path:** `packages\nexdata\nexdata\repositories\mglst_repository.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Repository for MGLST (Pohyby)

---

## Classes

### MGLSTRepository(Unknown)

Repository for accessing MGLST records (Pohyby)

**Methods:**

#### `table_name(self)`

Get table file path

#### `from_bytes(self, data)`

Convert bytes to MGLSTRecord

#### `to_bytes(self, record)`

Convert record to bytes

#### `get_by_product_code(self, product_code)`

Get all movements for product code

Args:
    product_code: Product code

Returns:
    List of movement records

#### `get_recent_movements(self, limit)`

Get recent movements (limited)

Args:
    limit: Maximum number of records

Returns:
    List of movement records

---
