# generic_extractor.py

**Path:** `apps\supplier-invoice-loader\src\extractors\generic_extractor.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Generic Extractor - For standard invoice formats

---

## Classes

### GenericExtractor(BaseExtractor)

Generic extractor for standard invoice formats
Works with most common accounting software outputs

**Methods:**

#### `__init__(self)`

#### `extract_from_pdf(self, pdf_path)`

Extract invoice data from standard PDF format

TODO: Implement generic extraction logic
- Detect common patterns (Invoice Number:, Date:, Total:)
- Extract using flexible regex patterns
- Handle multiple date formats
- Parse simple item tables

Args:
    pdf_path: Path to PDF file

Returns:
    InvoiceData object or None

---

## Functions

### `extract_invoice_data(pdf_path)`

Wrapper function for generic extraction

---
