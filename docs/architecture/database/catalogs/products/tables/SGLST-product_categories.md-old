# SGLST.BTR → product_categories (Špecifické skupiny)

**Kategória:** Catalogs  
**NEX Genesis:** SGLST.BTR (Zoznam špecifikačných skupín)  
**NEX Automat:** `product_categories` (WHERE category_type = 'specific')  
**Vytvorené:** 2025-12-10  
**Status:** ✅ Finalizované

---

## PREHĽAD

**Stará tabuľka:** SGLST.BTR  
**Nová tabuľka:** `product_categories` (univerzálny číselník)  
**Typ kategórie:** `category_type = 'specific'`  
**Popis:** Špecifické skupiny produktov pre vlastnú kategorizáciu zákazníka

---

## KOMPLETNÁ ŠTRUKTÚRA TABUĽKY product_categories

**Tabuľka `product_categories` je UNIVERZÁLNY číselník pre všetky 3 typy kategórií:**
- `category_type = 'product'` - Tovarové skupiny (MGLST.BTR)
- `category_type = 'financial'` - Finančné skupiny (FGLST.BTR)
- `category_type = 'specific'` - Špecifické skupiny (SGLST.BTR) ← **tento dokument**

### SQL CREATE TABLE

```sql
CREATE TABLE product_categories (
    -- Základné polia (všetky typy)
    category_id SERIAL PRIMARY KEY,
    category_type VARCHAR(20) NOT NULL CHECK (category_type IN ('product', 'financial', 'specific')),
    category_code VARCHAR(20) UNIQUE NOT NULL,
    category_name VARCHAR(100) NOT NULL,
    parent_category_id INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_by VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(30),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Polia pre tovarové skupiny (MGLST)
    profit_margin DECIMAL(5,2),  -- Doporučený zisk predaja (%)
    
    -- Polia pre finančné skupiny (FGLST)
    category_description TEXT,  -- Podrobný popis
    max_discount DECIMAL(5,2),  -- Maximálna zľava (%)
    min_profit_margin DECIMAL(5,2),  -- Minimálna marža (%)
    
    -- Väzba na účtovnú osnovu (voliteľné)
    account_number VARCHAR(10),
    
    FOREIGN KEY (parent_category_id) REFERENCES product_categories(category_id) ON DELETE RESTRICT
);

CREATE INDEX idx_product_categories_type ON product_categories(category_type);
CREATE INDEX idx_product_categories_code ON product_categories(category_code);
CREATE INDEX idx_product_categories_parent ON product_categories(parent_category_id);
CREATE INDEX idx_product_categories_active ON product_categories(is_active);
CREATE INDEX idx_product_categories_description ON product_categories USING gin(to_tsvector('slovak', category_description));
```

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

**Poznámka:** `parent_category_id` pridávame pre budúcu hierarchiu, aj keď v SGLST.BTR nie je.

---

## MIGRAČNÝ SCRIPT

### INSERT do product_categories

```sql
-- Migrácia špecifických skupín z SGLST.BTR
INSERT INTO product_categories (
    category_id,
    category_type,
    category_code,
    category_name,
    parent_category_id,
    is_active,
    created_by,
    created_at,
    updated_by,
    updated_at
)
SELECT 
    SgCode AS category_id,
    'specific' AS category_type,
    CAST(SgCode AS VARCHAR(20)) AS category_code,
    SgName AS category_name,
    NULL AS parent_category_id,  -- zatiaľ bez hierarchie
    TRUE AS is_active,
    COALESCE(CrtUser, 'MIGRATION') AS created_by,
    COALESCE(
        CAST(CrtDate AS TIMESTAMP) + CAST(CrtTime AS INTERVAL),
        CURRENT_TIMESTAMP
    ) AS created_at,
    COALESCE(ModUser, CrtUser, 'MIGRATION') AS updated_by,
    COALESCE(
        CAST(ModDate AS TIMESTAMP) + CAST(ModTime AS INTERVAL),
        CAST(CrtDate AS TIMESTAMP) + CAST(CrtTime AS INTERVAL),
        CURRENT_TIMESTAMP
    ) AS updated_at
FROM SGLST
ORDER BY SgCode;
```

