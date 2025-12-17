# config.py

**Path:** `apps\supplier-invoice-editor\src\utils\config.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Configuration Loader for Invoice Editor

---

## Classes

### Config

Configuration manager for Invoice Editor

**Methods:**

#### `__init__(self, config_path)`

#### `_load(self)`

Load configuration from YAML file

#### `_expand_env_vars(self, config)`

Expand environment variables

#### `get(self, key_path, default)`

Get config value by dot-notation path

#### `get_postgres_config(self)`

Get PostgreSQL configuration

#### `get_nex_genesis_config(self)`

Get NEX Genesis configuration

#### `nex_root_path(self)`

Get NEX Genesis root path

#### `nex_stores_path(self)`

Get NEX Genesis stores path

---

## Functions

### `load_config(config_path)`

Load configuration (singleton pattern)

---

### `get_config()`

Get config singleton instance

---
