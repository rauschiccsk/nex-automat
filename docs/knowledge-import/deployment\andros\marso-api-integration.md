# MARSO API Integration - Complete Guide

**Status:** PRODUCTION READY
**Prostredia:** Dev PC (Windows), ANDROS Server (Ubuntu/Windows)
**Posledná aktualizácia:** 2026-01-27

---

## 1. Prehľad

### 1.1 Cieľ
Automatizovaný import dodávateľských faktúr z MARSO Hungary Kft. cez SOAP API do NEX Automat systému.

### 1.2 Workflow
```
MARSO SOAP API → JSON → ISDOC XML → FastAPI Pipeline → PostgreSQL → NEX Genesis
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
│ supplier-invoice-worker (Temporal Workflow)                      │
│   ├── MARSOAdapter - SOAP client (zeep)                         │
│   ├── MARSOToISDOCConverter - JSON → ISDOC XML                  │
│   └── Activities: fetch, convert, archive, post                 │
└──────────────────────┬──────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│ Archive & Storage                                               │
│   ├── JSON: /SUPPLIER-INVOICES/MARSO/YYYY/MM/*.json (raw)       │
│   └── XML:  /SUPPLIER-INVOICES/MARSO/YYYY/MM/*.xml  (ISDOC)     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Infraštruktúra

### 2.1 ANDROS Environment

| Component | Location | Details |
|-----------|----------|---------|
| Windows VM | 192.168.100.10 | NEX Genesis, Invoice Loader service |
| Ubuntu Docker Host | 192.168.100.23 | PostgreSQL, Temporal |
| Git Repo | C:\ANDROS\nex-automat | Branch: develop |

### 2.2 Port Mapping

| Service | ANDROS | ICC | Notes |
|---------|--------|-----|-------|
| PostgreSQL | 5432 | 5433 | Different containers |
| Temporal | 7233 | 7234 | Different containers |
| Temporal UI | 8080 | 8082 | Web interface |
| Invoice Loader API | 8001 | 8002 | FastAPI |

### 2.3 Cesty na ANDROS

| Typ | Cesta |
|-----|-------|
| Source code (Ubuntu) | `/opt/nex-automat-src/` |
| Source code (Windows) | `C:\ANDROS\nex-automat\` |
| Archive (Ubuntu) | `/opt/nex-automat/data/supplier-invoices/` |
| Archive (Windows) | `C:\NEX\YEARACT\ARCHIV\SUPPLIER-INVOICES\` |

---

## 3. API Credentials

### 3.1 MARSO SOAP API

| Parameter | Hodnota | Zdroj |
|-----------|---------|-------|
| WSDL LIVE | `http://195.228.175.10:8081/ComaxWS/Comax.asmx?wsdl` | DeliveryOrders_Marso.pas |
| WSDL TEST | `http://195.228.175.10:8082/ComaxWS/Comax.asmx?wsdl` | - |
| Method | `CallComax` | - |
| AccountNum | `339792` | MarsoConverter.pas |
| API Key | `feixRjG254zft3zqnxx4kACZHEyX01` | MarsoConverter.pas:63 |
| Sender | `WebCatHU` | - |
| Receiver | `Ax` | - |

### 3.2 Environment Variables (.env)

```bash
# MARSO Supplier API
MARSO_API_KEY=feixRjG254zft3zqnxx4kACZHEyX01
MARSO_ACCOUNT_NUM=339792
MARSO_USE_TEST=false

# Archive path (Linux)
ARCHIVE_PATH=/opt/nex-automat/data/supplier-invoices

# Archive path (Windows)
# ARCHIVE_PATH=C:\NEX\YEARACT\ARCHIV\SUPPLIER-INVOICES
```

---

## 4. SOAP MessageTypes & Formáty

### 4.1 MessageTypes

| MessageType | Účel | Response |
|-------------|------|----------|
| `CustInvoiceList` | Zoznam faktúr s riadkami | JSON array |
| `CustInvoices` | Len hlavičky faktúr | JSON array |
| `CustInvoiceLines` | Detaily riadkov faktúry | JSON array |
| `ItemQty` | Dopyt na dostupnosť (objednávky) | JSON |
| `CreateSalesOrder` | Vytvorenie objednávky | JSON |

