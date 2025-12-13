# FGLST.BTR → product_categories (Finančné skupiny)

**Kategória:** Catalogs  
**NEX Genesis:** FGLST.BTR (Zoznam finančných skupín)  
**NEX Automat:** `product_categories` (WHERE category_type = 'financial')  
**Vytvorené:** 2025-12-10  
**Status:** ✅ Finalizované

---

## PREHĽAD

**Stará tabuľka:** FGLST.BTR  
**Nová tabuľka:** `product_categories` (univerzálny číselník)  
**Typ kategórie:** `category_type = 'financial'`  
**Popis:** Finančné skupiny produktov pre účtovníctvo a kontrolu marží/zliav

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

**Poznámka:** `parent_category_id` pridávame aj keď v FGLST.BTR nie je - pre budúcu hierarchiu.

---

## SQL SCHÉMA

### Rozšírenie product_categories pre finančné skupiny

```sql
-- Tabuľka už existuje, pridávame len nové stĺpce
ALTER TABLE product_categories 
    ADD COLUMN IF NOT EXISTS category_description TEXT;
    
ALTER TABLE product_categories 
    ADD COLUMN IF NOT EXISTS max_discount DECIMAL(5,2);
    
ALTER TABLE product_categories 
    ADD COLUMN IF NOT EXISTS min_profit_margin DECIMAL(5,2);

-- Audit polia (už by mali existovať z MGLST, ale pre istotu)
ALTER TABLE product_categories 
    ADD COLUMN IF NOT EXISTS updated_by VARCHAR(30);
    
ALTER TABLE product_categories 
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Index pre popis (full-text search)
CREATE INDEX IF NOT EXISTS idx_product_categories_description ON product_categories 
    USING gin(to_tsvector('slovak', category_description));
```

**Poznámka:** Tieto stĺpce budú používané len pre `category_type = 'financial'`, pre ostatné typy budú NULL.

---

## MIGRAČNÝ SCRIPT

### INSERT do product_categories

```sql
-- Migrácia finančných skupín z FGLST.BTR
INSERT INTO product_categories (
    category_id,
    category_type,
    category_code,
    category_name,
    category_description,
    parent_category_id,
    max_discount,
    min_profit_margin,
    is_active,
    created_by,
    created_at,
    updated_by,
    updated_at
)
SELECT 
    FgCode AS category_id,
    'financial' AS category_type,
    CAST(FgCode AS VARCHAR(20)) AS category_code,
    FgName AS category_name,
    NULLIF(TRIM(Describe), '') AS category_description,
    NULL AS parent_category_id,  -- zatiaľ bez hierarchie
    MaxDsc AS max_discount,
    MinPrf AS min_profit_margin,
    TRUE AS is_active,
    COALESCE(ModUser, 'MIGRATION') AS created_by,
    COALESCE(
        CAST(ModDate AS TIMESTAMP) + CAST(ModTime AS INTERVAL),
        CURRENT_TIMESTAMP
    ) AS created_at,
    COALESCE(ModUser, 'MIGRATION') AS updated_by,
    COALESCE(
        CAST(ModDate AS TIMESTAMP) + CAST(ModTime AS INTERVAL),
        CURRENT_TIMESTAMP
    ) AS updated_at
FROM FGLST
ORDER BY FgCode;
```

**Poznámka:** 
- `ModUser/ModDate/ModTime` sa použijú pre `created_by/created_at` aj `updated_by/updated_at`
- Ak ModUser neexistuje, použije sa 'MIGRATION'

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

### Príklad použitia

```sql
-- Produkt má finančnú skupinu "Potraviny - DPH 10%"
-- Finančná skupina má: min_profit_margin = 15%, max_discount = 10%

-- Validácia pri zadávaní ceny:
IF (calculated_margin < 15.0) THEN
    RAISE WARNING 'Marža % je nižšia ako minimálna povolená 15%', calculated_margin;
END IF;

-- Validácia pri zadávaní zľavy:
IF (discount_percent > 10.0) THEN
    RAISE WARNING 'Zľava % prekračuje maximálnu povolenú 10%', discount_percent;
END IF;
```

---

## VZŤAHY S INÝMI TABUĽKAMI

### product_catalog ← product_catalog_categories → product_categories

```sql
-- Získať produkty v danej finančnej skupine
SELECT p.*
FROM product_catalog p
INNER JOIN product_catalog_categories pcc ON p.product_id = pcc.product_id
INNER JOIN product_categories pc ON pcc.category_id = pc.category_id
WHERE pc.category_type = 'financial'
  AND pc.category_id = ?;
```

