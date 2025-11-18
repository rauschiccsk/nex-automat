# NEX Automat - Session Notes

**Date:** 2025-11-18  
**Project:** nex-automat  
**Location:** C:/Development/nex-automat  
**Session:** Monorepo Migration - Phase Complete (Testing)

---

## 🎯 Current Status

### ✅ Completed Tasks

**FÁZA 1-3: Monorepo Setup & Migration** ✅ DOKONČENÉ
- [x] Vytvorená monorepo štruktúra (apps/, packages/, docs/, tools/)
- [x] Migrované oba projekty z lokálnych adresárov
  - supplier-invoice-loader: 129 súborov
  - invoice-editor → supplier-invoice-editor: 71 súborov (renamed)
- [x] Vytvorený invoice-shared package
  - postgres_staging.py, text_utils.py extrahované
- [x] Aktualizované importy v oboch apps
  - `from src.* → from invoice_shared.*`
- [x] Odstránené duplicitné súbory

**Dependencies & Configuration** ✅ DOKONČENÉ
- [x] UV workspace config (root pyproject.toml)
- [x] Hatchling build config pre všetky packages
- [x] pip install dependencies (32-bit Python compatible)
- [x] psutil urobené optional (PSUTIL_AVAILABLE flag)
- [x] SQLAlchemy odstránené (používame len asyncpg)

**Testing Infrastructure** ✅ ČIASTOČNE
- [x] Presunuté ad-hoc test scripty do scripts/
  - manual_test_extraction.py
  - manual_test_isdoc.py
  - manual_test_batch_extraction.py
- [x] Opravené monitoring.py API (get_metrics(), reset_metrics())
- [x] Opravené conftest.py fixtures
- [x] 46/71 testov prechádza ✅
- [x] 11 testov skipped (nefunkčné monitoring features)
- [ ] 14 testov failed (monitoring API mismatches)

### ⏳ In Progress

**Test Fixes Needed:**
- [ ] Opraviť test_monitoring.py - nekompatibilné API
  - increment_processed() vs invoices_processed
  - increment_failed() vs increment_invoice()
  - get_uptime_seconds() vs get_uptime()
  - invoices_duplicates neexistuje
- [ ] Opraviť test_api.py - check_storage_health() chýba
- [ ] Opraviť test_api.py - api_requests attribute chýba

### 📋 Next Steps

**PRIORITY 1: Dokončiť monitoring API alignment**
Možnosti:
1. Rozšíriť Metrics class o chýbajúce metódy
2. Upraviť testy na nové API
3. Skip všetky monitoring testy a opraviť neskôr

**PRIORITY 2: Final verification**
```
pytest --tb=no -q
Cieľ: 60+ passing tests
```

**PRIORITY 3: Documentation update**
- Update docs/MIGRATION_SUMMARY.md
- Update docs/SESSION_NOTES.md
- Create MONOREPO_GUIDE.md

---

## 🏗️ Monorepo Structure

```
C:/Development/nex-automat/
├── apps/
│   ├── supplier-invoice-loader/        ✅ Migrated, 46/71 tests passing
│   │   ├── src/
│   │   ├── tests/
│   │   ├── scripts/                    (ad-hoc test scripts)
│   │   └── pyproject.toml
│   └── supplier-invoice-editor/        ✅ Migrated, ready
│       └── pyproject.toml
│
├── packages/
│   ├── invoice-shared/                 ✅ Created
│   │   └── invoice_shared/
│   │       ├── database/               (postgres_staging.py)
│   │       ├── utils/                  (text_utils.py)
│   │       ├── models/
│   │       └── schemas/
│   └── nex-shared/                     ✅ Placeholder
│
├── docs/
│   ├── SESSION_NOTES.md                ✅ This file
│   ├── INIT_PROMPT_NEW_CHAT.md         ✅ Ready
│   └── MIGRATION_SUMMARY.md            ✅ Created
│
├── tools/scripts/
├── pyproject.toml                      ✅ UV workspace config
└── README.md                           ✅ Created
```

---

## 🔧 Technical Details

### Python Environment
- **Version:** Python 3.13 32-bit (later tests showed 3.11 32-bit used)
- **Reason:** Btrieve requires 32-bit Python (NEX Genesis ERP dependency)
- **Package Manager:** pip (UV má problémy s 32-bit packages)

### Key Dependencies
**invoice-shared:**
- asyncpg>=0.29.0 ✅
- pydantic>=2.0.0 ✅

**supplier-invoice-loader:**
- fastapi, uvicorn, pypdf, pillow ✅
- psutil (optional - not installed due to C++ compiler requirement) ⚠️

**Development:**
- pytest, black, ruff ✅

### Import Pattern Changes
```python
# PRED (single repo)
from src.database.postgres_staging import PostgresStagingClient
from src.utils.text_utils import clean_string

# PO (monorepo)
from invoice_shared.database.postgres_staging import PostgresStagingClient
from invoice_shared.utils.text_utils import clean_string
```

