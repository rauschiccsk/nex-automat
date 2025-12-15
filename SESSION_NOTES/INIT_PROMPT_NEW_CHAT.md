# INIT PROMPT - NEX Automat: Systematická Migrácia .md-old Dokumentov

**Projekt:** nex-automat  
**Úloha:** Pokračovanie systematickej migrácie .md-old súborov  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** https://claude.ai/chat/[CURRENT_CHAT_URI]  
**Status:** ✅ Dokumentačná štruktúra pripravená, začíname migráciu

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

## 📋 ČO SME DOKONČILI V PREVIOUS SESSION

### ✅ Definitívna Dokumentačná Štruktúra (v2.0 FINAL)

**Vytvorené:**
- Script: `02-update-documentation-structure.py` ✅
- 10 kategórií dokumentácie
- 35 nových súborov (draft)
- 6 nových adresárov
- Status: Commitnuté

**Štruktúra:**
```
docs/
├── strategic/ (4 docs)
├── system/ (6 docs)
├── database/ (3 adresáre)
├── documents/ (3 docs)
├── applications/ (2 apps, 10 docs)
├── packages/ (2 packages, 7 docs)
├── development/ (3 docs)
├── migration/ (2 docs)
├── reference/ (3 docs)
└── archive/ (sessions/)
```

### ✅ Všetky Indexy Aktualizované

**Vytvorené:**
- Script: `03-update-all-indexes.py` ✅
- 10 index súborov s kompletným obsahom
- Status: **PENDING COMMIT**

**Indexy obsahujú:**
- Zoznam existujúcich .md dokumentov
- Status dokumentov (Complete/Draft)
- Quick links, štatistiky
- See Also cross-references

### ✅ Prvá .md-old Migrácia

**Súbor:** `AI_ML_TOOLS_TECHNOLOGY_GUIDE.md-old`  
**→ Nový:** `docs/strategic/AI_ML_TECHNOLOGIES.md`  
**Status:** Complete ✅  
**Akcia:** `.md-old` ready to delete

---

## 🔄 ČO TREBA UROBIŤ TERAZ

### Priority 1: Git Commit (PRVÉ!)

```bash
git add docs/
git commit -m "docs: Update all index files with content"
```

### Priority 2: Pokračovať Migráciu .md-old

**Zostáva:** 59 .md-old súborov (z 60 pôvodných)

**Workflow per súbor:**
```
1. Zoltán dá názov .md-old súboru
2. Claude načíta z GitHub (raw URL z manifestu)
3. Claude analyzuje obsah:
   - Typ/kategória
   - Cieľové umiestnenie v novej štruktúre
   - Navrhne akciu (merge/new/archive/delete)
4. Claude spracuje obsah (ak treba)
5. Claude vytvorí artifact s novým .md
6. Zoltán potvrdí
7. Zoltán uložíš nový .md
8. Zoltán vymaže .md-old
9. Next súbor
```

---

## 📊 DOSTUPNÉ .md-old SÚBORY (z manifestu)

### Root Dokumenty (4 zostáva)
- GIT_GUIDE.md-old (4.9 KB)
- PROJECT_ARCHIVE.md-old (112.7 KB) ⚠️ VEĽKÝ
- PROJECT_STATUS.md-old (16.0 KB)
- WORKFLOW_QUICK_REFERENCE.md-old (4.7 KB)

### Database Architecture (32 súborov)
**Všeobecné:**
- COMMON_DOCUMENT_PRINCIPLES.md-old (42.8 KB)
- DATABASE_RELATIONSHIPS.md-old (24.1 KB)
- DATA_DICTIONARY.md-old (22.7 KB)
- INDEX.md-old (6.0 KB)

**Katalógy - Produkty (5):**
- GSCAT-product_catalog.md-old (20.7 KB)
- BARCODE-product_catalog_identifiers.md-old (24.2 KB)
- FGLST, MGLST, SGLST kategórie (16-20 KB každý)

**Katalógy - Partneri (9):**
- PAB-partner_catalog.md-old (39.9 KB)
- PABACC, PACNCT, PAGLST, PANOTI, PASUBC (12-23 KB)
- BANKLST, PAYLST, TRPLST (8-11 KB)

**Stock (7):**
- STK, STM, FIF stock cards (28-39 KB)
- STKLST, WRILST (17-20 KB)
- TSH, TSI delivery docs (25-30 KB)

**Accounting (3):**
- ISH, ISI invoice docs (29-35 KB)
- PAYJRN payment journal (25.8 KB)

