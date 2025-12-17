# apply_xml_import_changes.py

**Path:** `apps\supplier-invoice-editor\scripts\apply_xml_import_changes.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Script na aplikovanie zmien pre XML import a NEX lookup funkcionalitu

Vytvori:
- scripts/import_xml_to_staging.py - Import XML do PostgreSQL
- src/business/nex_lookup_service.py - NEX Genesis lookup service
- database/schemas/002_add_nex_columns.sql - Nová migrácia

Modifikuje:
- src/business/invoice_service.py - Pridá NEX lookup
- src/ui/widgets/invoice_items_grid.py - Pridá farebné označenie

---

## Functions

### `create_file(relative_path, content)`

Vytvorí nový súbor s obsahom

---

### `main()`

---
