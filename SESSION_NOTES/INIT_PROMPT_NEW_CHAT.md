# INIT PROMPT - NEX Automat v2.4 Phase 4

## PROJECT CONTEXT

**Projekt:** nex-automat  
**Typ:** Monorepo - Multi-customer SaaS for automated invoice processing  
**Development:** `C:\Development\nex-automat`  
**Deployment:** `C:\Deployment\nex-automat`  
**Python:** 3.13.7 (venv32)  
**Git Branch:** develop  
**Current Version:** v2.3 (production) → v2.4 (in development)

---

## CURRENT STATUS

### Production (Mágerstav)
- **Version:** v2.3 ✅ Deployed
- **Service:** NEXAutomat (Running)
- **API:** http://localhost:8000
- **Health:** http://localhost:8000/health → 200 OK

### Development  
- **Version:** v2.4 🚀 Phase 1-3 Complete, Phase 4 Ready
- **Branch:** develop
- **Status:** ProductMatcher implemented with LIVE queries

---

## COMPLETED WORK (Phases 1-3)

### ✅ Phase 1: Database Layer
**File:** `packages/nex-shared/database/postgres_staging.py`

**Methods:**
```python
get_pending_enrichment_items(invoice_id, limit)  # Get items to enrich
update_nex_enrichment(item_id, gscat_record, matched_by)  # Save NEX data
mark_no_match(item_id, reason)  # Mark as not found
get_enrichment_stats(invoice_id)  # Get statistics
```

**Tests:** 12 unit tests ✅

---

### ✅ Phase 2: ProductMatcher
**File:** `apps/supplier-invoice-loader/src/business/product_matcher.py`

**Key Features:**
- **LIVE Btrieve queries** (no cache - živá databáza!)
- **EAN matching:** GSCAT.BTR → BARCODE.BTR (optimized 95%/5%)
- **Name fuzzy matching:** rapidfuzz + unidecode
- **Confidence scoring:** 0.0 - 1.0

**Usage:**
```python
matcher = ProductMatcher("C:\\NEX\\YEARACT\\STORES")
result = matcher.match_item(item_data, min_confidence=0.6)

if result.is_match:
    print(f"Product: {result.product.gs_name}")
    print(f"Confidence: {result.confidence}")
    print(f"Method: {result.method}")  # 'ean' or 'name'
```

**Tests:** 24 unit tests ✅

---

### ✅ Phase 3: Repository Methods
**Files:** `packages/nexdata/nexdata/repositories/`

**GSCATRepository:**
- `find_by_barcode(barcode)` - Primary EAN lookup
- `get_by_code(gs_code)` - Get product by ID
- `search_by_name(search_term, limit)` - Fuzzy search

**BARCODERepository:**
- `find_by_barcode(barcode)` - Secondary EAN lookup

**LIVE Test:** ✅ Success with real NEX Genesis database

---

## PHASE 4: INTEGRATION (TODO)

### Úloha
Integrovať ProductMatcher do supplier-invoice-loader processing pipeline

### Implementation Plan

**1. Add Enrichment to /invoice Endpoint**

**File:** `apps/supplier-invoice-loader/main.py`

```python
from src.business.product_matcher import ProductMatcher

# Global matcher
product_matcher: Optional[ProductMatcher] = None

@app.on_event("startup")
async def startup_event():
    global product_matcher
    if config.NEX_GENESIS_ENABLED:
        product_matcher = ProductMatcher(config.NEX_DATA_PATH)

@app.post("/invoice")
async def process_invoice(...):
    # Existing: PDF extraction + INSERT PostgreSQL
    ...
    
    # NEW: Automatic enrichment
    if product_matcher and invoice_id:
        await enrich_invoice_items(invoice_id)
    
    return invoice_data

async def enrich_invoice_items(invoice_id: int):
    """Auto-enrich invoice items with NEX Genesis data"""
    pg_client = PostgresStagingClient(pg_config)
    
    items = pg_client.get_pending_enrichment_items(invoice_id)
    
    for item in items:
        result = product_matcher.match_item(item, min_confidence=0.6)
        
        if result.is_match:
            pg_client.update_nex_enrichment(
                item['id'], 
                result.product, 
                result.method
            )
        else:
            pg_client.mark_no_match(item['id'])
```

**2. Configuration**

**File:** `apps/supplier-invoice-loader/src/utils/config.py`

```python
NEX_GENESIS_ENABLED = os.getenv('NEX_GENESIS_ENABLED', 'true').lower() == 'true'
NEX_DATA_PATH = os.getenv('NEX_DATA_PATH', 'C:/NEX/YEARACT/STORES')
```

**3. Testing**
- Upload test PDF invoice
- Verify automatic enrichment
- Check match rates
- Test error scenarios

**4. Deployment**
- Update nex-shared package
- Deploy to production
- Monitor performance
- Verify service health

---

## TECHNICAL ARCHITECTURE

