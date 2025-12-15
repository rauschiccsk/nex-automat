# INIT PROMPT - NEX Automat: Next Development Phase

**Projekt:** nex-automat  
**Current Status:** Database documentation complete, ready for implementation focus  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** https://claude.ai/chat/[LINK_TO_CURRENT_SESSION]  
**Status:** 🎉 MILESTONE REACHED - Database Docs 100% Complete

---

## ⚠️ KRITICKÉ: COLLABORATION RULES

**MUSÍŠ dodržiavať 22 pravidiel z memory_user_edits!**

Kľúčové pravidlá:
- **Rule #7:** CRITICAL artifacts pre všetky dokumenty/kód
- **Rule #8:** Step-by-step, confirmation pred pokračovaním
- **Rule #20:** "novy chat" = **3 artifacts** (SESSION_ARCHIVE, INIT, commit)
- **Rule #5:** Slovak language, presná terminológia projektov
- **Rule #22:** Na začiatku každého chatu skontrolovať všetky pravidlá

---

## ✅ ČO SME DOKONČILI

### 🎉 MAJOR MILESTONE: Database Documentation

**Status:** 25/25 dokumentov (100%) ✅

**By Section:**
- ✅ **Partners:** 9/9 (100%) - BANKLST, PAB, PABACC, PACNCT, PAGLST, PAYLST, TRPLST, PANOTI, PASUBC
- ✅ **Products:** 5/5 (100%) - BARCODE, FGLST, GSCAT, MGLST, SGLST
- ✅ **Stock Management:** 7/7 (100%) - WRILST, STKLST, TSH, FIF, TSI, STM, STK
- ✅ **Accounting:** 3/3 (100%) - ISH, ISI, PAYJRN
- ✅ **Sales:** 1/1 (100%) - PLSnnnnn

**Priemerná redukcia:** ~55% veľkosti (odstránené SQL/Python, zachovaný mapping + logika)

### Strategic Documentation

- ✅ **N8N_TO_TEMPORAL_MIGRATION.md** - relocate + rozšírenie
  - Implementation roadmap (7-10 týždňov)
  - Risks & mitigation
  - Docker compose
  - Success criteria

### Cleanup

