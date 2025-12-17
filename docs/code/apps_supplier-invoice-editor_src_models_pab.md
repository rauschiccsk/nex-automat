# pab.py

**Path:** `apps\supplier-invoice-editor\src\models\pab.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

PAB Table Model
Katalóg obchodných partnerov (dodávatelia, odberatelia)

Table: PAB00000.BTR
Location: C:\NEX\YEARACT\DIALS\PAB00000.BTR
Definition: pab.bdf
Record Size: 1269 bytes

---

## Classes

### PABRecord

PAB record structure - Obchodní partneri

Evidencia všetkých obchodných partnerov (dodávatelia, odberatelia, ostatní).

**Methods:**

#### `from_bytes(cls, data, encoding)`

Deserialize PAB record from bytes

Field Layout (approximate, based on 1269 bytes record):
- PabCode: 4 bytes (0-3) - longint
- Name1: 100 bytes (4-103) - string
- Name2: 100 bytes (104-203) - string
- ShortName: 40 bytes (204-243) - string
- Street: 80 bytes (244-323) - string
- City: 50 bytes (324-373) - string
- ZipCode: 10 bytes (374-383) - string
- Country: 50 bytes (384-433) - string
- Phone: 30 bytes (434-463) - string
- Fax: 30 bytes (464-493) - string
- Email: 60 bytes (494-553) - string
- Web: 60 bytes (554-613) - string
- ContactPerson: 50 bytes (614-663) - string
- ICO: 20 bytes (664-683) - string
- DIC: 20 bytes (684-703) - string
- ICDPH: 30 bytes (704-733) - string
- BankAccount: 30 bytes (734-763) - string
- BankCode: 10 bytes (764-773) - string
- BankName: 60 bytes (774-833) - string
- IBAN: 40 bytes (834-873) - string
- SWIFT: 20 bytes (874-893) - string
- PartnerType: 4 bytes (894-897) - longint
- PaymentTerms: 4 bytes (898-901) - longint
- CreditLimit: 8 bytes (902-909) - double
- DiscountPercent: 8 bytes (910-917) - double
- Active: 1 byte (918) - boolean
- VatPayer: 1 byte (919) - boolean
- Note: 200 bytes (920-1119) - string
- Note2: 100 bytes (1120-1219) - string
- InternalNote: 100 bytes (1220-1319) - string (may overflow)

Args:
    data: Raw bytes from Btrieve
    encoding: String encoding (cp852 for Czech/Slovak)

Returns:
    PABRecord instance

#### `validate(self)`

Validate record

#### `get_full_name(self)`

Get full company name (Name1 + Name2)

#### `get_full_address(self)`

Get full address as single line

#### `is_supplier(self)`

Check if partner is supplier

#### `is_customer(self)`

Check if partner is customer

#### `__str__(self)`

---
