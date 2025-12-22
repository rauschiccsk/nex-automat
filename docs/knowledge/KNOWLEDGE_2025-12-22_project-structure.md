# NEX Automat - Project Structure & Architecture

**Dátum:** 2025-12-22
**Verzia:** v2.5
**Status:** Production (Mágerstav)

---

## 1. Adresárová štruktúra projektu

```
C:\Development\nex-automat\           <- Development
C:\Deployment\nex-automat\            <- Production (Mágerstav)

nex-automat/
├── apps/                             <- Aplikácie
│   ├── nex-brain/                    <- AI knowledge management (RAG)
│   ├── supplier-invoice-editor/      <- DEPRECATED: Stará GUI (PyQt5)
│   ├── supplier-invoice-loader/      <- FastAPI server pre príjem faktúr
│   ├── supplier-invoice-staging/     <- GUI aplikácia pre správu faktúr (PySide6)
│   └── supplier-invoice-worker/      <- Temporal worker (email polling)
│
├── packages/                         <- Zdieľané balíky
│   ├── nex-shared/                   <- PostgreSQL client, UI base classes
│   ├── nexdata/                      <- Btrieve wrapper pre NEX Genesis
│   └── shared-pyside6/               <- Zdieľané PySide6 komponenty
│
├── docs/                             <- Dokumentácia
│   └── knowledge/                    <- KNOWLEDGE_*.md súbory pre RAG
│
├── scripts/                          <- Utility a migračné skripty
├── tools/                            <- Externé nástroje (nssm, rag)
└── tests/                            <- Testy
```

---

## 2. Aplikácie (apps/)

### 2.1 supplier-invoice-loader

**Účel:** Príjem a spracovanie dodávateľských faktúr
**Typ:** FastAPI REST API server
**Port:** 8001
**Python:** 32-bit (kvôli Btrieve)

```
supplier-invoice-loader/
├── config/
│   ├── config_customer.py           <- Zákaznícka konfigurácia (HLAVNÝ CONFIG)
│   ├── config.yaml                  <- YAML konfigurácia
│   └── invoices.db                  <- SQLite databáza (legacy)
├── database/
│   ├── migrations/                  <- SQL migrácie (003_add_file_tracking_columns.sql)
│   └── schemas/                     <- DB schémy (001_initial_schema.sql)
├── src/
│   ├── api/models.py                <- Pydantic modely pre API
│   ├── business/
│   │   ├── isdoc_service.py         <- ISDOC XML generátor
│   │   └── product_matcher.py       <- NEX Genesis product matching
│   ├── database/database.py         <- SQLite operácie
│   ├── extractors/ls_extractor.py   <- PDF extrakcia (L&Š faktúry)
│   └── utils/
│       ├── config.py                <- Config wrapper
│       ├── monitoring.py            <- Metriky
│       └── notifications.py         <- Email notifikácie
├── main.py                          <- Entry point (FastAPI app)
└── requirements.txt
```

**Kľúčové endpointy:**
- `POST /invoice` - Príjem faktúry (PDF base64)
- `GET /health` - Health check
- `GET /metrics` - Prometheus metriky

### 2.2 supplier-invoice-staging

**Účel:** Zobrazenie, schválenie a import faktúr do NEX Genesis
**Typ:** PySide6 desktop aplikácia
**Python:** 64-bit

```
supplier-invoice-staging/
├── config/
│   ├── settings.py                  <- Settings trieda
│   └── config.yaml                  <- YAML konfigurácia
├── data/
│   └── settings.db                  <- SQLite pre window/grid nastavenia
├── database/
│   ├── repositories/
│   │   ├── __init__.py              <- Export InvoiceRepository
│   │   └── invoice_repository.py    <- DB operácie (get_invoice_heads, get_invoice_items)
│   └── schemas/
│       └── 001_supplier_invoice_staging.sql
├── services/
│   ├── __init__.py                  <- Export move_files_to_archive
│   └── file_mover.py                <- Presun súborov (staged → archive)
├── ui/
│   ├── dialogs/                     <- Dialógové okná
│   ├── main_window.py               <- Hlavné okno (zoznam faktúr)
│   └── invoice_items_window.py      <- Detail faktúry (položky)
├── app.py                           <- Entry point
├── __main__.py                      <- python -m support
└── requirements.txt
```

