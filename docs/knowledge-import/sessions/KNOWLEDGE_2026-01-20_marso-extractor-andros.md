# MARSO Extractor Implementation for ANDROS

**Dátum:** 2026-01-20
**Status:** ✅ Implementované, ⚠️ Testovanie prerušené

---

## Dokončené úlohy

### 1. MARSO Invoice Extractor
Vytvorený nový extraktor pre maďarské MARSO faktúry (dodávateľ pneumatík pre ANDROS).

**Súbor:** `apps/supplier-invoice-loader/src/extractors/marso_extractor.py`

**Špecifiká oproti L&Š:**
- Maďarská faktúra - bilingválne HU/EN
- Dátum: YYYY.MM.DD → konvertuje na DD.MM.YYYY
- Číslo faktúry: 11925-10338 (s pomlčkou)
- DPH: 0% (EU intra-community)
- EU VAT: HU10428342 / SK2120582200
- Tax number: 10428342-2-15
- Položky: customs_code (4011100000), popis pneumatiky, Pcs jednotka
- Desatinné čísla: maďarský formát (2 647,40 → 2647.40)

**Hlavné triedy:**
- `MarsoInvoiceItem` - položka faktúry
- `MarsoInvoiceData` - hlavička faktúry
- `MarsoInvoiceExtractor` - extraktor s pdfplumber

**Funkcie:**
- `detect_marso_invoice_from_pdf()` - detekcia MARSO faktúr
- `extract_marso_invoice()` - extrakcia dát
- `extract_marso_as_standard()` - konverzia na štandardný InvoiceData

### 2. Integrácia do Pipeline
Pridaná auto-detekcia a routing v `main.py`:

```python
if detect_marso_invoice_from_pdf(str(pdf_path)):
    print("[INFO] Detected MARSO invoice - using MARSO extractor")
    invoice_data = extract_marso_as_standard(str(pdf_path))
else:
    print("[INFO] Using L&Š extractor (default)")
    invoice_data = extract_invoice_data(str(pdf_path))
```

### 3. Config Template Opravy
Pridané chýbajúce premenné do `config_template.py`:
- `STAGING_DIR`
- `NEX_DATA_PATH`

### 4. Unicode Emoji Oprava
Nahradené unicode emoji v `main.py` za ASCII text pre Windows cp1250 kompatibilitu:
- 🔍 → [ENRICH]
- ✅ → [OK]
- ⚠ → [WARNING]
- ❌ → [ERROR]
- 📊 → [STATS]

### 5. ANDROS Windows VM Setup
Vytvorený `config_customer.py` pre ANDROS:

```python
CUSTOMER_NAME = "ANDROS"
CUSTOMER_FULL_NAME = "Andros s.r.o."
API_KEY = "ls-dev-key-change-in-production-2025"
NEX_GENESIS_ENABLED = False

# Paths
PDF_DIR = Path(r"C:\ANDROS\NEX\IMPORT\SUPPLIER-INVOICES")
XML_DIR = Path(r"C:\ANDROS\NEX\IMPORT\SUPPLIER-INVOICES")
STAGING_DIR = Path(r"C:\ANDROS\NEX\IMPORT\SUPPLIER-STAGING")
NEX_DATA_PATH = Path(r"C:\ANDROS\NEX\DATA")
DB_FILE = Path(r"C:\ANDROS\nex-automat\apps\supplier-invoice-loader\config\invoices.db")

# PostgreSQL
POSTGRES_STAGING_ENABLED = True
POSTGRES_HOST = "192.168.122.1"
POSTGRES_PORT = 5432
POSTGRES_DATABASE = "nex_automat"
POSTGRES_USER = "nex_admin"
POSTGRES_PASSWORD = "Nex1968"
```

---

## Test Results

### Lokálny test (Development)
- ✅ MARSO detekcia funguje
- ✅ Extrakcia: 69/80 položiek (niektoré cez viac strán)
- ✅ Invoice: 11925-10338
- ✅ Total: 26295.71 EUR
- ✅ ISDOC XML generovanie: 55KB

### End-to-end test (ANDROS)
- ✅ Email polling funguje (mail.webglobe.sk)
- ✅ 2 MARSO faktúry detekované
- ✅ POST /invoice vrátil 200 OK
- ⚠️ Súbory nie sú v adresároch (spracované pred opravou config)
- ⏳ PostgreSQL overenie pending

---

## Git Commits

1. `3231d34` - feat: MARSO invoice extractor for ANDROS
2. `be5cfd2` - fix: add missing STAGING_DIR and NEX_DATA_PATH to config template
3. `f00835d` - fix: replace unicode emoji with ASCII text for Windows cp1250 compatibility

---

## Architektúra - Supplier Detection

```
PDF príde → detect_marso_invoice_from_pdf()
              ↓
        Je MARSO? 
           ↓
    ┌──────┴──────┐
   Áno           Nie
    ↓             ↓
 MARSO        L&Š extractor
 extractor        ↓
    ↓             ↓
    └─────┬───────┘
          ↓
   InvoiceData (štandardný)
          ↓
   ISDOC XML generátor
          ↓
   PostgreSQL + súbory
```

Extraktory sú v jednom repo, auto-detekcia podľa obsahu PDF - nie podľa zákazníka.

---

## Pending / Next Steps

1. **Overiť PostgreSQL** - či faktúry boli uložené do DB
2. **Nový E2E test** - poslať novú MARSO faktúru po oprave config
3. **Skontrolovať súbory** - či sa ukladajú do správnych adresárov
4. **ICC Deployment** - podľa pôvodného INIT promptu (zatiaľ odložené)

---

## Dôležité súbory

| Súbor | Účel |
|-------|------|
| `apps/supplier-invoice-loader/src/extractors/marso_extractor.py` | MARSO extraktor |
| `apps/supplier-invoice-loader/src/extractors/ls_extractor.py` | L&Š extraktor |
| `apps/supplier-invoice-loader/main.py` | FastAPI + routing |
| `apps/supplier-invoice-loader/config/config_template.py` | Config template |
| `C:\ANDROS\...\config\config_customer.py` | ANDROS config (nie v Git) |

---

## Windows Services (ANDROS)

| Service | Status |
|---------|--------|
| NEX-Automat-Loader-ANDROS | ✅ Running |
| NEX-Invoice-Worker-ANDROS | ✅ Running |
| NEX-Polling-Scheduler-ANDROS | ✅ Running |

**API:** http://localhost:8001/health → 200 OK