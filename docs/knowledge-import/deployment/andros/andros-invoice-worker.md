# ANDROS Invoice Worker - Complete Guide

**Status:** PRODUCTION READY
**Aplikácia:** `apps/andros-invoice-worker/`
**Prostredia:** Dev PC (Windows), ANDROS Server (Ubuntu/Windows)
**Posledná aktualizácia:** 2026-01-27

---

## 1. Prehľad

### 1.1 Účel
Dedikovaná aplikácia pre ANDROS s.r.o. na automatizovaný import dodávateľských faktúr z API dodávateľov (MARSO, budúci Continental, Goodyear) do PostgreSQL staging tabuliek.

### 1.2 Workflow
```
MARSO SOAP API → JSON → UnifiedInvoice → PostgreSQL Staging → ISDOC XML → NEX Genesis
                                              ↓
                        supplier_invoice_heads + supplier_invoice_items
                        (customer_code='ANDROS', supplier_code='MARSO')
```

### 1.3 Architektúra
```
┌─────────────────────────────────────────────────────────────────┐
│ MARSO SOAP API (195.228.175.10:8081)                            │
│   └── CallComax method                                          │
│       └── CustInvoiceList (MessageType)                         │
│           └── Response: XML with embedded JSON                  │
└──────────────────────┬──────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│ andros-invoice-worker (Temporal Workflow)                       │
│   ├── MARSOAdapter - SOAP client (zeep)                         │
│   ├── postgres_activities - INSERT heads + items                │
│   ├── MARSOToISDOCConverter - JSON → ISDOC XML                  │
│   └── Scheduler - Temporal Schedule (daily 6:00)                │
└──────────────────────┬──────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│ PostgreSQL Staging                                              │
│   ├── supplier_invoice_heads (customer_code, supplier_code)     │
│   └── supplier_invoice_items (product matching ready)           │
└──────────────────────┬──────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│ Archive & Storage                                               │
│   ├── JSON: /SUPPLIER-INVOICES/MARSO/YYYY/MM/*.json (raw)       │
│   └── XML:  /SUPPLIER-INVOICES/MARSO/YYYY/MM/*.xml  (ISDOC)     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Súborová štruktúra

```
apps/andros-invoice-worker/
├── __init__.py
├── adapters/
│   ├── __init__.py
│   ├── base_adapter.py           # Abstraktná trieda, SupplierConfig
│   └── marso_adapter.py          # MARSO SOAP adapter (zeep)
├── activities/
│   ├── __init__.py
│   ├── supplier_api_activities.py # API activities (fetch, convert)
│   └── postgres_activities.py     # ★ NEW: INSERT heads + items
├── config/
│   ├── __init__.py
│   ├── settings.py               # Pydantic settings (DB, Temporal)
│   ├── config_loader.py          # YAML config loader
│   └── suppliers/
│       ├── __init__.py
│       └── marso.yaml            # MARSO konfigurácia
├── converters/
│   ├── __init__.py
│   └── marso_to_isdoc.py         # JSON → ISDOC XML
├── models/
│   ├── __init__.py
│   └── unified_invoice.py        # UnifiedInvoice, InvoiceItem
├── scheduler/
│   ├── __init__.py
│   └── schedule_manager.py       # ★ Temporal Schedule manager
├── scripts/
│   ├── __init__.py
│   └── setup_schedules.py        # CLI pre schedule management
├── sql/
│   └── create_tables.sql         # ★ PostgreSQL schema
├── workflows/
│   ├── __init__.py
│   └── api_invoice_workflow.py   # ANDROSInvoiceWorkflow
├── workers/
│   ├── __init__.py
│   └── main_worker.py            # Temporal worker entry point
├── tests/
│   ├── __init__.py
│   └── test_marso_adapter.py     # 11 unit testov
├── requirements.txt
└── .env.example
```

---

## 3. PostgreSQL Staging Schema

### 3.1 Tabuľka: supplier_invoice_heads

```sql
CREATE TABLE supplier_invoice_heads (
    id SERIAL PRIMARY KEY,

    -- Multi-tenant identifikácia
    customer_code VARCHAR(50) NOT NULL,     -- 'ANDROS'
    supplier_code VARCHAR(50) NOT NULL,     -- 'MARSO'
    supplier_id VARCHAR(50) NOT NULL,       -- 'marso'
    supplier_name VARCHAR(255),

    -- Faktúra
    invoice_number VARCHAR(100) NOT NULL,
    external_invoice_id VARCHAR(100),
    invoice_date TIMESTAMP,
    due_date TIMESTAMP,
    delivery_date TIMESTAMP,

    -- Sumy
    total_without_vat DECIMAL(15, 2),
    total_vat DECIMAL(15, 2),
    total_with_vat DECIMAL(15, 2),
    currency VARCHAR(3) DEFAULT 'EUR',

    -- Status
    source_type VARCHAR(20) DEFAULT 'api',
    status VARCHAR(50) DEFAULT 'pending',

    -- Dodávateľ
    supplier_ico VARCHAR(50),
    supplier_dic VARCHAR(50),
    supplier_ic_dph VARCHAR(50),

    -- Timestamps
    fetched_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP,

    UNIQUE (customer_code, supplier_code, invoice_number)
);
```

### 3.2 Tabuľka: supplier_invoice_items

```sql
CREATE TABLE supplier_invoice_items (
    id SERIAL PRIMARY KEY,
    head_id INTEGER REFERENCES supplier_invoice_heads(id) ON DELETE CASCADE,

    -- Položka
    line_number INTEGER NOT NULL,
    product_code VARCHAR(100),
    product_code_type VARCHAR(50),     -- 'ean', 'marso_code'
    product_name VARCHAR(500),

    -- Množstvo a ceny
    quantity DECIMAL(15, 4),
    unit VARCHAR(20),
    unit_price DECIMAL(15, 4),
    total_price DECIMAL(15, 2),
    vat_rate DECIMAL(5, 2),
    vat_amount DECIMAL(15, 2),

    -- Alternatívne kódy
    ean VARCHAR(50),
    supplier_product_code VARCHAR(100),

    -- NEX Genesis mapping (vyplnené po product matching)
    nex_product_id VARCHAR(50),
    nex_product_code VARCHAR(100),
    match_confidence DECIMAL(5, 2),

    created_at TIMESTAMP DEFAULT NOW(),

    UNIQUE (head_id, line_number)
);
```

### 3.3 Vytvorenie tabuliek

```bash
# Na ANDROS Ubuntu Docker Host
docker exec -it nex-postgres psql -U nex_admin -d nex_automat \
  -f /path/to/create_tables.sql

