# tsh.py

**Path:** `packages\nexdata\nexdata\models\tsh.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

TSH Table Model
Dodacie listy - Header (hlavičky dokladov)

Table: TSHA-001.BTR (actual year, book 001)
Location: C:\NEX\YEARACT\STORES\TSHA-001.BTR
Definition: tsh.bdf
Record Size: ~800 bytes

---

## Classes

### TSHRecord

TSH record structure - Dodacie listy Header

Obsahuje hlavičku dodacieho listu (zákazník, dátumy, sumy).
Položky sú v TSI tabuľke (TSI records s rovnakým DocNumber).

**Methods:**

#### `from_bytes(cls, data, encoding)`

Deserialize TSH record from bytes

Field Layout (approximate, ~800 bytes):
- DocNumber: 20 bytes (0-19) - string
- DocType: 4 bytes (20-23) - longint
- DocDate: 4 bytes (24-27) - longint (Delphi date)
- DeliveryDate: 4 bytes (28-31) - longint
- DueDate: 4 bytes (32-35) - longint
- PabCode: 4 bytes (36-39) - longint
- PabName: 100 bytes (40-139) - string
- PabAddress: 150 bytes (140-289) - string
- PabICO: 20 bytes (290-309) - string
- PabDIC: 20 bytes (310-329) - string
- PabICDPH: 30 bytes (330-359) - string
- Currency: 4 bytes (360-363) - string
- ExchangeRate: 8 bytes (364-371) - double
- AmountBase: 8 bytes (372-379) - double
- AmountVat: 8 bytes (380-387) - double
- AmountTotal: 8 bytes (388-395) - double
- Vat20Base: 8 bytes (396-403) - double
- Vat20Amount: 8 bytes (404-411) - double
- Vat10Base: 8 bytes (412-419) - double
- Vat10Amount: 8 bytes (420-427) - double
- Vat0Base: 8 bytes (428-435) - double
- PaymentMethod: 4 bytes (436-439) - longint
- PaymentTerms: 4 bytes (440-443) - longint
- Paid: 1 byte (444) - boolean
- PaidDate: 4 bytes (445-448) - longint
- PaidAmount: 8 bytes (449-456) - double
- InvoiceNumber: 30 bytes (457-486) - string
- OrderNumber: 30 bytes (487-516) - string
- InternalNote: 200 bytes (517-716) - string
- PublicNote: 200 bytes (717-916) - string (may be shorter)

Args:
    data: Raw bytes from Btrieve
    encoding: String encoding

Returns:
    TSHRecord instance

#### `_decode_delphi_date(days)`

Convert Delphi date to Python date

#### `validate(self)`

Validate record

#### `__str__(self)`

---
