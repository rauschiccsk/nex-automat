# SGLST.BTR → product_categories (Špecifické skupiny)

**Kategória:** Catalogs  
**NEX Genesis:** SGLST.BTR (Zoznam špecifikačných skupín)  
**NEX Automat:** `product_categories` (WHERE category_type = 'specific')  
**Vytvorené:** 2025-12-10  
**Aktualizované:** 2025-12-15  
**Status:** ✅ Pripravené na migráciu

---

## PREHĽAD

### Btrieve súbor

**SGLST.BTR:**
- **Názov:** SGLST.BTR
- **Umiestnenie:** `C:\NEX\YEARACT\STORES\SGLST.BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\STORES\`
- **Účel:** Špecifické skupiny produktov pre vlastnú kategorizáciu zákazníka

**Migrácia do:**
- Tabuľka: `product_categories` (univerzálny číselník)
- Typ: `category_type = 'specific'`

---

## KOMPLETNÁ ŠTRUKTÚRA TABUĽKY product_categories

**Tabuľka `product_categories` je UNIVERZÁLNY číselník pre všetky 3 typy kategórií:**
- `category_type = 'product'` - Tovarové skupiny (MGLST.BTR)
- `category_type = 'financial'` - Finančné skupiny (FGLST.BTR)
- `category_type = 'specific'` - Špecifické skupiny (SGLST.BTR) ← **tento dokument**

### Použitie polí podľa typu

| Pole | product | financial | specific | Poznámka |
|------|---------|-----------|----------|----------|
| category_id | ✅ | ✅ | ✅ | PRIMARY KEY |
| category_type | ✅ | ✅ | ✅ | 'product'/'financial'/'specific' |
| category_code | ✅ | ✅ | ✅ | Unikátny kód |
| category_name | ✅ | ✅ | ✅ | Názov skupiny |
| parent_category_id | ✅ | ⚠️ | ⚠️ | Tovarové majú, ostatné zatiaľ nie |
| is_active | ✅ | ✅ | ✅ | Aktívna/neaktívna |
| created_by | ⚠️ | ⚠️ | ✅ | **Len špecifické majú** |
| created_at | ✅ | ✅ | ✅ | Timestamp vytvorenia |
| updated_by | ✅ | ✅ | ✅ | Kto naposledy modifikoval |
| updated_at | ✅ | ✅ | ✅ | Kedy naposledy modifikované |
| profit_margin | ✅ | ❌ | ❌ | Len tovarové skupiny |
| category_description | ❌ | ✅ | ❌ | Len finančné skupiny |
| max_discount | ❌ | ✅ | ❌ | Len finančné skupiny |
| min_profit_margin | ❌ | ✅ | ❌ | Len finančné skupiny |
| account_number | ❌ | ⚠️ | ❌ | Voliteľné pre finančné |

---

## MAPPING POLÍ

### Polia ktoré SA PRENÁŠAJÚ

| NEX Genesis | Typ | NEX Automat | Typ | Popis |
|-------------|-----|-------------|-----|-------|
| SgCode | longint | category_id | INTEGER | Číselný kód špecifikačnej skupiny |
| SgName | Str50 | category_name | VARCHAR(100) | Názov špecifikačnej skupiny |
| CrtUser | Str8 | created_by | VARCHAR(30) | Užívateľ ktorý vytvoril |
| CrtDate | DateType | created_at | TIMESTAMP | Dátum a čas vytvorenia |
| CrtTime | TimeType | created_at | TIMESTAMP | Zahrnuté v created_at |
| ModUser | Str8 | updated_by | VARCHAR(30) | Kto naposledy modifikoval |
| ModDate | DateType | updated_at | TIMESTAMP | Kedy naposledy modifikované |
| ModTime | TimeType | updated_at | TIMESTAMP | Zahrnuté v updated_at |

### Dodatočné polia (nové v NEX Automat)

| NEX Automat | Typ | Popis | Hodnota |
|-------------|-----|-------|---------|
| category_type | VARCHAR(20) | Typ kategórie | 'specific' (fixed) |
| category_code | VARCHAR(20) | Alfanumerický kód | SgCode (string) |
| parent_category_id | INTEGER | Nadradená skupina | NULL (zatiaľ) |
| is_active | BOOLEAN | Aktívna skupina | TRUE |

**Poznámky k mappingu:**
- `CrtUser/CrtDate/CrtTime` sa použijú pre `created_by/created_at`
- `ModUser/ModDate/ModTime` sa použijú pre `updated_by/updated_at`
- Ak ModUser neexistuje, použije sa CrtUser
- Ak ani CrtUser neexistuje, použije sa 'MIGRATION'
- `parent_category_id` pridávame pre budúcu hierarchiu, aj keď v SGLST.BTR nie je

---

## POLIA KTORÉ SA NEPRENÁŠAJÚ

| NEX Genesis | Typ | Dôvod neprenášania |
|-------------|-----|--------------------|
| _SgName | Str50 | Vyhľadávacie pole - PostgreSQL full-text search |

---

## BIZNIS LOGIKA

### Účel špecifických skupín

**Flexibilná kategorizácia podľa potrieb zákazníka:**

Špecifické skupiny slúžia na **vlastnú kategorizáciu**, ktorú si definuje každý zákazník podľa svojich potrieb. Na rozdiel od:
- **Tovarové skupiny (MGLST)** - hlavná kategorizácia produktov
- **Finančné skupiny (FGLST)** - účtovníctvo a kontrola marží

**Príklady použitia:**

1. **Regionálna kategorizácia:**
   - "Slovenské produkty"
   - "Zahraničné produkty"
   - "Bio produkty"

2. **Marketingová kategorizácia:**
   - "Akciový tovar"
   - "Novinky"
   - "Výpredaj"
   - "Top produkty"

3. **Sezónna kategorizácia:**
   - "Vianočný sortiment"
   - "Letný sortiment"
   - "Grilová sezóna"

4. **Dodávateľská kategorizácia:**
   - "Produkty dodávateľa X"
   - "Vlastná výroba"
   - "Privátna značka"

5. **Zákaznícka kategorizácia:**
   - "Pre vegánov"
   - "Bezlepkové"
   - "Pre diabetikov"
   - "Pre deti"

### Viacnásobnosť

**KRITICKÝ ROZDIEL oproti tovarovým a finančným skupinám:**

- **Tovarová skupina:** Produkt má **max. 1** (povinné)
- **Finančná skupina:** Produkt má **max. 1** (voliteľné)
- **Špecifická skupina:** Produkt môže mať **0-N** (viacnásobné)

**Príklad:**
```
Produkt "Bio mlieko" môže patriť súčasne do:
- "Bio produkty"
- "Slovenské produkty"
- "Top produkty"
```

---

## VZŤAHY S INÝMI TABUĽKAMI

### product_catalog ← product_catalog_categories → product_categories

**Vzťah:** Many-to-Many cez `product_catalog_categories`
- Produkt môže patriť do viacerých špecifických skupín
- Špecifická skupina je jeden typ kategórie (`category_type = 'specific'`)

**Foreign Key:** `category_id` → `product_categories(category_id)` ON DELETE RESTRICT

**UNIQUE Constraint:**
- Pre 'product' a 'financial': UNIQUE(product_id, category_type) - len 1 kategória
- Pre 'specific': **ŽIADNY UNIQUE** - môže byť viac kategórií

---

## VALIDAČNÉ PRAVIDLÁ

### 1. Kategória musí byť typu 'specific'

**Kontrola:** `category_type = 'specific'`

### 2. Nesmie sa zmazať špecifická skupina s produktmi

**Ošetrené:** FK constraint ON DELETE RESTRICT

### 3. Produkt môže mať viac špecifických skupín

**Implementácia:** UNIQUE constraint platí len pre 'product' a 'financial', nie pre 'specific'

### 4. Audit polia (štandard pre všetky tabuľky)

- `created_by`, `created_at` - kto a kedy vytvoril záznam (nemenné)
- `updated_by`, `updated_at` - kto a kedy naposledy modifikoval (aktualizuje sa pri každej zmene)

**Špecifické skupiny majú CrtUser:**
- Na rozdiel od MGLST a FGLST, SGLST má CrtUser/CrtDate/CrtTime
- Tieto sa mapujú na created_by/created_at

---

## PRÍKLADY DÁT

### Príklad 1 - Základné špecifické skupiny

```
category_id=100, type='specific', name='Bio produkty'
category_id=101, type='specific', name='Slovenské produkty'
category_id=102, type='specific', name='Akciový tovar'
category_id=103, type='specific', name='Novinky'
category_id=104, type='specific', name='Top produkty'
category_id=105, type='specific', name='Vianočný sortiment'
category_id=106, type='specific', name='Bezlepkové'
category_id=107, type='specific', name='Pre vegánov'
category_id=108, type='specific', name='Pre diabetikov'
category_id=109, type='specific', name='Privátna značka'
```

### Príklad 2 - Produkt vo viacerých skupinách

**Produkt "Bio mlieko" (product_id=3786):**
```
product_catalog_categories:
  product_id=3786, category_type='specific', category_id=100  -- Bio produkty
  product_id=3786, category_type='specific', category_id=101  -- Slovenské produkty
  product_id=3786, category_type='specific', category_id=104  -- Top produkty
