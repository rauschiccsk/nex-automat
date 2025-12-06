# INIT PROMPT - Nový chat (supplier-invoice-editor)

## KONTEXT Z PREDCHÁDZAJÚCEHO CHATU

Úspešne implementovaný **BaseGrid** pattern v nex-automat projekte.

---

## AKTUÁLNY STAV PROJEKTU

**Projekt:** supplier-invoice-editor (NEX Automat v2.0)  
**Development:** `C:\Development\nex-automat\apps\supplier-invoice-editor\`  
**Python:** 3.13.7 (venv32)  
**Git Branch:** develop

---

## ČO JE NOVÉ

### BaseGrid v nex-shared

**Vytvorené:**
- `packages/nex-shared/ui/base_grid.py` - Univerzálna base trieda pre gridy
- Exportované v `packages/nex-shared/ui/__init__.py`

**Funkcionalita:**
- Automatická QTableView + GreenHeaderView
- Automatická grid persistence (column widths, active column)
- QuickSearch integration
- Auto-load/save settings

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

        # Load settings
        self.apply_model_and_load_settings()
```

---

### Refaktorované Gridy

**invoice_list_widget.py:**
- Base: QWidget → BaseGrid
- Odstránený duplicitný kód (~150 riadkov)
- Zachované: Model, API, signals

**invoice_items_grid.py:**
- Base: QWidget → BaseGrid
- Odstránený duplicitný kód (~150 riadkov)
- Zachované: Model, editing logic, API

**quick_search.py:**
- Odstránený GreenHeaderView (teraz v BaseGrid)
- Vyčistené (~70 riadkov)

---

## ŠTRUKTÚRA PROJEKTU

```
nex-automat/
├── packages/
│   └── nex-shared/
│       └── ui/
│           ├── base_window.py      ← Window persistence
│           ├── base_grid.py        ← Grid persistence (NEW!)
│           └── __init__.py
└── apps/
    └── supplier-invoice-editor/
        └── src/
            └── ui/
                └── widgets/
                    ├── invoice_list_widget.py    ← Uses BaseGrid
                    ├── invoice_items_grid.py     ← Uses BaseGrid
                    └── quick_search.py           ← Clean
```

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

## POUŽÍVANÉ PATTERNS

### BaseWindow Pattern
```python
class MyWindow(BaseWindow):
    def __init__(self):
        super().__init__(
            window_name="unique_name",
            default_size=(800, 600)
        )
```

### BaseGrid Pattern (NEW!)
```python
class MyGrid(BaseGrid):
    def __init__(self, parent=None):
        super().__init__(
            window_name=WINDOW_MAIN,
            grid_name=GRID_NAME,
            parent=parent
        )
        # Model setup
        # Quick search setup
        # Load settings
```

---

## TESTING CHECKLIST

Pri testovaní BaseGrid refactoringu:
- [ ] Spustiť aplikáciu
- [ ] Invoice list zobrazuje dáta
- [ ] Quick search funguje (zelený header)
- [ ] Column widths sa ukladajú
- [ ] Active column sa ukladá
- [ ] Sorting funguje
- [ ] Invoice detail grid funguje
- [ ] Editácia položiek funguje

---

## POZNÁMKY

### Import Paths
```python
# BaseGrid import
from nex_shared.ui import BaseGrid

# QuickSearch import (lokálne)
from .quick_search import QuickSearchContainer, QuickSearchController
```

### Persistence Locations
```
Window settings: C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db
Grid settings:   C:\NEX\YEARACT\SYSTEM\SQLITE\grid_settings.db
```

---

**Init Prompt Created:** 2025-12-06  
**Status:** BaseGrid implementovaný a otestovaný  
**Ready for:** Nové gridy a ďalší vývoj
