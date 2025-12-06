# INIT PROMPT - Nový chat (supplier-invoice-editor)

## KONTEXT Z PREDCHÁDZAJÚCEHO CHATU

Úspešne implementovaný **BaseGrid pattern** s plnou persistence funkčnosťou (column widths + active column).

---

## AKTUÁLNY STAV PROJEKTU

**Projekt:** supplier-invoice-editor (NEX Automat v2.0)  
**Development:** `C:\Development\nex-automat\apps\supplier-invoice-editor\`  
**Python:** 3.13.7 (venv32)  
**Git Branch:** develop

---

## ČO JE NOVÉ

### BaseGrid Pattern - KOMPLETNÉ

**Vytvorené v nex-shared:**
- `packages/nex-shared/ui/base_grid.py` - Univerzálna base trieda
- `packages/nex-shared/utils/grid_settings.py` - Persistence do SQLite
- `packages/nex-shared/utils/__init__.py` - Export funkcií

**Funkcionalita:**
- ✅ Automatická QTableView + GreenHeaderView
- ✅ Automatická grid persistence (column widths, active column)
- ✅ QuickSearch integration
- ✅ Auto-load/save settings
- ✅ Disconnect/reconnect signals počas load (no recursive save)
- ✅ Active column signal v QuickSearchController

**Použitie:**
```python
from nex_shared.ui import BaseGrid
from .quick_search import QuickSearchContainer, QuickSearchController

class MyGrid(BaseGrid):
    def __init__(self, parent=None):
        super().__init__(
            window_name=WINDOW_MAIN,
            grid_name=GRID_MY_GRID,
            parent=parent
        )

        # Model
        self.model = MyModel()
        self.table_view.setModel(self.model)

        # Quick search
        self.setup_quick_search(QuickSearchContainer, QuickSearchController)

        # Load settings (MUST be after model and quick search!)
        self.apply_model_and_load_settings()
```

---

### Refaktorované Gridy

**invoice_list_widget.py:**
- Base: QWidget → BaseGrid
- Odstránený _setup_custom_ui() (hardcoded widths)
- Zachované: Model, API, signals
- Persistence: ✅ FUNGUJE

**invoice_items_grid.py:**
- Base: QWidget → BaseGrid
- Odstránený _setup_custom_ui() (hardcoded widths)
- Zachované: Model, editing logic, API
- Persistence: ✅ FUNGUJE

**quick_search.py:**
- Pridaný signal: `active_column_changed = pyqtSignal(int)`
- Emit v `_change_column()` pre save pri šípkach
- GreenHeaderView presunutý do base_grid.py

---

## ŠTRUKTÚRA PROJEKTU

```
nex-automat/
├── packages/
│   └── nex-shared/
│       ├── ui/
│       │   ├── base_window.py      ← Window persistence
│       │   ├── base_grid.py        ← Grid persistence ✅ NEW
│       │   └── __init__.py
│       └── utils/
│           ├── grid_settings.py    ← SQLite persistence ✅ NEW
│           └── __init__.py         ✅ NEW
└── apps/
    └── supplier-invoice-editor/
        └── src/
            └── ui/
                └── widgets/
                    ├── invoice_list_widget.py    ← Uses BaseGrid ✅
                    ├── invoice_items_grid.py     ← Uses BaseGrid ✅
                    └── quick_search.py           ← Updated signal ✅
```

---

## KRITICKÉ PRAVIDLÁ

### BaseGrid Použitie

**Poradie inicializácie (DÔLEŽITÉ!):**
```python
# 1. Init BaseGrid
super().__init__(window_name=..., grid_name=..., parent=...)

# 2. Set model
self.model = MyModel()
self.table_view.setModel(self.model)

# 3. Setup quick search
self.setup_quick_search(QuickSearchContainer, QuickSearchController)

# 4. Load settings (MUST BE LAST!)
self.apply_model_and_load_settings()
```

**NIKDY:**
- ❌ Nevolať `_setup_custom_ui()` s hardcoded widths
- ❌ Nevolať `apply_model_and_load_settings()` pred setup_quick_search()
- ❌ Meniť header signals manuálne (BaseGrid ich riadi)

---

## PERSISTENCE LOCATIONS

```
Window settings: C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db
Grid settings:   C:\NEX\YEARACT\SYSTEM\SQLITE\grid_settings.db
```

**Databázové tabuľky:**
- `grid_column_settings` - column_name, width, visual_index, visible
- `grid_settings` - active_column_index

---

## WORKFLOW

### Development → Git → Deployment
```
1. Zmeny v Development
2. Test lokálne
3. Git commit & push
4. Pull v Deployment
5. Restart aplikácie
```

**NIKDY nerobiť zmeny priamo v Deployment!**

---

## DEBUG TOOLS

**Debug výpisy v console:**
- `[LOAD]` - načítavanie settings z DB
- `[DEBUG]` - ukladanie settings do DB
- `[ACTIVE]` - zmena active column

**Diagnostický script:**
```powershell
python scripts\06_diagnose_grid_settings.py
```

---

## TESTING CHECKLIST

Pri testovaní novej funkcionality:
- [ ] Spustiť aplikáciu bez errors
- [ ] Grid zobrazuje dáta správne
- [ ] Quick search funguje (zelený header)
- [ ] Column widths persistence (resize → restart → check)
- [ ] Active column persistence (šípky → restart → check)
- [ ] Sorting funguje
- [ ] Editácia funguje (ak applicable)

---

## ZNÁME LIMITÁCIE

**nex-shared package:**
- Používa FLAT štruktúru (nex-shared appears ONLY ONCE in path)
- Po zmenách v nex-shared: `pip install -e .` v packages/nex-shared

**Grid persistence:**
- Settings sú per user (default: "Server")
- Last-write-wins pri concurrent updates
- Vymazať DB pre reset: `del C:\NEX\YEARACT\SYSTEM\SQLITE\grid_settings.db`

---

## MOŽNÉ BUDÚCE ÚLOHY

1. **Aplikovať BaseGrid na ďalšie gridy** v systéme
2. **Odstrániť debug print statements** (nahradiť logger calls)
3. **Pridať context menu** pre grid (reset settings, export/import)
4. **Multi-user testing** (rôzne user_id values)
5. **Unit testy** pre BaseGrid
6. **Dokumentácia** pre vývojárov

---

## PRÍKLADY POUŽITIA

### Jednoduchý Read-Only Grid
```python
class SimpleGrid(BaseGrid):
    def __init__(self, parent=None):
        super().__init__(
            window_name="my_window",
            grid_name="simple_grid",
            parent=parent
        )
        
        self.model = SimpleModel()
        self.table_view.setModel(self.model)
        self.setup_quick_search(QuickSearchContainer, QuickSearchController)
        self.apply_model_and_load_settings()
```

### Editable Grid
```python
class EditableGrid(BaseGrid):
    items_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(
            window_name="my_window",
            grid_name="editable_grid",
            parent=parent
        )
        
        self.model = EditableModel()
        self.table_view.setModel(self.model)
        self.setup_quick_search(QuickSearchContainer, QuickSearchController)
        
        # Connect model signals
        self.model.dataChanged.connect(self.items_changed.emit)
        
        self.apply_model_and_load_settings()
```

---

**Init Prompt Created:** 2025-12-06  
**Status:** BaseGrid plne funkčný  
**Ready for:** Production deployment a ďalší vývoj