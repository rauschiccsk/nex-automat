# text_utils.py

**Path:** `packages\nex-shared\utils\text_utils.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

NEX Shared - Text Utilities
Utility functions for text processing and cleaning.

---

## Functions

### `clean_string(value)`

Odstráni null bytes a control characters z reťazcov.
NEX Genesis Btrieve polia obsahujú \x00 padding.

Args:
    value: String alebo iná hodnota na vyčistenie

Returns:
    Vyčistený string alebo None/original value

---
