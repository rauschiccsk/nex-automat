# tsi.py

**Path:** `packages\nexdata\nexdata\models\tsi.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

TSI Table Model
Dodacie listy - Items (položky dokladov)

Table: TSIA-001.BTR (actual year, book 001)
Location: C:\NEX\YEARACT\STORES\TSIA-001.BTR
Definition: tsi.bdf
Record Size: ~400 bytes

---

## Classes

### TSIRecord

TSI record structure - Dodacie listy Items

Obsahuje jednotlivé položky dodacieho listu.
Viaceré TSI záznamy patria k jednému TSH záznamu (rovnaký DocNumber).

**Methods:**

#### `from_bytes(cls, data, encoding)`

Deserialize TSI record from bytes

Field Layout (approximate, ~400 bytes):
- DocNumber: 20 bytes (0-19) - string
- LineNumber: 4 bytes (20-23) - longint
- GsCode: 4 bytes (24-27) - longint
- GsName: 80 bytes (28-107) - string
- BarCode: 15 bytes (108-122) - string
- Quantity: 8 bytes (123-130) - double
- Unit: 10 bytes (131-140) - string
- UnitCoef: 8 bytes (141-148) - double
- PriceUnit: 8 bytes (149-156) - double
- PriceUnitVat: 8 bytes (157-164) - double
- VatRate: 8 bytes (165-172) - double
- DiscountPercent: 8 bytes (173-180) - double
- LineBase: 8 bytes (181-188) - double
- LineVat: 8 bytes (189-196) - double
- LineTotal: 8 bytes (197-204) - double
- WarehouseCode: 4 bytes (205-208) - longint
- BatchNumber: 30 bytes (209-238) - string
- SerialNumber: 30 bytes (239-268) - string
- Note: 100 bytes (269-368) - string
- SupplierItemCode: 30 bytes (369-398) - string
- Status: 4 bytes (399-402) - longint
- ModUser: 8 bytes (403-410) - string
- ModDate: 4 bytes (411-414) - longint
- ModTime: 4 bytes (415-418) - longint

Args:
    data: Raw bytes from Btrieve
    encoding: String encoding

Returns:
    TSIRecord instance

#### `_decode_delphi_date(days)`

Convert Delphi date to Python datetime

#### `_decode_delphi_time(milliseconds)`

Convert Delphi time to Python datetime

#### `calculate_line_totals(self)`

Calculate line totals based on quantity, price, discount, and VAT
Updates line_base, line_vat, and line_total

#### `validate(self)`

Validate record

#### `__str__(self)`

---
