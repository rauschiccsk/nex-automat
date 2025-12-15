# Supplier Invoice Loader

**Automated supplier invoice processing - Email to NEX Genesis**

## Overview

FastAPI aplikácia pre automatizované spracovanie faktúr dodávateľov:
- Email monitoring → PDF extraction → PostgreSQL staging → NEX Genesis import

## Project Location

This is part of the **nex-automat** monorepo.

**Root:** `C:/Development/nex-automat/`  
**This app:** `apps/supplier-invoice-loader/`  
**Shared packages:** `packages/invoice-shared/`

## Dependencies

**Runtime:**
- FastAPI, SQLAlchemy, asyncpg
- pypdf, Pillow (PDF/image processing)

**Shared Packages:**
- `invoice-shared` - PostgreSQL models, database clients, utilities

## Running

```bash
# From monorepo root
cd apps/supplier-invoice-loader
uv run python -m src.main

# Run tests
uv run pytest
```

## Database

**PostgreSQL:** `invoice_staging`  
**Tables:** `invoices_pending`, `invoice_items_pending`  
**Shared with:** supplier-invoice-editor

## Original Repository

Previously standalone at: https://github.com/rauschiccsk/supplier-invoice-loader  
Migrated to monorepo: 2025-11-18
