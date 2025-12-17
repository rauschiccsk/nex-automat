# barcode.py

**Path:** `apps\supplier-invoice-editor\src\models\barcode.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

BARCODE Table Model
Druhotné identifikačné kódy (čiarové kódy) produktov

Table: BARCODE.BTR
Location: C:\NEX\YEARACT\STORES\BARCODE.BTR
Definition: barcode.bdf
Record Size: ~50 bytes

---

## Classes

### BarcodeRecord

BARCODE record structure

Jeden produkt môže mať viacero čiarových kódov.
Composite index GsBc zabezpečuje unique constraint (GsCode + BarCode).

**Methods:**

#### `from_bytes(cls, data, encoding)`

Deserialize Btrieve record from bytes

Field Layout (approximate):
- GsCode: 4 bytes (0-3) - longint
- BarCode: 15 bytes (4-18) - string
- ModUser: 8 bytes (19-26) - string
- ModDate: 4 bytes (27-30) - longint (days since 1899-12-30)
- ModTime: 4 bytes (31-34) - longint (milliseconds since midnight)

Args:
    data: Raw bytes from Btrieve
    encoding: String encoding (cp852 for Czech/Slovak)

Returns:
    BarcodeRecord instance

#### `to_bytes(self, encoding)`

Serialize record to bytes for Btrieve

Args:
    encoding: String encoding (cp852 for Czech/Slovak)

Returns:
    Raw bytes for Btrieve

#### `_decode_delphi_date(days)`

Convert Delphi TDateTime date part to Python datetime

Delphi date: days since 1899-12-30

#### `_encode_delphi_date(dt)`

Convert Python datetime to Delphi date (days since 1899-12-30)

#### `_decode_delphi_time(milliseconds)`

Convert Delphi TDateTime time part to Python datetime

Delphi time: milliseconds since midnight

#### `_encode_delphi_time(dt)`

Convert Python datetime to Delphi time (milliseconds since midnight)

#### `validate(self)`

Validate record fields

Returns:
    List of validation errors (empty if valid)

#### `__str__(self)`

String representation

#### `__repr__(self)`

Debug representation

---
