# INIT PROMPT - NEX Automat: .md-old Migration (Batch 5)

**Projekt:** nex-automat  
**Úloha:** Pokračovanie systematickej migrácie .md-old súborov  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** https://claude.ai/chat/[CURRENT_CHAT_URI]  
**Status:** ✅ Batch 4 complete (25/60 súborov), pokračujeme

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

## 📋 ČO SME DOKONČILI V PREVIOUS SESSION (Batch 4)

### ✅ Migrované Dokumenty (5 → 8)

**1. MAGERSTAV_ONBOARDING_GUIDE.md-old (11.4 KB)**
- Action: EXTRACT TEMPLATE + ARCHIVE
- Result: USER_GUIDE_TEMPLATE.md + archive
- Script: 20_extract_user_guide_template.py

**2. TRAINING_GUIDE.md-old (9.1 KB)**
- Action: EXTRACT TEMPLATE + ARCHIVE
- Result: TRAINING_GUIDE_TEMPLATE.md + archive
- Script: 21_extract_training_template.py

**3. COMMON_DOCUMENT_PRINCIPLES.md-old (42.8 KB)**
- Action: SPLIT (3 dokumenty)
- Result: DOCUMENT_TYPES.md, NUMBERING.md, DATABASE_PRINCIPLES.md
- Script: 22_split_common_principles.py

**4. DATABASE_RELATIONSHIPS.md-old (24.1 KB)**
- Action: RELOCATE
- Result: docs/database/RELATIONSHIPS.md
- Script: 23_relocate_relationships.py

**5. DATA_DICTIONARY.md-old (22.7 KB)**
- Action: RELOCATE
- Result: docs/database/MIGRATION_MAPPING.md
- Script: 24_relocate_data_dictionary.py

### 📜 Scripts Vytvorené (5)

- `20_extract_user_guide_template.py`
- `21_extract_training_template.py`
- `22_split_common_principles.py`
- `23_relocate_relationships.py`
- `24_relocate_data_dictionary.py`

### 📊 Progress

**Dokončené:** 25/60 súborov (41.7%)  
**Zostáva:** 35 súborov

**By Category:**
- ✅ Deployment: 11/11 (100%) - **COMPLETE**
- ✅ Database General: 4/4 (100%) - **COMPLETE**
- ⏳ Database Tables: 0/28 (0%) - **NEXT**
- ⏳ Strategic: 0/2 (0%)
- ⏳ Development: 0/1 (0%)
- ⏳ Other: 0/4 (0%)

---

## 🔄 ČO TREBA UROBIŤ TERAZ

### Priority 1: Git Commit (PRVÉ!)

```powershell
# Commit batch 4 changes
git add docs/ SESSION_NOTES/ scripts/
git commit -m "docs: Migrate .md-old batch 4 - deployment templates + database docs"
git push origin develop
```

### Priority 2: Pokračovať Migráciu (Batch 5)

**Immediate Next:** INDEX.md-old (6 KB) - DELETE

**Strategy:** Individuálna analýza každého súboru

---

## 📂 DOSTUPNÉ .md-old SÚBORY (zostáva 35)

### Database - Index Files (7 súborov) ⭐ ODPORÚČAM ZAČAŤ TU

1. **INDEX.md-old** (6.0 KB) - docs/architecture/database/
   - Old database docs index
   - Likely: DELETE (replaced by new index)

2. **catalogs/INDEX.md-old** (6.7 KB)
   - Old catalogs index
   - Likely: DELETE or MERGE

3. **catalogs/partners/INDEX.md-old** (7.5 KB)
   - Old partners catalog index
   - Analyze individually

4. **catalogs/products/INDEX.md-old** (5.7 KB)
   - Old products catalog index
   - Analyze individually

5. **sales/INDEX.md-old** (8.1 KB)
   - Old sales index
   - Analyze individually

6. **stock/INDEX.md-old** (0 KB - empty!)
   - Empty file
   - DELETE

7. **stock/cards/INDEX.md-old** (20.4 KB)
   - Stock cards index
   - Analyze individually

---

### Database Tables (28 súborov) ⏳ AFTER INDEXES

**Catalogs - Partners (9):**
- BANKLST-bank_catalog.md-old (10.7 KB)
- PAB-partner_catalog.md-old (39.9 KB) ⚠️ LARGE
- PABACC-partner_catalog_bank_accounts.md-old (12.6 KB)
- PACNCT-partner_catalog_contacts.md-old (22.8 KB)
- PAGLST-partner_categories.md-old (14.9 KB)
- PANOTI-partner_catalog_texts.md-old (15.4 KB)
- PASUBC-partner_catalog_facilities.md-old (18.0 KB)
- PAYLST-payment_methods.md-old (8.3 KB)
- TRPLST-transport_methods.md-old (8.6 KB)

