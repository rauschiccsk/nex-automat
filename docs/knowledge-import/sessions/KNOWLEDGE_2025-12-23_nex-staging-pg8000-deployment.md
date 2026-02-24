# Session: nex-staging pg8000 Migration & Deployment

**Dátum:** 2025-12-22 - 2025-12-23
**Status:** 🔄 IN PROGRESS

---

## Dokončené úlohy ✅

1. **nex-staging package migrovaný z psycopg2 na pg8000**
   - `connection.py` - kompletne prepísaný pre pg8000 API
   - `staging_client.py` - prepísaný pre pg8000
   - `pyproject.toml` - dependency zmenená na pg8000>=1.30.0
   - Funguje vo venv32 (32-bit) aj venv64 (64-bit)

2. **Deployment na Mágerstav server**
   - Git checkout develop
   - nex-staging reinstalovaný
   - venv64 vytvorený s Python 3.12 64-bit pre GUI
   - PySide6, shared-pyside6, nex-staging nainštalované

3. **Konfigurácia opravená**
   - config_customer.py - nové cesty SUPPLIER-INVOICES/SUPPLIER-STAGING
   - main.py - StagingClient(config=pg_config) fix
   - Emoji odstránené z print statements

4. **Databáza supplier_invoice_staging vytvorená**
   - CREATE DATABASE supplier_invoice_staging
   - Schema 001_supplier_invoice_staging.sql aplikovaná

## Aktuálny problém ❌

```
[WARN] PostgreSQL staging error: list index out of range
```

Chyba v pg8000 kóde - pravdepodobne v Pg8000Cursor alebo StagingClient pri INSERT RETURNING.

## Riešenie (TODO)

Analyzovať stderr log a opraviť `list index out of range` chybu v:
- `packages/nex-staging/nex_staging/connection.py` - Pg8000Cursor.fetchone()
- `packages/nex-staging/nex_staging/staging_client.py` - insert_invoice_with_items()

## Dôležité príkazy

```powershell
# Development
cd C:\Development\nex-automat
python scripts/0X_fix_script.py
git add . && git commit -m "message" && git push

# Server Mágerstav
cd C:\Deployment\nex-automat
git pull
Stop-Service NEXAutomat
Start-Service NEXAutomat

# Logy
Get-Content C:\Deployment\nex-automat\logs\service-stdout.log -Tail 30
Get-Content C:\Deployment\nex-automat\logs\service-stderr.log -Tail 50

# GUI test
C:\Deployment\nex-automat\venv64\Scripts\python.exe "C:\Deployment\nex-automat\apps\supplier-invoice-staging\app.py"
```

## Štruktúra nex-staging

```
packages/nex-staging/
├── nex_staging/
│   ├── __init__.py
│   ├── connection.py        # pg8000 DatabaseConnection + Pg8000Cursor
│   ├── staging_client.py    # INSERT operácie
│   ├── models/
│   │   ├── invoice_head.py
│   │   └── invoice_item.py
│   └── repositories/
│       └── invoice_repository.py
└── pyproject.toml           # pg8000>=1.30.0
```
