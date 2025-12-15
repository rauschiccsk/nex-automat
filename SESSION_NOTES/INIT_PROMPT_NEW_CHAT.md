# INIT PROMPT - NEX Automat: .md-old Migration (Batch 4)

**Projekt:** nex-automat  
**Úloha:** Pokračovanie systematickej migrácie .md-old súborov  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** https://claude.ai/chat/[CURRENT_CHAT_URI]  
**Status:** ✅ Batch 3 complete (20/60 súborov), pokračujeme

---

## ⚠️ KRITICKÉ: COLLABORATION RULES

**MUSÍŠ dodržiavať 21 pravidiel z memory_user_edits!**

Kľúčové pravidlá pre túto session:
- **Rule #7:** CRITICAL artifacts pre všetky dokumenty/kód
- **Rule #8:** Step-by-step, confirmation pred pokračovaním
- **Rule #20:** "novy chat" = 4 artifacts (ARCHIVE, NOTES, INIT, commit)
- **Rule #5:** Slovak language, presná terminológia projektov
- **Rule #22:** Na začiatku každého chatu skontrolovať všetky pravidlá

---

## 📋 ČO SME DOKONČILI V PREVIOUS SESSION (Batch 3)

### ✅ Migrované Dokumenty (9)

**Deployment Documents:**

1. **MAGERSTAV_DEPLOYMET_SUMMARY.md-old** → ARCHIVED
2. **GO_LIVE_CHECKLIST.md-old** → Template + Archive
3. **PRE_DEPLOYMENT_CHECKLIST.md-old** → Template + Archive
4. **SERVICE_MANAGEMENT.md-old** → NEW (generic)
5. **DEPLOYMENT_GUIDE.md-old** → Template + Archive
6. **OPERATIONS_GUIDE.md-old** → Template + Archive (Slovak)
7. **RECOVERY_GUIDE.md-old** → Template + Archive
8. **RECOVERY_PROCEDURES.md-old** → ARCHIVED (duplicate)
9. **TROUBLESHOOTING.md-old** → Template + Archive

**Results:**
- ✅ 8 reusable templates created
- ✅ 9 Mágerstav-specific archives
- ✅ New directory: `docs/archive/deployments/`
- ✅ All indexes updated

### 📜 Scripts Vytvorené (9)

- `11_archive_magerstav_deployment.py`
- `12_extract_golive_checklist_template.py`
- `13_extract_predeployment_checklist.py`
- `14_migrate_service_management.py`
- `15_extract_deployment_guide.py`
- `16_extract_operations_guide.py`
- `17_extract_recovery_guide.py`
- `18_archive_recovery_procedures.py`
- `19_extract_troubleshooting_guide.py`

### 📊 Progress

**Dokončené:** 20/60 súborov (33.3%)  
**Zostáva:** 40 súborov

---

## 🔄 ČO TREBA UROBIŤ TERAZ

### Priority 1: Git Commit (PRVÉ!)

```powershell
# Commit batch 3 changes
git add docs/ SESSION_NOTES/ scripts/
git commit -m "docs: Migrate .md-old batch 3 - deployment templates + archives"
git push origin develop
```

### Priority 2: Pokračovať Migráciu (Batch 4)

**Zostáva:** 40 .md-old súborov

---

## 📂 DOSTUPNÉ .md-old SÚBORY (zostáva 40)

### Deployment (2 zostáva) ⭐ ODPORÚČAM ZAČAŤ TU

1. **MAGERSTAV_ONBOARDING_GUIDE.md-old** (11.4 KB)
   - Customer onboarding process
   - Likely: EXTRACT TEMPLATE + ARCHIVE

2. **TRAINING_GUIDE.md-old** (9.1 KB)
   - User training documentation
   - Likely: EXTRACT TEMPLATE + ARCHIVE

**Strategy:** Dokončiť deployment kategóriu pred prechodom na database docs

---

### Database Architecture (32 súborov)

**Všeobecné dokumenty (4):**

1. **COMMON_DOCUMENT_PRINCIPLES.md-old** (42.8 KB) ⚠️ LARGE
   - Common patterns across documents
   - Likely: ARCHIVE as reference

2. **DATABASE_RELATIONSHIPS.md-old** (24.1 KB)
   - Database schema relationships
   - Likely: MERGE into new DB docs or ARCHIVE

3. **DATA_DICTIONARY.md-old** (22.7 KB)
   - Field definitions
   - Likely: MERGE or ARCHIVE

4. **INDEX.md-old** (6.0 KB)
   - Database docs index
   - Likely: DELETE (replaced by new structure)

**Table Documentation (28 súborov):**

**Catalogs - Partners (8):**
- BANKLST-bank_catalog.md-old (10.7 KB)
- PAB-partner_catalog.md-old (39.9 KB)
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

**Stock Management (5):**
- FIF-stock_card_fifos.md-old (28.5 KB)
- STK-stock_cards.md-old (38.5 KB)
- STKLST-stocks.md-old (20.4 KB)
- STM-stock_card_movements.md-old (35.6 KB)
- WRILST-facilities.md-old (17.9 KB)

**Documents (2):**
- TSH-supplier_delivery_heads.md-old (25.4 KB)
- TSI-supplier_delivery_items.md-old (29.7 KB)

**Accounting (3):**
- ISH-supplier_invoice_heads.md-old (34.8 KB)
- ISI-supplier_invoice_items.md-old (29.6 KB)
- PAYJRN-payment_journal.md-old (25.8 KB)

**Sales (1):**
- PLSnnnnn-price_list_items.md-old (20.5 KB)

