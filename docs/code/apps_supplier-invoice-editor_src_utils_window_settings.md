# window_settings.py

**Path:** `apps\supplier-invoice-editor\src\utils\window_settings.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Window and Grid Settings Persistence
Grid settings functions (active column) - window persistence je v BaseWindow.

---

## Functions

### `save_grid_settings(window_name, grid_name, active_column, user_id)`

Save grid settings (active column).

Args:
    window_name: Window identifier
    grid_name: Grid identifier
    active_column: Active column index
    user_id: User ID

Returns:
    bool: True if successful

---

### `load_grid_settings(window_name, grid_name, user_id)`

Load grid settings (active column).

Args:
    window_name: Window identifier
    grid_name: Grid identifier
    user_id: User ID

Returns:
    int: Active column index or None

---
