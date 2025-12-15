# STKnnnnn.BTR → stock_cards

## 1. PREHĽAD

**Účel:** Skladové karty zásob - evidencia aktuálneho stavu produktov na skladoch.

**Charakteristika:**
- Hlavná tabuľka pre sledovanie zásob po skladoch
- Každý produkt má samostatnú kartu na každom sklade
- Obsahuje aktuálne množstvá, hodnoty, rezervácie, objednávky
- Sleduje príjmy, výdaje, predaj od začiatku roka
- Eviduje normatívy (min/max/opt), ceny (avg/last/act)
- Podporuje AVCO (Average Cost) aj FIFO oceňovanie

**Btrieve architektúra:**
- NEX Genesis: `STK00001.BTR` (sklad 1), `STK00002.BTR` (sklad 2), ...
- Samostatný súbor pre každý sklad

**PostgreSQL architektúra:**
- `stock_cards` - jedna tabuľka pre všetky sklady
- Pridané pole: `stock_id` (číslo skladu)
- Composite PK: `(stock_id, product_id)`

**Vzťahy:**
- Parent: `stocks` (1:N) + `products` (1:N)
- Child: `stock_movements` (1:N), `stock_batches` (1:N), `stock_reservations` (1:N)

**Btrieve súbor:** `STKnnnnn.BTR` (n = číslo skladu)  
**Primárny kľúč:** GsCode (product_id) v rámci jedného skladu  
**PostgreSQL PK:** (stock_id, product_id)  
**Hlavný index:** GsCode

---

## 2. KOMPLEXNÁ SQL SCHÉMA

