# NEX Automat - New Chat Initialization

**Project:** nex-automat  
**Location:** C:/Development/nex-automat  
**GitHub:** https://github.com/[username]/nex-automat  
**Last Session:** 2025-11-19

---

## 📋 Quick Context

Claude, prosím načítaj kontext projektu pomocou týchto manifestov:

### Root Overview
```
web_fetch('https://raw.githubusercontent.com/[username]/nex-automat/main/docs/PROJECT_MANIFEST.json')
```

### Session Notes
```
web_fetch('https://raw.githubusercontent.com/[username]/nex-automat/main/docs/SESSION_NOTES.md')
```

### Ak pracujem na konkrétnom app:
```
# Supplier Invoice Loader
web_fetch('https://raw.githubusercontent.com/[username]/nex-automat/main/docs/apps/supplier-invoice-loader.json')

# Supplier Invoice Editor
web_fetch('https://raw.githubusercontent.com/[username]/nex-automat/main/docs/apps/supplier-invoice-editor.json')
```

---

## 🎯 Current Project Status

### ✅ COMPLETE (Ready to use)
- Monorepo structure with 2 apps, 2 packages
- Python 3.13.7 32-bit venv32
- Testing: 71/86 passing (83% coverage)
- Documentation complete
- Git repository ready

### 📋 TODO (Next priorities)
1. CI/CD Setup (GitHub Actions)
2. Additional apps migration
3. Production deployment
4. Advanced testing

---

## 🏗️ Project Structure

```
nex-automat/
├── apps/
│   ├── supplier-invoice-loader/    # FastAPI service (85% tested)
│   └── supplier-invoice-editor/    # PyQt5 desktop app (71% tested)
├── packages/
│   ├── invoice-shared/             # Shared utilities
│   └── nex-shared/                 # NEX Genesis utilities (placeholder)
├── docs/
│   ├── guides/
│   │   ├── MONOREPO_GUIDE.md
│   │   └── CONTRIBUTING.md
│   ├── SESSION_NOTES.md
│   └── PROJECT_MANIFEST.json
└── venv32/                         # Python 3.13.7 32-bit
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
- asyncpg (PostgreSQL)
- invoice-shared (workspace package)

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

---

## 📝 Development Workflow

```bash
# Activate venv
.\venv32\Scripts\Activate.ps1

# Install/update packages
pip install -e packages/invoice-shared -e packages/nex-shared
pip install -e apps/supplier-invoice-loader -e apps/supplier-invoice-editor

# Run tests
pytest

# Format code
black .
ruff check . --fix

# Generate manifests
python generate_projects_access.py
```

---

## 🎯 Common Tasks

### Add New App
1. Create directory in apps/
2. Create pyproject.toml
3. Install: `pip install -e apps/new-app`
4. Add tests
5. Regenerate manifests

### Fix Tests
1. Identify failing tests
2. Fix code or update tests
3. Verify: `pytest apps/app-name/tests/ -v`
4. Update SESSION_NOTES.md

### Update Documentation
1. Edit docs/*.md files
2. Regenerate manifests if structure changed
3. Commit and push

---

## 📚 Key Documentation Files

- **README.md** - Project overview and quick start
- **docs/guides/MONOREPO_GUIDE.md** - Development guide
- **docs/guides/CONTRIBUTING.md** - Contribution guidelines
- **docs/SESSION_NOTES.md** - Current status and history

---

## 💡 Important Notes

### Critical Rules:
1. **32-bit Python only** (Btrieve requirement)
2. **Install order matters:** packages first, then apps
3. **Always run tests** before committing
4. **Regenerate manifests** after structural changes

### Known Issues:
- psutil not installed (C++ compiler required)
- Some Qt tests require display server
- Integration tests need --run-integration flag

---

## 🚀 Quick Commands Reference

```bash
# Setup new venv (if needed)
& "C:\Program Files (x86)\Python313-32\python.exe" -m venv venv32
.\venv32\Scripts\Activate.ps1

# Install everything
pip install -e packages/invoice-shared -e packages/nex-shared
pip install -e apps/supplier-invoice-loader -e apps/supplier-invoice-editor
pip install pytest pytest-asyncio pytest-cov pytest-qt black ruff

# Test specific app
pytest apps/supplier-invoice-loader/tests/ -v
pytest apps/supplier-invoice-editor/tests/ -v

# Run loader API
cd apps/supplier-invoice-loader
python main.py
# → http://localhost:8000/docs

# Run editor GUI
cd apps/supplier-invoice-editor
python main.py

# Cleanup
python cleanup_monorepo.py

# Generate manifests
python generate_projects_access.py
```

---

## 📊 Git Repository

**Status:** All changes committed and pushed  
**Commits:** 6 (migration, docs, tests, cleanup)  
**Branch:** main  
**Remote:** GitHub

**Recent Commits:**
1. feat: Complete monorepo migration with venv32 setup
2. docs: add comprehensive project documentation
3. test: add basic tests for supplier-invoice-editor
4. docs: update README with editor info and cleanup monorepo

---

## 🎯 Session Objectives Template

When starting new session, define:
1. **Primary Goal:** What to achieve
2. **Expected Output:** Deliverables
3. **Success Criteria:** How to measure completion
4. **Time Budget:** Estimated duration

---

## ✅ Pre-Session Checklist

Before starting work:
- [ ] Pull latest changes: `git pull origin main`
- [ ] Activate venv: `.\venv32\Scripts\Activate.ps1`
- [ ] Verify tests pass: `pytest --tb=no -q`
- [ ] Check SESSION_NOTES.md for context

After session:
- [ ] Run tests: `pytest`
- [ ] Update SESSION_NOTES.md
- [ ] Commit changes with proper message
- [ ] Push to GitHub

---

**Developer:** Zoltán Rausch (rausch@icc.sk)  
**Organization:** ICC Komárno - Innovation & Consulting Center  
**Project Version:** 2.0.0  
**Status:** Production Ready ✅