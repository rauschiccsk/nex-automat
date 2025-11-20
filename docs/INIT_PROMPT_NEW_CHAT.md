# NEX Automat - New Chat Initialization

**Project:** nex-automat  
**Location:** C:/Development/nex-automat  
**GitHub:** https://github.com/rauschiccsk/nex-automat  
**Last Session:** 2025-11-20

---

## 📋 Quick Context

Claude, prosím načítaj kontext projektu pomocou týchto manifestov:

### Root Overview
```
web_fetch('https://raw.githubusercontent.com/rauschiccsk/nex-automat/main/docs/PROJECT_MANIFEST.json')
```

### Session Notes
```
web_fetch('https://raw.githubusercontent.com/rauschiccsk/nex-automat/main/docs/SESSION_NOTES.md')
```

### Ak pracujem na konkrétnom app:
```
# Supplier Invoice Loader
web_fetch('https://raw.githubusercontent.com/rauschiccsk/nex-automat/main/docs/apps/supplier-invoice-loader.json')

# Supplier Invoice Editor
web_fetch('https://raw.githubusercontent.com/rauschiccsk/nex-automat/main/docs/apps/supplier-invoice-editor.json')
```

---

## 🎯 Current Project Status

### ✅ COMPLETE (Ready to use)
- Monorepo structure with 2 apps, 2 packages
- Python 3.13.7 32-bit venv32
- Testing: 71/86 passing (83% coverage)
- **End-to-End workflow TESTED and WORKING** ✅
- Documentation complete with GitHub URLs
- Git repository public and up-to-date

### 🔄 RECENT UPDATES (2025-11-20)
- ✅ E2E testing workflow implemented
- ✅ Manifest system enhanced with GitHub URLs
- ✅ Editor database connection fixed
- ✅ pg8000 dependency added
- ✅ Full workflow verified (Email → n8n → FastAPI → DB → GUI)

### 📋 TODO (Next priorities)
1. Production deployment monitoring
2. Error handling improvements
3. Additional test coverage
4. Performance optimization

---

## 🗂️ Project Structure

```
nex-automat/
├── apps/
│   ├── supplier-invoice-loader/    # FastAPI service (85% tested)
│   │   ├── src/
│   │   ├── tests/
│   │   │   └── samples/           # 18 test PDF invoices
│   │   └── pyproject.toml
│   └── supplier-invoice-editor/    # PyQt5 desktop app (71% tested)
│       ├── src/
│       │   ├── business/          # invoice_service.py
│       │   ├── database/          # postgres_client.py
│       │   └── ui/                # PyQt5 widgets
│       ├── tests/
│       ├── config/
│       │   └── config.yaml        # DB config
│       └── pyproject.toml
├── packages/
│   ├── invoice-shared/            # Shared utilities
│   └── nex-shared/                # NEX Genesis utilities
├── docs/
│   ├── guides/
│   ├── SESSION_NOTES.md
│   ├── PROJECT_MANIFEST.json      # ✅ With GitHub URLs
│   ├── apps/                      # ✅ Per-app manifests
│   └── packages/                  # ✅ Per-package manifests
├── scripts/
│   └── generate_projects_access.py # ✅ Updated with github_raw
├── e2e_test_workflow.py           # ✅ NEW - E2E testing
├── diagnose_editor_db.py          # ✅ NEW - DB diagnostics
└── venv32/                        # Python 3.13.7 32-bit + pg8000
```

---

## 🔧 Environment

**Python:** 3.13.7 32-bit (Btrieve compatibility)  
**venv:** venv32 (gitignored)  
**Package Manager:** pip  
**IDE:** PyCharm

**Key Dependencies:**
- FastAPI, Uvicorn (loader)
- PyQt5, PyYAML (editor)
- asyncpg, pg8000 (PostgreSQL)
- invoice-shared (workspace package)

**NEW Dependencies (2025-11-20):**
- pg8000==1.31.5 (pure Python PostgreSQL driver)

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Expected: 71 passed, 15 skipped, 0 failed
```

**Coverage:**
- supplier-invoice-loader: 61/72 (85%)
- supplier-invoice-editor: 10/14 (71%)

**E2E Testing:**
```bash
# Full workflow test (Email → n8n → FastAPI → DB → GUI)
python e2e_test_workflow.py