**Spustenie:**
```bash
cd apps/supplier-invoice-staging
python app.py
# alebo
python -m supplier-invoice-staging
```

### 2.3 supplier-invoice-worker

**Účel:** Email polling, orchestrácia workflow
**Typ:** Temporal worker
**Python:** 64-bit

```
supplier-invoice-worker/
├── activities/
│   ├── email_activities.py          <- fetch_emails, process_email
│   └── invoice_activities.py        <- send_to_loader
├── config/
│   ├── gmail_oauth.py               <- OAuth2 helper
│   ├── oauth_authorize.py           <- Autorizácia
│   └── settings.py                  <- Konfigurácia
├── scheduler/
│   └── polling_scheduler.py         <- Email polling (každých 5 min)
├── workers/
│   └── main_worker.py               <- Temporal worker
├── workflows/
│   └── invoice_workflow.py          <- InvoiceProcessingWorkflow
├── .env                             <- Konfigurácia (Temporal, IMAP)
└── .gmail_tokens.json               <- OAuth2 tokeny (NEZDIEĽAŤ!)
```

### 2.4 supplier-invoice-editor (DEPRECATED)

**Status:** ❌ DEPRECATED - nahradené supplier-invoice-staging
**Dôvod:** Stará PyQt5 aplikácia, nová je PySide6
**Poznámka:** Nepoužívať, ponechané len pre referenciu

### 2.5 nex-brain

**Účel:** AI-powered knowledge management
**Typ:** FastAPI + Ollama (llama3.1:8b) + Telegram bot
**Status:** Development

```
nex-brain/
├── api/
│   ├── routes/chat.py               <- Chat endpoint
│   ├── services/
│   │   ├── llm_service.py           <- Ollama integrácia
│   │   └── rag_service.py           <- RAG vyhľadávanie
│   └── main.py                      <- FastAPI app
├── cli/
│   └── chat_cli.py                  <- CLI chat interface
├── telegram/
│   └── bot.py                       <- Telegram bot
└── config/settings.py               <- Konfigurácia
```

---

## 3. Zdieľané balíky (packages/)

### 3.1 nex-shared

**Účel:** PostgreSQL klient, UI base classes, utilities

**KRITICKÉ:** Flat štruktúra (bez vnoreného nex_shared/)!

```
packages/nex-shared/
├── database/
│   ├── __init__.py                  <- Export PostgresStagingClient
│   ├── postgres_staging.py          <- PostgresStagingClient trieda
│   └── window_settings_db.py        <- Window settings DB
├── ui/
│   ├── __init__.py
│   ├── base_grid.py                 <- BaseGrid (11.9K)
│   ├── base_window.py               <- BaseWindow
│   └── window_persistence.py        <- Window state persistence
├── utils/
│   ├── __init__.py
│   ├── grid_settings.py             <- Grid settings helper
│   └── text_utils.py                <- clean_string()
├── __init__.py
└── setup.py                         <- pip install -e .
```

**Import:**
```python
from nex_shared.database import PostgresStagingClient
from nex_shared.utils import clean_string
```

### 3.2 nexdata

**Účel:** Btrieve wrapper pre NEX Genesis
**Python:** Vyžaduje 32-bit (w3btrv7.dll)

```
packages/nexdata/
├── nexdata/                         <- Vnorený package
│   ├── btrieve/
│   │   └── btrieve_client.py        <- Btrieve operácie
│   ├── models/
│   │   ├── barcode.py               <- Barcode model
│   │   ├── gscat.py                 <- GSCAT (produkty)
│   │   ├── mglst.py                 <- MGLST
│   │   ├── pab.py                   <- PAB (partneri)
│   │   ├── tsh.py                   <- TSH (transakcie head)
│   │   └── tsi.py                   <- TSI (transakcie items)
│   └── repositories/
│       ├── base_repository.py       <- Základný repozitár
│       ├── barcode_repository.py
│       ├── gscat_repository.py
│       └── pab_repository.py
└── pyproject.toml
```

