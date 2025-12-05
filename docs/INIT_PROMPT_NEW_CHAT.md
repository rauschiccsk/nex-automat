# Init Prompt - NEX Automat v2.1 Grid Settings Fix

**Project:** NEX Automat v2.0 - Supplier Invoice Processing  
**Customer:** Mágerstav s.r.o.  
**Current Version:** v2.1 (Production)  
**Status:** ⚠️ Window Settings OK, Grid Settings BROKEN  
**Last Session:** Window & Grid Settings Implementation (2025-12-05)  
**This Session:** Fix Grid Settings in invoice_list_widget.py

---

## Quick Context

**NEX Automat v2.1** má implementované window settings (funguje ✅) a čiastočne implementované grid settings (nefunguje ❌).

### Čo funguje ✅
- Window settings - ukladanie pozície a veľkosti okna
- Klávesové skratky (ENTER, ESC)
- Quick search s zeleným headerom
- Základná funkcionalita aplikácie

### Čo nefunguje ❌
- Grid settings - aplikácia spadne pri štarte
- Chyba: `AttributeError: 'InvoiceListWidget' object has no attribute '_on_selection_changed'`

---

## Aktuálny problém

### Chybová správa
```
AttributeError: 'InvoiceListWidget' object has no attribute '_on_selection_changed'
File "invoice_list_widget.py", line 196, in _setup_ui
    selection_model.currentRowChanged.connect(self._on_selection_changed)
```

### Príčina
Súbor `invoice_list_widget.py` bol v predchádzajúcej session rozbittý postupnými opravami (35 skriptov). Pri pridávaní grid settings metód sa stratili pôvodné metódy:
- `_on_selection_changed()` - chýba
- `_on_double_clicked()` - chýba  
- Pravdepodobne aj ďalšie

### Riešenie
1. **Git restore** `invoice_list_widget.py` na fungujúcu verziu (pred grid settings)
2. **Jeden komplexný script** ktorý pridá grid settings správne
3. **Testovať** po každej zmene

---

## Implementované v predchádzajúcej session

### 1. Window Settings (✅ FUNKČNÉ)

**Databáza:** `C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db`

**Súbory:**
- `src/utils/constants.py` - APP_PREFIX, WINDOW_MAIN, GRID_INVOICE_LIST, atď.
- `src/utils/window_settings.py` - load/save window settings
- `src/ui/main_window.py` - integrované window settings

**Funkcie:**
- Ukladanie/načítavanie pozície okna (x, y)
- Ukladanie/načítavanie veľkosti okna (width, height)
- Per-user (Windows username)
- ESC klávesa pre zatvorenie

### 2. Grid Settings (⚠️ IMPLEMENTOVANÉ, ALE ROZBITÉ)

**Databáza:** `C:\NEX\YEARACT\SYSTEM\SQLITE\grid_settings.db` (prázdna)

**Súbory vytvorené:**
- `src/utils/grid_settings.py` - load/save grid settings (264 riadkov)

**Súbory upravené (ROZBITÉ):**
- `src/ui/widgets/invoice_list_widget.py` - pridané metódy, ale chýbajú pôvodné
- `src/ui/widgets/quick_search.py` - pridané get/set_active_column() ✅

**Metódy ktoré MALI BYŤ pridané:**
```python
def _load_grid_settings(self):
    """Načíta a aplikuje uložené nastavenia gridu."""
    # Načíta column_settings a grid_settings z databázy
    # Aplikuje width, visual_index, visible, active_column

def _save_grid_settings(self):
    """Uloží aktuálne nastavenia gridu."""
    # Zozbiera šírky, poradie, viditeľnosť stĺpcov
    # Uloží do databázy

def _on_column_resized(self, logical_index, old_size, new_size):
    """Handler pre zmenu šírky stĺpca."""
    self._save_grid_settings()

def _on_column_moved(self, logical_index, old_visual_index, new_visual_index):
    """Handler pre presunutie stĺpca."""
    self._save_grid_settings()
```

**Signály ktoré MALI BYŤ pripojené v _setup_ui:**
```python
header.sectionResized.connect(self._on_column_resized)
header.sectionMoved.connect(self._on_column_moved)
```

---

## Postup pre túto session

### Krok 1: Diagnostika
```powershell
# Zisti aktuálny stav súboru
git status src/ui/widgets/invoice_list_widget.py

# Zobraz rozdiely oproti commit
git diff src/ui/widgets/invoice_list_widget.py
```

### Krok 2: Restore na funkčnú verziu
```powershell
# Obnov súbor pred grid settings
git restore src/ui/widgets/invoice_list_widget.py

# Alebo z konkrétneho commitu
git checkout <commit_hash> -- src/ui/widgets/invoice_list_widget.py
```

### Krok 3: Verifikácia
```powershell
# Spusti aplikáciu - mala by fungovať BEZ grid settings
python main.py
```

### Krok 4: Integrácia grid settings - SPRÁVNE

**Vytvor JEDEN komplexný script ktorý:**

1. Pridá importy na začiatok súboru:
```python
from utils.constants import WINDOW_MAIN, GRID_INVOICE_LIST
from utils.grid_settings import (
    load_column_settings, save_column_settings,
    load_grid_settings, save_grid_settings
)
```

