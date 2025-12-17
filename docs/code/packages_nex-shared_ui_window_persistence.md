# window_persistence.py

**Path:** `packages\nex-shared\ui\window_persistence.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Window Persistence Manager
Validácia a persistence logika pre okná.

---

## Classes

### WindowPersistenceManager

Manager pre window persistence s validáciou a multi-monitor supportom.

Singleton pattern.

**Methods:**

#### `__new__(cls)`

#### `validate_position(cls, x, y, width, height)`

Validuje či je window position platná.

Args:
    x, y: Window position
    width, height: Window size

Returns:
    bool: True ak je pozícia platná

#### `get_monitor_geometry(cls, screen_index)`

Vráti geometriu monitora.

Args:
    screen_index: Index monitora (0 = primary)

Returns:
    QRect: Geometria monitora alebo None

#### `find_monitor_for_position(cls, x, y)`

Nájde monitor ktorý obsahuje danú pozíciu.

Args:
    x, y: Pozícia okna

Returns:
    int: Index monitora alebo 0 (primary)

#### `get_safe_position(cls, settings, default_size, default_pos)`

Vráti bezpečnú pozíciu okna.

Ak settings sú None alebo invalid, použije default hodnoty.

Args:
    settings: Načítané settings z DB alebo None
    default_size: Default veľkosť (width, height)
    default_pos: Default pozícia (x, y)

Returns:
    dict: Safe settings {'x', 'y', 'width', 'height', 'window_state'}

#### `log_monitor_info(cls)`

Log info o všetkých monitoroch (pre debugging).

---