**Catalogs - Products (5):**
- BARCODE-product_catalog_identifiers.md-old (24.2 KB)
- FGLST-product_categories.md-old (16.1 KB)
- GSCAT-product_catalog.md-old (20.7 KB)
- MGLST-product_categories.md-old (17.4 KB)
- SGLST-product_categories.md-old (20.1 KB)

**Stock Management (7):**
- FIF-stock_card_fifos.md-old (28.5 KB)
- STK-stock_cards.md-old (38.5 KB) ⚠️ LARGE
- STKLST-stocks.md-old (20.4 KB)
- STM-stock_card_movements.md-old (35.6 KB) ⚠️ LARGE
- WRILST-facilities.md-old (17.9 KB)
- TSH-supplier_delivery_heads.md-old (25.4 KB)
- TSI-supplier_delivery_items.md-old (29.7 KB)

**Accounting (3):**
- ISH-supplier_invoice_heads.md-old (34.8 KB)
- ISI-supplier_invoice_items.md-old (29.6 KB)
- PAYJRN-payment_journal.md-old (25.8 KB)

**Sales (1):**
- PLSnnnnn-price_list_items.md-old (20.5 KB)

---

### Strategic (2 súborov) ⚠️ VERY LARGE

1. **PROJECT_BLUEPRINT_SUPPLIER_CLASSIFIER.md-old** (51 KB)
   - AI/ML supplier classification system design
   - Strategy: ARCHIVE as historical research

2. **RESEARCH_ANALYSIS_TECHNOLOGY_LANDSCAPE.md-old** (84 KB)
   - Technology research and analysis
   - Strategy: ARCHIVE as historical research

---

### Development (1 súbor)

1. **CONTRIBUTING.md-old** (12.5 KB) in `docs/giudes/` [typo!]
   - Development contribution guide
   - Strategy: FIX directory typo, RELOCATE to `docs/development/`

---

## 💡 ESTABLISHED WORKFLOW PATTERN

### Pre Každý .md-old Súbor:

**1. Načítanie**
```
web_fetch: https://raw.githubusercontent.com/.../[filename].md-old
```

**2. Analýza (stručne, bez verbose output)**
- Typ dokumentu
- Kvalita obsahu (⭐1-5)
- Relevancia (High/Medium/Low)
- Rozhodnutie (ARCHIVE/NEW/EXTRACT/DELETE/SPLIT/RELOCATE)

**3. Rozhodnutie**
- **SPLIT:** Veľký dokument s viacerými témami → viacero súborov
- **RELOCATE:** Aktívny dokument, presunúť na správne miesto
- **EXTRACT TEMPLATE:** Generic process + customer data → template + archive
- **ARCHIVE:** Historický/customer-specific → archive
- **DELETE:** Obsolete, replaced (zriedkavé, s potvrdením)
- **MERGE:** Pridať do existujúceho dokumentu

**4. Spracovanie**
- Vytvor numbered script (25, 26, 27...)
- Artifact FIRST, potom čakaj na potvrdenie
- User spustí script lokálne
- User potvrdí success

**5. Po Potvrdení**
- Next súbor

---

## 🔑 KĽÚČOVÉ TECHNICKÉ INFO

### Documentation Manifest Location
```
C:\Development\nex-automat\SESSION_NOTES\docs.json
```

### GitHub Raw URL Pattern
```
https://raw.githubusercontent.com/rauschiccsk/nex-automat/develop/[path]
```

### Dokumentačné Štandardy

**Header Template:**
```markdown
# [Document Title]

**Category:** [Strategic/System/Database/...]  
**Status:** 🟢 Complete / 🟡 In Progress / 🔴 Draft  
**Created:** YYYY-MM-DD  
**Updated:** YYYY-MM-DD  
**Related:** [Links]

---

[Content]

---

**See Also:**
- [Related document 1]
```

---

## ⚠️ KNOWN PATTERNS & REMINDERS

### Token Management
- Check usage pri ~80K tokens
- Database table docs môžu byť veľké (>30 KB)
- Strategic docs sú VERY LARGE (>50 KB)
- Pri veľkých súboroch analyzuj hlavičku PRED načítaním celého obsahu

### Migration Decisions Learned (Batch 4)

**SPLIT:**
- Veľké dokumenty (>40 KB) s viacerými témami
- Example: COMMON_DOCUMENT_PRINCIPLES → 3 docs

