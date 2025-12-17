# tsh_repository.py

**Path:** `packages\nexdata\nexdata\repositories\tsh_repository.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Repository for TSH (Dodacie listy - Header)

---

## Classes

### TSHRepository(Unknown)

Repository for accessing TSH records (Dodacie listy - Header)

**Methods:**

#### `__init__(self, btrieve_client, book_id)`

Initialize TSH repository

Args:
    btrieve_client: Btrieve client instance
    book_id: Book identifier (default: "001")

#### `table_name(self)`

Get table file path

#### `from_bytes(self, data)`

Convert bytes to TSHRecord

#### `to_bytes(self, record)`

Convert record to bytes

#### `get_by_document_number(self, doc_number)`

Get TSH record by document number

Args:
    doc_number: Document number (e.g., "240001")

Returns:
    TSHRecord if found, None otherwise

#### `get_recent_documents(self, limit)`

Get recent documents (limited)

Args:
    limit: Maximum number of records to return

Returns:
    List of TSH records

---
