# invoice_items_grid.py

**Path:** `apps\supplier-invoice-editor\src\ui\widgets\invoice_items_grid.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Invoice Items Grid - Editable grid for invoice line items
Refactored to use BaseGrid from nex-shared

---

## Classes

### InvoiceItemsModel(QAbstractTableModel)

Editable table model for invoice items

**Methods:**

#### `__init__(self, parent)`

#### `set_items(self, items)`

Set item data

#### `get_items(self)`

Get current items

#### `rowCount(self, parent)`

Return number of rows

#### `columnCount(self, parent)`

Return number of columns

#### `data(self, index, role)`

Return cell data

#### `setData(self, index, value, role)`

Set cell data

#### `_calculate_item_prices(self, item)`

Calculate price_after_rabat and total_price

#### `flags(self, index)`

Return item flags

#### `headerData(self, section, orientation, role)`

Return header data

#### `sort(self, column, order)`

Sort data by column

---

### InvoiceItemsGrid(BaseGrid)

Widget for editable invoice items grid - uses BaseGrid

**Methods:**

#### `__init__(self, invoice_service, parent)`

#### `_connect_signals(self)`

Connect signals

#### `set_items(self, items)`

Set item data

#### `get_items(self)`

Get current items

---