**Poznámka:** 
- `CrtUser/CrtDate/CrtTime` sa použijú pre `created_by/created_at`
- `ModUser/ModDate/ModTime` sa použijú pre `updated_by/updated_at`
- Ak ModUser neexistuje, použije sa CrtUser
- Ak ani CrtUser neexistuje, použije sa 'MIGRATION'

---

## AUTOMATICKÁ AKTUALIZÁCIA updated_at

### Trigger pre automatickú aktualizáciu

**Funkcia:**
```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

**Trigger:**
```sql
-- Tento trigger je spoločný pre všetky typy kategórií
CREATE TRIGGER update_product_categories_updated_at
    BEFORE UPDATE ON product_categories
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

**Vysvetlenie:**
- Pri každom UPDATE sa automaticky nastaví `updated_at = CURRENT_TIMESTAMP`
- `updated_by` sa musí nastaviť manuálne v aplikácii (user context)
- Toto je štandardný pattern pre všetky tabuľky NEX Automat

---

## POLIA KTORÉ SA NEPRENÁŠAJÚ

**Dôvod:** Zastarané, nepoužité alebo nahradené lepším riešením

| NEX Genesis | Typ | Dôvod neprenášania |
|-------------|-----|--------------------|
| _SgName | Str50 | Vyhľadávacie pole - PostgreSQL full-text search |

**Poznámka:** ModUser/ModDate/ModTime sa prenášajú ako updated_by/updated_at (viď mapping tabuľka vyššie).

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

---

## VZŤAHY S INÝMI TABUĽKAMI

### product_catalog ← product_catalog_categories → product_categories

```sql
-- Získať produkty v danej špecifickej skupine
SELECT p.*
FROM product_catalog p
INNER JOIN product_catalog_categories pcc ON p.product_id = pcc.product_id
INNER JOIN product_categories pc ON pcc.category_id = pc.category_id
WHERE pc.category_type = 'specific'
  AND pc.category_id = ?;
```

```sql
-- Získať špecifickú skupinu produktu
SELECT pc.*
FROM product_categories pc
INNER JOIN product_catalog_categories pcc ON pc.category_id = pcc.category_id
WHERE pcc.product_id = ?
  AND pcc.category_type = 'specific';
```

```sql
-- Produkt môže patriť do VIACERÝCH špecifických skupín súčasne
-- (na rozdiel od tovarovej a finančnej skupiny kde je len 1)
SELECT 
    p.product_name,
    STRING_AGG(pc.category_name, ', ' ORDER BY pc.category_name) AS specific_groups
FROM product_catalog p
INNER JOIN product_catalog_categories pcc ON p.product_id = pcc.product_id
INNER JOIN product_categories pc ON pcc.category_id = pc.category_id
WHERE pc.category_type = 'specific'
  AND p.product_id = ?
GROUP BY p.product_id, p.product_name;
```

---

## VALIDAČNÉ PRAVIDLÁ

### 1. Kategória musí byť typu 'specific'
```sql
CHECK (category_type = 'specific')
```

### 2. Nesmie sa zmazať špecifická skupina s produktmi
```sql
-- Už je ošetrené cez FK constraint:
-- product_catalog_categories.category_id → product_categories.category_id ON DELETE RESTRICT
```

### 3. Produkt môže mať viac špecifických skupín
```sql
-- Na rozdiel od 'product' a 'financial' kde je UNIQUE(product_id, category_type),
-- špecifické skupiny môžu byť viacnásobné

-- Kontrola pri INSERT do product_catalog_categories:
-- Pre category_type = 'specific' -> povoliť viac záznamov pre jeden product_id
```

**Poznámka:** Ak chceme povoliť viac špecifických skupín, musíme upraviť UNIQUE constraint:

```sql
-- Pôvodný constraint (jeden typ kategórie = jedna kategória)
-- UNIQUE(product_id, category_type)  -- príliš reštriktívne!

-- Upravený constraint (povoliť viac specific skupín)
CREATE UNIQUE INDEX idx_product_catalog_categories_unique 
    ON product_catalog_categories (product_id, category_type)
    WHERE category_type IN ('product', 'financial');

-- Pre 'specific' nie je UNIQUE constraint -> môže byť viac skupín
```

---

## QUERY PATTERNS

