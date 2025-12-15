# INIT PROMPT - NEX Automat: .md-old Migration (Batch 6)

**Projekt:** nex-automat  
**Úloha:** Database table docs migration (batch archive approach)  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** https://claude.ai/chat/[CURRENT_CHAT_URI]  
**Status:** ✅ Batch 5 complete (32/60 súborov), **HALFWAY!** 🎯

---

## ⚠️ KRITICKÉ: COLLABORATION RULES

**MUSÍŠ dodržiavať 22 pravidiel z memory_user_edits!**

Kľúčové pravidlá pre túto session:
- **Rule #7:** CRITICAL artifacts pre všetky dokumenty/kód
- **Rule #8:** Step-by-step, confirmation pred pokračovaním
- **Rule #20:** "novy chat" = 4 artifacts (ARCHIVE, NOTES, INIT, commit)
- **Rule #5:** Slovak language, presná terminológia projektov
- **Rule #22:** Na začiatku každého chatu skontrolovať všetky pravidlá

---

## 📋 ČO SME DOKONČILI V PREVIOUS SESSION (Batch 5)

### ✅ Migrované Dokumenty (7 → 32 total)

**Database Index Files (7):**

1. **INDEX.md-old** (6 KB) - docs/architecture/database/
   - Action: DELETE
   - Reason: Replaced by new 00_DATABASE_INDEX.md
   - Script: 25_delete_old_database_index.py

2. **catalogs/INDEX.md-old** (6.7 KB)
   - Action: RELOCATE → CATALOGS_REFERENCE.md
   - Content: Products + Partners overview (12 docs, 16 tables)
   - Script: 26_relocate_catalogs_index.py

3. **catalogs/partners/INDEX.md-old** (7.5 KB)
   - Action: RELOCATE → PARTNERS_REFERENCE.md
   - Content: 7 docs, 9 tables (100% complete)
   - Script: 27_relocate_partners_index.py

4. **catalogs/products/INDEX.md-old** (5.7 KB)
   - Action: RELOCATE → PRODUCTS_REFERENCE.md
   - Content: 5 docs, 7 tables (100% complete)
   - Script: 28_relocate_products_index.py

5. **sales/INDEX.md-old** (8.1 KB)
   - Action: RELOCATE → SALES_REFERENCE.md
   - Content: Price lists, discount system, business logic
   - Script: 29_relocate_sales_index.py

6. **stock/INDEX.md-old** (0 KB - empty!)
   - Action: CREATE PLACEHOLDER → STOCK_REFERENCE.md
   - Content: Placeholder for future stock documentation
   - Script: 30_delete_empty_stock_index.py (renamed)

7. **stock/cards/INDEX.md-old** (20.4 KB)
   - Action: RELOCATE → STOCK_CARDS_REFERENCE.md
   - Content: Complete FIFO system (3 tables, queries, implementation)
   - Script: 31_relocate_stock_cards_index.py

### 📜 Scripts Vytvorené (7)

- `25_delete_old_database_index.py`
- `26_relocate_catalogs_index.py`
- `27_relocate_partners_index.py`
- `28_relocate_products_index.py`
- `29_relocate_sales_index.py`
- `30_delete_empty_stock_index.py`
- `31_relocate_stock_cards_index.py`

### 📊 Progress

**Dokončené:** 32/60 súborov (53.3%) - **🎯 HALFWAY MILESTONE!**  
**Zostáva:** 28 súborov

**By Category:**
- ✅ Deployment: 11/11 (100%) - **COMPLETE**
- ✅ Database General: 4/4 (100%) - **COMPLETE**
- ✅ Database Indexes: 7/7 (100%) - **COMPLETE**
- ⏳ Database Tables: 0/28 (0%) - **NEXT (THIS SESSION)**
- ⏳ Strategic: 0/2 (0%)
- ⏳ Development: 0/1 (0%)
- ⏳ Other: 0/4 (0%)

---

## 🎯 ČO TREBA UROBIŤ TERAZ

### Priority 1: Git Commit (PRVÉ!)

```powershell
# Commit batch 5 changes
git add docs/ SESSION_NOTES/ scripts/
git commit -m "docs: Migrate .md-old batch 5 - database reference docs"
git push origin develop
```

### Priority 2: Database Table Docs Migration (Batch 6)

**Files:** 28 .md-old table documentation files

**Type:** Btrieve → PostgreSQL mapping documentation  
**Status:** Historical reference (migration already completed)  
**Quality:** Very detailed (8-40 KB each)

---

## 📂 DATABASE TABLE DOCS (28 súborov)

### Catalogs - Partners (9 súborov)

1. **BANKLST-bank_catalog.md-old** (10.7 KB)
2. **PAB-partner_catalog.md-old** (39.9 KB) ⚠️ LARGE
3. **PABACC-partner_catalog_bank_accounts.md-old** (12.6 KB)
4. **PACNCT-partner_catalog_contacts.md-old** (22.8 KB)
5. **PAGLST-partner_categories.md-old** (14.9 KB)
6. **PANOTI-partner_catalog_texts.md-old** (15.4 KB)
7. **PASUBC-partner_catalog_facilities.md-old** (18.0 KB)
8. **PAYLST-payment_methods.md-old** (8.3 KB)
9. **TRPLST-transport_methods.md-old** (8.6 KB)