**Import:**
```python
from nexdata.btrieve import BtrieveClient
from nexdata.models import GSCAT, PAB
from nexdata.repositories import GscatRepository
```

### 3.3 shared-pyside6

**Účel:** Zdieľané PySide6 komponenty pre GUI aplikácie

```
packages/shared-pyside6/
├── shared_pyside6/                  <- Vnorený package
│   ├── database/
│   │   └── settings_repository.py   <- Settings DB operácie
│   ├── ui/
│   │   ├── base_grid.py             <- BaseGrid (27K - plná verzia)
│   │   ├── base_window.py           <- BaseWindow
│   │   └── quick_search.py          <- QuickSearch komponenty
│   └── utils/
│       └── text_utils.py
├── tests/                           <- Pytest testy
└── pyproject.toml
```

**Import:**
```python
from shared_pyside6.ui import BaseWindow, BaseGrid
from shared_pyside6.ui.quick_search import QuickSearchContainer
```

---

## 4. Databázy

### 4.1 PostgreSQL databázy

| Databáza | Účel | Status |
|----------|------|--------|
| `supplier_invoice_staging` | Hlavná DB pre faktúry | ✅ AKTÍVNA |
| `invoice_staging` | Stará DB | ❌ DEPRECATED |
| `temporal` | Temporal persistence | ✅ AKTÍVNA |
| `temporal_visibility` | Temporal visibility | ✅ AKTÍVNA |
| `nex_automat_rag` | RAG vektorová DB | ✅ AKTÍVNA |
| `ai_dev_automation` | AI development | Development |

### 4.2 supplier_invoice_staging - Tabuľky

| Tabuľka | Účel |
|---------|------|
| `supplier_invoice_heads` | Hlavičky faktúr |
| `supplier_invoice_items` | Položky faktúr |
| `invoices` | Legacy tabuľka (nepoužívať) |

### 4.3 supplier_invoice_heads - Kľúčové stĺpce

**XML dáta (z faktúry):**
- `xml_invoice_number`, `xml_variable_symbol`
- `xml_issue_date`, `xml_tax_point_date`, `xml_due_date`
- `xml_supplier_ico`, `xml_supplier_name`, `xml_supplier_dic`
- `xml_total_without_vat`, `xml_total_vat`, `xml_total_with_vat`
- `xml_currency`, `xml_iban`, `xml_swift`

**NEX Genesis dáta:**
- `nex_supplier_id`, `nex_supplier_modify_id`
- `nex_stock_id`, `nex_book_num`
- `nex_document_id` - ID dokladu v NEX
- `nex_invoice_doc_id` - Číslo DF (napr. DF2500100123)
- `nex_delivery_doc_id` - Číslo DD (napr. DD2500100205)

**File tracking:**
- `file_basename` - Názov súboru bez ext (napr. `20251222_125701_32506183`)
- `file_status` - Stav: `received`, `staged`, `archived`
- `pdf_file_path`, `xml_file_path` - Aktuálne cesty k súborom

**Status:**
- `status` - pending/approved/imported/rejected
- `validation_status`, `validation_errors`
- `item_count`, `items_matched`, `match_percent`

---

## 5. Súborový systém faktúr

### 5.1 Životný cyklus súborov

```
Fáza 1: RECEIVED (nové faktúry)
  C:\NEX\IMPORT\SUPPLIER-INVOICES\
    └── {timestamp}_{invoice_number}.pdf
    └── {timestamp}_{invoice_number}.xml

Fáza 2: STAGED (v PostgreSQL, čaká na NEX import)
  C:\NEX\IMPORT\SUPPLIER-STAGING\
    └── {timestamp}_{invoice_number}.pdf
    └── {timestamp}_{invoice_number}.xml

Fáza 3: ARCHIVED (importované do NEX Genesis)
  C:\NEX\YEARACT\ARCHIV\SUPPLIER-INVOICES\
    ├── PDF\{DF_number}-{DD_number}.pdf
    └── XML\{DF_number}-{DD_number}.xml
```

### 5.2 Príklad pomenovania

