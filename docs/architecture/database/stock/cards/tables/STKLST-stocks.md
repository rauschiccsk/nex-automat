# STKLST.BTR → stocks

## 1. PREHĽAD

### Btrieve súbor
- **Názov:** STKLST.BTR
- **Umiestnenie:** `C:\NEX\YEARACT\STORES\STKLST.BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\STORES\`
- **Účel:** Číselník skladov (stocks catalog)

### PostgreSQL tabuľka
- **Názov:** `stocks`
- **Schema:** `public`
- **Účel:** Evidencia všetkých skladov v systéme

### Popis
Číselník skladov definuje všetky sklady používané v NEX Genesis systéme. Každý sklad má typ (tovarový, materiálový, výrobný), je priradený k prevádzkovej jednotke a môže mať priradený default cenník. Tabuľka je základom pre skladové karty (`stock_cards`) a všetky skladové dokumenty.

---

## 2. KOMPLEXNÁ SQL SCHÉMA

```sql
-- ============================================================================
-- STOCKS - Číselník skladov
-- ============================================================================

CREATE TABLE stocks (
    -- Primárny kľúč
    stock_id                INTEGER PRIMARY KEY,
    stock_code              VARCHAR(10) NOT NULL UNIQUE,
    
    -- Základné údaje
    stock_name              VARCHAR(30) NOT NULL,
    stock_type              CHAR(1) NOT NULL,
    
    -- Väzby
    facility_id             INTEGER,
    price_list_id           INTEGER,
    
    -- Audit polia
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by              VARCHAR(50),
    updated_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by              VARCHAR(50),
    
    -- Constraints
    CONSTRAINT chk_stock_type 
        CHECK (stock_type IN ('T', 'M', 'V')),
    CONSTRAINT chk_stock_name_not_empty 
        CHECK (TRIM(stock_name) <> ''),
    CONSTRAINT chk_stock_code_not_empty 
        CHECK (TRIM(stock_code) <> '')
);

-- ============================================================================
-- INDEXY
-- ============================================================================

-- Primárny kľúč index (automaticky vytvorený)
-- CREATE UNIQUE INDEX idx_stocks_pk ON stocks(stock_id);

-- Unique index na stock_code (automaticky vytvorený cez UNIQUE constraint)
-- CREATE UNIQUE INDEX idx_stocks_code ON stocks(stock_code);

-- Index na stock_name pre vyhľadávanie
CREATE INDEX idx_stocks_name ON stocks(stock_name);

-- Index na stock_type pre filtrovanie
CREATE INDEX idx_stocks_type ON stocks(stock_type);

-- Index na facility_id pre JOIN queries
CREATE INDEX idx_stocks_facility_id ON stocks(facility_id);

-- ============================================================================
-- FOREIGN KEY CONSTRAINTS
-- ============================================================================

