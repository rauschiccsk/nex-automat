# Session Notes - 2025-12-05: Window & Grid Settings Implementation

## Zhrnutie session

Implementovali sme komplexnú funkcionalitu pre ukladanie užívateľských nastavení okien a gridov pomocou SQLite databáz.

## Čo bolo implementované

### 1. Window Settings (✅ FUNKČNÉ)

**Databáza:** `C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db`

**Vytvorené súbory:**
- `src/utils/constants.py` (21 riadkov) - konštanty pre window/grid ID
- `src/utils/window_settings.py` (155 riadkov) - SQLite logika
- Upravené: `src/utils/__init__.py`, `src/ui/main_window.py`

**Funkcie:**
- ✅ Automatické ukladanie pozície okna (x, y)
- ✅ Automatické ukladanie veľkosti okna (width, height)
- ✅ Per-user settings (Windows username)
- ✅ Načítanie pri štarte, uloženie pri zatvorení

**Tabuľka: `window_settings`**
```sql
CREATE TABLE window_settings (
    id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL,
    window_name TEXT NOT NULL,  -- "sie_main_window"
    x, y, width, height INTEGER,
    updated_at TIMESTAMP,
    UNIQUE(user_id, window_name)
);
```

### 2. Klávesové skratky (✅ FUNKČNÉ)

**Pridané:**
- ✅ **ENTER** v zozname faktúr → otvorí detail faktúry
- ✅ **ESC** v hlavnom okne → zatvorí aplikáciu (s uložením pozície)

**Upravené súbory:**
- `src/ui/widgets/invoice_list_widget.py` - ENTER handler
- `src/ui/main_window.py` - ESC handler

### 3. Grid Settings (⚠️ IMPLEMENTOVANÉ, ALE NEFUNKČNÉ)

**Databáza:** `C:\NEX\YEARACT\SYSTEM\SQLITE\grid_settings.db`

**Vytvorené súbory:**
- `src/utils/grid_settings.py` (264 riadkov) - SQLite logika pre gridy

**Upravené súbory:**
- `src/ui/widgets/invoice_list_widget.py` - pridané metódy pre grid settings
- `src/ui/widgets/quick_search.py` - pridané get/set_active_column()

**Tabuľky:**
```sql
-- Nastavenia stĺpcov
CREATE TABLE grid_column_settings (
    id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL,
    window_name TEXT NOT NULL,  -- "sie_main_window"
    grid_name TEXT NOT NULL,     -- "invoice_list"
    column_name TEXT NOT NULL,   -- "invoice_number"
    width INTEGER,
    visual_index INTEGER,        -- poradie po drag-and-drop
    visible BOOLEAN DEFAULT 1,
    updated_at TIMESTAMP,
    UNIQUE(user_id, window_name, grid_name, column_name)
);

-- Grid-level nastavenia
CREATE TABLE grid_settings (
    id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL,
    window_name TEXT NOT NULL,
    grid_name TEXT NOT NULL,
    active_column_index INTEGER,  -- aktívny stĺpec pre quick search
    updated_at TIMESTAMP,
    UNIQUE(user_id, window_name, grid_name)
);
```

**Plánované funkcie:**
- Ukladanie šírky stĺpcov
- Ukladanie poradia stĺpcov (drag-and-drop)
- Skrývanie/zobrazovanie stĺpcov
- Ukladanie aktívneho stĺpca (zelený header)

## Vytvorené skripty (35 total)

### Window Settings (Scripts 01-15)
- `01_create_constants.py` - vytvorenie constants.py
- `02_create_window_settings.py` - vytvorenie window_settings.py
- `03_update_utils_init.py` - aktualizácia utils/__init__.py
- `04-12` - integrácia do main_window.py (s opravami)
- `13-15` - pridanie ENTER a ESC klávesových skratiek

### Grid Settings (Scripts 16-35)
- `16_update_constants_grids.py` - pridanie grid konštánt
- `17_create_grid_settings.py` - vytvorenie grid_settings.py
- `18_update_utils_init_grids.py` - aktualizácia utils/__init__.py
- `19-35` - integrácia do invoice_list_widget.py (viacero pokusov)

