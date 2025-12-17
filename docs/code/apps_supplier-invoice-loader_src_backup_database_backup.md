# database_backup.py

**Path:** `apps\supplier-invoice-loader\src\backup\database_backup.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Database Backup Module
Handles PostgreSQL database backups with rotation, compression, and verification.

---

## Classes

### DatabaseBackup

Handles PostgreSQL database backups with rotation and verification.

**Methods:**

#### `__init__(self, backup_dir, db_config, retention_days, retention_weeks, compression_level)`

Initialize backup manager.

Args:
    backup_dir: Directory for storing backups
    db_config: Database connection configuration
    retention_days: Number of daily backups to keep
    retention_weeks: Number of weekly backups to keep
    compression_level: Gzip compression level (1-9)

#### `_setup_logging(self)`

Configure logging for backup operations.

#### `_create_directories(self)`

Create backup directory structure.

#### `create_backup(self, backup_type)`

Create database backup.

Args:
    backup_type: Type of backup ('daily' or 'weekly')

Returns:
    Path to created backup file, or None on failure

#### `_build_pg_dump_command(self, output_file)`

Build pg_dump command with connection parameters.

#### `_compress_backup(self, backup_file)`

Compress backup file with gzip.

#### `_generate_checksum(self, file_path)`

Generate SHA256 checksum for file.

#### `_save_checksum(self, backup_file, checksum)`

Save checksum to file.

#### `_verify_backup(self, backup_file)`

Verify backup file integrity.

#### `rotate_backups(self)`

Remove old backups based on retention policy.

#### `_rotate_directory(self, directory, max_age_days)`

Remove old backup files from directory.

#### `list_backups(self)`

List all available backups.

#### `_list_directory_backups(self, directory)`

List backups in directory.

---

## Functions

### `load_config(config_path)`

Load configuration from YAML file.

---
