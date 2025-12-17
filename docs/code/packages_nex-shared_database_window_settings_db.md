# window_settings_db.py

**Path:** `packages\nex-shared\database\window_settings_db.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Window Settings Database Layer
Univerzálne DB operácie pre window persistence.

---

## Classes

### WindowSettingsDB

Database layer for window settings persistence.

Singleton pattern - jedna inštancia pre celú aplikáciu.

**Methods:**

#### `__new__(cls, db_path)`

#### `_init_db(self)`

Initialize database and create table if not exists.

#### `save(self, window_name, x, y, width, height, window_state, user_id)`

Save window settings using DELETE + INSERT pattern.

Args:
    window_name: Unique window identifier
    x, y: Window position
    width, height: Window size
    window_state: 0=normal, 2=maximized
    user_id: User identifier

Returns:
    bool: True if successful

#### `load(self, window_name, user_id)`

Load window settings from database.

Args:
    window_name: Unique window identifier
    user_id: User identifier

Returns:
    dict: {'x', 'y', 'width', 'height', 'window_state'} or None

#### `delete(self, window_name, user_id)`

Delete window settings from database.

Args:
    window_name: Unique window identifier
    user_id: User identifier

Returns:
    bool: True if successful

---
