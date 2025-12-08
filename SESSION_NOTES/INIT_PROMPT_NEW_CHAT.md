# INIT PROMPT - NEX Automat v2.4 Implementation

## PROJECT CONTEXT

**Projekt:** nex-automat  
**Typ:** Monorepo - Multi-customer SaaS for automated invoice processing  
**Development:** `C:\Development\nex-automat`  
**Deployment:** `C:\Deployment\nex-automat`  
**Python:** 3.13.7 (venv32)  
**Git Branch:** develop → feature/enrichment-v2.4  
**Current Version:** v2.3 (production) → v2.4 (in development)

---

## CURRENT STATUS

### Production (Magerstav)
- **Version:** v2.3 ✅ Deployed
- **Service:** NEXAutomat (Running)
- **API:** http://localhost:8000
- **Health:** http://localhost:8000/health → 200 OK

### Development
- **Version:** v2.4 🚧 Ready for Phase 1
- **Branch:** feature/enrichment-v2.4 (to be created)
- **Task:** Implement NEX Genesis product enrichment

---

## MISSION: NEX Genesis Enrichment v2.4

### Problem Statement
Invoice items in PostgreSQL have **EMPTY NEX Genesis fields**:
- `nex_gs_code` = NULL
- `nex_name` = NULL
- `nex_category` = NULL
- `in_nex` = NULL

**Impact:** No automatic product matching, all manual work

### Solution Overview
Implement automatic product matching between invoice items and NEX Genesis catalog:

1. **Match by EAN** (BARCODE → GSCAT) - highest confidence
2. **Match by Name** (fuzzy matching) - medium confidence
3. **Manual fallback** - low/no confidence

### Success Criteria
- ✅ Enrichment API working
- ✅ Match rate > 70% (EAN + Name)
- ✅ Confidence tracking
- ✅ Manual review workflow

---

## IMPLEMENTATION PLAN v2.4

### Phase 1: Database Layer (6h) 🎯 START HERE

**Súbor:** `packages/nex-shared/database/postgres_staging.py`

