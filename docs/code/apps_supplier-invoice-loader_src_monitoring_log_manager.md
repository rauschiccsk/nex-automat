# log_manager.py

**Path:** `apps\supplier-invoice-loader\src\monitoring\log_manager.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Log Manager for centralized logging with rotation and retention
Provides structured logging with automatic cleanup

---

## Classes

### LogConfig

Log manager configuration

---

### JsonFormatter(logging.Formatter)

JSON log formatter for structured logging

**Methods:**

#### `format(self, record)`

Format log record as JSON

---

### LogManager

Centralized log management system

**Methods:**

#### `__init__(self, config)`

Initialize log manager

Args:
    config: Log configuration

#### `_setup_logging(self)`

Setup logging configuration

#### `get_logger(self, name)`

Get logger instance

Args:
    name: Logger name (defaults to root)

Returns:
    Logger instance

#### `cleanup_old_logs(self, days)`

Remove log files older than retention period

Args:
    days: Number of days to retain (uses config if not specified)

Returns:
    Number of files deleted

#### `get_log_files(self)`

Get list of all log files

Returns:
    List of log file paths

#### `get_log_stats(self)`

Get log statistics

Returns:
    Dictionary with log statistics

#### `analyze_logs(self, level, since, limit)`

Analyze log entries

Args:
    level: Filter by log level
    since: Filter by timestamp
    limit: Maximum number of entries

Returns:
    List of log entries

#### `get_error_summary(self, hours)`

Get summary of errors in recent period

Args:
    hours: Number of hours to analyze

Returns:
    Error summary statistics

#### `set_level(self, level)`

Change log level dynamically

Args:
    level: New log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

#### `rotate_logs(self)`

Force log rotation

---

## Functions

### `setup_logging(log_dir, log_level, use_json, console)`

Quick setup for logging

Args:
    log_dir: Log directory path
    log_level: Log level
    use_json: Use JSON formatting
    console: Enable console output

Returns:
    LogManager instance

---
