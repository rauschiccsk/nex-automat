# monitoring.py

**Path:** `apps\supplier-invoice-loader\src\utils\monitoring.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Supplier Invoice Loader - Monitoring & Metrics
Tracks application health, uptime, and processing statistics

---

## Classes

### Metrics

Application metrics tracker

**Methods:**

#### `__init__(self)`

#### `get_uptime(self)`

Get application uptime in seconds

#### `get_system_metrics(self)`

Get system metrics (CPU, memory) if psutil available

#### `increment_request(self, success)`

Increment request counter

#### `increment_invoice(self, success)`

Increment invoice processing counter

#### `get_stats(self)`

Get all statistics

#### `reset(self)`

Reset all counters (for testing)

---

## Functions

### `get_metrics()`

Get global metrics instance

---

### `reset_metrics()`

Reset global metrics (for testing)

---

### `check_storage_health()`

Check storage directories health

Returns:
    dict with storage health status

---