2. Pridá volanie `self._load_grid_settings()` do `__init__` (za `self._setup_ui()`)

3. Pridá pripojenie signálov v `_setup_ui()` (za `header.resizeSection...`):
```python
# Connect header signals for grid settings
header.sectionResized.connect(self._on_column_resized)
header.sectionMoved.connect(self._on_column_moved)
```

4. Pridá všetky 4 metódy NA KONIEC triedy `InvoiceListWidget`:
   - `_load_grid_settings()`
   - `_save_grid_settings()`
   - `_on_column_resized()`
   - `_on_column_moved()`

**KRITICKÉ:** Nesmie sa stratiť žiadna existujúca metóda!

### Krok 5: Testovanie
```powershell
# Test 1: Aplikácia sa spustí
python main.py

# Test 2: Zmena šírky stĺpca
# - Potiahnuť okraj hlavičky
# - Zatvoriť aplikáciu
# - Skontrolovať databázu

# Test 3: Opätovné spustenie
# - Šírka by mala zostať
```

---

## File Locations

### Development (ICC Server)
```
C:\Development\nex-automat\
├── apps\
│   └── supplier-invoice-editor\
│       ├── src\
│       │   ├── utils\
│       │   │   ├── constants.py          [OK ✅]
│       │   │   ├── window_settings.py    [OK ✅]
│       │   │   ├── grid_settings.py      [OK ✅]
│       │   │   └── __init__.py           [OK ✅]
│       │   └── ui\
│       │       ├── main_window.py        [OK ✅]
│       │       └── widgets\
│       │           ├── invoice_list_widget.py  [BROKEN ❌]
│       │           └── quick_search.py         [OK ✅]
│       └── scripts\
│           ├── 01-35_*.py                [35 scripts z predch. session]
│           └── 36_restore_and_integrate_grid.py  [NOVÝ - vytvor tento!]
```

### Production (Mágerstav Server)
```
C:\Deployment\nex-automat\
└── apps\
    └── supplier-invoice-editor\
        └── [Window settings už sú deployed, fungujú ✅]
```

---

## Connection Details

### NEX Automat API
- **Public URL:** https://magerstav-invoices.icc.sk
- **Status:** Running ✅

### PostgreSQL (Mágerstav Server)
- **Host:** localhost
- **Database:** invoice_staging
- **User:** postgres
- **Password:** Nex1968

### Databázy (Development)
- `C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db` - funguje ✅
- `C:\NEX\YEARACT\SYSTEM\SQLITE\grid_settings.db` - prázdna (implementácia nedokončená)

---

## Known Issues

### 🔴 Kritické (blokujúce)
- **invoice_list_widget.py je rozbytý** - aplikácia spadne pri štarte
  - Chýbajúce metódy: `_on_selection_changed()`, `_on_double_clicked()`
  - Riešenie: Git restore + správna integrácia

### 🟡 Menšie (nefunkčné features)
- **Grid settings neukladajú** - databáza je prázdna
  - Riešenie: Po oprave invoice_list_widget.py by malo fungovať

---

## Possible Next Steps

### Option 1: Dokončiť Grid Settings (PRIORITA)
1. Git restore `invoice_list_widget.py`
2. Vytvoriť komplexný script pre integráciu
3. Otestovať funkčnosť
4. Commit funkčnej verzie

### Option 2: Grid Settings pre invoice items
- Po dokončení invoice_list gridu
- Rovnaký prístup pre items grid

### Option 3: Deployment do Production
- Ak grid settings fungujú
- Deploy do Mágerstav
- User testing

---

## Success Criteria

### Must Have (tento chat)
- [ ] `invoice_list_widget.py` funkčný - aplikácia sa spustí
- [ ] Grid settings implementované správne
- [ ] Test: Zmena šírky stĺpca → ulož → otvor → šírka zostala
- [ ] Databáza `grid_settings.db` obsahuje záznamy

### Should Have
- [ ] Test: Drag-and-drop stĺpca → poradie zostane
- [ ] Test: Zmena aktívneho stĺpca → zostane

### Nice to Have
- [ ] Dokumentácia pre grid settings
- [ ] Deployment do Production

---

## Documentation References

### Súbory z predchádzajúcej session
- **SESSION_NOTES.md** - kompletné poznámky z poslednej session
- **PROJECT_MANIFEST.json** - štruktúra projektu

### Kód referencie
- `window_settings.py` - funkčný príklad (použiť ako vzor)
- `grid_settings.py` - hotové funkcie, len integrovať

---

**Session Type:** Fix Grid Settings Integration  
**Expected Focus:** Oprava invoice_list_widget.py  
**Status:** ⚠️ **BROKEN - NEEDS IMMEDIATE FIX**  
**Priority:** 🔴 **HIGH**

---

**Last Updated:** 2025-12-05 20:10  
**Previous Session:** Window & Grid Settings Implementation  
**Version:** v2.1 (Window Settings OK, Grid Settings Broken)  
**Next Milestone:** Funkčné Grid Settings