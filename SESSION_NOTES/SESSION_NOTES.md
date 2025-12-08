# SESSION NOTES - nex-automat v2.4

## CURRENT STATUS

**Verzia:** v2.4 (in development)  
**Status:** Ready for Phase 1 Implementation  
**Posledná zmena:** 2025-12-08

### Production (Magerstav)
- **Lokácia:** `C:\Deployment\nex-automat`
- **Verzia:** v2.3 ✅
- **Service:** NEXAutomat (Running) ✅
- **API:** http://localhost:8000 ✅
- **Health Check:** 200 OK ✅

### Development
- **Lokácia:** `C:\Development\nex-automat`
- **Branch:** develop
- **Verzia:** v2.4 (WIP)
- **Python:** 3.13.7 (venv32)

---

## VERSION ROADMAP

### v2.3 (2025-12-08) - Current Production ✅

**Status:** Deployed and running

**Features:**
- Email PDF → PostgreSQL staging
- ISDOC XML generation
- Duplicate detection
- Basic invoice processing

**Known Limitations:**
- NEX Genesis enrichment NOT implemented
- Items have empty nex_* fields
- Manual product matching required

---

### v2.4 (2025-12-08) - In Development 🚧

**Goal:** Implement NEX Genesis product enrichment

**Status:** Phase 0 - Analysis Complete ✅

**Next:** Phase 1 - Database Layer

**Implementation Plan:**

| Phase | Task | Hours | Status |
|-------|------|-------|--------|
| 1 | PostgreSQL methods | 6h | 🔲 TODO |
| 2 | ProductMatcher class | 11h | 🔲 TODO |
| 3 | API endpoints | 6h | 🔲 TODO |
| 4 | Deployment | 4h | 🔲 TODO |
| **TOTAL** | | **27h** | **~4 dni** |

---

## ARCHITECTURAL OVERVIEW

### Current Workflow (v2.3)

```
┌──────────────┐
│ Email (n8n)  │
└──────┬───────┘
       │ PDF
       ↓
┌──────────────────────┐
│ supplier-invoice-    │
│ loader (FastAPI)     │
│                      │
│ POST /invoice        │
└──────┬───────────────┘
       │
       ├─→ SQLite (local)
       │   - invoices table
       │   - status tracking
       │
       └─→ PostgreSQL (staging)
           - invoices_pending
           - invoice_items_pending
             ├─ original_* (from PDF) ✅
             ├─ edited_* (manual) ✅
             ├─ nex_* (EMPTY) ❌
             └─ in_nex (NULL) ❌
```

### Target Workflow (v2.4)

```
┌──────────────┐
│ Email (n8n)  │
└──────┬───────┘
       │
       ↓
┌──────────────────────┐
│ supplier-invoice-    │
│ loader (FastAPI)     │
└──────┬───────────────┘
       │
       ├─→ SQLite
       │
       └─→ PostgreSQL
           ├─ invoice_items_pending
           │  (original_*, edited_*)
           │
           ↓ NEW: Enrichment API
           │
           ├─→ ProductMatcher
           │   ├─ Match by EAN (BARCODE)
           │   └─ Match by Name (fuzzy)
           │
           └─→ NEX Genesis (Btrieve)
               ├─ GSCAT.BTR (products)
               └─ BARCODE.BTR (EAN codes)
               
           Result:
           └─→ PostgreSQL UPDATE
               ├─ nex_gs_code ✅
               ├─ nex_name ✅
               ├─ nex_category ✅
               └─ in_nex = TRUE ✅
```

---

## PROJECT STRUCTURE

```
nex-automat/
├── apps/
│   ├── supplier-invoice-editor/    # PyQt5 Desktop (v2.2)
│   │
│   └── supplier-invoice-loader/    # FastAPI Service (v2.3 → v2.4)
│       ├── main.py (v2.3)
│       │   └── NEW in v2.4:
│       │       ├── POST /enrich/invoice/{id}
│       │       ├── GET /enrich/stats/{id}
│       │       └── GET /pending/items
│       │
│       └── src/
│           ├── api/
│           ├── business/
│           │   └── product_matcher.py (NEW v2.4) 🚧
│           ├── database/
│           │   └── database.py (SQLite)
│           └── utils/
│
├── packages/
│   ├── nex-shared/ (v1.0.0 → v1.1.0)
│   │   ├── ui/
│   │   │   ├── base_grid.py
│   │   │   └── base_window.py
│   │   ├── utils/
│   │   │   ├── text_utils.py (v2.3)
│   │   │   └── grid_settings.py
│   │   └── database/
│   │       ├── window_settings_db.py
│   │       └── postgres_staging.py (UPDATE v2.4) 🚧
│   │           └── NEW methods:
│   │               ├── get_pending_enrichment_items()
│   │               ├── update_nex_enrichment()
│   │               ├── mark_no_match()
│   │               └── get_enrichment_stats()
│   │
│   └── nexdata/ (v1.0.0)
│       ├── models/
│       │   ├── gscat.py ✅ (705 bytes record)
│       │   └── barcode.py ✅ (50 bytes record)
│       ├── repositories/
│       │   ├── gscat_repository.py ✅
│       │   └── barcode_repository.py ✅
│       └── btrieve/
│           └── btrieve_client.py ✅
│
└── scripts/
    ├── 01_migrate_invoice_shared_v2.3.py
    ├── 02_fix_utils_init.py
    ├── 03_deploy_v2.3_magerstav.ps1
    └── 04_deploy_enrichment_v2.4.py (NEW) 🚧
```

