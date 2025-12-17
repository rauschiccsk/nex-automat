# test_backup_database.py

**Path:** `apps\supplier-invoice-loader\tests\unit\test_backup_database.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Unit tests for backup_database.py
Tests backup creation, compression, verification, and rotation.

---

## Classes

### TestDatabaseBackupInit

Test DatabaseBackup initialization.

**Methods:**

#### `test_init_creates_directories(self, temp_backup_dir, db_config)`

Test that initialization creates required directories.

#### `test_init_sets_config(self, temp_backup_dir, db_config)`

Test that configuration is properly stored.

#### `test_init_creates_log_file(self, temp_backup_dir, db_config)`

Test that log file is created.

---

### TestBackupCreation

Test backup creation functionality.

**Methods:**

#### `test_create_backup_success(self, mock_subprocess, backup_manager, temp_backup_dir)`

Test successful backup creation.

#### `test_create_backup_pg_dump_failure(self, mock_subprocess, backup_manager)`

Test backup creation when pg_dump fails.

#### `test_create_backup_timeout(self, mock_subprocess, backup_manager)`

Test backup creation with timeout.

#### `test_create_weekly_backup(self, mock_subprocess, backup_manager)`

Test weekly backup is stored in correct directory.

---

### TestCompression

Test backup compression functionality.

**Methods:**

#### `test_compress_backup(self, backup_manager, temp_backup_dir)`

Test backup file compression.

#### `test_compress_backup_failure(self, backup_manager, temp_backup_dir)`

Test compression handles non-existent file.

---

### TestChecksumVerification

Test checksum generation and verification.

**Methods:**

#### `test_generate_checksum(self, backup_manager, temp_backup_dir)`

Test SHA256 checksum generation.

#### `test_save_and_verify_checksum(self, backup_manager, temp_backup_dir)`

Test checksum saving and verification.

#### `test_verify_backup_checksum_mismatch(self, backup_manager, temp_backup_dir)`

Test verification fails when checksum doesn't match.

#### `test_verify_backup_missing_checksum(self, backup_manager, temp_backup_dir)`

Test verification fails when checksum file missing.

---

### TestBackupRotation

Test backup rotation functionality.

**Methods:**

#### `test_rotate_backups_removes_old(self, backup_manager, temp_backup_dir)`

Test rotation removes old backups.

#### `test_rotate_backups_keeps_recent(self, backup_manager, temp_backup_dir)`

Test rotation keeps recent backups.

---

### TestBackupListing

Test backup listing functionality.

**Methods:**

#### `test_list_backups_empty(self, backup_manager)`

Test listing when no backups exist.

#### `test_list_backups_with_files(self, backup_manager, temp_backup_dir)`

Test listing backups.

---

### TestConfigLoading

Test configuration loading.

**Methods:**

#### `test_load_config_success(self, tmp_path)`

Test loading valid configuration.

---

### TestCommandInterface

Test command line interface.

**Methods:**

#### `test_pg_dump_command_building(self, mock_subprocess, backup_manager)`

Test pg_dump command is built correctly.

---

## Functions

### `temp_backup_dir(tmp_path)`

Create temporary backup directory.

---

### `db_config()`

Sample database configuration.

---

### `backup_manager(temp_backup_dir, db_config)`

Create DatabaseBackup instance for testing.

---
