# Init Prompt - NEX Automat v2.1 Testing & Cleanup

**Project:** NEX Automat v2.0 - Supplier Invoice Editor  
**Customer:** Mágerstav s.r.o.  
**Current Version:** v2.1 (Grid Settings + Fixes)  
**Status:** ⚠️ **NEEDS TESTING & CLEANUP**  
**Last Session:** Active Column & Window Position Fixes (2025-12-05)  
**This Session:** Testing, Database Cleanup, Git Commit

---

## CRITICAL - Must Do First! ⚠️

**Before ANY other work, execute cleanup script:**

```powershell
cd C:\Development\nex-automat
python scripts\04_clean_invalid_window_positions.py
```

**Why:** Window settings database contains invalid position (x=-1827) that prevents proper window positioning.

---

## Quick Context

**V minulej session boli OPRAVENÉ 3 problémy:**

### 1. ✅ Manifest System Fixed
- **Problém:** Claude nemohol načítať súbory (404 error)
- **Príčina:** Manifest mal `/main/` branch, projekt používa `/develop/`
- **Riešenie:** Upravený `scripts/generate_projects_access.py` s parametrom branch
- **Status:** VYRIEŠENÉ, manifest funguje

### 2. ✅ Active Column Persistence Fixed  
- **Problém:** Aktívny stĺpec sa nezapamätal po reštarte
- **Príčina:** Nesprávny názov atribútu (`quick_search` vs `search_controller`)
- **Riešenie:** Script `01_fix_active_column_persistence.py` opravil 2 miesta
- **Status:** OPRAVENÉ, čaká na testing

### 3. ✅ Window Position Validation Added
- **Problém:** Okno sa mohlo posunúť mimo obrazovky
- **Príčina:** Chýbala validácia pozície v `window_settings.py`
- **Riešenie:** Script `02_fix_window_position_validation.py` pridal validáciu
- **Status:** OPRAVENÉ, ale databáza obsahuje nevalidný záznam

---

## Current Status

### Development (ICC Server)
**Location:** `C:\Development\nex-automat\apps\supplier-invoice-editor`

**Opravy aplikované:** ✅ ÁNO
- `invoice_list_widget.py` - active column fix
- `window_settings.py` - validation added
- `generate_projects_access.py` - branch parameter

**Testing:** ❌ NIE (čaká na cleanup)

**Database problém:**
```
C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db
└─ Záznam ID 34: x=-1827 (NEVALIDNÉ)
```

### Production (Mágerstav Server)
**Location:** `C:\Deployment\nex-automat\apps\supplier-invoice-editor`

**Status:** ⏸️ Čaká na development testing a Git commit

---

## Priority Tasks - In Order!

### 🔴 PRIORITY 1: Database Cleanup (BLOCKING)

**Pred AKÝMKOĽVEK testovaním:**

```powershell
cd C:\Development\nex-automat
python scripts\04_clean_invalid_window_positions.py
```

**Script vymaže:**
- Nevalidný záznam s x=-1827
- Umožní uložiť novú validnú pozíciu

**Očakávaný output:**
```
✅ Vymazaných 1 záznamov
✅ Zostalo 0
```

---

### 🟡 PRIORITY 2: Testing (After Cleanup)

#### Test A: Window Position Persistence

1. **Spusti aplikáciu:**
   ```powershell
   cd C:\Development\nex-automat\apps\supplier-invoice-editor
   C:\Development\nex-automat\venv32\Scripts\python.exe main.py
   ```

2. **Test scenario:**
   - Presuň okno na inú pozíciu
   - Zmeň veľkosť okna
   - Zatvor aplikáciu (ESC)
   - Znovu spusti aplikáciu
   - **Overiť:** Pozícia a veľkosť zostali? ✅/❌

3. **Diagnostika (ak nefunguje):**
   ```powershell
   python scripts\03_check_window_settings_db.py
   ```

#### Test B: Active Column Persistence