# Alebo priamo
cat apps/andros-invoice-worker/sql/create_tables.sql | \
  docker exec -i nex-postgres psql -U nex_admin -d nex_automat
```

---

## 4. Temporal Workflow

### 4.1 ANDROSInvoiceWorkflow

```python
@workflow.defn
class ANDROSInvoiceWorkflow:
    """
    Flow:
    1. Load supplier configuration
    2. Authenticate with supplier API
    3. Fetch list of invoices for date range
    4. For each invoice:
       - Check if already exists in DB (duplicate check)
       - Fetch invoice details
       - Convert to UnifiedInvoice format
       - Save to PostgreSQL (heads + items)
       - Convert to ISDOC XML
       - Archive raw data and XML
       - Post to invoice pipeline (optional)
       - Acknowledge to supplier
    """
```

### 4.2 Activities

| Activity | Popis |
|----------|-------|
| `fetch_supplier_config_activity` | Load YAML config |
| `authenticate_supplier_activity` | SOAP authentication |
| `fetch_invoice_list_activity` | CustInvoiceList API call |
| `fetch_invoice_detail_activity` | CustInvoiceLines API call |
| `convert_to_unified_activity` | JSON → UnifiedInvoice |
| `save_invoice_to_postgres_activity` | ★ INSERT heads + items |
| `check_invoice_exists_activity` | ★ Duplicate check |
| `update_invoice_status_activity` | ★ Status update |
| `convert_to_isdoc_activity` | JSON → ISDOC XML |
| `archive_raw_data_activity` | Save JSON + XML |
| `post_isdoc_to_pipeline_activity` | POST to FastAPI |
| `acknowledge_invoice_activity` | Mark as processed |

---

## 5. Temporal Schedule

### 5.1 Schedule Manager

```python
from scheduler.schedule_manager import ScheduleManager

manager = ScheduleManager(client, task_queue="andros-invoice-queue")

# Vytvoriť MARSO schedule (denne o 6:00, 7 dní dozadu)
await manager.create_marso_schedule(
    schedule_id="andros-marso-daily",
    cron_expression="0 6 * * *",
    lookback_days=7,
    customer_code="ANDROS",
)
```

### 5.2 CLI Management

```bash
# Setup všetkých schedules
python scripts/setup_schedules.py

