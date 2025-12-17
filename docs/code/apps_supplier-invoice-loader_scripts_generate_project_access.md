# generate_project_access.py

**Path:** `apps\supplier-invoice-loader\scripts\generate_project_access.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Generate Project File Access Manifest
======================================

Vygeneruje unified JSON manifest pre supplier-invoice-loader projekt.
Používa sa po každom push do GitHub pre cache-busting.

Použitie:
    python scripts/generate_project_access.py

Output:
    supplier-invoice-loader_project_file_access.json

---

## Functions

### `get_git_commit_sha()`

Get current git commit SHA.

---

### `get_git_short_sha()`

Get short git commit SHA (12 chars).

---

### `categorize_file(file_path)`

Determine file category.

---

### `generate_manifest(project_root)`

Generate project file access manifest.

---
