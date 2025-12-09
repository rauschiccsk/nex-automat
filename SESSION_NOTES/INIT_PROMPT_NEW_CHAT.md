# INIT PROMPT - NEX Automat v2.4 Post-Deployment

## PROJECT CONTEXT

**Projekt:** nex-automat  
**Typ:** Monorepo - Multi-customer SaaS for automated invoice processing  
**Development:** `C:\Development\nex-automat`  
**Deployment:** `C:\Deployment\nex-automat`  
**Python:** 3.13.7 (venv32)  
**Git Branch:** develop  
**Current Version:** v2.4 Phase 4 ✅ DEPLOYED

---

## CURRENT STATUS

### Production (Mágerstav) ✅ LIVE
- **Version:** v2.4 Phase 4 DEPLOYED
- **Service:** NEX-Automat-Loader (Ready to start as Windows Service)
- **Currently:** Running in debug mode (manual python main.py)
- **API:** http://localhost:8001
- **ProductMatcher:** ✅ INITIALIZED
- **Btrieve:** ✅ CONNECTED to C:\NEX\YEARACT\STORES

**Startup Log:**
```
✅ Loaded Btrieve DLL: w3btrv7.dll from C:\PVSW\bin
✅ ProductMatcher initialized: C:\NEX\YEARACT\STORES
INFO: Uvicorn running on http://0.0.0.0:8001
```

### Development
- **Version:** v2.4 Phase 4 Complete
- **Branch:** develop
- **Status:** Ready for testing and Git operations

---

## COMPLETED WORK

### ✅ Phase 1: Database Layer (Completed)
- PostgreSQL enrichment methods in postgres_staging.py
- 12 unit tests passing

### ✅ Phase 2: ProductMatcher (Completed)
- LIVE Btrieve queries (no cache)
- EAN matching (GSCAT.BTR → BARCODE.BTR)
- Name fuzzy matching (rapidfuzz + unidecode)
- 24 unit tests passing

### ✅ Phase 3: Repository Methods (Completed)
- GSCATRepository with find_by_barcode, search_by_name
- BARCODERepository with find_by_barcode
- LIVE test successful

### ✅ Phase 4: Integration & Deployment (Completed Today)

**supplier-invoice-loader:**
- ProductMatcher integrated into /invoice endpoint
- Automatic enrichment after PDF extraction
- Config properly set (NEX_GENESIS_ENABLED=True)
- Dependencies installed (rapidfuzz, unidecode)

**supplier-invoice-editor:**
- Grid shows 4 NEX columns (NEX Kód, NEX Názov, NEX Kat., Match)
- Color-coded rows:
  - Green = matched (in_nex = TRUE)
  - Red = no match (in_nex = FALSE)
  - Yellow = pending (in_nex = NULL)
- Tooltips show match method (EAN/Name)
- PostgreSQL loads all NEX fields

**Deployment:**
- Backup created: C:\Deployment\nex-automat\BACKUP_2025-12-09_09-18-30
- All files deployed from Development
- Service verified functional
- 20 deployment scripts created

---

## IMMEDIATE NEXT STEPS

### 🎯 Priority 1: Start Windows Service

Currently supplier-invoice-loader runs in debug mode (manual). Need to:

1. **Stop debug mode** (CTRL+C in current terminal)

2. **Start Windows Service:**
```powershell
Start-Service NEX-Automat-Loader
Get-Service NEX-Automat-Loader  # Verify Running
```

3. **Verify health:**
```powershell
curl http://localhost:8001/health
```

4. **Check logs** for ProductMatcher initialization

---

### Priority 2: End-to-End Testing

1. **Upload test PDF** via n8n workflow
2. **Check PostgreSQL** for enrichment:
```sql
SELECT 
  original_name, 
  nex_name, 
  nex_gs_code, 
  in_nex, 
  matched_by 
FROM invoice_items_pending 
ORDER BY id DESC LIMIT 10;
```

3. **Open supplier-invoice-editor** and verify:
   - NEX columns visible
   - Color coding works
   - Tooltips display correctly

---

### Priority 3: Git Operations

```bash
cd C:\Development\nex-automat
git status
git add .
git commit -m "Phase 4: NEX Genesis Product Enrichment Integration

- ProductMatcher integrated into supplier-invoice-loader
- Automatic enrichment on /invoice endpoint
- supplier-invoice-editor displays NEX data with color coding
- PostgreSQL enrichment methods implemented
- 36 unit tests passing
- Deployed to production (Mágerstav)"

git push origin develop
```

After successful testing:
```bash
git checkout main
git merge develop
git tag v2.4
git push origin main --tags
```

---