### 4.2 Request XML (CustInvoiceList)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Document>
  <ComaxEnvelope>
    <Sender>WebCatHU</Sender>
    <Receiver>Ax</Receiver>
    <MessageType>CustInvoiceList</MessageType>
    <MessageId/>
    <RespMessageId/>
    <test>0</test>
  </ComaxEnvelope>
  <Message>
    <AccountNum>339792</AccountNum>
    <DatumTol>2026-01-01</DatumTol>
    <DatumIg>2026-01-31</DatumIg>
    <SzlSzamResz></SzlSzamResz>
    <Key>feixRjG254zft3zqnxx4kACZHEyX01</Key>
  </Message>
</Document>
```

### 4.3 Response (XML s embedded JSON)

```xml
<Document>
  <Message>
    <Status>1</Status>
    <Invoices>[{"11926-00447": {"InvoiceId": "11926-00447", ...}}]</Invoices>
  </Message>
</Document>
```

### 4.4 Invoice JSON štruktúra

```json
{
  "InvoiceId": "11926-00447",
  "SalesId": "VR3760770",
  "Kelt": "2026.01.21",
  "Teljesites": "2026.01.21",
  "Hatarido": "2026.01.22",
  "InvName": "Andros s.r.o.",
  "InvCity": "Bratislava",
  "InvStreet": "Tallerova 4.",
  "InvZipCode": "81102",
  "InvCountryRegionId": "SK",
  "Netto": "5488.06",
  "Afa": "1097.61",
  "Brutto": "6585.67",
  "Penznem": "EUR",
  "Lines": [...]
}
```

---

## 5. Mapovanie polí

### 5.1 Hlavička faktúry (MARSO → ISDOC)

| MARSO | ISDOC | Popis |
|-------|-------|-------|
| InvoiceId | ID | Číslo faktúry |
| Kelt | IssueDate | Dátum vystavenia |
| Teljesites | TaxPointDate | Dátum plnenia |
| Hatarido | PaymentDueDate | Dátum splatnosti |
| Penznem | LocalCurrencyCode | Mena |
| Netto | TaxExclusiveAmount | Suma bez DPH |
| Afa | TaxAmount | DPH |
| Brutto | TaxInclusiveAmount | Suma s DPH |

### 5.2 Riadky faktúry

| MARSO | ISDOC | Popis |
|-------|-------|-------|
| ItemId | SellersItemIdentification/ID | EAN/SKU |
| ItemName | Description | Názov produktu |
| Qty | InvoicedQuantity | Množstvo |
| SalesUnit | @unitCode | Jednotka |
| Netto | LineExtensionAmount | Cena bez DPH |

### 5.3 Jednotky (MARSO → UN/ECE)

| MARSO | UN/ECE | Popis |
|-------|--------|-------|
| Db | PCE | Kus |
| Pr | PR | Pár |
| Kg | KGM | Kilogram |
| M | MTR | Meter |

---

## 6. Implementácia

### 6.1 Aplikácie

**Existujú dve aplikácie pre MARSO:**

| Aplikácia | Účel | PostgreSQL |
|-----------|------|------------|
| `apps/supplier-invoice-worker/` | Generický worker (ISDOC) | invoices_pending |
| `apps/andros-invoice-worker/` | ★ ANDROS staging | supplier_invoice_heads/items |

**Odporúčané:** Použiť `andros-invoice-worker` pre ANDROS s.r.o.

### 6.2 Súborová štruktúra (andros-invoice-worker)

```
apps/andros-invoice-worker/
├── adapters/
│   ├── base_adapter.py           # Abstraktná trieda
│   └── marso_adapter.py          # MARSO SOAP adapter ★
├── activities/
│   ├── supplier_api_activities.py # API activities
│   └── postgres_activities.py     # ★ PostgreSQL staging
├── converters/
│   └── marso_to_isdoc.py         # JSON → ISDOC XML
├── config/
│   ├── settings.py               # Pydantic settings
│   └── suppliers/marso.yaml      # MARSO konfigurácia
├── scheduler/
│   └── schedule_manager.py       # ★ Temporal Schedule
├── scripts/
│   └── setup_schedules.py        # Schedule CLI
├── sql/
│   └── create_tables.sql         # ★ PostgreSQL schema
├── workflows/
│   └── api_invoice_workflow.py   # ANDROSInvoiceWorkflow ★
├── workers/
│   └── main_worker.py            # Temporal worker
├── tests/
│   └── test_marso_adapter.py     # 11 testov
├── .env                          # Credentials (nie v git)
└── requirements.txt              # zeep, temporalio, asyncpg
```

### 6.2 Kľúčové triedy

**MARSOAdapter** (`adapters/marso_adapter.py`):
- `authenticate()` - SOAP autentifikácia
- `fetch_invoice_list(date_from, date_to)` - CustInvoiceList
- `fetch_invoice_by_id(invoice_id)` - CustInvoiceLines
- `_parse_response()` - XML → JSON extraction
- `_parse_marso_date()` - "YYYY.MM.DD" format handling
- `to_unified_invoice()` - JSON → UnifiedInvoice

**MARSOToISDOCConverter** (`converters/marso_to_isdoc.py`):
- `convert(raw_invoice)` - MARSO JSON → ISDOC XML
- `validate(xml)` - Basic XML validation

### 6.3 Opravené problémy

| Problém | Riešenie |
|---------|----------|
| XML response s embedded JSON | Regex extraction z `<Invoices>` elementu |
| Nested JSON `[{id: {data}}]` | Flatten v `_parse_response()` |
| Dátum "YYYY.MM.DD" | Multi-format parser |
| Windows cesta na Linux | Environment variable `ARCHIVE_PATH` |

---

## 7. PostgreSQL Schema

### 7.1 Tabuľky

**invoices_pending** (41 stĺpcov):
```sql
-- XML data from ISDOC
xml_invoice_number, xml_variable_symbol, xml_issue_date, xml_due_date,
xml_supplier_ico, xml_supplier_name, xml_supplier_dic, xml_supplier_ic_dph,
xml_total_without_vat, xml_total_vat, xml_total_with_vat, xml_currency,
xml_iban, xml_swift, xml_tax_point_date

