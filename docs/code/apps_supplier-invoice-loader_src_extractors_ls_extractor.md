# ls_extractor.py

**Path:** `apps\supplier-invoice-loader\src\extractors\ls_extractor.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

L&Š Invoice Loader - PDF Data Extraction
Extracts invoice data from L&Š PDF invoices

---

## Classes

### InvoiceItem

Jedna položka na faktúre

---

### InvoiceData

Kompletné dáta z faktúry

---

### LSInvoiceExtractor

Extraktor pre L&Š faktúry

**Methods:**

#### `__init__(self)`

#### `_init_patterns(self)`

Inicializácia regex patterns pre L&Š faktúry

#### `extract_from_pdf(self, pdf_path)`

Hlavná metóda - extrahuje dáta z PDF

Args:
    pdf_path: Cesta k PDF súboru

Returns:
    InvoiceData alebo None ak extraction zlyhal

#### `_extract_text_from_pdf(self, pdf_path, pdfplumber)`

Extrahuje text z PDF pomocou pdfplumber

#### `_extract_header(self, text)`

Extrahuje hlavičku faktúry

#### `_extract_items(self, text)`

Extrahuje položky z tabuľky faktúry

L&Š formát:
č. Názov                Množstvo MJ  Zľava  Cena/MJ bez DPH  Cena/MJ s DPH  Spolu s DPH
   Kód tovaru  EAN      Sadzba DPH   Pôv.cena...

1  Akcia KO             3 KS                0.010            0.012          0.037
   293495               23%                 0.010            0.012

#### `_parse_decimal(self, value)`

Parsuje string na Decimal

---

## Functions

### `extract_invoice_data(pdf_path)`

Wrapper funkcia pre extrahovanie dát

Usage:
    from extraction import extract_invoice_data
    data = extract_invoice_data("/path/to/invoice.pdf")
    if data:
        print(f"Invoice: {data.invoice_number}")
        print(f"Items: {len(data.items)}")

---
