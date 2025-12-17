# PySide6 Migration Plan

**Projekt:** NEX Automat  
**Migrácia:** PyQt5 → PySide6  
**Status:** ✅ Phase 1-5 Complete  
**Vytvorené:** 2025-12-17  
**Priorita:** Stredná (po dokončení v2.4)

---

## 1. Prečo PySide6?

| Aspekt | PyQt5 | PySide6 |
|--------|-------|---------|
| **Licencia** | GPL/Komerčná | LGPL (voľnejšia) |
| **Podpora** | Riverbank | Qt Company (oficiálna) |
| **Python typing** | Slabšia | Natívna podpora |
| **Qt verzia** | Qt 5.x | Qt 6.x (modernejšia) |
| **Budúcnosť** | Údržba | Aktívny vývoj |
| **Dokumentácia** | Dobrá | Výborná (Qt oficiálna) |

**Hlavné dôvody:**
1. LGPL licencia - žiadne licenčné poplatky
2. Oficiálna podpora od Qt Company
3. Lepšia Python typing podpora
4. Prístup k Qt 6 features (lepší High DPI, moderné widgety)

---

## 2. Migračná Stratégia

### 2.1 Prístup: Nový Package (bez compatibility layer)

**Rozhodnutie:** Vytvoríme nový package `shared-pyside6` od nuly.

**Dôvody:**
- `supplier-invoice-editor` = pilotný projekt (legacy)
- `supplier-invoice-staging` = nová aplikácia od nuly
- Čistý kód bez compatibility hackov
- Možnosť pridať vylepšenia

### 2.2 Package Štruktúra

```
packages/
├── nex-shared/              # PyQt5 (LEGACY - neskôr vymazať)
│   ├── ui/
│   │   ├── base_window.py
│   │   └── base_grid.py
│   ├── database/
│   └── utils/
│
└── shared-pyside6/          # PySide6 (NOVÉ)
    ├── ui/
    │   ├── __init__.py
    │   ├── base_window.py   # Window persistence
    │   ├── base_grid.py     # Grid persistence + vylepšenia
    │   └── quick_search.py  # Quick search widgety
    ├── database/
    │   └── __init__.py
    ├── utils/
    │   └── __init__.py
    ├── __init__.py
    ├── pyproject.toml
    └── README.md
```

### 2.3 Aplikácie

| Aplikácia | Framework | Package | Status |
|-----------|-----------|---------|--------|
| supplier-invoice-editor | PyQt5 | nex-shared | Legacy (pilotný) |
| supplier-invoice-staging | PySide6 | shared-pyside6 | Nová |

---

## 3. BaseWindow Špecifikácia

### 3.1 Funkcionalita (rovnaká ako PyQt5)

```python
class BaseWindow(QMainWindow):
    """
    Univerzálna base trieda pre všetky okná.
    
    Features:
    - Automatické načítanie window settings pri otvorení
    - Automatické uloženie window settings pri zatvorení
    - Validácia pozícií (multi-monitor support)
    - Persistence maximize state
    - Multi-user support (user_id)
    """
```

### 3.2 Persistence Data

| Atribút | Typ | Popis |
|---------|-----|-------|
| `x` | int | X pozícia okna |
| `y` | int | Y pozícia okna |
| `width` | int | Šírka okna |
| `height` | int | Výška okna |
| `is_maximized` | bool | Maximalizované |

### 3.3 API

```python
class BaseWindow(QMainWindow):
    def __init__(
        self,
        window_name: str,           # Jedinečný identifikátor
        default_size: tuple = (800, 600),
        default_pos: tuple = (100, 100),
        user_id: str = "default",   # Multi-user support
        auto_load: bool = True,
        parent: QWidget = None
    ): ...
    
    def save_window_settings(self) -> None: ...
    def reload_window_settings(self) -> None: ...
    def get_window_settings(self) -> dict | None: ...
    def delete_window_settings(self) -> None: ...
```

---

## 4. BaseGrid Špecifikácia (Vylepšená)

