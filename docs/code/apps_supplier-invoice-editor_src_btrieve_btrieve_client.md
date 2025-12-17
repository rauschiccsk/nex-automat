# btrieve_client.py

**Path:** `apps\supplier-invoice-editor\src\btrieve\btrieve_client.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Python wrapper pre Pervasive Btrieve API (32-bit)
Adapted for supplier-invoice-editor Qt5 application

---

## Classes

### BtrieveClient

Python wrapper pre Pervasive Btrieve API (32-bit)

**Methods:**

#### `__init__(self, config)`

Initialize Btrieve client

#### `_load_dll(self)`

Load Btrieve DLL

#### `open_file(self, filename, owner_name, mode)`

Open Btrieve file

#### `close_file(self, pos_block)`

Close Btrieve file

#### `get_first(self, pos_block, key_num)`

Get first record

#### `get_next(self, pos_block)`

Get next record

#### `insert(self, pos_block, data)`

Insert new record

#### `update(self, pos_block, data)`

Update current record

#### `get_status_message(self, status_code)`

Convert status code to message

---

## Functions

### `open_btrieve_file(filename, config)`

Helper function to open Btrieve file

---
