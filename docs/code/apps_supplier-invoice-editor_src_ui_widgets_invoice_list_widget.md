# invoice_list_widget.py

**Path:** `apps\supplier-invoice-editor\src\ui\widgets\invoice_list_widget.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Invoice List Widget - QTableView for displaying pending invoices
Refactored to use BaseGrid from nex-shared

---

## Classes

### InvoiceListModel(QAbstractTableModel)

Table model for invoice list

**Methods:**

#### `__init__(self, parent)`

#### `set_invoices(self, invoices)`

Set invoice data

#### `update_invoices(self, invoices)`

Alias for set_invoices() - for compatibility with main_window.py

#### `rowCount(self, parent)`

Return number of rows

#### `columnCount(self, parent)`

Return number of columns

#### `data(self, index, role)`

Return cell data

#### `headerData(self, section, orientation, role)`

Return header data

#### `get_invoice(self, row)`

Get invoice at row

#### `get_invoice_id(self, row)`

Get invoice ID at row

#### `sort(self, column, order)`

Sort data by column

---

### InvoiceListWidget(BaseGrid)

Widget for displaying invoice list - uses BaseGrid

**Methods:**

#### `__init__(self, invoice_service, parent)`

#### `_connect_signals(self)`

Connect signals

#### `set_invoices(self, invoices)`

Set invoice data

#### `update_invoices(self, invoices)`

Alias for set_invoices() - for compatibility with main_window.py

#### `_on_selection_changed(self, current, previous)`

Handle selection change

#### `_on_double_clicked(self, index)`

Handle double-click

#### `get_selected_invoice(self)`

Get currently selected invoice

#### `get_selected_invoice_id(self)`

Get currently selected invoice ID

---
