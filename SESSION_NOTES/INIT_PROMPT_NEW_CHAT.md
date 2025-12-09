# INIT PROMPT - NEX Automat v2.4 Phase 4 Deployment

## PROJECT CONTEXT

**Projekt:** nex-automat  
**Typ:** Monorepo - Multi-customer SaaS for automated invoice processing  
**Development:** `C:\Development\nex-automat`  
**Deployment:** `C:\Deployment\nex-automat`  
**Python:** 3.13.7 (venv32)  
**Git Branch:** develop  
**Current Version:** v2.4 Phase 4 - DEPLOYMENT READY

---

## CURRENT STATUS 🔧

### Phase 4: NEX Genesis Product Enrichment
**Status:** DEPLOYMENT PENDING - Critical fix required

**What Works:**
- ✅ PostgreSQL enrichment methods
- ✅ Re-processing script tested (5% match rate)
- ✅ ProductMatcher initialized with Btrieve
- ✅ supplier-invoice-editor displays NEX columns

**What's Broken:**
- ⚠️ **CRITICAL:** BarCode field missing in GSCATRecord model
- ⚠️ EAN matching 0% (should be >65%)
- ⚠️ Overall match rate 5% (target >70%)

**Root Cause:**
GSCATRecord model incomplete - missing 40+ fields from Btrieve including **BarCode** (EAN field)

---

## IMMEDIATE PRIORITY 🎯

### Deploy Complete GSCAT Model

**Problem:**
```python
# Current model (INCOMPLETE):
@dataclass
class GSCATRecord:
    gs_code: int
    gs_name: str  # Only ~20 fields
    # ... BarCode field MISSING!
```

**Solution:**
Complete model with ALL 60+ fields created in artifact `04_create_complete_gscat_model.py`

**Deployment Steps:**
1. Backup current `packages/nexdata/nexdata/models/gscat.py`
2. Replace with complete model from artifact
3. Fix `GSCATRepository.find_by_barcode()` to use `product.BarCode`
4. Test EAN lookup (expect 3/20 matches)
5. Re-run re-processing (expect >70% match rate)

---

## KEY FILES

### Models
```
packages/nexdata/nexdata/models/
└── gscat.py  ← NEEDS REPLACEMENT (missing BarCode!)
```

### Repositories
```
packages/nexdata/nexdata/repositories/
└── gscat_repository.py  ← Fix find_by_barcode() method
```

### Business Logic
```
apps/supplier-invoice-loader/src/business/
└── product_matcher.py  ← May need field name updates
```

### Scripts
```
scripts/
├── 02_reprocess_nex_enrichment.py  # Re-test after fix
└── 03_test_ean_lookup.py           # Verify EAN matching works
```

---

## VERIFIED EAN CODES

These 3 EAN codes ARE in NEX Genesis (manually verified):
- 8715743018251
- 5203473211316
- 3838847028515

After deploying complete GSCAT model, these should match successfully.

---

## TECHNICAL DETAILS

### BarCode Field Specification
```
Field:    BarCode
Type:     Str15 (15 bytes, fixed width)
Offset:   57 (after FgCode)
Encoding: cp852
Content:  EAN barcode code
Index:    IND BarCode=BarCode (Btrieve indexed)
```

### Field Mapping (Btrieve → Python)
```python
# Complete model uses Btrieve field names:
GsCode    → GsCode    (not gs_code)
GsName    → GsName    (not gs_name)
MgCode    → MgCode    (not mglst_code)
BarCode   → BarCode   ← NEW! (EAN field)
```

### Required Changes

**1. GSCATRepository.find_by_barcode():**
```python
# OLD (broken):
if product.barcode and product.barcode.strip() == barcode:
    
# NEW (correct):
if product.BarCode and product.BarCode.strip() == barcode:
```

**2. ProductMatcher (if needed):**
```python
# Check all references to GSCATRecord fields
# Use: product.GsCode, product.GsName, product.BarCode
```

---

## EXPECTED RESULTS AFTER FIX

