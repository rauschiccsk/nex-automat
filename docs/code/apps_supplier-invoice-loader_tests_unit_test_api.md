# test_api.py

**Path:** `apps\supplier-invoice-loader\tests\unit\test_api.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Tests for FastAPI endpoints

---

## Functions

### `client()`

Create test client

---

### `api_key()`

Get API key from config

---

### `test_root_endpoint(client)`

Test root endpoint returns service info

---

### `test_health_endpoint_no_auth(client)`

Test health endpoint works without authentication

---

### `test_status_endpoint_requires_auth(client)`

Test status endpoint requires authentication

---

### `test_status_endpoint_with_auth(client, api_key)`

Test status endpoint with valid API key

---

### `test_metrics_endpoint_no_auth(client)`

Test metrics endpoint works without authentication

---

### `test_metrics_prometheus_endpoint(client)`

Test Prometheus metrics endpoint

---

### `test_stats_endpoint_no_auth(client)`

Test stats endpoint works without authentication

---

### `test_invoices_endpoint_requires_auth(client)`

Test invoices list endpoint requires authentication

---

### `test_invoices_endpoint_with_auth(client, api_key)`

Test invoices list endpoint with authentication

---

### `test_invoice_endpoint_requires_auth(client)`

Test invoice processing endpoint requires authentication

---

### `test_invoice_endpoint_with_invalid_data(client, api_key)`

Test invoice endpoint with invalid data

---

### `test_invoice_endpoint_with_valid_structure(client, api_key)`

Test invoice endpoint with valid request structure

---

### `test_admin_test_email_endpoint(client, api_key)`

Test admin test email endpoint

---

### `test_admin_send_summary_endpoint(client, api_key)`

Test admin send summary endpoint

---

### `test_invalid_api_key_returns_401(client)`

Test that invalid API key returns 401

---

### `test_docs_endpoints_exist(client)`

Test that API documentation endpoints exist

---

### `test_openapi_json_exists(client)`

Test that OpenAPI JSON schema exists

---

### `test_cors_headers_if_enabled(client)`

Test CORS headers if CORS is enabled

---

### `test_full_invoice_processing_flow(client, api_key)`

Integration test: Full invoice processing

---

### `test_api_metrics_increment(client)`

Test that API requests increment metrics

---