```sql
-- Získať finančnú skupinu produktu
SELECT 
    pc.category_name,
    pc.category_description,
    pc.max_discount,
    pc.min_profit_margin
FROM product_categories pc
INNER JOIN product_catalog_categories pcc ON pc.category_id = pcc.category_id
WHERE pcc.product_id = ?
  AND pcc.category_type = 'financial';
```

```sql
-- Validovať maržu produktu
SELECT 
    p.product_name,
    p.unit_price - p.purchase_price AS margin_amount,
    ((p.unit_price - p.purchase_price) / NULLIF(p.purchase_price, 0)) * 100 AS margin_percent,
    pc.min_profit_margin,
    CASE 
        WHEN ((p.unit_price - p.purchase_price) / NULLIF(p.purchase_price, 0)) * 100 < pc.min_profit_margin 
        THEN 'WARNING: Margin too low!'
        ELSE 'OK'
    END AS validation_status
FROM product_catalog p
INNER JOIN product_catalog_categories pcc ON p.product_id = pcc.product_id
INNER JOIN product_categories pc ON pcc.category_id = pc.category_id
WHERE pc.category_type = 'financial'
  AND p.product_id = ?;
```

---

## VALIDAČNÉ PRAVIDLÁ

### 1. Kategória musí byť typu 'financial'
```sql
CHECK (category_type = 'financial')
```

### 2. Marža a zľava musia byť v rozumných medziach
```sql
-- Trigger pre validáciu
CREATE OR REPLACE FUNCTION validate_financial_margins()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.category_type = 'financial' THEN
        IF NEW.min_profit_margin IS NOT NULL AND (NEW.min_profit_margin < 0 OR NEW.min_profit_margin > 100) THEN
            RAISE EXCEPTION 'min_profit_margin must be between 0 and 100';
        END IF;
        
        IF NEW.max_discount IS NOT NULL AND (NEW.max_discount < 0 OR NEW.max_discount > 100) THEN
            RAISE EXCEPTION 'max_discount must be between 0 and 100';
        END IF;
        
        -- Logická kontrola: zľava by nemala byť väčšia ako marža
        IF NEW.min_profit_margin IS NOT NULL AND NEW.max_discount IS NOT NULL THEN
            IF NEW.max_discount >= NEW.min_profit_margin THEN
                RAISE WARNING 'max_discount (%) is >= min_profit_margin (%) - profit may be negative!', 
                    NEW.max_discount, NEW.min_profit_margin;
            END IF;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_financial_margins
    BEFORE INSERT OR UPDATE ON product_categories
    FOR EACH ROW
    EXECUTE FUNCTION validate_financial_margins();
```

### 3. Nesmie sa zmazať finančná skupina s produktmi
```sql
-- Už je ošetrené cez FK constraint:
-- product_catalog_categories.category_id → product_categories.category_id ON DELETE RESTRICT
```

---

## QUERY PATTERNS

### Získať všetky finančné skupiny
```sql
SELECT 
    category_id,
    category_code,
    category_name,
    category_description,
    max_discount,
    min_profit_margin,
    updated_by,
    updated_at
FROM product_categories
WHERE category_type = 'financial'
  AND is_active = TRUE
ORDER BY category_name;
```

### Full-text vyhľadávanie v popise
```sql
SELECT 
    category_name,
    category_description,
    ts_rank(to_tsvector('slovak', category_description), query) AS rank
FROM product_categories,
     to_tsquery('slovak', 'potraviny & dph') AS query
WHERE category_type = 'financial'
  AND to_tsvector('slovak', category_description) @@ query
ORDER BY rank DESC;
```

### Zoznam produktov s nízkou maržou
```sql
SELECT 
    p.product_id,
    p.product_name,
    p.unit_price,
    p.purchase_price,
    ((p.unit_price - p.purchase_price) / NULLIF(p.purchase_price, 0)) * 100 AS actual_margin,
    pc.min_profit_margin,
    pc.category_name AS financial_group
FROM product_catalog p
INNER JOIN product_catalog_categories pcc ON p.product_id = pcc.product_id
INNER JOIN product_categories pc ON pcc.category_id = pc.category_id
WHERE pc.category_type = 'financial'
  AND ((p.unit_price - p.purchase_price) / NULLIF(p.purchase_price, 0)) * 100 < pc.min_profit_margin
ORDER BY actual_margin ASC;
```