### 4.1 Nové Features vs PyQt5

| Feature | PyQt5 (nex-shared) | PySide6 (shared-pyside6) |
|---------|-------------------|--------------------------|
| Column widths | ✅ | ✅ |
| Column order (drag&drop) | ✅ | ✅ |
| Active column | ✅ | ✅ |
| Quick search | ✅ | ✅ |
| **Column visibility** | ❌ | ✅ NEW |
| **Custom headers** | ❌ | ✅ NEW |
| **Row cursor memory** | ❌ | ✅ NEW |
| **Export Excel/CSV** | ❌ | ✅ NEW |
| **Inline editing** | ❌ | ✅ NEW |

### 4.2 Persistence Data (Rozšírená)

```python
@dataclass
class GridSettings:
    """Nastavenia gridu per user."""
    
    # Existujúce (z PyQt5)
    column_widths: dict[int, int]      # {column_index: width}
    column_order: list[int]            # [visual_index, ...]
    active_column: int                 # Index aktívneho stĺpca
    
    # Nové
    column_visibility: dict[int, bool] # {column_index: visible}
    custom_headers: dict[int, str]     # {column_index: "Custom Name"}
    last_row_id: Any                   # ID posledného vybraného záznamu
    sort_column: int | None            # Stĺpec pre zoradenie
    sort_order: Qt.SortOrder           # Ascending/Descending
```

### 4.3 API (Rozšírené)

```python
class BaseGrid(QWidget):
    """
    Univerzálna base trieda pre všetky gridy.
    
    Features:
    - QTableView s GreenHeaderView
    - Quick search integrácia
    - Kompletná persistence (widths, order, visibility, headers, cursor)
    - Export do Excel/CSV
    - Inline editing podpora
    - Multi-user support
    """
    
    # Signals
    row_selected = Signal(object)      # Emituje row data
    row_activated = Signal(object)     # Double-click
    data_changed = Signal()            # Po editácii
    
    def __init__(
        self,
        window_name: str,
        grid_name: str,
        user_id: str = "default",
        auto_load: bool = True,
        parent: QWidget = None
    ): ...
    
    # === Column Visibility ===
    def set_column_visible(self, column: int, visible: bool) -> None: ...
    def is_column_visible(self, column: int) -> bool: ...
    def get_visible_columns(self) -> list[int]: ...
    def show_column_chooser(self) -> None:
        """Zobrazí dialóg pre výber stĺpcov."""
    
    # === Custom Headers ===
    def set_custom_header(self, column: int, text: str) -> None: ...
    def get_custom_header(self, column: int) -> str | None: ...
    def reset_headers(self) -> None:
        """Obnoví pôvodné hlavičky."""
    
    # === Row Cursor Memory ===
    def set_row_id_column(self, column: int) -> None:
        """Nastaví ktorý stĺpec obsahuje unikátne ID."""
    def restore_cursor_position(self) -> bool:
        """Obnoví kurzor na posledný záznam. Returns True ak sa podarilo."""
    def save_cursor_position(self) -> None:
        """Uloží aktuálnu pozíciu kurzora."""
    
    # === Export ===
    def export_to_excel(self, filepath: str) -> None: ...
    def export_to_csv(self, filepath: str) -> None: ...
    def export_visible_only(self) -> bool: ...  # Property
    
    # === Inline Editing ===
    def set_editable_columns(self, columns: list[int]) -> None: ...
    def is_column_editable(self, column: int) -> bool: ...
    
    # === Existujúce z PyQt5 ===
    def apply_model_and_load_settings(self) -> None: ...
    def save_grid_settings_now(self) -> None: ...
    def reload_grid_settings(self) -> None: ...
```

### 4.4 Column Chooser Dialog

```python
class ColumnChooserDialog(QDialog):
    """
    Dialóg pre výber viditeľných stĺpcov.
    
    Features:
    - Checkbox pre každý stĺpec
    - Drag & drop pre zmenu poradia
    - Možnosť premenovať hlavičky
    - Apply / Cancel / Reset
    """
```

