# backup_database.py

**Path:** `apps\supplier-invoice-loader\scripts\backup_database.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Database Backup Script - CLI Wrapper
Automated PostgreSQL backup with rotation, compression, and verification.

---

## CLI Arguments

| Argument | Description |
|----------|-------------|
| `--config` | Path to configuration file |
| `--type` | Backup type |
| `--backup-dir` | Backup directory |
| `--verify` | Verify existing backup file |
| `--list` | List all backups |
| `--rotate` | Rotate old backups only |

---

## Functions

### `main()`

Main entry point for backup script.

---