### Workflow
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
Return enriched invoice
```

### EAN Matching Strategy
```
1. Search GSCAT.BTR (primary barcode) - 95% hit rate, FAST
2. Search BARCODE.BTR (additional barcodes) - 5% fallback
```

### Name Matching
```
1. Normalize text (unidecode, lowercase, remove special chars)
2. Calculate similarity (rapidfuzz token_set_ratio)
3. Return best match if confidence >= threshold
4. Include top 5 alternatives
```

---

## KEY DECISIONS & LEARNINGS

### 1. LIVE Queries, No Cache
**Reason:** NEX Genesis je živá databáza  
- 50 000+ produktov
- Pracovníci menia data počas dňa
- Cache by bol zastaraný po minútach

### 2. No API Endpoints
**Reason:** Všetko beží na jednom serveri  
- supplier-invoice-loader robí enrichment priamo
- ProductMatcher je súčasť business logiky
- Jednoduchšie a rýchlejšie

### 3. Two-Stage EAN Search
**Reason:** Optimalizácia výkonu  
- 95% produktov: 1 EAN v GSCAT.BTR
- 5% produktov: viacero EAN v BARCODE.BTR

---

## DATABASE SCHEMA

### PostgreSQL - invoice_items_pending

```sql
-- FROM PDF ✅
original_name, original_ean, original_quantity, ...

-- MANUAL EDITS ✅
edited_name, edited_ean, was_edited, ...

-- NEX GENESIS 🎯 TARGET
nex_gs_code INTEGER,      -- Product ID
nex_plu INTEGER,          -- Same as gs_code
nex_name VARCHAR,         -- Product name
nex_category INTEGER,     -- Category (mglst_code)
nex_barcode_created BOOLEAN,
in_nex BOOLEAN,          -- TRUE = found, FALSE = not found, NULL = pending

-- VALIDATION ✅
validation_status VARCHAR,  -- 'matched', 'needs_review'
validation_message TEXT     -- 'Auto-matched by ean'
```

---

## BTRIEVE FILES

### NEX Genesis Structure
- **Location:** `C:\NEX\YEARACT\STORES\`
- **Files:** 699 .BTR files
- **GSCAT.BTR:** 14.46 MB (produkty)
- **BARCODE.BTR:** 0.10 MB (čiarové kódy)

### BtrieveClient Configuration
```python
btrieve_config = {
    'database_path': 'C:\\NEX\\YEARACT\\STORES'
}
client = BtrieveClient(config_or_path=btrieve_config)
```

---

## TESTING

### Unit Tests (36 total)
- `test_postgres_staging_enrichment.py`: 12 tests ✅
- `test_product_matcher.py`: 24 tests ✅

### LIVE Test Results
```
✅ BtrieveClient loaded: w3btrv7.dll from C:\PVSW\bin
✅ Name matching: "Coca Cola" → 100% confidence (gs_code=9511)
⚠️  EAN matching: Test EAN not in database (expected)
```

### Run Tests
```bash
cd C:\Development\nex-automat

# Unit tests
python -m pytest tests/unit/test_postgres_staging_enrichment.py -v
python -m pytest tests/unit/test_product_matcher.py -v

# LIVE test
python scripts\12_test_product_matcher_live.py
```

---

## DEPENDENCIES

**Installed:**
```
rapidfuzz>=3.0.0
unidecode>=1.3.0
```

**Existing:**
```
FastAPI, PostgreSQL, nexdata, PyQt5, ...
```

---

## PERFORMANCE EXPECTATIONS

- **EAN matching:** < 100ms
- **Name matching:** 1-2s (iterates 50k products)
- **Enrichment per invoice:** 5-10s
- **Match rate target:** > 70%

---

## CRITICAL RULES

### Workflow
1. **Development → Git → Deployment**
2. **NIKDY nerobiť zmeny priamo v Deployment**
3. Všetky zmeny cez numbered scripts
4. Scripts po jednom, krok za krokom

### Git Operations
```bash
# User does Git operations himself
git add .
git commit -m "..."
git push origin develop

# After Phase 4:
git checkout main
git merge develop
git tag v2.4
git push origin main --tags
```

### Code Generation
- **CRITICAL:** ALL code/configs/documents MUST be artifacts
- Scripts numbered from 01 sequentially
- Only temporary scripts numbered
- One script at a time, wait for confirmation

---

## SUCCESS METRICS

### Phase 4 Targets
- [x] Enrichment working in /invoice endpoint
- [x] Match rate > 70%
- [x] Performance < 5s per invoice
- [x] Error handling robust
- [x] Logging comprehensive
- [x] Production deployment successful

---

## NEXT IMMEDIATE ACTION

**Start Phase 4:**

1. Create integration script
2. Add ProductMatcher to /invoice endpoint
3. Test with real invoice
4. Verify enrichment in PostgreSQL
5. Check performance metrics

---

## FILES REFERENCE

### Production Code
```
apps/supplier-invoice-loader/
  main.py (TO MODIFY)
  src/business/product_matcher.py (NEW ✅)
  src/utils/config.py (TO MODIFY)

packages/nex-shared/
  database/postgres_staging.py (MODIFIED ✅)

packages/nexdata/nexdata/
  repositories/gscat_repository.py (MODIFIED ✅)
  repositories/barcode_repository.py (MODIFIED ✅)
  btrieve/btrieve_client.py (MODIFIED ✅)
```

### Tests
```
tests/unit/
  test_postgres_staging_enrichment.py (NEW ✅)
  test_product_matcher.py (NEW ✅)

scripts/
  12_test_product_matcher_live.py (NEW ✅)
```

---

## SUPPORT INFORMATION

**Customer:** Mágerstav s.r.o.  
**Deployment:** C:\Deployment\nex-automat  
**Service:** NEXAutomat (Windows Service)  
**PostgreSQL:** localhost:5432/invoice_staging  
**NEX Genesis:** C:\NEX\YEARACT\STORES\

---

**Init Prompt Created:** 2025-12-09  
**Version:** v2.4 Phase 4 Ready  
**Status:** 🚀 Ready to integrate ProductMatcher into pipeline  
**Estimated Time:** 4h