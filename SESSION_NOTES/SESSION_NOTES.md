# NEX Automat - Session Notes

**Projekt:** nex-automat  
**Developer:** Zoltán (40 rokov skúseností)  
**Current Focus:** Documentation Migration (.md-old systematic processing)  
**Last Updated:** 2025-12-15

---

## CURRENT STATUS

### Active Task: Documentation Migration - Batch 5

**Progress:** 32/60 súborov (53.3%) - **🎯 HALFWAY!**

**Completed:**
- ✅ Batch 1-4: Deployment docs, database general (25 files)
- ✅ Batch 5: Database indexes (7 files)

**Next:**
- ⏳ Database table docs (28 files) - **Batch archive recommended**
- ⏳ Strategic docs (2 files)
- ⏳ Development docs (1 file)
- ⏳ Other docs (4 files)

---

## RECENT SESSIONS

### Session 2025-12-15: Documentation Migration Batch 5

**Focus:** Database index files migration

**Completed:**
1. ✅ INDEX.md-old (database) - DELETE
2. ✅ catalogs/INDEX.md-old → CATALOGS_REFERENCE.md
3. ✅ catalogs/partners/INDEX.md-old → PARTNERS_REFERENCE.md
4. ✅ catalogs/products/INDEX.md-old → PRODUCTS_REFERENCE.md
5. ✅ sales/INDEX.md-old → SALES_REFERENCE.md
6. ✅ stock/INDEX.md-old → STOCK_REFERENCE.md (placeholder)
7. ✅ stock/cards/INDEX.md-old → STOCK_CARDS_REFERENCE.md

**Scripts:** 25-31 (7 scripts)

**Key Decisions:**
- Created consistent reference doc structure
- Placeholder for empty files
- Identified batch archive strategy for table docs

**Archive:** [SESSION_2025-12-15_documentation-migration-batch5.md](docs/archive/sessions/SESSION_2025-12-15_documentation-migration-batch5.md)

---

### Session 2025-12-15: Documentation Migration Batch 4

**Focus:** Deployment templates + database docs

**Completed:**
1. ✅ MAGERSTAV_ONBOARDING_GUIDE.md-old → USER_GUIDE_TEMPLATE.md
2. ✅ TRAINING_GUIDE.md-old → TRAINING_GUIDE_TEMPLATE.md
3. ✅ COMMON_DOCUMENT_PRINCIPLES.md-old → SPLIT (3 docs)
4. ✅ DATABASE_RELATIONSHIPS.md-old → RELATIONSHIPS.md
5. ✅ DATA_DICTIONARY.md-old → MIGRATION_MAPPING.md

**Scripts:** 20-24 (5 scripts)

**Archive:** [SESSION_2025-12-15_documentation-migration-batch4.md](docs/archive/sessions/SESSION_2025-12-15_documentation-migration-batch4.md)

---

### Session 2025-12-15: Documentation Migration Batch 3

**Focus:** Deployment documentation migration

**Completed:**
1. ✅ DEPLOYMENT_GUIDE_TEMPLATE.md-old → DEPLOYMENT_GUIDE.md
2. ✅ PRE_DEPLOYMENT_CHECKLIST_TEMPLATE.md-old → PRE_DEPLOYMENT_CHECKLIST.md
3. ✅ GO_LIVE_CHECKLIST_TEMPLATE.md-old → GO_LIVE_CHECKLIST.md
4. ✅ OPERATIONS_GUIDE_TEMPLATE.md-old → OPERATIONS_GUIDE.md
5. ✅ RECOVERY_PROCEDURES_TEMPLATE.md-old → RECOVERY_GUIDE.md
6. ✅ SERVICE_MANAGEMENT_TEMPLATE.md-old → SERVICE_MANAGEMENT.md
7. ✅ TROUBLESHOOTING_TEMPLATE.md-old → TROUBLESHOOTING.md

**Scripts:** 13-19 (7 scripts)

**Archive:** [SESSION_2025-12-15_documentation-migration-batch3.md](docs/archive/sessions/SESSION_2025-12-15_documentation-migration-batch3.md)

---

### Session 2025-12-15: Documentation Migration Batch 2

**Focus:** Batch 2 migration (6 files)

**Completed:**
1. ✅ QUICK_WINS_TECHNOLOGIES.md-old → QUICK_WINS_TECHNOLOGIES.md
2. ✅ AI_ML_TECHNOLOGIES.md-old → AI_ML_TECHNOLOGIES.md
3. ✅ PROJECT_VISION.md-old → PROJECT_VISION.md
4. ✅ PROJECT_ROADMAP.md-old → PROJECT_ROADMAP.md
5. ✅ GIT_WORKFLOW.md-old → GIT_WORKFLOW.md
6. ✅ WORKFLOW_REFERENCE.md-old → WORKFLOW_REFERENCE.md

**Scripts:** 07-12 (6 scripts)

**Archive:** [SESSION_2025-12-15_documentation-migration-batch2.md](docs/archive/sessions/SESSION_2025-12-15_documentation-migration-batch2.md)

---

## CRITICAL INFORMATION

### Documentation Manifest

**Location:** `SESSION_NOTES/docs.json`

