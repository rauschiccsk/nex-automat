# MGLST.BTR → product_categories (Tovarové skupiny)

**Kategória:** Catalogs  
**NEX Genesis:** MGLST.BTR (Zoznam tovarových skupín)  
**NEX Automat:** `product_categories` (WHERE category_type = 'product')  
**Vytvorené:** 2025-12-10  
**Status:** ✅ Finalizované

---

## PREHĽAD

**Stará tabuľka:** MGLST.BTR  
**Nová tabuľka:** `product_categories` (univerzálny číselník)  
**Typ kategórie:** `category_type = 'product'`  
**Popis:** Hierarchická štruktúra tovarových skupín s doporučeným ziskom

---

## KOMPLETNÁ ŠTRUKTÚRA TABUĽKY product_categories

**Tabuľka `product_categories` je UNIVERZÁLNY číselník pre všetky 3 typy kategórií:**
- `category_type = 'product'` - Tovarové skupiny (MGLST.BTR) ← **tento dokument**
- `category_type = 'financial'` - Finančné skupiny (FGLST.BTR)
- `category_type = 'specific'` - Špecifické skupiny (SGLST.BTR)

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
| ModUser | Str8 | updated_by | VARCHAR(20) | Kto naposledy modifikoval |
| ModDate | DateType | updated_at | TIMESTAMP | Kedy naposledy modifikované |
| ModTime | TimeType | updated_at | TIMESTAMP | Kedy naposledy modifikované |

### Dodatočné polia (nové v NEX Automat)

| NEX Automat | Typ | Popis | Hodnota |
|-------------|-----|-------|---------|
| category_type | VARCHAR(20) | Typ kategórie | 'product' (fixed) |
| category_code | VARCHAR(20) | Alfanumerický kód | MgCode (string) |
| is_active | BOOLEAN | Aktívna skupina | TRUE |
| created_by | VARCHAR(50) | Kto vytvoril | NULL alebo ModUser |
| created_at | TIMESTAMP | Dátum vytvorenia | CURRENT_TIMESTAMP |

---

## MIGRAČNÝ SCRIPT

### INSERT do product_categories

```sql
-- Migrácia tovarových skupín z MGLST.BTR
INSERT INTO product_categories (
    category_id,
    category_type,
    category_code,
    category_name,
    parent_category_id,
    profit_margin,
    is_active,
    created_by,
    created_at,
    updated_by,
    updated_at
)
SELECT 
    MgCode AS category_id,
    'product' AS category_type,
    CAST(MgCode AS VARCHAR(20)) AS category_code,
    MgName AS category_name,
    CASE WHEN Parent = 0 THEN NULL ELSE Parent END AS parent_category_id,
    Profit AS profit_margin,
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
FROM MGLST
ORDER BY MgCode;
```

**Poznámka:** 
- `Parent = 0` sa transformuje na `NULL` (hlavná skupina nemá rodiča)
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

**SQL Query - celá hierarchia:**
```sql
WITH RECURSIVE category_tree AS (
    -- Hlavné skupiny
    SELECT 
        category_id,
        category_code,
        category_name,
        parent_category_id,
        profit_margin,
        0 AS level,
        category_name AS path
    FROM product_categories
    WHERE category_type = 'product'
      AND parent_category_id IS NULL
    
    UNION ALL
    
    -- Podskupiny
    SELECT 
        c.category_id,
        c.category_code,
        c.category_name,
        c.parent_category_id,
        c.profit_margin,
        ct.level + 1,
        ct.path || ' > ' || c.category_name
    FROM product_categories c
    INNER JOIN category_tree ct ON c.parent_category_id = ct.category_id
    WHERE c.category_type = 'product'
)
SELECT * FROM category_tree
ORDER BY path;
```

---

### Doporučený zisk (Profit Margin)

**Použitie:**
- Automatický výpočet predajnej ceny z nákupnej
- Predajná cena = Nákupná cena × (1 + profit_margin / 100)
- Príklad: profit_margin = 25% → predajná cena = nákupná × 1.25

**Aplikácia:**
1. Produkt má priradené `product_catalog_categories` s `category_type = 'product'`
2. Z tejto kategórie sa načíta `profit_margin`
3. Ak produkt nemá priradené, použije sa profit_margin z nadriadenej skupiny
4. Ak ani tam nie je, použije se systémový default

