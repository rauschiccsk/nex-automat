# Database Documentation Index

**Kategória:** Database  
**Status:** 🟡 In Progress  
**Vytvorené:** 2025-12-15  
**Aktualizované:** 2025-12-15

---

## Účel

Databázová dokumentácia obsahuje schémy, mappingy NEX Genesis → NEX Automat, migration dokumenty a detailné popisy tabuliek.

---

## Štruktúra

Databázová dokumentácia je rozdelená do kategórií:

### [catalogs/](catalogs/)
Katalógové tabuľky (master data)
- **Produkty:** GSCAT, BARCODE, FGLST, MGLST, SGLST
- **Partneri:** PAB, PABACC, PACNCT, PAGLST, PANOTI, PASUBC
- **Podporné:** BANKLST, PAYLST, TRPLST

**Status:** Obsahuje .md-old súbory na migráciu

### [documents/](documents/)
Dokladové tabuľky (transactional data)
- **Nákup:** TSH, TSI (supplier deliveries)
- **Predaj:** (budúce dokumenty)
- **Účtovníctvo:** ISH, ISI, PAYJRN

**Status:** Obsahuje .md-old súbory na migráciu

### [migrations/](migrations/)
Migration dokumenty
- Btrieve → PostgreSQL migration plány
- Data transformation rules
- Schema evolution

**Status:** Prázdne, pripravené na dokumenty

---

## Dostupné .md-old Súbory na Migráciu

### Katalógy - Produkty (5 súborov)
- `GSCAT-product_catalog.md-old` (20.7 KB)
- `BARCODE-product_catalog_identifiers.md-old` (24.2 KB)
- `FGLST-product_categories.md-old` (16.1 KB)
- `MGLST-product_categories.md-old` (17.4 KB)
- `SGLST-product_categories.md-old` (20.1 KB)

### Katalógy - Partneri (9 súborov)
- `PAB-partner_catalog.md-old` (39.9 KB)
- `PABACC-partner_catalog_bank_accounts.md-old` (12.6 KB)
- `PACNCT-partner_catalog_contacts.md-old` (22.8 KB)
- `PAGLST-partner_categories.md-old` (14.9 KB)
- `PANOTI-partner_catalog_texts.md-old` (15.4 KB)
- `PASUBC-partner_catalog_facilities.md-old` (18.0 KB)
- `BANKLST-bank_catalog.md-old` (10.7 KB)
- `PAYLST-payment_methods.md-old` (8.3 KB)
- `TRPLST-transport_methods.md-old` (8.6 KB)

### Doklady - Stock (7 súborov)
- `STK-stock_cards.md-old` (38.5 KB)
- `STM-stock_card_movements.md-old` (35.6 KB)
- `FIF-stock_card_fifos.md-old` (28.5 KB)
- `STKLST-stocks.md-old` (20.4 KB)
- `WRILST-facilities.md-old` (17.9 KB)
- `TSH-supplier_delivery_heads.md-old` (25.4 KB)
- `TSI-supplier_delivery_items.md-old` (29.7 KB)

### Doklady - Accounting (3 súbory)
- `ISH-supplier_invoice_heads.md-old` (34.8 KB)
- `ISI-supplier_invoice_items.md-old` (29.6 KB)
- `PAYJRN-payment_journal.md-old` (25.8 KB)

### Všeobecné (4 súbory)
- `COMMON_DOCUMENT_PRINCIPLES.md-old` (42.8 KB)
- `DATABASE_RELATIONSHIPS.md-old` (24.1 KB)
- `DATA_DICTIONARY.md-old` (22.7 KB)
- `INDEX.md-old` (6.0 KB)

---

## Migration Strategy

Databázová dokumentácia sa bude migrovať postupne:

1. **Fáza 1:** Všeobecné dokumenty (principles, relationships, dictionary)
2. **Fáza 2:** Katalógy produktov (GSCAT, BARCODE, kategórie)
3. **Fáza 3:** Katalógy partnerov (PAB a súvisiace)
4. **Fáza 4:** Stock dokumenty (STK, STM, doklady)
5. **Fáza 5:** Accounting dokumenty (faktúry, platby)

---

## Quick Links

**Katalógy:**
- [Catalogs Directory](catalogs/) - Master data tabuľky

**Doklady:**
- [Documents Directory](documents/) - Transactional data tabuľky

**Migrácie:**
- [Migrations Directory](migrations/) - Migration plány

---

## Štatistika

- **Kategórie:** 3 (catalogs, documents, migrations)
- **.md-old súborov:** 32
- **Total veľkosť .md-old:** ~540 KB
- **Status:** Pripravené na systematickú migráciu

---

**See Also:**
- [Documentation Index](../00_DOCUMENTATION_INDEX.md) - Hlavný index
- [System Architecture](../system/ARCHITECTURE.md) - Systémová architektúra
- [Migration Index](../migration/00_MIGRATION_INDEX.md) - Migration dokumenty
