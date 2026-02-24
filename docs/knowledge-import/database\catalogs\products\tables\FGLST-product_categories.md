# FGLST.BTR → product_categories (Finančné skupiny)

**Kategória:** Catalogs  
**NEX Genesis:** FGLST.BTR (Zoznam finančných skupín)  
**NEX Automat:** `product_categories` (WHERE category_type = 'financial')  
**Vytvorené:** 2025-12-10  
**Aktualizované:** 2025-12-15  
**Status:** ✅ Pripravené na migráciu

---

## PREHĽAD

### Btrieve súbor

**FGLST.BTR:**
- **Názov:** FGLST.BTR
- **Umiestnenie:** `C:\NEX\YEARACT\STORES\FGLST.BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\STORES\`
- **Účel:** Finančné skupiny produktov pre účtovníctvo a kontrolu marží/zliav

**Migrácia do:**
- Tabuľka: `product_categories` (univerzálny číselník)
- Typ: `category_type = 'financial'`

---

## MAPPING POLÍ

### Polia ktoré SA PRENÁŠAJÚ

| NEX Genesis | Typ | NEX Automat | Typ | Popis |
|-------------|-----|-------------|-----|-------|
| FgCode | longint | category_id | INTEGER | Číselný kód finančnej skupiny |
| FgName | Str30 | category_name | VARCHAR(100) | Názov finančnej skupiny |
| Describe | Str150 | category_description | TEXT | Podrobný popis skupiny |
| MaxDsc | double | max_discount | DECIMAL(5,2) | Maximálna hodnota zľavy (%) |
| MinPrf | double | min_profit_margin | DECIMAL(5,2) | Minimálna obchodná marža (%) |
| ModUser | Str8 | updated_by | VARCHAR(30) | Kto naposledy modifikoval |
| ModDate | DateType | updated_at | TIMESTAMP | Kedy naposledy modifikované |
| ModTime | TimeType | updated_at | TIMESTAMP | Kedy naposledy modifikované |

### Dodatočné polia (nové v NEX Automat)

| NEX Automat | Typ | Popis | Hodnota |
|-------------|-----|-------|---------|
| category_type | VARCHAR(20) | Typ kategórie | 'financial' (fixed) |
| category_code | VARCHAR(20) | Alfanumerický kód | FgCode (string) |
| parent_category_id | INTEGER | Nadradená skupina | NULL (zatiaľ) |
| is_active | BOOLEAN | Aktívna skupina | TRUE |
| created_by | VARCHAR(30) | Kto vytvoril | NULL alebo ModUser |
| created_at | TIMESTAMP | Dátum vytvorenia | CURRENT_TIMESTAMP |

**Poznámky k mappingu:**
- `ModUser/ModDate/ModTime` sa použijú pre `created_by/created_at` aj `updated_by/updated_at`
- Ak ModUser neexistuje, použije sa 'MIGRATION'
- `parent_category_id` pridávame aj keď v FGLST.BTR nie je - pre budúcu hierarchiu

---

## POLIA KTORÉ SA NEPRENÁŠAJÚ

| NEX Genesis | Typ | Dôvod neprenášania |
|-------------|-----|--------------------|
| _FgName | Str20 | Vyhľadávacie pole - PostgreSQL full-text search |
| Sended | byte | Zastarané (sync flag) |
| ModNum | word | PostgreSQL má verziu cez trigger |

---

## BIZNIS LOGIKA

### Účel finančných skupín

**1. Účtovníctvo:**
- Finančná skupina určuje na ktorý účet sa zaúčtuje predaj/nákup
- Väzba na účtovú osnovu (`chart_of_accounts`)

**2. Kontrola marží:**
- `min_profit_margin` = minimálna povolená marža pre produkty v tejto skupine
- Systém varuje ak sa snaží používateľ zadať nižšiu maržu

**3. Kontrola zliav:**
- `max_discount` = maximálna povolená zľava pre produkty v tejto skupine
- Systém varuje/blokuje vyššiu zľavu

### Príklad validácie

Pri zadávaní ceny/zľavy systém kontroluje:
- Ak vypočítaná marža < `min_profit_margin` → WARNING
- Ak zľava % > `max_discount` → WARNING/BLOCK

---

## VZŤAHY S INÝMI TABUĽKAMI

### product_catalog ← product_catalog_categories → product_categories

**Vzťah:** Many-to-Many cez `product_catalog_categories`
- Produkt môže patriť do viacerých kategórií
- Finančná skupina je jeden typ kategórie (`category_type = 'financial'`)

**Foreign Key:** `category_id` → `product_categories(category_id)` ON DELETE RESTRICT

**Poznámka:** Nesmie sa zmazať finančná skupina s produktmi (RESTRICT).

---

## VALIDAČNÉ PRAVIDLÁ

### 1. Kategória musí byť typu 'financial'

**Kontrola:** `category_type = 'financial'`

### 2. Marža a zľava musia byť v rozumných medziach

**Pravidlá:**
- `min_profit_margin` musí byť 0-100%
- `max_discount` musí byť 0-100%
- Logická kontrola: zľava by nemala byť väčšia ako marža (WARNING ak áno)

### 3. Nesmie sa zmazať finančná skupina s produktmi

**Ošetrené:** FK constraint ON DELETE RESTRICT

### 4. Audit polia (štandard pre všetky tabuľky)

- `created_by`, `created_at` - kto a kedy vytvoril záznam (nemenné)
- `updated_by`, `updated_at` - kto a kedy naposledy modifikoval (aktualizuje sa pri každej zmene)

---

## PRÍKLADY DÁT

### Príklad 1 - Základné finančné skupiny

```
category_id=10, type='financial', name='Potraviny - DPH 10%', 
    description='Základné potraviny so zníženou sadzbou DPH 10%',
    max_discount=10.00, min_profit_margin=15.00