# List schedules
python scripts/setup_schedules.py --list

# Trigger immediately
python scripts/setup_schedules.py --trigger marso

# Pause/unpause
python scripts/setup_schedules.py --pause marso
python scripts/setup_schedules.py --unpause marso
```

### 5.3 Schedule konfigurácia

| Parameter | Hodnota |
|-----------|---------|
| Schedule ID | `andros-marso-daily` |
| Cron | `0 6 * * *` (denne o 6:00) |
| Lookback | 7 dní |
| Overlap | SKIP (nespúšťať ak beží) |
| Catchup | 1 hodina |

---

## 6. Environment Variables

### 6.1 .env súbor

```bash
# Temporal Server
TEMPORAL_HOST=localhost
TEMPORAL_PORT=7233
TEMPORAL_NAMESPACE=default
TEMPORAL_TASK_QUEUE=andros-invoice-queue

# PostgreSQL Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=nex_invoices
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password_here

# MARSO API Credentials
MARSO_API_KEY=feixRjG254zft3zqnxx4kACZHEyX01
MARSO_ACCOUNT_NUM=339792
MARSO_USE_TEST=false

# ANDROS Customer
CUSTOMER_CODE=ANDROS

# Archive Path
ARCHIVE_PATH=C:/NEX/YEARACT/ARCHIV

# Logging
LOG_LEVEL=INFO
```

---

## 7. Deployment

### 7.1 Spustenie workera

**Windows (ANDROS VM):**
```powershell
cd C:\ANDROS\nex-automat\apps\andros-invoice-worker
.\venv\Scripts\activate
python -m workers.main_worker
```

**Linux (Ubuntu):**
```bash
cd /opt/nex-automat-src/apps/andros-invoice-worker
source venv/bin/activate
python -m workers.main_worker
```

### 7.2 Setup schedules

```bash
# Po štarte workera
python scripts/setup_schedules.py

# Verify
python scripts/setup_schedules.py --list
```

### 7.3 Manuálny trigger

```bash
# Cez Temporal UI
# http://localhost:8080 → Schedules → andros-marso-daily → Trigger

# Alebo CLI
python scripts/setup_schedules.py --trigger marso
```

---

## 8. Testovanie

### 8.1 Unit testy

```bash
cd apps/andros-invoice-worker
pytest tests/ -v

# Výsledok: 11/11 PASSED
```

### 8.2 Integration test (bez Temporal)

```python
import asyncio
from adapters.marso_adapter import MARSOAdapter
from config.config_loader import load_supplier_config
from datetime import date

async def test():
    config = load_supplier_config("marso")
    adapter = MARSOAdapter(config)

    # Test auth
    auth_ok = await adapter.authenticate()
    print(f"Auth: {auth_ok}")

    # Test fetch
    invoices = await adapter.fetch_invoice_list(
        date_from=date(2026, 1, 1),
        date_to=date(2026, 1, 27),
    )
    print(f"Invoices: {len(invoices)}")

asyncio.run(test())
```

---

## 9. Rozdiely od supplier-invoice-worker

| Aspekt | supplier-invoice-worker | andros-invoice-worker |
|--------|------------------------|----------------------|
| Účel | Generický worker | ANDROS-špecifický |
| PostgreSQL | invoices_pending (ISDOC) | supplier_invoice_heads/items (staging) |
| Multi-tenant | Nie | Áno (customer_code, supplier_code) |
| Scheduler | Polling scheduler | Temporal Schedule |
| Duplicate check | Nie | Áno (pred INSERT) |
| Status tracking | Nie | Áno (status field) |

---

## 10. Git Commits

| SHA | Popis |
|-----|-------|
| `35f0eee` | fix(andros): InvoiceStatus enum JSON serialization |
| `1de5c9a` | feat(andros): Add andros-invoice-worker for API suppliers |

---

## 11. TODO

- [ ] Rozšíriť na Continental API
- [ ] Rozšíriť na Goodyear API
- [ ] Product matching workflow
- [ ] NEX Genesis import activity
- [ ] Monitoring a alerting
- [ ] Systemd service na Ubuntu

---

## Súvisiace dokumenty

- `docs/knowledge/deployment/andros/marso-api-integration.md` - MARSO API detaily
- `apps/andros-invoice-worker/sql/create_tables.sql` - DB schema
- `apps/andros-invoice-worker/.env.example` - Environment template

---

*Vytvorené: 2026-01-27*
*Posledná aktualizácia: 2026-01-27*