-- FK: facility_id → facilities.facility_id
-- Poznámka: Tabuľka facilities môže byť z PASUBC-partner_catalog_facilities.md
--           alebo vlastná tabuľka facilities ak sú prevádzky evidované samostatne
ALTER TABLE stocks
    ADD CONSTRAINT fk_stocks_facility
    FOREIGN KEY (facility_id)
    REFERENCES facilities(facility_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE;

-- FK: price_list_id → price_lists.price_list_id  
-- Poznámka: Default cenník pre sklad (môže byť NULL)
ALTER TABLE stocks
    ADD CONSTRAINT fk_stocks_price_list
    FOREIGN KEY (price_list_id)
    REFERENCES price_lists(price_list_id)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

-- ============================================================================
-- TRIGGERS
-- ============================================================================

-- Trigger: Automatická aktualizácia updated_at pri UPDATE
CREATE OR REPLACE FUNCTION trg_stocks_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_stocks_updated_at
    BEFORE UPDATE ON stocks
    FOR EACH ROW
    EXECUTE FUNCTION trg_stocks_updated_at();

-- Trigger: Validácia pred DELETE - RESTRICT ak existujú stock_cards
CREATE OR REPLACE FUNCTION trg_stocks_before_delete()
RETURNS TRIGGER AS $$
DECLARE
    v_count INTEGER;
BEGIN
    -- Kontrola stock_cards
    SELECT COUNT(*) INTO v_count
    FROM stock_cards
    WHERE stock_id = OLD.stock_id;
    
    IF v_count > 0 THEN
        RAISE EXCEPTION 'Cannot delete stock %: % stock cards exist',
            OLD.stock_code, v_count;
    END IF;
    
    -- Kontrola stock_movements
    SELECT COUNT(*) INTO v_count
    FROM stock_movements
    WHERE stock_id = OLD.stock_id;
    
    IF v_count > 0 THEN
        RAISE EXCEPTION 'Cannot delete stock %: % stock movements exist',
            OLD.stock_code, v_count;
    END IF;
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_stocks_before_delete
    BEFORE DELETE ON stocks
    FOR EACH ROW
    EXECUTE FUNCTION trg_stocks_before_delete();

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE stocks IS 'Číselník skladov - evidencia všetkých skladov v systéme';
COMMENT ON COLUMN stocks.stock_id IS 'Primárny kľúč (z Btrieve StkNum)';
COMMENT ON COLUMN stocks.stock_code IS 'Kód skladu (human-readable, napr. SK01, SK02)';
COMMENT ON COLUMN stocks.stock_name IS 'Názov skladu';
COMMENT ON COLUMN stocks.stock_type IS 'Typ skladu: T=Tovarový, M=Materiálový, V=Výrobný';
COMMENT ON COLUMN stocks.facility_id IS 'FK: Prevádzková jednotka (facility) kde je sklad';
COMMENT ON COLUMN stocks.price_list_id IS 'FK: Default cenník pre sklad (môže byť NULL)';
```

---

## 3. MAPPING POLÍ

### Prenášané polia

| Btrieve pole | Typ | PostgreSQL pole | Typ | Poznámka |
|---|---|---|---|---|
| `StkNum` | word | `stock_id` | INTEGER | Primárny kľúč |
| - | - | `stock_code` | VARCHAR(10) | **NOVÉ**: Generované z stock_id (napr. "SK01") |
| `StkName` | Str30 | `stock_name` | VARCHAR(30) | Názov skladu |
| `StkType` | Str1 | `stock_type` | CHAR(1) | T/M/V |
| `WriNum` | word | `facility_id` | INTEGER | FK: Prevádzková jednotka |
| `PlsNum` | word | `price_list_id` | INTEGER | FK: Cenník (NULL allowed) |
| `ModUser` | Str8 | `updated_by` | VARCHAR(50) | Používateľ |
| `ModDate` + `ModTime` | DateType + TimeType | `updated_at` | TIMESTAMP | **ZLÚČENÉ**: Dátum + čas do TIMESTAMP |

### Neprenášané polia (s dôvodom)

| Btrieve pole | Typ | Dôvod neprenášania |
|---|---|---|
| `Shared` | byte | FTP synchronizácia - Btrieve technický príznak |
| `ModNum` | word | Poradové číslo modifikácie - internal counter |
| `_StkName` | Str15 | Denormalizované vyhľadávacie pole pre Btrieve index |
| `IvDate` | DateType | Dátum inventúry - historická informácia, možno vlastná tabuľka inventory |

### Nové polia v PostgreSQL

| Pole | Typ | Účel |
|---|---|---|
| `stock_code` | VARCHAR(10) | Human-readable kód (napr. "SK01", "SK02") |
| `created_at` | TIMESTAMP | Dátum vytvorenia záznamu |
| `created_by` | VARCHAR(50) | Používateľ ktorý vytvoril záznam |

---

## 4. BIZNIS LOGIKA

### Typ skladu (stock_type)

| Kód | Význam | Účel |
|---|---|---|
| `T` | Tovarový | Sklad tovaru (trade goods) |
| `M` | Materiálový | Sklad materiálu (raw materials) |
| `V` | Výrobný | Výrobný sklad (production warehouse) |

### Väzby

**1. Prevádzková jednotka (facility_id)**
- Každý sklad je priradený k prevádzkovej jednotke
- ON DELETE RESTRICT - nemožno zmazať facility ak má sklady
- Umožňuje organizačnú štruktúru (pobočky, závody)

**2. Default cenník (price_list_id)**
- Môže byť NULL (nie je povinný)
- Ak je nastavený, používa sa ako default pre dokument/faktúru zo skladu
- ON DELETE SET NULL - pri zmazaní cenníka sa iba nullne, sklad zostáva

### Validácie

```sql
-- 1. Typ skladu musí byť platný
CHECK (stock_type IN ('T', 'M', 'V'))

-- 2. Názov nesmie byť prázdny
CHECK (TRIM(stock_name) <> '')

-- 3. Kód nesmie byť prázdny
CHECK (TRIM(stock_code) <> '')

-- 4. Kód musí byť unique
UNIQUE (stock_code)
```

### Automatizácia

**Trigger: updated_at**
- Pri každom UPDATE automaticky aktualizuje `updated_at = CURRENT_TIMESTAMP`
- Zabezpečuje audit trail

**Trigger: before_delete**
- Kontroluje či neexistujú skladové karty (`stock_cards`)
- Kontroluje či neexistujú pohyby (`stock_movements`)
- RAISE EXCEPTION ak existujú → RESTRICT delete

---

## 5. VZŤAHY S INÝMI TABUĽKAMI

### Parent tabuľky (Master data)

```sql
facilities (facility_id)
    ↓ ON DELETE RESTRICT
stocks (facility_id)

price_lists (price_list_id)
    ↓ ON DELETE SET NULL
stocks (price_list_id)
```

### Child tabuľky (Dependent data)

```sql
stocks (stock_id)
    ↓ ON DELETE RESTRICT (via trigger)
stock_cards (stock_id)

stocks (stock_id)
    ↓ ON DELETE RESTRICT (via trigger)
stock_movements (stock_id)

stocks (stock_id)
    ↓ ON DELETE RESTRICT
stock_documents (stock_id)
```

### Query patterns

**1. Zoznam skladov s facility**
```sql
SELECT 
    s.stock_code,
    s.stock_name,
    s.stock_type,
    f.facility_name,
    s.updated_at
FROM stocks s
LEFT JOIN facilities f ON s.facility_id = f.facility_id
ORDER BY s.stock_code;
```

**2. Sklady podľa typu**
```sql
SELECT * FROM stocks 
WHERE stock_type = 'T'  -- Tovarové sklady
ORDER BY stock_name;
```

**3. Kontrola existencie skladových kariet**
```sql
SELECT 
    s.stock_code,
    s.stock_name,
    COUNT(sc.stock_card_id) AS card_count,
    SUM(sc.quantity_on_hand) AS total_quantity
FROM stocks s
LEFT JOIN stock_cards sc ON s.stock_id = sc.stock_id
GROUP BY s.stock_id, s.stock_code, s.stock_name
ORDER BY card_count DESC;
```

---

## 6. VALIDAČNÉ PRAVIDLÁ

### CHECK constraints

```sql
-- 1. Typ skladu
CONSTRAINT chk_stock_type 
    CHECK (stock_type IN ('T', 'M', 'V'))

-- 2. Názov nie prázdny
CONSTRAINT chk_stock_name_not_empty 
    CHECK (TRIM(stock_name) <> '')

-- 3. Kód nie prázdny
CONSTRAINT chk_stock_code_not_empty 
    CHECK (TRIM(stock_code) <> '')
```

### UNIQUE constraints

```sql
-- stock_code musí byť unique
CONSTRAINT stocks_stock_code_key 
    UNIQUE (stock_code)
```

### Trigger validations

```sql
-- Pred DELETE: kontrola stock_cards a stock_movements
-- Ak existujú → RAISE EXCEPTION
CREATE TRIGGER trg_stocks_before_delete
    BEFORE DELETE ON stocks
    FOR EACH ROW
    EXECUTE FUNCTION trg_stocks_before_delete();
```

---

## 7. QUERY PATTERNS

### Základné queries

**1. Zoznam všetkých skladov**
```sql
SELECT 
    stock_code,
    stock_name,
    CASE stock_type
        WHEN 'T' THEN 'Tovarový'
        WHEN 'M' THEN 'Materiálový'
        WHEN 'V' THEN 'Výrobný'
    END AS type_description,
    updated_at
FROM stocks
ORDER BY stock_code;
```

**2. Vyhľadanie skladu podľa kódu**
```sql
SELECT * FROM stocks
WHERE stock_code = 'SK01';
```

**3. Vyhľadanie skladov podľa názvu (LIKE)**
```sql
SELECT * FROM stocks
WHERE stock_name ILIKE '%bratislava%'
ORDER BY stock_name;
```

### Pokročilé queries

**4. Sklady s počtom skladových kariet**
```sql
SELECT 
    s.stock_code,
    s.stock_name,
    s.stock_type,
    COUNT(sc.stock_card_id) AS products_count,
    SUM(sc.quantity_on_hand) AS total_quantity,
    SUM(sc.value_total) AS total_value
FROM stocks s
LEFT JOIN stock_cards sc ON s.stock_id = sc.stock_id
GROUP BY s.stock_id, s.stock_code, s.stock_name, s.stock_type
ORDER BY total_value DESC NULLS LAST;
```

**5. Sklady s poslednou aktivitou**
```sql
SELECT 
    s.stock_code,
    s.stock_name,
    MAX(sm.movement_date) AS last_movement_date,
    COUNT(sm.movement_id) AS movement_count_today
FROM stocks s
LEFT JOIN stock_movements sm ON s.stock_id = sm.stock_id
    AND sm.movement_date = CURRENT_DATE
GROUP BY s.stock_id, s.stock_code, s.stock_name
ORDER BY last_movement_date DESC NULLS LAST;
```

**6. Kontrola pred zmazaním**
```sql
-- Zistiť či je možné zmazať sklad
SELECT 
    s.stock_code,
    s.stock_name,
    (SELECT COUNT(*) FROM stock_cards WHERE stock_id = s.stock_id) AS stock_cards_count,
    (SELECT COUNT(*) FROM stock_movements WHERE stock_id = s.stock_id) AS movements_count,
    CASE 
        WHEN (SELECT COUNT(*) FROM stock_cards WHERE stock_id = s.stock_id) > 0 THEN 'Nemožno zmazať - existujú skladové karty'
        WHEN (SELECT COUNT(*) FROM stock_movements WHERE stock_id = s.stock_id) > 0 THEN 'Nemožno zmazať - existujú pohyby'
        ELSE 'Možno zmazať'
    END AS delete_status
FROM stocks s
WHERE s.stock_id = 1;
```

---

## 8. PRÍKLAD DÁT

```sql
-- ============================================================================
-- PRÍKLAD: INSERT sample data
-- ============================================================================

INSERT INTO stocks (
    stock_id,
    stock_code,
    stock_name,
    stock_type,
    facility_id,
    price_list_id,
    created_by,
    updated_by
) VALUES
    (1, 'SK01', 'Hlavný sklad Bratislava', 'T', 1, 1, 'SYSTEM', 'SYSTEM'),
    (2, 'SK02', 'Pobočka Košice', 'T', 2, 1, 'SYSTEM', 'SYSTEM'),
    (3, 'SK03', 'Materiálový sklad', 'M', 1, NULL, 'SYSTEM', 'SYSTEM'),
    (4, 'SK04', 'Výrobný sklad Žilina', 'V', 3, NULL, 'SYSTEM', 'SYSTEM'),
    (5, 'SK05', 'Konsignačný sklad', 'T', 1, 2, 'SYSTEM', 'SYSTEM');

-- ============================================================================
-- PRÍKLAD: SELECT výsledok
-- ============================================================================

/*
stock_id | stock_code | stock_name                  | stock_type | facility_id | price_list_id
---------|------------|----------------------------|------------|-------------|---------------
1        | SK01       | Hlavný sklad Bratislava    | T          | 1           | 1
2        | SK02       | Pobočka Košice             | T          | 2           | 1
3        | SK03       | Materiálový sklad          | M          | 1           | NULL
4        | SK04       | Výrobný sklad Žilina       | V          | 3           | NULL
5        | SK05       | Konsignačný sklad          | T          | 1           | 2
*/
```

---

## 9. POZNÁMKY PRE MIGRÁCIU

### Python transformácie

**1. Generovanie stock_code**
```python
def generate_stock_code(stock_num: int) -> str:
    """
    Generuje stock_code z Btrieve StkNum.
    
    Args:
        stock_num: Číslo skladu z Btrieve (StkNum)
        
    Returns:
        Kód skladu napr. "SK01", "SK02"
    """
    return f"SK{stock_num:02d}"

# Príklad:
# StkNum = 1 → stock_code = "SK01"
# StkNum = 15 → stock_code = "SK15"
```

**2. Zlúčenie ModDate + ModTime do TIMESTAMP**
```python
from datetime import datetime, date, time

def merge_date_time(mod_date: date, mod_time: time) -> datetime:
    """
    Zlúči Btrieve DateType a TimeType do PostgreSQL TIMESTAMP.
    
    Args:
        mod_date: Dátum z Btrieve (ModDate)
        mod_time: Čas z Btrieve (ModTime)
        
    Returns:
        TIMESTAMP pre PostgreSQL
    """
    return datetime.combine(mod_date, mod_time)

# Príklad:
# ModDate = 2024-12-11, ModTime = 14:30:00
# → updated_at = 2024-12-11 14:30:00
```

**3. Validácia stock_type**
```python
def validate_stock_type(stk_type: str) -> str:
    """
    Validuje a normalizuje typ skladu.
    
    Args:
        stk_type: Typ z Btrieve (StkType)
        
    Returns:
        Validovaný typ ('T', 'M', 'V')
        
    Raises:
        ValueError: Ak typ nie je platný
    """
    valid_types = {'T', 'M', 'V'}
    stk_type = stk_type.strip().upper()
    
    if stk_type not in valid_types:
        raise ValueError(f"Invalid stock type: {stk_type}")
    
    return stk_type
```

**4. Kompletný migration príklad**
```python
import pypyodbc
import psycopg2
from datetime import datetime

def migrate_stocks(btrieve_path: str, pg_conn):
    """
    Migruje STKLST.BTR → stocks tabuľku.
    
    Args:
        btrieve_path: Cesta k Btrieve súboru (napr. "C:\\NEX\\YEARACT\\STORES\\STKLST.BTR")
        pg_conn: PostgreSQL connection
    """
    # 1. Pripojenie k Btrieve
    btrieve_conn_str = f"Driver={{Pervasive ODBC Client Interface}};ServerName=localhost;DBQ={btrieve_path};"
    btrieve_conn = pypyodbc.connect(btrieve_conn_str)
    btrieve_cursor = btrieve_conn.cursor()
    
    # 2. SELECT z Btrieve
    btrieve_cursor.execute("""
        SELECT 
            StkNum, 
            StkName, 
            StkType, 
            WriNum, 
            PlsNum, 
            ModUser, 
            ModDate, 
            ModTime
        FROM STKLST
        ORDER BY StkNum
    """)
    
    # 3. INSERT do PostgreSQL
    pg_cursor = pg_conn.cursor()
    
    for row in btrieve_cursor:
        stock_id = row.StkNum
        stock_code = generate_stock_code(stock_id)
        stock_name = row.StkName.strip()
        stock_type = validate_stock_type(row.StkType)
        facility_id = row.WriNum if row.WriNum > 0 else None
        price_list_id = row.PlsNum if row.PlsNum > 0 else None
        updated_by = row.ModUser.strip()
        updated_at = merge_date_time(row.ModDate, row.ModTime)
        
        pg_cursor.execute("""
            INSERT INTO stocks (
                stock_id,
                stock_code,
                stock_name,
                stock_type,
                facility_id,
                price_list_id,
                updated_by,
                updated_at,
                created_by,
                created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            stock_id,
            stock_code,
            stock_name,
            stock_type,
            facility_id,
            price_list_id,
            updated_by,
            updated_at,
            updated_by,  # created_by = updated_by pri migrácii
            updated_at   # created_at = updated_at pri migrácii
        ))
    
    pg_conn.commit()
    
    btrieve_cursor.close()
    btrieve_conn.close()
    
    print(f"✅ Migration completed: {btrieve_cursor.rowcount} stocks migrated")
```

### Poradie migrácie

**KRITICKÉ:** Stocks je master tabuľka - musí sa migrovať pred:

```
1. ✅ facilities (prevádzky) - musí existovať PRED stocks
2. ✅ price_lists (cenníky) - musí existovať PRED stocks
3. → stocks (táto tabuľka)
4. → stock_cards (skladové karty) - závisia od stocks
5. → stock_movements (pohyby) - závisia od stocks
6. → stock_documents (doklady) - závisia od stocks
```

### Špeciálne prípady

**1. NULL hodnoty**
```python
# facility_id môže byť NULL ak WriNum = 0
facility_id = row.WriNum if row.WriNum > 0 else None

# price_list_id môže byť NULL ak PlsNum = 0
price_list_id = row.PlsNum if row.PlsNum > 0 else None
```

**2. Duplicitné stock_code**
```python
# Kontrola duplicity pred INSERT
pg_cursor.execute("""
    SELECT stock_id FROM stocks 
    WHERE stock_code = %s
""", (stock_code,))

if pg_cursor.fetchone():
    print(f"⚠️ Duplicate stock_code: {stock_code}")
    # Riešenie: Pridať suffix alebo upraviť generovanie kódu
    stock_code = f"{stock_code}_DUP"
```

---

## 10. VERZIA A ZMENY

| Verzia | Dátum | Autor | Zmeny |
|---|---|---|---|
| 1.0 | 2025-12-11 | Zoltán + Claude | Počiatočná verzia - kompletná dokumentácia STKLST.BTR → stocks |

---

**Súvisiace dokumenty:**
- `DATABASE_RELATIONSHIPS.md` - Cross-system vzťahy
- `stock/INDEX.md` - Prehľad stock systému
- `stock/cards/INDEX.md` - Prehľad skladových kariet
- `catalogs/partners/tables/PASUBC-partner_catalog_facilities.md` - Prevádzky (facilities)
- `sales/tables/PLSnnnnn-price_list_items.md` - Cenníky (price_lists)

---

**Migračné dependencies:**
```
facilities → stocks
price_lists → stocks
stocks → stock_cards
stocks → stock_movements
```