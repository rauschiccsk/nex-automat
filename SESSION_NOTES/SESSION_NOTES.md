# SESSION NOTES - nex-automat v2.3

## CURRENT STATUS

**Verzia:** v2.3 ✅  
**Status:** Production Deployed  
**Posledná zmena:** 2025-12-08

### Production Deployment (Magerstav)
- **Lokácia:** `C:\Deployment\nex-automat`
- **Verzia:** v2.3
- **Service:** NEXAutomat (Running) ✅
- **API:** http://localhost:8000 ✅
- **Health Check:** 200 OK ✅

### Development
- **Lokácia:** `C:\Development\nex-automat`
- **Branch:** develop
- **Verzia:** v2.3
- **Python:** 3.13.7 (venv32)

---

## VERSION HISTORY

### v2.3 (2025-12-08) - Migration Success ✅

**Problem Solved:**
- supplier-invoice-loader používal neexistujúci `invoice-shared` package
- v2.2 deployment FAILED kvôli missing dependencies

**Migrated to nex-shared:**
- `clean_string` → `nex-shared/utils/text_utils.py`
- `PostgresStagingClient` → `nex-shared/database/postgres_staging.py`

**Files Created:**
- `packages/nex-shared/utils/text_utils.py`
- `packages/nex-shared/database/postgres_staging.py`
- `scripts/01_migrate_invoice_shared_v2.3.py`
- `scripts/02_fix_utils_init.py`

**Files Updated:**
- `packages/nex-shared/utils/__init__.py` (exports)
- `packages/nex-shared/database/__init__.py` (exports)
- `apps/supplier-invoice-loader/main.py` (imports)
- `apps/supplier-invoice-loader/scripts/test_invoice_integration.py` (imports)

**Testing:**
- ✅ nex-shared reinstalled successfully
- ✅ supplier-invoice-loader starts without errors
- ✅ API health check: http://localhost:8001/health → 200 OK (dev)
- ✅ API health check: http://localhost:8000/health → 200 OK (production)

**Deployment:**
- ✅ Git push develop + main + tags
- ✅ Magerstav deployment successful
- ✅ Service NEXAutomat running
- ✅ Imports verified

---

### v2.2 (2025-12-06) - BaseGrid Pattern + Cleanup ✅

**Features:**
- Universal BaseGrid pattern v nex-shared
- Grid persistence (column widths, active column)
- QuickSearch integration
- Cleanup backup files (vymazaných 17 .backup súborov)

**Known Issue:**
- v2.2 deployment FAILED pre loader (používal invoice-shared)
- Rollback na v2.0.0 ✅
- Fixed in v2.3 ✅

---

### v2.0.0 (2025-11-12) - Initial Stable Release

**Applications:**
- supplier-invoice-editor - PyQt5 desktop app
- supplier-invoice-loader - FastAPI service

**Packages:**
- nex-shared - UI components, utilities
- nexdata - Btrieve/NEX Genesis access

---

## ARCHITECTURE

### Project Structure

```
nex-automat/
├── apps/
│   ├── supplier-invoice-editor/    # PyQt5 Desktop App
│   │   ├── src/
│   │   │   ├── ui/widgets/
│   │   │   │   ├── invoice_list_widget.py    (BaseGrid)
│   │   │   │   ├── invoice_items_grid.py     (BaseGrid)
│   │   │   │   └── quick_search.py
│   │   │   ├── business/
│   │   │   ├── database/
│   │   │   └── utils/
│   │   └── tests/
│   │
│   └── supplier-invoice-loader/    # FastAPI Service
│       ├── main.py
│       ├── src/
│       │   ├── api/
│       │   ├── business/
│       │   ├── database/
│       │   ├── extractors/
│       │   └── utils/
│       └── tests/
│
├── packages/
│   ├── nex-shared/                 # Shared Components v1.0.0
│   │   ├── ui/
│   │   │   ├── base_grid.py       # Universal BaseGrid
│   │   │   └── base_window.py
│   │   ├── utils/
│   │   │   ├── grid_settings.py   # Grid persistence
│   │   │   └── text_utils.py      # clean_string (v2.3)
│   │   └── database/
│   │       ├── window_settings_db.py
│   │       └── postgres_staging.py  # PostgresStagingClient (v2.3)
│   │
│   └── nexdata/                    # Btrieve Access
│       └── ...
│
└── scripts/                        # Migration Scripts
    ├── 01_migrate_invoice_shared_v2.3.py
    ├── 02_fix_utils_init.py
    ├── 03_deploy_v2.3_magerstav.ps1
    └── cleanup_backup_files.py
```

---

## KEY PATTERNS

### 1. BaseGrid Pattern (v2.2)

