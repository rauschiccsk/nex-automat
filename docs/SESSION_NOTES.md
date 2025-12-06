# Session Notes - Window Persistence Fix

**Dátum:** 2025-12-06  
**Projekt:** NEX Automat v2.0 - supplier-invoice-editor  
**Téma:** Oprava window persistence - zachovávanie pozície a rozmerov okien

---

## Dosiahnuté výsledky

### ✅ Window Size Persistence (BaseWindow)
**Problém:** Okná sa otvorili vždy s default rozmermi (1400x900) namiesto uložených rozmerov z databázy.

**Riešenia:**
1. **get_safe_position() bug** - Metóda vracala default rozmery pri invalid pozícii
   - Opravené: Opravuje len pozíciu, zachováva rozmery z DB
   - Súbor: `packages/nex-shared/ui/window_persistence.py`

2. **MainWindow resize() konflikt** - Volanie `resize(1400, 900)` prepisovalo načítané rozmery
   - Opravené: Odstránené volanie, BaseWindow kontroluje rozmery
   - Súbor: `apps/supplier-invoice-editor/src/ui/main_window.py`

3. **Window position drift** - Okno sa posúvalo pri každom otvorení kvôli frame geometry
   - Opravené: Použitie `pos()` + `resize()` namiesto `setGeometry()`
   - Súbor: `packages/nex-shared/ui/base_window.py`

### ✅ Grid Settings Error Fix
**Problém:** Chyba "type 'dict' is not supported" pri ukladaní grid settings.

**Riešenie:**
- Opravené volanie `save_grid_settings()` s int namiesto dict
- Súbor: `apps/supplier-invoice-editor/src/ui/widgets/invoice_items_grid.py`
- Zmena: `save_grid_settings(WINDOW_MAIN, GRID_INVOICE_ITEMS, -1)` namiesto dict

### ✅ InvoiceDetailWindow Persistence
**Problém:** Detail okno (s položkami faktúry) nededilo z BaseWindow → bez persistence.

**Riešenia:**
1. Zmena dedenia z `QDialog` na `BaseWindow`
2. Pridané importy: `BaseWindow`, `WINDOW_INVOICE_DETAIL`
3. Opravené metódy: `accept()`, `reject()` → `close()`
4. Opravené volanie v MainWindow: `exec_()` → `show()`
5. Opravený layout: používa `central_widget` pre QMainWindow
6. Pridaný `QWidget` import

### ✅ Klávesové skratky
**Problém:** Stratila sa možnosť otvoriť faktúru klávesou ENTER.

**Riešenie:**
- Pridaný ENTER/RETURN handling do `keyPressEvent()`
- Používa `get_selected_invoice_id()` metódu
- Súbor: `apps/supplier-invoice-editor/src/ui/main_window.py`

---

## Technické detaily

### Upravené súbory

**packages/nex-shared/**
- `ui/base_window.py` - window persistence logika
- `ui/window_persistence.py` - get_safe_position() fix
- `database/window_settings_db.py` - bez zmien (správne)

**apps/supplier-invoice-editor/src/**
- `ui/main_window.py` - odstránené resize(), pridaný ENTER handling
- `ui/invoice_detail_window.py` - zmena na BaseWindow, layout fix
- `ui/widgets/invoice_items_grid.py` - oprava save_grid_settings()

### Databázová štruktúra
```sql
-- C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db
CREATE TABLE window_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    window_name TEXT NOT NULL,
    x INTEGER,
    y INTEGER,
    width INTEGER,
    height INTEGER,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    window_state INTEGER DEFAULT 0,  -- 0=Normal, 2=Maximized
    UNIQUE(user_id, window_name)
);
```

### Window Names
- `WINDOW_MAIN = "sie_main_window"` - hlavné okno so zoznamom faktúr
- `WINDOW_INVOICE_DETAIL = "sie_invoice_detail"` - detail okno s položkami

---

## Kľúčové poznatky

### BaseWindow Pattern
```python
# Správne použitie BaseWindow
class MyWindow(BaseWindow):
    def __init__(self, parent=None):
        super().__init__(
            window_name="unique_window_id",
            default_size=(800, 600),
            default_pos=(100, 100),
            parent=parent
        )
        # Layout pre QMainWindow vyžaduje central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
```

### Window Persistence Flow
1. **Load:** `_load_and_apply_settings()` v `__init__`
   - Načíta z DB cez `WindowSettingsDB.load()`
   - Validuje cez `WindowPersistenceManager.get_safe_position()`
   - Aplikuje cez `move()` + `resize()`

2. **Save:** `_save_settings()` v `closeEvent()`
   - Získa rozmery cez `pos()` a `size()`
   - Validuje a opraví pozíciu ak je invalid
   - Uloží cez `WindowSettingsDB.save()`

### Kritické body
- ❌ NIKDY nepoužívať `self.resize()` po inicializácii BaseWindow
- ❌ NIKDY nepoužívať `setGeometry()` - spôsobuje position drift
- ✅ VŽDY používať `move()` + `resize()` pre nastavenie pozície/rozmerov
- ✅ VŽDY používať `pos()` + `size()` pre získanie pozície/rozmerov
- ✅ QMainWindow vyžaduje `setCentralWidget()` pre layout

---

## Testovanie

### Test 1: Hlavné okno persistence
1. Spustiť aplikáciu
2. Zmeniť veľkosť okna (napr. 800x600)
3. Zatvoriť aplikáciu
4. Otvoriť znova → rozmery 800x600 ✅

### Test 2: Detail okno persistence
1. Otvoriť faktúru (double-click alebo ENTER)
2. Zmeniť veľkosť detail okna
3. Zatvoriť detail okno
4. Otvoriť inú faktúru → rozmery zachované ✅

### Test 3: Position stability
1. Otvoriť/zatvoriť aplikáciu 5x
2. Pozícia by mala ostať stabilná (bez posúvania) ✅

### Test 4: Klávesové skratky
1. Vybrať faktúru v zozname
2. Stlačiť ENTER → detail sa otvorí ✅
3. Stlačiť ESC → aplikácia sa zatvorí ✅

---

## Štatistiky

- **Vytvorené scripty:** 43 (01-43)
- **Upravené súbory:** 6
- **Opravené bugy:** 5
- **Pridané funkcie:** 1 (ENTER handling)
- **Čas riešenia:** ~2.5 hodiny

---

## Ďalšie kroky (budúce session)

### Možné vylepšenia
1. **Multi-monitor support** - validácia pozície pre viacero monitorov
2. **Window state templates** - prednastavené layouty (malý/veľký/maximalizovaný)
3. **Per-user settings** - rôzne rozmery pre rôznych používateľov
4. **Grid column persistence** - zachovanie poradia stĺpcov v grids

### Cleanup
- Vymazať dočasné scripty 01-43 po commite
- Aktualizovať PROJECT_MANIFEST.json

---

## Poznámky pre Development → Deployment

**Development zmeny:**
- `packages/nex-shared/` - shared package s persistence
- `apps/supplier-invoice-editor/src/ui/` - UI komponenty

**Deployment workflow:**
1. Commit changes v Development
2. Git push
3. Git pull v Deployment
4. Restart aplikácie

**Databáza:**
- SQLite: `C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db`
- Automaticky sa vytvorí pri prvom spustení
- Žiadna migrácia potrebná

---

**Session ukončená:** 2025-12-06  
**Status:** ✅ Všetky ciele dosiahnuté