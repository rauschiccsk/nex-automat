# Products Reference - Produktový katalóg

**Category:** Database / Catalogs  
**Status:** 🟢 Complete  
**Created:** 2025-12-11  
**Updated:** 2025-12-15  
**Related:** [CATALOGS_REFERENCE.md](CATALOGS_REFERENCE.md), [PARTNERS_REFERENCE.md](PARTNERS_REFERENCE.md)

---


## PREHĽAD

Produktový katalóg s tovarovými skupinami, identifikátormi, rozšírenými údajmi a cenovými politikami.

**Zdokumentované:** 5 dokumentov (7 tabuliek)  
**Status:** ✅ Kompletné

---

## ŠTRUKTÚRA DOKUMENTÁCIE

```
products/
├── INDEX.md                                 ✅ (v1.0)
└── tables/
    ├── GSCAT-product_catalog.md             ✅ Hlavný katalóg (6 tabuliek)
    ├── MGLST-product_categories.md          ✅ Tovarové skupiny
    ├── FGLST-product_categories.md          ✅ Finančné skupiny
    ├── SGLST-product_categories.md          ✅ Špecifické skupiny
    └── BARCODE-product_catalog_identifiers.md ✅ Čiarové kódy a identifikátory
```

---

## HLAVNÝ KATALÓG PRODUKTOV

### GSCAT-product_catalog.md (6 tabuliek)

**Btrieve súbor:** GSCAT.BTR

**PostgreSQL tabuľky:**
1. `product_catalog` - hlavné údaje produktu
2. `product_catalog_identifiers` - EAN, SKU, výrobné čísla
3. `product_catalog_extensions` - rozšírené údaje (rozmery, hmotnosť)
4. `product_catalog_texts` - textové polia (výrobca, krajina pôvodu)
5. `product_catalog_categories` - mapovanie tovarových skupín
6. `product_catalog_prices` - cenové údaje (nákup, predaj)

**Účel:** Komplexný katalóg produktov s rozšírenými údajmi.

---

## DETAILNÁ DOKUMENTÁCIA

### 1. Hlavný katalóg - GSCAT-product_catalog.md

**Btrieve:** GSCAT.BTR  
**Tabuľky:** 6 tabuliek

**Kľúčové vlastnosti:**
- Základné údaje produktu (kód, názov, MJ)
- EAN kódy, SKU, PLU, katalógové čísla
- Rozmery, hmotnosť, objem
- Výrobca, krajina pôvodu
- Tovarové skupiny (product, financial, specific)
- Nákupné a predajné ceny

### 2. Tovarové skupiny - MGLST-product_categories.md

**Btrieve:** MGLST.BTR  
**Tabuľka:** `product_categories` WHERE `category_type='product'`

**Kľúčové vlastnosti:**
- Klasifikácia produktov podľa typu
- Napríklad: "Potraviny", "Elektronika", "Textil"

### 3. Finančné skupiny - FGLST-product_categories.md

**Btrieve:** FGLST.BTR  
**Tabuľka:** `product_categories` WHERE `category_type='financial'`

**Kľúčové vlastnosti:**
- Klasifikácia pre účtovníctvo
- Napríklad: "Zboží", "Materiál", "Služby"

### 4. Špecifické skupiny - SGLST-product_categories.md

**Btrieve:** SGLST.BTR  
**Tabuľka:** `product_categories` WHERE `category_type='specific'`

**Kľúčové vlastnosti:**
- Vlastné klasifikácie používateľa
- Flexibilné kategorizovanie

### 5. Čiarové kódy - BARCODE-product_catalog_identifiers.md

**Btrieve:** GSCAT.BTR (súčasť hlavného katalógu)  
**Tabuľka:** `product_catalog_identifiers`

**Typy identifikátorov:**
- `identifier_type='ean'` - EAN-13, EAN-8
- `identifier_type='sku'` - Stock Keeping Unit
- `identifier_type='plu'` - Price Look-Up
- `identifier_type='manufacturer_code'` - Kód výrobcu
- `identifier_type='catalog_number'` - Katalógové číslo

**Kľúčové vlastnosti:**
- Viacero identifikátorov na produkt
- is_primary flag
- Validácia EAN kontrolného čísla

---

## PRIORITA MIGRÁCIE

### Fáza 1: Číselníky (✅ Hotovo)

```
1. MGLST.BTR → product_categories (type='product')     ✅
2. FGLST.BTR → product_categories (type='financial')   ✅
3. SGLST.BTR → product_categories (type='specific')    ✅
```

### Fáza 2: Hlavný katalóg (✅ Hotovo)

```
4. GSCAT.BTR → product_catalog + 5 tabuliek            ✅
```

---

## KĽÚČOVÉ PRINCÍPY

### 1. Univerzálny číselník kategórií

```sql
-- Namiesto: product_groups, financial_groups, specific_groups
product_categories WHERE category_type IN ('product', 'financial', 'specific')
```

### 2. Viacero identifikátorov

```sql
-- Jeden produkt môže mať:
product_catalog_identifiers WHERE product_id = 123
  ├─ identifier_type='ean', identifier_value='8584001234567'
  ├─ identifier_type='sku', identifier_value='ABC-123'
  ├─ identifier_type='plu', identifier_value='1234'
  └─ identifier_type='manufacturer_code', identifier_value='MAN-XYZ'
```

### 3. Normalizovaná štruktúra

```sql
-- Hlavná tabuľka: len základné údaje
product_catalog (product_code, product_name, unit_id...)

-- Rozšírené údaje: oddelené tabuľky
product_catalog_identifiers  -- EAN, SKU, PLU
product_catalog_extensions   -- rozmery, hmotnosť
product_catalog_texts        -- výrobca, krajina
product_catalog_categories   -- tovarové skupiny
product_catalog_prices       -- ceny
```

### 4. Referenčná integrita

```sql
ON DELETE RESTRICT  → Master data (produkty, kategórie)
ON DELETE CASCADE   → Závislé dáta (identifiers, extensions)
BEZ FK              → Archívne dokumenty (invoice_items)
```

---

## KONZISTENCIA NÁZVOV POLÍ

```sql
*_id          INTEGER       -- FK primárny kľúč
*_code        VARCHAR       -- Textový kód
*_name        VARCHAR       -- Názov
category_type VARCHAR(20)   -- Typ kategórie
identifier_type VARCHAR(30) -- Typ identifikátora
is_primary    BOOLEAN       -- Primárny príznak
```

---

## ŠTATISTIKA

**Dokumenty:** 5  
**Tabuľky:** 7  
**Btrieve súbory:** 4  
**Status:** ✅ 100% kompletné

---

## VERZIA A ZMENY

### v1.0 (2025-12-11)
- Prvotná verzia
- Kompletná dokumentácia produktového katalógu
- 5 dokumentov, 7 tabuliek
- Nová štruktúra adresárov

---

**Koniec dokumentu products/INDEX.md**