### Získať všetky špecifické skupiny
```sql
SELECT 
    category_id,
    category_code,
    category_name,
    created_by,
    created_at,
    updated_by,
    updated_at
FROM product_categories
WHERE category_type = 'specific'
  AND is_active = TRUE
ORDER BY category_name;
```

### Produkty v špecifickej skupine
```sql
SELECT 
    p.product_id,
    p.product_name,
    p.product_type,
    p.unit_name
FROM product_catalog p
INNER JOIN product_catalog_categories pcc ON p.product_id = pcc.product_id
INNER JOIN product_categories pc ON pcc.category_id = pc.category_id
WHERE pc.category_type = 'specific'
  AND pc.category_name = 'Bio produkty'
ORDER BY p.product_name;
```

### Všetky špecifické skupiny produktu
```sql
SELECT 
    pc.category_name,
    pc.category_code,
    pc.updated_by,
    pc.updated_at
FROM product_categories pc
INNER JOIN product_catalog_categories pcc ON pc.category_id = pcc.category_id
WHERE pcc.product_id = ?
  AND pcc.category_type = 'specific'
ORDER BY pc.category_name;
```

### Štatistika produktov podľa špecifických skupín
```sql
SELECT 
    pc.category_name,
    COUNT(pcc.product_id) AS product_count,
    COUNT(DISTINCT CASE WHEN p.is_disabled = FALSE THEN p.product_id END) AS active_products,
    COUNT(DISTINCT CASE WHEN p.is_disabled = TRUE THEN p.product_id END) AS disabled_products
FROM product_categories pc
LEFT JOIN product_catalog_categories pcc ON pc.category_id = pcc.category_id
LEFT JOIN product_catalog p ON pcc.product_id = p.product_id
WHERE pc.category_type = 'specific'
GROUP BY pc.category_id, pc.category_name
ORDER BY product_count DESC;
```

### Produkty bez špecifickej skupiny
```sql
SELECT 
    p.product_id,
    p.product_name
FROM product_catalog p
WHERE NOT EXISTS (
    SELECT 1 
    FROM product_catalog_categories pcc
    INNER JOIN product_categories pc ON pcc.category_id = pc.category_id
    WHERE pcc.product_id = p.product_id
      AND pcc.category_type = 'specific'
)
ORDER BY p.product_name;
```

---

## PRÍKLAD DÁT

```sql
-- Špecifické skupiny
INSERT INTO product_categories (category_id, category_type, category_code, category_name, created_by, created_at, updated_by, updated_at) VALUES
(100, 'specific', '100', 'Bio produkty', 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00'),
(101, 'specific', '101', 'Slovenské produkty', 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00'),
(102, 'specific', '102', 'Akciový tovar', 'admin', '2025-01-01 10:00:00', 'manager', '2025-02-15 14:30:00'),
(103, 'specific', '103', 'Novinky', 'admin', '2025-01-01 10:00:00', 'manager', '2025-03-10 09:15:00'),
(104, 'specific', '104', 'Top produkty', 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00'),
(105, 'specific', '105', 'Vianočný sortiment', 'admin', '2024-11-01 08:00:00', 'admin', '2025-01-05 16:00:00'),
(106, 'specific', '106', 'Bezlepkové', 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00'),
(107, 'specific', '107', 'Pre vegánov', 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00'),
(108, 'specific', '108', 'Pre diabetikov', 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00'),
(109, 'specific', '109', 'Privátna značka', 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00');
```

**Poznámka k príkladu:**
- Niektoré skupiny boli modifikované neskôr (Akciový tovar, Novinky, Vianočný sortiment)
- Vianočný sortiment bol vytvorený v novembri a deaktivovaný začiatkom januára

**Príklad použitia:**
```sql
-- Produkt "Bio mlieko" patrí do viacerých špecifických skupín
INSERT INTO product_catalog_categories (product_id, category_type, category_id) VALUES
(3786, 'specific', 100),  -- Bio produkty
(3786, 'specific', 101),  -- Slovenské produkty
(3786, 'specific', 104);  -- Top produkty
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

**Ak v budúcnosti bude potreba hierarchie:**
```sql
UPDATE product_categories 
SET parent_category_id = 100,
    updated_by = 'admin',
    updated_at = CURRENT_TIMESTAMP
