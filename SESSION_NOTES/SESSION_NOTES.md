# SESSION NOTES - NEX Automat v2.4

**Last Updated:** 2025-12-09 20:30  
**Current Phase:** v2.4 Phase 4 - DEPLOYED (Column Names Issue)  
**Next Priority:** Fix Invoice Editor Column Mapping

---

## CURRENT STATUS

### Production (Mágerstav) - DEPLOYED ✅
```
Service: NEXAutomat (NSSM)
Status: Running
Version: v2.4 (Git tag pushed)
API: http://localhost:8001
Health: ✅ Healthy
Features: NEX Genesis Product Enrichment Active
Match Rate: 77.4% (278/359 items)
```

### CRITICAL ISSUE ⚠️
**Problem:** Column names in Invoice Editor are incorrect
- **PLU** stĺpec obsahuje GsCode (prepísaný z čiarového kódu)
- **Čiarový kód** sa stratil
- **NEX Kód** stĺpec je prázdny

**Expected:**
| Column | Content | Source |
|--------|---------|--------|
| Čiarový kód | 8594002536213 | From invoice (IMMUTABLE) |
| PLU | 3786 | GSCAT.GsCode |
| NEX Názov | Product name | GSCAT.NAZ |
| Match | ean | matched_by field |

---

## NEXT STEPS

### Priority 1: Fix Column Mapping (URGENT)
1. [ ] Analyze: Why plu_code gets overwritten
2. [ ] Check: Invoice Editor column mapping
3. [ ] Check: ProductMatcher update logic
4. [ ] Check: PostgreSQL schema field names
5. [ ] Fix: Preserve barcode, add GsCode to separate column
6. [ ] Test: Re-process with correct mapping
7. [ ] Verify: All columns display correctly

### Priority 2: Production Monitoring
- [ ] Monitor service stability (1 week)
- [ ] Test verification workflow
- [ ] Document any issues

---

## RECENT CHANGES (2025-12-09)

### Deployment v2.4 Completed
1. ✅ Git: merge develop → main, tag v2.4
2. ✅ Dependencies: rapidfuzz, unidecode
3. ✅ Config: NEX_GENESIS_ENABLED, NEX_DATA_PATH
4. ✅ Btrieve: GSCAT.BTR copied to server
5. ✅ PostgreSQL: Migration 22 (matched_by column)
6. ✅ Re-processing: 278/359 matched (77.4%)
7. ✅ Service: NEXAutomat running

### Issues Resolved
- ❌→✅ Missing rapidfuzz dependency
- ❌→✅ Missing unidecode dependency
- ❌→✅ Missing nexdata/nex-shared packages
- ❌→✅ Missing NEX_GENESIS config
- ❌→✅ Btrieve error 11 (GSCAT.BTR missing)
- ❌→✅ PostgreSQL matched_by column missing

### Issues Discovered
- ⚠️ Column names mapping incorrect (PLU vs Čiarový kód)

---

## TECHNICAL NOTES

### PostgreSQL Schema (invoice_items_pending)
```sql
-- NEX Enrichment columns (Phase 3+4)
nex_gs_code INTEGER          -- GsCode from GSCAT
nex_name VARCHAR(255)         -- Product name from GSCAT
in_nex BOOLEAN                -- Found in NEX Genesis
matched_by VARCHAR(20)        -- Method: 'ean' | 'name' | 'manual'
validation_status VARCHAR(20) -- 'pending' | 'valid' | 'warning' | 'error'

-- Original columns
plu_code VARCHAR(50)          -- SHOULD BE: Barcode from invoice
-- BUT: Currently gets overwritten with GsCode!
```

### Column Mapping Problem
**Current behavior (WRONG):**
```python
# Somewhere in code:
item.plu_code = gscat_record.GsCode  # ❌ Overwrites barcode!
```

**Expected behavior (CORRECT):**
```python
# Should be:
item.barcode = original_barcode      # ✅ Preserve original
item.plu_code = gscat_record.GsCode  # ✅ Or rename to nex_gs_code?
```

### Files to Investigate
1. `apps/supplier-invoice-loader/src/business/product_matcher.py` - Match logic
2. `scripts/reprocess_nex_enrichment.py` - Re-processing logic
3. `apps/supplier-invoice-editor/src/ui/widgets/invoice_items_grid.py` - Grid columns
4. `packages/nex-shared/database/postgres_staging.py` - PostgreSQL schema

---

## DEPLOYMENT INFO

### Service Configuration (NSSM)
```
Service Name: NEXAutomat
Display Name: NEX Automat v2.0 - Supplier Invoice Loader
Application: C:\Deployment\nex-automat\venv32\Scripts\python.exe
Parameters: C:\Deployment\nex-automat\apps\supplier-invoice-loader\main.py
Directory: C:\Deployment\nex-automat
Account: LocalSystem
Status: Running
```

### Environment
- Python: 3.13.7 32-bit (venv32)
- PostgreSQL: localhost:5432/invoice_staging
- Btrieve: C:\NEX\YEARACT\STORES (w3btrv7.dll)
- Git Branch: main (deployed), develop (active development)

### Dependencies (New in v2.4)
```
rapidfuzz==3.14.3     # Fuzzy string matching
unidecode==1.4.0      # Unicode normalization
nexdata==0.1.0        # Btrieve access layer
nex-shared==1.0.0     # Shared models
```

---

## TESTING CHECKLIST

### When Column Fix is Ready
- [ ] Test: Load invoice 32509318
- [ ] Verify: Čiarový kód column shows barcodes
- [ ] Verify: PLU column shows GsCodes
- [ ] Verify: NEX Názov shows product names
- [ ] Verify: Match column shows 'ean'
- [ ] Test: Re-process all invoices
- [ ] Verify: Match rate still ~77%
- [ ] Test: Manual invoice upload
- [ ] Verify: Real-time enrichment works

---

## IMPORTANT REMINDERS

### Config Changes (Not in Git)
File: `apps/supplier-invoice-loader/config/config_customer.py`
```python
NEX_GENESIS_ENABLED = True
NEX_DATA_PATH = r"C:\NEX\YEARACT\STORES"
```

### Development → Git → Deployment Workflow
1. Fix in Development
2. Test locally
3. Commit and push
4. Pull in Deployment
5. Restart service
6. Verify

### Critical Rules
- ⚠️ NEVER fix directly in Deployment
- ⚠️ NEVER reboot test server (Pervasive breaks)
- ⚠️ ALWAYS use artifacts for code/configs
- ⚠️ ALWAYS test after deployment

---

## QUICK COMMANDS

### Check Service Status
```powershell
Get-Service -Name "NEXAutomat"
Test-NetConnection localhost -Port 8001
curl http://localhost:8001/health
```

### Restart Service
```powershell
Stop-Service -Name "NEXAutomat" -Force
Start-Service -Name "NEXAutomat"
```

### View Logs
```powershell
Get-Content C:\Deployment\nex-automat\logs\service-stderr.log -Tail 50
```

### Git Operations
```powershell
# In Deployment
cd C:\Deployment\nex-automat
git pull origin main
```

---

**Session Status:** Active  
**Focus:** Fix Invoice Editor Column Mapping  
**Goal:** Preserve barcodes, display GsCodes correctly