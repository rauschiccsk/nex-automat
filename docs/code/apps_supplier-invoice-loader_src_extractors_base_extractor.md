# base_extractor.py

**Path:** `apps\supplier-invoice-loader\src\extractors\base_extractor.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Base Extractor - Abstract class for all invoice extractors

---

## Classes

### BaseExtractor(ABC)

Abstract base class for invoice extractors
All supplier-specific extractors must inherit from this

**Methods:**

#### `__init__(self)`

#### `extract_from_pdf(self, pdf_path)`

Extract invoice data from PDF file

Args:
    pdf_path: Path to PDF file

Returns:
    InvoiceData object or None if extraction failed

#### `validate_pdf(self, pdf_path)`

Validate that PDF file exists and is readable

---
