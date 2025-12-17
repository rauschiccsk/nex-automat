# tsi_repository.py

**Path:** `packages\nexdata\nexdata\repositories\tsi_repository.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Repository for TSI (Dodacie listy - Items)

---

## Classes

### TSIRepository(Unknown)

Repository for accessing TSI records (Dodacie listy - Items)

**Methods:**

#### `__init__(self, btrieve_client, book_id)`

Initialize TSI repository

Args:
    btrieve_client: Btrieve client instance
    book_id: Book identifier (default: "001")

#### `table_name(self)`

Get table file path

#### `from_bytes(self, data)`

Convert bytes to TSIRecord

#### `to_bytes(self, record)`

Convert record to bytes

#### `get_by_document(self, doc_number)`

Get all items for specific document

Args:
    doc_number: Document number (e.g., "240001")

Returns:
    List of TSI records for the document

#### `get_by_document_and_line(self, doc_number, line_number)`

Get specific item by document and line number

Args:
    doc_number: Document number
    line_number: Line number within document

Returns:
    TSIRecord if found, None otherwise

---
