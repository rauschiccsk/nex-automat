# btrieve_client.py

**Path:** `packages\nexdata\nexdata\btrieve\btrieve_client.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Python wrapper pre Pervasive Btrieve API (32-bit)
FIXED: Correct BTRCALL signature based on Delphi btrapi32.pas

---

## Classes

### BtrieveClient

Python wrapper pre Pervasive Btrieve API (32-bit)
Používa w3btrv7.dll alebo wbtrv32.dll

**Methods:**

#### `__init__(self, config_or_path)`

Inicializácia Btrieve klienta

Args:
    config_or_path: Dict s config dátami ALEBO string s cestou ku config súboru (YAML)

#### `_resolve_table_path(self, table_name_or_path)`

Resolve table name to filesystem path using config

Args:
    table_name_or_path: Either table name (e.g. 'gscat', 'tsh-001') or direct path

Returns:
    Filesystem path to .BTR file

#### `_load_dll(self)`

Načítaj Btrieve DLL a nastav BTRCALL funkciu - NO EMOJIS

#### `open_file(self, filename, owner_name, mode)`

Otvor Btrieve súbor - FIXED with owner name support

CRITICAL: Owner name must be in data_buffer for files with owner security!

Args:
    filename: Cesta k .dat/.BTR súboru
    owner_name: Owner name (required for secured files!)
    mode: Open mode
          0 = Normal
         -1 = Accelerated
         -2 = Read-only (DEFAULT - safest)
         -3 = Exclusive

Returns:
    Tuple[status_code, position_block]

#### `close_file(self, pos_block)`

Zavri Btrieve súbor

Args:
    pos_block: Position block z open_file()

Returns:
    status_code

#### `get_first(self, pos_block, key_num)`

Načítaj prvý záznam

Args:
    pos_block: Position block
    key_num: Index number (default: 0)

Returns:
    Tuple[status_code, data]

#### `get_next(self, pos_block)`

Načítaj ďalší záznam

Args:
    pos_block: Position block

Returns:
    Tuple[status_code, data]

#### `get_status_message(self, status_code)`

Konvertuj status code na human-readable správu

Args:
    status_code: Btrieve status code

Returns:
    Status message

---

## Functions

### `open_btrieve_file(filename, config_path)`

Helper funkcia na otvorenie Btrieve súboru

Args:
    filename: Cesta k .BTR súboru
    config_path: Cesta ku config súboru

Returns:
    Tuple[client, position_block]

---
