# INIT PROMPT - NEX Automat v2.4 Column Mapping Fix

## PROJECT CONTEXT

**Projekt:** nex-automat  
**Typ:** Monorepo - Multi-customer SaaS for automated invoice processing  
**Development:** `C:\Development\nex-automat`  
**Deployment:** `C:\Deployment\nex-automat`  
**Python:** 3.13.7 (venv32)  
**Git Branch:** develop  
**Current Version:** v2.4 - DEPLOYED with Column Mapping Issue

---

## ⚠️ CRITICAL ISSUE - MUST FIX FIRST

### Problem: Invoice Editor Column Names Incorrect

**Current State (WRONG):**
| Column Header | Contains | Should Contain |
|---------------|----------|----------------|
| PLU | GsCode (3786) | GsCode (3786) ✅ |
| ??? | MISSING | Barcode (8594002536213) ❌ |
| NEX Kód | EMPTY | ??? |
| NEX Názov | EMPTY | Product name from GSCAT |

**Expected State (CORRECT):**
| Column Header | Contains | Source |
|---------------|----------|--------|
| Čiarový kód | 8594002536213 | From invoice PDF/XML (IMMUTABLE) |
| PLU | 3786 | GSCAT.GsCode (NEX Genesis) |
| NEX Názov | AT GRUND 3kg koncentrát | GSCAT.NAZ |
| NEX Kat. | 0 | GSCAT.Kategória |
| Match | ean | matched_by (ean/name/manual) |

**Root Cause:**
- Re-processing overwrites `plu_code` with `GsCode`
- Original barcode from invoice is **lost**
- Column mapping in Invoice Editor is incorrect

**Impact:**
- ⚠️ User cannot verify which invoice item was matched
- ⚠️ Original barcode data is lost
- ⚠️ Cannot re-match if needed

---

## CURRENT STATUS - v2.4 DEPLOYED

### Production (Mágerstav) ✅
```
Service: NEXAutomat (NSSM)
Status: Running
Version: v2.4 (Git tag: v2.4)
API: http://localhost:8001
Health: ✅ {"status":"healthy"}
NEX Enrichment: ✅ Active (77.4% match rate)
Column Mapping: ❌ INCORRECT (needs fix)
```

**Recent Deployment (2025-12-09):**
- ✅ Git: merged develop → main, tagged v2.4
- ✅ Dependencies: rapidfuzz, unidecode installed
- ✅ Config: NEX_GENESIS_ENABLED = True
- ✅ Btrieve: GSCAT.BTR accessible
- ✅ PostgreSQL: matched_by column added (Migration 22)
- ✅ Re-processing: 278/359 items matched (77.4%)
- ❌ Column mapping: BROKEN (plu_code overwritten)

---

## IMMEDIATE TASKS

### Priority 1: Fix Column Mapping (URGENT)

**Files to Check:**
1. **PostgreSQL Schema:**
   - `packages/nex-shared/database/postgres_staging.py`
   - Check: Which field stores barcode vs GsCode?
   - Current: `plu_code` gets overwritten (WRONG)

2. **ProductMatcher:**
   - `apps/supplier-invoice-loader/src/business/product_matcher.py`
   - Check: `match_item()` method
   - Problem: Likely overwrites plu_code with GsCode

3. **Re-processing Script:**
   - `scripts/reprocess_nex_enrichment.py`
   - Check: UPDATE query
   - Problem: Updates plu_code instead of nex_gs_code

4. **Invoice Editor Grid:**
   - `apps/supplier-invoice-editor/src/ui/widgets/invoice_items_grid.py`
   - Check: Column definitions
   - Problem: May have wrong column names/mapping

**Required Fix:**
```python
# WRONG (current):
UPDATE invoice_items_pending SET
    plu_code = {gscat.GsCode},  # ❌ Overwrites barcode!
    nex_name = {gscat.NAZ}
WHERE id = ...

# CORRECT (needed):
UPDATE invoice_items_pending SET
    nex_gs_code = {gscat.GsCode},  # ✅ Separate field!
    nex_name = {gscat.NAZ},
    matched_by = 'ean'
WHERE id = ...
-- plu_code stays UNCHANGED (original barcode)
```

**Steps:**
1. [ ] Analyze current column mapping
2. [ ] Identify where plu_code gets overwritten
3. [ ] Fix ProductMatcher to use nex_gs_code
4. [ ] Fix reprocess script
5. [ ] Fix Invoice Editor column headers
6. [ ] Test with invoice 32509318
7. [ ] Verify barcodes preserved

---

## PROJECT STRUCTURE

```
nex-automat/
├── apps/
│   ├── supplier-invoice-editor/      # PyQt5 desktop app
│   │   └── src/ui/widgets/
│   │       └── invoice_items_grid.py # ⚠️ CHECK: Column names
│   └── supplier-invoice-loader/      # FastAPI service (port 8001)
│       └── src/business/
│           └── product_matcher.py    # ⚠️ CHECK: Match logic
├── packages/
│   ├── nex-shared/                   # Shared models (FLAT structure)
│   │   └── database/
│   │       └── postgres_staging.py   # ⚠️ CHECK: Schema
│   └── nexdata/                      # Btrieve access layer
└── scripts/
    ├── reprocess_nex_enrichment.py   # ⚠️ CHECK: UPDATE query
    └── 22_migrate_postgres_phase4.py # Migration (already run)
```