---

## DATABASE SCHEMA

### PostgreSQL: invoice_items_pending (REAL SCHEMA)

```sql
CREATE TABLE invoice_items_pending (
    -- Primary
    id INTEGER PRIMARY KEY,
    invoice_id INTEGER REFERENCES invoices_pending(id),
    line_number INTEGER,
    
    -- ORIGINAL (from PDF) ✅
    original_name VARCHAR,
    original_quantity NUMERIC,
    original_unit VARCHAR,
    original_price_per_unit NUMERIC,
    original_ean VARCHAR,
    original_vat_rate NUMERIC,
    
    -- EDITED (manual corrections) ✅
    edited_name VARCHAR,
    edited_mglst_code INTEGER,
    edited_price_buy NUMERIC,
    edited_price_sell NUMERIC,
    edited_discount_percent NUMERIC,
    edited_ean VARCHAR,
    edited_at TIMESTAMP,
    was_edited BOOLEAN,
    
    -- FINAL (computed) ✅
    final_price_buy NUMERIC,
    final_price_sell NUMERIC,
    
    -- NEX GENESIS (v2.4 target) 🚧
    nex_gs_code INTEGER,           -- GSCAT.gs_code
    nex_plu INTEGER,               -- Alternative code
    nex_name VARCHAR,              -- GSCAT.gs_name
    nex_category INTEGER,          -- GSCAT.mglst_code
    nex_barcode_created BOOLEAN,   -- Flag
    in_nex BOOLEAN,                -- Product exists in NEX
    
    -- VALIDATION ✅
    validation_status VARCHAR,
    validation_message TEXT
);
```

### NEX Genesis: GSCAT.BTR

```python
@dataclass
class GSCATRecord:
    # Primary key
    gs_code: int                # Product code (PLU)
    
    # Product info
    gs_name: str               # Product name
    gs_name2: str              # Alternative name
    gs_short_name: str         # Short name
    
    # Classification
    mglst_code: int            # Category code
    
    # Measurement
    unit: str                  # Unit (ks, kg, l)
    unit_coef: Decimal         # Unit coefficient
    
    # Pricing
    price_buy: Decimal         # Buy price
    price_sell: Decimal        # Sell price
    vat_rate: Decimal          # VAT rate (%)
    
    # Stock
    stock_min: Decimal
    stock_max: Decimal
    stock_current: Decimal
    
    # Status
    active: bool
    discontinued: bool
    
    # Supplier
    supplier_code: int
    supplier_item_code: str
```

### NEX Genesis: BARCODE.BTR

```python
@dataclass
class BarcodeRecord:
    gs_code: int               # Product code (FK → GSCAT)
    bar_code: str              # EAN code (up to 15 chars)
    
    # Audit
    mod_user: str
    mod_date: datetime
    mod_time: datetime
```

---

## IMPLEMENTATION DETAILS

### Phase 1: PostgreSQL Methods (6h)

**Súbor:** `packages/nex-shared/database/postgres_staging.py`

**New Methods:**

```python
def get_pending_enrichment_items(
    self, 
    invoice_id: Optional[int] = None,
    limit: int = 100
) -> List[Dict]:
    """
    Get items needing enrichment
    WHERE in_nex IS NULL OR in_nex = FALSE
    """
    
def update_nex_enrichment(
    self,
    item_id: int,
    gscat_record: GSCATRecord,
    matched_by: str = 'ean'
) -> bool:
    """
    Update item with NEX data
    SET nex_gs_code, nex_name, nex_category, in_nex = TRUE
    """
    
def mark_no_match(
    self,
    item_id: int,
    reason: str
) -> bool:
    """
    Mark as not found
    SET in_nex = FALSE, validation_status = 'needs_review'
    """
    
def get_enrichment_stats(
    self,
    invoice_id: Optional[int] = None
) -> Dict:
    """
    Get enrichment statistics
    COUNT enriched/not_found/pending
    """
```

