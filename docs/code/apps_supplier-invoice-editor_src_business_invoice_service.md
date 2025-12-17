# invoice_service.py

**Path:** `apps\supplier-invoice-editor\src\business\invoice_service.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Invoice Service - Business logic for invoice operations
Adapted for production database schema from supplier_invoice_loader

---

## Classes

### InvoiceService

Service for invoice operations

**Methods:**

#### `__init__(self, config)`

#### `_init_database(self)`

Initialize database connection

#### `get_pending_invoices(self)`

Get list of pending invoices

Returns:
    List of invoice dictionaries

#### `_get_invoices_from_database(self)`

Get invoices from PostgreSQL

#### `_get_stub_invoices(self)`

Get stub invoice data for testing

#### `get_invoice_by_id(self, invoice_id)`

Get single invoice by ID

Args:
    invoice_id: Invoice ID

Returns:
    Invoice dictionary or None

#### `get_invoice_items(self, invoice_id)`

Get invoice line items - ADAPTED FOR PRODUCTION SCHEMA

Args:
    invoice_id: Invoice ID

Returns:
    List of item dictionaries

#### `_get_items_from_database(self, invoice_id)`

Get items from PostgreSQL - ADAPTED FOR PRODUCTION SCHEMA

Maps production columns to UI expected columns:
- edited_name OR original_name → item_name
- edited_mglst_code → category_code
- original_unit → unit
- original_quantity → quantity
- edited_price_buy OR original_price_per_unit → unit_price
- edited_discount_percent → rabat_percent
- final_price_buy → price_after_rabat
- (final_price_buy * original_quantity) → total_price
- original_ean OR nex_gs_code → plu_code

#### `_get_stub_items(self, invoice_id)`

Get stub item data for testing

#### `save_invoice(self, invoice_id, items)`

Save invoice items - ADAPTED FOR PRODUCTION SCHEMA

Args:
    invoice_id: Invoice ID
    items: List of item dictionaries

Returns:
    True if saved successfully

#### `_save_to_database(self, invoice_id, items)`

Save items to PostgreSQL - ADAPTED FOR PRODUCTION SCHEMA

Maps UI columns back to production columns:
- item_name → edited_name
- category_code → edited_mglst_code
- unit_price → edited_price_buy
- rabat_percent → edited_discount_percent
- price_after_rabat → final_price_buy

#### `calculate_item_price(self, unit_price, rabat_percent, quantity)`

Calculate item prices

Args:
    unit_price: Unit price
    rabat_percent: Rabat percentage (0-100)
    quantity: Quantity

Returns:
    Tuple (price_after_rabat, total_price)

---