- ✅ Zmazaný **SESSION_SUMMARY.md** (duplikát)
- ✅ Premenovaný **SESSION_NOTES/** → **init_chat/** (jasnejší názov)
- ✅ Aktualizované indexy (strategic, database, archive)

---

## 📊 CURRENT PROJECT STATUS

### Documentation Progress

| Kategória | Complete | Draft | Total | % |
|-----------|----------|-------|-------|---|
| Database Tables | 25 | 0 | 25 | 100% ✅ |
| Database Reference | 11 | 0 | 11 | 100% ✅ |
| Strategic | 4 | 2 | 6 | 67% |
| System | 2 | 4 | 6 | 33% |
| Applications | 0 | 10 | 10 | 0% |
| Packages | 0 | 7 | 7 | 0% |
| Development | 0 | 3 | 3 | 0% |
| Migration | 0 | 2 | 2 | 0% |
| Reference | 0 | 2 | 2 | 0% |

**Total:** 42 complete, 30 draft, 72 dokumentov

### Technical Stack Status

**Production:**
- ✅ FastAPI Backend (supplier-invoice-loader)
- ✅ PostgreSQL (staging database)
- ✅ NEX Genesis integration (Btrieve ODBC)
- ✅ Product enrichment (EAN matching 77-81%)

**In Development:**
- 🟡 PySide6 GUI (supplier-invoice-staging) - replacing PyQt5 editor
- 🟡 BaseWindow + BaseGrid persistence
- 🟡 Quick search functionality

**Planned:**
- 📋 Temporal workflow (n8n replacement)
- 📋 Docker deployment (customer-side)
- 📋 PySide6 migration (complete)

---

## 🎯 ODPORÚČANÉ NEXT STEPS

### Priority 1: Application Documentation (HIGH)

**supplier-invoice-loader/** (FastAPI Backend)
- ❌ API_SPECIFICATION.md - REST endpoints, payload structures
- ❌ WORKFLOWS.md - Email → PDF → Staging → NEX
- ❌ CONFIGURATION.md - Environment vars, database config

**supplier-invoice-staging/** (PySide6 GUI)
- ❌ GUI_STRUCTURE.md - Window hierarchy, BaseWindow usage
- ❌ DATABASE_SCHEMA.md - Staging tables, relationships
- ❌ NEX_INTEGRATION.md - Import to NEX Genesis
- ❌ WORKFLOWS.md - User workflows, state transitions

**Dôvod:** Apps sú v produkcii/vývoji, potrebujú dokumentáciu pre maintainability.

### Priority 2: Packages Documentation (HIGH)

**nex-shared/** (GUI Components)
- ❌ BASE_WINDOW.md - Window base class, persistence
- ❌ BASE_GRID.md - Grid component, quick search
- ❌ UTILITIES.md - DB helpers, config loaders

**nexdata/** (NEX Genesis Data Access)
- ❌ BTRIEVE_ACCESS.md - Btrieve connection, queries
- ❌ DATA_MODELS.md - Business models (GSCAT, PAB, ...)

**Dôvod:** Shared packages používané všetkými apps, kritické pre development.

### Priority 3: System Documentation (MEDIUM)

- ❌ GUI_FRAMEWORK.md - PySide6 standards, widget guidelines
- ❌ CONFIGURATION.md - Config system (YAML, env vars)
- ❌ CODING_STANDARDS.md - Python style, naming conventions
- ❌ MONOREPO_STRUCTURE.md - Apps, packages, tools organization

**Dôvod:** Štandardy pre konzistentný development.

### Priority 4: Migration Guides (MEDIUM)

- ❌ PYSIDE6_MIGRATION.md - PyQt5 → PySide6 migration plan
- ❌ DATABASE_MIGRATION.md - Btrieve → PostgreSQL tooling

**Dôvod:** Aktívne migračné projekty.

---

## 💡 IMPLEMENTATION PRIORITIES

### Immediate Development Focus

Po dokončení dokumentácie odporúčam:

1. **PySide6 Migration** (nex-shared package)
   - BaseWindow migration
   - BaseGrid migration
   - Testing framework

2. **Temporal Workflow** (n8n replacement)
   - Docker compose setup
   - Email monitoring activities
   - Invoice processing workflow
   - Testing + deployment

3. **Product Enrichment Improvements**
   - Zvýšenie match rate (77-81% → 90%+)
   - Fuzzy matching algoritmy
   - Manual matching UI

---

## 📂 TECHNICAL INFO

### Project Structure

```
nex-automat/
├── apps/
│   ├── supplier-invoice-loader/    # FastAPI (port 8001)
│   └── supplier-invoice-staging/   # PySide6 GUI (in dev)
├── packages/
│   ├── nex-shared/                 # GUI components (FLAT structure!)
│   └── nexdata/                    # NEX Genesis data access
├── docs/
│   ├── strategic/                  # 6 docs (4 complete, 2 draft)
│   ├── database/                   # 36 docs (100% complete!)
│   ├── applications/               # 10 docs (0% complete)
│   ├── packages/                   # 7 docs (0% complete)
│   ├── system/                     # 6 docs (2 complete, 4 draft)
│   └── archive/
│       └── sessions/               # 25+ session histories
├── scripts/
│   └── update_all_indexes.py      # Index update utility
└── init_chat/                      # Init files for new chat
    ├── INIT_PROMPT_NEW_CHAT.md
    └── PROJECT_MANIFEST.json
```

### Btrieve Locations (Complete Mapping)

**DIALS:** BANKLST, PAB, PABACC, PACNCT, PAGLST, PAYLST, TRPLST, PANOTI, PASUBC  
**STORES:** BARCODE, FGLST, GSCAT, MGLST, SGLST, WRILST, STKLST, TSH, TSI, FIF, STM, STK, PLS  
**LEDGER:** ISH, ISI, PAYJRN

### PostgreSQL Tables (Documented)

**25 tables fully documented:**
- 9 partner tables
- 5 product tables
- 7 stock management tables
- 3 accounting tables
- 1 sales table

---

## 📋 DOKUMENTAČNÉ ŠTANDARDY

### Artifact Requirements

**VŽDY artifacts pre:**
- Code snippets >5 lines
- Configs >10 lines
- Documents >10 lines
- Python scripts
- Markdown dokumenty

**Format:**
- Concise, action-oriented
- Slovak language
- Technical terminology presná
- Step-by-step approach

### Documentation Style

**Complete documents:**
- Purpose statement
- Technical details
- Code examples (where applicable)
- Related documents links
- Metadata (status, date, version)

**Draft documents:**
- Purpose statement
- TODO sections
- Priority indicator
- Target completion

---

## ⚡ WORKFLOW BEST PRACTICES

### Overený proces

1. **web_fetch** - načítaj existujúci dokument (ak existuje)
2. **Analyzuj** - určí scope, related docs
3. **Vytvor artifact** - kompletný dokument
4. **User skopíruje** - do správneho umiestnenia
5. **Čakaj na confirmation** - pred pokračovaním

### Komunikácia

✅ **Stručne** - žiadny verbose output  
✅ **Akcie** - artifacts, konkrétne kroky  
✅ **Čakanie** - po každom artifacte čakať na potvrdenie  
✅ **Progress** - token stats na konci každej odpovede

---

## 🚀 IMMEDIATE ACTION

**Prvý krok po načítaní tohto promptu:**

1. Skontroluj memory_user_edits (22 pravidiel) ✅
2. Opýtaj sa: "Ktorú dokumentáciu chceš dokončiť?"
   - Applications (HIGH priority)
   - Packages (HIGH priority)
   - System (MEDIUM priority)
   - Migration (MEDIUM priority)
3. Alebo: "Chceš pokračovať v implementácii?"
   - PySide6 migration
   - Temporal workflow
   - Product enrichment improvements

---

## 📊 SUCCESS METRICS

**Documentation:**
- Database: 25/25 (100%) ✅
- Applications: Target 10/10 (100%)
- Packages: Target 7/7 (100%)
- Overall: Target 80%+ complete

**Implementation:**
- PySide6 migration: Complete BaseWindow + BaseGrid
- Temporal: Working email workflow
- Product enrichment: 90%+ match rate

---

## 🔗 SÚVISIACE DOKUMENTY

**Already processed (reference):**
- docs/database/00_DATABASE_INDEX.md (všetky table docs complete)
- docs/strategic/N8N_TO_TEMPORAL_MIGRATION.md (migration plan)
- docs/strategic/00_STRATEGIC_INDEX.md (6 docs)
- docs/archive/00_ARCHIVE_INDEX.md (25+ sessions)

**To be processed (high priority):**
- docs/applications/supplier-invoice-loader/ (4 docs)
- docs/applications/supplier-invoice-staging/ (6 docs)
- docs/packages/nex-shared/ (4 docs)
- docs/packages/nexdata/ (3 docs)

**Reference documents:**
- docs/COLLABORATION_RULES.md (22 pravidiel)
- docs/archive/00_ARCHIVE_INDEX.md (update po session)
- init_chat/PROJECT_MANIFEST.json (project structure)

---

## ⚠️ ŠPECIÁLNE UPOZORNENIA

### nex-shared Package Structure

**CRITICAL:** nex-shared používa FLAT štruktúru:
```
packages/nex-shared/models/      ✅ CORRECT
packages/nex-shared/nex_shared/  ❌ WRONG
```

**"nex-shared" sa objavuje iba RAZ v ceste!**

### Token Budget

**Budget:** 190,000 tokens  
**Estimated session:** Závisí od rozsahu úlohy  
**Strategy:** Step-by-step, confirmation medzi krokmi

---

**Token Budget:** 190,000  
**Ready to Start:** ✅ ÁNO  
**Milestone:** 🎉 Database Documentation 100% Complete

---

**KONIEC INIT PROMPTU**