```sql
-- =====================================================
-- Table: stock_cards
-- Purpose: Skladové karty zásob (aktuálny stav produktov na skladoch)
-- =====================================================

CREATE TABLE stock_cards (
    -- Composite primárny kľúč
    stock_id                INTEGER NOT NULL,
    product_id              INTEGER NOT NULL,
    
    PRIMARY KEY (stock_id, product_id),
    
    -- Začiatočný stav (na začiatku roka)
    beginning_quantity      DECIMAL(15,3) NOT NULL DEFAULT 0,
    beginning_value         DECIMAL(15,2) NOT NULL DEFAULT 0,
    
    -- Celkové príjmy/výdaje od začiatku roka
    total_in_quantity       DECIMAL(15,3) NOT NULL DEFAULT 0,
    total_in_value          DECIMAL(15,2) NOT NULL DEFAULT 0,
    total_out_quantity      DECIMAL(15,3) NOT NULL DEFAULT 0,
    total_out_value         DECIMAL(15,2) NOT NULL DEFAULT 0,
    
    -- Aktuálny stav (vypočítaný triggermi z movements)
    quantity_on_hand        DECIMAL(15,3) NOT NULL DEFAULT 0,
    value_total             DECIMAL(15,2) NOT NULL DEFAULT 0,
    
    -- Predaj (ešte neodpočítané zo skladu)
    sold_quantity           DECIMAL(15,3) NOT NULL DEFAULT 0,
    
    -- Nevysporiadané položky
    unsettled_quantity      DECIMAL(15,3) NOT NULL DEFAULT 0,
    
    -- Rezervácie
    reserved_customer_orders DECIMAL(15,3) NOT NULL DEFAULT 0,  -- OcdQnt
    reserved_other          DECIMAL(15,3) NOT NULL DEFAULT 0,   -- OsrQnt
    unavailable_quantity    DECIMAL(15,3) NOT NULL DEFAULT 0,   -- NrsQnt (nemožné rezervovať)
    
    -- Voľné množstvo (dostupné na vydanie)
    free_quantity           DECIMAL(15,3) NOT NULL DEFAULT 0,   -- FreQnt
    free_order_quantity     DECIMAL(15,3) NOT NULL DEFAULT 0,   -- FroQnt
    
    -- Objednané od dodávateľov
    ordered_quantity        DECIMAL(15,3) NOT NULL DEFAULT 0,   -- OsdQnt
    available_supplier_quantity DECIMAL(15,3) NOT NULL DEFAULT 0, -- OfrQnt (dostupné od dodávateľov)
    
    -- Tovar na ceste (z príjemiek)
    incoming_reserved_quantity DECIMAL(15,3) NOT NULL DEFAULT 0, -- ImrQnt
    
    -- Množstvo na pozičných miestach
    location_quantity       DECIMAL(15,3) NOT NULL DEFAULT 0,   -- PosQnt
    
    -- Ceny
    average_price           DECIMAL(15,2) NOT NULL DEFAULT 0,   -- AVCO
    last_purchase_price     DECIMAL(15,2) NOT NULL DEFAULT 0,   -- Posledná nákupná
    current_fifo_price      DECIMAL(15,2) NOT NULL DEFAULT 0,   -- Aktuálna FIFO
    
    -- Normatívy
    max_quantity            DECIMAL(15,3),                       -- Horná hranica
    min_quantity            DECIMAL(15,3),                       -- Dolná hranica
    optimal_quantity        DECIMAL(15,3),                       -- Optimálne množstvo
    
    -- Posledné pohyby
    last_receipt_date       DATE,
    last_issue_date         DATE,
    last_receipt_quantity   DECIMAL(15,3),
    last_issue_quantity     DECIMAL(15,3),
    
    -- Dátum poslednej inventúry
    last_inventory_date     DATE,
    
    -- Predaj/výdaj za aktuálny rok
    current_year_sold_quantity  DECIMAL(15,3) NOT NULL DEFAULT 0,  -- ASaQnt
    current_year_issued_quantity DECIMAL(15,3) NOT NULL DEFAULT 0, -- AOuQnt
    
    -- Predaj/výdaj za predošlý rok
    previous_year_sold_quantity  DECIMAL(15,3) NOT NULL DEFAULT 0, -- PSaQnt
    previous_year_issued_quantity DECIMAL(15,3) NOT NULL DEFAULT 0, -- POuQnt
    
    -- Výrobné čísla
    unreleased_serial_count INTEGER NOT NULL DEFAULT 0,          -- ActSnQnt
    
    -- Posledný dodávateľ
    last_supplier_id        INTEGER,                             -- LinPac
    
    -- Vyradenie
    is_discontinued         BOOLEAN NOT NULL DEFAULT false,      -- DisFlag
    
    -- Audit polia
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by              VARCHAR(50),
    updated_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by              VARCHAR(50),
    
    -- Foreign Keys
    CONSTRAINT fk_stock_cards_stock
        FOREIGN KEY (stock_id) 
        REFERENCES stocks(stock_id)
        ON DELETE RESTRICT,
    
    CONSTRAINT fk_stock_cards_product
        FOREIGN KEY (product_id) 
        REFERENCES products(product_id)
        ON DELETE RESTRICT,
    
    CONSTRAINT fk_stock_cards_supplier
        FOREIGN KEY (last_supplier_id) 
        REFERENCES partners(partner_id)
        ON DELETE SET NULL
);

-- Indexy pre výkon
CREATE INDEX idx_stock_cards_stock ON stock_cards(stock_id);
CREATE INDEX idx_stock_cards_product ON stock_cards(product_id);
CREATE INDEX idx_stock_cards_quantity ON stock_cards(quantity_on_hand);
CREATE INDEX idx_stock_cards_value ON stock_cards(value_total);
CREATE INDEX idx_stock_cards_avg_price ON stock_cards(average_price);
CREATE INDEX idx_stock_cards_last_price ON stock_cards(last_purchase_price);
CREATE INDEX idx_stock_cards_last_receipt ON stock_cards(last_receipt_date);
CREATE INDEX idx_stock_cards_last_issue ON stock_cards(last_issue_date);
CREATE INDEX idx_stock_cards_supplier ON stock_cards(last_supplier_id);
CREATE INDEX idx_stock_cards_discontinued ON stock_cards(is_discontinued);

-- Composite indexy pre vyhľadávanie
CREATE INDEX idx_stock_cards_stock_active ON stock_cards(stock_id, is_discontinued);
CREATE INDEX idx_stock_cards_product_active ON stock_cards(product_id, is_discontinued);

-- Komentáre
COMMENT ON TABLE stock_cards IS 'Skladové karty zásob - aktuálny stav produktov na skladoch';
COMMENT ON COLUMN stock_cards.stock_id IS 'ID skladu (pridané pre PostgreSQL multi-sklad)';
COMMENT ON COLUMN stock_cards.product_id IS 'ID produktu (z Btrieve GsCode)';
COMMENT ON COLUMN stock_cards.quantity_on_hand IS 'Aktuálna skladová zásoba (aktualizovaná triggermi)';
COMMENT ON COLUMN stock_cards.value_total IS 'Aktuálna hodnota zásoby (aktualizovaná triggermi)';
COMMENT ON COLUMN stock_cards.average_price IS 'Priemerná nákupná cena (AVCO metóda)';
COMMENT ON COLUMN stock_cards.current_fifo_price IS 'Aktuálna cena podľa FIFO karty';
COMMENT ON COLUMN stock_cards.free_quantity IS 'Voľné množstvo = quantity_on_hand - reserved - sold';
COMMENT ON COLUMN stock_cards.reserved_customer_orders IS 'Rezervované pre zákaznícke objednávky';
COMMENT ON COLUMN stock_cards.ordered_quantity IS 'Objednané od dodávateľov';

-- Trigger pre updated_at
CREATE TRIGGER update_stock_cards_updated_at
    BEFORE UPDATE ON stock_cards
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger pre automatický prepočet free_quantity
CREATE OR REPLACE FUNCTION calculate_stock_card_free_quantity()
RETURNS TRIGGER AS $$
BEGIN
    NEW.free_quantity = NEW.quantity_on_hand 
                      - NEW.reserved_customer_orders 
                      - NEW.reserved_other 
                      - NEW.sold_quantity;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_stock_cards_free_quantity
    BEFORE INSERT OR UPDATE ON stock_cards
    FOR EACH ROW
    EXECUTE FUNCTION calculate_stock_card_free_quantity();

-- Check constraints
ALTER TABLE stock_cards
ADD CONSTRAINT chk_stock_cards_quantities_positive
CHECK (
    quantity_on_hand >= 0 AND
    beginning_quantity >= 0 AND
    total_in_quantity >= 0 AND
    total_out_quantity >= 0
);

ALTER TABLE stock_cards
ADD CONSTRAINT chk_stock_cards_normals
CHECK (
    (min_quantity IS NULL OR min_quantity >= 0) AND
    (max_quantity IS NULL OR max_quantity >= 0) AND
    (optimal_quantity IS NULL OR optimal_quantity >= 0) AND
    (min_quantity IS NULL OR max_quantity IS NULL OR min_quantity <= max_quantity)
);
```

---

## 3. MAPPING POLÍ

### Stock Cards (hlavná tabuľka)