**Purpose:** Universal grid with persistence and quick search

**Features:**
- Auto QTableView + GreenHeaderView
- Auto grid persistence (column widths, active column)
- QuickSearch integration
- Load/save settings automatically

**Usage:**
```python
from nex_shared.ui import BaseGrid

class MyGrid(BaseGrid):
    def __init__(self, parent=None):
        super().__init__(
            window_name="my_window",
            grid_name="my_grid",
            parent=parent
        )
        self.setup_model()  # Your model setup
```

---

### 2. Migration Pattern (v2.3)

**From:** `invoice-shared` (deleted package)  
**To:** `nex-shared` (unified package)

**Process:**
1. Identify functions/classes in old package
2. Create in nex-shared (utils/ or database/)
3. Update __init__.py exports
4. Update imports in apps
5. Test locally
6. Git commit + tag
7. Deployment

**Example Migration:**
```python
# OLD (v2.2)
from invoice_shared.utils.text_utils import clean_string
from invoice_shared.database.postgres_staging import PostgresStagingClient

# NEW (v2.3)
from nex_shared.utils import clean_string
from nex_shared.database import PostgresStagingClient
```

---

## PERSISTENCE LOCATIONS

### SQLite Databases
```
Window settings: C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db
Grid settings:   C:\NEX\YEARACT\SYSTEM\SQLITE\grid_settings.db
```

### PostgreSQL Staging
```
Database: invoice_staging
Host: localhost:5432
Tables:
  - invoices_pending
  - invoice_items_pending
  - invoice_log
  - categories_cache
  - products_staging
  - barcodes_staging
```

---

## WORKFLOW

### Development → Git → Deployment

1. **Development** (`C:\Development\nex-automat`)
   - Make changes
   - Test locally
   - Create migration scripts
   - Commit to develop branch

2. **Git Operations**
   ```powershell
   git add .
   git commit -m "message"
   git tag vX.X
   git checkout main
   git merge develop
   git push origin develop main --tags
   ```

3. **Deployment** (`C:\Deployment\nex-automat`)
   ```powershell
   Stop-Service NEXAutomat
   git checkout main
   git pull origin main
   git fetch --tags
   cd packages\nex-shared
   pip install -e .
   Start-Service NEXAutomat
   ```

---

## SERVICES (Magerstav)

### Active Services
- **NEXAutomat** - supplier-invoice-loader API (port 8000) ✅ POUŽÍVA SA

### Inactive Services
- **SupplierInvoiceLoader** - duplicitná služba ❌ NEPOUŽIVA SA

---

## TESTING

### Local Testing
```powershell
# Editor
cd apps\supplier-invoice-editor
python main.py

# Loader
cd apps\supplier-invoice-loader
python main.py
# API: http://localhost:8001
# Health: http://localhost:8001/health
```

### Production Testing
```powershell
# Health check
Invoke-WebRequest -Uri "http://localhost:8000/health"

# Service status
Get-Service NEXAutomat
```

---

## DEPENDENCIES

### Core Dependencies
```
PyQt5>=5.15.0          # Desktop UI
fastapi                # API framework
uvicorn                # ASGI server
asyncpg                # PostgreSQL async
pydantic               # Data validation
nexdata                # Btrieve access
pg8000                 # PostgreSQL pure Python (v2.3)
```

### Development
```
pytest                 # Testing
black                  # Code formatting
```

---

## KNOWN ISSUES

### Resolved
- ✅ v2.2 deployment failed for loader → Fixed in v2.3
- ✅ invoice-shared dependency → Migrated to nex-shared
- ✅ Grid settings persistence → Implemented in v2.2
- ✅ Quick search active column → Implemented in v2.2

### Current
- None ✅

---

## NEXT STEPS

### Immediate
- Monitor production deployment
- Verify invoice processing workflow

### Future
- Consider editor deployment (currently only loader deployed)
- Implement automated tests
- Add logging/monitoring improvements

---

## SCRIPTS INVENTORY

### Migration Scripts (Numbered)
- `01_migrate_invoice_shared_v2.3.py` - Migrate to nex-shared
- `02_fix_utils_init.py` - Fix __init__.py exports
- `03_deploy_v2.3_magerstav.ps1` - Deployment script

### Utility Scripts (Permanent)
- `cleanup_backup_files.py` - Remove .backup files
- Various database migration scripts in apps/

---

## CONTACTS

**Project:** nex-automat  
**Customer:** Mágerstav s.r.o.  
**Repository:** https://github.com/rauschiccsk/nex-automat

---

**Last Updated:** 2025-12-08  
**Current Version:** v2.3  
**Status:** ✅ Production Ready