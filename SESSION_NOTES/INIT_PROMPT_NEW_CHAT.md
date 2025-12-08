# INIT PROMPT - Nový chat (nex-automat v2.3)

## AKTUÁLNY STAV PROJEKTU

**Projekt:** nex-automat (NEX Automat v2.0)  
**Development:** `C:\Development\nex-automat`  
**Deployment:** `C:\Deployment\nex-automat`  
**Python:** 3.13.7 (venv32)  
**Git Branch:** develop  
**Aktuálna verzia:** v2.3 ✅

---

## PRODUCTION STATUS (Magerstav)

**Verzia:** v2.3 ✅  
**Lokácia:** `C:\Deployment\nex-automat`  
**Service:** NEXAutomat (Running) ✅  
**API:** http://localhost:8000  
**Health:** http://localhost:8000/health → 200 OK ✅

---

## ČO JE HOTOVÉ

### v2.3 - Migration Complete ✅
**Problem Solved:**
- supplier-invoice-loader používal vymazaný `invoice-shared` package
- v2.2 deployment FAILED → rollback na v2.0.0
- v2.3 migrácia → SUCCESS ✅

**Migrated to nex-shared:**
- `clean_string` → `nex-shared/utils/text_utils.py`
- `PostgresStagingClient` → `nex-shared/database/postgres_staging.py`

**Files Created:**
- `packages/nex-shared/utils/text_utils.py`
- `packages/nex-shared/database/postgres_staging.py`
- `scripts/01_migrate_invoice_shared_v2.3.py`
- `scripts/02_fix_utils_init.py`

**Testing:**
- ✅ Development: API na port 8001
- ✅ Production: API na port 8000
- ✅ Imports verified
- ✅ Service running

---

### v2.2 - BaseGrid Pattern ✅
**Features:**
- Universal BaseGrid pattern v nex-shared
- Grid persistence (column widths, active column)
- QuickSearch integration
- Cleanup backup files

**Known Issue:**
- Deployment FAILED pre loader → Fixed in v2.3 ✅

---

### v2.0.0 - Initial Release ✅
**Applications:**
- supplier-invoice-editor (PyQt5)
- supplier-invoice-loader (FastAPI)

**Packages:**
- nex-shared (UI components)
- nexdata (Btrieve access)

---

## ŠTRUKTÚRA PROJEKTU

```
nex-automat/
├── apps/
│   ├── supplier-invoice-editor/    # v2.2 (uses BaseGrid)
│   │   ├── src/
│   │   │   ├── ui/widgets/
│   │   │   │   ├── invoice_list_widget.py    (BaseGrid)
│   │   │   │   ├── invoice_items_grid.py     (BaseGrid)
│   │   │   │   └── quick_search.py
│   │   │   ├── business/
│   │   │   ├── database/
│   │   │   │   └── postgres_client.py
│   │   │   └── utils/
│   │   └── tests/
│   │
│   └── supplier-invoice-loader/    # v2.3 (uses nex-shared)
│       ├── main.py                 # Updated imports ✅
│       ├── src/
│       │   ├── api/
│       │   ├── business/
│       │   ├── database/
│       │   │   └── database.py     # SQLite operations
│       │   ├── extractors/
│       │   └── utils/
│       └── scripts/
│           └── test_invoice_integration.py  # Updated imports ✅
│
├── packages/
│   ├── nex-shared/                 # v1.0.0 with v2.3 additions
│   │   ├── ui/
│   │   │   ├── base_grid.py       # Universal BaseGrid
│   │   │   └── base_window.py
│   │   ├── utils/
│   │   │   ├── grid_settings.py   # Grid persistence
│   │   │   └── text_utils.py      # clean_string (NEW v2.3) ✅
│   │   └── database/
│   │       ├── window_settings_db.py
│   │       └── postgres_staging.py  # PostgresStagingClient (NEW v2.3) ✅
│   │
│   └── nexdata/                    # Btrieve access
│       └── ...
│
└── scripts/                        # Numbered migration scripts
    ├── 01_migrate_invoice_shared_v2.3.py
    ├── 02_fix_utils_init.py
    ├── 03_deploy_v2.3_magerstav.ps1
    └── cleanup_backup_files.py
```

---

## KRITICKÉ PRAVIDLÁ

### Workflow
1. **Development → Git → Deployment**
2. **NIKDY nerobiť zmeny priamo v Deployment!**
3. Všetky zmeny cez numbered scripts v `scripts/`

### Package štruktúra
- **nex-shared** - FLAT štruktúra (nex-shared appears ONLY ONCE in path)
- Po zmenách v nex-shared: `pip install -e .` v packages/nex-shared