| Btrieve Pole | Typ Btrieve | PostgreSQL Pole | Typ PostgreSQL | Transformácia | Poznámka |
|--------------|-------------|-----------------|----------------|---------------|----------|
| **PRIDANÉ** | - | stock_id | INTEGER | - | **PK part 1** (číslo skladu) |
| GsCode | LONGINT | product_id | INTEGER | Priamo | **PK part 2** |
| BegQnt | DOUBLE | beginning_quantity | DECIMAL(15,3) | Priamo | Začiatočný stav |
| InQnt | DOUBLE | total_in_quantity | DECIMAL(15,3) | Priamo | Príjem od začiatku roka |
| OutQnt | DOUBLE | total_out_quantity | DECIMAL(15,3) | Priamo | Výdaj od začiatku roka |
| ActQnt | DOUBLE | quantity_on_hand | DECIMAL(15,3) | Priamo | Aktuálna zásoba |
| SalQnt | DOUBLE | sold_quantity | DECIMAL(15,3) | Priamo | Predané (neodpočítané) |
| NrsQnt | DOUBLE | unavailable_quantity | DECIMAL(15,3) | Priamo | Nemožné rezervovať |
| OcdQnt | DOUBLE | reserved_customer_orders | DECIMAL(15,3) | Priamo | Rezervácie objednávky |
| FreQnt | DOUBLE | free_quantity | DECIMAL(15,3) | Vypočítané | Voľné množstvo |
| OsdQnt | DOUBLE | ordered_quantity | DECIMAL(15,3) | Priamo | Objednané od dodávateľa |
| BegVal | DOUBLE | beginning_value | DECIMAL(15,2) | Priamo | Začiatočná hodnota |
| InVal | DOUBLE | total_in_value | DECIMAL(15,2) | Priamo | Hodnota príjmu |
| OutVal | DOUBLE | total_out_value | DECIMAL(15,2) | Priamo | Hodnota výdaja |
| ActVal | DOUBLE | value_total | DECIMAL(15,2) | Priamo | Aktuálna hodnota |
| AvgPrice | DOUBLE | average_price | DECIMAL(15,2) | Priamo | Priemerná cena (AVCO) |
| LastPrice | DOUBLE | last_purchase_price | DECIMAL(15,2) | Priamo | Posledná nákupná |
| ActPrice | DOUBLE | current_fifo_price | DECIMAL(15,2) | Priamo | Aktuálna FIFO cena |
| MaxQnt | DOUBLE | max_quantity | DECIMAL(15,3) | Priamo | Maximum normatív |
| MinQnt | DOUBLE | min_quantity | DECIMAL(15,3) | Priamo | Minimum normatív |
| OptQnt | DOUBLE | optimal_quantity | DECIMAL(15,3) | Priamo | Optimum normatív |
| LastIDate | DATE | last_receipt_date | DATE | Priamo | Dátum posledného príjmu |
| LastODate | DATE | last_issue_date | DATE | Priamo | Dátum posledného výdaja |
| LastIQnt | DOUBLE | last_receipt_quantity | DECIMAL(15,3) | Priamo | Posledné množstvo príjmu |
| LastOQnt | DOUBLE | last_issue_quantity | DECIMAL(15,3) | Priamo | Posledné množstvo výdaja |
| ActSnQnt | LONGINT | unreleased_serial_count | INTEGER | Priamo | Počet nevydaných výr. čísiel |
| DisFlag | BYTE | is_discontinued | BOOLEAN | 1→true | Vyradenie |
| ModUser | STRING[8] | updated_by | VARCHAR(50) | Priamo | Audit |
| ModDate | DATE | updated_at | TIMESTAMP | Date+Time | Part of |
| ModTime | TIME | updated_at | TIMESTAMP | Date+Time | Part of |
| LinPac | LONGINT | last_supplier_id | INTEGER | Priamo | FK na partners |
| NsuQnt | DOUBLE | unsettled_quantity | DECIMAL(15,3) | Priamo | Nevysporiadané |
| OsrQnt | DOUBLE | reserved_other | DECIMAL(15,3) | Priamo | Iné rezervácie |
| FroQnt | DOUBLE | free_order_quantity | DECIMAL(15,3) | Priamo | Voľné z objednávky |
| ASaQnt | DOUBLE | current_year_sold_quantity | DECIMAL(15,3) | Priamo | Predaj aktuálny rok |
| AOuQnt | DOUBLE | current_year_issued_quantity | DECIMAL(15,3) | Priamo | Výdaj aktuálny rok |
| PSaQnt | DOUBLE | previous_year_sold_quantity | DECIMAL(15,3) | Priamo | Predaj predošlý rok |
| POuQnt | DOUBLE | previous_year_issued_quantity | DECIMAL(15,3) | Priamo | Výdaj predošlý rok |
| ImrQnt | DOUBLE | incoming_reserved_quantity | DECIMAL(15,3) | Priamo | Tovar na ceste |
| PosQnt | DOUBLE | location_quantity | DECIMAL(15,3) | Priamo | Na pozičných miestach |
| InvDate | DATE | last_inventory_date | DATE | Priamo | Posledná inventúra |

### Polia ktoré SA NEPRENÁŠAJÚ (sú v products tabuľke)