```

### Príklad 3 - Dočasné skupiny (sezónne)

**Vianočný sortiment:**
```
category_id=105, type='specific', name='Vianočný sortiment'
  created_by='admin', created_at='2024-11-01'
  updated_by='admin', updated_at='2025-01-05'
  is_active=FALSE  -- deaktivované po Vianociach
```

---

## HIERARCHIA (BUDÚCNOSŤ)

**V SGLST.BTR nie je pole Parent, ale v product_categories máme `parent_category_id` pre budúcu hierarchiu.**

**Príklad možnej hierarchie:**
```
100 - Bio produkty (parent = NULL)
  ├── 110 - Bio mliečne výrobky (parent = 100)
  ├── 111 - Bio ovocie a zelenina (parent = 100)
  └── 112 - Bio mäso (parent = 100)

105 - Vianočný sortiment (parent = NULL)
  ├── 115 - Vianočné cukrovinky (parent = 105)
  ├── 116 - Vianočné nápoje (parent = 105)
  └── 117 - Vianočné dekorácie (parent = 105)
```

---

## POROVNANIE TROCH TYPOV SKUPÍN

| Vlastnosť | MGLST (Tovarové) | FGLST (Finančné) | SGLST (Špecifické) |
|-----------|------------------|------------------|-------------------|
| **Účel** | Hlavná kategorizácia | Účtovníctvo + kontrola | Vlastná kategorizácia |
| **Hierarchia** | ✅ Má Parent | ❌ Nemá (pridávame) | ❌ Nemá (pridávame) |
| **Popis** | ❌ Nemá | ✅ Describe (150) | ❌ Nemá |
| **Profit Margin** | ✅ Profit | ✅ MinPrf | ❌ Nemá |
| **Max Discount** | ❌ Nemá | ✅ MaxDsc | ❌ Nemá |
| **Viacnásobnosť** | ❌ Produkt má 1 | ❌ Produkt má 1 | ✅ Produkt môže mať viac |
| **Audit created** | ⚠️ Nemá CrtUser | ⚠️ Nemá CrtUser | ✅ Má CrtUser/Date |
| **Audit updated** | ✅ Má ModUser | ✅ Má ModUser | ✅ Má ModUser |
| **Povinnosť** | ✅ Povinná | ⚠️ Voliteľná | ⚠️ Voliteľná |

---

## PRAKTICKÉ POUŽITIE

### 1. E-shop filter (Bio produkty)

Získať všetky bio produkty pre e-shop filter - spojenie cez product_catalog_categories kde category_type='specific'.

### 2. Akciový letáK

Získať všetky produkty v akcii pre tlač letáku - spojenie cez kategóriu "Akciový tovar".

### 3. Multi-filter (Bio + Bezlepkové + Slovenské)

Vyhľadať produkty ktoré spĺňajú všetky 3 podmienky súčasne - použiť GROUP BY + HAVING COUNT.

---

## ÚDRŽBA ŠPECIFICKÝCH SKUPÍN

### Dočasné skupiny (sezónne)

**Deaktivovať po sezóne:**
- Nastaviť `is_active = FALSE` pre "Vianočný sortiment" po Vianociach
- Produkty ostávajú priradené, len sa neobjavia vo filtroch

**Aktivovať pred sezónou:**
- Nastaviť `is_active = TRUE` pred začiatkom sezóny

### Hromadné priradenie

Možnosť hromadne priradiť produkty do špecifickej skupiny na základe kritérií (napr. všetky slovenské mliečne výrobky → "Slovenské produkty").

---

## MIGRAČNÉ POZNÁMKY

### Poradie migrácie

1. Najprv migrovať číselníky kategórií (MGLST, FGLST, SGLST)
2. Potom migrovať produkty (GSCAT)
3. Nakoniec vytvoriť väzby (product_catalog_categories)

### Kontrola po migrácii

- Overiť počet záznamov: SGLST.BTR vs product_categories WHERE category_type='specific'
- Skontrolovať že audit polia sú správne naplnené (CrtUser → created_by)
- Overiť že produkty môžu mať viacero špecifických skupín
- Testovať že nesmie sa zmazať kategória s produktmi

---

## SÚVISIACE DOKUMENTY

- **product_catalog** → `GSCAT-product_catalog.md`
- **product_catalog_categories** → `GSCAT-product_catalog.md` (mapovacia tabuľka)
- **MGLST** (tovarové skupiny) → `MGLST-product_categories.md`
- **FGLST** (finančné skupiny) → `FGLST-product_categories.md`
- **DATABASE_RELATIONSHIPS** → `DATABASE_RELATIONSHIPS.md`

---

**Vytvoril:** Claude & Zoltán  
**Dátum:** 2025-12-10  
**Aktualizované:** 2025-12-15  
**Verzia:** 1.2  
**Status:** ✅ Pripravené na migráciu