# Database diagnostics
python diagnose_editor_db.py
```

---

## 📊 E2E Workflow

**Email:** magerstavinvoice@gmail.com  
**n8n:** Active workflow on localhost  
**FastAPI:** https://magerstav-invoices.icc.sk  
**Database:** invoice_staging (PostgreSQL)  
**Table:** invoices_pending (2 pending invoices)

**Test Flow:**
1. Send email with PDF attachment
2. n8n IMAP trigger (30s delay)
3. n8n → FastAPI /invoice endpoint
4. FastAPI → PostgreSQL
5. GUI Editor displays invoices

**Status:** ✅ Fully tested and working

---

## 🔑 Important Notes

### Critical Rules:
1. **32-bit Python only** (Btrieve requirement)
2. **Install order matters:** packages first, then apps
3. **Always run tests** before committing
4. **Regenerate manifests** after structural changes
5. **pg8000 required** for editor DB connection

### Known Working Configuration:
- Gmail: App Password authentication
- PostgreSQL: invoice_staging database
- Editor: Real DB connection (no stub data)
- n8n: IMAP trigger with 30s polling

### Recent Fixes:
- ✅ invoice_service.py import path fixed
- ✅ invoices_pending table name corrected
- ✅ GitHub URLs added to all manifest files
- ✅ pg8000 dependency installed

---

## 🚀 Quick Commands Reference

```bash
# Setup (if needed)
.\venv32\Scripts\Activate.ps1

# Install packages
pip install -e packages/invoice-shared -e packages/nex-shared
pip install -e apps/supplier-invoice-loader -e apps/supplier-invoice-editor

# Test
pytest
python e2e_test_workflow.py
python diagnose_editor_db.py

# Run services
cd apps/supplier-invoice-loader
python main.py  # → http://localhost:8000/docs

cd apps/supplier-invoice-editor
python main.py  # → GUI Editor

# Regenerate manifests
python scripts/generate_projects_access.py
```

---

## 📁 Database Schema

**Database:** invoice_staging  
**Main Table:** invoices_pending

**Columns:**
- id, invoice_number, invoice_date, due_date
- supplier_name, supplier_ico, supplier_dic
- total_amount, total_vat, total_without_vat, currency
- status (pending/approved/rejected)
- nex_pab_code, nex_doc_number, nex_book, nex_book_type
- created_at, approved_at, imported_at, rejected_at
- error_message, rejection_reason, isdoc_xml

---

## 🎯 Common Tasks

### Run E2E Test
```bash
python e2e_test_workflow.py
# Sends email → n8n → FastAPI → DB → GUI
```

### Diagnose DB Connection
```bash
python diagnose_editor_db.py
# Checks: pg8000, config, connection, data
```

### Add New Invoice (via email)
1. Send email with PDF to magerstavinvoice@gmail.com
2. Wait 30 seconds for n8n processing
3. Check database: `SELECT * FROM invoices_pending ORDER BY created_at DESC LIMIT 5`
4. Open GUI Editor to view

### Fix Editor DB Connection
If editor shows stub data:
1. Check pg8000: `pip list | grep pg8000`
2. Run diagnostics: `python diagnose_editor_db.py`
3. Verify config: `type apps\supplier-invoice-editor\config\config.yaml`
4. Check import paths in invoice_service.py

---

## 📚 Key Documentation Files

- **README.md** - Project overview
- **docs/guides/MONOREPO_GUIDE.md** - Development guide
- **docs/guides/CONTRIBUTING.md** - Contribution guidelines
- **docs/SESSION_NOTES.md** - Current status and history
- **apps/supplier-invoice-editor/docs/POSTGRESQL_SETUP.md** - DB setup

---

## 🔗 GitHub Repository

**URL:** https://github.com/rauschiccsk/nex-automat  
**Status:** Public, up-to-date  
**Manifests:** All files have github_raw URLs  

**Access Pattern:**
```python
# Load manifest
manifest = web_fetch('https://raw.githubusercontent.com/rauschiccsk/nex-automat/main/docs/apps/supplier-invoice-editor.json')

# Access any file
config = web_fetch(manifest['files'][X]['github_raw'])
```

---

## ✅ Pre-Session Checklist

Before starting work:
- [ ] Load PROJECT_MANIFEST.json
- [ ] Read SESSION_NOTES.md for current status
- [ ] Activate venv: `.\venv32\Scripts\Activate.ps1`
- [ ] Verify environment: `python diagnose_editor_db.py`

---

**Developer:** Zoltán Rausch (rausch@icc.sk)  
**Organization:** ICC Komárno - Innovation & Consulting Center  
**Project Version:** 2.0.0  
**Status:** Production Ready ✅  
**Last E2E Test:** 2025-11-20 ✅ Success