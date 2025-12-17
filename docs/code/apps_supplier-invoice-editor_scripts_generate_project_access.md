# generate_project_access.py

**Path:** `apps\supplier-invoice-editor\scripts\generate_project_access.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Generate unified project_file_access.json manifest
Combines documentation, source code, and configuration
WITH CACHE BUSTING for fresh GitHub content

Invoice Editor - ISDOC approval and NEX Genesis integration

---

## Functions

### `get_current_commit_sha(repo_path)`

Get current Git commit SHA

---

### `should_skip(path)`

Check if path should be skipped

---

### `matches_include_pattern(file_name, patterns)`

Check if file name matches any include pattern

---

### `scan_category(category_name, config, base_path, base_url, cache_version)`

Scan files for a specific category

---

### `print_usage_urls(base_url, cache_version)`

Print ready-to-use URLs for next Claude chat

---

### `generate_manifest()`

Generate unified project file access manifest

---
