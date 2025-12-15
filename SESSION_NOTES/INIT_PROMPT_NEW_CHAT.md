# INIT PROMPT - NEX Automat: .md-old Migration (Batch 2)

**Projekt:** nex-automat  
**Úloha:** Pokračovanie systematickej migrácie .md-old súborov  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** https://claude.ai/chat/[CURRENT_CHAT_URI]  
**Status:** ✅ Batch 1 complete (8/60 súborov), pokračujeme

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

## 📋 ČO SME DOKONČILI V PREVIOUS SESSION (Batch 1)

### ✅ Migrované Dokumenty (6)

**Strategic (1):**
- ✅ QUICK_WINS_TECHNOLOGIES.md (19 KB) - Quick wins tech (Redis, Sentry, Docker...)

**Development (2):**
- ✅ GIT_WORKFLOW.md (5 KB) - Git branching, PyCharm operations
- ✅ CONTRIBUTING.md (12 KB) - Contributing guidelines, PR process

**Reference (1):**
- ✅ WORKFLOW_REFERENCE.md (5 KB) - Session workflow, file access

**System (1):**
- ✅ MONOREPO_GUIDE.md (11 KB) - Monorepo setup & workflow

**Archive (1):**
- 📦 CURRENT_STATE_2025-11-26.md (14 KB) - Historical GO-LIVE snapshot

### ❌ Deleted Dokumenty (1)

- ❌ REQUIREMENTS.md-old (9.4 KB) - obsolete (Btrieve done, n8n→Temporal)

### 📜 Script Vytvorený

- ✅ `04-update-indexes-after-migration.py` - Update indexes with new docs

### 📊 Progress

**Dokončené:** 8/60 súborov (13.3%)  
**Zostáva:** 52 súborov

---

## 🔄 ČO TREBA UROBIŤ TERAZ

### Priority 1: Index Update a Cleanup (PRVÉ!)

```powershell
# 1. Run update script
python scripts\04-update-indexes-after-migration.py

# 2. Delete migrated .md-old files
Remove-Item "C:\Development\nex-automat\docs\strategy\QUICK_WINS_TECHNOLOGY_GUIDE.md-old"
Remove-Item "C:\Development\nex-automat\docs\GIT_GUIDE.md-old"
Remove-Item "C:\Development\nex-automat\docs\giudes\CONTRIBUTING.md-old"
Remove-Item "C:\Development\nex-automat\docs\WORKFLOW_QUICK_REFERENCE.md-old"
Remove-Item "C:\Development\nex-automat\docs\giudes\MONOREPO_GUIDE.md-old"
Remove-Item "C:\Development\nex-automat\docs\strategy\CURRENT_STATE.md-old"
Remove-Item "C:\Development\nex-automat\docs\strategy\REQUIREMENTS.md-old"

# 3. Commit
git add docs/ scripts/ SESSION_NOTES/
git commit -m "docs: Migrate .md-old documents (batch 1) and update indexes"
git push origin develop
```

### Priority 2: Pokračovať Migráciu (Batch 2)

**Zostáva:** 52 .md-old súborov

---

## 📂 DOSTUPNÉ .md-old SÚBORY (zostáva 52)

### Strategic (4 zostáva)
- ✅ AI_ML_TOOLS... (DONE in previous session)
- ✅ QUICK_WINS... (DONE this session)
- ❌ REQUIREMENTS.md-old (DELETED)
- PROJECT_BLUEPRINT_SUPPLIER_CLASSIFIER.md-old (51 KB) ⚠️ LARGE
- RESEARCH_ANALYSIS_TECHNOLOGY_LANDSCAPE.md-old (84 KB) ⚠️ VERY LARGE
- PROJECT_STATUS.md-old (16 KB)
- CURRENT_STATE.md-old (ARCHIVED)

### Root Documents (3 zostáva)
- ✅ GIT_GUIDE.md-old (DONE)
- ✅ WORKFLOW_QUICK_REFERENCE.md-old (DONE)
- PROJECT_ARCHIVE.md-old (112 KB) ⚠️ VERY LARGE

### Guides (0 zostáva)
- ✅ CONTRIBUTING.md-old (DONE)
- ✅ MONOREPO_GUIDE.md-old (DONE)

### Deployment (12 súborov)
- DEPLOYMENT_GUIDE.md-old (13.8 KB)
- GO_LIVE_CHECKLIST.md-old (6.3 KB)
- OPERATIONS_GUIDE.md-old (8.1 KB)
- RECOVERY_GUIDE.md-old (13.6 KB)
- SERVICE_MANAGEMENT.md-old (7.7 KB)
- TROUBLESHOOTING.md-old (9.6 KB)
- KNOWN_ISSUES.md-old (1.4 KB)
- MAGERSTAV_DEPLOYMENT_SUMMARY.md-old (4.5 KB)
- MAGERSTAV_ONBOARDING_GUIDE.md-old (11.4 KB)
- PRE_DEPLOYMENT_CHECKLIST.md-old (6.4 KB)
- RECOVERY_PROCEDURES.md-old (9.8 KB)
- TRAINING_GUIDE.md-old (9.1 KB)

