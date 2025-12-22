# nex-staging

Shared PostgreSQL models and repositories for invoice staging system.

## Installation

```bash
pip install -e packages/nex-staging
```

## Usage

```python
from nex_staging.connection import DatabaseConnection
from nex_staging.repositories import InvoiceRepository

# Initialize
db = DatabaseConnection(host="localhost", database="nex_automat", user="nex", password="...")
repo = InvoiceRepository(db)

# Get invoices
invoices = repo.get_invoice_heads()
items = repo.get_invoice_items(invoice_id=1)
```

## Structure

- `connection.py` - PostgreSQL connection manager with context manager
- `models/` - Pydantic models for type safety
- `repositories/` - Data access layer
