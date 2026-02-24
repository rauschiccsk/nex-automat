# KNOWLEDGE: andros-invoice-worker Implementation

**Dátum:** 2026-01-27  
**Projekt:** NEX Automat  
**Zákazník:** ANDROS s.r.o.  
**Stav:** Deployed, E2E test pending

---

## 1. PREHĽAD

Vytvorený nový worker `andros-invoice-worker` pre spracovanie API faktúr od dodávateľov (MARSO, budúci CONTINENTAL, GOODYEAR). Oddelený od `supplier-invoice-worker` (MÁGERSTAV - email workflow) pre elimináciu rizika regresie.

---

## 2. ARCHITEKTÚRA

```
LINUX (Ubuntu 24.04)                        WINDOWS VM (Server 2025)
┌─────────────────────────────┐             ┌─────────────────────────────┐
│ andros-invoice-worker       │             │ supplier-invoice-staging-web│
│ ├── MARSO API (SOAP)        │             │ ├── React frontend          │
│ ├── JSON → ISDOC XML        │             │ ├── Product Matching        │
│ └── Uloženie do PostgreSQL  │             │ └── Import do Btrieve       │
│                             │             │                             │
│ PostgreSQL (Docker :5432)   │◄───────────►│ NEX Genesis (Btrieve)       │
│ Temporal (Docker :7233)     │             │                             │
└─────────────────────────────┘             └─────────────────────────────┘
```

**Kľúčové rozhodnutie:** Product Matching až pri schvaľovaní vo Web UI na Windows (Variant A), nie pri príjme faktúry.

---

## 3. ŠTRUKTÚRA APLIKÁCIE

```
apps/andros-invoice-worker/
├── adapters/
│   ├── base_adapter.py
│   └── marso_adapter.py
├── activities/
│   ├── supplier_api_activities.py
│   └── postgres_activities.py      # INSERT do DB
├── workflows/
│   └── api_invoice_workflow.py     # ANDROSInvoiceWorkflow
├── converters/
│   └── marso_to_isdoc.py
├── scheduler/
│   └── schedule_manager.py         # Temporal Schedule
├── scripts/
│   └── setup_schedules.py          # CLI pre schedules
├── workers/
│   └── main_worker.py
├── models/
│   └── unified_invoice.py
├── sql/
│   └── create_tables.sql
├── config/
│   └── suppliers/marso.yaml
├── .env
└── requirements.txt
```

---

## 4. DEPLOYMENT NA ANDROS

### Systemd Service
```
/etc/systemd/system/andros-invoice-worker.service
```
- User: andros
- WorkingDirectory: /opt/nex-automat-src/apps/andros-invoice-worker
- EnvironmentFile: .env.systemd
- ExecStart: /opt/nex-automat/venv/bin/python -m workers.main_worker

### Temporal Schedule
- Schedule ID: `andros-marso-daily`
- Čas: 06:00 UTC denne
- Task Queue: `andros-invoice-queue`

### Príkazy
```bash
# Status
sudo systemctl status andros-invoice-worker

# Logy
sudo journalctl -u andros-invoice-worker -f

# Manuálny trigger
cd /opt/nex-automat-src/apps/andros-invoice-worker
source /opt/nex-automat/venv/bin/activate
python scripts/setup_schedules.py --trigger marso

# List schedules
python scripts/setup_schedules.py --list
```

---

## 5. POSTGRESQL TABUĽKY

### supplier_invoice_heads
- customer_code (ANDROS)
- supplier_code (MARSO)
- invoice_number, invoice_date, due_date
- total_without_vat, total_vat, total_with_vat
- status (pending, processed, failed)
- UNIQUE (customer_code, supplier_code, invoice_number)

### supplier_invoice_items
- head_id (FK)
- product_code, product_name, ean
- quantity, unit_price, total_price, vat_rate
- nex_product_id, nex_product_code, match_confidence

---

## 6. ENVIRONMENT (.env)

```bash
TEMPORAL_HOST=localhost
TEMPORAL_PORT=7233
TEMPORAL_TASK_QUEUE=andros-invoice-queue

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=nex_automat
POSTGRES_USER=nex_admin
POSTGRES_PASSWORD=Nex1968

MARSO_API_KEY=feixRjG254zft3zqnxx4kACZHEyX01
MARSO_ACCOUNT_NUM=339792

ARCHIVE_PATH=/opt/nex-automat/data/supplier-invoices
CUSTOMER_CODE=ANDROS
```

---

## 7. OPRAVENÉ CHYBY

### InvoiceStatus JSON serialization (commit 35f0eee)
```python
# Pred
class InvoiceStatus(Enum):

# Po
class InvoiceStatus(str, Enum):
```

---

## 8. GIT COMMITY

| SHA | Popis |
|-----|-------|
| 1de5c9a | feat(andros): Add andros-invoice-worker for API suppliers |
| 35f0eee | fix(andros): InvoiceStatus enum JSON serialization |

---

## 9. REGISTERED WORKFLOWS & ACTIVITIES

**Workflows:**
- ANDROSInvoiceWorkflow
- SingleInvoiceWorkflow

**Activities:**
- fetch_supplier_config_activity
- authenticate_supplier_activity
- fetch_invoice_list_activity
- check_invoice_exists_activity
- fetch_invoice_detail_activity
- convert_to_unified_activity
- convert_to_isdoc_activity
- save_invoice_to_postgres_activity
- archive_raw_data_activity
- update_invoice_status_activity

---

## 10. CLAUDE CODE - MAX SUBSCRIPTION

**Problém:** Claude Code používal API kredity namiesto MAX subscription kvôli nastavenej premennej ANTHROPIC_API_KEY.

**Riešenie:**
```bash
# Odstrániť API key
unset ANTHROPIC_API_KEY
# Windows: Remove-Item Env:ANTHROPIC_API_KEY

# Logout a login
claude logout
claude login
# alebo v Claude Code: /logout, /login
```

**Overenie:** `/status` → Login method: Claude Max Account

---

## 11. BUDÚCE ROZŠÍRENIA

- Continental adapter (SFTP)
- Goodyear adapter (TBD)
- Web UI integrácia na Windows VM