## Aktuálny stav

### ✅ Funguje
- Window settings - pozícia a veľkosť okna sa ukladá/načítava
- Klávesové skratky (ENTER, ESC)
- Quick search (zelený header, šípky ←→)

### ❌ Nefunguje (potrebuje opravu)
- Grid settings - aplikácia spadne pri štarte
- Chybná implementácia invoice_list_widget.py

### 🔧 Chyby na opravu

**Posledná chyba:**
```
AttributeError: 'InvoiceListWidget' object has no attribute '_on_selection_changed'
```

**Príčina:**  
Metóda `_setup_ui()` v `invoice_list_widget.py` je rozbitá - boli pridané metódy grid settings, ale súčasne sa stratili pôvodné metódy:
- `_on_selection_changed()`
- `_on_double_clicked()`

**Riešenie pre ďalší chat:**
1. Obnoviť pôvodný funkčný stav `invoice_list_widget.py` z Git
2. Systematicky integrovať grid settings bez narušenia existujúceho kódu
3. Vytvoriť jeden komplexný script namiesto postupných opráv

## Lessons Learned

### Čo fungovalo dobre
- Systematický prístup k window settings
- Diagnostické skripty odhalili problémy rýchlo
- Raw string docstrings (r""") pre cesty s backslash

### Čo nefungovalo
- Postupné opravy invoice_list_widget.py viedli k rozbití súboru
- Script 20 mal pridať všetky metódy naraz, ale nepodarilo sa
- Viacero skriptov sa pokúšalo opraviť to isté → chaos

### Odporúčania pre budúcnosť
- Pri komplexných zmenách: obnoviť súbor z Git a spraviť jednu úplnú zmenu
- Používať backup súborov pred každou zmenou
- Testovať aplikáciu po každom scripte
- Nevytvárať viac ako 3-4 opravné skripty na jednu vec

## Štatistiky

- **Celkový čas:** ~3 hodiny
- **Vytvorené skripty:** 35
- **Modifikované súbory:** 8
- **Vytvorené nové súbory:** 3
- **Pridané riadky kódu:** ~800+
- **Token usage:** 112K / 190K (59%)

## Ďalšie kroky

### Priorita 1: Opraviť grid settings
1. Git restore `invoice_list_widget.py` na fungujúcu verziu
2. Vytvoriť komplexný script ktorý:
   - Pridá importy
   - Pridá volanie `_load_grid_settings()` do `__init__`
   - Pripojí signály v `_setup_ui`
   - Pridá všetky 4 metódy naraz
3. Otestovať funkčnosť

### Priorita 2: Rozšírenie
- Grid settings pre invoice items grid
- Skrývanie/zobrazovanie stĺpcov (context menu)
- Resetovanie nastavení na default

### Priorita 3: Deployment
- Deployment do Production (Mágerstav)
- Testovanie s reálnymi používateľmi
- Dokumentácia pre používateľa

## Súbory na commit

### Nové súbory
```
src/utils/constants.py
src/utils/window_settings.py
src/utils/grid_settings.py
scripts/01_create_constants.py
... (scripts 02-35)
```

### Modifikované súbory
```
src/utils/__init__.py
src/ui/main_window.py
src/ui/widgets/invoice_list_widget.py
src/ui/widgets/quick_search.py
```

### Databázy (nie v Git)
```
C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db
C:\NEX\YEARACT\SYSTEM\SQLITE\grid_settings.db (empty)
```

## Poznámky

- Všetky cesty v docstringoch musia byť raw strings: `r"""`
- SQLite databázy sú v `C:\NEX\YEARACT\SYSTEM\SQLITE\` (centrálne)
- Prefix "sie" (Supplier Invoice Editor) pre odlíšenie od iných aplikácií
- Window settings sú plne funkčné a otestované ✅
- Grid settings potrebujú dokončenie v ďalšom chate