### Catalogs - Products (5 súborov)

10. **BARCODE-product_catalog_identifiers.md-old** (24.2 KB)
11. **FGLST-product_categories.md-old** (16.1 KB)
12. **GSCAT-product_catalog.md-old** (20.7 KB)
13. **MGLST-product_categories.md-old** (17.4 KB)
14. **SGLST-product_categories.md-old** (20.1 KB)

### Stock Management (7 súborov)

15. **FIF-stock_card_fifos.md-old** (28.5 KB)
16. **STK-stock_cards.md-old** (38.5 KB) ⚠️ LARGE
17. **STKLST-stocks.md-old** (20.4 KB)
18. **STM-stock_card_movements.md-old** (35.6 KB) ⚠️ LARGE
19. **WRILST-facilities.md-old** (17.9 KB)
20. **TSH-supplier_delivery_heads.md-old** (25.4 KB)
21. **TSI-supplier_delivery_items.md-old** (29.7 KB)

### Accounting (3 súbory)

22. **ISH-supplier_invoice_heads.md-old** (34.8 KB)
23. **ISI-supplier_invoice_items.md-old** (29.6 KB)
24. **PAYJRN-payment_journal.md-old** (25.8 KB)

### Sales (1 súbor)

25. **PLSnnnnn-price_list_items.md-old** (20.5 KB)

---

## 💡 RECOMMENDED STRATEGY: BATCH ARCHIVE

### Prečo Batch Approach?

**Dôvody:**
1. ✅ **Všetky súbory rovnakého typu** - Btrieve → PostgreSQL mapping
2. ✅ **Historical reference** - Migration už complete
3. ✅ **Similar structure** - SQL schemas, field mappings, queries
4. ✅ **Time efficiency** - 1 script namiesto 28× scriptov
5. ✅ **Consistent treatment** - Všetky do archive category

**Alternative:**
- ❌ Individual processing = 28× scripts
- ❌ Much slower (~90-120 minút)
- ❌ Same end result

### Navrhovaný Proces

**1. Sample Analysis (2-3 súbory)**
- Analyze PAYLST (8.3 KB) - malý
- Analyze PAB (39.9 KB) - veľký
- Confirm all are historical mapping docs

**2. Create Batch Script (script 32)**
```python
# 32_archive_database_table_docs.py
# Move all 28 .md-old table docs to docs/archive/database-tables/
```

**3. Single Execution**
- Presunie všetky súbory naraz
- Creates archive directory
- Preserves structure (partners/, products/, stock/, etc.)

**4. Update Indexes**
- docs/database/00_DATABASE_INDEX.md
- docs/archive/00_ARCHIVE_INDEX.md
- SESSION_NOTES/docs.json

---

## 🔧 KRITICKÉ TECHNICKÉ INFO

### Documentation Manifest Location
```
C:\Development\nex-automat\SESSION_NOTES\docs.json
```

### GitHub Raw URL Pattern
```
https://raw.githubusercontent.com/rauschiccsk/nex-automat/develop/[path]
```

### Archive Target Structure
```
docs/archive/database-tables/
├── catalogs/
│   ├── partners/
│   │   ├── BANKLST-bank_catalog.md
│   │   ├── PAB-partner_catalog.md
│   │   ├── PABACC-partner_catalog_bank_accounts.md
│   │   ├── PACNCT-partner_catalog_contacts.md
│   │   ├── PAGLST-partner_categories.md
│   │   ├── PANOTI-partner_catalog_texts.md
│   │   ├── PASUBC-partner_catalog_facilities.md
│   │   ├── PAYLST-payment_methods.md
│   │   └── TRPLST-transport_methods.md
│   └── products/
│       ├── BARCODE-product_catalog_identifiers.md
│       ├── FGLST-product_categories.md
│       ├── GSCAT-product_catalog.md
│       ├── MGLST-product_categories.md
│       └── SGLST-product_categories.md
├── stock/
│   ├── cards/
│   │   ├── FIF-stock_card_fifos.md
│   │   ├── STK-stock_cards.md
│   │   ├── STKLST-stocks.md
│   │   ├── STM-stock_card_movements.md
│   │   └── WRILST-facilities.md
│   └── documents/
│       ├── TSH-supplier_delivery_heads.md
│       └── TSI-supplier_delivery_items.md
├── accounting/
│   ├── ISH-supplier_invoice_heads.md
│   ├── ISI-supplier_invoice_items.md
│   └── PAYJRN-payment_journal.md
└── sales/
    └── PLSnnnnn-price_list_items.md
```

---

## 📝 DOKUMENTAČNÉ ŠTANDARDY

### Archive Document Header

```markdown
# [Original Title]

**Category:** Archive / Database Tables  
**Original Location:** docs/architecture/database/[path]  
**Archived:** 2025-12-15  
**Reason:** Historical Btrieve → PostgreSQL mapping (migration complete)  
**Related:** [PARTNERS_REFERENCE.md](../../database/PARTNERS_REFERENCE.md)

---

[Original content preserved]
```