### Monitoring API Changes
```python
# PRED
monitoring.metrics.increment_api_request()
monitoring.metrics.increment_processed()
monitoring.ApplicationMetrics()

# PO
monitoring.get_metrics().increment_request()
monitoring.get_metrics().increment_invoice(success=True)
monitoring.Metrics()
monitoring.reset_metrics()
```

---

## 📊 Test Results

**Latest Run:** 2025-11-18
```
46 passed, 14 failed, 11 skipped
```

**Passing Test Suites:**
- ✅ test_config.py: 14/14 passing
- ✅ test_notifications.py: 15/15 passing (1 skipped)
- ✅ test_api.py: 17/20 passing

**Failing Test Suites:**
- ❌ test_monitoring.py: 3/22 passing (9 skipped, 10 failed)
  - API mismatches: increment_processed(), get_uptime_seconds(), etc.

**Skipped Tests:**
- check_storage_health(), check_database_health()
- check_smtp_config(), get_system_info()
- get_health_status(), get_detailed_status()
- get_metrics_prometheus()
- (Features removed from simplified monitoring.py)

---

## 🐛 Known Issues

### 1. Monitoring API Incompatibility
**Problem:** Tests expect old API methods
**Impact:** 10 tests failing
**Solution Options:**
a) Add legacy methods to Metrics class
b) Update tests to new API
c) Skip tests temporarily

### 2. C++ Compiler Dependencies
**Problem:** psutil, greenlet require C++ compiler for 32-bit Python 3.13
**Solution:** Made psutil optional, removed SQLAlchemy
**Status:** ✅ Resolved

### 3. Ad-hoc Test Scripts
**Problem:** Tests with top-level exit() calls crash pytest
**Solution:** Moved to scripts/ as manual_test_*.py
**Status:** ✅ Resolved

---

## 📝 Scripts Created

All scripts in `C:/Development/nex-automat/`:

1. **setup_nex_automat_monorepo.py** - Initial structure
2. **copy_projects_to_monorepo.py** - FÁZA 1: Copy projects
3. **create_invoice_shared.py** - FÁZA 2: Extract shared code
4. **update_all_imports.py** - FÁZA 3: Update imports
5. **fix_workspace_dependencies.py** - UV workspace config
6. **fix_root_pyproject.py** - Remove build-system from root
7. **fix_hatch_build_config.py** - Hatchling packages config
8. **fix_extraction_test.py** - Move ad-hoc tests
9. **fix_all_broken_tests.py** - Find & move exit() tests
10. **add_missing_dependencies.py** - Add psutil
11. **fix_monitoring_optional_psutil.py** - Optional psutil
12. **fix_conftest_metrics.py** - Update conftest.py
13. **fix_import_and_monitoring_errors.py** - Import fixes
14. **fix_remaining_test_errors.py** - Final test fixes

---

## 🎯 Success Criteria

### Phase 1: Setup ✅ DONE
- [x] Monorepo structure created
- [x] Both projects migrated
- [x] Shared package created
- [x] Imports updated

### Phase 2: Testing ⏳ IN PROGRESS
- [x] 40+ tests passing (46/71 ✅)
- [ ] All critical tests passing (14 failing)
- [ ] No import errors (✅ resolved)

### Phase 3: Documentation 📋 TODO
- [ ] MONOREPO_GUIDE.md
- [ ] CONTRIBUTING.md
- [ ] Architecture documentation

### Phase 4: Git 📋 TODO
- [ ] Initial commit
- [ ] Create GitHub repo
- [ ] Push to GitHub

---

## 🔗 Resources

**Project Location:** `C:/Development/nex-automat/`

**Original Repos:**
- `C:/Development/supplier-invoice-loader` (source)
- `C:/Development/invoice-editor` (source)

**Documentation:**
- UV Workspace: https://docs.astral.sh/uv/concepts/workspaces/
- Python Packaging: https://packaging.python.org/

**Developer:**
- Zoltán Rausch (rausch@icc.sk)
- ICC Komárno - Innovation & Consulting Center

---

## 💡 Lessons Learned

1. **32-bit Python Constraint:** Some packages (greenlet, psutil) don't have pre-built wheels for 32-bit Python 3.13 → use pip, make dependencies optional
2. **Ad-hoc Test Scripts:** Tests with top-level code crash pytest → always wrap in functions
3. **API Changes:** When refactoring, update both code AND tests simultaneously
4. **UV Workspace:** Requires explicit tool.uv.sources for workspace dependencies
5. **Monorepo Benefits:** Shared code DRY, consistent versions, easier refactoring

---

**Last Updated:** 2025-11-18 (Session End)
**Next Session:** Continue with test fixes (monitoring API alignment)