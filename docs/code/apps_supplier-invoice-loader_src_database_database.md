# database.py

**Path:** `apps\supplier-invoice-loader\src\database\database.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Supplier Invoice Loader - Database Operations v2.0
Enhanced with multi-customer support

---

## Functions

### `init_database()`

Vytvorí databázovú štruktúru - v2.0 s multi-customer podporou

---

### `calculate_file_hash(file_content)`

Vypočíta SHA-256 hash súboru

---

### `is_duplicate(file_hash, message_id, customer_name)`

Skontroluje či faktúra už existuje v databáze
V2.0: Kontroluje duplicity v rámci zákazníka

Args:
    file_hash: SHA-256 hash PDF súboru
    message_id: Gmail message ID (optional)
    customer_name: Meno zákazníka (optional, default from config)

Returns:
    True ak faktúra už existuje

---

### `insert_invoice(file_hash, pdf_path, original_filename, message_id, gmail_id, sender, subject, received_date, customer_name, nex_genesis_id)`

Vloží novú faktúru do databázy
V2.0: Pridaná podpora pre customer_name a nex_genesis_id

Returns:
    ID novej faktúry

---

### `update_nex_genesis_status(invoice_id, nex_genesis_id, status, error_message)`

Update NEX Genesis sync status

Args:
    invoice_id: Invoice ID in local database
    nex_genesis_id: ID from NEX Genesis system
    status: Sync status ('synced', 'error', 'pending')
    error_message: Error message if sync failed

Returns:
    True if updated successfully

---

### `get_invoice_by_id(invoice_id)`

Vráti faktúru podľa ID

---

### `get_invoice_by_nex_id(nex_genesis_id)`

Vráti faktúru podľa NEX Genesis ID

Args:
    nex_genesis_id: NEX Genesis ID

Returns:
    Invoice dict or None

---

### `get_all_invoices(limit, customer_name)`

Vráti zoznam faktúr
V2.0: Možnosť filtrovať podľa zákazníka

Args:
    limit: Max počet faktúr
    customer_name: Filter podľa zákazníka (None = všetci)

Returns:
    List of invoice dicts

---

### `get_pending_nex_sync(customer_name, limit)`

Get invoices pending NEX Genesis sync

Args:
    customer_name: Filter by customer (None = all)
    limit: Max number of results

Returns:
    List of invoices pending sync

---

### `get_stats(customer_name)`

Vráti štatistiky o faktúrach
V2.0: Možnosť získať štatistiky pre konkrétneho zákazníka

Args:
    customer_name: Filter podľa zákazníka (None = všetci)

Returns:
    Statistics dict

---

### `get_customer_list()`

Get list of all customers in database

Returns:
    List of unique customer names

---

### `save_invoice(customer_name, invoice_number, invoice_date, total_amount, file_path, file_hash, status, message_id, gmail_id)`

Save invoice to database (simplified wrapper for insert_invoice)

Args:
    customer_name: Customer name
    invoice_number: Invoice number
    invoice_date: Invoice date
    total_amount: Total amount
    file_path: Path to PDF file
    file_hash: File hash
    status: Invoice status
    message_id: Email message ID
    gmail_id: Gmail ID

Returns:
    Invoice ID

---

### `get_all_invoices_legacy(limit)`

Legacy function for backward compatibility

---

### `get_stats_legacy()`

Legacy function for backward compatibility

---