**Testing:**
```python
# tests/unit/test_postgres_staging_enrichment.py
def test_get_pending_enrichment_items()
def test_update_nex_enrichment()
def test_mark_no_match()
def test_get_enrichment_stats()
```

---

### Phase 2: ProductMatcher (11h)

**Súbor:** `apps/supplier-invoice-loader/src/business/product_matcher.py`

**Class Structure:**

```python
class ProductMatcher:
    """Match invoice items with NEX Genesis products"""
    
    def __init__(self, nex_data_path: str):
        # Load GSCAT and BARCODE into memory cache
        self._products_cache: Dict[int, GSCATRecord]
        self._barcode_cache: Dict[str, int]  # ean → gs_code
    
    def match_item(
        self, 
        item_data: Dict,
        min_confidence: float = 0.6
    ) -> MatchResult:
        """
        Main matching logic
        
        Strategy:
        1. Try EAN match (confidence 0.95)
        2. Try name match (confidence 0.6-0.9)
        3. Return no match (confidence 0.0)
        """
    
    def _match_by_ean(self, ean: str) -> MatchResult:
        """BARCODE.bar_code → GSCAT.gs_code"""
    
    def _match_by_name(
        self, 
        name: str, 
        min_confidence: float
    ) -> MatchResult:
        """Fuzzy match using rapidfuzz"""
    
    def _normalize_text(self, text: str) -> str:
        """unidecode + lowercase + clean"""
    
    def _calculate_similarity(
        self, 
        text1: str, 
        text2: str
    ) -> float:
        """fuzz.token_set_ratio() / 100"""
```

**Dependencies:**
```txt
rapidfuzz>=3.0.0
unidecode>=1.3.0
```

**Testing:**
```python
# tests/unit/test_product_matcher.py
def test_match_by_ean_found()
def test_match_by_ean_not_found()
def test_match_by_name_exact()
def test_match_by_name_fuzzy()
def test_normalize_text()
def test_calculate_similarity()
```

---

### Phase 3: API Endpoints (6h)

**Súbor:** `apps/supplier-invoice-loader/main.py`

**New Endpoints:**

```python
@app.post("/enrich/invoice/{invoice_id}")
async def enrich_invoice_items(
    invoice_id: int,
    min_confidence: float = 0.6,
    api_key: str = Depends(verify_api_key)
):
    """
    Enrich all items of invoice
    
    Process:
    1. Get pending items
    2. For each: match_item()
    3. Update or mark_no_match
    4. Return stats
    """

@app.get("/enrich/stats/{invoice_id}")
async def get_enrichment_stats(
    invoice_id: int,
    api_key: str = Depends(verify_api_key)
):
    """Get enrichment statistics"""

@app.get("/pending/items")
async def get_pending_items(
    limit: int = 100,
    invoice_id: Optional[int] = None,
    api_key: str = Depends(verify_api_key)
):
    """List items pending enrichment"""
```

**Startup Initialization:**
```python
# Global matcher
product_matcher: Optional[ProductMatcher] = None

@app.on_event("startup")
async def startup_event():
    global product_matcher
    
    if config.NEX_GENESIS_ENABLED:
        product_matcher = ProductMatcher(config.NEX_DATA_PATH)
```

**Testing:**
```python
# tests/integration/test_enrichment_api.py
def test_enrich_invoice_success()
def test_enrich_invoice_partial()
def test_enrich_stats()
def test_get_pending_items()
```

---

### Phase 4: Deployment (4h)

**Script:** `scripts/04_deploy_enrichment_v2.4.py`

```python
def main():
    # 1. Install dependencies
    pip install rapidfuzz unidecode
    
    # 2. Update nex-shared
    pip install -e packages/nex-shared
    
    # 3. Test imports
    from nex_shared.database import PostgresStagingClient
    from src.business.product_matcher import ProductMatcher
    
    # 4. Verify config
    check NEX_DATA_PATH, PostgreSQL connection
    
    # 5. Git operations
    git add .
    git commit -m "feat: Implement NEX Genesis enrichment v2.4"
    git tag v2.4
    git push
```

