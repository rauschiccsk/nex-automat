# NEX Automat - Init Prompt for New Chat

**Project:** nex-automat  
**Type:** Python Monorepo (pip-based, UV compatible)  
**Location:** C:/Development/nex-automat  
**Generated:** 2025-11-18

---

## 🎯 Project Status

**Monorepo Migration:** ✅ **95% COMPLETE**

**What's Done:**
- ✅ Monorepo structure created (apps/, packages/, docs/, tools/)
- ✅ Both projects migrated and renamed
- ✅ Shared package (invoice-shared) extracted and working
- ✅ All imports updated to use invoice_shared.*
- ✅ Dependencies installed via pip (32-bit Python compatible)
- ✅ 46/71 tests passing ⚡

**What's Remaining:**
- 14 tests failing (monitoring API mismatches)
- Final documentation
- Git repository setup

---

## 📂 Project Structure

```
C:/Development/nex-automat/
├── apps/
│   ├── supplier-invoice-loader/        # Email → NEX invoice automation
│   └── supplier-invoice-editor/        # GUI approval workflow
│
├── packages/
│   ├── invoice-shared/                 # Shared: postgres_staging, text_utils
│   └── nex-shared/                     # Common NEX utilities (placeholder)
│
├── docs/
│   ├── SESSION_NOTES.md                # ← LOAD THIS FIRST!
│   └── INIT_PROMPT_NEW_CHAT.md         # This file
│
├── tools/scripts/                      # Build & migration scripts
└── pyproject.toml                      # Workspace config
```

---

## 🚀 Quick Start for New Chat

### Step 1: Load Context
```
Claude, please load: C:/Development/nex-automat/docs/SESSION_NOTES.md
```

### Step 2: Review Current Status
Look for these sections in SESSION_NOTES.md:
- **Current Status** → What's done
- **In Progress** → What's being worked on
- **Next Steps** → What to do next (PRIORITY items)

### Step 3: Continue Work
Focus on **PRIORITY 1** from Next Steps:
```
Opraviť monitoring API alignment v testoch
```

---

## 🔧 Technology Stack

- **Python:** 3.11/3.13 32-bit (Btrieve requirement)
- **Package Manager:** pip (not UV - 32-bit compatibility)
- **Workspace:** UV-compatible structure (manual pip install)
- **Apps:** FastAPI, asyncpg, pypdf, pillow
- **Testing:** pytest, pytest-asyncio

---

## 📋 Key Facts

### Python Environment
- **32-bit Python REQUIRED** - NEX Genesis ERP uses 32-bit Btrieve
- **pip preferred over UV** - better 32-bit package support
- **psutil is optional** - requires C++ compiler, made optional

### Import Patterns
```python
# Shared code usage
from invoice_shared.database.postgres_staging import PostgresStagingClient
from invoice_shared.utils.text_utils import clean_string

# Monitoring API
monitoring.get_metrics().increment_request()
monitoring.get_metrics().increment_invoice(success=True)
monitoring.reset_metrics()
```

### Database
- **PostgreSQL:** invoice_staging (shared between apps)
- **Tables:** invoices_pending, invoice_items_pending
- **Client:** packages/invoice-shared/invoice_shared/database/postgres_staging.py

---

## 🎯 Current Priority Tasks

### PRIORITY 1: Fix Monitoring Tests (14 failing)

**Problem:** Tests expect old API methods that don't exist in new Metrics class

**Failed Tests:**
1. `test_api.py::test_status_endpoint_with_auth` - check_storage_health() missing
2. `test_api.py::test_api_metrics_increment` - api_requests attribute missing
3. `test_monitoring.py` - 10 tests with API mismatches

**Solutions (choose one):**

**Option A: Add Legacy Methods to Metrics Class**
```python
# In monitoring.py, add:
def increment_processed(self):
    self.invoices_processed += 1

def increment_failed(self):
    self.invoices_failed += 1

def get_uptime_seconds(self):
    return self.get_uptime()

# etc.
```

**Option B: Update Tests to New API**
```python
# In tests, change:
metrics.increment_processed() → metrics.increment_invoice(success=True)
metrics.increment_failed() → metrics.increment_invoice(success=False)
metrics.get_uptime_seconds() → metrics.get_uptime()
```

