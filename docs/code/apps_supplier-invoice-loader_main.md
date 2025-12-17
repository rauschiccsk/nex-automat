# main.py

**Path:** `apps\supplier-invoice-loader\main.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Supplier Invoice Loader - Entry Point
======================================

Multi-customer SaaS for automated invoice processing.

---

## Functions

### `async track_requests(request, call_next)`

Middleware to track API requests in metrics

---

### `async verify_api_key(x_api_key)`

Verify API key from X-API-Key header

Args:
    x_api_key: API key from header

Raises:
    HTTPException: If API key is invalid or missing

---

### `async root()`

Root endpoint - service information

---

### `async health()`

Health check endpoint - for monitoring systems

---

### `async metrics()`

Metrics endpoint - basic metrics in JSON format

---

### `async metrics_prometheus()`

Metrics endpoint - Prometheus format

---

### `async stats()`

Statistics endpoint - database statistics

---

### `async status(api_key)`

Detailed status endpoint - requires authentication

Returns system status, components health, and statistics

---

### `async list_invoices(limit, api_key)`

List invoices - requires authentication

Args:
    limit: Maximum number of invoices to return

Returns:
    List of invoices with metadata

---

### `async enrich_invoice_items(invoice_id)`

Automatic enrichment of invoice items with NEX Genesis data

Args:
    invoice_id: ID of invoice to enrich

---

### `async process_invoice(request, api_key)`

Process invoice - requires authentication

Main endpoint for invoice processing from n8n workflow

Workflow:
1. Decode and save PDF
2. Extract invoice data from PDF
3. Save to SQLite database
4. Generate ISDOC XML
5. Save XML to disk
6. [Optional] Save to PostgreSQL staging database for invoice-editor

Args:
    request: Invoice data including PDF file

Returns:
    Processing result with status and extracted data

---

### `async admin_test_email(api_key)`

Admin endpoint - send test email

Sends a test email to verify SMTP configuration

---

### `async admin_send_summary(api_key)`

Admin endpoint - send daily summary

Sends daily summary email with processing statistics

---

### `async startup_event()`

Initialize application on startup

---

### `async shutdown_event()`

Cleanup on shutdown

---