1. **V aplikácii:**
   - Použite šípky ← → na zmenu aktívneho stĺpca
   - Skontrolujte že sa zmení zelený header
   - Zatvorte aplikáciu (ESC)
   - Znovu spustite aplikáciu
   - **Overiť:** Aktívny stĺpec zostal rovnaký? ✅/❌

2. **Diagnostika (ak nefunguje):**
   ```powershell
   # Pozri logs v konzole - hľadaj "Loaded active column" a "Saving active column"
   ```

#### Test C: Grid Settings (Regression Test)

1. **Overenie že stále funguje:**
   - Zmeň šírku stĺpcov v invoice list
   - Zatvor a znovu otvor aplikáciu
   - **Overiť:** Šírky stĺpcov zostali? ✅/❌

---

### 🟢 PRIORITY 3: Git Commit (After Successful Testing)

**Súbory na commit:**

```
Modified:
  scripts/generate_projects_access.py
  apps/supplier-invoice-editor/src/ui/widgets/invoice_list_widget.py
  apps/supplier-invoice-editor/src/utils/window_settings.py

New:
  scripts/01_fix_active_column_persistence.py
  scripts/02_fix_window_position_validation.py
  scripts/03_check_window_settings_db.py
  scripts/04_clean_invalid_window_positions.py
  docs/apps/supplier-invoice-editor.json (updated manifest)
```

**Commit message je v artifacts nižšie.**

---

### 🔵 PRIORITY 4: Production Deployment (After Git Push)

**Na Mágerstav serveri:**

```powershell
cd C:\Deployment\nex-automat
git pull origin develop

# Vyčistiť production database
python scripts\04_clean_invalid_window_positions.py

# Testovať
cd apps\supplier-invoice-editor
python main.py
```

---

## Available Utility Scripts

### Script 03: Database Inspector
```powershell
python scripts\03_check_window_settings_db.py
```
**Purpose:** Zobrazí obsah window_settings databázy  
**Use when:** Debugging ukladania/načítania okna

### Script 04: Database Cleaner
```powershell
python scripts\04_clean_invalid_window_positions.py
```
**Purpose:** Vymaže nevalidné pozície okien  
**Use when:** Okno mimo obrazovky alebo iné problémy s pozíciou

---

## File Structure

```
C:\Development\nex-automat\
├── scripts\
│   ├── generate_projects_access.py      [MODIFIED - develop branch]
│   ├── 01_fix_active_column_persistence.py      [NEW]
│   ├── 02_fix_window_position_validation.py     [NEW]
│   ├── 03_check_window_settings_db.py           [NEW]
│   └── 04_clean_invalid_window_positions.py     [NEW]
│
├── apps\supplier-invoice-editor\
│   ├── src\
│   │   ├── ui\
│   │   │   ├── main_window.py                   [OK]
│   │   │   └── widgets\
│   │   │       ├── invoice_list_widget.py       [MODIFIED]
│   │   │       ├── invoice_items_grid.py        [OK]
│   │   │       └── quick_search.py              [OK]
│   │   └── utils\
│   │       ├── window_settings.py               [MODIFIED]
│   │       ├── grid_settings.py                 [OK]
│   │       └── constants.py                     [OK]
│   └── main.py                                  [OK]
│
└── docs\
    └── apps\
        └── supplier-invoice-editor.json         [UPDATED]
```

---

## Connection Details

### Development Server (ICC)
- **Path:** C:\Development\nex-automat
- **Python:** C:\Development\nex-automat\venv32\Scripts\python.exe
- **Database:** C:\NEX\YEARACT\SYSTEM\SQLITE\
- **Git Branch:** develop

### Production Server (Mágerstav)
- **Path:** C:\Deployment\nex-automat
- **Database:** C:\NEX\YEARACT\SYSTEM\SQLITE\
- **Service:** NEXAutomat (pre supplier-invoice-loader)

### PostgreSQL Database (Mágerstav)
- **Host:** localhost
- **Database:** invoice_staging
- **User:** postgres
- **Password:** Nex1968

### GitHub Repository
- **URL:** https://github.com/rauschiccsk/nex-automat
- **Active Branch:** develop
- **Stable Branch:** main

