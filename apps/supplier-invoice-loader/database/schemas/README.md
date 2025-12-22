# Database Schemas

Databázové schémy pre supplier-invoice-loader.

## Súbory

| Súbor | Popis |
|-------|-------|
| 001_initial_schema.sql | Základná schéma (supplier_invoice_heads, supplier_invoice_items) |
| 002_add_nex_columns.sql | NEX Genesis lookup stĺpce |
| test_schema.sql | Testovacie dáta |

## Migrácie

Migrácie sú v adresári `../migrations/`:

| Súbor | Popis |
|-------|-------|
| 003_add_file_tracking_columns.sql | File tracking pre novú organizáciu súborov |

## Spustenie migrácie

```powershell
$env:PGPASSWORD = $env:POSTGRES_PASSWORD
psql -h localhost -U postgres -d invoice_staging -f migrations/003_add_file_tracking_columns.sql
```
