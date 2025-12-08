# INIT PROMPT - Nový chat (supplier-invoice-loader migrácia v2.3)

## KONTEXT Z PREDCHÁDZAJÚCEHO CHATU

**Deployment v2.2 FAILED** - Rollback na v2.0.0 ✅

**Dôvod:** supplier-invoice-loader nie je kompatibilný s v2.2 (používa vymazaný `invoice-shared` package)

---

## AKTUÁLNY STAV PROJEKTU

**Projekt:** nex-automat (NEX Automat v2.0)  
**Development:** `C:\Development\nex-automat`  
**Python:** 3.13.7 (venv32)  
**Git Branch:** develop  
**Aktuálna verzia:** v2.2 (len editor), v2.0.0 (loader)

**Magerstav Deployment:**
- Lokácia: `C:\Deployment\nex-automat`
- Verzia: v2.0.0 (rollback z v2.2)
- Služba: NEXAutomat beží ✅

---

## ČO JE PROBLÉM

### supplier-invoice-loader používa invoice-shared

**invoice-shared bol vymazaný v v2.2**, ale supplier-invoice-loader stále používa:

1. **clean_string** z `invoice_shared.utils.text_utils`
2. **PostgresStagingClient** z `invoice_shared.database.postgres_staging`

**Súbory s problémom:**
```
apps/supplier-invoice-loader/main.py (2 importy)
apps/supplier-invoice-loader/tests/test_invoice_integration.py (2 importy)
```

---

## CIEĽ v2.3

**Migrovať supplier-invoice-loader z invoice-shared na nex-shared**

**Kroky:**
1. ✅ Nájsť/vytvoriť `clean_string` funkciu
2. ✅ Nájsť/presunúť `PostgresStagingClient` class
3. ✅ Update importov v loader aplikácii
4. ✅ Test lokálne
5. ✅ Git commit & tag v2.3
6. ✅ Deployment na Magerstav

---

## ČO JE HOTOVÉ (v2.2)

### BaseGrid Pattern - Production Ready
- **Vytvorené v nex-shared:**
  - `packages/nex-shared/ui/base_grid.py` - Univerzálna base trieda
  - `packages/nex-shared/utils/grid_settings.py` - Persistence do SQLite
  - `packages/nex-shared/ui/__init__.py` - Export

- **Funkcionalita:**
  - ✅ Automatická QTableView + GreenHeaderView
  - ✅ Automatická grid persistence (column widths, active column)
  - ✅ QuickSearch integration
  - ✅ Auto-load/save settings
  - ✅ Debug printy odstránené (v2.2)

### Refaktorované gridy v supplier-invoice-editor
- `invoice_list_widget.py` - používa BaseGrid ✅
- `invoice_items_grid.py` - používa BaseGrid ✅
- `quick_search.py` - signal pre active column ✅

---

## ŠTRUKTÚRA PROJEKTU

```
nex-automat/
├── apps/
│   ├── supplier-invoice-editor/    ← v2.2 ✅ FUNGUJE
│   │   └── src/
│   │       ├── ui/widgets/
│   │       │   ├── invoice_list_widget.py    (BaseGrid)
│   │       │   ├── invoice_items_grid.py     (BaseGrid)
│   │       │   └── quick_search.py
│   │       └── utils/
│   │           └── text_utils.py             (remove_diacritics, normalize_for_search)
│   │
│   └── supplier-invoice-loader/    ← v2.0.0, TREBA MIGROVAŤ
│       ├── main.py                 ← 2x invoice_shared import
│       ├── src/
│       │   └── database/
│       │       └── database.py
│       └── tests/
│           └── test_invoice_integration.py   ← 2x invoice_shared import
│
└── packages/
    ├── nex-shared/                 ← v2.2 ✅ FUNGUJE
    │   ├── ui/
    │   │   ├── base_grid.py
    │   │   ├── base_window.py
    │   │   └── __init__.py
    │   ├── utils/
    │   │   ├── grid_settings.py
    │   │   └── __init__.py
    │   └── database/               ← Sem presunúť PostgresStagingClient?
    │       └── window_settings_db.py
    │
    └── nexdata/                    ← Btrieve/NEX Genesis prístup
        └── ...
```