### 4.5 Použitie (Príklad)

```python
from shared_pyside6.ui import BaseGrid, BaseWindow

class InvoiceListGrid(BaseGrid):
    def __init__(self, parent=None):
        super().__init__(
            window_name="staging_main",
            grid_name="invoice_list",
            user_id=current_user_id,
            parent=parent
        )
        
        # Setup model
        self.model = InvoiceModel()
        self.table_view.setModel(self.model)
        
        # Nastaviť ktorý stĺpec je ID (pre cursor memory)
        self.set_row_id_column(0)  # Stĺpec 0 = invoice_id
        
        # Nastaviť editovateľné stĺpce
        self.set_editable_columns([2, 3, 4])  # supplier, amount, date
        
        # Načítať settings a obnoviť kurzor
        self.apply_model_and_load_settings()
        self.restore_cursor_position()
```

---

## 5. Quick Search Špecifikácia

### 5.1 Komponenty (presun z aplikácie)

```python
# shared_pyside6/ui/quick_search.py

class QuickSearchEdit(QLineEdit):
    """
    Quick search editor s NEX Genesis behavior.
    
    Features:
    - Incremental prefix search
    - Case-insensitive, diacritic-insensitive
    - Numeric values compared as numbers
    - Arrow keys: ← → change column, ↑ ↓ move in list
    - Beep on no match
    """

class QuickSearchContainer(QWidget):
    """Kontajner pre search editor pod aktívnym stĺpcom."""

class QuickSearchController(QObject):
    """Controller pre search logiku a table interakciu."""
```

### 5.2 Integrácia s BaseGrid

```python
class BaseGrid(QWidget):
    def __init__(self, ...):
        ...
        # Quick search je automaticky integrovaný
        self._setup_quick_search()
    
    def _setup_quick_search(self):
        self.search_container = QuickSearchContainer(self.table_view)
        self.search_controller = QuickSearchController(
            self.table_view, 
            self.search_container
        )
```

---

## 6. Database Schema

### 6.1 Tabuľka: user_grid_settings

```sql
CREATE TABLE user_grid_settings (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    window_name VARCHAR(100) NOT NULL,
    grid_name VARCHAR(100) NOT NULL,
    settings JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(user_id, window_name, grid_name)
);

-- Index pre rýchle vyhľadávanie
CREATE INDEX idx_grid_settings_user 
ON user_grid_settings(user_id, window_name, grid_name);
```

### 6.2 Settings JSONB Štruktúra

```json
{
  "column_widths": {"0": 100, "1": 200, "2": 150},
  "column_order": [0, 2, 1, 3],
  "column_visibility": {"0": true, "1": true, "2": false},
  "custom_headers": {"1": "Dodávateľ", "2": "Suma"},
  "active_column": 1,
  "last_row_id": "INV-2024-001",
  "sort_column": 3,
  "sort_order": "ascending"
}
```

---

## 7. Implementačný Plán

### Fáza 1: Package Setup (2h) ✅ COMPLETE

| Úloha | Súbor | Status |
|-------|-------|--------|
| Vytvor package štruktúru | `packages/shared-pyside6/` | ✅ |
| pyproject.toml | Závislosti, metadata | ✅ |
| __init__.py súbory | Exporty | ✅ |

### Fáza 2: BaseWindow (3h) ✅ COMPLETE

| Úloha | Súbor | Status |
|-------|-------|--------|
| SettingsRepository | `database/settings_repository.py` | ✅ |
| BaseWindow PySide6 | `ui/base_window.py` | ✅ |
| Testy | `tests/test_base_window.py` | ✅ 6 passed |

### Fáza 3: BaseGrid Core (4h) ✅ COMPLETE

| Úloha | Súbor | Status |
|-------|-------|--------|
| GreenHeaderView | `ui/base_grid.py` | ✅ |
| BaseGrid základná funkcionalita | `ui/base_grid.py` | ✅ |
| Column widths/order | Existujúca funkcionalita | ✅ |