**Implementovať:**
```python
def get_pending_enrichment_items(
    self, 
    invoice_id: Optional[int] = None,
    limit: int = 100
) -> List[Dict]:
    """
    Get items WHERE in_nex IS NULL OR in_nex = FALSE
    
    Returns list of items with:
    - id, invoice_id, line_number
    - original_name, original_ean
    - original_quantity, original_unit
    - original_price_per_unit, original_vat_rate
    - edited_name, edited_ean
    - was_edited
    - nex_gs_code, in_nex
    """
    cursor = self._conn.cursor()
    
    if invoice_id:
        cursor.execute("""
            SELECT 
                id, invoice_id, line_number,
                original_name, original_ean,
                original_quantity, original_unit,
                original_price_per_unit, original_vat_rate,
                edited_name, edited_ean,
                was_edited,
                nex_gs_code, in_nex
            FROM invoice_items_pending
            WHERE invoice_id = %s
              AND (in_nex IS NULL OR in_nex = FALSE)
            ORDER BY line_number
            LIMIT %s
        """, (invoice_id, limit))
    else:
        cursor.execute("""
            SELECT 
                id, invoice_id, line_number,
                original_name, original_ean,
                original_quantity, original_unit,
                original_price_per_unit, original_vat_rate,
                edited_name, edited_ean,
                was_edited,
                nex_gs_code, in_nex
            FROM invoice_items_pending
            WHERE in_nex IS NULL OR in_nex = FALSE
            ORDER BY invoice_id, line_number
            LIMIT %s
        """, (limit,))
    
    rows = cursor.fetchall()
    cursor.close()
    
    columns = [
        'id', 'invoice_id', 'line_number',
        'original_name', 'original_ean',
        'original_quantity', 'original_unit',
        'original_price_per_unit', 'original_vat_rate',
        'edited_name', 'edited_ean',
        'was_edited',
        'nex_gs_code', 'in_nex'
    ]
    
    return [dict(zip(columns, row)) for row in rows]


def update_nex_enrichment(
    self,
    item_id: int,
    gscat_record,  # GSCATRecord from nexdata
    matched_by: str = 'ean'
) -> bool:
    """
    Update item with NEX Genesis data
    
    Args:
        item_id: Item ID
        gscat_record: GSCATRecord with product data
        matched_by: 'ean', 'name', 'manual'
    """
    cursor = self._conn.cursor()
    
    cursor.execute("""
        UPDATE invoice_items_pending SET
            nex_gs_code = %s,
            nex_plu = %s,
            nex_name = %s,
            nex_category = %s,
            in_nex = TRUE,
            nex_barcode_created = FALSE,
            validation_status = %s,
            validation_message = %s
        WHERE id = %s
    """, (
        gscat_record.gs_code,
        gscat_record.gs_code,
        gscat_record.gs_name,
        gscat_record.mglst_code,
        'matched',
        f'Auto-matched by {matched_by}',
        item_id
    ))
    
    success = cursor.rowcount > 0
    cursor.close()
    return success


def mark_no_match(
    self,
    item_id: int,
    reason: str = 'No matching product found'
) -> bool:
    """Mark item as not found in NEX"""
    cursor = self._conn.cursor()
    
    cursor.execute("""
        UPDATE invoice_items_pending SET
            in_nex = FALSE,
            validation_status = 'needs_review',
            validation_message = %s
        WHERE id = %s
    """, (reason, item_id))
    
    success = cursor.rowcount > 0
    cursor.close()
    return success


def get_enrichment_stats(
    self,
    invoice_id: Optional[int] = None
) -> Dict:
    """Get enrichment statistics"""
    cursor = self._conn.cursor()
    
    if invoice_id:
        cursor.execute("""
            SELECT 
                COUNT(*) FILTER (WHERE in_nex = TRUE) as enriched,
                COUNT(*) FILTER (WHERE in_nex = FALSE) as not_found,
                COUNT(*) FILTER (WHERE in_nex IS NULL) as pending,
                COUNT(*) as total
            FROM invoice_items_pending
            WHERE invoice_id = %s
        """, (invoice_id,))
    else:
        cursor.execute("""
            SELECT 
                COUNT(*) FILTER (WHERE in_nex = TRUE) as enriched,
                COUNT(*) FILTER (WHERE in_nex = FALSE) as not_found,
                COUNT(*) FILTER (WHERE in_nex IS NULL) as pending,
                COUNT(*) as total
            FROM invoice_items_pending
        """)
    
    row = cursor.fetchone()
    cursor.close()
    
    return {
        'enriched': row[0] or 0,
        'not_found': row[1] or 0,
        'pending': row[2] or 0,
        'total': row[3] or 0
    }
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

**Dependencies:**
```bash
pip install rapidfuzz>=3.0.0 unidecode>=1.3.0
```

**Implementovať:**
```python
from dataclasses import dataclass
from typing import Optional, List, Tuple, Dict

from rapidfuzz import fuzz
from unidecode import unidecode

from nexdata.repositories.gscat_repository import GSCATRepository
from nexdata.repositories.barcode_repository import BARCODERepository


@dataclass
class MatchResult:
    product: Optional['GSCATRecord']
    confidence: float  # 0.0 - 1.0
    method: str  # 'ean', 'name', 'none'
    alternatives: List[Tuple['GSCATRecord', float]] = None
    
    def __post_init__(self):
        if self.alternatives is None:
            self.alternatives = []


