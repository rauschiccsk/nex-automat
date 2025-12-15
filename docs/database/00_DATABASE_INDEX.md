# Database Documentation Index

**Kategória:** Database  
**Status:** 🟢 Complete  
**Vytvorené:** 2025-12-15  
**Aktualizované:** 2025-12-15

---

## Účel

Databázová dokumentácia obsahuje schémy, mappingy NEX Genesis → NEX Automat, migration dokumenty a detailné popisy tabuliek.

---

## Hlavné Dokumenty

### Kompletné Dokumenty

**[DATABASE_PRINCIPLES.md](DATABASE_PRINCIPLES.md)**
- Design principles, naming conventions
- Status: 🟢 Complete
- Veľkosť: ~24 KB, 985 riadkov

**[MIGRATION_MAPPING.md](MIGRATION_MAPPING.md)**
- Btrieve → PostgreSQL mapping
- Status: 🟢 Complete
- Veľkosť: ~23 KB, 657 riadkov

**[RELATIONSHIPS.md](RELATIONSHIPS.md)**
- Relationships medzi tabuľkami
- Status: 🟢 Complete
- Veľkosť: ~24 KB, 707 riadkov

**Reference dokumenty:**
- [CATALOGS_REFERENCE.md](CATALOGS_REFERENCE.md) - ~7 KB, 244 riadkov
- [PARTNERS_REFERENCE.md](PARTNERS_REFERENCE.md) - ~8 KB, 270 riadkov
- [PRODUCTS_REFERENCE.md](PRODUCTS_REFERENCE.md) - ~6 KB, 209 riadkov
- [SALES_REFERENCE.md](SALES_REFERENCE.md) - ~8 KB, 305 riadkov
- [STOCK_REFERENCE.md](STOCK_REFERENCE.md) - ~3 KB, 119 riadkov
- [STOCK_CARDS_REFERENCE.md](STOCK_CARDS_REFERENCE.md) - ~20 KB, 580 riadkov

---

## Database Table Documentation

### Partners Section (9 dokumentov) ✅ COMPLETE

**Location:** `catalogs/partners/tables/`

1. **BANKLST-bank_catalog.md** (~8 KB) - Číselník bánk
2. **PAB-partner_catalog.md** (~20 KB) - Katalóg partnerov
3. **PABACC-partner_catalog_bank_accounts.md** (~10 KB) - Bankové účty
4. **PACNCT-partner_catalog_contacts.md** (~13 KB) - Kontaktné osoby
5. **PAGLST-partner_categories.md** (~7 KB) - Kategórie partnerov
6. **PAYLST-payment_methods.md** (~6 KB) - Spôsoby platby
7. **TRPLST-transport_methods.md** (~6 KB) - Spôsoby dopravy
8. **PANOTI-partner_catalog_texts.md** (~7 KB) - Texty partnerov
9. **PASUBC-partner_catalog_facilities.md** (~8 KB) - Prevádzky partnerov

### Products Section (5 dokumentov) ✅ COMPLETE

**Location:** `catalogs/products/tables/`

1. **BARCODE-product_catalog_identifiers.md** (~11 KB) - Identifikátory produktov
2. **FGLST-product_categories.md** (~8 KB) - Kategórie F
3. **GSCAT-product_catalog.md** (~15 KB) - Katalóg produktov
4. **MGLST-product_categories.md** (~10 KB) - Kategórie M
5. **SGLST-product_categories.md** (~12 KB) - Kategórie S

### Stock Management Section (7 dokumentov) ✅ COMPLETE

**Location:** `stock/cards/tables/` a `stock/documents/tables/`

1. **WRILST-facilities.md** (~9 KB) - Sklady
2. **STKLST-stocks.md** (~9 KB) - Číselník skladov
3. **TSH-supplier_delivery_heads.md** (~15 KB) - Hlavičky dodacích listov
4. **FIF-stock_card_fifos.md** (~12 KB) - FIFO skladových kariet
5. **TSI-supplier_delivery_items.md** (~16 KB) - Položky dodacích listov
6. **STM-stock_card_movements.md** (~15 KB) - Pohyby skladových kariet
7. **STK-stock_cards.md** (~19 KB) - Skladové karty

### Accounting Section (3 dokumenty) ✅ COMPLETE

**Location:** `accounting/tables/`

1. **ISH-supplier_invoice_heads.md** (~22 KB) - Hlavičky faktúr
2. **ISI-supplier_invoice_items.md** (~21 KB) - Položky faktúr
3. **PAYJRN-payment_journal.md** (~18 KB) - Platobný denník

### Sales Section (1 dokument) ✅ COMPLETE

**Location:** `sales/tables/`

1. **PLSnnnnn-price_list_items.md** (~11 KB) - Položky cenníkov

---

## Štatistika

**Database Table Docs:**
- ✅ Partners: 9/9 (100%)
- ✅ Products: 5/5 (100%)
- ✅ Stock Management: 7/7 (100%)
- ✅ Accounting: 3/3 (100%)
- ✅ Sales: 1/1 (100%)
- **TOTAL: 25/25 (100%)** 🎉

**Reference Docs:** 11 dokumentov (100%)

**Total:** 36 kompletných dokumentov

---

## Quick Links

**Katalógy:**
- [Partners Tables](catalogs/partners/tables/) - 9 dokumentov
- [Products Tables](catalogs/products/tables/) - 5 dokumentov

**Doklady:**
- [Stock Cards](stock/cards/tables/) - 5 dokumentov
- [Stock Documents](stock/documents/tables/) - 2 dokumenty
- [Accounting](accounting/tables/) - 3 dokumenty
- [Sales](sales/tables/) - 1 dokument

**Reference:**
- [Database Principles](DATABASE_PRINCIPLES.md)
- [Migration Mapping](MIGRATION_MAPPING.md)
- [Relationships](RELATIONSHIPS.md)

---

**See Also:**
- [Documentation Index](../00_DOCUMENTATION_INDEX.md) - Hlavný index
- [System Architecture](../system/ARCHITECTURE.md) - Systémová architektúra
