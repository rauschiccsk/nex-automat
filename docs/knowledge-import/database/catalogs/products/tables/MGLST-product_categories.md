# MGLST.BTR → product_categories (Tovarové skupiny)

**Kategória:** Catalogs  
**NEX Genesis:** MGLST.BTR (Zoznam tovarových skupín)  
**NEX Automat:** `product_categories` (WHERE category_type = 'product')  
**Vytvorené:** 2025-12-10  
**Aktualizované:** 2025-12-15  
**Status:** ✅ Pripravené na migráciu

---

## PREHĽAD

### Btrieve súbor

**MGLST.BTR:**
- **Názov:** MGLST.BTR
- **Umiestnenie:** `C:\NEX\YEARACT\STORES\MGLST.BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\STORES\`
- **Účel:** Hierarchická štruktúra tovarových skupín s doporučeným ziskom

**Migrácia do:**
- Tabuľka: `product_categories` (univerzálny číselník)
- Typ: `category_type = 'product'`

---

## KOMPLETNÁ ŠTRUKTÚRA TABUĽKY product_categories

**Tabuľka `product_categories` je UNIVERZÁLNY číselník pre všetky 3 typy kategórií:**
- `category_type = 'product'` - Tovarové skupiny (MGLST.BTR) ← **tento dokument**
- `category_type = 'financial'` - Finančné skupiny (FGLST.BTR)
- `category_type = 'specific'` - Špecifické skupiny (SGLST.BTR)

### Použitie polí podľa typu

| Pole | product | financial | specific | Poznámka |
|------|---------|-----------|----------|----------|
| category_id | ✅ | ✅ | ✅ | PRIMARY KEY |
| category_type | ✅ | ✅ | ✅ | 'product'/'financial'/'specific' |
| category_code | ✅ | ✅ | ✅ | Unikátny kód |
| category_name | ✅ | ✅ | ✅ | Názov skupiny |
| parent_category_id | ✅ | ⚠️ | ⚠️ | Tovarové majú, ostatné zatiaľ nie |
| is_active | ✅ | ✅ | ✅ | Aktívna/neaktívna |
| created_by | ⚠️ | ⚠️ | ✅ | Len špecifické majú |
| created_at | ✅ | ✅ | ✅ | Timestamp vytvorenia |
| updated_by | ✅ | ✅ | ✅ | Kto naposledy modifikoval |
| updated_at | ✅ | ✅ | ✅ | Kedy naposledy modifikované |
| profit_margin | ✅ | ❌ | ❌ | **Len tovarové skupiny** |
| category_description | ❌ | ✅ | ❌ | **Len finančné skupiny** |
| max_discount | ❌ | ✅ | ❌ | **Len finančné skupiny** |
| min_profit_margin | ❌ | ✅ | ❌ | **Len finančné skupiny** |
| account_number | ❌ | ⚠️ | ❌ | Voliteľné pre finančné |

---

## MAPPING POLÍ

### Polia ktoré SA PRENÁŠAJÚ

| NEX Genesis | Typ | NEX Automat | Typ | Popis |
|-------------|-----|-------------|-----|-------|
| MgCode | longint | category_id | INTEGER | Číselný kód tovarovej skupiny |
| MgName | Str30 | category_name | VARCHAR(100) | Názov tovarovej skupiny |
| Parent | longint | parent_category_id | INTEGER | Nadradená skupina (0 = hlavná) |
| Profit | double | profit_margin | DECIMAL(5,2) | Doporučený zisk predaja (%) |
| ModUser | Str8 | updated_by | VARCHAR(30) | Kto naposledy modifikoval |
| ModDate | DateType | updated_at | TIMESTAMP | Kedy naposledy modifikované |
| ModTime | TimeType | updated_at | TIMESTAMP | Kedy naposledy modifikované |

### Dodatočné polia (nové v NEX Automat)

| NEX Automat | Typ | Popis | Hodnota |
|-------------|-----|-------|---------|
| category_type | VARCHAR(20) | Typ kategórie | 'product' (fixed) |
| category_code | VARCHAR(20) | Alfanumerický kód | MgCode (string) |
| is_active | BOOLEAN | Aktívna skupina | TRUE |
| created_by | VARCHAR(30) | Kto vytvoril | NULL alebo ModUser |
| created_at | TIMESTAMP | Dátum vytvorenia | CURRENT_TIMESTAMP |

**Poznámky k mappingu:**
- `Parent = 0` sa transformuje na `NULL` (hlavná skupina nemá rodiča)
- `ModUser/ModDate/ModTime` sa použijú pre `created_by/created_at` aj `updated_by/updated_at`
- Ak ModUser neexistuje, použije sa 'MIGRATION'

---

## POLIA KTORÉ SA NEPRENÁŠAJÚ

| NEX Genesis | Typ | Dôvod neprenášania |
|-------------|-----|--------------------|
| _MgName | Str15 | Vyhľadávacie pole - PostgreSQL full-text search |
| Sended | byte | Zastarané (sync flag) |
| ModNum | word | PostgreSQL má verziu cez trigger |
| PrfPrc1-3 | double | Doporučený zisk pre D1-D3 - riešime inak |
| DscPrc1-3 | double | Percentuálna zľava - riešime inak |
| Eshop1-5 | byte | E-shop príznaky - riešime inak |

**Poznámka k cenám a zľavám:**  
- Doporučené zisky pre rôzne ceny (D1, D2, D3) a zľavy budú riešené cez samostatný cenníkový systém
- E-shop príznaky budú riešené cez `product_catalog_extensions.eshop_id`

---

## BIZNIS LOGIKA

### Hierarchická štruktúra

**Príklad:**
```
1000 - Potraviny (parent = NULL)
  ├── 1100 - Mliečne výrobky (parent = 1000)
  │   ├── 1110 - Mlieko (parent = 1100)
  │   └── 1120 - Syry (parent = 1100)
  └── 1200 - Pečivo (parent = 1000)
      ├── 1210 - Chlieb (parent = 1200)
      └── 1220 - Rožky (parent = 1200)
