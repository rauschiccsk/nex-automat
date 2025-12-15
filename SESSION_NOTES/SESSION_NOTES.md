# SESSION NOTES - NEX Automat

**Last Updated:** 2025-12-15  
**Current Phase:** Documentation Migration  
**Status:** 🟡 IN PROGRESS

---

## 📌 Current Status

### Documentation Migration Progress

**Completed:** 8/60 .md-old súborov (13.3%)
- ✅ Migrované: 6 dokumentov
- ❌ Deleted: 1 dokument (obsolete)
- 📦 Archived: 1 dokument (historical)

**Zostáva:** 52 .md-old súborov

### Recent Achievements

**Batch 1 Completed (2025-12-15):**
- ✅ QUICK_WINS_TECHNOLOGIES.md (strategic)
- ✅ GIT_WORKFLOW.md (development)
- ✅ CONTRIBUTING.md (development)
- ✅ WORKFLOW_REFERENCE.md (reference)
- ✅ MONOREPO_GUIDE.md (system)
- 📦 CURRENT_STATE_2025-11-26.md (archive)

**Script Created:**
- 04-update-indexes-after-migration.py (ready to run)

---

## 🎯 Next Steps

### Immediate Actions

**1. Update Indexes**
```powershell
python scripts\04-update-indexes-after-migration.py
```

**2. Delete Migrated .md-old Files**
```powershell
Remove-Item "C:\Development\nex-automat\docs\strategy\QUICK_WINS_TECHNOLOGY_GUIDE.md-old"
Remove-Item "C:\Development\nex-automat\docs\GIT_GUIDE.md-old"
Remove-Item "C:\Development\nex-automat\docs\giudes\CONTRIBUTING.md-old"
Remove-Item "C:\Development\nex-automat\docs\WORKFLOW_QUICK_REFERENCE.md-old"
Remove-Item "C:\Development\nex-automat\docs\giudes\MONOREPO_GUIDE.md-old"
Remove-Item "C:\Development\nex-automat\docs\strategy\CURRENT_STATE.md-old"
Remove-Item "C:\Development\nex-automat\docs\strategy\REQUIREMENTS.md-old"
```

**3. Commit Changes**
```powershell
git add docs/ scripts/ SESSION_NOTES/
git commit -m "docs: Migrate .md-old documents (batch 1) and update indexes"
git push origin develop
```

### Next Migration Batch

**Priority Documents:**

1. **PROJECT_STATUS.md-old** (16 KB) - analyze for ARCHIVE/UPDATE
2. **Deployment documents** (12 súborov) - merge strategy needed
3. **Database documents** (začať so všeobecnými)

---

## 📊 Migration Statistics

### By Category

| Kategória | Celkom | Hotové | Zostáva |
|-----------|--------|--------|---------|
| Strategic | 6 | 2 | 4 |
| System | 2 | 1 | 1 |
| Development | 5 | 2 | 3 |
| Reference | 3 | 1 | 2 |
| Deployment | 12 | 0 | 12 |
| Database | 32 | 0 | 32 |
| Archive | 1 | 1 | 0 |
| **TOTAL** | **61** | **8** | **53** |

Note: TOTAL includes 1 deleted (REQUIREMENTS.md-old)

### Size Distribution

**Completed:**
- Small (<10 KB): 4 dokumenty
- Medium (10-20 KB): 2 dokumenty
- Large (>20 KB): 0 dokumentov

**Remaining Large Documents (>40 KB):**
- RESEARCH_ANALYSIS_TECHNOLOGY_LANDSCAPE.md-old (84 KB) ⚠️
- PROJECT_BLUEPRINT_SUPPLIER_CLASSIFIER.md-old (51 KB)
- COMMON_DOCUMENT_PRINCIPLES.md-old (42 KB)

---

## 🔧 Technical Context

### Project Structure

```
nex-automat/
├── apps/
│   ├── supplier-invoice-loader/    # Production (Mágerstav)
│   ├── supplier-invoice-editor/    # Deprecated (PyQt5)
│   └── supplier-invoice-staging/   # Development (PySide6)
├── packages/
│   ├── nex-shared/                 # GUI components (FLAT structure)
│   └── nexdata/                    # Btrieve data access
├── docs/                           # ← ACTIVE MIGRATION
│   ├── strategic/
│   ├── system/
│   ├── database/
│   ├── development/
│   ├── reference/
│   └── archive/
└── scripts/
    └── 04-update-indexes-after-migration.py
```

### Active Technologies

**Current:**
- Python 3.13.7 32-bit (Btrieve compatibility)
- FastAPI (supplier-invoice-loader)
- PySide6 (supplier-invoice-staging - in development)
- PostgreSQL (staging database)
- Btrieve (NEX Genesis - legacy)

**Planned Migration:**
- n8n → Temporal (workflow engine)
- PyQt5 → PySide6 (GUI framework)

---

## 📝 Important Notes

### Migration Guidelines

**ALWAYS:**
- ✅ Štandardný header s kategóriou, status, dátumy
- ✅ Zachovať celý obsah (ak relevant)
- ✅ Pridať See Also links
- ✅ Update príslušný index

**NEVER:**
- ❌ Delete .md-old bez potvrdenia
- ❌ Migrate bez analysis
- ❌ Skip index updates

### Decision Framework

**NEW:** Vytvor nový dokument
- Kvalitný, aktuálny obsah
- Jasné umiestnenie v kategórii
- Samostatný dokument

**ARCHIVE:** Presun do archive/
- Historický kontext cenný
- Outdated ale užitočné pre referenciu
- Snapshot projektu

**DELETE:** Vymaž súbor
- Kompletne obsolete
- Duplikát existujúceho
- Nepoužiteľný obsah

**MERGE:** Zlúč s existujúcim
- Deployment documents → DEPLOYMENT.md
- Fragmentované dokumenty

---

## 🚀 Session Workflow

### Standard Session Pattern

1. **Init:** Load INIT_PROMPT_NEW_CHAT.md + PROJECT_MANIFEST.json
2. **Analyze:** Check SESSION_NOTES.md for next steps
3. **Execute:** Process 5-10 .md-old files
4. **Update:** Run index update script
5. **Commit:** Git commit & push
6. **Archive:** Create session archive

### Files Per Session

**Target:** 5-10 dokumentov
- Small (<10 KB): 7-10 súborov
- Medium (10-20 KB): 5-7 súborov
- Large (>40 KB): 1-3 súbory (analyze/split first)

---

## 🔗 Quick Links

**Documentation:**
- [Main Index](../docs/00_DOCUMENTATION_INDEX.md)
- [Strategic Index](../docs/strategic/00_STRATEGIC_INDEX.md)
- [System Index](../docs/system/00_SYSTEM_INDEX.md)
- [Development Index](../docs/development/00_DEVELOPMENT_INDEX.md)

**Scripts:**
- [Update Indexes](../scripts/04-update-indexes-after-migration.py)

**GitHub:**
- [Repository](https://github.com/rauschiccsk/nex-automat)
- [Raw Docs](https://raw.githubusercontent.com/rauschiccsk/nex-automat/develop/docs/)

---

## 📞 Contact

**Project:** NEX Automat v2.0  
**Developer:** Zoltán Rausch  
**Organization:** ICC Komárno  
**Email:** rausch@icc.sk

---

**Last session:** 2025-12-15 (.md-old migration batch 1)  
**Next session:** Continue with batch 2 (strategic/deployment docs)  
**Status:** Ready to continue ✅