class ProductMatcher:
    """Match invoice items with NEX Genesis products"""
    
    def __init__(self, nex_data_path: str):
        self.gscat_repo = GSCATRepository(nex_data_path)
        self.barcode_repo = BARCODERepository(nex_data_path)
        
        # Load into memory
        self._products_cache: Dict[int, GSCATRecord] = {}
        self._barcode_cache: Dict[str, int] = {}
        self._load_caches()
    
    def _load_caches(self):
        for product in self.gscat_repo.get_all():
            self._products_cache[product.gs_code] = product
        
        for barcode in self.barcode_repo.get_all():
            self._barcode_cache[barcode.bar_code.strip()] = barcode.gs_code
    
    def match_item(
        self, 
        item_data: Dict,
        min_confidence: float = 0.6
    ) -> MatchResult:
        """Main matching logic"""
        name = item_data.get('edited_name') or item_data.get('original_name', '')
        ean = item_data.get('edited_ean') or item_data.get('original_ean', '')
        
        # Try EAN
        if ean and ean.strip():
            result = self._match_by_ean(ean.strip())
            if result.product:
                return result
        
        # Try name
        if name and name.strip():
            result = self._match_by_name(name.strip(), min_confidence)
            if result.product:
                return result
        
        # No match
        return MatchResult(product=None, confidence=0.0, method='none')
    
    def _match_by_ean(self, ean: str) -> MatchResult:
        ean_normalized = ean.replace(' ', '').replace('-', '').strip()
        gs_code = self._barcode_cache.get(ean_normalized)
        
        if gs_code:
            product = self._products_cache.get(gs_code)
            if product:
                return MatchResult(
                    product=product,
                    confidence=0.95,
                    method='ean'
                )
        
        return MatchResult(product=None, confidence=0.0, method='none')
    
    def _match_by_name(
        self, 
        name: str, 
        min_confidence: float
    ) -> MatchResult:
        name_normalized = self._normalize_text(name)
        
        matches = []
        for gs_code, product in self._products_cache.items():
            if product.discontinued:
                continue
            
            product_name = self._normalize_text(product.gs_name)
            score = self._calculate_similarity(name_normalized, product_name)
            
            if score >= min_confidence:
                matches.append((product, score))
        
        if not matches:
            return MatchResult(product=None, confidence=0.0, method='none')
        
        matches.sort(key=lambda x: x[1], reverse=True)
        best_product, best_score = matches[0]
        
        return MatchResult(
            product=best_product,
            confidence=best_score,
            method='name',
            alternatives=matches[1:6]
        )
    
    def _normalize_text(self, text: str) -> str:
        if not text:
            return ""
        
        text = unidecode(text)
        text = text.lower()
        text = ''.join(c if c.isalnum() or c.isspace() else ' ' for c in text)
        text = ' '.join(text.split())
        
        return text
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        score = fuzz.token_set_ratio(text1, text2)
        return score / 100.0
```

---

### Phase 3: API Endpoints (6h)

**Súbor:** `apps/supplier-invoice-loader/main.py`

**Pridať:**
```python
# Global matcher
product_matcher: Optional[ProductMatcher] = None

@app.on_event("startup")
async def startup_event():
    global product_matcher
    # ... existing code ...
    
    if config.NEX_GENESIS_ENABLED:
        try:
            product_matcher = ProductMatcher(config.NEX_DATA_PATH)
            print(f"[OK] ProductMatcher initialized")
        except Exception as e:
            print(f"[WARN] ProductMatcher init failed: {e}")

@app.post("/enrich/invoice/{invoice_id}")
async def enrich_invoice_items(
    invoice_id: int,
    min_confidence: float = 0.6,
    api_key: str = Depends(verify_api_key)
):
    if not product_matcher:
        raise HTTPException(503, "ProductMatcher not initialized")
    
    pg_config = {
        'host': config.POSTGRES_HOST,
        'port': config.POSTGRES_PORT,
        'database': config.POSTGRES_DATABASE,
        'user': config.POSTGRES_USER,
        'password': config.POSTGRES_PASSWORD
    }
    
    stats = {
        'invoice_id': invoice_id,
        'total': 0,
        'matched': 0,
        'matched_ean': 0,
        'matched_name': 0,
        'not_found': 0,
        'errors': 0
    }
    
    with PostgresStagingClient(pg_config) as pg_client:
        items = pg_client.get_pending_enrichment_items(invoice_id=invoice_id)
        stats['total'] = len(items)
        
        for item in items:
            try:
                match_result = product_matcher.match_item(item, min_confidence)
                
                if match_result.product:
                    pg_client.update_nex_enrichment(
                        item['id'],
                        match_result.product,
                        match_result.method
                    )
                    stats['matched'] += 1
                    if match_result.method == 'ean':
                        stats['matched_ean'] += 1
                    else:
                        stats['matched_name'] += 1
                else:
                    pg_client.mark_no_match(item['id'])
                    stats['not_found'] += 1
            except Exception as e:
                logger.error(f"Error: {e}")
                stats['errors'] += 1
    
    return {
        'success': True,
        'message': f"Enriched {stats['matched']}/{stats['total']} items",
        'statistics': stats
    }