**Statistics:**
- Total files: 129
- Markdown files: 90
- .md-old files: 28 (zostáva) - **database tables**

### Project Structure

```
nex-automat/
├── apps/                           # 3 applications
│   ├── supplier-invoice-editor/
│   ├── supplier-invoice-loader/
│   └── supplier-invoice-staging/
├── packages/                       # 2 shared packages
│   ├── nex-shared/
│   └── nexdata/
├── docs/                           # Documentation
│   ├── database/                   # ✨ NEW: Reference docs
│   │   ├── CATALOGS_REFERENCE.md
│   │   ├── PARTNERS_REFERENCE.md
│   │   ├── PRODUCTS_REFERENCE.md
│   │   ├── SALES_REFERENCE.md
│   │   ├── STOCK_REFERENCE.md
│   │   └── STOCK_CARDS_REFERENCE.md
│   └── archive/
│       ├── deployments/            # Customer-specific
│       └── sessions/               # Session archives
├── scripts/                        # Migration scripts 01-31
└── tools/                          # Claude automation
```

---

## NEXT STEPS

### Immediate Priority: Database Table Docs

**Files:** 28 .md-old table documentation files

**Categories:**
- Catalogs - Partners (9): BANKLST, PAB, PABACC, PACNCT, PAGLST, PANOTI, PASUBC, PAYLST, TRPLST
- Catalogs - Products (5): BARCODE, FGLST, GSCAT, MGLST, SGLST
- Stock Management (7): FIF, STK, STKLST, STM, WRILST, TSH, TSI
- Accounting (3): ISH, ISI, PAYJRN
- Sales (1): PLSnnnnn

**Recommended Strategy:**
1. Analyze 1-2 samples
2. Create batch archive script
3. Move all to `docs/archive/database-tables/`
4. Single execution for all 28 files

**Alternative:** Individual processing (28 scripts) - slower

---

### After Database Tables

**Strategic Docs (2):**
- PROJECT_BLUEPRINT_SUPPLIER_CLASSIFIER.md-old (51 KB)
- RESEARCH_ANALYSIS_TECHNOLOGY_LANDSCAPE.md-old (84 KB)
- Strategy: ARCHIVE as historical research

**Development (1):**
- CONTRIBUTING.md-old (12.5 KB) in `docs/giudes/` [typo!]
- Strategy: Fix typo, RELOCATE to `docs/development/`

**Other (4):**
- To be analyzed individually

---

## WORKFLOW BEST PRACTICES

### Established Pattern

**For Each .md-old File:**
1. Load with web_fetch
2. Analyze (quality, relevance, type)
3. Decide action (ARCHIVE/RELOCATE/DELETE/SPLIT/EXTRACT)
4. Create numbered script
5. User executes locally
6. Confirm success
7. Continue to next

### Communication Style

✅ **Stručne** - No verbose analysis  
✅ **Akcie** - Artifacts first, discussions minimal  
✅ **Čakanie** - Wait for confirmation after each artifact  
✅ **Progress** - Token stats at end of each response

---

## DOCUMENTATION STANDARDS

### Header Template

```markdown
# [Document Title]

**Category:** [Database/System/Strategic/...]  
**Status:** 🟢 Complete / 🟡 In Progress / 🔴 Draft  
**Created:** YYYY-MM-DD  
**Updated:** YYYY-MM-DD  
**Related:** [Links]

---
```

### File Naming

- Use `00_` prefix for index files
- UPPERCASE for important reference docs
- Descriptive names with underscores
- .md extension for active docs

---

## KEY METRICS

**Migration Progress:** 32/60 (53.3%)

**By Category:**
- ✅ Deployment: 11/11 (100%)
- ✅ Database General: 4/4 (100%)
- ✅ Database Indexes: 7/7 (100%)
- ⏳ Database Tables: 0/28 (0%)
- ⏳ Strategic: 0/2 (0%)
- ⏳ Development: 0/1 (0%)
- ⏳ Other: 0/4 (0%)

**Scripts Created:** 31

**Documentation Quality:** High - all verified

---

## IMPORTANT REMINDERS

### Memory Rules (22 pravidiel)

**CRITICAL rules for this project:**
- Rule #7: ALL artifacts for code/docs
- Rule #8: Step-by-step, wait for confirmation
- Rule #20: "novy chat" = 4 artifacts
- Rule #22: Check rules at start of EVERY chat

### Git Workflow

**Development → Git → Deployment**
- Never fix directly in Deployment
- All changes via numbered scripts
- User handles git operations

### Token Management

- Check at ~80K tokens
- Large files analyzed carefully
- Strategic docs are VERY LARGE (>50 KB)

---

## CONTACTS & REFERENCES

**Developer:** Zoltán  
**Company:** ICC Komárno  
**Project:** NEX Automat v2.4  

**Key URLs:**
- Repo: https://github.com/rauschiccsk/nex-automat
- Branch: develop
- Session Notes: SESSION_NOTES/SESSION_NOTES.md
- Manifests: SESSION_NOTES/*.json

---

**Last Session:** 2025-12-15  
**Next Focus:** Database table docs batch processing  
**Status:** 🟢 On track - halfway milestone achieved!