---

## ⚠️ KNOWN PATTERNS & REMINDERS

### Token Management
- Check usage pri ~80K tokens
- Database table docs môžu byť veľké (>30 KB)
- Sample analysis pred full batch operation

### Batch Script Best Practices

```python
#!/usr/bin/env python3
"""
Script 32: Batch archive all database table .md-old docs
Reason: Historical Btrieve mapping docs, migration complete
"""

from pathlib import Path
import shutil

# Define all 28 files with source → target mapping
FILES_TO_ARCHIVE = [
    {
        'source': 'docs/architecture/database/catalogs/partners/tables/PAYLST-payment_methods.md-old',
        'target': 'docs/archive/database-tables/catalogs/partners/PAYLST-payment_methods.md'
    },
    # ... (all 28 files)
]

def archive_file(source: Path, target: Path) -> bool:
    """Archive single file with header update."""
    # Implementation
    
def main():
    """Batch archive all database table docs."""
    # Process all 28 files
    # Report progress
    # Summary statistics
```

### .md-old Meaning (CRITICAL!)

**.md-old** = Waiting for systematic integration  
**.md** = Already in new systematic structure

**NOT** "old = delete" but "old = needs processing"

---

## 🚀 IMMEDIATE ACTION

**Prvý krok po načítaní tohto promptu:**

1. Skontroluj memory_user_edits (22 pravidiel) ✅
2. Opýtaj sa: "Spustil si už git commit z Batch 5?"
3. Ak ÁNO → "Chceš použiť batch approach pre database table docs (28 súborov)?"
4. Ak NIE → "Mám ti pomôcť s git commit?"

**Odporúčaný workflow:**
1. **Git commit batch 5 FIRST** (ak ešte nie)
2. **Sample analysis:** Load 2-3 table docs
3. **Confirm strategy:** Batch archive vs individual
4. **Create script 32:** Batch archive all 28 files
5. **Execute & verify**
6. **Update indexes**

---

## 📈 SUCCESS METRICS

**Pre túto session očakávame:**
- ✅ Git commit batch 5 dokončený (PRVÉ!)
- ✅ 28 database table docs archived (ONE batch operation)
- ✅ Archive structure vytvorená
- ✅ Indexy aktualizované
- ✅ Progress: 60/60 súborov (100% database docs)

**Alebo (individual approach):**
- ⏳ 5-10 table docs individually processed
- ⏳ Continue in next session

---

## 🎯 WORKFLOW BEST PRACTICES (from Batch 5)

### What Works Perfectly

✅ **Load → Analyze → Decide → Script → Execute → Verify**  
✅ **One decision at a time, wait for confirmation**  
✅ **Artifacts FIRST, discussions minimal**  
✅ **Clear script names with numbers**  
✅ **Proper categorization per file type**

### Communication Style

✅ **Stručne** - Žiadny verbose analysis output  
✅ **Akcie** - artifacts, scripts, konkrétne kroky  
✅ **Čakanie** - po každom artifacte čakať na potvrdenie  
✅ **Progress** - token stats na konci každej odpovede

---

## 📋 DECISION FRAMEWORK QUICK REFERENCE

| Typ dokumentu | Rozhodnutie | Príklad |
|---------------|-------------|---------|
| Historical mapping docs | ARCHIVE | All 28 table .md-old docs |
| Active reference | RELOCATE | INDEX.md → REFERENCE.md |
| Empty file | CREATE PLACEHOLDER | stock/INDEX.md-old |
| Obsolete replaced | DELETE | Old database INDEX.md |
| Multi-topic large doc | SPLIT | COMMON_DOCUMENT_PRINCIPLES |

---

## 📧 CRITICAL REMINDERS

### Before Starting

1. Check memory_user_edits (22 rules)
2. Confirm git commit status
3. Understand batch vs individual strategy
4. Review token budget (190,000 available)

### During Batch Operation

1. Sample 2-3 files first
2. Confirm structure consistency
3. Create comprehensive script
4. Test on 1-2 files before full batch
5. Verify all operations

### After Completion

1. Update all indexes
2. Generate fresh manifests
3. Verify archive structure
4. Check remaining .md-old count
5. Plan next session

---

**Token Budget:** 190,000  
**Estimated Session:** 1-2 hodiny (batch) / 3-4 hodiny (individual)  
**Ready to Continue:** ✅ ÁNO

---

**KONIEC INIT PROMPTU**

---

## 🔧 QUICK COMMANDS FOR REFERENCE

```powershell
# Check docs.json
cat SESSION_NOTES/docs.json | jq '.statistics'

# Count remaining .md-old files
(Get-ChildItem -Path docs -Recurse -Filter "*.md-old").Count

# Run batch script
python scripts/32_archive_database_table_docs.py

# Git workflow
git status
git add docs/ SESSION_NOTES/ scripts/
git commit -m "docs: Archive database table .md-old docs (batch 6)"
git push origin develop

# Generate manifests
python tools/generate_manifests.py
```