**Other (2):**
- catalogs/INDEX.md-old (6.7 KB)
- catalogs/partners/INDEX.md-old (7.5 KB)
- catalogs/products/INDEX.md-old (5.7 KB)
- sales/INDEX.md-old (8.1 KB)
- stock/INDEX.md-old (0 KB - empty!)
- stock/cards/INDEX.md-old (20.4 KB)

---

### Strategic (2 súborov) ⚠️ VERY LARGE

1. **PROJECT_BLUEPRINT_SUPPLIER_CLASSIFIER.md-old** (51 KB)
   - AI/ML supplier classification system design
   - Strategy: ARCHIVE as historical research

2. **RESEARCH_ANALYSIS_TECHNOLOGY_LANDSCAPE.md-old** (84 KB)
   - Technology research and analysis
   - Strategy: ARCHIVE as historical research

---

### Other (4 súborov)

1. **CONTRIBUTING.md-old** (12.5 KB) in `docs/giudes/` [typo!]
   - Development contribution guide
   - Strategy: FIX directory typo, migrate to `docs/development/`

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
- Rozhodnutie (ARCHIVE/NEW/EXTRACT/DELETE)

**3. Rozhodnutie**
- **ARCHIVE:** Historický/customer-specific
- **NEW:** Generický dokument
- **EXTRACT TEMPLATE + ARCHIVE:** Generic process + customer data
- **DELETE:** Obsolete (rare, s potvrdením)

**4. Spracovanie**
- Vytvor numbered script (20, 21, 22...)
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

**Kategória:** [Strategic/System/Database/...]  
**Status:** 🟢 Complete / 🟡 In Progress / 🔴 Draft  
**Vytvorené:** YYYY-MM-DD  
**Aktualizované:** YYYY-MM-DD  
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

### Migration Decisions Learned
- **Templates** pre reusable processes (checklists, guides)
- **Archive** pre customer-specific (Mágerstav dates, contacts)
- **Generic docs** kde nie sú customer specifics
- **Duplicates** - archive s poznámkou

### Database Docs Strategy (TBD)
- Možno BATCH archive všetkých 28 table docs
- Možno CREATE database doc generator
- DISCUSS s Zoltánom stratégiu pred spracovaním

### Index Updates
- `docs/00_DOCUMENTATION_INDEX.md` - main index
- `docs/archive/00_ARCHIVE_INDEX.md` - archive index
- Update PO KAŽDOM successful migration

---

## 📈 SUCCESS METRICS

**Pre túto session očakávame:**
- ✅ Git commit batch 3 dokončený (PRVÉ!)
- ✅ 2 deployment docs zmigrované (MAGERSTAV_ONBOARDING, TRAINING)
- ✅ Možno začať database docs (ak čas)
- ✅ Indexy aktualizované
- ✅ Tokens < 80% pred koncom session

---

## 🚀 IMMEDIATE ACTION

**Prvý krok po načítaní tohto promptu:**

1. Skontroluj memory_user_edits (21 pravidiel) ✅
2. Opýtaj sa: "Spustil si už git commit z Batch 3?"
3. Ak ÁNO → "Ktorý .md-old súbor chceš spracovať ďalej?"
4. Ak NIE → "Mám ti pomôcť s git commit?"

**Odporúčaný workflow:**
1. **Git commit batch 3 FIRST** (ak ešte nie)
2. **Start:** MAGERSTAV_ONBOARDING_GUIDE.md-old (11.4 KB)
3. **Then:** TRAINING_GUIDE.md-old (9.1 KB)
4. **Assess:** Database docs strategy discussion

---

## 🎯 WORKFLOW BEST PRACTICES (from Batch 3)

### What Works Perfectly

✅ **Load → Analyze → Decide → Script → Execute → Verify**  
✅ **One file at a time, wait for confirmation**  
✅ **Artifacts FIRST, discussions minimal**  
✅ **Clear script names with numbers**  
✅ **Update indexes immediately**  
✅ **Template extraction for reusable docs**  
✅ **Archive customer-specific versions**

### Communication Style

✅ **Stručne** - žiadny verbose analysis output  
✅ **Akcie** - artifacts, scripts, konkrétne kroky  
✅ **Čakanie** - po každom artifacte čakať na potvrdenie  
✅ **Progress** - token stats na konci každej odpovede  

---

## 📝 DECISION FRAMEWORK QUICK REFERENCE

| Typ dokumentu | Rozhodnutie | Príklad |
|---------------|-------------|---------|
| Deployment checklist | EXTRACT TEMPLATE + ARCHIVE | GO_LIVE_CHECKLIST |
| Customer-specific summary | ARCHIVE | MAGERSTAV_DEPLOYMENT |
| Generic operations guide | NEW or EXTRACT | SERVICE_MANAGEMENT |
| Duplicate content | ARCHIVE s poznámkou | RECOVERY_PROCEDURES |
| Table documentation | TBD - discuss strategy | Database tables |
| Strategic research | ARCHIVE | Technology landscape |

---

**Token Budget:** 190,000  
**Estimated Session:** 2-4 hodiny  
**Ready to Continue:** ✅ ÁNO

---

**KONIEC INIT PROMPTU**

---

## 🔧 QUICK COMMANDS FOR REFERENCE

```powershell
# Check docs.json
cat SESSION_NOTES/docs.json | jq '.statistics'

# Run script
python scripts/20_script_name.py

# Git workflow
git status
git add docs/ SESSION_NOTES/ scripts/
git commit -m "docs: Migrate .md-old batch 4 - [description]"
git push origin develop

# Generate manifests (if needed)
python tools/generate_manifests.py
```