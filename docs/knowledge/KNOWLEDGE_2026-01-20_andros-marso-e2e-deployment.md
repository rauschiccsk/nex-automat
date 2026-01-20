# KNOWLEDGE: ANDROS MARSO E2E Deployment

**Date:** 2026-01-20
**Session:** ANDROS Loader fixes, MARSO extractor integration, PostgreSQL schema alignment

---

## 1. Infrastructure Overview

### ANDROS Environment

| Component | Location | Details |
|-----------|----------|---------|
| Windows VM | 192.168.100.10 | NEX Genesis, Invoice Loader service |
| Ubuntu Docker Host | 192.168.100.23 | PostgreSQL, Temporal |
| Git Repo | C:\ANDROS\nex-automat | Branch: develop |

### ICC Environment (for comparison)

| Component | Location | Details |
|-----------|----------|---------|
| Windows VM | 192.168.100.11 | NEX Genesis (Mágerstav) |
| Ubuntu Docker Host | 192.168.100.23 | Shared with ANDROS |

### Port Mapping

| Service | ANDROS | ICC | Notes |
|---------|--------|-----|-------|
| PostgreSQL | 5432 | 5433 | Different containers |
| Temporal | 7233 | 7234 | Different containers |
| Temporal UI | 8080 | 8082 | Web interface |
| Invoice Loader API | 8000 | 8001 | FastAPI |

---

## 2. MARSO Extractor

### Purpose
Extract invoice data from Hungarian MARSO tire supplier PDF invoices for ANDROS.

### Files
- `apps/supplier-invoice-loader/src/extractors/marso_extractor.py` - Main extractor
- `apps/supplier-invoice-loader/scripts/test_marso_integration.py` - Integration test

### Key Functions

```python
# Detection - checks if PDF is MARSO invoice
detect_marso_invoice_from_pdf(pdf_path: str) -> bool

# Extraction - extracts and converts to standard format
extract_marso_as_standard(pdf_path: str) -> InvoiceData

# Internal conversion
convert_to_standard_invoice_data(marso_data: MarsoInvoiceData) -> InvoiceData
```

### Routing in main.py

```python
# Line ~459 in main.py
if detect_marso_invoice_from_pdf(str(pdf_path)):
    print("[INFO] Detected MARSO invoice - using MARSO extractor")
    invoice_data = extract_marso_as_standard(str(pdf_path))
else:
    print("[INFO] Using L&Š extractor (default)")
    invoice_data = extract_invoice_data(str(pdf_path))
```

### MARSO Invoice Characteristics
- Hungarian supplier (HU VAT: HU12345678)
- EUR currency
- Date format: DD.MM.YYYY
- Number format: space as thousands separator, comma as decimal
- IČO pattern: 8-digit Hungarian company ID

---

## 3. PostgreSQL Schema

### Problem
Code used `supplier_invoice_heads` but schema had `invoices_pending`.

### Solution
1. Renamed all table references in code
2. Created new schema file matching nex-staging package expectations

### Schema Files

| File | Purpose |
|------|---------|
| `001_initial_schema.sql` | Original schema (invoices_pending) |
| `002_nex_staging_schema.sql` | NEW - nex-staging compatible schema |
| `003_add_file_tracking_columns.sql` | Migration for file tracking |

### Table Structure (002_nex_staging_schema.sql)

**invoices_pending** (41 columns):
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

**invoice_items_pending** (24 columns):
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

### Applying Schema on ANDROS

```bash
# Connect to PostgreSQL
docker exec -it nex-postgres psql -U nex_admin -d nex_automat

# Check existing tables
\dt

# Apply new schema
\i /path/to/002_nex_staging_schema.sql

# Or from host:
docker exec -i nex-postgres psql -U nex_admin -d nex_automat < 002_nex_staging_schema.sql
```

---

## 4. DateStyle Fix

### Problem
PostgreSQL default DateStyle is MDY (US format), but Slovak invoices use DMY (DD.MM.YYYY).

### Solution
Set DateStyle in PostgreSQL session or config:

```sql
-- Per session
SET DateStyle = 'ISO, DMY';

-- Verify
SHOW DateStyle;
```

### Permanent Fix (postgresql.conf)
```
datestyle = 'ISO, DMY'
```

