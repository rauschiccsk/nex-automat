# Supplier Invoice Editor

**GUI approval workflow for supplier invoices before NEX import**

## Overview

GUI aplikácia pre kontrolu a schvaľovanie faktúr dodávateľov pred importom do NEX Genesis.

## Project Location

This is part of the **nex-automat** monorepo.

**Root:** `C:/Development/nex-automat/`  
**This app:** `apps/supplier-invoice-editor/`  
**Shared packages:** `packages/invoice-shared/`

## Dependencies

**Shared Packages:**
- `invoice-shared` - PostgreSQL models, database clients, utilities

## Running

```bash
# From monorepo root
cd apps/supplier-invoice-editor
uv run python -m src.main
```

## Database

**PostgreSQL:** `invoice_staging`  
**Tables:** `invoices_pending`, `invoice_items_pending`  
**Shared with:** supplier-invoice-loader

## Migration Notes

**Original name:** invoice-editor  
**Renamed to:** supplier-invoice-editor  
**Date:** 2025-11-18