| Btrieve Pole | Dôvod neprenášania |
|--------------|-------------------|
| MgCode | FK na product_categories (v products) |
| FgCode | FK na product_categories (v products) |
| GsName | product_name (v products) |
| _GsName | Vyhľadávacie pole (nepotrebné v PostgreSQL) |
| BarCode | product_catalog_identifiers tabuľka |
| StkCode | product_code (v products) |
| MsName | unit (v products) |
| VatPrc | vat_rate (v products) |
| GsType | product_type (v products) |
| DrbMust | track_expiration (v products) |
| PdnMust | track_serial_numbers (v products) |
| GrcMth | warranty_months (v products) |
| MinMax | Vypočítané (trigger na základe min/max) |
| Profit | Obchodná marža (vypočítaná) |
| BPrice | sale_price_with_vat (v products) |
| Action | Cenová akcia (samostatná tabuľka?) |
| DefPos | Hlavné pozičné miesto (samostatná tabuľka?) |
| GaName | additional_name (v products) |
| _GaName | Vyhľadávacie pole (nepotrebné) |
| OsdCode | supplier_product_code (v products) |
| Sended | Technický príznak (NEX Genesis replikácia) |

**Zlúčené polia:**
- `ModDate` + `ModTime` → `updated_at` (TIMESTAMP)

**Vypočítané polia:**
- `free_quantity` = `quantity_on_hand` - `reserved_customer_orders` - `reserved_other` - `sold_quantity`
- `MinMax` príznak → vypočítané cez trigger (porovnanie s min/max)

---

## 4. BIZNIS LOGIKA

### 1. Oceňovanie zásob

**NEX Genesis používa 3 metódy:**

```sql
-- AVCO (Average Cost) - hlavná metóda
-- Priemerná cena = Celková hodnota / Celkové množstvo
average_price = value_total / quantity_on_hand

-- FIFO (First In, First Out)
-- Aktuálna cena podľa najstaršej FIFO karty
current_fifo_price  -- Z FIFO kariet (samostatná tabuľka)

-- Last Purchase Price
-- Posledná nákupná cena pri príjme
last_purchase_price
```

### 2. Voľné množstvo (Free Quantity)

```sql
-- Automatický prepočet cez trigger
free_quantity = quantity_on_hand 
              - reserved_customer_orders 
              - reserved_other 
              - sold_quantity

-- Príklad:
-- quantity_on_hand = 100
-- reserved_customer_orders = 20
-- reserved_other = 10
-- sold_quantity = 5
-- → free_quantity = 100 - 20 - 10 - 5 = 65
```

### 3. Normatívy (Min/Max/Opt)

```sql
-- Kontrola normatívov
SELECT 
    sc.stock_id,
    sc.product_id,
    p.product_name,
    sc.quantity_on_hand,
    sc.min_quantity,
    sc.max_quantity,
    sc.optimal_quantity,
    CASE 
        WHEN sc.quantity_on_hand < sc.min_quantity THEN 'UNDER_MIN'
        WHEN sc.quantity_on_hand > sc.max_quantity THEN 'OVER_MAX'
        WHEN sc.quantity_on_hand = sc.optimal_quantity THEN 'OPTIMAL'
        ELSE 'NORMAL'
    END as stock_status
FROM stock_cards sc
JOIN products p ON sc.product_id = p.product_id
WHERE sc.is_discontinued = false;
```

### 4. Objednávanie

```sql
-- Produkty ktoré treba objednať (pod minimom)
SELECT 
    sc.stock_id,
    sc.product_id,
    p.product_name,
    sc.quantity_on_hand,
    sc.min_quantity,
    sc.optimal_quantity,
    (sc.optimal_quantity - sc.quantity_on_hand) as order_quantity,
    sc.ordered_quantity,
    sc.available_supplier_quantity
FROM stock_cards sc
JOIN products p ON sc.product_id = p.product_id
WHERE sc.quantity_on_hand < sc.min_quantity
  AND sc.is_discontinued = false
ORDER BY (sc.min_quantity - sc.quantity_on_hand) DESC;
```

### 5. Rezervácie

```sql
-- Kontrola možnosti rezervácie
CREATE OR REPLACE FUNCTION can_reserve_quantity(
    p_stock_id INTEGER,
    p_product_id INTEGER,
    p_quantity DECIMAL(15,3)
) RETURNS BOOLEAN AS $$
DECLARE
    v_free_quantity DECIMAL(15,3);
BEGIN
    SELECT free_quantity INTO v_free_quantity
    FROM stock_cards
    WHERE stock_id = p_stock_id
      AND product_id = p_product_id;
    
    RETURN (v_free_quantity >= p_quantity);
END;
$$ LANGUAGE plpgsql;
```

### 6. Agregácia naprieč skladmi

```sql
-- Celkový stav produktu na všetkých skladoch
SELECT 
    p.product_id,
    p.product_code,
    p.product_name,
    SUM(sc.quantity_on_hand) as total_quantity,
    SUM(sc.value_total) as total_value,
    AVG(sc.average_price) as avg_price_all_stocks,
    SUM(sc.free_quantity) as total_free,
    SUM(sc.reserved_customer_orders) as total_reserved
FROM products p
LEFT JOIN stock_cards sc ON p.product_id = sc.product_id
WHERE sc.is_discontinued = false
GROUP BY p.product_id, p.product_code, p.product_name
HAVING SUM(sc.quantity_on_hand) > 0;
```

---

## 5. VZŤAHY S INÝMI TABUĽKAMI

