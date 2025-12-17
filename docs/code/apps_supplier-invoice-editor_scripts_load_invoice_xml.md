# load_invoice_xml.py

**Path:** `apps\supplier-invoice-editor\scripts\load_invoice_xml.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Script na nacitanie a zobrazenie ISDOC XML faktury
Pouzitie: python scripts/load_invoice_xml.py [path_to_xml]

Ak nie je zadana cesta, hlada XML subory v C:\NEX\

---

## Classes

### ISDOCParser

Parser pre ISDOC XML format

**Methods:**

#### `__init__(self, xml_path)`

#### `load(self)`

Nacita XML subor

#### `get_text(self, element, path, default)`

Ziska text z elementu

#### `parse_header(self)`

Parsuje hlavicku faktury

#### `parse_supplier(self)`

Parsuje udaje dodavatela

#### `parse_customer(self)`

Parsuje udaje odberatela

#### `parse_items(self)`

Parsuje polozky faktury

#### `print_summary(self)`

Vypise prehlad faktury

---

## Functions

### `find_xml_files(base_path)`

Najde XML subory v zadanej ceste

---

### `main()`

Hlavna funkcia

---
