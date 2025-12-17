# database_restore.py

**Path:** `apps\supplier-invoice-loader\src\backup\database_restore.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Database Restore Module for NEX Automat
Restores PostgreSQL databases from backup files

Author: Zoltán Rausch, ICC Komárno
Date: 2025-11-21

---

## Classes

### DatabaseRestore

Manages PostgreSQL database restoration from backups

**Methods:**

#### `__init__(self, config_path)`

Initialize DatabaseRestore

Args:
    config_path: Path to configuration file

#### `list_backups(self, backup_type)`

List available backup files

Args:
    backup_type: Type of backups to list ('daily', 'weekly', 'all')

Returns:
    List of backup info dictionaries

#### `verify_backup(self, backup_path)`

Verify backup file integrity

Args:
    backup_path: Path to backup file

Returns:
    Tuple of (success, message)

#### `restore_database(self, backup_path, drop_existing, verify_first)`

Restore database from backup

Args:
    backup_path: Path to backup file
    drop_existing: Whether to drop existing database first
    verify_first: Whether to verify backup before restore

Returns:
    Tuple of (success, message)

#### `_drop_database(self)`

Drop existing database

#### `_create_database(self)`

Create new database

#### `get_restore_point_info(self, backup_path)`

Get information about a restore point

Args:
    backup_path: Path to backup file

Returns:
    Dictionary with restore point information

---

## Functions

### `load_config(config_path)`

Load configuration from YAML file with defaults.

---