**Deployment Steps:**
```bash
# Development
cd C:\Development\nex-automat
python scripts/04_deploy_enrichment_v2.4.py

# Production (Magerstav)
cd C:\Deployment\nex-automat
Stop-Service NEXAutomat
git pull origin main
python scripts/04_deploy_enrichment_v2.4.py
Start-Service NEXAutomat

# Verify
Invoke-WebRequest http://localhost:8000/health
Invoke-WebRequest http://localhost:8000/pending/items
```

---

## CONFIGURATION

### Config Updates (v2.4)

**Súbor:** `config/config.yaml`

```yaml
# NEX Genesis Integration (NEW)
nex_genesis:
  enabled: true
  data_path: "C:/NEX/YEARACT/STORES"
  
  # Btrieve files
  files:
    gscat: "GSCAT.BTR"
    barcode: "BARCODE.BTR"
    mglst: "MGLST.BTR"
  
  # Matching parameters
  matching:
    min_confidence: 0.6
    fuzzy_enabled: true
```

**Súbor:** `src/utils/config.py`

```python
# NEX Genesis config (NEW)
NEX_GENESIS_ENABLED = os.getenv(
    'NEX_GENESIS_ENABLED', 
    'true'
).lower() == 'true'

NEX_DATA_PATH = os.getenv(
    'NEX_DATA_PATH', 
    'C:/NEX/YEARACT/STORES'
)
```

---

## TESTING STRATEGY

### Test Coverage Goals

| Component | Target | Priority |
|-----------|--------|----------|
| PostgreSQL methods | 90%+ | HIGH |
| ProductMatcher | 85%+ | HIGH |
| API endpoints | 80%+ | MEDIUM |
| Integration | 70%+ | MEDIUM |

### Manual Testing Checklist

```
Phase 1 Testing:
[ ] Can query pending items
[ ] Can update enrichment
[ ] Can mark no match
[ ] Stats are correct

Phase 2 Testing:
[ ] EAN match works
[ ] Name match works
[ ] Text normalization OK
[ ] Similarity calculation OK

Phase 3 Testing:
[ ] Can enrich via API
[ ] Stats endpoint works
[ ] Pending endpoint works
[ ] Integration flow complete

Phase 4 Testing:
[ ] Service starts
[ ] Health check OK
[ ] Can process real invoice
[ ] Match rate > 70%
```

---

## KNOWN ISSUES & RISKS

### Technical Risks

**1. Fuzzy Matching Accuracy** ⚠️ MEDIUM
- **Risk:** Low match rate, too many false positives
- **Mitigation:** 
  - Confidence threshold 0.7
  - Manual review 0.5-0.7
  - Log all matches

**2. Btrieve Performance** ⚠️ MEDIUM
- **Risk:** Slow get_all() on large tables
- **Mitigation:**
  - In-memory cache
  - Load on startup
  - Periodic refresh

**3. Data Quality** ⚠️ HIGH
- **Risk:** Missing/incorrect EAN codes
- **Mitigation:**
  - Fallback to name matching
  - Manual review workflow
  - Training data collection

---

## MONITORING & METRICS

### Key Metrics (v2.4)

```python
# Prometheus metrics
app_enrichment_total
app_enrichment_success
app_enrichment_failed
app_match_method_counts {method="ean|name|none"}
app_match_confidence_avg
app_enrichment_time_seconds
```

### Alerts

```
- enrichment_failed_rate > 20%
- match_confidence_avg < 0.6
- enrichment_time > 10s
- btrieve_connection_errors
```

---

## NEXT STEPS

### Immediate Actions

1. **Create Feature Branch**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/enrichment-v2.4
   ```

2. **Start Phase 1**
   ```bash
   cd packages/nex-shared
   # Edit database/postgres_staging.py
   # Add new methods
   # Write unit tests
   ```

3. **Install Dependencies**
   ```bash
   pip install rapidfuzz>=3.0.0 unidecode>=1.3.0
   ```

### Daily Goals

**Day 1:** Phase 1 complete + tested  
**Day 2:** Phase 2 complete + tested  
**Day 3:** Phase 3 complete + tested  
**Day 4:** Phase 4 deployment + verification

---

## REFERENCES

### Documentation
- Implementation Plan v2.4 (full details)
- PostgreSQL Schema (real schema)
- NEX Genesis Models (GSCAT, BARCODE)

### Key Contacts
- **Zákazník:** Mágerstav s.r.o.
- **Deployment:** C:\Deployment\nex-automat (Magerstav)

---

**Session Notes Created:** 2025-12-08  
**Ready for:** Phase 1 Implementation  
**Estimated Duration:** 4 pracovné dni  
**Status:** 🚧 Ready to start coding