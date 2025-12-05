# Session Notes - Window Maximize State Fix

**Dátum:** 2025-12-06  
**Projekt:** nex-automat v2.0.0  
**Aplikácia:** supplier-invoice-editor  
**Status:** ✅ VYRIEŠENÉ

## Problém

Aplikácia nezapamätala **maximalizovaný stav okna**. Po reštarte sa okno vždy otvorilo v normálnom stave, aj keď bolo zatvorené maximalizované.

## Root Cause Analysis

Našli sa **DVA nezávislé problémy**:

### 1. INSERT OR REPLACE nefungoval správne
- `window_state=2` sa správne posielal do `save_window_settings()`
- `INSERT OR REPLACE` statement ale nezapisoval hodnotu do DB
- V DB zostávalo `window_state=0` napriek commit

### 2. SELECT nečítal window_state stĺpec
- `load_window_settings()` obsahoval: `SELECT x, y, width, height`
- Chýbalo: `window_state` v SELECT
- Return dictionary neobsahoval `window_state` kľúč

## Riešenie

### Fix 1: DELETE + INSERT pattern
**Súbor:** `apps/supplier-invoice-editor/src/utils/window_settings.py`

Zmenené z:
```python
cursor.execute("""
    INSERT OR REPLACE INTO window_settings
    (user_id, window_name, x, y, width, height, window_state, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (user_id, window_name, x, y, width, height, window_state, datetime.now()))
```

Na:
```python
# First DELETE existing record
cursor.execute("""
    DELETE FROM window_settings
    WHERE user_id = ? AND window_name = ?
""", (user_id, window_name))

# Then INSERT new record
cursor.execute("""
    INSERT INTO window_settings
    (user_id, window_name, x, y, width, height, window_state, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (user_id, window_name, x, y, width, height, window_state, datetime.now()))
```

### Fix 2: SELECT window_state
**Súbor:** `apps/supplier-invoice-editor/src/utils/window_settings.py`

Zmenené z:
```python
cursor.execute("""
    SELECT x, y, width, height
    FROM window_settings
    WHERE user_id = ? AND window_name = ?
""", (user_id, window_name))
```

Na:
```python
cursor.execute("""
    SELECT x, y, width, height, window_state
    FROM window_settings
    WHERE user_id = ? AND window_name = ?
""", (user_id, window_name))
```

### Fix 3: Return dictionary
Pridané do return:
```python
return {
    'x': row[0],
    'y': row[1],
    'width': row[2],
    'height': row[3],
    'window_state': row[4] if len(row) > 4 else 0
}
```

### Fix 4: Drobné opravy
- `get_user_id()` → `'Server'` (default user ID)
- `_get_db_connection()` → `sqlite3.connect(db_path)`
- Pridaný `import logging`

## Verifikácia

**Test scenár:**
1. Spusti aplikáciu
2. Maximalizuj okno
3. Zavri aplikáciu
4. Spusti aplikáciu znova
5. ✅ Okno sa otvorí maximalizované

**DB verifikácia:**
```sql
SELECT window_state FROM window_settings WHERE window_name='sie_main_window'
-- Result: 2 (maximized) ✅
```

## Súbory zmenené

1. `apps/supplier-invoice-editor/src/utils/window_settings.py`
   - Funkcia `save_window_settings()` - DELETE + INSERT pattern
   - Funkcia `load_window_settings()` - SELECT window_state, return dictionary

## Scripts vytvorené (dočasné)

1. `scripts/01_diagnose_save_function.py` - diagnostika INSERT
2. `scripts/02_add_debug_to_save.py` - pridanie debug výpisov
3. `scripts/03_fix_logging_import.py` - fix import logging
4. `scripts/04_show_current_db_values.py` - zobrazenie DB hodnôt
5. `scripts/05_delete_window_position.py` - DELETE DB záznamu
6. `scripts/06_verify_db_immediately.py` - verifikácia DB
7. `scripts/07_fix_save_window_settings.py` - DELETE + INSERT fix
8. `scripts/08_fix_syntax_error.py` - oprava syntax error
9. `scripts/09_check_close_event.py` - kontrola closeEvent()
10. `scripts/10_fix_get_user_id_error.py` - fix get_user_id()
11. `scripts/11_fix_db_connection.py` - fix DB connection
12. `scripts/12_fix_db_path_definition.py` - fix DB_PATH
13. `scripts/13_check_load_window_settings.py` - diagnostika load
14. `scripts/14_fix_load_select_statement.py` - fix SELECT + return
15. `scripts/15_cleanup_debug_outputs.py` - cleanup debug

## Výsledok

✅ **Window maximize state persistence FUNGUJE**

- Grid settings persistence: ✅
- Window position persistence: ✅
- Multi-monitor support: ✅
- Invalid position validation: ✅
- **Window maximize state persistence: ✅**

## Ďalšie kroky

Môžu sa odstrániť dočasné diagnostic/fix scripty (01-15).