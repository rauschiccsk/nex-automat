# gscat.py

**Path:** `apps\supplier-invoice-editor\src\models\gscat.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

GSCAT Table Model
Produktový katalóg (master produktová tabuľka)

Table: GSCAT.BTR
Location: C:\NEX\YEARACT\STORES\GSCAT.BTR
Definition: gscat.bdf
Record Size: 705 bytes

---

## Classes

### GSCATRecord

GSCAT record structure - Produktový katalóg

Master tabuľka pre všetky produkty v systéme.

**Methods:**

#### `from_bytes(cls, data, encoding)`

Deserialize GSCAT record from bytes

Field Layout (approximate, based on 705 bytes record):
- GsCode: 4 bytes (0-3) - longint
- GsName: 80 bytes (4-83) - string
- GsName2: 80 bytes (84-163) - string
- GsShortName: 30 bytes (164-193) - string
- MglstCode: 4 bytes (194-197) - longint
- Unit: 10 bytes (198-207) - string
- UnitCoef: 8 bytes (208-215) - double
- PriceBuy: 8 bytes (216-223) - double
- PriceSell: 8 bytes (224-231) - double
- VatRate: 8 bytes (232-239) - double
- StockMin: 8 bytes (240-247) - double
- StockMax: 8 bytes (248-255) - double
- StockCurrent: 8 bytes (256-263) - double
- Active: 1 byte (264) - boolean
- Discontinued: 1 byte (265) - boolean
- SupplierCode: 4 bytes (266-269) - longint
- SupplierItemCode: 30 bytes (270-299) - string
- Note: 200 bytes (300-499) - string
- Note2: 100 bytes (500-599) - string
- ModUser: 8 bytes (600-607) - string
- ModDate: 4 bytes (608-611) - longint
- ModTime: 4 bytes (612-615) - longint
- CreatedDate: 4 bytes (616-619) - longint
- CreatedUser: 8 bytes (620-627) - string
- Reserved: ~78 bytes (628-705) - padding/reserved

Args:
    data: Raw bytes from Btrieve
    encoding: String encoding (cp852 for Czech/Slovak)

Returns:
    GSCATRecord instance

#### `to_bytes(self, encoding)`

Serialize record to bytes for Btrieve

Args:
    encoding: String encoding

Returns:
    Raw bytes (705 bytes)

#### `_decode_delphi_date(days)`

Convert Delphi date to Python datetime

#### `_encode_delphi_date(dt)`

Convert Python datetime to Delphi date

#### `_decode_delphi_time(milliseconds)`

Convert Delphi time to Python datetime

#### `_encode_delphi_time(dt)`

Convert Python datetime to Delphi time

#### `validate(self)`

Validate record

#### `__str__(self)`

---