```

**Hierarchia sa implementuje cez rekurzívne SQL dotazy (recursive CTE).**

### Doporučený zisk (Profit Margin)

**Použitie:**
- Automatický výpočet predajnej ceny z nákupnej
- Predajná cena = Nákupná cena × (1 + profit_margin / 100)
- Príklad: profit_margin = 25% → predajná cena = nákupná × 1.25

**Aplikácia:**
1. Produkt má priradené `product_catalog_categories` s `category_type = 'product'`
2. Z tejto kategórie sa načíta `profit_margin`
3. Ak produkt nemá priradené, použije sa profit_margin z nadriadenej skupiny
4. Ak ani tam nie je, použije sa systémový default

---

## VZŤAHY S INÝMI TABUĽKAMI

### product_catalog ← product_catalog_categories → product_categories

**Vzťah:** Many-to-Many cez `product_catalog_categories`
- Produkt môže patriť do viacerých kategórií
- Tovarová skupina je jeden typ kategórie (`category_type = 'product'`)

**Foreign Keys:**
- `category_id` → `product_categories(category_id)` ON DELETE RESTRICT
- `parent_category_id` → `product_categories(category_id)` ON DELETE RESTRICT (self-reference)

**Poznámky:**
- Nesmie sa zmazať kategória s produktmi (RESTRICT)
- Nesmie sa zmazať kategória s podskupinami (RESTRICT)

---

## VALIDAČNÉ PRAVIDLÁ

### 1. Kategória musí byť typu 'product'

**Kontrola:** `category_type = 'product'`

### 2. Parent nesmie vytvoriť cyklus

**Kontrola:** Aplikačná logika - pred INSERT/UPDATE skontrolovať že nový parent nevytvorí cyklickú referenciu

### 3. Parent musí byť rovnakého typu

**Pravidlo:** Ak tovarová skupina má parent, musí to byť tiež tovarová skupina (`category_type = 'product'`)

### 4. Nesmie sa zmazať kategória s produktmi

**Ošetrené:** FK constraint ON DELETE RESTRICT

### 5. Nesmie sa zmazať kategória s podskupinami

**Ošetrené:** Self-reference FK constraint ON DELETE RESTRICT

### 6. Audit polia (štandard pre všetky tabuľky)

- `created_by`, `created_at` - kto a kedy vytvoril záznam (nemenné)
- `updated_by`, `updated_at` - kto a kedy naposledy modifikoval (aktualizuje sa pri každej zmene)

---

## PRÍKLADY DÁT

### Príklad 1 - Hlavné skupiny

```
category_id=1000, type='product', name='Potraviny', parent=NULL, profit_margin=25.00
category_id=2000, type='product', name='Nápoje', parent=NULL, profit_margin=30.00
category_id=3000, type='product', name='Drogéria', parent=NULL, profit_margin=35.00
```

### Príklad 2 - Podskupiny (1. úroveň)

```
category_id=1100, type='product', name='Mliečne výrobky', parent=1000, profit_margin=20.00
category_id=1200, type='product', name='Pečivo', parent=1000, profit_margin=15.00
category_id=2100, type='product', name='Nealkoholické', parent=2000, profit_margin=28.00
category_id=2200, type='product', name='Alkoholické', parent=2000, profit_margin=40.00
```

### Príklad 3 - Podpodskupiny (2. úroveň)

```
category_id=1110, type='product', name='Mlieko', parent=1100, profit_margin=18.00
category_id=1120, type='product', name='Syry', parent=1100, profit_margin=22.00
category_id=1210, type='product', name='Chlieb', parent=1200, profit_margin=12.00
category_id=2110, type='product', name='Minerálne vody', parent=2100, profit_margin=25.00
```

---

## ROZDIEL OPROTI FGLST

| Vlastnosť | MGLST (Tovarové) | FGLST (Finančné) |
|-----------|------------------|------------------|
| Parent | ✅ Má | ❌ Nemá (pridávame) |
| Popis | ❌ Nemá | ✅ Describe (150 znakov) |
| Profit Margin | ✅ Profit | ✅ MinPrf |
| Max Discount | ❌ Nemá | ✅ MaxDsc |
| Účel | Kategorizácia | Účtovníctvo + kontrola |
| Hierarchia | ✅ Viacúrovňová | ❌ Plochá |
| Audit polia | ✅ created/updated | ✅ created/updated |

---

## MIGRAČNÉ POZNÁMKY

### Poradie migrácie

1. Najprv migrovať číselníky kategórií (MGLST, FGLST, SGLST)
2. Potom migrovať produkty (GSCAT)
3. Nakoniec vytvoriť väzby (product_catalog_categories)

### Kontrola hierarchie

- Skontrolovať že všetky Parent hodnoty existujú v MGLST
- Detekovať cyklické referencie pred migráciou
- Overiť že žiadna kategória neodkazuje sama na seba

### Testovanie po migrácii

- Overiť počet záznamov: MGLST.BTR vs product_categories WHERE category_type='product'
- Skontrolovať hierarchiu (recursive query)
- Overiť že audit polia sú správne naplnené
- Testovať že nesmie sa zmazať kategória s produktmi

---

## SÚVISIACE DOKUMENTY

- **product_catalog** → `GSCAT-product_catalog.md`
- **product_catalog_categories** → `GSCAT-product_catalog.md` (mapovacia tabuľka)
- **FGLST** (finančné skupiny) → `FGLST-product_categories.md`
- **SGLST** (špecifické skupiny) → `SGLST-product_categories.md`
- **DATABASE_RELATIONSHIPS** → `DATABASE_RELATIONSHIPS.md`

---

**Vytvoril:** Claude & Zoltán  
**Dátum:** 2025-12-10  
**Aktualizované:** 2025-12-15  
**Verzia:** 1.2  
**Status:** ✅ Pripravené na migráciu