```sql
-- Stock Cards → Stocks (N:1)
ALTER TABLE stock_cards
ADD CONSTRAINT fk_stock_cards_stock
FOREIGN KEY (stock_id) 
REFERENCES stocks(stock_id)
ON DELETE RESTRICT;  -- Nemožno zmazať sklad s kartami

-- Stock Cards → Products (N:1)
ALTER TABLE stock_cards
ADD CONSTRAINT fk_stock_cards_product
FOREIGN KEY (product_id) 
REFERENCES products(product_id)
ON DELETE RESTRICT;  -- Nemožno zmazať produkt so skladovou kartou

-- Stock Cards → Partners (N:1, optional)
-- Posledný dodávateľ
ALTER TABLE stock_cards
ADD CONSTRAINT fk_stock_cards_supplier
FOREIGN KEY (last_supplier_id) 
REFERENCES partners(partner_id)
ON DELETE SET NULL;  -- Ak zmazať partnera, ponechať NULL

-- Stock Cards ← Stock Movements (1:N)
-- Pohyby aktualizujú stock_cards cez triggery
-- Poznámka: Bude definované v stock_movements tabuľke

-- Stock Cards ← Stock Batches (1:N)
-- Šarže/Trvanlivosti pre produkty
-- Poznámka: Ak je track_expiration = true v products

-- Stock Cards ← Stock Reservations (1:N)
-- Detailné rezervácie
-- Poznámka: Bude definované v stock_reservations tabuľke
```

### Diagram vzťahov

```
stocks (1) ----< (N) stock_cards (N) >---- (1) products
                         |
                         | (optional)
                         +---- (N) >---- (1) partners (last_supplier)
                         |
                         +----< (1:N) stock_movements
                         +----< (1:N) stock_batches
                         +----< (1:N) stock_reservations
```

---

## 6. VALIDAČNÉ PRAVIDLÁ

```sql
-- 1. Množstvá musia byť nezáporné
ALTER TABLE stock_cards
ADD CONSTRAINT chk_stock_cards_quantities_positive
CHECK (
    quantity_on_hand >= 0 AND
    beginning_quantity >= 0 AND
    total_in_quantity >= 0 AND
    total_out_quantity >= 0
);

-- 2. Normatívy musia byť logické
ALTER TABLE stock_cards
ADD CONSTRAINT chk_stock_cards_normals
CHECK (
    (min_quantity IS NULL OR min_quantity >= 0) AND
    (max_quantity IS NULL OR max_quantity >= 0) AND
    (optimal_quantity IS NULL OR optimal_quantity >= 0) AND
    (min_quantity IS NULL OR max_quantity IS NULL OR min_quantity <= max_quantity)
);

-- 3. Ceny musia byť nezáporné
ALTER TABLE stock_cards
ADD CONSTRAINT chk_stock_cards_prices_positive
CHECK (
    average_price >= 0 AND
    last_purchase_price >= 0 AND
    current_fifo_price >= 0
);

-- 4. Hodnoty musia byť nezáporné
ALTER TABLE stock_cards
ADD CONSTRAINT chk_stock_cards_values_positive
CHECK (
    value_total >= 0 AND
    beginning_value >= 0 AND
    total_in_value >= 0 AND
    total_out_value >= 0
);

-- 5. Jedinečnosť (stock_id, product_id)
-- Automaticky zabezpečené PRIMARY KEY

-- 6. Trigger pre kontrolu normatívov
CREATE OR REPLACE FUNCTION check_stock_card_normals()
RETURNS TRIGGER AS $$
BEGIN
    -- Upozorniť ak pod minimom
    IF NEW.quantity_on_hand < NEW.min_quantity THEN
        RAISE NOTICE 'Produkt % na sklade % je pod minimom (%)!', 
            NEW.product_id, NEW.stock_id, NEW.min_quantity;
    END IF;
    
    -- Upozorniť ak nad maximom
    IF NEW.quantity_on_hand > NEW.max_quantity THEN
        RAISE NOTICE 'Produkt % na sklade % je nad maximom (%)!', 
            NEW.product_id, NEW.stock_id, NEW.max_quantity;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_stock_cards_check_normals
    AFTER INSERT OR UPDATE ON stock_cards
    FOR EACH ROW
    EXECUTE FUNCTION check_stock_card_normals();
```

---

## 7. QUERY PATTERNS

### Základné queries

```sql
-- 1. Detail skladovej karty
SELECT 
    sc.*,
    s.stock_name,
    p.product_code,
    p.product_name,
    p.unit
FROM stock_cards sc
JOIN stocks s ON sc.stock_id = s.stock_id
JOIN products p ON sc.product_id = p.product_id
WHERE sc.stock_id = 1
  AND sc.product_id = 12345;

-- 2. Produkty na sklade s množstvom > 0
SELECT 
    sc.product_id,
    p.product_code,
    p.product_name,
    sc.quantity_on_hand,
    sc.value_total,
    sc.average_price,
    sc.free_quantity
FROM stock_cards sc
JOIN products p ON sc.product_id = p.product_id
WHERE sc.stock_id = 1
  AND sc.quantity_on_hand > 0
  AND sc.is_discontinued = false
ORDER BY p.product_name;

-- 3. Celková hodnota skladu
SELECT 
    sc.stock_id,
    s.stock_name,
    SUM(sc.value_total) as total_value,
    COUNT(*) as product_count,
    SUM(sc.quantity_on_hand) as total_quantity
FROM stock_cards sc
JOIN stocks s ON sc.stock_id = s.stock_id
WHERE sc.quantity_on_hand > 0
  AND sc.is_discontinued = false
GROUP BY sc.stock_id, s.stock_name;

-- 4. Produkt na všetkých skladoch
SELECT 
    sc.stock_id,
    s.stock_name,
    sc.quantity_on_hand,
    sc.value_total,
    sc.average_price,
    sc.free_quantity,
    sc.reserved_customer_orders
FROM stock_cards sc
JOIN stocks s ON sc.stock_id = s.stock_id
WHERE sc.product_id = 12345
  AND sc.is_discontinued = false
ORDER BY sc.quantity_on_hand DESC;

-- 5. Produkty pod minimom (na objednanie)
SELECT 
    sc.stock_id,
    sc.product_id,
    p.product_code,
    p.product_name,
    sc.quantity_on_hand,
    sc.min_quantity,
    (sc.optimal_quantity - sc.quantity_on_hand) as order_quantity
FROM stock_cards sc
JOIN products p ON sc.product_id = p.product_id
WHERE sc.quantity_on_hand < sc.min_quantity
  AND sc.is_discontinued = false
ORDER BY (sc.min_quantity - sc.quantity_on_hand) DESC;
```