### Import Pattern (v2.3)
```python
# SPRÁVNE (v2.3+)
from nex_shared.utils import clean_string
from nex_shared.database import PostgresStagingClient

# NESPRÁVNE (deprecated v2.2)
from invoice_shared.utils.text_utils import clean_string
from invoice_shared.database.postgres_staging import PostgresStagingClient
```

### Migration Best Practices
1. Najprv nájdi originálne implementácie
2. Skopíruj/presun do vhodného package
3. Update __init__.py exports
4. Update importov v aplikáciách
5. Test lokálne pred commitom
6. Git tag pre každú release verziu

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
User: postgres

Tables:
  - invoices_pending
  - invoice_items_pending  
  - invoice_log
  - categories_cache
  - products_staging
  - barcodes_staging
```

### Deployment Paths
```
Development: C:\Development\nex-automat
Deployment:  C:\Deployment\nex-automat
Persistence: C:\NEX\YEARACT\SYSTEM\SQLITE\
```

---

## SERVICES (Magerstav)

### Active Services
- **NEXAutomat** - supplier-invoice-loader API ✅  
  - Port: 8000
  - Status: Running
  - Health: http://localhost:8000/health

### Inactive Services  
- **SupplierInvoiceLoader** - duplicitná služba ❌ NEPOUŽÍVA SA

---

## TESTING

### Development Testing
```powershell
# 1. Test nex-shared imports
cd C:\Development\nex-automat
python -c "from nex_shared.utils import clean_string; from nex_shared.database import PostgresStagingClient; print('OK')"

# 2. Test loader
cd apps\supplier-invoice-loader
python main.py
# API: http://localhost:8001
# Health: http://localhost:8001/health

# 3. Test editor
cd ..\supplier-invoice-editor
python main.py
```

### Production Testing
```powershell
# 1. Service status
Get-Service NEXAutomat

# 2. API health
Invoke-WebRequest -Uri "http://localhost:8000/health"

# 3. Verify imports
cd C:\Deployment\nex-automat\apps\supplier-invoice-loader
python -c "from nex_shared.utils import clean_string; from nex_shared.database import PostgresStagingClient; print('OK')"
```

---

## DEPLOYMENT PROCESS

### 1. Development
```powershell
cd C:\Development\nex-automat

# Make changes
# Create migration script if needed
# Test locally

# Git operations
git add .
git commit -m "message"
git tag vX.X
git checkout main
git merge develop
git push origin develop main --tags
git checkout develop
```

### 2. Deployment (Magerstav)
```powershell
cd C:\Deployment\nex-automat

# Stop service
Stop-Service NEXAutomat

# Pull latest
git checkout main
git pull origin main
git fetch --tags

# Reinstall packages if needed
cd packages\nex-shared
pip install -e .

# Start service
Start-Service NEXAutomat

# Verify
Invoke-WebRequest -Uri "http://localhost:8000/health"
```

---

## DEBUG TOOLS

### Development
```powershell
cd C:\Development\nex-automat

# Check imports
Get-ChildItem -Path . -Include *.py -Recurse | Select-String "from invoice_shared"

# Test loader
cd apps\supplier-invoice-loader
python main.py

# Check Git status
git status
git log --oneline -5
git describe --tags
```

### Deployment
```powershell
cd C:\Deployment\nex-automat

# Check verziu
git describe --tags

# Check služby
Get-Service | Where-Object {$_.DisplayName -like "*Invoice*"}

# Check API
Invoke-WebRequest -Uri "http://localhost:8000/health"

# Check logs
Get-Content apps\supplier-invoice-loader\logs\app.log -Tail 50
```

---

## ZNÁME LIMITÁCIE

### Services
- **NEXAutomat** - supplier-invoice-loader API (port 8000) ✅ POUŽÍVA SA
- **SupplierInvoiceLoader** - duplicitná služba ❌ NEPOUŽÍVA SA

### PostgreSQL Connection
- Development: localhost:5432 (optional)
- Production: localhost:5432 (enabled)

---

## DEPENDENCIES

### Core
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

## QUICK REFERENCE

### Common Tasks

**Check version:**
```powershell
git describe --tags
```

**Update nex-shared:**
```powershell
cd packages\nex-shared
pip install -e .
```

**Restart service:**
```powershell
Restart-Service NEXAutomat
```

**Test health:**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/health"
```

---

## VERSION HISTORY SUMMARY

| Version | Date | Status | Key Changes |
|---------|------|--------|-------------|
| v2.3 | 2025-12-08 | ✅ Deployed | Migration to nex-shared |
| v2.2 | 2025-12-06 | ❌ Failed | BaseGrid pattern, cleanup |
| v2.0.0 | 2025-11-12 | ✅ Deployed | Initial release |

---

**Init Prompt Created:** 2025-12-08  
**Status:** Ready for work on v2.3  
**Next:** Monitor production, plan future features