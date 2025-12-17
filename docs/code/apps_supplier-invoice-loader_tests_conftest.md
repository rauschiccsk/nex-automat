# conftest.py

**Path:** `apps\supplier-invoice-loader\tests\conftest.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Pytest configuration and shared fixtures

---

## Functions

### `pytest_addoption(parser)`

Add custom command line options

---

### `pytest_configure(config)`

Configure pytest

---

### `test_data_dir()`

Path to test data directory

---

### `sample_invoice_data()`

Sample invoice data for testing

---

### `mock_config(monkeypatch)`

Mock configuration for testing

---

### `temp_database(tmp_path)`

Create temporary database for testing

---

### `sample_pdf_content()`

Sample PDF content (minimal valid PDF)

---

### `mock_smtp_server(monkeypatch)`

Mock SMTP server for email testing

---

### `reset_metrics()`

Reset metrics before each test

---

### `api_client()`

FastAPI test client

---

### `pytest_report_header(config)`

Add custom header to pytest output

---
