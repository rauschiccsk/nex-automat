# pab_repository.py

**Path:** `packages\nexdata\nexdata\repositories\pab_repository.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Repository for PAB (Adresár)

---

## Classes

### PABRepository(Unknown)

Repository for accessing PAB records (Adresár)

**Methods:**

#### `table_name(self)`

Get table file path

#### `from_bytes(self, data)`

Convert bytes to PABRecord

#### `to_bytes(self, record)`

Convert record to bytes

#### `get_by_code(self, code)`

Get PAB record by code

Args:
    code: Address code

Returns:
    PABRecord if found, None otherwise

#### `search_by_name(self, search_term)`

Search addresses by name

Args:
    search_term: Search term

Returns:
    List of matching records

#### `get_suppliers(self)`

Get all supplier records

Returns:
    List of supplier records

---