### Pokročilé queries

```sql
-- 6. ABC analýza (podľa hodnoty)
WITH stock_values AS (
    SELECT 
        sc.product_id,
        p.product_code,
        p.product_name,
        SUM(sc.value_total) as total_value
    FROM stock_cards sc
    JOIN products p ON sc.product_id = p.product_id
    WHERE sc.quantity_on_hand > 0
      AND sc.is_discontinued = false
    GROUP BY sc.product_id, p.product_code, p.product_name
),
cumulative AS (
    SELECT 
        *,
        SUM(total_value) OVER (ORDER BY total_value DESC) as cumulative_value,
        SUM(total_value) OVER () as grand_total
    FROM stock_values
)
SELECT 
    product_id,
    product_code,
    product_name,
    total_value,
    ROUND((cumulative_value / grand_total * 100), 2) as cumulative_percent,
    CASE 
        WHEN (cumulative_value / grand_total) <= 0.80 THEN 'A'
        WHEN (cumulative_value / grand_total) <= 0.95 THEN 'B'
        ELSE 'C'
    END as abc_category
FROM cumulative
ORDER BY total_value DESC;

-- 7. Obrátkovosť zásob (inventory turnover)
SELECT 
    sc.product_id,
    p.product_code,
    p.product_name,
    sc.total_out_quantity,
    sc.quantity_on_hand,
    CASE 
        WHEN sc.quantity_on_hand > 0 
        THEN ROUND((sc.total_out_quantity / sc.quantity_on_hand), 2)
        ELSE 0 
    END as turnover_ratio,
    CASE 
        WHEN sc.total_out_quantity > 0 
        THEN ROUND((365.0 * sc.quantity_on_hand / sc.total_out_quantity), 0)
        ELSE NULL 
    END as days_on_hand
FROM stock_cards sc
JOIN products p ON sc.product_id = p.product_id
WHERE sc.stock_id = 1
  AND sc.is_discontinued = false
ORDER BY turnover_ratio DESC;

-- 8. Dead stock (nula pohyb dlho)
SELECT 
    sc.stock_id,
    sc.product_id,
    p.product_code,
    p.product_name,
    sc.quantity_on_hand,
    sc.value_total,
    sc.last_issue_date,
    CURRENT_DATE - sc.last_issue_date as days_since_last_issue
FROM stock_cards sc
JOIN products p ON sc.product_id = p.product_id
WHERE sc.quantity_on_hand > 0
  AND sc.is_discontinued = false
  AND (sc.last_issue_date IS NULL OR 
       CURRENT_DATE - sc.last_issue_date > 180)  -- 6 mesiacov
ORDER BY days_since_last_issue DESC;

-- 9. Rezervácie vs. dostupnosť
SELECT 
    sc.stock_id,
    sc.product_id,
    p.product_code,
    p.product_name,
    sc.quantity_on_hand,
    sc.reserved_customer_orders,
    sc.reserved_other,
    sc.free_quantity,
    ROUND((sc.reserved_customer_orders / 
           NULLIF(sc.quantity_on_hand, 0) * 100), 2) as reserved_percent
FROM stock_cards sc
JOIN products p ON sc.product_id = p.product_id
WHERE sc.reserved_customer_orders > 0
  AND sc.is_discontinued = false
ORDER BY reserved_percent DESC;

-- 10. Porovnanie aktuálny vs. predošlý rok
SELECT 
    sc.stock_id,
    sc.product_id,
    p.product_code,
    p.product_name,
    sc.current_year_sold_quantity,
    sc.previous_year_sold_quantity,
    CASE 
        WHEN sc.previous_year_sold_quantity > 0 
        THEN ROUND(((sc.current_year_sold_quantity - sc.previous_year_sold_quantity) / 
                    sc.previous_year_sold_quantity * 100), 2)
        ELSE NULL 
    END as year_over_year_percent
FROM stock_cards sc
JOIN products p ON sc.product_id = p.product_id
WHERE sc.is_discontinued = false
  AND (sc.current_year_sold_quantity > 0 OR sc.previous_year_sold_quantity > 0)
ORDER BY year_over_year_percent DESC;
```

---

## 8. PRÍKLAD DÁT

