# text_utils.py

**Path:** `apps\supplier-invoice-editor\src\utils\text_utils.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Text utilities for normalization and comparison
Nástroje pre normalizáciu a porovnávanie textu

---

## Functions

### `remove_diacritics(text)`

Remove diacritical marks from text

Converts: "Žeľazničný" -> "Zelaznicny"

Args:
    text: Input text with diacritics

Returns:
    Text without diacritical marks

---

### `normalize_for_search(text)`

Normalize text for search comparison
- Remove diacritics
- Convert to lowercase
- Strip whitespace

Args:
    text: Input text

Returns:
    Normalized text suitable for comparison

Examples:
    >>> normalize_for_search("  ŽLTÝ Čaj  ")
    'zlty caj'
    >>> normalize_for_search("Košice")
    'kosice'

---

### `is_numeric(text)`

Check if text represents a number

Args:
    text: Input text

Returns:
    True if text is numeric

Examples:
    >>> is_numeric("123")
    True
    >>> is_numeric("12.5")
    True
    >>> is_numeric("abc")
    False

---

### `normalize_numeric(text)`

Normalize numeric text for comparison
- Convert comma to dot
- Remove leading zeros
- Strip whitespace

Args:
    text: Numeric text

Returns:
    Normalized numeric string

Examples:
    >>> normalize_numeric("0123")
    '123'
    >>> normalize_numeric("12,5")
    '12.5'

---
