# Invoice Shared

**Shared utilities for invoice processing projects**

## Overview

Tento package obsahuje zdieľaný kód používaný v invoice processing projektoch:
- `supplier-invoice-loader` - Email → NEX automation
- `supplier-invoice-editor` - GUI approval workflow

## Structure

```
invoice_shared/
├── database/
│   └── postgres_staging.py    # PostgreSQL staging client
├── models/                     # SQLAlchemy models
├── schemas/                    # Pydantic schemas
└── utils/
    └── text_utils.py          # Text processing utilities
```

## Usage

```python
from invoice_shared.database import PostgresStagingClient
from invoice_shared.utils import normalize_text, clean_string

# PostgreSQL client
client = PostgresStagingClient()

# Text utilities
normalized = normalize_text("Some Text")
cleaned = clean_string("  text  ")
```

## Dependencies

- SQLAlchemy 2.0+ (PostgreSQL models)
- asyncpg (async PostgreSQL driver)
- Pydantic 2.0+ (schemas)

## Database

**PostgreSQL Database:** `invoice_staging`

**Tables:**
- `invoices_pending` - Invoice headers
- `invoice_items_pending` - Invoice line items

**Shared by:**
- apps/supplier-invoice-loader (writer)
- apps/supplier-invoice-editor (reader/updater)

## Development

This package is part of the nex-automat monorepo.

**Location:** `packages/invoice-shared/`
