# Session Notes - 2025-12-05: Active Column Persistence & Window Position Fix

## Zhrnutie session

Session riešila dva problémy v NEX Automat v2.1 - Supplier Invoice Editor:
1. **Active Column Persistence** - Grid settings nezapamätali aktívny stĺpec pre quick search
2. **Window Position Validation** - Okno sa mohlo posunúť mimo obrazovky

## Nový Workflow: Local File Scripts ⭐ PERMANENT

**Od tejto session používame HYBRIDNÝ prístup pre prácu so súbormi:**

### Ako to funguje

1. **Session start:** Priložený manifest (prehľad projektu)
2. **Active work:** Local scripts (real-time prístup k súborom)
3. **Session end:** Git commit + push (verziovanie)

### Utility Scripts

#### Script 1: `read_project_file.py` - Jeden súbor
```powershell
python scripts\read_project_file.py apps/supplier-invoice-editor/src/ui/main_window.py
```
**Output:** Kompletný obsah súboru s metadátami  
**Copy-paste** output do chatu → Claude má súbor

#### Script 2: `read_module_files.py` - Viacero súborov
```powershell
# Celý modul
python scripts\read_module_files.py --module apps/supplier-invoice-editor/src/ui/widgets

# Konkrétne súbory
python scripts\read_module_files.py file1.py file2.py file3.py

# Pattern
python scripts\read_module_files.py --pattern "*/utils/*.py"
```
**Output:** Všetky súbory naraz  
**Copy-paste** output do chatu → Claude má všetky súbory

### Pravidlá Workflow

| Potrebujem... | Použijem... |
|---------------|-------------|
| Prehľad projektu | Priložený manifest |
| 1 súbor | `read_project_file.py` |
| Celý modul/package | `read_module_files.py --module` |
| 2-5 konkrétnych súborov | `read_module_files.py file1 file2 ...` |
| Súbory podľa pattern | `read_module_files.py --pattern` |

### Výhody

✅ **Rýchle** - žiadne web requests  
✅ **Real-time** - vidím uncommitted changes  
✅ **Spoľahlivé** - žiadne GitHub problémy  
✅ **Jednoduché** - len copy-paste  
✅ **Efektívne** - viacero súborov naraz

### Nevýhody

❌ Funguje len na dev PC (nie cross-machine)  
❌ Žiadna history (musí commit pre audit)

### Kedy ešte používať GitHub?

- Session review (porovnanie zmien medzi sessionami)
- Audit trail (kto/čo/kedy zmenil)
- Backup (záloha projektu)
- Cross-machine (práca z iného PC)

---

## Hlavné problémy a riešenia

### Problém 1: Manifest System - Branch Mismatch

**Symptóm:**
- Claude nemohol načítať súbory z GitHub pomocou manifestu
- Dostal 404 error na všetky URL

**Root Cause:**
- Manifest mal hardcoded `/main/` branch v GitHub raw URL
- Projekt používa `/develop/` branch pre aktívny vývoj
- Claude nedokázal načítať súbory lebo URL boli nesprávne

**Riešenie:**
1. Upravený `scripts/generate_projects_access.py`
   - Pridané konfiguračné konštanty:
     ```python
     GITHUB_REPO = "rauschiccsk/nex-automat"
     GITHUB_BRANCH = "develop"  # Changed from "main"
     ```
   - Všetky GitHub raw URL teraz používajú `GITHUB_BRANCH` variable
2. Vygenerovaný nový manifest pre všetky aplikácie
3. Overené načítanie súborov z develop branch

**Status:** ✅ VYRIEŠENÉ - Manifest system funguje s develop branch

---

### Problém 2: Active Column Persistence Nefungovala

**Symptóm:**
- Grid settings ukladali šírky stĺpcov správne
- Ale aktívny stĺpec pre quick search sa nezapamätal
- Po reštarte aplikácie vždy default stĺpec (0)

**Root Cause:**
Nesprávny názov atribútu v `invoice_list_widget.py`:
- Controller vytvorený ako: `self.search_controller` (riadok 196)
- Ale používaný ako: `self.quick_search` (riadky 295, 317)
- Metódy `get_active_column()` a `set_active_column()` volané na neexistujúcom atribúte

**Riešenie:**
Script `01_fix_active_column_persistence.py`:
```python
# Fix 1: Načítanie (riadok ~295)
- if hasattr(self, 'quick_search') and self.quick_search:
-     self.quick_search.set_active_column(active_col)
+ if hasattr(self, 'search_controller') and self.search_controller:
+     self.search_controller.set_active_column(active_col)

# Fix 2: Ukladanie (riadok ~317)
- if hasattr(self, 'quick_search') and self.quick_search:
-     active_column = self.quick_search.get_active_column()
+ if hasattr(self, 'search_controller') and self.search_controller:
+     active_column = self.search_controller.get_active_column()
```

**Súbory upravené:**
- `apps/supplier-invoice-editor/src/ui/widgets/invoice_list_widget.py`