WHERE category_id IN (110, 111, 112);
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
```sql
SELECT DISTINCT p.*
FROM product_catalog p
INNER JOIN product_catalog_categories pcc ON p.product_id = pcc.product_id
INNER JOIN product_categories pc ON pcc.category_id = pc.category_id
WHERE pc.category_type = 'specific'
  AND pc.category_name = 'Bio produkty'
  AND p.is_disabled = FALSE
ORDER BY p.product_name;
```

### 2. Akciový letáK
```sql
SELECT 
    p.product_name,
    p.unit_price,
    p.unit_name,
    pt.text AS extended_name
FROM product_catalog p
INNER JOIN product_catalog_categories pcc ON p.product_id = pcc.product_id
INNER JOIN product_categories pc ON pcc.category_id = pc.category_id
LEFT JOIN product_catalog_texts pt ON p.product_id = pt.product_id AND pt.text_type = 'extended_name'
WHERE pc.category_type = 'specific'
  AND pc.category_name = 'Akciový tovar'
ORDER BY p.product_name;
```

### 3. Multi-filter (Bio + Bezlepkové + Slovenské)
```sql
SELECT p.*
FROM product_catalog p
WHERE p.product_id IN (
    SELECT pcc.product_id
    FROM product_catalog_categories pcc
    INNER JOIN product_categories pc ON pcc.category_id = pc.category_id
    WHERE pc.category_type = 'specific'
      AND pc.category_name IN ('Bio produkty', 'Bezlepkové', 'Slovenské produkty')
    GROUP BY pcc.product_id
    HAVING COUNT(DISTINCT pc.category_name) = 3  -- všetky 3 podmienky
);
```

---

## ÚDRŽBA ŠPECIFICKÝCH SKUPÍN

### Dočasné skupiny (sezónne)
```sql
-- Deaktivovať vianočný sortiment po Vianociach
UPDATE product_categories 
SET is_active = FALSE,
    updated_by = 'admin',
    updated_at = CURRENT_TIMESTAMP
WHERE category_type = 'specific' 
  AND category_name = 'Vianočný sortiment';

-- Aktivovať pred sezónou
UPDATE product_categories 
SET is_active = TRUE,
    updated_by = 'admin',
    updated_at = CURRENT_TIMESTAMP
WHERE category_type = 'specific' 
  AND category_name = 'Vianočný sortiment';
```

### Hromadné priradenie
```sql
-- Všetky slovenské mliečne výrobky → Slovenské produkty
INSERT INTO product_catalog_categories (product_id, category_type, category_id)
SELECT DISTINCT 
    p.product_id,
    'specific' AS category_type,
    101 AS category_id  -- Slovenské produkty
FROM product_catalog p
INNER JOIN product_catalog_categories pcc1 ON p.product_id = pcc1.product_id
INNER JOIN product_categories pc1 ON pcc1.category_id = pc1.category_id
INNER JOIN product_catalog_partners pcp ON p.product_id = pcp.product_id
INNER JOIN partner_catalog part ON pcp.partner_id = part.partner_id
WHERE pc1.category_type = 'product'
  AND pc1.category_name = 'Mliečne výrobky'
  AND part.country_code = 'SK'
  AND NOT EXISTS (
      SELECT 1 FROM product_catalog_categories pcc2
      WHERE pcc2.product_id = p.product_id
        AND pcc2.category_type = 'specific'
        AND pcc2.category_id = 101
  );
```

---

## SÚVISIACE DOKUMENTY

- **product_catalog** → `GSCAT-product_catalog.md`
- **product_catalog_categories** → `GSCAT-product_catalog.md` (mapovacia tabuľka)
- **DATABASE_RELATIONSHIPS** → `DATABASE_RELATIONSHIPS.md`
- **MGLST** (tovarové skupiny) → `MGLST-product_categories.md`
- **FGLST** (finančné skupiny) → `FGLST-product_categories.md`
- **PAB** (partneri) → `PAB-partner_catalog.md` (ďalší dokument)

---

**Vytvoril:** Claude & Zoltán  
**Dátum:** 2025-12-10  
**Verzia:** 1.1  
**Status:** ✅ Schválené - aktualizované audit polia