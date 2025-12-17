# invoice_detail_window.py

**Path:** `apps\supplier-invoice-editor\src\ui\invoice_detail_window.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Invoice Detail Window - Display and edit invoice with items

---

## Classes

### InvoiceDetailWindow(BaseWindow)

Dialog window for invoice detail and editing

**Methods:**

#### `__init__(self, invoice_service, invoice_id, parent)`

#### `_load_data(self)`

Load invoice and items data

#### `_setup_ui(self)`

Setup window UI

#### `_create_header_group(self)`

Create invoice header group box

#### `_create_summary_group(self)`

Create summary group box

#### `_create_buttons(self)`

Create button layout

#### `_connect_signals(self)`

Connect widget signals

#### `_update_summary(self)`

Update summary totals

#### `_on_save(self)`

Handle save button click

#### `keyPressEvent(self, event)`

Handle key press events

---