---

## VZŤAHY S INÝMI TABUĽKAMI

### product_catalog ← product_catalog_categories → product_categories

```sql
-- Získať produkty v danej tovarovej skupine
SELECT p.*
FROM product_catalog p
INNER JOIN product_catalog_categories pcc ON p.product_id = pcc.product_id
INNER JOIN product_categories pc ON pcc.category_id = pc.category_id
WHERE pc.category_type = 'product'
  AND pc.category_id = ?;
```

```sql
-- Získať tovarovú skupinu produktu
SELECT pc.*
FROM product_categories pc
INNER JOIN product_catalog_categories pcc ON pc.category_id = pcc.category_id
WHERE pcc.product_id = ?
  AND pcc.category_type = 'product';
```

```sql
-- Získať všetky produkty vrátane podskupín
WITH RECURSIVE subcategories AS (
    -- Hlavná skupina
    SELECT category_id
    FROM product_categories
    WHERE category_type = 'product'
      AND category_id = ?
    
    UNION ALL
    
    -- Podskupiny
    SELECT c.category_id
    FROM product_categories c
    INNER JOIN subcategories s ON c.parent_category_id = s.category_id
    WHERE c.category_type = 'product'
)
SELECT DISTINCT p.*
FROM product_catalog p
INNER JOIN product_catalog_categories pcc ON p.product_id = pcc.product_id
WHERE pcc.category_id IN (SELECT category_id FROM subcategories)
  AND pcc.category_type = 'product';
```

---

## VALIDAČNÉ PRAVIDLÁ

### 1. Kategória musí byť typu 'product'
```sql
CHECK (category_type = 'product')
```

### 2. Parent nesmie vytvoriť cyklus
```sql
-- Aplikačná logika - kontrola pred INSERT/UPDATE
-- Najskôr získaj všetkých predkov:
WITH RECURSIVE ancestors AS (
    SELECT parent_category_id, 1 AS depth
    FROM product_categories
    WHERE category_id = :new_category_id
    
    UNION ALL
    
    SELECT c.parent_category_id, a.depth + 1
    FROM product_categories c
    INNER JOIN ancestors a ON c.category_id = a.parent_category_id
    WHERE a.depth < 100  -- ochrana pred nekonečnou slučkou
)
SELECT COUNT(*) FROM ancestors
WHERE parent_category_id = :new_parent_id;  -- ak > 0 → cyklus!
```

### 3. Parent musí byť rovnakého typu
```sql
-- Trigger pre validáciu
CREATE OR REPLACE FUNCTION validate_category_parent()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.parent_category_id IS NOT NULL THEN
        IF NOT EXISTS (
            SELECT 1 FROM product_categories
            WHERE category_id = NEW.parent_category_id
              AND category_type = NEW.category_type
        ) THEN
            RAISE EXCEPTION 'Parent category must be of the same type';
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_category_parent
    BEFORE INSERT OR UPDATE ON product_categories
    FOR EACH ROW
    EXECUTE FUNCTION validate_category_parent();
```

### 4. Nesmie sa zmazať kategória s produktmi
```sql
-- Už je ošetrené cez FK constraint:
-- product_catalog_categories.category_id → product_categories.category_id ON DELETE RESTRICT
```

### 5. Nesmie sa zmazať kategória s podskupinami
```sql
-- Už je ošetrené cez self-reference:
-- product_categories.parent_category_id → product_categories.category_id ON DELETE RESTRICT
```

---

## QUERY PATTERNS

### Získať celú hierarchiu skupín
```sql
WITH RECURSIVE category_tree AS (
    SELECT 
        category_id,
        category_name,
        parent_category_id,
        profit_margin,
        0 AS level
    FROM product_categories
    WHERE category_type = 'product'
      AND parent_category_id IS NULL
    
    UNION ALL
    
    SELECT 
        c.category_id,
        c.category_name,
        c.parent_category_id,
        c.profit_margin,
        ct.level + 1
    FROM product_categories c
    INNER JOIN category_tree ct ON c.parent_category_id = ct.category_id
    WHERE c.category_type = 'product'
)
SELECT 
    REPEAT('  ', level) || category_name AS hierarchy,
    category_id,
    profit_margin
FROM category_tree
ORDER BY hierarchy;
```