## TECHNICAL ARCHITECTURE

### Enrichment Workflow
```
POST /invoice (PDF)
  ↓
Extract PDF → PostgreSQL (original_* fields)
  ↓
ProductMatcher.match_item() [LIVE Btrieve queries]
  ├─ Try EAN: GSCAT.BTR (95%) → BARCODE.BTR (5%)
  └─ Try Name: fuzzy search (confidence 0.6-1.0)
  ↓
PostgreSQL UPDATE (nex_* fields)
  ↓
supplier-invoice-editor displays with color coding
```

### Files Structure
```
apps/
  supplier-invoice-loader/
    main.py - ProductMatcher integration
    config/config_customer.py - NEX_GENESIS_ENABLED=True
    src/business/product_matcher.py - NEW
    src/utils/config.py - _Config wrapper
  
  supplier-invoice-editor/
    src/ui/widgets/invoice_items_grid.py - NEX columns + colors
    src/business/invoice_service.py - NEX fields in query

packages/
  nex-shared/
    database/postgres_staging.py - enrichment methods
    database/__init__.py - exports
  
  nexdata/
    repositories/gscat_repository.py
    repositories/barcode_repository.py
    btrieve/btrieve_client.py
```

---

## CONFIGURATION

### NEX Genesis (Mágerstav)
```python
NEX_GENESIS_ENABLED = True
NEX_DATA_PATH = r"C:\NEX\YEARACT\STORES"
```

### PostgreSQL
```python
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_DATABASE = "invoice_staging"
```

### API
```
Port: 8001
Health: http://localhost:8001/health
Docs: http://localhost:8001/docs
```

---

## DEPLOYMENT BACKUP

**Location:** `C:\Deployment\nex-automat\BACKUP_2025-12-09_09-18-30`

**Backed up files:**
- loader_main.py
- loader_config_customer.py
- loader_config.py
- editor_invoice_items_grid.py
- editor_invoice_service.py

**Rollback if needed:**
1. Stop service
2. Restore files from backup
3. Restart service

---

## TESTING STATUS

### Unit Tests
- postgres_staging_enrichment: 12/12 ✅
- product_matcher: 24/24 ✅
- Total: 36/36 ✅

### Integration Test
- Imports: ✅
- Configuration: ✅
- ProductMatcher Init: ✅
- Product Matching: ✅
- PostgreSQL Methods: ✅

### Production Verification
- Service starts: ✅
- ProductMatcher initializes: ✅
- Btrieve connects: ✅
- Health endpoint: ✅

---

## SUCCESS METRICS

**Phase 4 Targets:**
- [x] Integration working in /invoice endpoint
- [x] ProductMatcher initialized with Btrieve
- [x] Grid displays NEX columns with color coding
- [x] PostgreSQL loads all NEX fields
- [x] Production deployment successful
- [ ] Match rate > 70% (needs testing with real data)
- [ ] Performance < 5s per invoice (needs testing)

---

## KNOWN ISSUES

**None currently** - All deployment issues resolved

Previous issues (fixed):
- ✅ Config structure (fixed with _Config wrapper)
- ✅ Missing imports (cleaned)
- ✅ Dependencies (installed)
- ✅ ProductMatcher initialization (added properly)
- ✅ Port conflicts (NEX-Automat-Loader service)

---

## CRITICAL RULES

### Workflow
1. **Development → Git → Deployment**
2. **NEVER modify Deployment directly**
3. All changes via numbered scripts
4. Scripts one at a time, wait for confirmation

### Git Operations
```bash
# User does Git operations himself
git add .
git commit -m "..."
git push origin develop
```

### Code Generation
- **CRITICAL:** ALL code/configs/documents MUST be artifacts
- Scripts numbered from 01 sequentially
- One script at a time, wait for confirmation

---

## MONITORING

### Daily Checks
- Service status: `Get-Service NEX-Automat-Loader`
- Logs review
- Match rates in PostgreSQL
- Error monitoring

### Performance Metrics
- Enrichment time per invoice
- Match rate percentage
- Database query performance
- Memory usage

---

## SUPPORT INFORMATION

**Customer:** Mágerstav s.r.o.  
**Deployment:** C:\Deployment\nex-automat  
**Service:** NEX-Automat-Loader (Windows Service)  
**Port:** 8001  
**PostgreSQL:** localhost:5432/invoice_staging  
**NEX Genesis:** C:\NEX\YEARACT\STORES  

---

**Init Prompt Created:** 2025-12-09  
**Version:** v2.4 Phase 4 DEPLOYED  
**Status:** 🎉 Ready for Windows Service start & E2E testing  
**Next Action:** Start NEX-Automat-Loader service