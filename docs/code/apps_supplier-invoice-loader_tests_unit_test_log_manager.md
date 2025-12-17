# test_log_manager.py

**Path:** `apps\supplier-invoice-loader\tests\unit\test_log_manager.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Tests for log manager system

---

## Functions

### `temp_log_dir()`

Create temporary log directory.

---

### `log_config(temp_log_dir)`

Create test log configuration

---

### `log_manager(log_config)`

Create log manager instance

---

### `test_log_manager_initialization(log_manager, temp_log_dir)`

Test log manager initializes correctly

---

### `test_log_directory_creation(temp_log_dir, log_config)`

Test log directory is created

---

### `test_logging_to_file(log_manager, temp_log_dir)`

Test logs are written to file

---

### `test_log_levels(log_manager)`

Test different log levels

---

### `test_get_log_files(log_manager, temp_log_dir)`

Test getting list of log files

---

### `test_log_stats(log_manager)`

Test log statistics

---

### `test_cleanup_old_logs(log_manager, temp_log_dir)`

Test cleanup of old log files

---

### `test_set_log_level(log_manager)`

Test changing log level dynamically

---

### `test_error_summary(log_manager)`

Test error summary generation

---

### `test_setup_logging_helper(temp_log_dir)`

Test quick setup helper function

---

### `test_json_logging(temp_log_dir)`

Test JSON formatted logging

---

### `test_named_logger(log_manager)`

Test getting named logger

---