### Deployment (12 súborov)
- DEPLOYMENT_GUIDE.md-old (13.8 KB)
- GO_LIVE_CHECKLIST.md-old (6.3 KB)
- OPERATIONS_GUIDE.md-old (8.1 KB)
- RECOVERY_GUIDE.md-old (13.6 KB)
- SERVICE_MANAGEMENT.md-old (7.7 KB)
- TROUBLESHOOTING.md-old (9.6 KB)
- + 6 ďalších (4-11 KB každý)

### Guides (2 súbory)
- CONTRIBUTING.md-old (12.5 KB)
- MONOREPO_GUIDE.md-old (11.4 KB)

### Strategy (5 zostáva)
- ✅ AI_ML_TOOLS... (DOKONČENÉ)
- RESEARCH_ANALYSIS_TECHNOLOGY...md-old (84.5 KB) ⚠️ VEĽKÝ
- PROJECT_BLUEPRINT_SUPPLIER...md-old (51.1 KB)
- QUICK_WINS_TECHNOLOGY_GUIDE.md-old (19.0 KB)
- CURRENT_STATE.md-old (14.4 KB)
- REQUIREMENTS.md-old (9.4 KB)

---

## 🎯 ODPORÚČANÉ PRIORITY

### Začať S (Quick Wins):
1. **QUICK_WINS_TECHNOLOGY_GUIDE.md-old** (19 KB)
   - Partner k AI_ML_TECHNOLOGIES
   - Strategic dokument
   - Stredná veľkosť

2. **GIT_GUIDE.md-old** (4.9 KB)
   - Malý, jednoduchý
   - Development / Reference kategória

3. **WORKFLOW_QUICK_REFERENCE.md-old** (4.7 KB)
   - Malý, užitočný
   - Reference kategória

### Potom (Valuable Content):
4. **Database dokumenty** (začať s GSCAT, PAB)
   - Kritický content
   - Veľa práce investovanej

5. **Deployment guides** (12 súborov)
   - Merge do DEPLOYMENT.md
   - Production knowledge

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

[Content]

---

**See Also:**
- [Related document 1]
- [Related document 2]
```

**Token Limit:** Max 15k per dokument

---

## 💡 WORKFLOW PATTERN

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
- **New:** Vytvor nový .md v príslušnej kategórii
- **Merge:** Zlúč s existujúcim dokumentom
- **Archive:** Presuň do archive/ (ak historický)
- **Delete:** Vymaž (ak obsolete/duplicate)

**4. Spracovanie**
- Pridaj štandardný header
- Vytvor TOC (ak potrebné)
- Pridaj See Also links
- Update príslušný index

**5. Artifact**
- Vytvor artifact s novým .md obsahom
- Čakaj na potvrdenie od Zoltána

**6. Po Potvrdení**
- Zoltán uloží nový .md
- Zoltán vymaže .md-old
- Update SESSION_NOTES.md
- Next súbor

---

## ⚠️ KNOWN ISSUES & REMINDERS

### Token Management
- Pravidelne check token usage
- Pri ~80% navrhni checkpoint
- Veľké dokumenty (>40 KB) rozdeliť na časti

### Git Workflow
- Development → Git → Deployment
- Never fix directly in Deployment
- Commit messages: clear & descriptive

### .md-old Handling
- **NEVER** delete bez potvrdenia
- **ALWAYS** verify migration success
- Keep track migrovaných vs zostávajúcich

---

## 🚀 IMMEDIATE ACTION

**Prvý krok po načítaní tohto promptu:**

1. Skontroluj memory_user_edits (21 pravidiel)
2. Load docs.json manifest (ak potrebné)
3. Opýtaj sa: "Chceš commitnúť index updates ALEBO začať s migráciou?"
4. Podľa odpovede:
   - **Commit:** Priprav commit message
   - **Migrácia:** "Ktorý .md-old súbor chceš spracovať?"

---

## 📈 SUCCESS METRICS

**Pre túto session očakávame:**
- ✅ Git commit index updates
- ✅ 3-5 .md-old súborov zmigrovaných
- ✅ Indexy aktualizované s novými dokumentmi
- ✅ Žiadne .md-old deleted bez verifikácie
- ✅ Tokens < 80% pred koncom session

---

**Token Budget:** 190,000  
**Estimated Session:** 2-4 hodiny  
**Ready to Continue:** ✅ ÁNO

---

**KONIEC INIT PROMPTU**