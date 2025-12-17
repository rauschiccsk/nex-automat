# test_invoice_integration.py

**Path:** `apps\supplier-invoice-loader\scripts\test_invoice_integration.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Test Invoice Integration
=========================

Test script pre overenie kompletnej integrácie:
- FastAPI server
- PostgreSQL staging database
- SQLite database
- File storage (PDF/XML)
- n8n workflow

Usage:
    python scripts/test_invoice_integration.py

---

## Functions

### `print_header(text)`

Print formatted header

---

### `print_step(step_num, text)`

Print test step

---

### `print_success(text)`

Print success message

---

### `print_error(text)`

Print error message

---

### `print_warning(text)`

Print warning message

---

### `check_environment()`

Check required environment variables

---

### `check_fastapi_server()`

Check if FastAPI server is running

---

### `check_postgresql_connection()`

Check PostgreSQL connection

---

### `check_test_pdf()`

Check if test PDF exists

---

### `send_test_invoice(pdf_path, api_key)`

Send test invoice to FastAPI

---

### `verify_postgresql_data(invoice_number)`

Verify data in PostgreSQL

---

### `main()`

Main test function

---
