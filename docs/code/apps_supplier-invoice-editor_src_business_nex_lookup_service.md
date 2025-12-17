# nex_lookup_service.py

**Path:** `apps\supplier-invoice-editor\src\business\nex_lookup_service.py`  
**Generated:** 2025-12-17 13:35  
**Type:** Python Source Code

---

## Overview

NEX Genesis Lookup Service
Vyhladavanie produktov v NEX Genesis GSCAT.BTR podla EAN

---

## Classes

### NexLookupService

Service pre vyhladavanie produktov v NEX Genesis

**Methods:**

#### `__init__(self, nex_path)`

Args:
    nex_path: Cesta k NEX Genesis YEARACT adresaru

#### `lookup_by_ean(self, ean)`

Vyhlada produkt podla EAN

Logika:
1. Najprv hlada v GSCAT.BarCode (primarny EAN)
2. Ak nenajde, hlada v BARCODE.BTR (druhotne EAN)

Args:
    ean: EAN kod

Returns:
    Dict s produktovymi udajmi alebo None
    {
        'plu': int,
        'name': str,
        'category': int,
        'price_buy': float,
        'price_sell': float,
        'unit': str,
        'in_nex': bool,
        'source': 'GSCAT' | 'BARCODE'
    }

#### `_find_in_gscat(self, ean)`

Najde produkt v GSCAT.BTR podla BarCode

#### `_find_in_gscat_by_plu(self, plu)`

Najde produkt v GSCAT.BTR podla PLU

#### `_find_in_barcode(self, ean)`

Najde zaznam v BARCODE.BTR

---