-- NEX Genesis references
nex_supplier_id, nex_supplier_modify_id, nex_stock_id, nex_book_num,
nex_payment_method_id, nex_price_list_id, nex_document_id,
nex_invoice_doc_id, nex_delivery_doc_id, nex_iban, nex_swift

-- Workflow
status, file_status, pdf_file_path, xml_file_path, file_basename,
item_count, items_matched, match_percent, validation_status, validation_errors,
created_at, updated_at, processed_at, imported_at
```

**invoice_items_pending** (24 stĺpcov):
```sql
-- XML data
xml_line_number, xml_seller_code, xml_ean, xml_product_name,
xml_quantity, xml_unit, xml_unit_price, xml_unit_price_vat,
xml_total_price, xml_total_price_vat, xml_vat_rate

-- NEX Genesis references
nex_product_id, nex_product_name, nex_ean, nex_stock_code, nex_stock_id

-- Matching
matched, matched_by, match_confidence, edited_unit_price, validation_status,
created_at, updated_at
```

### 7.2 DateStyle Fix

```sql
-- PostgreSQL DateStyle pre slovenské dátumy
SET DateStyle = 'ISO, DMY';
```

Docker Compose:
```yaml
command: postgres -c datestyle='ISO,DMY'
```

---

## 8. Testovanie

### 8.1 Unit testy

```bash
cd apps/supplier-invoice-worker
pytest tests/test_marso_adapter.py tests/test_marso_converter.py -v
# Výsledok: 38/38 PASSED
```

### 8.2 Integration test

```bash
# Direct API test (bez Temporal)
python -c "
from adapters.marso_adapter import MARSOAdapter
# ... test connection and fetch invoices
"
# Výsledok: 1 faktúra, 53 položiek, ISDOC 41KB
```

### 8.3 Temporal workflow test

```bash
# Na ANDROS serveri
python -m scheduler.polling_scheduler --once
```

---

## 9. Deployment & Operations

### 9.1 Git pull a restart

**Windows (ANDROS VM):**
```powershell
cd C:\ANDROS\nex-automat
git pull origin develop
Restart-Service -Name "NEX-*-ANDROS"
```

**Ubuntu:**
```bash
cd /opt/nex-automat-src
git pull origin develop
# Restart worker ak beží
```

### 9.2 Spustenie workera

**Windows:**
```powershell
cd C:\ANDROS\nex-automat\apps\supplier-invoice-worker
.\venv\Scripts\activate
python -m workers.main_worker
```

**Linux:**
```bash
cd /opt/nex-automat-src/apps/supplier-invoice-worker
source venv/bin/activate
MARSO_API_KEY="..." ARCHIVE_PATH="..." python3 -m workers.main_worker
```

### 9.3 Windows Services (NSSM)

```powershell
# Status
Get-Service NEX-*-ANDROS