---

## POSTGRESQL SCHEMA

### invoice_items_pending (Current Schema)

**Current Columns:**
```sql
-- Original columns
id SERIAL PRIMARY KEY
invoice_id INTEGER
plu_code VARCHAR(50)           -- ⚠️ CURRENTLY: Gets overwritten with GsCode
item_name VARCHAR(255)
quantity DECIMAL(10,3)
unit_price DECIMAL(10,2)
...

-- NEX Enrichment columns (Phase 3+4)
nex_gs_code INTEGER            -- GsCode from GSCAT (SHOULD be used!)
nex_name VARCHAR(255)          -- Product name from GSCAT
in_nex BOOLEAN                 -- Found in NEX Genesis
matched_by VARCHAR(20)         -- 'ean' | 'name' | 'manual' (Phase 4)
validation_status VARCHAR(20)  -- 'pending' | 'valid' | 'warning' | 'error'
```

**Problem:**
- `plu_code` should contain **barcode from invoice** (IMMUTABLE)
- `nex_gs_code` should contain **GsCode from GSCAT** (from matching)
- Currently: `plu_code` gets **overwritten** with `nex_gs_code` value

---

## DEVELOPMENT WORKFLOW

```
1. Development → Git → Deployment
2. All fixes via Development first
3. Test locally
4. Commit and push
5. Pull in Deployment
6. Restart service/task
```

**Git:**
```powershell
git add .
git commit -m "Fix: Preserve barcode in plu_code, use nex_gs_code for GsCode"
git push
```

**Deployment:**
```powershell
cd C:\Deployment\nex-automat
git pull
Stop-Service -Name "NEXAutomat" -Force
Start-Service -Name "NEXAutomat"
```

---

## TESTING CHECKLIST

### After Fix is Applied
- [ ] Re-process invoice 32509318
- [ ] Open in Invoice Editor
- [ ] Verify columns:
  - [ ] **Čiarový kód**: Shows 8594002536213 (barcode)
  - [ ] **PLU**: Shows 3786 (GsCode)
  - [ ] **NEX Názov**: Shows "AT GRUND 3kg koncentrát"
  - [ ] **Match**: Shows "ean"
- [ ] Check PostgreSQL:
  ```sql
  SELECT plu_code, nex_gs_code, nex_name, matched_by
  FROM invoice_items_pending
  WHERE invoice_id = ...
  LIMIT 10;
  ```
- [ ] Verify: plu_code = barcode, nex_gs_code = GsCode

---

## COMMON ISSUES

### Column Mapping
**Q:** Why is plu_code overwritten?  
**A:** ProductMatcher or reprocess script updates wrong field

**Q:** Where should GsCode be stored?  
**A:** In `nex_gs_code` field (already exists!)

**Q:** What is plu_code?  
**A:** Should be barcode from invoice XML/PDF (original data)

### Re-processing
**Q:** Can we re-process without losing barcodes?  
**A:** Yes, after fixing UPDATE query to use nex_gs_code

---

## ENVIRONMENT DETAILS

**Production Server (Mágerstav):**
- OS: Windows Server
- Python: 3.13.7 32-bit (venv32)
- Database: PostgreSQL (invoice_staging) + Btrieve (NEX Genesis)
- Service: NEXAutomat (NSSM)
- Status: ✅ Running
- Version: v2.4

**Configuration:**
```python
# config_customer.py (not in Git!)
NEX_GENESIS_ENABLED = True
NEX_DATA_PATH = r"C:\NEX\YEARACT\STORES"
CUSTOMER_CODE = "MAGERSTAV"
```

---

## KEY REMINDERS

### Communication
- All communication in Slovak language
- One solution at a time, wait for confirmation
- End response with token usage

### Code Standards
- ALL code/configs/docs in artifacts (ALWAYS)
- Development → Git → Deployment workflow
- Never fix directly in Deployment
- Test after every change

### Critical Rules
- NEVER start work if GitHub files fail to load
- NEVER reboot test server (Pervasive breaks)
- ALWAYS preserve original invoice data
- NEVER overwrite immutable fields (like barcode)

---

## QUICK COMMANDS

### Development Testing
```powershell
cd C:\Development\nex-automat
python -m pytest packages/nexdata/tests/ -v
```

### Deployment Service
```powershell
# Restart
Stop-Service -Name "NEXAutomat" -Force
Start-Service -Name "NEXAutomat"

# Status
Get-Service -Name "NEXAutomat"
Test-NetConnection localhost -Port 8001
curl http://localhost:8001/health
```

### View Logs
```powershell
Get-Content C:\Deployment\nex-automat\logs\service-stderr.log -Tail 50
```

---

## SUPPORT INFO

**Developer:** Zoltán  
**Company:** ICC Komárno  
**Customer:** Mágerstav s.r.o.  
**Deployment Date:** 2025-12-09  
**Current Issue:** Column mapping incorrect  
**Priority:** URGENT FIX NEEDED

---

**Init Prompt Created:** 2025-12-09 20:30  
**Version:** v2.4 - DEPLOYED (Column Fix Needed)  
**Status:** ⚠️ Fix column mapping before new features  
**Next:** Analyze and fix plu_code overwrite issue