**Option C: Skip All Monitoring Tests**
```python
# Add to all failing tests:
@pytest.mark.skip(reason="Monitoring API refactoring in progress")
```

**Recommendation:** Option A (add legacy methods) - quickest path to green tests

---

## 🧪 Testing Commands

```bash
# Quick test run (summary only)
cd C:/Development/nex-automat/apps/supplier-invoice-loader
pytest --tb=no -q

# Run specific test file
pytest tests/unit/test_monitoring.py -v

# Stop on first failure
pytest -x --tb=short

# Current status: 46 passed, 14 failed, 11 skipped
```

---

## 🛠️ Common Operations

### Running Scripts
All scripts are in root: `C:/Development/nex-automat/`
```bash
cd C:/Development/nex-automat
python <script_name>.py
```

### Installing Dependencies
```bash
# From monorepo root
pip install -e packages/invoice-shared
pip install -e apps/supplier-invoice-loader
pip install -e apps/supplier-invoice-editor
```

### Modifying Code
All changes done via Python scripts:
```python
# Pattern:
# 1. Read file
# 2. Modify content
# 3. Write back
# 4. No manual editing
```

---

## ⚠️ Critical Constraints

### 1. 32-bit Python Requirement
- NEX Genesis ERP Btrieve database requires 32-bit Python
- Some packages (psutil, greenlet) don't have 32-bit wheels for Python 3.13
- Solution: Use pip (better 32-bit support), make problematic deps optional

### 2. No UV Package Manager
- UV has issues with 32-bit packages
- Use pip for installations
- Keep UV-compatible structure for future

### 3. Monitoring API Evolution
- Old API: `monitoring.metrics.increment_processed()`
- New API: `monitoring.get_metrics().increment_invoice(success=True)`
- Tests need updating or legacy methods needed

---

## 📝 Script Inventory

All migration scripts in `C:/Development/nex-automat/`:

**Setup & Migration:**
1. setup_nex_automat_monorepo.py
2. copy_projects_to_monorepo.py
3. create_invoice_shared.py
4. update_all_imports.py

**Configuration Fixes:**
5. fix_workspace_dependencies.py
6. fix_root_pyproject.py
7. fix_hatch_build_config.py

**Test Fixes:**
8. fix_extraction_test.py
9. fix_all_broken_tests.py
10. fix_conftest_metrics.py
11. fix_import_and_monitoring_errors.py
12. fix_remaining_test_errors.py

**Dependencies:**
13. add_missing_dependencies.py
14. fix_monitoring_optional_psutil.py
15. install_dependencies_pip.py

---

## 🎓 What Claude Should Know

### When Starting New Chat:
1. **Always load SESSION_NOTES.md first**
2. Look at Current Status section
3. Check Next Steps for PRIORITY tasks
4. Ask user to confirm before starting work

### When Creating Scripts:
- Place all scripts in root: `C:/Development/nex-automat/`
- Never in subdirectories
- Use pathlib.Path for cross-platform compatibility
- Always print progress and results

### When Fixing Code:
- Create Python scripts, not manual edits
- Test after each change
- Update SESSION_NOTES.md with progress

### Communication Style:
- Slovak language (English for technical terms)
- Step-by-step approach
- Wait for confirmation before next step
- One solution, no alternatives (unless requested)

---

## 📞 Contact

**Developer:** Zoltán Rausch  
**Email:** rausch@icc.sk  
**Organization:** ICC Komárno (Innovation & Consulting Center)  
**GitHub:** @rauschiccsk

---

## 🎬 Recommended First Message in New Chat

```
Claude, prosím načítaj kontext z tohto projektu:

Súbor: C:/Development/nex-automat/docs/SESSION_NOTES.md

Pozri si sekcie:
- Current Status (čo je hotové)
- Next Steps (čo treba urobiť)

Potom mi povedz:
1. Aký je aktuálny stav projektu
2. Čo je nasledujúca priorita
3. Či máme pokračovať

Ďakujem!
```

---

**End of Init Prompt**

**Project:** nex-automat monorepo  
**Status:** 95% complete, testing phase  
**Next:** Fix monitoring tests (14 failing)