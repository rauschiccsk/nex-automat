# test_config.py

**Path:** `apps\supplier-invoice-loader\tests\unit\test_config.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Tests for configuration loading

---

## Functions

### `test_config_imports()`

Test that config module can be imported

---

### `test_config_has_required_attributes()`

Test that config has all required attributes

---

### `test_config_customer_name_type()`

Test that CUSTOMER_NAME is a string

---

### `test_config_paths_are_pathlib()`

Test that path configs are Path objects

---

### `test_config_storage_directories_exist()`

Test that storage directories are created

---

### `test_config_smtp_port_is_int()`

Test that SMTP_PORT is an integer

---

### `test_config_boolean_flags()`

Test that boolean flags are actually boolean

---

### `test_config_api_key_not_default()`

Test that API key has been changed from default (in production)

---

### `test_config_environment_variable_override()`

Test that environment variables override config values

---

### `test_config_log_level_valid()`

Test that LOG_LEVEL is a valid logging level

---

### `test_config_storage_base_exists()`

Test that STORAGE_BASE directory exists

---

### `test_config_customer_specific_file_exists()`

Test that config_customer.py exists (production check)

---

### `test_config_nex_genesis_url_format()`

Test that NEX_GENESIS_API_URL has valid format

---

### `test_config_email_addresses_format()`

Test that email addresses have valid format (basic check)

---