### Štatistika marží podľa finančných skupín
```sql
SELECT 
    pc.category_name,
    COUNT(p.product_id) AS product_count,
    AVG(((p.unit_price - p.purchase_price) / NULLIF(p.purchase_price, 0)) * 100) AS avg_margin,
    MIN(((p.unit_price - p.purchase_price) / NULLIF(p.purchase_price, 0)) * 100) AS min_margin,
    MAX(((p.unit_price - p.purchase_price) / NULLIF(p.purchase_price, 0)) * 100) AS max_margin,
    pc.min_profit_margin AS required_margin
FROM product_categories pc
INNER JOIN product_catalog_categories pcc ON pc.category_id = pcc.category_id
INNER JOIN product_catalog p ON pcc.product_id = p.product_id
WHERE pc.category_type = 'financial'
  AND p.purchase_price > 0
GROUP BY pc.category_id, pc.category_name, pc.min_profit_margin
ORDER BY pc.category_name;
```

---

## PRÍKLAD DÁT

```sql
-- Finančné skupiny
INSERT INTO product_categories (category_id, category_type, category_code, category_name, category_description, max_discount, min_profit_margin, created_by, created_at, updated_by, updated_at) VALUES
(10, 'financial', '10', 'Potraviny - DPH 10%', 'Základné potraviny so zníženou sadzbou DPH 10%', 10.00, 15.00, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00'),
(20, 'financial', '20', 'Potraviny - DPH 20%', 'Potraviny so základnou sadzbou DPH 20%', 15.00, 20.00, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00'),
(30, 'financial', '30', 'Nápoje alkoholické', 'Alkoholické nápoje s DPH 20% a spotrebnou daňou', 5.00, 40.00, 'admin', '2025-01-01 10:00:00', 'manager', '2025-02-15 14:30:00'),
(40, 'financial', '40', 'Drogéria', 'Drogéria a kozmetika s DPH 20%', 20.00, 35.00, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00'),
(50, 'financial', '50', 'Lieky', 'Lieky a zdravotnícke pomôcky s DPH 10%', 0.00, 10.00, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00');
```

**Poznámka k príkladu:**
- Lieky majú `max_discount = 0%` (zákaz zliav na lieky)
- Alkohol má vyššiu minimálnu maržu (40%) kvôli spotrebnej dani
- Potraviny majú rôzne skupiny podľa DPH sadzby
- Alkoholické nápoje boli modifikované neskôr (updated_by = 'manager', updated_at = 2025-02-15)

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

**Ak v budúcnosti bude potreba hierarchie, stačí aktualizovať `parent_category_id`:**
```sql
UPDATE product_categories 
SET parent_category_id = 10,
    updated_by = 'admin',
    updated_at = CURRENT_TIMESTAMP
WHERE category_id IN (11, 12);
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

```sql
-- Rozšírenie product_categories (voliteľné)
ALTER TABLE product_categories 
    ADD COLUMN IF NOT EXISTS account_number VARCHAR(10);

-- Príklad
UPDATE product_categories 
SET account_number = '604.001',
    updated_by = 'admin',
    updated_at = CURRENT_TIMESTAMP
WHERE category_type = 'financial' 
  AND category_id = 10;  -- Potraviny - DPH 10%
```

**Použitie pri zaúčtovaní:**
```sql
-- Pri vytváraní účtovného zápisu z faktúry
SELECT 
    pc.account_number,
    SUM(ii.line_total) AS amount
FROM invoice_items ii
INNER JOIN product_catalog p ON ii.product_id = p.product_id
INNER JOIN product_catalog_categories pcc ON p.product_id = pcc.product_id
INNER JOIN product_categories pc ON pcc.category_id = pc.category_id
WHERE ii.invoice_id = ?
  AND pcc.category_type = 'financial'
GROUP BY pc.account_number;
```

---

## SÚVISIACE DOKUMENTY

- **product_catalog** → `GSCAT-product_catalog.md`
- **product_catalog_categories** → `GSCAT-product_catalog.md` (mapovacia tabuľka)
- **DATABASE_RELATIONSHIPS** → `DATABASE_RELATIONSHIPS.md`
- **MGLST** (tovarové skupiny) → `MGLST-product_categories.md`
- **SGLST** (špecifické skupiny) → `SGLST-product_categories.md` (ďalší dokument)
- **chart_of_accounts** (účtová osnova) → `accounting/CHART_OF_ACCOUNTS.md`

---

**Vytvoril:** Claude & Zoltán  
**Dátum:** 2025-12-10  
**Verzia:** 1.1  
**Status:** ✅ Schválené - aktualizované audit polia