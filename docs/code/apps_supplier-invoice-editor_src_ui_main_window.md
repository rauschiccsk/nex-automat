# main_window.py

**Path:** `apps\supplier-invoice-editor\src\ui\main_window.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Main Window - Invoice Editor
Qt5 main application window with menu, toolbar, and invoice list

---

## Classes

### MainWindow(BaseWindow)

Main application window

**Methods:**

#### `__init__(self, config, parent)`

#### `_setup_ui(self)`

Setup main window UI

#### `_create_menu_bar(self)`

Create menu bar

#### `_create_toolbar(self)`

Create toolbar

#### `_create_status_bar(self)`

Create status bar

#### `_connect_signals(self)`

Connect widget signals

#### `_load_invoices(self)`

Load invoices from database

#### `_on_refresh(self)`

Refresh invoice list

#### `_on_search(self)`

Open search dialog

#### `_on_invoice_selected(self, invoice_id)`

Handle invoice selection

#### `_on_invoice_activated(self, invoice_id)`

Handle invoice double-click

#### `_on_invoice_saved(self, invoice_id)`

Handle invoice saved signal

#### `_on_about(self)`

Show about dialog

#### `keyPressEvent(self, event)`

Handle key press events - ESC closes application.

---
