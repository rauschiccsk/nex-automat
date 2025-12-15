# NEX Automat - Database Documentation

**Projekt:** nex-automat  
**Vytvorené:** 2025-12-10  
**Účel:** Kompletná databázová dokumentácia pre migráciu NEX Genesis → NEX Automat

---

## PREHĽAD DOKUMENTÁCIE

### 1. DATABASE_RELATIONSHIPS.md ✅
**Hlavný dokument o vzťahoch medzi tabuľkami**

- Cross-system vzťahy (Catalogs ↔ Stock ↔ Accounting)
- Referenčná integrita (FK constraints, cascading rules)
- Archívne dokumenty (denormalizácia faktúr, dokladov)
- Biznis pravidlá a validácie
- Query patterns a indexy
- ER diagram

**Cesta:** `DATABASE_RELATIONSHIPS.md`

---

## KATEGÓRIE TABULIEK

### 📊 Catalogs (Číselníky)
**Folder:** `catalogs/`

| Kategória | Zdokumentované | Celkom | Progress |
|-----------|----------------|--------|----------|
| Produkty | 1 | 1 | ✅ 100% |
| Kategórie | 3 | 3 | ✅ 100% |
| Partneri | 0 | 1 | ⏳ 0% |
| Ostatné | 0 | 3 | ⏳ 0% |

**Detaily:** Pozri [catalogs/INDEX.md](catalogs/products/INDEX.md)

**Zdokumentované tabuľky:**
- ✅ product_catalog (GSCAT.BTR)
- ✅ product_categories - tovarové skupiny (MGLST.BTR)
- ✅ product_categories - finančné skupiny (FGLST.BTR)
- ✅ product_categories - špecifické skupiny (SGLST.BTR)

**Čakajú:**
- ⏳ partner_catalog (PAB.BTR)
- ⏳ units (merné jednotky)
- ⏳ warehouses (sklady)

---

### 📦 Stock (Skladové hospodárstvo)
**Folder:** `stock/`

| Kategória | Zdokumentované | Celkom | Progress |
|-----------|----------------|--------|----------|
| Stock Cards | 0 | 1 | ⏳ 0% |
| Movements | 0 | 1 | ⏳ 0% |
| Documents | 0 | 2 | ⏳ 0% |

**Čakajú:**
- ⏳ stock_cards (skladové karty)
- ⏳ stock_movements (pohyby)
- ⏳ receipt_documents (príjemky)
- ⏳ issue_documents (výdajky)

---

### 💰 Accounting (Účtovníctvo)
**Folder:** `accounting/`

| Kategória | Zdokumentované | Celkom | Progress |
|-----------|----------------|--------|----------|
| Chart of Accounts | 0 | 1 | ⏳ 0% |
| Invoices | 0 | 2 | ⏳ 0% |

**Čakajú:**
- ⏳ chart_of_accounts (účtová osnova)
- ⏳ invoices (faktúry - archívne)
- ⏳ invoice_items (položky faktúr - archívne)

---

### 📁 System (Systémové tabuľky)
**Folder:** `system/`

| Kategória | Zdokumentované | Celkom | Progress |
|-----------|----------------|--------|----------|
| System | 0 | ~5 | ⏳ 0% |

**Čakajú:**
- ⏳ users (užívatelia)
- ⏳ permissions (oprávnenia)
- ⏳ configuration (konfigurácia)

---

## ŠTATISTIKA

### Celkový pokrok

```
📊 Zdokumentované: 4 tabuľky
📋 Čakajú: ~20 tabuliek
📈 Pokrok: ~17%

✅ Catalogs: 4/8 (50%)
⏳ Stock: 0/4 (0%)
⏳ Accounting: 0/3 (0%)
⏳ System: 0/5 (0%)
```

### Dokumenty

```
✅ DATABASE_RELATIONSHIPS.md
✅ catalogs/INDEX.md
✅ catalogs/tables/GSCAT-product_catalog.md
✅ catalogs/tables/MGLST-product_categories.md
✅ catalogs/tables/FGLST-product_categories.md
✅ catalogs/tables/SGLST-product_categories.md
```

---

## KĽÚČOVÉ PRINCÍPY

### 1. Naming Convention

**Mapping dokumenty:**
```
STARY_NAZOV-novy_nazov.md
```

**Príklady:**
- GSCAT-product_catalog.md (GSCAT.BTR → product_catalog)
- PAB-partner_catalog.md (PAB.BTR → partner_catalog)
- MGLST-product_categories.md (MGLST.BTR → product_categories WHERE category_type='product')

### 2. Univerzálne číselníky

**Namiesto:**
```
product_groups (MGLST)
financial_groups (FGLST)
specific_groups (SGLST)
```

**Používame:**
```
product_categories (jedna tabuľka, 3 typy)
WHERE category_type IN ('product', 'financial', 'specific')
```

### 3. Archívne dokumenty

**Faktúry, príjemky, výdajky:**
- ✅ Denormalizované (všetky údaje uložené v dokumente)
- ✅ BEZ FK constraints (partner_id, product_id môžu byť NULL)
- ✅ Nemenné (právny požiadavok)

### 4. Referenčná integrita

**ON DELETE RESTRICT:**
- Master data (produkty, kategórie, partneri)
- Operatívne dáta (stock cards)

**ON DELETE CASCADE:**
- Závislé dáta (extensions, identifiers, categories, texts)

**BEZ FK:**
- Archívne dokumenty (invoices, receipts, issues)

---

## KONVENCIE DOKUMENTÁCIE

### Štruktúra mapping dokumentu

1. **Prehľad** - NEX Genesis → NEX Automat
2. **Kompletná štruktúra tabuľky** - SQL CREATE TABLE
3. **Mapping polí** - Stará → Nová tabuľka
4. **Migračný script** - INSERT/UPDATE príkazy
5. **Polia ktoré sa neprenášajú** - Zastaralé/nepoužité
6. **Biznis logika** - Ako sa používa v praxi
7. **Vzťahy s inými tabuľkami** - FK relationships
8. **Validačné pravidlá** - CHECK constraints, triggers
9. **Query patterns** - Typické SQL queries
10. **Príklad dát** - Sample INSERT statements

---

## NÁSTROJE

### SQL Scripts

**Migračné skripty:**
```
scripts/migrations/
├── 01_create_product_categories.sql
├── 02_migrate_mglst.sql
├── 03_migrate_fglst.sql
├── 04_migrate_sglst.sql
└── 05_migrate_gscat.sql
```

**Validačné skripty:**
```
scripts/validation/
├── check_product_categories.sql
├── check_data_integrity.sql
└── compare_counts.sql
```

---

## QUICK START

### Pre nového developera

1. **Čítaj najprv:** `DATABASE_RELATIONSHIPS.md`
2. **Potom kategóriu:** `catalogs/INDEX.md`
3. **Detail tabuľky:** `catalogs/tables/GSCAT-product_catalog.md`

### Pre migráciu

1. **Prečítaj mapping:** `GSCAT-product_catalog.md`
2. **Spusti migration script:** `01_create_product_categories.sql`
3. **Validuj dáta:** `check_product_categories.sql`
4. **Skontroluj vzťahy:** `DATABASE_RELATIONSHIPS.md`

---

## KONTAKT

**Developer:** Zoltán  
**Company:** ICC Komárno  
**Projekt:** NEX Automat v2.4  
**Dátum start:** 2025-12-10

---

**Vytvoril:** Claude & Zoltán  
**Verzia:** 1.0  
**Status:** 🔄 V práci - rozširuje sa s každou novou tabuľkou