**Status:** ✅ OPRAVENÉ (čaká na testing)

---

### Problém 3: Window Position Mimo Obrazovky

**Symptóm:**
- Po spustení aplikácie bolo okno posunuté tak že hlavička bola mimo obrazovky
- Používateľ nemohol okno posunúť späť

**Root Cause:**
- `window_settings.py` nemal validáciu pozície okna
- Databáza obsahovala nevalidný záznam: `x=-1827, y=74`
- `load_window_settings()` vrátil túto pozíciu bez kontroly

**Riešenie - Časť 1: Pridanie validácie**

Script `02_fix_window_position_validation.py`:
- Pridaná validácia do `load_window_settings()`:
  ```python
  MIN_X = -50   # Povoliť čiastočne mimo (multi-monitor)
  MIN_Y = 0     # Hlavička musí byť viditeľná
  MIN_WIDTH = 400
  MIN_HEIGHT = 300
  MAX_WIDTH = 3840   # 4K
  MAX_HEIGHT = 2160
  ```
- Ak pozícia nevalidná → vráti `None` → použije sa default

**Riešenie - Časť 2: Vyčistenie nevalidných záznamov**

Script `04_clean_invalid_window_positions.py`:
- Kontroluje všetky záznamy v databáze
- Identifikuje nevalidné pozície
- Vymaže ich z databázy
- Umožní uloženie novej validnej pozície

**Súbory upravené:**
- `apps/supplier-invoice-editor/src/utils/window_settings.py`

**Status:** ✅ OPRAVENÉ (čaká na vyčistenie databázy)

---

## Vytvorené scripty

### File Access Scripts (NEW - Permanent Workflow Change)

#### Script: `read_project_file.py`
**Location:** `scripts/read_project_file.py`  
**Purpose:** Načíta jeden súbor z projektu  
**Usage:**
```powershell
python scripts\read_project_file.py apps/supplier-invoice-editor/src/ui/main_window.py
```
**Status:** ✅ Vytvorený, funkčný

#### Script: `read_module_files.py`
**Location:** `scripts/read_module_files.py`  
**Purpose:** Načíta viacero súborov naraz (modul, pattern, list)  
**Usage:**
```powershell
# Celý modul
python scripts\read_module_files.py --module apps/supplier-invoice-editor/src/ui/widgets

# Konkrétne súbory
python scripts\read_module_files.py file1.py file2.py

# Pattern
python scripts\read_module_files.py --pattern "*/utils/*.py"
```
**Status:** ✅ Vytvorený, funkčný

---

### Bug Fix Scripts

### Script 01: Fix Active Column Persistence
**Location:** `scripts/01_fix_active_column_persistence.py`  
**Purpose:** Opraví odkazy na search_controller v invoice_list_widget.py  
**Status:** ✅ Spustený, úspešne aplikovaný

### Script 02: Fix Window Position Validation  
**Location:** `scripts/02_fix_window_position_validation.py`  
**Purpose:** Pridá validáciu pozície okna do window_settings.py  
**Status:** ✅ Spustený, úspešne aplikovaný

### Script 03: Check Window Settings DB
**Location:** `scripts/03_check_window_settings_db.py`  
**Purpose:** Diagnostický nástroj - zobrazí obsah window_settings databázy  
**Status:** ✅ Vytvorený, funguje

### Script 04: Clean Invalid Window Positions
**Location:** `scripts/04_clean_invalid_window_positions.py`  
**Purpose:** Vymaže nevalidné záznamy z window_settings databázy  
**Status:** ✅ Vytvorený (čaká na spustenie)

---

## Aktuálny stav databáz

### Window Settings Database
**Location:** `C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db`

**Aktuálny obsah:**
```
ID: 34
User: Server
Window: sie_main_window
Position: x=-1827, y=74  ❌ NEVALIDNÉ
Size: 1216 x 449
```

**Akcia potrebná:** Spustiť script 04 na vyčistenie

### Grid Settings Database
**Location:** `C:\NEX\YEARACT\SYSTEM\SQLITE\grid_settings.db`

**Status:** Funkčné, ukladá:
- Šírky stĺpcov ✅
- Poradie stĺpcov ✅
- Viditeľnosť stĺpcov ✅
- Aktívny stĺpec ✅ (po oprave)

---

## Testing Checklist

### ✅ Test 1: Manifest System
- [x] Vygenerovaný nový manifest s develop branch
- [x] Načítané súbory z GitHub develop branch
- [x] `quick_search.py` načítaný úspešne
- [x] `invoice_list_widget.py` načítaný úspešne

### ⏳ Test 2: Active Column Persistence
- [x] Fix aplikovaný
- [ ] Aplikácia spustená
- [ ] Aktívny stĺpec zmenený (← → šípky)
- [ ] Zelený header sa posunul
- [ ] Aplikácia zatvorená (ESC)
- [ ] Aplikácia znovu spustená
- [ ] Aktívny stĺpec zostal rovnaký

