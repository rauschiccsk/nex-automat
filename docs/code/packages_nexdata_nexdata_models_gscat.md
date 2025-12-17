# gscat.py

**Path:** `packages\nexdata\nexdata\models\gscat.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

GSCAT.BTR Model - Correct Structure (705 bytes)
===============================================

Correct model based on actual Btrieve record analysis.

CRITICAL: BarCode field starts at offset 60, not 64!

File: GSCAT.BTR
Location: C:\NEX\YEARACT\STORES\GSCAT.BTR
Record Size: 705 bytes
Encoding: cp852

---

## Classes

### GSCATRecord

GSCAT record - simplified model with verified fields only

**Methods:**

#### `__post_init__(self)`

Clean up string fields

#### `from_bytes(cls, data, encoding)`

Deserialize GSCATRecord from Btrieve bytes

Args:
    data: Raw bytes from Btrieve record (705 bytes)
    encoding: Character encoding (default: cp852)

Returns:
    GSCATRecord instance

#### `barcode(self)`

Alias for BarCode field (for backward compatibility)

#### `gs_code(self)`

Alias for GsCode field (for backward compatibility)

#### `gs_name(self)`

Alias for GsName field (for backward compatibility)

#### `mg_code(self)`

Alias for MgCode field (for backward compatibility)

---