### Získať breadcrumb (cestu) ku kategórii
```sql
WITH RECURSIVE breadcrumb AS (
    SELECT 
        category_id,
        category_name,
        parent_category_id,
        1 AS level
    FROM product_categories
    WHERE category_id = ?
    
    UNION ALL
    
    SELECT 
        c.category_id,
        c.category_name,
        c.parent_category_id,
        b.level + 1
    FROM product_categories c
    INNER JOIN breadcrumb b ON c.category_id = b.parent_category_id
)
SELECT 
    category_name,
    level
FROM breadcrumb
ORDER BY level DESC;
-- Výsledok: "Potraviny > Mliečne výrobky > Syry"
```

### Počet produktov v skupine (vrátane podskupín)
```sql
WITH RECURSIVE subcategories AS (
    SELECT category_id
    FROM product_categories
    WHERE category_type = 'product'
      AND category_id = ?
    
    UNION ALL
    
    SELECT c.category_id
    FROM product_categories c
    INNER JOIN subcategories s ON c.parent_category_id = s.category_id
)
SELECT COUNT(DISTINCT p.product_id)
FROM product_catalog p
INNER JOIN product_catalog_categories pcc ON p.product_id = pcc.product_id
WHERE pcc.category_id IN (SELECT category_id FROM subcategories)
  AND pcc.category_type = 'product';
```

---

## PRÍKLAD DÁT

```sql
-- Hlavné skupiny
INSERT INTO product_categories (category_id, category_type, category_code, category_name, parent_category_id, profit_margin, created_by, created_at, updated_by, updated_at) VALUES
(1000, 'product', '1000', 'Potraviny', NULL, 25.00, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00'),
(2000, 'product', '2000', 'Nápoje', NULL, 30.00, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00'),
(3000, 'product', '3000', 'Drogéria', NULL, 35.00, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00');

-- Podskupiny
INSERT INTO product_categories (category_id, category_type, category_code, category_name, parent_category_id, profit_margin, created_by, created_at, updated_by, updated_at) VALUES
(1100, 'product', '1100', 'Mliečne výrobky', 1000, 20.00, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00'),
(1200, 'product', '1200', 'Pečivo', 1000, 15.00, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00'),
(2100, 'product', '2100', 'Nealkoholické', 2000, 28.00, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00'),
(2200, 'product', '2200', 'Alkoholické', 2000, 40.00, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00');

-- Podpodskupiny
INSERT INTO product_categories (category_id, category_type, category_code, category_name, parent_category_id, profit_margin, created_by, created_at, updated_by, updated_at) VALUES
(1110, 'product', '1110', 'Mlieko', 1100, 18.00, 'admin', '2025-01-01 10:00:00', 'operator', '2025-02-15 14:30:00'),
(1120, 'product', '1120', 'Syry', 1100, 22.00, 'admin', '2025-01-01 10:00:00', 'operator', '2025-02-20 09:15:00'),
(1210, 'product', '1210', 'Chlieb', 1200, 12.00, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00'),
(2110, 'product', '2110', 'Minerálne vody', 2100, 25.00, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00');
```

**Poznámka:** V príkladoch vidíme že niektoré záznamy boli modifikované neskôr (updated_by = 'operator', updated_at = 2025-02-15).

---

## SÚVISIACE DOKUMENTY

- **product_catalog** → `GSCAT-product_catalog.md`
- **product_catalog_categories** → `GSCAT-product_catalog.md` (mapovacia tabuľka)
- **DATABASE_RELATIONSHIPS** → `DATABASE_RELATIONSHIPS.md`
- **FGLST** (finančné skupiny) → `FGLST-product_categories.md` (ďalší dokument)
- **SGLST** (špecifické skupiny) → `SGLST-product_categories.md` (ďalší dokument)

---

**Vytvoril:** Claude & Zoltán  
**Dátum:** 2025-12-10  
**Verzia:** 1.1  
**Status:** ✅ Schválené - aktualizované audit polia