@app.get("/enrich/stats/{invoice_id}")
async def get_enrichment_stats(...):
    # Implementation similar to above

@app.get("/pending/items")
async def get_pending_items(...):
    # Implementation similar to above
```

---

### Phase 4: Deployment (4h)

**Script:** `scripts/04_deploy_enrichment_v2.4.py`

```python
import subprocess
import sys
from pathlib import Path

def main():
    print("=" * 60)
    print("Deploying v2.4 - NEX Genesis Enrichment")
    print("=" * 60)
    
    # 1. Dependencies
    print("\n[1/4] Installing dependencies...")
    subprocess.run([
        sys.executable, '-m', 'pip', 'install',
        'rapidfuzz>=3.0.0', 'unidecode>=1.3.0'
    ])
    
    # 2. Update nex-shared
    print("\n[2/4] Updating nex-shared...")
    subprocess.run([
        sys.executable, '-m', 'pip', 'install', '-e',
        'packages/nex-shared'
    ])
    
    # 3. Test
    print("\n[3/4] Testing imports...")
    from nex_shared.database import PostgresStagingClient
    from src.business.product_matcher import ProductMatcher
    print("✅ Imports OK")
    
    # 4. Verify
    print("\n[4/4] Verifying...")
    from src.utils import config
    print(f"PostgreSQL: {config.POSTGRES_HOST}")
    print(f"NEX Data: {config.NEX_DATA_PATH}")
    
    print("\n✅ Deployment complete!")

if __name__ == '__main__':
    main()
```

---

## POSTGRESQL SCHEMA (REAL)

```sql
CREATE TABLE invoice_items_pending (
    id INTEGER PRIMARY KEY,
    invoice_id INTEGER,
    line_number INTEGER,
    
    -- FROM PDF ✅
    original_name VARCHAR,
    original_quantity NUMERIC,
    original_unit VARCHAR,
    original_price_per_unit NUMERIC,
    original_ean VARCHAR,
    original_vat_rate NUMERIC,
    
    -- MANUAL EDITS ✅
    edited_name VARCHAR,
    edited_mglst_code INTEGER,
    edited_price_buy NUMERIC,
    edited_price_sell NUMERIC,
    edited_discount_percent NUMERIC,
    edited_ean VARCHAR,
    edited_at TIMESTAMP,
    was_edited BOOLEAN,
    
    -- COMPUTED ✅
    final_price_buy NUMERIC,
    final_price_sell NUMERIC,
    
    -- NEX GENESIS 🎯 TARGET
    nex_gs_code INTEGER,
    nex_plu INTEGER,
    nex_name VARCHAR,
    nex_category INTEGER,
    nex_barcode_created BOOLEAN,
    in_nex BOOLEAN,
    
    -- VALIDATION ✅
    validation_status VARCHAR,
    validation_message TEXT
);
```

---

## NEX GENESIS DATA MODELS

### GSCAT (Products)
```python
@dataclass
class GSCATRecord:
    gs_code: int              # Primary key
    gs_name: str              # Product name
    mglst_code: int           # Category
    unit: str                 # Unit (ks, kg)
    price_buy: Decimal        # Buy price
    price_sell: Decimal       # Sell price
    vat_rate: Decimal         # VAT %
    active: bool
    discontinued: bool
```

### BARCODE (EAN codes)
```python
@dataclass
class BarcodeRecord:
    gs_code: int              # FK → GSCAT
    bar_code: str             # EAN code
```

---

## TESTING CHECKLIST

### Phase 1 ✅
- [ ] get_pending_enrichment_items() works
- [ ] update_nex_enrichment() works
- [ ] mark_no_match() works
- [ ] get_enrichment_stats() works
- [ ] Unit tests passing

### Phase 2 ✅
- [ ] ProductMatcher loads caches
- [ ] EAN matching works
- [ ] Name matching works
- [ ] Text normalization OK
- [ ] Unit tests passing

### Phase 3 ✅
- [ ] Enrichment endpoint works
- [ ] Stats endpoint works
- [ ] Pending items endpoint works
- [ ] Integration tests passing

### Phase 4 ✅
- [ ] Deployed to production
- [ ] Service running
- [ ] Health check OK
- [ ] Real invoice enriched
- [ ] Match rate > 70%

---

## WORKFLOW DIAGRAM

```
POST /invoice
    ↓