---

## Known Issues & Limitations

### Issue 1: Multi-Monitor Edge Case
- **Problém:** Validácia MIN_X = -50 môže byť nedostatočná pre wide multi-monitor setup
- **Workaround:** Ak okno zmizne, vymazať databázu
- **Future Fix:** Detekcia dostupných monitorov a dynamická validácia

### Issue 2: Aktívny stĺpec pri prázdnej tabuľke
- **Problém:** Ak tabuľka nemá dáta, aktívny stĺpec sa nemusí zobraziť správne
- **Impact:** Low - v produkcii vždy sú dáta
- **Future Fix:** Pridať check pre prázdnu tabuľku

---

## Testing Checklist

### ✅ Completed (Previous Session)
- [x] Manifest system fixed
- [x] Active column fix applied
- [x] Window validation added
- [x] Database inspector created
- [x] Database cleaner created

### ⏳ TODO (This Session)
- [ ] Run database cleanup script
- [ ] Test window position persistence
- [ ] Test active column persistence
- [ ] Test grid settings (regression)
- [ ] Git commit
- [ ] Git push
- [ ] Production deployment
- [ ] Production testing

---

## Troubleshooting Guide

### Problém: Okno mimo obrazovky
**Riešenie:**
```powershell
del "C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db"
```

### Problém: Aktívny stĺpec sa nezapamätá
**Diagnostika:**
1. Pozri console output - hľadaj "Loaded active column" a "Saving active column"
2. Over databázu: `python scripts\03_check_window_settings_db.py`
3. Over že `search_controller` existuje v `invoice_list_widget.py`

### Problém: Šírky stĺpcov sa nezapamätajú
**Diagnostika:**
1. Over že existuje: `C:\NEX\YEARACT\SYSTEM\SQLITE\grid_settings.db`
2. Over že column_settings tabuľka má záznamy
3. Skontroluj logy v konzole

### Problém: Manifest nemôže načítať súbory
**Riešenie:**
1. Over že repository je PUBLIC na GitHub
2. Over že branch existuje: `git branch -r`
3. Vygeneruj nový manifest: `python scripts\generate_projects_access.py`

---

## Next Features (Backlog)

**Po úspešnom deploymente v2.1:**

1. **Column Visibility UI**
   - Right-click context menu na header
   - Show/Hide checkboxes
   - Save to grid_settings

2. **Reset Settings Button**
   - Toolbar button "Reset nastavenia"
   - Vymaže databázy
   - Reštartuje aplikáciu

3. **Settings Export/Import**
   - Export nastavení do JSON
   - Import z JSON
   - Zdieľanie medzi používateľmi

4. **Global Settings Option**
   - Toggle: Per-user / Global (všetci používatelia)
   - Admin može nastaviť default pre všetkých

---

## Important Notes

### Window Settings Validácia
```python
MIN_X = -50    # Povoliť čiastočne mimo (multi-monitor)
MIN_Y = 0      # Hlavička MUSÍ byť viditeľná
MIN_WIDTH = 400
MIN_HEIGHT = 300
MAX_WIDTH = 3840   # 4K
MAX_HEIGHT = 2160
```

### Grid Settings - Two Databases
1. **window_settings.db** - pozície okien
2. **grid_settings.db** - grid nastavenia (šírky, poradie, viditeľnosť, aktívny stĺpec)

### Quick Search - Arrow Keys
- **← →** Change active column
- **↑ ↓** Move selection + clear search
- **ESC** Close application

---

**Session Type:** Testing, Cleanup & Deployment  
**Critical Path:** Cleanup → Test → Commit → Deploy  
**Status:** ⚠️ **BLOCKED ON DATABASE CLEANUP**  
**Next Action:** 🔴 **RUN SCRIPT 04 FIRST!**

---

**Last Updated:** 2025-12-05 22:30  
**Previous Session:** Active Column & Window Position Fixes  
**Version:** v2.1.1 (with fixes)  
**Target:** Production Deployment