### Database Architecture (32 súborov)
**Všeobecné (4):**
- COMMON_DOCUMENT_PRINCIPLES.md-old (42.8 KB)
- DATABASE_RELATIONSHIPS.md-old (24.1 KB)
- DATA_DICTIONARY.md-old (22.7 KB)
- INDEX.md-old (6.0 KB)

**Katalógy - Produkty (5):**
- GSCAT, BARCODE, FGLST, MGLST, SGLST (16-24 KB každý)

**Katalógy - Partneri (9):**
- PAB, PABACC, PACNCT, PAGLST, PANOTI, PASUBC, BANKLST, PAYLST, TRPLST

**Stock (7):**
- STK, STM, FIF, STKLST, WRILST, TSH, TSI

**Accounting (3):**
- ISH, ISI, PAYJRN

---

## 🎯 ODPORÚČANÉ PRIORITY PRE BATCH 2

### Možnosť A: Strategic Documents (3 súbory)

**1. PROJECT_STATUS.md-old (16 KB)**
- Analyze: ARCHIVE vs UPDATE decision
- Likely outdated → ARCHIVE ako historical snapshot

**2. PROJECT_BLUEPRINT_SUPPLIER_CLASSIFIER.md-old (51 KB)**
- LARGE document, analyze first
- Consider: ARCHIVE (historical blueprint) vs UPDATE

**3. RESEARCH_ANALYSIS_TECHNOLOGY_LANDSCAPE.md-old (84 KB)**
- VERY LARGE, may require splitting
- Likely: ARCHIVE as research document

### Možnosť B: Deployment Documents (začať s menšími)

**Quick wins (small documents):**
1. KNOWN_ISSUES.md-old (1.4 KB)
2. MAGERSTAV_DEPLOYMENT_SUMMARY.md-old (4.5 KB)
3. GO_LIVE_CHECKLIST.md-old (6.3 KB)
4. PRE_DEPLOYMENT_CHECKLIST.md-old (6.4 KB)

**Strategy:** Merge do `docs/development/DEPLOYMENT.md`

### Možnosť C: Database Documents (začať s INDEX)

**Start small:**
1. INDEX.md-old (6.0 KB) - Overview database documentation
2. DATA_DICTIONARY.md-old (22.7 KB) - Data dictionary
3. DATABASE_RELATIONSHIPS.md-old (24.1 KB) - Relationships

**Then:** COMMON_DOCUMENT_PRINCIPLES.md-old (42.8 KB)

---

## 💡 WORKFLOW PATTERN (established)

### Pre Každý .md-old Súbor:

**1. Načítanie**
```
web_fetch: https://raw.githubusercontent.com/.../[filename].md-old
```

**2. Analýza**
- Typ dokumentu (Strategic/Technical/Reference/...)
- Kvalita obsahu (⭐1-5)
- Relevancia (High/Medium/Low)
- Cieľová kategória

**3. Rozhodnutie**
- **NEW:** Vytvor nový .md v príslušnej kategórii
- **MERGE:** Zlúč s existujúcim dokumentom
- **ARCHIVE:** Presuň do archive/ (ak historický)
- **DELETE:** Vymaž (ak obsolete/duplicate)

**4. Spracovanie**
- Pridaj štandardný header
- Vytvor TOC (ak potrebné)
- Pridaj See Also links

**5. Artifact**
- Vytvor artifact s novým .md obsahom
- Čakaj na potvrdenie od Zoltána

**6. Po Potvrdení**
- Zoltán uloží nový .md
- Zoltán vymaže .md-old (Remove-Item command)
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

## Obsah

[TOC if needed]

---

[Content]

---

**See Also:**
- [Related document 1]
- [Related document 2]
```

---

## ⚠️ KNOWN ISSUES & REMINDERS

### Token Management
- Pravidelne check token usage
- Pri ~80% navrhni checkpoint
- Veľké dokumenty (>40 KB) analyzuj PRED načítaním celého obsahu

### Migration Decisions
- **NEVER** delete bez potvrdenia
- **ALWAYS** verify migration success
- Keep track migrovaných vs zostávajúcich

### Index Updates
- Po každom batch run update script
- Commit indexes spolu s novými dokumentmi

---

## 🚀 IMMEDIATE ACTION

**Prvý krok po načítaní tohto promptu:**

1. Skontroluj memory_user_edits (21 pravidiel)
2. Opýtaj sa: "Spustil si už cleanup a commit z Batch 1?"
3. Ak ÁNO → "Ktorý .md-old súbor chceš spracovať ďalej?"
4. Ak NIE → "Mám ti pomôcť s cleanup commands?"

**Odporúčaný workflow:**
1. Cleanup batch 1 FIRST (ak ešte nie)
2. Začni s PROJECT_STATUS.md-old (analyze ARCHIVE vs UPDATE)
3. Potom deployment documents (small ones first)

---

## 📈 SUCCESS METRICS

**Pre túto session očakávame:**
- ✅ Cleanup batch 1 dokončený
- ✅ 5-10 .md-old súborov zmigrovaných
- ✅ Indexy aktualizované
- ✅ Žiadne .md-old deleted bez verifikácie
- ✅ Tokens < 80% pred koncom session

---

**Token Budget:** 190,000  
**Estimated Session:** 2-4 hodiny  
**Ready to Continue:** ✅ ÁNO

---

**KONIEC INIT PROMPTU**