# Restart
Get-Service NEX-*-ANDROS | Restart-Service
```

---

## 10. Troubleshooting

### 10.1 Windows (ANDROS VM)

```powershell
# Check service status
Get-Service -Name "NEX-Automat-Loader-ANDROS"

# View logs
Get-Content C:\ANDROS\nex-automat\logs\*.log -Tail 100

# Test API
Invoke-WebRequest -Uri "http://localhost:8001/health" -Method GET
```

### 10.2 Ubuntu Docker Host

```bash
# PostgreSQL
docker exec -it nex-postgres psql -U nex_admin -d nex_automat

# Check tables
docker exec -it nex-postgres psql -U nex_admin -d nex_automat -c "\dt"

# Check invoices
docker exec -it nex-postgres psql -U nex_admin -d nex_automat \
  -c "SELECT id, xml_invoice_number, status FROM invoices_pending LIMIT 10;"

# Temporal logs
docker logs nex-temporal --tail 100

# Container status
docker ps --filter "name=nex-"
```

### 10.3 MARSO API test

```bash
# Quick API test
curl -s "http://195.228.175.10:8081/ComaxWS/Comax.asmx?wsdl" | head -20
```

---

## 11. Kontakty & História

### 11.1 MARSO Kontakty

| Osoba | Email | Téma |
|-------|-------|------|
| Imre Belinszki | imre@marso.hu | API parametre |
| Tamás Nagy | nagy.tamas@marso.hu | Technické problémy |

### 11.2 Git Commits

| SHA | Popis |
|-----|-------|
| `6943fa4` | fix imports and add ARCHIVE_PATH for Linux |
| `03b1826` | fix XML/JSON response parsing and date format |
| `17bd07b` | load API credentials from environment variables |
| `3aedbbc` | add MARSO API configuration to env examples |
| `90bb0cf` | implement complete API invoice workflow |

---

## 12. TODO

- [x] ~~Nastaviť scheduler~~ → Temporal Schedule (andros-invoice-worker)
- [x] ~~Konfigurovať CRON~~ → `0 6 * * *` v schedule_manager.py
- [ ] Spustiť invoice pipeline API na ANDROS
- [ ] Monitoring a alerting
- [ ] Rozšíriť na ďalších dodávateľov (CONTINENTAL, GOODYEAR)
- [ ] Product matching workflow

---

## Súvisiace dokumenty

- `docs/knowledge/deployment/andros/andros-invoice-worker.md` - ★ ANDROS Invoice Worker Guide
- `docs/knowledge/MARSO_DELPHI_EXTRACTION.md` - Extrakcia z Delphi kódu
- `docs/knowledge/deployment/DEPLOYMENT_GUIDE_ANDROS.md` - Všeobecný deployment guide
- `apps/andros-invoice-worker/sql/create_tables.sql` - PostgreSQL schema
- `apps/andros-invoice-worker/.env.example` - Environment template

---

*Vytvorené: 2026-01-20*
*Posledná aktualizácia: 2026-01-27*
