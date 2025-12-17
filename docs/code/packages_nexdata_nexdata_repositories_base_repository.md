# base_repository.py

**Path:** `packages\nexdata\nexdata\repositories\base_repository.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Base Repository Pattern
Fix: Replace BtrStatus with BtrieveClient status codes

---

## Classes

### BaseRepository(Unknown, ABC)

Base repository providing common CRUD operations

**Methods:**

#### `__init__(self, btrieve_client)`

Initialize repository with Btrieve client

#### `table_name(self)`

Table name for BtrieveClient (e.g., 'gscat', 'barcode')

#### `from_bytes(self, data)`

Convert raw Btrieve bytes to model instance

#### `to_bytes(self, record)`

Convert model instance to raw Btrieve bytes

#### `open(self)`

Open Btrieve table

#### `close(self)`

Close Btrieve table

#### `__enter__(self)`

Context manager entry

#### `__exit__(self, exc_type, exc_val, exc_tb)`

Context manager exit

#### `get_first(self)`

Get first record in table

#### `get_next(self)`

Get next record in current position

#### `get_all(self, max_records)`

Get all records from table

#### `find(self, predicate, max_results)`

Find records matching predicate

#### `find_one(self, predicate)`

Find first record matching predicate

#### `exists(self, predicate)`

Check if any record matches predicate

---

### ReadOnlyRepository(Unknown, ABC)

Read-only repository (no write operations)

**Methods:**

#### `insert(self, record)`

Not implemented for read-only repository

#### `update(self, record)`

Not implemented for read-only repository

---

### CRUDRepository(Unknown, ABC)

Full CRUD repository with write operations

**Methods:**

#### `insert(self, record)`

Insert new record

#### `update(self, record)`

Update existing record

---
