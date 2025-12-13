# Catalogs - Číselníky

**Verzia:** 2.0  
**Dátum:** 2025-12-11  
**Status:** ✅ Kompletná dokumentácia

---

## PREHĽAD

Číselníky v NEX Automat systéme zabezpečujú konzistentné dáta pre katalógy, produkty, partnerov a obchodné transakcie.

**Zdokumentované:** 12 dokumentov (16 tabuliek)  
**Progress:** ✅ 100% (katalógy produktov a partnerov kompletné)

---

## NOVÁ ŠTRUKTÚRA DOKUMENTÁCIE

```
catalogs/
├── INDEX.md                    ✅ (v2.0) - Hlavný index
├── partners/
│   ├── INDEX.md                ✅ Prehľad partner katalógu
│   └── tables/
│       ├── PAB-partner_catalog.md
│       ├── PABACC-partner_catalog_bank_accounts.md
│       ├── PASUBC-partner_catalog_facilities.md
│       ├── PACNCT-partner_catalog_contacts.md
│       ├── PANOTI-partner_catalog_texts.md
│       ├── PAGLST-partner_categories.md
│       ├── PAYLST-payment_methods.md
│       ├── TRPLST-transport_methods.md
│       └── BANKLST-bank_catalog.md
└── products/
    ├── INDEX.md                ✅ Prehľad produktového katalógu
    └── tables/
        ├── GSCAT-product_catalog.md
        ├── MGLST-product_categories.md
        ├── FGLST-product_categories.md
        ├── SGLST-product_categories.md
        └── BARCODE-product_catalog_identifiers.md
```

---

## PRODUKTOVÝ KATALÓG

**Dokumenty:** 5  
**Tabuľky:** 7  
**Status:** ✅ 100% Kompletné

Detailná dokumentácia: [products/INDEX.md](./products/INDEX.md)

### Hlavné komponenty:

1. **GSCAT-product_catalog.md** (6 tabuliek)
   - product_catalog
   - product_catalog_identifiers
   - product_catalog_extensions
   - product_catalog_texts
   - product_catalog_categories
   - product_catalog_prices

2. **product_categories** (univerzálny číselník)
   - MGLST - tovarové skupiny
   - FGLST - finančné skupiny
   - SGLST - špecifické skupiny

3. **BARCODE-product_catalog_identifiers.md**
   - EAN, SKU, PLU, katalógové čísla

---

## PARTNER KATALÓG

**Dokumenty:** 7  
**Tabuľky:** 9  
**Status:** ✅ 100% Kompletné

Detailná dokumentácia: [partners/INDEX.md](./partners/INDEX.md)

### Hlavné komponenty:

1. **PAB-partner_catalog.md** (8 tabuliek)
   - partner_catalog
   - partner_catalog_extensions
   - partner_catalog_categories
   - partner_catalog_addresses
   - partner_catalog_contacts (univerzálna)
   - partner_catalog_texts (univerzálna)
   - partner_catalog_bank_accounts
   - partner_catalog_facilities

2. **Číselníky:**
   - PAGLST - skupiny partnerov
   - PAYLST - formy úhrady
   - TRPLST - spôsoby dopravy
   - BANKLST - číselník bánk

3. **Rozšírené tabuľky:**
   - PABACC - bankové účty
   - PASUBC - prevádzkové jednotky
   - PACNCT - kontakty (address + person)
   - PANOTI - textové polia (notice)

---

## KĽÚČOVÉ PRINCÍPY DOKUMENTÁCIE

### 1. Univerzálne tabuľky s typom

**Products:**
```sql
product_categories WHERE category_type IN ('product', 'financial', 'specific')
```

**Partners:**
```sql
partner_categories WHERE category_type IN ('supplier', 'customer')
partner_catalog_contacts WHERE contact_type IN ('address', 'person')
partner_catalog_texts WHERE text_type IN ('owner_name', 'description', 'notice')
```

### 2. Numerické ID pre číselníky

```sql
payment_method_id SERIAL PRIMARY KEY  -- 1, 2, 3...
payment_method_code VARCHAR(10)        -- "HOT", "KAR"...
```

