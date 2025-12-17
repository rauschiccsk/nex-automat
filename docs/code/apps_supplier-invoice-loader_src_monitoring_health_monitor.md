# health_monitor.py

**Path:** `apps\supplier-invoice-loader\src\monitoring\health_monitor.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Health monitoring system for supplier-invoice-loader
Provides system metrics, database status, and application health checks

---

## Classes

### SystemMetrics

System resource metrics

**Methods:**

#### `to_dict(self)`

Convert to dictionary

---

### DatabaseStatus

Database connection status

**Methods:**

#### `to_dict(self)`

Convert to dictionary

---

### InvoiceStats

Invoice processing statistics

**Methods:**

#### `to_dict(self)`

Convert to dictionary

---

### HealthStatus(BaseModel)

Overall health status

**Methods:**

#### `model_dump(self)`

Override model_dump to handle datetime serialization

---

### HealthMonitor

Health monitoring system

**Methods:**

#### `__init__(self, db_pool)`

Initialize health monitor

Args:
    db_pool: Database connection pool

#### `get_uptime_seconds(self)`

Get application uptime in seconds

#### `get_uptime_formatted(self)`

Get formatted uptime string

#### `get_system_metrics(self)`

Get current system metrics

#### `async check_database_status(self)`

Check database connection status

#### `async get_invoice_stats(self)`

Get invoice processing statistics

#### `async get_health_status(self)`

Get overall health status

#### `get_quick_status(self)`

Get quick status without async operations

---