### ⏳ Test 3: Window Position
- [x] Validácia pridaná
- [x] Nevalidný záznam identifikovaný
- [ ] Databáza vyčistená (script 04)
- [ ] Aplikácia spustená - default pozícia
- [ ] Okno presunuté a zmenená veľkosť
- [ ] Aplikácia zatvorená (ESC)
- [ ] Aplikácia znovu spustená
- [ ] Pozícia a veľkosť zapamätané

---

## Ďalšie kroky (Priority pre ďalší chat)

### Priorita 1: Dokončiť Testing ⚠️ URGENT
1. Spustiť `python scripts\04_clean_invalid_window_positions.py`
2. Otestovať active column persistence
3. Otestovať window position persistence
4. Overiť že oba systémy fungujú správne

### Priorita 2: Git Commit
Po úspešnom testingu:
```
Súbory na commit:
- scripts/generate_projects_access.py (upravený)
- scripts/01_fix_active_column_persistence.py (nový)
- scripts/02_fix_window_position_validation.py (nový)
- scripts/03_check_window_settings_db.py (nový)
- scripts/04_clean_invalid_window_positions.py (nový)
- apps/supplier-invoice-editor/src/ui/widgets/invoice_list_widget.py (upravený)
- apps/supplier-invoice-editor/src/utils/window_settings.py (upravený)
- docs/apps/supplier-invoice-editor.json (nový manifest)
```

### Priorita 3: Deployment do Production
Po úspešnom testingu v Development:
1. Git commit a push
2. Pull v Production (Mágerstav server)
3. Production testing
4. User acceptance

### Priorita 4: Rozšírenia (Nice to Have)
- Column visibility UI (right-click context menu)
- Reset settings button
- Export/import settings
- Global vs per-user settings toggle

---

## Lessons Learned

### Čo fungovalo dobre ✅
1. **Systematická diagnostika** - krok po kroku identifikácia problémov
2. **Manifest system** - po oprave veľmi efektívne načítanie súborov
3. **Utility scripty** - Script 03 (check DB) bol kľúčový pre diagnostiku
4. **Validácia pozície** - predíde budúcim problémom s oknom mimo obrazovky

### Čo nefungovalo ❌
1. **Branch assumption** - Manifest mal hardcoded "main" namiesto parametrizovaného branch
2. **Chýbajúca validácia** - Window settings nemali od začiatku validáciu hraníc
3. **Naming inconsistency** - `search_controller` vs `quick_search` spôsobilo bug

### Odporúčania pre budúcnosť 💡
1. **Manifest generator** - Pridať branch ako parameter alebo auto-detect
2. **Validácia vždy** - Každé načítanie z DB by malo mať validáciu hraníc
3. **Testing pred commitom** - Necommitovať zmeny bez testovania funkcionality
4. **Naming conventions** - Konzistentné názvy atribútov cez celý projekt

---

## Štatistiky

- **Celkový čas:** ~2 hodiny
- **Vytvorené scripty:** 4
- **Upravené súbory:** 3
- **Vyriešené problémy:** 3
- **Token usage:** ~103K / 190K (54%)

---

## Technical Notes

### Window Settings - Súbory a cesty
```
Database: C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db
Module:   apps/supplier-invoice-editor/src/utils/window_settings.py
Usage:    apps/supplier-invoice-editor/src/ui/main_window.py
```

### Grid Settings - Súbory a cesty
```
Database: C:\NEX\YEARACT\SYSTEM\SQLITE\grid_settings.db
Module:   apps/supplier-invoice-editor/src/utils/grid_settings.py
Usage:    apps/supplier-invoice-editor/src/ui/widgets/invoice_list_widget.py
```

### Quick Search - Komponenty
```
Controller: ui/widgets/quick_search.py (QuickSearchController)
Methods:    get_active_column(), set_active_column()
Database:   Ukladá sa cez grid_settings.py
```

---

## Connection Details

### Development Server (ICC Komárno)
- **Location:** C:\Development\nex-automat
- **Python:** C:\Development\nex-automat\venv32\Scripts\python.exe
- **Database:** C:\NEX\YEARACT\SYSTEM\SQLITE\
- **Status:** ✅ Opravy aplikované, čaká na testing

### Production Server (Mágerstav)
- **Location:** C:\Deployment\nex-automat
- **Database:** C:\NEX\YEARACT\SYSTEM\SQLITE\
- **Status:** ⏸️ Čaká na deployment

### GitHub Repository
- **Repo:** rauschiccsk/nex-automat
- **Branch:** develop (aktívny vývoj)
- **Branch:** main (stable releases)
- **Visibility:** Public

---

**Session Type:** Bug Fixes & System Maintenance  
**Version:** v2.1 (Grid Settings era)  
**Next Session:** Testing & Deployment  
**Status:** ⚠️ **NEEDS TESTING**

**Critical Path:**
1. Vyčistiť databázu (script 04) ← **NEXT ACTION**
2. Otestovať oba systémy
3. Git commit
4. Production deployment