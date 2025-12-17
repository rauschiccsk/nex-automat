# base_grid.py

**Path:** `packages\nex-shared\ui\base_grid.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

BaseGrid - univerzálna base trieda pre všetky gridy
Automatická grid persistence (column widths, active column, quick search).

---

## Classes

### GreenHeaderView(QHeaderView)

Custom QHeaderView s green highlighting pre active column

**Methods:**

#### `__init__(self, orientation, parent)`

#### `paintSection(self, painter, rect, logicalIndex)`

Custom paint pre každý header section

#### `set_active_column(self, column)`

Nastav ktorý column je active pre search

---

### BaseGrid(QWidget)

Base trieda pre všetky gridy v NEX Automat systéme.

Automaticky:
- Vytvorí QTableView s GreenHeaderView
- Pridá QuickSearchContainer (musí byť importovaný potomkom)
- Načíta column settings pri inicializácii
- Uloží column settings pri zmene
- Persistence active column

Použitie:
    class MyGrid(BaseGrid):
        def __init__(self, parent=None):
            super().__init__(
                window_name="my_window",
                grid_name="my_grid",
                parent=parent
            )
            # Create model
            self.model = MyModel()
            self.table_view.setModel(self.model)

            # Špecifická logika
            self._setup_custom_stuff()

**Methods:**

#### `__init__(self, window_name, grid_name, user_id, auto_load, parent)`

Inicializácia BaseGrid.

Args:
    window_name: Identifikátor okna (napr. "sie_main_window")
    grid_name: Identifikátor gridu (napr. "invoice_list")
    user_id: User ID pre multi-user support
    auto_load: Ak True, automaticky načíta settings
    parent: Parent widget

#### `_setup_base_ui(self)`

Setup základného UI s QTableView a QuickSearch.

#### `setup_quick_search(self, QuickSearchContainer, QuickSearchController)`

Setup quick search functionality.

MUSÍ byť zavolaný potomkom ABY fungoval quick search.

Args:
    QuickSearchContainer: Trieda QuickSearchContainer z widgets
    QuickSearchController: Trieda QuickSearchController z widgets

#### `_load_grid_settings(self)`

Načíta a aplikuje uložené nastavenia gridu.

#### `_save_grid_settings(self)`

Uloží aktuálne nastavenia gridu.

#### `_on_active_column_changed(self, column)`

Handler pre zmenu active column.

#### `_on_column_resized(self, logical_index, old_size, new_size)`

Handler pre zmenu šírky stĺpca.

#### `_on_column_moved(self, logical_index, old_visual_index, new_visual_index)`

Handler pre presunutie stĺpca.

#### `apply_model_and_load_settings(self)`

Aplikuje settings PO nastavení modelu.

MUSÍ byť zavolaný potomkom PO self.table_view.setModel()!

#### `save_grid_settings_now(self)`

Manuálne uloženie grid settings (napr. pri Apply button).

#### `reload_grid_settings(self)`

Manuálne reload grid settings.

#### `window_name(self)`

Vráti window name.

#### `grid_name(self)`

Vráti grid name.

---