---

## KRITICKÉ PRAVIDLÁ

### Workflow
1. **Development → Git → Deployment**
2. **NIKDY nerobiť zmeny priamo v Deployment!**
3. Všetky zmeny cez numbered scripts

### Package štruktúra
- **nex-shared** - FLAT štruktúra (nex-shared appears ONLY ONCE in path)
- Po zmenách v nex-shared: `pip install -e .` v packages/nex-shared

### Migrácia best practices
1. Najprv nájdi originálne implementácie
2. Skopíruj/presun do vhodného package
3. Update importov
4. Test lokálne pred commitom
5. Git tag pre každú release verziu

---

## ĎALŠIE KROKY PRE NOVÝ CHAT

### 1. PRIESKUM (PRVÁ ÚLOHA)
```powershell
cd C:\Development\nex-automat

# Nájdi clean_string
Get-ChildItem -Path . -Include *.py -Recurse | Select-String "def clean_string"

# Nájdi PostgresStagingClient
Get-ChildItem -Path . -Include *.py -Recurse | Select-String "class PostgresStagingClient"

# Pozri použitie v main.py
Get-Content apps\supplier-invoice-loader\main.py | Select-String -Context 5,5 "clean_string"
Get-Content apps\supplier-invoice-loader\main.py | Select-String -Context 5,5 "PostgresStagingClient"
```

### 2. IMPLEMENTÁCIA
Na základe nájdených implementácií:
- Vytvor/presun `clean_string`
- Vytvor/presun `PostgresStagingClient`
- Update importov v loader
- Vytvor migračný script

### 3. TESTOVANIE
```powershell
# Test loader
cd apps\supplier-invoice-loader
python main.py

# API health check
Invoke-WebRequest -Uri "http://localhost:8000/health"
```

### 4. GIT & DEPLOYMENT
- Tag v2.3
- Merge do main
- Deployment na Magerstav

---

## ZNÁME LIMITÁCIE

### Magerstav Služby
- **NEXAutomat** - supplier-invoice-loader API (port 8000) ✅ POUŽÍVA SA
- **SupplierInvoiceLoader** - duplicitná služba ❌ NEPOUŽÍVA SA

### Deployment Paths
```
Development: C:\Development\nex-automat
Deployment:  C:\Deployment\nex-automat
Persistence: C:\NEX\YEARACT\SYSTEM\SQLITE\
```

---

## PERSISTENCE LOCATIONS

```
Window settings: C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db
Grid settings:   C:\NEX\YEARACT\SYSTEM\SQLITE\grid_settings.db
```

---

## DEBUG TOOLS

**Na Development:**
```powershell
# Check imports
Get-ChildItem -Path apps\supplier-invoice-loader -Include *.py -Recurse | Select-String "from invoice_shared"

# Test loader
cd apps\supplier-invoice-loader
python main.py

# Check Git status
git status
git log --oneline -5
```

**Na Deployment:**
```powershell
# Check verziu
git log --oneline -1

# Check služby
Get-Service | Where-Object {$_.DisplayName -like "*Invoice*"}

# Check API
Invoke-WebRequest -Uri "http://localhost:8000/health"
```

---

## MOŽNÉ UMIESTNENIA FUNKCIÍ

### clean_string
**Možnosť 1:** `packages/nex-shared/utils/text_utils.py`  
**Možnosť 2:** `apps/supplier-invoice-loader/src/utils/text_utils.py`

### PostgresStagingClient
**Možnosť 1:** `packages/nex-shared/database/postgres_staging.py`  
**Možnosť 2:** `apps/supplier-invoice-loader/src/database/postgres_staging.py`

**Odporúčanie:** Ak sa používa len v loader → nechať v loader/src  
Ak sa bude používať aj v editor → presunúť do nex-shared

---

**Init Prompt Created:** 2025-12-08  
**Status:** Pripravený na migráciu v2.3  
**Ready for:** Prieskum implementácií a migrácia supplier-invoice-loader