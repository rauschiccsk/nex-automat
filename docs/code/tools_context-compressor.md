# context-compressor.py

**Path:** `tools\context-compressor.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Context Compressor - nex-automat projekt
Komprimuje históriu chatu pomocou Claude API
POZNÁMKA: Vyžaduje ANTHROPIC_API_KEY v config.py

---

## Classes

### ContextCompressor

**Methods:**

#### `__init__(self, api_key)`

#### `compress_chat_history(self, history_file)`

Skomprimuj históriu chatu do kompaktného zhrnutia

Args:
    history_file: Cesta k súboru s históriou

Returns:
    Komprimovaný text

#### `compress_session_notes(self)`

Skomprimuj aktuálne session notes

#### `compress_init_prompt(self)`

Skomprimuj init prompt

#### `batch_compress(self, directory)`

Skomprimuj všetky .md súbory v adresári

---

## Functions

### `main()`

Hlavná funkcia

---
