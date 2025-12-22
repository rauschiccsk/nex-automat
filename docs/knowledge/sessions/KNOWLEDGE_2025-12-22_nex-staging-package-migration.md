# Session: nex-staging Package Migration

**Dátum:** 2025-12-22
**Status:** 🔄 IN PROGRESS

---

## Dokončené úlohy ✅

1. **Package nex-staging vytvorený** (packages/nex-staging/)
   - `connection.py` - DatabaseConnection manager
   - `models/invoice_head.py` - Pydantic model (41 stĺpcov)
   - `models/invoice_item.py` - Pydantic model
   - `repositories/invoice_repository.py` - SELECT operácie
   - `staging_client.py` - INSERT operácie (nahrada PostgresStagingClient)

2. **supplier-invoice-staging migrovaný**
   - Import z nex_staging namiesto database.repositories
   - GUI otestované - funguje ✅

3. **supplier-invoice-loader aktualizovaný**
   - Import zmenený: `from nex_staging import StagingClient`
   - PostgresStagingClient -> StagingClient

4. **nex-shared vyčistený**
   - postgres_staging.py odstránený
   - PostgresStagingClient export odstránený

## Aktuálny problém ❌

- supplier-invoice-loader používa venv32 (32-bit pre Btrieve)
- pip install nex-staging vo venv32 zlyháva (psycopg2-binary problém)

## Riešenie

- Použiť pg8000 namiesto psycopg2 vo venv32
- Alebo: nex-staging podporuje oba drivery

## Štruktúra nex-staging

```
packages/nex-staging/
├── nex_staging/
│   ├── __init__.py
│   ├── connection.py
│   ├── staging_client.py      # INSERT operácie
│   ├── models/
│   │   ├── invoice_head.py
│   │   └── invoice_item.py
│   └── repositories/
│       └── invoice_repository.py  # SELECT operácie
└── pyproject.toml
```

## Databáza

- **Správna DB:** supplier_invoice_staging
- **Správne tabuľky:** supplier_invoice_heads, supplier_invoice_items
- **Staré (VYMAZAŤ):** invoices_pending, invoice_items_pending, invoice_staging DB

## Dôležité príkazy

```powershell
# Test nex-staging
python -c "from nex_staging import StagingClient, InvoiceRepository; print('OK')"

# GUI test
cd apps/supplier-invoice-staging
python app.py

# Loader test (vo venv32)
cd apps/supplier-invoice-loader
python -c "from main import app; print('OK')"
```