Or in Docker:
```yaml
environment:
  POSTGRES_INITDB_ARGS: "--locale=sk_SK.UTF-8"
command: postgres -c datestyle='ISO,DMY'
```

---

## 5. Code Fixes Applied

### Unicode Emoji Removal
Replaced emoji with ASCII text for Windows cp1250 compatibility:

| Original | Replacement |
|----------|-------------|
| 🔍 | [ENRICH] |
| ✅ | [OK] |
| ⚠ | [WARNING] |
| ❌ | [ERROR] |
| 📊 | [STATS] |

### Table Name Renames

Files modified:
- `apps/supplier-invoice-loader/main.py`
- `apps/supplier-invoice-loader/reports/daily_summary.py`
- `apps/supplier-invoice-loader/database/migrations/003_add_file_tracking_columns.sql`
- `apps/supplier-invoice-loader/database/schemas/README.md`
- `packages/nex-staging/nex_staging/staging_client.py`
- `packages/nex-staging/nex_staging/repositories/invoice_repository.py`

Changes:
- `supplier_invoice_heads` → `invoices_pending`
- `supplier_invoice_items` → `invoice_items_pending`
- `idx_sih_*` → `idx_ip_*`

### Config Template Fixes
Added missing variables to `config_template.py`:
- `STAGING_DIR`
- `NEX_DATA_PATH`

---

## 6. Troubleshooting Commands

### Windows (ANDROS VM)

```powershell
# Check service status
Get-Service -Name "NEX-Automat-Loader-ANDROS"

# Restart service
Restart-Service -Name "NEX-Automat-Loader-ANDROS"

# View logs
Get-Content C:\ANDROS\nex-automat\apps\supplier-invoice-loader\logs\loader.log -Tail 100

# Test API
Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET
```

### Ubuntu Docker Host

```bash
# PostgreSQL
docker exec -it nex-postgres psql -U nex_admin -d nex_automat

# Check tables
docker exec -it nex-postgres psql -U nex_admin -d nex_automat -c "\dt"

# Check invoices
docker exec -it nex-postgres psql -U nex_admin -d nex_automat -c "SELECT id, xml_invoice_number, status FROM invoices_pending LIMIT 10;"

# Temporal
docker logs nex-temporal --tail 100

# Container status
docker ps --filter "name=nex-"
```

### Git Operations

```bash
# On ANDROS Windows
cd C:\ANDROS\nex-automat
git pull origin develop

# Check status
git status
git log --oneline -5
```

---

## 7. Deployment Checklist

### After Code Changes

1. **Development machine:**
   ```bash
   git add .
   git commit -m "fix: description"
   git push
   ```

2. **ANDROS Windows VM:**
   ```powershell
   cd C:\ANDROS\nex-automat
   git pull
   Restart-Service -Name "NEX-Automat-Loader-ANDROS"
   ```

3. **If schema changed:**
   ```bash
   # On Ubuntu Docker host
   docker exec -i nex-postgres psql -U nex_admin -d nex_automat < schema.sql
   ```

### Verification

```bash
# Check loader is responding
curl http://192.168.100.10:8000/health

# Check PostgreSQL connection
docker exec -it nex-postgres psql -U nex_admin -d nex_automat -c "SELECT 1;"

# Check recent invoices
docker exec -it nex-postgres psql -U nex_admin -d nex_automat -c "SELECT COUNT(*) FROM invoices_pending;"
```

---

## 8. Git Commits from This Session

```
56fc038 feat: add nex-staging compatible schema
ba2af41 fix: rename table references in nex-staging package
4cec23b fix: rename supplier_invoice_heads to invoices_pending
f00835d fix: replace unicode emoji with ASCII text for Windows cp1250 compatibility
be5cfd2 fix: add missing STAGING_DIR and NEX_DATA_PATH to config template
3231d34 feat: MARSO invoice extractor for ANDROS
```

---

## 9. Related Documentation

- `docs/knowledge/deployment/DEPLOYMENT_ANDROS_ICC.md` - Full deployment guide
- `apps/supplier-invoice-loader/config/config_template.py` - Configuration reference
- `packages/nex-staging/README.md` - nex-staging package docs

---

*Last updated: 2026-01-20*