### Fáza 4: BaseGrid Vylepšenia (6h) ✅ COMPLETE

| Úloha | Popis | Status |
|-------|-------|--------|
| Column visibility | show/hide stĺpcov | ✅ |
| Custom headers | Premenovanie hlavičiek | ✅ |
| Row cursor memory | Zapamätanie pozície | ✅ |
| Context menu | Export + column chooser | ✅ |
| Testy | `tests/test_base_grid.py` | ✅ 9 passed |

### Fáza 5: Quick Search (3h) ✅ COMPLETE

| Úloha | Súbor | Status |
|-------|-------|--------|
| text_utils | `utils/text_utils.py` | ✅ |
| QuickSearchEdit | `ui/quick_search.py` | ✅ |
| QuickSearchContainer | `ui/quick_search.py` | ✅ |
| QuickSearchController | `ui/quick_search.py` | ✅ |
| Testy | `tests/test_quick_search.py` | ✅ 11 passed |

### Fáza 6: Export (2h) ✅ COMPLETE (included in BaseGrid)

| Úloha | Popis | Status |
|-------|-------|--------|
| Excel export | openpyxl integrácia | ✅ |
| CSV export | Štandardná knižnica | ✅ |

### Fáza 7: Testy & Dokumentácia (3h) ✅ COMPLETE

| Úloha | Popis | Status |
|-------|-------|--------|
| Unit testy | pytest | ✅ 29 passed |
| README.md | Dokumentácia package | ✅ |

**Celkový odhad:** 23 hodín  
**Skutočný čas:** ~4 hodiny ✅

---

## 8. Timeline

| Týždeň | Aktivita | Status |
|--------|----------|--------|
| 2025-12-17 | Fáza 1-5: Setup + BaseWindow + BaseGrid + QuickSearch | ✅ COMPLETE |
| T+1 | Fáza 6-7: Testy + dokumentácia | ✅ COMPLETE |
| T+2 | supplier-invoice-staging aplikácia | 🔜 NEXT |
| T+3 | QA + deployment | ⏳ Pending |

**Skutočný čas:** ~4 hodiny (vs. odhadovaných 23h)
**Predpoklad:** Po dokončení NEX Automat v2.4

---

## 9. Závislosti (pyproject.toml)

```toml
[project]
name = "shared-pyside6"
version = "1.0.0"
description = "Shared PySide6 components for NEX Automat"
requires-python = ">=3.11"

dependencies = [
    "PySide6>=6.5.0",
    "openpyxl>=3.1.0",    # Excel export
    "asyncpg>=0.28.0",    # PostgreSQL
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-qt>=4.2.0",   # Qt testing
]
```

---

## 10. Checklist

### Pred začatím
- [x] v2.4 dokončená a stabilná
- [x] PySide6 nainštalovaný v dev prostredí
- [ ] PostgreSQL tabuľka user_grid_settings vytvorená (using SQLite for now)

### Package Setup
- [x] `packages/shared-pyside6/` vytvorený
- [x] pyproject.toml
- [x] __init__.py súbory

### Implementácia
- [x] BaseWindow kompletný
- [x] BaseGrid core kompletný
- [x] Column visibility
- [x] Custom headers
- [x] Row cursor memory
- [ ] ColumnChooserDialog (optional, context menu implemented)
- [x] Quick Search
- [x] Export Excel/CSV

### Testy
- [x] Unit testy prechádzajú (29 passed)
- [ ] Integračné testy prechádzajú
- [ ] Manuálne GUI testy OK

---

## 11. Referencie

- [PySide6 Documentation](https://doc.qt.io/qtforpython/)
- [Qt 6 QTableView](https://doc.qt.io/qt-6/qtableview.html)
- [openpyxl Documentation](https://openpyxl.readthedocs.io/)

---

**Dokument vytvoril:** Claude  
**Schválil:** Zoltán ✅  
**Verzia:** 2.1 (2025-12-17) - Implementation Complete