```sql
-- Príklad 1: Bežný produkt s dostatočnou zásobou
INSERT INTO stock_cards (
    stock_id, product_id,
    beginning_quantity, beginning_value,
    total_in_quantity, total_in_value,
    total_out_quantity, total_out_value,
    quantity_on_hand, value_total,
    average_price, last_purchase_price, current_fifo_price,
    min_quantity, max_quantity, optimal_quantity,
    free_quantity,
    last_receipt_date, last_issue_date,
    created_by, updated_by
) VALUES (
    1, 12345,                                    -- Sklad 1, Produkt 12345
    100.000, 5000.00,                           -- Začiatok: 100 ks, 5000 €
    500.000, 26000.00,                          -- Príjem: 500 ks, 26000 €
    380.000, 19570.00,                          -- Výdaj: 380 ks, 19570 €
    220.000, 11430.00,                          -- Aktuálne: 220 ks, 11430 €
    51.95, 52.00, 51.90,                        -- Ceny: avg, last, fifo
    50.000, 300.000, 200.000,                   -- Normatívy: min, max, opt
    195.000,                                     -- Voľné: 195 (trigger vypočíta)
    '2025-12-01', '2025-12-10',                 -- Posledný príjem/výdaj
    'system', 'system'
);

-- Príklad 2: Produkt pod minimom (treba objednať)
INSERT INTO stock_cards (
    stock_id, product_id,
    beginning_quantity, beginning_value,
    quantity_on_hand, value_total,
    average_price, last_purchase_price,
    min_quantity, max_quantity, optimal_quantity,
    reserved_customer_orders,
    free_quantity,
    last_issue_date,
    created_by, updated_by
) VALUES (
    1, 67890,                                    -- Sklad 1, Produkt 67890
    200.000, 10000.00,                          -- Začiatok
    35.000, 1750.00,                            -- Aktuálne: ⚠️ POD MINIMOM
    50.00, 50.00,                               -- Ceny
    50.000, 300.000, 200.000,                   -- Min=50, aktuálne=35 ⚠️
    10.000,                                      -- Rezervované: 10
    25.000,                                      -- Voľné: 35 - 10 = 25
    '2025-12-08',                               -- Posledný výdaj
    'system', 'system'
);

-- Príklad 3: Produkt s vysokými rezerváciami
INSERT INTO stock_cards (
    stock_id, product_id,
    quantity_on_hand, value_total,
    average_price,
    reserved_customer_orders,
    reserved_other,
    sold_quantity,
    free_quantity,
    created_by, updated_by
) VALUES (
    2, 11111,                                    -- Sklad 2, Produkt 11111
    100.000, 8000.00,                           -- Aktuálne: 100 ks
    80.00,                                      -- Priemerná cena
    60.000,                                      -- Rezervované objednávky: 60
    15.000,                                      -- Iné rezervácie: 15
    5.000,                                       -- Predané (neodpočítané): 5
    20.000,                                      -- Voľné: 100-60-15-5 = 20
    'system', 'system'
);

-- Príklad 4: Vyradený produkt
INSERT INTO stock_cards (
    stock_id, product_id,
    quantity_on_hand, value_total,
    average_price,
    is_discontinued,
    created_by, updated_by
) VALUES (
    1, 99999,                                    -- Sklad 1, Produkt 99999
    0.000, 0.00,                                -- Nula zásob
    25.00,                                      -- Posledná cena
    true,                                        -- ❌ VYRADENÉ
    'system', 'system'
);
```

---

## 9. POZNÁMKY PRE MIGRÁCIU

### Python príklad načítania z viacerých Btrieve súborov

```python
from btrieve import Btrieve
import psycopg2
from datetime import datetime
import os
import glob

def migrate_stock_cards():
    # Pripojiť sa na PostgreSQL
    conn = psycopg2.connect(
        host="localhost",
        database="nex_automat",
        user="postgres",
        password="password"
    )
    cur = conn.cursor()
    
    # Nájsť všetky STK súbory (STK00001.BTR, STK00002.BTR, ...)
    stk_files = glob.glob('STK?????.BTR')
    
    print(f"Našiel som {len(stk_files)} skladových súborov")
    
    for stk_file in sorted(stk_files):
        # Extrahovať číslo skladu z názvu súboru
        # STK00001.BTR → stock_id = 1
        stock_id = int(stk_file[3:8])
        
        print(f"Migrujem {stk_file} (stock_id={stock_id})...")
        
        # Otvoriť Btrieve súbor
        btr = Btrieve()
        btr.open(stk_file, 'r')
        
        # Prechádzať záznamy
        for record in btr:
            # Zlúčenie dátumu a času
            updated_at = None
            if record.get('ModDate') and record.get('ModTime'):
                updated_at = datetime.combine(
                    record['ModDate'], 
                    record['ModTime']
                )
            
            # INSERT do PostgreSQL
            cur.execute("""
                INSERT INTO stock_cards (
                    stock_id, product_id,
                    beginning_quantity, beginning_value,
                    total_in_quantity, total_in_value,
                    total_out_quantity, total_out_value,
                    quantity_on_hand, value_total,
                    sold_quantity, unavailable_quantity,
                    reserved_customer_orders, reserved_other,
                    free_quantity, free_order_quantity,
                    ordered_quantity, available_supplier_quantity,
                    incoming_reserved_quantity, location_quantity,
                    average_price, last_purchase_price, current_fifo_price,
                    max_quantity, min_quantity, optimal_quantity,
                    last_receipt_date, last_issue_date,
                    last_receipt_quantity, last_issue_quantity,
                    last_inventory_date,
                    current_year_sold_quantity, current_year_issued_quantity,
                    previous_year_sold_quantity, previous_year_issued_quantity,
                    unreleased_serial_count,
                    last_supplier_id,
                    is_discontinued,
                    unsettled_quantity,
                    updated_at, updated_by
                ) VALUES (
                    %s, %s,
                    %s, %s,
                    %s, %s,
                    %s, %s,
                    %s, %s,
                    %s, %s,
                    %s, %s,
                    %s, %s,
                    %s, %s,
                    %s, %s,
                    %s, %s, %s,
                    %s, %s, %s,
                    %s, %s,
                    %s, %s,
                    %s,
                    %s, %s,
                    %s, %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s, %s
                )
                ON CONFLICT (stock_id, product_id) DO UPDATE SET
                    quantity_on_hand = EXCLUDED.quantity_on_hand,
                    value_total = EXCLUDED.value_total,
                    updated_at = EXCLUDED.updated_at
            """, (
                stock_id, record['GsCode'],
                record.get('BegQnt', 0), record.get('BegVal', 0),
                record.get('InQnt', 0), record.get('InVal', 0),
                record.get('OutQnt', 0), record.get('OutVal', 0),
                record.get('ActQnt', 0), record.get('ActVal', 0),
                record.get('SalQnt', 0), record.get('NrsQnt', 0),
                record.get('OcdQnt', 0), record.get('OsrQnt', 0),
                record.get('FreQnt', 0), record.get('FroQnt', 0),
                record.get('OsdQnt', 0), record.get('OfrQnt', 0),
                record.get('ImrQnt', 0), record.get('PosQnt', 0),
                record.get('AvgPrice', 0), record.get('LastPrice', 0), 
                record.get('ActPrice', 0),
                record.get('MaxQnt'), record.get('MinQnt'), 
                record.get('OptQnt'),
                record.get('LastIDate'), record.get('LastODate'),
                record.get('LastIQnt'), record.get('LastOQnt'),
                record.get('InvDate'),
                record.get('ASaQnt', 0), record.get('AOuQnt', 0),
                record.get('PSaQnt', 0), record.get('POuQnt', 0),
                record.get('ActSnQnt', 0),
                record.get('LinPac') if record.get('LinPac') else None,
                record.get('DisFlag', 0) == 1,
                record.get('NsuQnt', 0),
                updated_at, record.get('ModUser')
            ))
        
        btr.close()
        print(f"  → Hotovo: {stk_file}")
    
    conn.commit()
    cur.close()
    conn.close()
    
    print("Migrácia stock_cards dokončená!")

if __name__ == '__main__':
    migrate_stock_cards()
```