### EAN Lookup Test
```bash
python scripts/03_test_ean_lookup.py
```
**Expected:**
- 3/20 EAN codes found (15% success rate)
- All 3 matches via GSCAT.BarCode
- No BARCODE.BTR fallback needed

### Re-processing Test
```bash
python scripts/02_reprocess_nex_enrichment.py
```
**Expected:**
- Match rate: >70%
- EAN matches: >65% (via BarCode field)
- Name matches: <5% (fuzzy fallback)
- Errors: <1%

---

## DEPLOYMENT WORKFLOW

```
1. Development Changes
   ├── Deploy complete GSCAT model
   ├── Fix GSCATRepository
   └── Update ProductMatcher (if needed)

2. Testing
   ├── Run 03_test_ean_lookup.py
   ├── Run 02_reprocess_nex_enrichment.py
   └── Verify >70% match rate

3. Git Operations (user does)
   ├── git add .
   ├── git commit -m "..."
   └── git push origin develop

4. Production Deployment (later)
   ├── SQL migration (matched_by column)
   ├── Deploy code changes
   └── Restart NEX-Automat-Loader service
```

---

## SCRIPTS AVAILABLE

### Deployment Scripts (Create)
```python
# 05_deploy_gscat_model.py       # Deploy complete model
# 06_fix_gscat_repository.py     # Fix find_by_barcode()
# 07_verify_field_names.py       # Check ProductMatcher
```

### Testing Scripts (Existing)
```python
scripts/03_test_ean_lookup.py          # Test EAN matching
scripts/02_reprocess_nex_enrichment.py # Full re-processing
```

---

## CRITICAL RULES

### Workflow
1. **Development → Git → Deployment** (never modify Deployment directly)
2. **One script at a time** - wait for confirmation
3. **ALL code MUST be artifacts** - never plain text
4. **Test after each change** - especially Btrieve model changes

### Code Generation
- Scripts numbered sequentially (05, 06, 07...)
- Always create backup before modifying existing files
- Use artifacts for all Python files >5 lines

---

## KNOWN ISSUES

### Issue #1: Missing BarCode Field (CRITICAL) 🔴
**Impact:** 0% EAN match rate  
**Status:** Fix ready in artifact, deployment pending  
**Priority:** P0 - blocks Phase 4 completion

### Issue #2: NULL Bytes in Strings ✅
**Impact:** PostgreSQL INSERT failures  
**Status:** FIXED in re-processing script  
**Solution:** .replace('\x00', '').strip()

### Issue #3: Invalid validation_status ✅
**Impact:** Check constraint violations  
**Status:** FIXED in re-processing script  
**Solution:** Use 'warning' not 'needs_review'

---

## SUCCESS CRITERIA

**Phase 4 Complete When:**
- [ ] Complete GSCAT model deployed
- [ ] EAN lookup test: >15% success rate
- [ ] Re-processing test: >70% match rate
- [ ] All 36 unit tests passing
- [ ] Production deployment successful
- [ ] Mágerstav verification complete

---

## ARTIFACTS REFERENCE

### Complete GSCAT Model
**Artifact:** `04_create_complete_gscat_model.py`
- Contains complete GSCATRecord with all 60+ fields
- BarCode field at offset 57
- All field names match Btrieve definition
- Ready for deployment

### Archive
**Artifact:** `PROJECT_ARCHIVE_SESSION.md`
- Session work summary
- Technical findings
- Metrics and next steps

---

## ENVIRONMENT

**Development:**
- Path: C:\Development\nex-automat
- Python: 3.13.7 (venv32)
- Branch: develop
- Status: Ready for deployment

**Production (Mágerstav):**
- Path: C:\Deployment\nex-automat
- Service: NEX-Automat-Loader (manual start)
- Port: 8001
- Status: Awaiting deployment

**Databases:**
- PostgreSQL: localhost:5432/invoice_staging
- NEX Genesis: C:\NEX\YEARACT\STORES (Btrieve)

---

**Init Prompt Created:** 2025-12-09  
**Version:** v2.4 Phase 4 Deployment  
**Status:** 🔧 Ready to deploy complete GSCAT model  
**Next Action:** Create deployment script for complete GSCAT model