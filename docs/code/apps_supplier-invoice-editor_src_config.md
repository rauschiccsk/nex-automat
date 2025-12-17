# config.py

**Path:** `apps\supplier-invoice-editor\src\config.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Configuration for Supplier Invoice Editor

---

## Classes

### Config

Configuration class compatible with postgres_client expectations

**Methods:**

#### `__init__(self)`

Initialize config with database connection parameters

#### `get(self, key, default)`

Get configuration value

Args:
    key: Configuration key
    default: Default value if key not found

Returns:
    Configuration value or default

#### `__contains__(self, key)`

Support 'in' operator for postgres_client compatibility

---