**RELOCATE:**
- Aktívne dokumenty, nie legacy
- Správna kategória v docs/
- Example: DATABASE_RELATIONSHIPS → docs/database/

**EXTRACT TEMPLATE:**
- Obsahuje generic process + customer specifics
- Create template + archive customer version
- Example: USER_GUIDE, TRAINING_GUIDE

**DELETE:**
- Obsolete indexes replaced by new structure
- Always confirm with user first

### .md-old Meaning (CRITICAL!)

**.md-old** = Waiting for systematic integration  
**.md** = Already in new systematic structure

**NOT** "old = archive" but "old = needs processing"

### Index Updates
- `docs/00_DOCUMENTATION_INDEX.md` - main index
- Category indexes (00_DATABASE_INDEX.md, etc.)
- Update PO KAŽDOM successful migration

---

## 📈 SUCCESS METRICS

**Pre túto session očakávame:**
- ✅ Git commit batch 4 dokončený (PRVÉ!)
- ✅ 5-10 index súborov zmigrovaných (DELETE alebo MERGE)
- ✅ Možno začať database table docs (ak čas)
- ✅ Indexy aktualizované
- ✅ Tokens < 80% pred koncom session

---

## 🚀 IMMEDIATE ACTION

**Prvý krok po načítaní tohto promptu:**

1. Skontroluj memory_user_edits (22 pravidiel) ✅
2. Opýtaj sa: "Spustil si už git commit z Batch 4?"
3. Ak ÁNO → "Ktorý .md-old súbor chceš spracovať ďalej?"
4. Ak NIE → "Mám ti pomôcť s git commit?"

**Odporúčaný workflow:**
1. **Git commit batch 4 FIRST** (ak ešte nie)
2. **Start:** INDEX.md-old (6 KB) - DELETE recommended
3. **Then:** 6 ďalších index súborov
4. **Assess:** Database table docs strategy

---

## 🎯 WORKFLOW BEST PRACTICES (from Batch 4)

### What Works Perfectly

✅ **Load → Analyze → Decide → Script → Execute → Verify**  
✅ **One file at a time, wait for confirmation**  
✅ **Artifacts FIRST, discussions minimal**  
✅ **Clear script names with numbers**  
✅ **Update indexes immediately**  
✅ **Individual analysis (NO batch operations)**  
✅ **Proper categorization per file type**

### Communication Style

✅ **Stručne** - žiadny verbose analysis output  
✅ **Akcie** - artifacts, scripts, konkrétne kroky  
✅ **Čakanie** - po každom artifacte čakať na potvrdenie  
✅ **Progress** - token stats na konci každej odpovede  

---

## 📋 DECISION FRAMEWORK QUICK REFERENCE

| Typ dokumentu | Rozhodnutie | Príklad |
|---------------|-------------|---------|
| Old index (replaced) | DELETE | INDEX.md-old |
| Empty file | DELETE | stock/INDEX.md-old (0 KB) |
| Large multi-topic doc | SPLIT | COMMON_DOCUMENT_PRINCIPLES |
| Active design doc | RELOCATE | DATABASE_RELATIONSHIPS |
| Generic + customer | EXTRACT TEMPLATE | USER_GUIDE, TRAINING |
| Pure Btrieve legacy | ARCHIVE | Table docs (TBD) |
| Historical research | ARCHIVE | Strategic docs |
| Duplicate content | MERGE | Category indexes (maybe) |

---

## 🔧 CRITICAL REMINDERS

### Before Each File

1. Load with web_fetch
2. Analyze content type and quality
3. Check if replaced by new docs
4. Make clear recommendation
5. Create script artifact
6. Wait for execution

### Script Creation

- Use numbered sequence (25, 26, 27...)
- Use pathlib for Windows paths
- Use raw strings (r"C:\...")
- Include error handling
- Clear progress output

### After Execution

- Wait for user confirmation
- Check for errors
- Note for index updates
- Continue to next file

---

**Token Budget:** 190,000  
**Estimated Session:** 2-4 hodiny  
**Ready to Continue:** ✅ ÁNO

---

**KONIEC INIT PROMPTU**

---

## 📧 QUICK COMMANDS FOR REFERENCE

```powershell
# Check docs.json
cat SESSION_NOTES/docs.json | jq '.statistics'

# Run script
python scripts/25_script_name.py

# Git workflow
git status
git add docs/ SESSION_NOTES/ scripts/
git commit -m "docs: Migrate .md-old batch 5 - [description]"
git push origin develop

# Generate manifests (if needed)
python tools/generate_manifests.py
```