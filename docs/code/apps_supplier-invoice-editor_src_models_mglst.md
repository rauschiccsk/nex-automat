# mglst.py

**Path:** `apps\supplier-invoice-editor\src\models\mglst.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

MGLST Table Model
Tovarové skupiny (hierarchická kategorizácia produktov)

Table: MGLST.BTR
Location: C:\NEX\YEARACT\STORES\MGLST.BTR
Definition: mglst.bdf
Record Size: ~200 bytes

---

## Classes

### MGLSTRecord

MGLST record structure - Tovarové skupiny

Hierarchická štruktúra kategórií produktov.
Podporuje multi-level kategorizáciu (napr. Elektronika > Počítače > Notebooky).

**Methods:**

#### `from_bytes(cls, data, encoding)`

Deserialize MGLST record from bytes

Field Layout (approximate, ~200 bytes):
- MglstCode: 4 bytes (0-3) - longint
- MglstName: 80 bytes (4-83) - string
- ShortName: 30 bytes (84-113) - string
- ParentCode: 4 bytes (114-117) - longint
- Level: 4 bytes (118-121) - longint
- SortOrder: 4 bytes (122-125) - longint
- ColorCode: 10 bytes (126-135) - string
- DefaultVatRate: 8 bytes (136-143) - double
- DefaultUnit: 10 bytes (144-153) - string
- Active: 1 byte (154) - boolean
- ShowInCatalog: 1 byte (155) - boolean
- Note: 100 bytes (156-255) - string
- Description: 200 bytes (256-455) - string (may be shorter)
- ModUser: 8 bytes - string
- ModDate: 4 bytes - longint
- ModTime: 4 bytes - longint

Args:
    data: Raw bytes from Btrieve
    encoding: String encoding (cp852 for Czech/Slovak)

Returns:
    MGLSTRecord instance

#### `_decode_delphi_date(days)`

Convert Delphi date to Python datetime

#### `_decode_delphi_time(milliseconds)`

Convert Delphi time to Python datetime

#### `validate(self)`

Validate record

#### `is_root(self)`

Check if this is a root-level category

#### `is_child_of(self, parent_code)`

Check if this category is a child of specified parent

#### `get_path(self, all_categories)`

Get full path from root to this category

Args:
    all_categories: List of all categories

Returns:
    List of categories from root to this one

#### `get_full_path_name(self, all_categories, separator)`

Get full category path as string (e.g., "Elektronika > Počítače > Notebooky")

Args:
    all_categories: List of all categories
    separator: Path separator

Returns:
    Full path string

#### `__str__(self)`

---
