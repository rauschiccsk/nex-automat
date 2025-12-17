# test_barcode_lookup.py

**Path:** `apps\supplier-invoice-editor\scripts\test_barcode_lookup.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

Script na test Btrieve lookup podla EAN kodu
Overi polozky faktury v NEX Genesis katalogu (BARCODE.BTR + GSCAT.BTR)

Pouzitie: python scripts/test_barcode_lookup.py [ean_code1] [ean_code2] ...
          python scripts/test_barcode_lookup.py --from-xml [xml_path]

---

## Classes

### BarcodeLookupService

Service pre vyhladavanie produktov podla EAN kodu v NEX Genesis

**Methods:**

#### `__init__(self, nex_path)`

Inicializacia sluzby

Args:
    nex_path: Cesta k NEX Genesis YEARACT adresaru

#### `lookup_by_ean(self, ean)`

Vyhlada produkt podla EAN kodu

Logika:
1. Najprv hlada EAN v GSCAT.BarCode (primarny EAN)
2. Ak nenajde, hlada v BARCODE.BTR (druhotne EAN)

Args:
    ean: EAN kod (ciarovy kod)

Returns:
    Tuple (BarcodeRecord|None, GSCATRecord) ak najdene, inak None

#### `_find_barcode(self, ean)`

Najde BARCODE zaznam podla EAN

#### `_find_product_by_barcode(self, ean)`

Najde GSCAT zaznam podla BarCode (primarny EAN v GSCAT)

#### `_find_product_by_plu(self, gs_code)`

Najde GSCAT zaznam podla PLU (gs_code)

#### `check_invoice_items(self, items)`

Skontroluje vsetky polozky faktury v NEX Genesis

Args:
    items: List slovnikov s klucmi: name, ean, quantity, unit_price

Returns:
    Dict so statistikami a detailmi

---

## Functions

### `load_invoice_xml(xml_path)`

Nacita polozky z ISDOC XML faktury

---

### `main()`

Hlavna funkcia

---