### Dôležité upozornenia

1. **Multi-sklad architektúra:**
   - Btrieve: Viacero súborov (STK00001.BTR, STK00002.BTR, ...)
   - PostgreSQL: Jedna tabuľka + stock_id
   - PK: Composite (stock_id, product_id)

2. **Denormalizované polia SA NEPRENÁŠAJÚ:**
   - Všetky údaje z `products` (názov, jednotka, DPH, typ...)
   - Získame cez `JOIN` na `products` tabuľku

3. **Vypočítané polia:**
   - `free_quantity` = automatický trigger
   - `MinMax` príznak → nahradené query

4. **Metódy oceňovania:**
   - AVCO: `average_price` (hlavná metóda)
   - FIFO: `current_fifo_price` (vyžaduje FIFO karty - samostatná tabuľka)
   - Last: `last_purchase_price`

5. **Negatívne stavy:**
   - CHECK constraint: `quantity_on_hand >= 0`
   - Ale `free_quantity` môže byť záporné (viac rezervácií ako zásob)

6. **Trigger aktualizácie:**
   - `stock_movements` INSERT/UPDATE → aktualizuje `stock_cards`
   - Automatický prepočet `quantity_on_hand`, `value_total`, `average_price`

7. **Validácie:**
   - Normatívy: min ≤ opt ≤ max
   - Množstvá ≥ 0
   - Ceny ≥ 0
   - Hodnoty ≥ 0

8. **Indexy:**
   - Composite PK: (stock_id, product_id)
   - Jednotlivé: stock_id, product_id
   - Výkonové: quantity, value, prices, dates

---

## 10. VERZIA A ZMENY

| Verzia | Dátum | Autor | Zmeny |
|--------|-------|-------|-------|
| 1.0 | 2025-12-11 | Zoltán + Claude | Prvá verzia dokumentácie stock_cards |

**Status:** ✅ Kompletný  
**Session:** 5  
**Súbor:** `docs/architecture/database/stock/cards/tables/STK-stock_cards.md`

---

## DODATOČNÉ POZNÁMKY

### Budúce rozšírenia

1. **stock_movements** (POHYB.BTR)
   - Detailné pohyby zásob (príjmy, výdaje, korekcie, prevody)
   - Aktualizuje `stock_cards` cez triggery

2. **stock_batches** (ak existuje ŠARŽE.BTR)
   - Sledovanie šarží a trvanlivosti
   - Pre produkty kde `track_expiration = true`

3. **stock_reservations**
   - Detailné rezervácie (kto, na čo, kedy)
   - Agregované do `reserved_customer_orders`, `reserved_other`

4. **stock_fifo_cards**
   - FIFO karty pre oceňovanie
   - Potrebné pre `current_fifo_price`

5. **stock_locations** (pozičné miesta)
   - DefPos → samostatná tabuľka?
   - Sledovanie pozícií v sklade

6. **stock_serial_numbers** (výrobné čísla)
   - Pre produkty kde `track_serial_numbers = true`
   - ActSnQnt = COUNT(*)

### Optimalizácia výkonu

```sql
-- Materializovaný view pre agregáciu
CREATE MATERIALIZED VIEW stock_totals AS
SELECT 
    product_id,
    SUM(quantity_on_hand) as total_quantity,
    SUM(value_total) as total_value,
    SUM(free_quantity) as total_free
FROM stock_cards
WHERE is_discontinued = false
GROUP BY product_id;

CREATE UNIQUE INDEX idx_stock_totals_product ON stock_totals(product_id);

-- Refresh periodicky
REFRESH MATERIALIZED VIEW CONCURRENTLY stock_totals;
```