PostgreSQL: invoice_items_pending
    original_* ✅
    nex_* ❌ NULL
    ↓
POST /enrich/invoice/{id}
    ↓
ProductMatcher.match_item()
    ├─ Try EAN → BARCODE → GSCAT
    │  └─ confidence 0.95
    ├─ Try Name → fuzzy → GSCAT
    │  └─ confidence 0.6-0.9
    └─ No match
       └─ confidence 0.0
    ↓
PostgresStagingClient
    ├─ update_nex_enrichment()
    │  └─ nex_gs_code ✅
    │     nex_name ✅
    │     in_nex = TRUE ✅
    └─ mark_no_match()
       └─ in_nex = FALSE
          validation_status = 'needs_review'
```

---

## CONFIGURATION

### NEX Genesis Config
```yaml
# config/config.yaml
nex_genesis:
  enabled: true
  data_path: "C:/NEX/YEARACT/STORES"
  matching:
    min_confidence: 0.6
```

### Environment
```python
# src/utils/config.py
NEX_GENESIS_ENABLED = os.getenv('NEX_GENESIS_ENABLED', 'true')
NEX_DATA_PATH = os.getenv('NEX_DATA_PATH', 'C:/NEX/YEARACT/STORES')
```

---

## CRITICAL RULES

### Workflow
1. **Development → Git → Deployment**
2. **NIKDY nerobiť zmeny priamo v Deployment**
3. Všetky zmeny cez numbered scripts

### Git Operations
```bash
git add .
git commit -m "feat: Phase X - description"
git push origin feature/enrichment-v2.4

# After Phase 4:
git tag v2.4
git checkout main
git merge feature/enrichment-v2.4
git push origin main --tags
```

### Testing
```bash
# Development
cd C:\Development\nex-automat
python -m pytest tests/

# Production
cd C:\Deployment\nex-automat
Restart-Service NEXAutomat
Invoke-WebRequest http://localhost:8000/health
```

---

## SUCCESS METRICS

### Performance
- Enrichment time: < 5s per invoice
- Match rate: > 70% (EAN + Name)
- API response: < 2s

### Quality
- False positive rate: < 5%
- Manual review needed: < 30%
- Confidence avg: > 0.75

---

## RISK MITIGATION

### Low Match Rate
- **If < 50%:** Review EAN data quality
- **Solution:** Collect training data, improve fuzzy matching

### Performance Issues
- **If > 10s:** Cache not working
- **Solution:** Verify cache loading, add indexes

### False Positives
- **If > 10%:** Confidence threshold too low
- **Solution:** Raise to 0.7, add manual review

---

## NEXT IMMEDIATE ACTION

```bash
# 1. Create feature branch
cd C:\Development\nex-automat
git checkout develop
git pull origin develop
git checkout -b feature/enrichment-v2.4

# 2. Install dependencies
pip install rapidfuzz>=3.0.0 unidecode>=1.3.0

# 3. Start Phase 1
cd packages/nex-shared
# Edit database/postgres_staging.py
# Add 4 new methods
# Write unit tests

# 4. Test
python -m pytest tests/unit/test_postgres_staging_enrichment.py
```

---

## SUPPORT INFORMATION

**Customer:** Mágerstav s.r.o.  
**Deployment:** C:\Deployment\nex-automat  
**Service:** NEXAutomat (Windows Service)  
**PostgreSQL:** localhost:5432/invoice_staging  
**NEX Genesis:** C:\NEX\YEARACT\STORES\

---

**Init Prompt Created:** 2025-12-08  
**Version:** v2.4 Implementation  
**Phase:** Ready for Phase 1  
**Estimated:** 4 pracovné dni (27h)  
**Status:** 🚀 Ready to start