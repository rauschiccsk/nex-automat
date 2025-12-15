# INIT PROMPT - NEX Automat: .md-old Migration (Batch 3)

**Projekt:** nex-automat  
**Úloha:** Pokračovanie systematickej migrácie .md-old súborov  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** https://claude.ai/chat/[CURRENT_CHAT_URI]  
**Status:** ✅ Batch 2 complete (11/60 súborov), pokračujeme

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

## 📋 ČO SME DOKONČILI V PREVIOUS SESSION (Batch 2)

### ✅ Migrované Dokumenty (3)

**1. PROJECT_ARCHIVE.md-old (126 KB) → 7 session files:**
- SESSION_2025-12-06_basegrid-persistence-implementation.md (4.7 KB)
- SESSION_2025-12-08_v22-cleanup-mágerstav-deployment-attempt.md (11.8 KB)
- SESSION_2025-12-08_documentation-restructure-v23-planning.md (21.9 KB)
- SESSION_2025-12-08_v23-loader-migration.md (10.1 KB)
- SESSION_2025-12-08_v24-product-enrichment.md (19.0 KB)
- SESSION_2025-12-09_v24-phase4-deployment.md (8.1 KB)
- SESSION_2025-12-09_v24-implementation-complete.md (50.0 KB)

**2. PROJECT_STATUS.md-old (16 KB):**
- ✅ Archived to: `docs/archive/PROJECT_STATUS_v2.1_2025-12-02.md`
- Decision: Will create NEW after all .md-old processed

**3. KNOWN_ISSUES.md-old (1.4 KB):**
- ❌ Deleted (obsolete, all issues fixed)

### 📜 Scripts Vytvorené (6)

- `05_split_project_archive.py` - Split archive by sessions
- `06_rename_generic_sessions.py` - Improve filenames
- `07_fix_session_names.py` - Manual filename fixes
- `08_archive_project_status.py` - Archive with notice
- `09_delete_known_issues.py` - Delete obsolete
- `10_update_documentation_indexes.py` - Update all indexes

### 📊 Indexes Updated

- ✅ `docs/archive/00_ARCHIVE_INDEX.md` - 7 sessions indexed
- ✅ `docs/00_DOCUMENTATION_INDEX.md` - 65 documents
- ✅ `SESSION_NOTES/docs.json` - Progress: 18.3%

### 📊 Progress

**Dokončené:** 11/60 súborov (18.3%)  
**Zostáva:** 49 súborov

---

## 🔄 ČO TREBA UROBIŤ TERAZ

### Priority 1: Git Commit (PRVÉ!)

```powershell
# Commit batch 2 changes
git add docs/ SESSION_NOTES/ scripts/
git commit -m "docs: Migrate .md-old batch 2 - PROJECT_ARCHIVE split, indexes updated"
git push origin develop
```

### Priority 2: Pokračovať Migráciu (Batch 3)

**Zostáva:** 49 .md-old súborov

**Odporúčané priority:**

**Option A: Deployment Docs (Quick Wins) ⭐ ODPORÚČAM**
Začať s malými súbormi:
1. MAGERSTAV_DEPLOYMET_SUMMARY.md-old (4.5 KB)
2. GO_LIVE_CHECKLIST.md-old (6.3 KB)
3. PRE_DEPLOYMENT_CHECKLIST.md-old (6.4 KB)
4. SERVICE_MANAGEMENT.md-old (7.7 KB)

**Strategy:** Merge do `docs/deployment/DEPLOYMENT.md`

**Option B: Continue Large Strategic**
1. PROJECT_BLUEPRINT_SUPPLIER_CLASSIFIER.md-old (51 KB)
2. RESEARCH_ANALYSIS_TECHNOLOGY_LANDSCAPE.md-old (84 KB)

**Strategy:** ARCHIVE ako research documents

---

## 📂 DOSTUPNÉ .md-old SÚBORY (zostáva 49)

### Strategic (2 zostáva)
- PROJECT_BLUEPRINT_SUPPLIER_CLASSIFIER.md-old (51 KB) ⚠️ LARGE
- RESEARCH_ANALYSIS_TECHNOLOGY_LANDSCAPE.md-old (84 KB) ⚠️ VERY LARGE

### Deployment (11 súborov)
- DEPLOYMENT_GUIDE.md-old (13.8 KB)
- GO_LIVE_CHECKLIST.md-old (6.3 KB)
- OPERATIONS_GUIDE.md-old (8.1 KB)
- RECOVERY_GUIDE.md-old (13.6 KB)
- SERVICE_MANAGEMENT.md-old (7.7 KB)
- TROUBLESHOOTING.md-old (9.6 KB)
- MAGERSTAV_DEPLOYMET_SUMMARY.md-old (4.5 KB) ⭐ START HERE
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

**Katalógy, Stock, Accounting...** (28 súborov)

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
- Vytvor numbered script
- Test locally
- Čakaj na potvrdenie od Zoltána

**5. Po Potvrdení**
- Zoltán spustí script
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
2. Opýtaj sa: "Spustil si už git commit z Batch 2?"
3. Ak ÁNO → "Ktorý .md-old súbor chceš spracovať ďalej?"
4. Ak NIE → "Mám ti pomôcť s git commit?"

**Odporúčaný workflow:**
1. Git commit batch 2 FIRST (ak ešte nie)
2. Začni MAGERSTAV_DEPLOYMET_SUMMARY.md-old (4.5 KB)
3. Potom GO_LIVE_CHECKLIST.md-old (6.3 KB)
4. Pokračuj ďalšími malými deployment docs

---

## 📈 SUCCESS METRICS

**Pre túto session očakávame:**
- ✅ Git commit batch 2 dokončený
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