# isdoc_service.py

**Path:** `apps\supplier-invoice-loader\src\business\isdoc_service.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

L&Š Invoice Loader - ISDOC 6.0.1 XML Generator
Generates ISDOC XML from extracted invoice data

---

## Classes

### ISDOCGenerator

Generator pre ISDOC 6.0.1 XML faktúry

**Methods:**

#### `__init__(self)`

#### `generate_from_invoice_data(self, data, output_path)`

Hlavná metóda - vytvorí ISDOC XML z InvoiceData

Args:
    data: InvoiceData objekt z ls_extractor.py
    output_path: Cesta kam uložiť XML (optional)

Returns:
    XML ako string

#### `_add_supplier_party(self, root, data)`

Pridá dodávateľa (L&Š)

#### `_add_customer_party(self, root, data)`

Pridá odberateľa

#### `_add_delivery(self, root, data)`

Pridá informácie o dodaní

#### `_add_payment_means(self, root, data)`

Pridá platobné údaje

#### `_add_tax_total(self, root, data)`

Pridá DPH súhrn

#### `_add_legal_monetary_total(self, root, data)`

Pridá celkové sumy

#### `_add_invoice_lines(self, root, data)`

Pridá položky faktúry

#### `_format_date(self, date_str)`

Konvertuje dátum na ISDOC formát YYYY-MM-DD

Args:
    date_str: Dátum v rôznych formátoch (napr. "16.09.2025")

Returns:
    Dátum v ISO formáte

#### `_format_amount(self, amount)`

Konvertuje Decimal na string vo formáte ISDOC

Args:
    amount: Decimal číslo

Returns:
    String s 2 desatinnými miestami

#### `_prettify_xml(self, elem)`

Naformátuje XML pre lepšiu čitateľnosť

Args:
    elem: Root element

Returns:
    Formatted XML string

---

## Functions

### `generate_isdoc_xml(invoice_data, output_path)`

Wrapper funkcia pre generovanie ISDOC XML

Args:
    invoice_data: InvoiceData objekt z ls_extractor.py
    output_path: Cesta kam uložiť XML (optional)

Returns:
    XML ako string

Usage:
    from src.business.isdoc_service import generate_isdoc_xml
    xml = generate_isdoc_xml(invoice_data, "/path/to/output.xml")

---