**Výhody:**
- Konzistentné referencovanie (FK)
- Rýchlejšie JOIN operácie
- Textový kód pre ľudskú čitateľnosť

### 3. Referenčná integrita

```sql
ON DELETE RESTRICT  → Master data (produkty, partneri, kategórie)
ON DELETE CASCADE   → Závislé dáta (extensions, identifiers, addresses)
BEZ FK              → Archívne dokumenty (invoices, receipts)
```

### 4. Archívne dokumenty

**KRITICKÉ:**
- ✅ DENORMALIZOVANÉ - všetky údaje snapshot v dokumente
- ✅ BEZ FK constraints - partner_id, product_id môžu byť NULL
- ✅ Dôvod: Právny požiadavok (SK účtovné predpisy)

---

## KONZISTENCIA NÁZVOV POLÍ

```sql
*_id          INTEGER       -- FK primárny kľúč
*_code        VARCHAR       -- Textový kód (ľudsky čitateľný)
*_name        VARCHAR       -- Názov
*_type        VARCHAR(20)   -- Typ (category_type, contact_type...)
*_seat        VARCHAR(200)  -- Komplexná adresa (sídlo)
iban_code     VARCHAR(50)   -- ⚠️ NIE "iban"!
is_primary    BOOLEAN       -- Primárny príznak
is_active     BOOLEAN       -- Aktivita záznamu
created_at    TIMESTAMP     -- Vytvorené
created_by    VARCHAR(50)   -- Vytvoril
updated_at    TIMESTAMP     -- Zmenené
updated_by    VARCHAR(50)   -- Zmenil
```

---

## ĎALŠIE KROKY

### Stock (Skladové hospodárstvo)

```
📋 SKL.BTR → warehouses (sklady)
📋 STP.BTR → receipt_documents (príjemky)
📋 STV.BTR → issue_documents (výdajky)
📋 stock_cards, stock_movements...
```

### Accounting (Účtovníctvo)

```
📋 FAV.BTR → invoices (vydané)
📋 FAP.BTR → invoices (prijaté)
📋 chart_of_accounts...
```

### Sales (Odbyt)

```
📋 PLSnnnnn.BTR → price_list_items (cenníkové položky)
📋 SOH.BTR → sales_orders (objednávky)
```

---

## ŠTATISTIKA

| Sekcia | Dokumenty | Tabuľky | Status |
|--------|-----------|---------|--------|
| **Products** | 5 | 7 | ✅ 100% |
| **Partners** | 7 | 9 | ✅ 100% |
| **Stock** | 0 | 0 | 📋 Čaká |
| **Accounting** | 0 | 0 | 📋 Čaká |
| **Sales** | 0 | 0 | 📋 Čaká |
| **CELKOM** | **12** | **16** | **75%** |

---

## VERZIA A ZMENY

### v2.0 (2025-12-11) - NOVÁ ŠTRUKTÚRA
- ✅ Reorganizácia do partners/ a products/
- ✅ Nové INDEX.md pre partners a products
- ✅ Pridaný PACNCT-partner_catalog_contacts.md (univerzálna tabuľka)
- ✅ Pridaný PANOTI-partner_catalog_texts.md (univerzálna tabuľka)
- ✅ Aktualizovaná štatistika (12 dokumentov, 16 tabuliek)
- ✅ Partner katalóg 100% kompletný
- ✅ Produktový katalóg 100% kompletný

### v1.2 (2025-12-11)
- Pridaný PASUBC-partner_catalog_facilities.md
- Pridaný PAGLST-partner_categories.md
- Aktualizovaná štatistika (11 dokumentov)

### v1.1 (2025-12-10)
- Pridané dokumenty: PABACC, PAYLST, TRPLST, BANKLST, partner_categories
- Aktualizovaná štatistika (9 dokumentov)
- Presun PLSnnnnn do sales sekcie

### v1.0 (2025-12-09)
- Prvotná verzia
- Dokumenty: GSCAT, MGLST, FGLST, SGLST, PAB

---

**Koniec dokumentu INDEX.md**