# base_window.py

**Path:** `packages\nex-shared\ui\base_window.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

BaseWindow - univerzálna base trieda pre všetky okná
Automatická window persistence (position, size, maximize state).

---

## Classes

### BaseWindow(QMainWindow)

Base trieda pre všetky okná v NEX Automat systéme.

Automaticky:
- Načíta window settings pri otvorení
- Uloží window settings pri zatvorení
- Validuje pozície
- Podporuje multi-monitor
- Persistence maximize state

Použitie:
    class MyWindow(BaseWindow):
        def __init__(self):
            super().__init__(
                window_name="my_unique_window",
                default_size=(800, 600),
                default_pos=(100, 100)
            )
            self.setup_ui()  # Tvoj UI

**Methods:**

#### `__init__(self, window_name, default_size, default_pos, user_id, auto_load, parent)`

Inicializácia BaseWindow.

Args:
    window_name: Jedinečný identifikátor okna (napr. "invoice_editor_main")
    default_size: Default veľkosť (width, height) ak nie sú settings
    default_pos: Default pozícia (x, y) ak nie sú settings
    user_id: User ID pre multi-user support
    auto_load: Ak True, automaticky načíta settings
    parent: Parent widget

#### `_load_and_apply_settings(self)`

Načíta a aplikuje window settings z DB.

#### `_save_settings(self)`

Uloží window settings do DB.

#### `closeEvent(self, event)`

Override closeEvent to save settings.

#### `save_window_settings(self)`

Manuálne uloženie window settings (napr. pri Apply button).

#### `reload_window_settings(self)`

Manuálne reload window settings.

#### `get_window_settings(self)`

Získaj aktuálne window settings z DB.

Returns:
    dict: Settings alebo None

#### `delete_window_settings(self)`

Vymaž window settings z DB.

#### `window_name(self)`

Vráti window name.

---