category_id=20, type='financial', name='Potraviny - DPH 20%',
    description='Potraviny so základnou sadzbou DPH 20%',
    max_discount=15.00, min_profit_margin=20.00

category_id=30, type='financial', name='Nápoje alkoholické',
    description='Alkoholické nápoje s DPH 20% a spotrebnou daňou',
    max_discount=5.00, min_profit_margin=40.00
```

### Príklad 2 - Lieky (zákaz zliav)

```
category_id=50, type='financial', name='Lieky',
    description='Lieky a zdravotnícke pomôcky s DPH 10%',
    max_discount=0.00, min_profit_margin=10.00
```

**Poznámka:** `max_discount = 0%` = zákaz zliav na lieky

---

## HIERARCHIA (BUDÚCNOSŤ)

**V FGLST.BTR nie je pole Parent, ale v product_categories sme pridali `parent_category_id` pre budúcu hierarchiu.**

**Príklad možnej hierarchie:**
```
10 - Potraviny - DPH 10% (parent = NULL)
  ├── 11 - Mliečne výrobky - DPH 10% (parent = 10)
  └── 12 - Pečivo - DPH 10% (parent = 10)
20 - Potraviny - DPH 20% (parent = NULL)
  ├── 21 - Sladkosti - DPH 20% (parent = 20)
  └── 22 - Delikatesy - DPH 20% (parent = 20)
```

---

## ROZDIEL OPROTI MGLST

| Vlastnosť | MGLST (Tovarové) | FGLST (Finančné) |
|-----------|------------------|------------------|
| Parent | ✅ Má | ❌ Nemá (pridávame) |
| Popis | ❌ Nemá | ✅ Describe (150 znakov) |
| Profit Margin | ✅ Profit | ✅ MinPrf |
| Max Discount | ❌ Nemá | ✅ MaxDsc |
| Účel | Kategorizácia | Účtovníctvo + kontrola |
| Audit polia | ✅ created/updated | ✅ created/updated |

---

## VÄZBA NA ÚČTOVNÍCTVO

**Finančná skupina môže mať väzbu na účtovú osnovu:**

Rozšírenie: `product_categories.account_number` (VARCHAR(10))

**Použitie:** Pri vytváraní účtovného zápisu z faktúry sa použije account_number z finančnej skupiny produktu.

---

## MIGRAČNÉ POZNÁMKY

### Poradie migrácie

1. Najprv migrovať číselníky kategórií (MGLST, FGLST, SGLST)
2. Potom migrovať produkty (GSCAT)
3. Nakoniec vytvoriť väzby (product_catalog_categories)

### Kontrola po migrácii

- Overiť počet záznamov: FGLST.BTR vs product_categories WHERE category_type='financial'
- Skontrolovať že marže a zľavy sú v rozsahu 0-100%
- Overiť že audit polia sú správne naplnené

---

## SÚVISIACE DOKUMENTY

- **product_catalog** → `GSCAT-product_catalog.md`
- **product_catalog_categories** → `GSCAT-product_catalog.md` (mapovacia tabuľka)
- **MGLST** (tovarové skupiny) → `MGLST-product_categories.md`
- **SGLST** (špecifické skupiny) → `SGLST-product_categories.md`
- **DATABASE_RELATIONSHIPS** → `DATABASE_RELATIONSHIPS.md`

---

**Vytvoril:** Claude & Zoltán  
**Dátum:** 2025-12-10  
**Aktualizované:** 2025-12-15  
**Verzia:** 1.2  
**Status:** ✅ Pripravené na migráciu