```
Received/Staged: 20251222_125701_32506183.pdf
Archived:        DF2500100123-DD2500100205.pdf
                 DF2500100123.pdf  (ak nie je DD)
```

### 5.3 Legacy cesty (NEPOUŽÍVAŤ)

```
C:\NEX\IMPORT\LS\PDF\   <- Stará štruktúra z n8n
C:\NEX\IMPORT\LS\XML\   <- Stará štruktúra z n8n
```

---

## 6. Windows Services (Mágerstav)

| Service | Účel | Port |
|---------|------|------|
| `NEX-Temporal-Server` | Temporal server | 7233 (gRPC), 8233 (UI) |
| `NEX-Invoice-Worker` | Temporal worker | - |
| `NEX-Polling-Scheduler` | Email polling (5 min) | - |
| `NEX-Automat-Loader` | FastAPI server | 8001 |
| `CloudflaredMagerstav` | Cloudflare tunnel | - |

**Správa služieb:**
```powershell
Get-Service "NEX-*"
Start-Service NEX-Automat-Loader
Stop-Service NEX-Invoice-Worker
```

---

## 7. Konfigurácia

### 7.1 Environment variables

```bash
POSTGRES_PASSWORD=<heslo>        # PostgreSQL
LS_API_KEY=<api_key>             # Loader API key
SMTP_USER=<email>                # Email notifikácie
SMTP_PASSWORD=<app_password>     # Gmail app password
```

### 7.2 Kľúčové config súbory

| Súbor | Účel |
|-------|------|
| `apps/supplier-invoice-loader/config/config_customer.py` | Loader - cesty, DB, NEX |
| `apps/supplier-invoice-worker/.env` | Worker - Temporal, IMAP |
| `apps/supplier-invoice-staging/config/settings.py` | Staging GUI |
| `apps/supplier-invoice-staging/config/config.yaml` | Staging GUI YAML |

---

## 8. Workflow - Spracovanie faktúry (E2E)

```
1. Email s PDF → Gmail (magerstavinvoice@gmail.com)
          ↓
2. NEX-Polling-Scheduler (každých 5 min)
          ↓
3. NEX-Invoice-Worker (Temporal)
   - fetch_emails → process_email → send_to_loader
          ↓
4. POST /invoice → NEX-Automat-Loader (FastAPI)
   - Extrakcia dát z PDF
   - Generovanie ISDOC XML
   - Uloženie do PostgreSQL (file_status='received')
   - Presun do STAGING (file_status='staged')
          ↓
5. supplier-invoice-staging (GUI)
   - Zobrazenie faktúry
   - Schválenie položiek
   - [TODO] Import do NEX Genesis
          ↓
6. [TODO] Po importe: Presun do ARCHIVE (file_status='archived')
```

---

## 9. Development Workflow

```
Development (C:\Development\nex-automat)
         ↓ git commit & push
GitHub (rauschiccsk/nex-automat)
         ↓ git pull (na Mágerstav serveri)
Deployment (C:\Deployment\nex-automat)
```

**KRITICKÉ:** Nikdy neopravovať priamo v Deployment!

---

## 10. Dôležité príkazy

### RAG update
```bash
python tools/rag/rag_update.py --new    # Dnes zmenené
python tools/rag/rag_update.py --all    # Všetko
python tools/rag/rag_update.py --stats  # Štatistiky
```

### Spustenie aplikácií
```bash
# Loader (32-bit Python)
cd apps/supplier-invoice-loader
python main.py

# Staging GUI (64-bit Python)
cd apps/supplier-invoice-staging
python app.py

# Worker (64-bit Python)
cd apps/supplier-invoice-worker
python -m workers.main_worker
```

---

## 11. Verzie a história

| Verzia | Dátum | Zmeny |
|--------|-------|-------|
| v2.0 | 2025-11-27 | GO-LIVE Mágerstav |
| v2.1 | 2025-12-02 | Duplicate detection fix |
| v2.2 | 2025-12-06 | BaseGrid cleanup |
| v2.3 | 2025-12-08 | invoice-shared → nex-shared migrácia |
| v2.4 | 2025-12-09 | NEX Genesis product enrichment |
| v2.5 | 2025-12-22 | Temporal production, File organization |