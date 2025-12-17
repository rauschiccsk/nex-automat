# quick_search.py

**Path:** `apps\supplier-invoice-editor\src\ui\widgets\quick_search.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Quick Search Widget - NEX Genesis style incremental search
Rýchlo-vyhľadávač v štýle NEX Genesis

Note: GreenHeaderView is now in nex-shared/ui/base_grid.py

---

## Classes

### QuickSearchEdit(QLineEdit)

Quick search editor with NEX Genesis behavior

Features:
- Incremental prefix search
- Case-insensitive, diacritic-insensitive
- Numeric values compared as numbers
- Arrow keys: ← → change column, ↑ ↓ move in list + clear
- Beep on no match

**Methods:**

#### `__init__(self, parent)`

#### `_setup_appearance(self)`

Setup green background and styling

#### `_on_text_changed(self, text)`

Handle text change

#### `keyPressEvent(self, event)`

Handle key press events

#### `trigger_beep(self)`

Trigger system beep

---

### QuickSearchContainer(QWidget)

Container for quick search that positions editor under active column

**Methods:**

#### `__init__(self, table_view, parent)`

#### `_update_position(self)`

Update editor position to match current column

#### `set_column(self, column)`

Set active search column

#### `_highlight_header(self, column)`

Highlight active column header with green background

---

### QuickSearchController(QObject)

Controller for quick search functionality
Handles search logic and table interaction

**Methods:**

#### `__init__(self, table_view, search_container)`

Initialize quick search controller

Args:
    table_view: QTableView instance
    search_container: QuickSearchContainer instance

#### `eventFilter(self, obj, event)`

Filter events from table view to redirect to search edit

#### `_connect_signals(self)`

Connect widget signals

#### `_sort_by_column(self, column)`

Sort table by column - force visual reordering

#### `_change_column(self, direction)`

Change search column

#### `_change_row(self, direction)`

Move to next/previous row

#### `_on_search(self, search_text)`

Handle search text change

#### `_find_match(self, search_text, column)`

Find first row matching search text (prefix)

Args:
    search_text: Text to search for
    column: Column index to search in

Returns:
    Row index or None if no match

#### `get_active_column(self)`

Vráti index aktuálne aktívneho stĺpca.

Returns:
    int: Index aktívneho stĺpca

#### `set_active_column(self, column)`

Nastaví aktívny stĺpec a aktualizuje UI.

Args:
    column: Index stĺpca

#### `set_column(self, column)`

Set active search column programmatically

---
