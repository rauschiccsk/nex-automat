# grid_settings.py

**Path:** `packages\nex-shared\utils\grid_settings.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Modul pre ukladanie a načítavanie grid a column nastavení.

Používa SQLite databázu v C:\NEX\YEARACT\SYSTEM\SQLITE\grid_settings.db
Databáza je zdieľaná medzi všetkými NEX aplikáciami.

---

## Functions

### `get_grid_settings_db_path()`

Vráti cestu k grid_settings.db v NEX systémovom priečinku.

Returns:
    str: Absolútna cesta k databáze

---

### `init_grid_settings_db()`

Inicializuje databázu grid_settings.db ak ešte neexistuje.
Vytvorí tabuľky grid_column_settings a grid_settings.

---

### `get_current_user_id()`

Vráti identifikátor aktuálneho používateľa.

Momentálne používa Windows username (os.getenv('USERNAME')).
V budúcnosti môže byť nahradené aplikačným prihlásením.

Returns:
    str: Identifikátor používateľa

---

### `load_column_settings(window_name, grid_name, user_id)`

Načíta uložené nastavenia stĺpcov pre daný grid.

Args:
    window_name: Identifikátor okna (napr. 'sie_main_window')
    grid_name: Identifikátor gridu (napr. 'invoice_list')
    user_id: ID používateľa (ak None, použije sa aktuálny Windows username)

Returns:
    List[Dict]: Zoznam slovníkov s nastaveniami stĺpcov
               [{'column_name': 'id', 'width': 100, 'visual_index': 0, 'visible': True}, ...]
               Prázdny list ak neexistuje

---

### `save_column_settings(window_name, grid_name, columns, user_id)`

Uloží nastavenia stĺpcov pre daný grid.

Args:
    window_name: Identifikátor okna
    grid_name: Identifikátor gridu
    columns: Zoznam slovníkov s nastaveniami stĺpcov
            [{'column_name': 'id', 'width': 100, 'visual_index': 0, 'visible': True}, ...]
    user_id: ID používateľa (ak None, použije sa aktuálny Windows username)

Returns:
    bool: True ak úspešné, False pri chybe

---

### `load_grid_settings(window_name, grid_name, user_id)`

Načíta grid-level nastavenia (aktívny stĺpec).

Args:
    window_name: Identifikátor okna
    grid_name: Identifikátor gridu
    user_id: ID používateľa (ak None, použije sa aktuálny Windows username)

Returns:
    Dict s kľúčom 'active_column_index' alebo None ak neexistuje

---

### `save_grid_settings(window_name, grid_name, active_column_index, user_id)`

Uloží grid-level nastavenia (aktívny stĺpec).

Args:
    window_name: Identifikátor okna
    grid_name: Identifikátor gridu
    active_column_index: Index aktívneho stĺpca
    user_id: ID používateľa (ak None, použije sa aktuálny Windows username)

Returns:
    bool: True ak úspešné, False pri chybe

---
