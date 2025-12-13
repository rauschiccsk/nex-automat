# STMnnnnn.BTR → stock_card_movements

## 1. PREHĽAD

**Účel:** Denník skladových pohybov - kompletný záznam všetkých príjmov, výdajov a korekcií zásob.

**Charakteristika:**
- Všetky pohyby zásob (príjem/výdaj/korekcia/prevod)
- Každý príjem = 1 STM záznam = 1 FIFO karta
- Každý výdaj = 1 alebo viacero STM záznamov (podľa FIFO logiky)
- Prepojenie na FIFO karty (FifNum)
- Sleduje typ pohybu (SmCode), partnera, hodnotu
- Umožňuje audit trail a históriu zmien

**Btrieve architektúra:**
- NEX Genesis: `STM00001.BTR` (sklad 1), `STM00002.BTR` (sklad 2), ...
- Samostatný súbor pre každý sklad

**PostgreSQL architektúra:**
- `stock_card_movements` - jedna tabuľka pre všetky sklady
- Pridané pole: `stock_id` (číslo skladu)
- PK: `movement_id` (BIGSERIAL)

**Vzťahy:**
- Parent: `stock_cards` (N:1), `stock_card_fifos` (N:1), `partners` (N:1)
- Trigger: Aktualizuje `stock_cards` a `stock_card_fifos`

**Btrieve súbor:** `STMnnnnn.BTR` (n = číslo skladu)  
**Primárny kľúč:** StmNum (LONGINT)  
**PostgreSQL PK:** movement_id (BIGSERIAL)

---

## 2. KOMPLEXNÁ SQL SCHÉMA

```sql
-- =====================================================
-- Table: stock_card_movements
-- Purpose: Denník skladových pohybov (všetky príjmy, výdaje, korekcie)
-- =====================================================

CREATE TABLE stock_card_movements (
    -- Primárny kľúč (musí byť unique naprieč skladmi)
    movement_id             BIGSERIAL PRIMARY KEY,
    
    -- Sklad (pridané pre PostgreSQL)
    stock_id                INTEGER NOT NULL,
    
    -- Produkt
    product_id              INTEGER NOT NULL,
    
    -- Doklad
    document_number         VARCHAR(12) NOT NULL,
    document_line_number    INTEGER NOT NULL,
    document_date           DATE NOT NULL,
    
    -- Typ pohybu
    movement_type_code      INTEGER NOT NULL,
    -- Príklady: 1=Príjem nákup, 2=Výdaj predaj, 3=Korekcia+, 4=Korekcia-, 
    --           5=Prevod IN, 6=Prevod OUT, 7=Inventúra, atď.
    
    -- FIFO karta (len pri príjme alebo výdaji z FIFO)
    fifo_id                 BIGINT,
    
    -- Množstvo (+ príjem, - výdaj)
    quantity                DECIMAL(15,3) NOT NULL,
    
    -- Hodnoty
    cost_value              DECIMAL(15,2) NOT NULL,      -- Nákupná hodnota bez DPH (CValue)
    
    -- Partner (dodávateľ alebo odberateľ)
    partner_id              INTEGER,                      -- PaCode (hlavný partner)
    supplier_id             INTEGER,                      -- SpaCode (originálny dodávateľ)
    
    -- Protisklad (pri prevodoch medzi skladmi)
    contra_stock_id         INTEGER,                      -- ConStk
    
    -- Príznak počiatočného stavu
    is_beginning_balance    BOOLEAN NOT NULL DEFAULT false, -- BegStat = 'B'
    
    -- Audit polia
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by              VARCHAR(50),
    updated_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by              VARCHAR(50),
    
    -- Foreign Keys
    CONSTRAINT fk_stock_card_movements_stock
        FOREIGN KEY (stock_id) 
        REFERENCES stocks(stock_id)
        ON DELETE RESTRICT,
    
    CONSTRAINT fk_stock_card_movements_product
        FOREIGN KEY (product_id) 
        REFERENCES products(product_id)
        ON DELETE RESTRICT,
    
    CONSTRAINT fk_stock_card_movements_fifo
        FOREIGN KEY (fifo_id) 
        REFERENCES stock_card_fifos(fifo_id)
        ON DELETE SET NULL,  -- Ak zmazať FIFO, ponechať záznam
    
    CONSTRAINT fk_stock_card_movements_stock_card
        FOREIGN KEY (stock_id, product_id) 
        REFERENCES stock_cards(stock_id, product_id)
        ON DELETE RESTRICT,
    
    CONSTRAINT fk_stock_card_movements_partner
        FOREIGN KEY (partner_id) 
        REFERENCES partners(partner_id)
        ON DELETE SET NULL,
    
    CONSTRAINT fk_stock_card_movements_supplier
        FOREIGN KEY (supplier_id) 
        REFERENCES partners(partner_id)
        ON DELETE SET NULL,
    
    CONSTRAINT fk_stock_card_movements_contra_stock
        FOREIGN KEY (contra_stock_id) 
        REFERENCES stocks(stock_id)
        ON DELETE SET NULL
);

-- Indexy pre výkon
CREATE INDEX idx_stock_card_movements_stock ON stock_card_movements(stock_id);
CREATE INDEX idx_stock_card_movements_product ON stock_card_movements(product_id);
CREATE INDEX idx_stock_card_movements_stock_card ON stock_card_movements(stock_id, product_id);
CREATE INDEX idx_stock_card_movements_document ON stock_card_movements(document_number, document_line_number);
CREATE INDEX idx_stock_card_movements_doc_date ON stock_card_movements(document_date);
CREATE INDEX idx_stock_card_movements_type ON stock_card_movements(movement_type_code);
CREATE INDEX idx_stock_card_movements_fifo ON stock_card_movements(fifo_id);
CREATE INDEX idx_stock_card_movements_partner ON stock_card_movements(partner_id);
CREATE INDEX idx_stock_card_movements_supplier ON stock_card_movements(supplier_id);
CREATE INDEX idx_stock_card_movements_contra_stock ON stock_card_movements(contra_stock_id);

-- Composite indexy pre časté queries
CREATE INDEX idx_stock_card_movements_product_date ON stock_card_movements(product_id, document_date DESC);
CREATE INDEX idx_stock_card_movements_stock_date ON stock_card_movements(stock_id, document_date DESC);
CREATE INDEX idx_stock_card_movements_type_date ON stock_card_movements(movement_type_code, document_date DESC);

-- Komentáre
COMMENT ON TABLE stock_card_movements IS 'Denník skladových pohybov - kompletný záznam všetkých príjmov a výdajov';
COMMENT ON COLUMN stock_card_movements.movement_id IS 'ID pohybu (z Btrieve StmNum, unique naprieč skladmi)';
COMMENT ON COLUMN stock_card_movements.stock_id IS 'ID skladu (pridané pre PostgreSQL multi-sklad)';
COMMENT ON COLUMN stock_card_movements.movement_type_code IS 'Typ pohybu (1=Príjem, 2=Výdaj, 3=Korekcia+, atď.)';
COMMENT ON COLUMN stock_card_movements.quantity IS 'Množstvo (+ príjem, - výdaj)';
COMMENT ON COLUMN stock_card_movements.fifo_id IS 'Odkaz na FIFO kartu (len pri príjme alebo výdaji z FIFO)';
COMMENT ON COLUMN stock_card_movements.contra_stock_id IS 'Protisklad (pri prevodoch medzi skladmi)';
COMMENT ON COLUMN stock_card_movements.is_beginning_balance IS 'Príznak počiatočného stavu (začiatok roka)';

-- Trigger pre updated_at
CREATE TRIGGER update_stock_card_movements_updated_at
    BEFORE UPDATE ON stock_card_movements
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger pre automatickú aktualizáciu stock_cards a stock_card_fifos
CREATE OR REPLACE FUNCTION update_stock_card_on_movement()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        -- Aktualizovať stock_cards
        IF NEW.quantity > 0 THEN
            -- Príjem
            UPDATE stock_cards
            SET quantity_on_hand = quantity_on_hand + NEW.quantity,
                value_total = value_total + NEW.cost_value,
                total_in_quantity = total_in_quantity + NEW.quantity,
                total_in_value = total_in_value + NEW.cost_value,
                last_receipt_date = NEW.document_date,
                last_receipt_quantity = NEW.quantity,
                updated_at = CURRENT_TIMESTAMP,
                updated_by = NEW.created_by
            WHERE stock_id = NEW.stock_id AND product_id = NEW.product_id;
        ELSE
            -- Výdaj
            UPDATE stock_cards
            SET quantity_on_hand = quantity_on_hand + NEW.quantity,  -- quantity je záporné!
                value_total = value_total + NEW.cost_value,          -- cost_value je záporná!
                total_out_quantity = total_out_quantity + ABS(NEW.quantity),
                total_out_value = total_out_value + ABS(NEW.cost_value),
                last_issue_date = NEW.document_date,
                last_issue_quantity = ABS(NEW.quantity),
                updated_at = CURRENT_TIMESTAMP,
                updated_by = NEW.created_by
            WHERE stock_id = NEW.stock_id AND product_id = NEW.product_id;
        END IF;
        
        -- Aktualizovať FIFO kartu (ak je zadaná)
        IF NEW.fifo_id IS NOT NULL AND NEW.quantity < 0 THEN
            -- Výdaj z FIFO karty
            UPDATE stock_card_fifos
            SET issued_quantity = issued_quantity + ABS(NEW.quantity),
                remaining_quantity = remaining_quantity - ABS(NEW.quantity),
                updated_at = CURRENT_TIMESTAMP,
                updated_by = NEW.created_by
            WHERE fifo_id = NEW.fifo_id;
        END IF;
        
        -- Prepočítať average_price
        UPDATE stock_cards
        SET average_price = CASE 
            WHEN quantity_on_hand > 0 THEN value_total / quantity_on_hand 
            ELSE 0 
        END
        WHERE stock_id = NEW.stock_id AND product_id = NEW.product_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_stock_card_movements_update_card
    AFTER INSERT ON stock_card_movements
    FOR EACH ROW
    EXECUTE FUNCTION update_stock_card_on_movement();

-- Check constraints
ALTER TABLE stock_card_movements
ADD CONSTRAINT chk_stock_card_movements_quantity_not_zero
CHECK (quantity != 0);

ALTER TABLE stock_card_movements
ADD CONSTRAINT chk_stock_card_movements_quantity_logic
CHECK (
    -- Príjem: quantity > 0 AND fifo_id NOT NULL
    (quantity > 0) OR
    -- Výdaj: quantity < 0
    (quantity < 0)
);
```

---

## 3. MAPPING POLÍ

### Stock Card Movements

| Btrieve Pole | Typ Btrieve | PostgreSQL Pole | Typ PostgreSQL | Transformácia | Poznámka |
|--------------|-------------|-----------------|----------------|---------------|----------|
| **PRIDANÉ** | - | stock_id | INTEGER | - | Číslo skladu |
| StmNum | LONGINT | movement_id | BIGSERIAL | Priamo | PK (unique naprieč skladmi) |
| DocNum | STRING[12] | document_number | VARCHAR(12) | Priamo | Číslo dokladu |
| ItmNum | LONGINT | document_line_number | INTEGER | Priamo | Riadok dokladu |
| DocDate | DATE | document_date | DATE | Priamo | Dátum dokladu |
| SmCode | WORD | movement_type_code | INTEGER | Priamo | Typ pohybu |
| GsCode | LONGINT | product_id | INTEGER | Priamo | FK na products |
| FifNum | LONGINT | fifo_id | BIGINT | Priamo | FK na stock_card_fifos |
| GsQnt | DOUBLE | quantity | DECIMAL(15,3) | Priamo | + príjem, - výdaj |
| CValue | DOUBLE | cost_value | DECIMAL(15,2) | Priamo | Nákupná hodnota bez DPH |
| PaCode | LONGINT | partner_id | INTEGER | Priamo | FK na partners (hlavný) |
| SpaCode | LONGINT | supplier_id | INTEGER | Priamo | FK na partners (dodávateľ) |
| ConStk | WORD | contra_stock_id | INTEGER | Priamo | FK na stocks (protisklad) |
| BegStat | STRING[1] | is_beginning_balance | BOOLEAN | 'B'→true | Počiatočný stav |
| ModUser | STRING[8] | updated_by | VARCHAR(50) | Priamo | Audit |
| ModDate | DATE | updated_at | TIMESTAMP | Date+Time | Part of |
| ModTime | TIME | updated_at | TIMESTAMP | Date+Time | Part of |

### Polia ktoré SA NEPRENÁŠAJÚ

| Btrieve Pole | Dôvod neprenášania |
|--------------|-------------------|
| MgCode | Tovarová skupina (v products) |
| GsName | Názov tovaru (v products) |
| BValue | Hodnota v PC s DPH (vypočítaná z cost_value + DPH) |
| Sended | Technický príznak (NEX Genesis replikácia) |
| OcdNum, OcdItm | Objednávka (môže byť samostatná tabuľka customer_orders) |
| Bprice | Predajná cena s DPH (v products alebo price_lists) |
| AcqStat | Príznak obstarania R/K (nepotrebné) |

**Zlúčené polia:**
- `ModDate` + `ModTime` → `updated_at` (TIMESTAMP)

---

## 4. BIZNIS LOGIKA

### 1. Typy skladových pohybov (movement_type_code)

**Príklady kódov SmCode:**

```sql
-- Príjmy (quantity > 0)
1  = Príjem z nákupu
5  = Prevod IN (z iného skladu)
11 = Príjem z výroby
21 = Korekcia + (inventúra)
31 = Počiatočný stav

-- Výdaje (quantity < 0)
2  = Výdaj na predaj
6  = Prevod OUT (do iného skladu)
12 = Výdaj do výroby
22 = Korekcia - (inventúra)
32 = Reklamácia
```

**Poznámka:** Konkrétne kódy závisia od NEX Genesis konfigurácie!

### 2. Logika príjmu

**Príjem vytvorí:**
- 1 záznam v `stock_card_movements` (quantity > 0)
- 1 záznam v `stock_card_fifos` (nová FIFO karta)

```sql
-- Príklad: Príjem 100 ks tovaru
BEGIN TRANSACTION;

-- 1. Vytvor FIFO kartu
INSERT INTO stock_card_fifos (
    stock_id, product_id,
    document_number, document_line_number, document_date,
    supplier_id,
    received_quantity, issued_quantity, remaining_quantity,
    purchase_price,
    status
) VALUES (
    1, 12345,
    'PRI2025/0100', 1, '2025-12-11',
    5001,
    100.000, 0.000, 100.000,
    50.00,
    'A'
) RETURNING fifo_id INTO v_fifo_id;

-- 2. Vytvor movement záznam
INSERT INTO stock_card_movements (
    stock_id, product_id,
    document_number, document_line_number, document_date,
    movement_type_code,
    fifo_id,
    quantity,
    cost_value,
    partner_id
) VALUES (
    1, 12345,
    'PRI2025/0100', 1, '2025-12-11',
    1,  -- Príjem z nákupu
    v_fifo_id,
    100.000,  -- + množstvo
    5000.00,  -- 100 * 50 = 5000
    5001
);

-- 3. Trigger automaticky aktualizuje stock_cards
COMMIT;
```

### 3. Logika výdaja (jednoduchý prípad)

**Výdaj z jednej FIFO karty:**

```sql
-- Príklad: Výdaj 30 ks tovaru (FIFO #100001 má zostatok 70 ks)
INSERT INTO stock_card_movements (
    stock_id, product_id,
    document_number, document_line_number, document_date,
    movement_type_code,
    fifo_id,
    quantity,
    cost_value,
    partner_id
) VALUES (
    1, 12345,
    'VYD2025/0050', 1, '2025-12-11',
    2,  -- Výdaj na predaj
    100001,  -- Z tejto FIFO karty
    -30.000,  -- - množstvo (výdaj!)
    -1500.00,  -- -(30 * 50) = -1500
    2001  -- Odberateľ
);

-- Trigger automaticky:
-- 1. Aktualizuje stock_card_fifos (issued_quantity += 30, remaining -= 30)
-- 2. Aktualizuje stock_cards (quantity_on_hand -= 30, value -= 1500)
```

### 4. Logika výdaja (cez viacero FIFO kariet) ⭐

**Výdaj väčší ako zostatok najstaršej FIFO:**

```sql
-- Dostupné FIFO karty:
--   FIFO #100001 (2025-01-15): 50 ks zostatok
--   FIFO #100002 (2025-02-01): 200 ks zostatok
-- Výdaj: 120 ks

BEGIN TRANSACTION;

-- 1. Výdaj z FIFO #100001 (celý zostatok)
INSERT INTO stock_card_movements (
    stock_id, product_id,
    document_number, document_line_number, document_date,
    movement_type_code,
    fifo_id,
    quantity, cost_value,
    partner_id
) VALUES (
    1, 12345,
    'VYD2025/0060', 1, '2025-12-11',
    2,
    100001,
    -50.000, -2500.00,  -- 50 * 50 = 2500
    2001
);

-- 2. Výdaj z FIFO #100002 (zostatok 70 ks)
INSERT INTO stock_card_movements (
    stock_id, product_id,
    document_number, document_line_number, document_date,
    movement_type_code,
    fifo_id,
    quantity, cost_value,
    partner_id
) VALUES (
    1, 12345,
    'VYD2025/0060', 1, '2025-12-11',  -- Ten istý doklad!
    2,
    100002,
    -70.000, -3640.00,  -- 70 * 52 = 3640
    2001
);

COMMIT;

-- Výsledok:
-- - 2 záznamy v stock_card_movements pre jeden výdaj
-- - FIFO #100001: status = 'X' (spotrebovaná)
-- - FIFO #100002: remaining = 130 ks
-- - stock_cards: quantity_on_hand -= 120, value -= 6140
```

### 5. Prevody medzi skladmi

**Prevod = 2 pohyby:**

```sql
-- Prevod 20 ks z Skladu 1 → Sklad 2

-- 1. Výdaj zo Skladu 1 (ConStk = 2)
INSERT INTO stock_card_movements (
    stock_id, product_id,
    document_number, document_line_number, document_date,
    movement_type_code,
    fifo_id,
    quantity, cost_value,
    contra_stock_id
) VALUES (
    1, 12345,
    'PRV2025/0010', 1, '2025-12-11',
    6,  -- Prevod OUT
    100001,
    -20.000, -1000.00,
    2  -- Do skladu 2
);

-- 2. Príjem do Skladu 2 (ConStk = 1)
INSERT INTO stock_card_movements (
    stock_id, product_id,
    document_number, document_line_number, document_date,
    movement_type_code,
    quantity, cost_value,
    contra_stock_id
) VALUES (
    2, 12345,
    'PRV2025/0010', 1, '2025-12-11',
    5,  -- Prevod IN
    20.000, 1000.00,
    1  -- Zo skladu 1
);

-- Vytvorí sa nová FIFO karta v Sklade 2
```

### 6. Korekcie (inventúra)

```sql
-- Korekcia + (našli sme viac)
INSERT INTO stock_card_movements (
    stock_id, product_id,
    document_number, document_line_number, document_date,
    movement_type_code,
    quantity, cost_value
) VALUES (
    1, 12345,
    'INV2025/0001', 1, '2025-12-11',
    21,  -- Korekcia +
    5.000, 250.00  -- 5 * priemerná cena
);

-- Korekcia - (našli sme menej)
INSERT INTO stock_card_movements (
    stock_id, product_id,
    document_number, document_line_number, document_date,
    movement_type_code,
    fifo_id,  -- Môže byť z konkrétnej FIFO
    quantity, cost_value
) VALUES (
    1, 12345,
    'INV2025/0001', 2, '2025-12-11',
    22,  -- Korekcia -
    -3.000, -150.00
);
```

---

## 5. VZŤAHY S INÝMI TABUĽKAMI

```sql
-- Stock Card Movements → Stocks (N:1)
ALTER TABLE stock_card_movements
ADD CONSTRAINT fk_stock_card_movements_stock
FOREIGN KEY (stock_id) 
REFERENCES stocks(stock_id)
ON DELETE RESTRICT;

-- Stock Card Movements → Products (N:1)
ALTER TABLE stock_card_movements
ADD CONSTRAINT fk_stock_card_movements_product
FOREIGN KEY (product_id) 
REFERENCES products(product_id)
ON DELETE RESTRICT;

-- Stock Card Movements → Stock Card FIFOs (N:1, optional)
ALTER TABLE stock_card_movements
ADD CONSTRAINT fk_stock_card_movements_fifo
FOREIGN KEY (fifo_id) 
REFERENCES stock_card_fifos(fifo_id)
ON DELETE SET NULL;

-- Stock Card Movements → Stock Cards (N:1)
-- Composite FK
ALTER TABLE stock_card_movements
ADD CONSTRAINT fk_stock_card_movements_stock_card
FOREIGN KEY (stock_id, product_id) 
REFERENCES stock_cards(stock_id, product_id)
ON DELETE RESTRICT;

-- Stock Card Movements → Partners (N:1, optional)
-- Hlavný partner (dodávateľ/odberateľ)
ALTER TABLE stock_card_movements
ADD CONSTRAINT fk_stock_card_movements_partner
FOREIGN KEY (partner_id) 
REFERENCES partners(partner_id)
ON DELETE SET NULL;

-- Stock Card Movements → Partners (N:1, optional)
-- Originálny dodávateľ
ALTER TABLE stock_card_movements
ADD CONSTRAINT fk_stock_card_movements_supplier
FOREIGN KEY (supplier_id) 
REFERENCES partners(partner_id)
ON DELETE SET NULL;

-- Stock Card Movements → Stocks (N:1, optional)
-- Protisklad (pri prevodoch)
ALTER TABLE stock_card_movements
ADD CONSTRAINT fk_stock_card_movements_contra_stock
FOREIGN KEY (contra_stock_id) 
REFERENCES stocks(stock_id)
ON DELETE SET NULL;
```

### Diagram vzťahov

```
stocks (1) ----< (N) stock_card_movements (N) >---- (1) products
                         |
                         +---- (N) >---- (1) stock_card_fifos
                         |
                         +---- (N) >---- (1) stock_cards (composite FK)
                         |
                         +---- (N) >---- (1) partners (partner_id)
                         |
                         +---- (N) >---- (1) partners (supplier_id)
                         |
                         +---- (N) >---- (1) stocks (contra_stock_id)
```

---

## 6. VALIDAČNÉ PRAVIDLÁ

```sql
-- 1. Množstvo nesmie byť 0
ALTER TABLE stock_card_movements
ADD CONSTRAINT chk_stock_card_movements_quantity_not_zero
CHECK (quantity != 0);

-- 2. Príjem musí mať FIFO
ALTER TABLE stock_card_movements
ADD CONSTRAINT chk_stock_card_movements_receipt_fifo
CHECK (
    quantity <= 0 OR  -- Výdaj/korekcia - nemá FIFO
    fifo_id IS NOT NULL  -- Príjem - musí mať FIFO
);

-- 3. Logika contra_stock_id (len pri prevodoch)
ALTER TABLE stock_card_movements
ADD CONSTRAINT chk_stock_card_movements_contra_stock
CHECK (
    contra_stock_id IS NULL OR
    movement_type_code IN (5, 6)  -- Len pri prevodoch IN/OUT
);

-- 4. Trigger validácia FIFO karty
CREATE OR REPLACE FUNCTION validate_movement_fifo()
RETURNS TRIGGER AS $$
BEGIN
    -- Pri výdaji skontroluj či FIFO má dostatok
    IF NEW.quantity < 0 AND NEW.fifo_id IS NOT NULL THEN
        DECLARE
            v_remaining DECIMAL(15,3);
        BEGIN
            SELECT remaining_quantity INTO v_remaining
            FROM stock_card_fifos
            WHERE fifo_id = NEW.fifo_id;
            
            IF v_remaining < ABS(NEW.quantity) THEN
                RAISE EXCEPTION 'FIFO karta % nemá dostatok (available: %, required: %)', 
                    NEW.fifo_id, v_remaining, ABS(NEW.quantity);
            END IF;
        END;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_stock_card_movements_validate_fifo
    BEFORE INSERT ON stock_card_movements
    FOR EACH ROW
    EXECUTE FUNCTION validate_movement_fifo();
```

---

## 7. QUERY PATTERNS

### Základné queries

```sql
-- 1. História pohybov produktu
SELECT 
    m.movement_id,
    m.document_date,
    m.document_number,
    m.movement_type_code,
    m.quantity,
    m.cost_value,
    p.partner_name
FROM stock_card_movements m
LEFT JOIN partners p ON m.partner_id = p.partner_id
WHERE m.stock_id = 1
  AND m.product_id = 12345
ORDER BY m.document_date DESC, m.movement_id DESC;

-- 2. Denný sumár pohybov
SELECT 
    document_date,
    SUM(CASE WHEN quantity > 0 THEN quantity ELSE 0 END) as total_receipts,
    SUM(CASE WHEN quantity < 0 THEN ABS(quantity) ELSE 0 END) as total_issues,
    SUM(quantity) as net_movement,
    COUNT(*) as movement_count
FROM stock_card_movements
WHERE stock_id = 1
  AND document_date >= '2025-12-01'
GROUP BY document_date
ORDER BY document_date;

-- 3. Pohyby podľa typu
SELECT 
    movement_type_code,
    COUNT(*) as movement_count,
    SUM(quantity) as total_quantity,
    SUM(cost_value) as total_value
FROM stock_card_movements
WHERE stock_id = 1
  AND document_date BETWEEN '2025-12-01' AND '2025-12-31'
GROUP BY movement_type_code
ORDER BY movement_type_code;

-- 4. Pohyby s konkrétnym dokladom
SELECT 
    m.*,
    p.product_name,
    pa.partner_name
FROM stock_card_movements m
JOIN products p ON m.product_id = p.product_id
LEFT JOIN partners pa ON m.partner_id = pa.partner_id
WHERE m.document_number = 'PRI2025/0100'
ORDER BY m.document_line_number;

-- 5. Pohyby z/do FIFO karty
SELECT 
    m.movement_id,
    m.document_date,
    m.document_number,
    m.quantity,
    f.received_quantity,
    f.issued_quantity,
    f.remaining_quantity
FROM stock_card_movements m
JOIN stock_card_fifos f ON m.fifo_id = f.fifo_id
WHERE f.fifo_id = 100001
ORDER BY m.document_date;
```

### Pokročilé queries

```sql
-- 6. Prevody medzi skladmi
SELECT 
    m1.movement_id as out_movement_id,
    m2.movement_id as in_movement_id,
    m1.document_number,
    m1.document_date,
    s1.stock_name as from_stock,
    s2.stock_name as to_stock,
    p.product_name,
    ABS(m1.quantity) as quantity
FROM stock_card_movements m1
JOIN stock_card_movements m2 
    ON m1.document_number = m2.document_number
   AND m1.product_id = m2.product_id
   AND m1.contra_stock_id = m2.stock_id
   AND m2.contra_stock_id = m1.stock_id
JOIN stocks s1 ON m1.stock_id = s1.stock_id
JOIN stocks s2 ON m2.stock_id = s2.stock_id
JOIN products p ON m1.product_id = p.product_id
WHERE m1.movement_type_code = 6  -- Prevod OUT
  AND m2.movement_type_code = 5  -- Prevod IN
ORDER BY m1.document_date DESC;

-- 7. Inventúrne korekcie
SELECT 
    m.document_date,
    m.document_number,
    p.product_code,
    p.product_name,
    m.quantity,
    m.cost_value,
    CASE m.movement_type_code
        WHEN 21 THEN 'Korekcia +'
        WHEN 22 THEN 'Korekcia -'
    END as correction_type
FROM stock_card_movements m
JOIN products p ON m.product_id = p.product_id
WHERE m.movement_type_code IN (21, 22)
  AND m.document_date >= '2025-12-01'
ORDER BY m.document_date DESC;

-- 8. Top dodávatelia (podľa objemu príjmov)
SELECT 
    p.partner_id,
    p.partner_name,
    COUNT(m.movement_id) as receipt_count,
    SUM(m.quantity) as total_quantity,
    SUM(m.cost_value) as total_value
FROM stock_card_movements m
JOIN partners p ON m.partner_id = p.partner_id
WHERE m.movement_type_code = 1  -- Príjem z nákupu
  AND m.document_date >= '2025-01-01'
GROUP BY p.partner_id, p.partner_name
ORDER BY total_value DESC
LIMIT 10;

-- 9. Obrátkovosť - pohyby vs. priemerná zásoba
WITH monthly_movements AS (
    SELECT 
        product_id,
        DATE_TRUNC('month', document_date) as month,
        SUM(CASE WHEN quantity < 0 THEN ABS(quantity) ELSE 0 END) as issued_quantity
    FROM stock_card_movements
    WHERE stock_id = 1
      AND document_date >= '2025-01-01'
    GROUP BY product_id, DATE_TRUNC('month', document_date)
),
avg_stock AS (
    SELECT 
        product_id,
        AVG(quantity_on_hand) as avg_quantity
    FROM stock_cards
    WHERE stock_id = 1
    GROUP BY product_id
)
SELECT 
    p.product_id,
    p.product_name,
    mm.issued_quantity,
    a.avg_quantity,
    CASE 
        WHEN a.avg_quantity > 0 
        THEN ROUND((mm.issued_quantity / a.avg_quantity), 2)
        ELSE 0 
    END as turnover_ratio
FROM monthly_movements mm
JOIN products p ON mm.product_id = p.product_id
JOIN avg_stock a ON mm.product_id = a.product_id
WHERE mm.month = '2025-12-01'
ORDER BY turnover_ratio DESC;

-- 10. Audit trail - kompletná história produktu
SELECT 
    m.document_date,
    m.document_number,
    m.movement_type_code,
    m.quantity,
    m.cost_value,
    pa.partner_name as partner,
    f.fifo_id,
    f.remaining_quantity as fifo_remaining,
    m.created_by,
    m.created_at
FROM stock_card_movements m
LEFT JOIN partners pa ON m.partner_id = pa.partner_id
LEFT JOIN stock_card_fifos f ON m.fifo_id = f.fifo_id
WHERE m.stock_id = 1
  AND m.product_id = 12345
ORDER BY m.created_at DESC;
```

---

## 8. PRÍKLAD DÁT

```sql
-- Príklad 1: Príjem z nákupu
INSERT INTO stock_card_movements (
    movement_id, stock_id, product_id,
    document_number, document_line_number, document_date,
    movement_type_code,
    fifo_id,
    quantity, cost_value,
    partner_id,
    created_by, updated_by
) VALUES (
    200001, 1, 12345,
    'PRI2025/0100', 1, '2025-12-11',
    1,  -- Príjem z nákupu
    100001,  -- FIFO karta
    100.000, 5000.00,  -- + 100 ks, hodnota 5000 €
    5001,  -- Dodávateľ
    'user1', 'user1'
);

-- Príklad 2: Výdaj na predaj (z jednej FIFO)
INSERT INTO stock_card_movements (
    movement_id, stock_id, product_id,
    document_number, document_line_number, document_date,
    movement_type_code,
    fifo_id,
    quantity, cost_value,
    partner_id,
    created_by, updated_by
) VALUES (
    200002, 1, 12345,
    'VYD2025/0050', 1, '2025-12-11',
    2,  -- Výdaj na predaj
    100001,  -- Z tejto FIFO
    -30.000, -1500.00,  -- - 30 ks, hodnota -1500 €
    2001,  -- Odberateľ
    'user2', 'user2'
);

-- Príklad 3a: Výdaj (z viacerých FIFO) - prvá časť
INSERT INTO stock_card_movements (
    movement_id, stock_id, product_id,
    document_number, document_line_number, document_date,
    movement_type_code,
    fifo_id,
    quantity, cost_value,
    partner_id,
    created_by, updated_by
) VALUES (
    200003, 1, 12345,
    'VYD2025/0060', 1, '2025-12-11',
    2,  -- Výdaj na predaj
    100001,  -- Celý zostatok z tejto FIFO
    -70.000, -3500.00,  -- Zostatok 70 ks
    2002,  -- Odberateľ
    'user2', 'user2'
);

-- Príklad 3b: Výdaj (z viacerých FIFO) - druhá časť
INSERT INTO stock_card_movements (
    movement_id, stock_id, product_id,
    document_number, document_line_number, document_date,
    movement_type_code,
    fifo_id,
    quantity, cost_value,
    partner_id,
    created_by, updated_by
) VALUES (
    200004, 1, 12345,
    'VYD2025/0060', 1, '2025-12-11',  -- Ten istý doklad!
    2,  -- Výdaj na predaj
    100002,  -- Ďalšia FIFO v poradí
    -50.000, -2600.00,  -- Ďalších 50 ks z novšej FIFO
    2002,  -- Ten istý odberateľ
    'user2', 'user2'
);

-- Príklad 4: Prevod OUT (do iného skladu)
INSERT INTO stock_card_movements (
    movement_id, stock_id, product_id,
    document_number, document_line_number, document_date,
    movement_type_code,
    fifo_id,
    quantity, cost_value,
    contra_stock_id,
    created_by, updated_by
) VALUES (
    200005, 1, 12345,
    'PRV2025/0010', 1, '2025-12-11',
    6,  -- Prevod OUT
    100002,
    -20.000, -1040.00,
    2,  -- Do skladu 2
    'user3', 'user3'
);

-- Príklad 5: Prevod IN (z iného skladu)
INSERT INTO stock_card_movements (
    movement_id, stock_id, product_id,
    document_number, document_line_number, document_date,
    movement_type_code,
    fifo_id,
    quantity, cost_value,
    contra_stock_id,
    created_by, updated_by
) VALUES (
    200006, 2, 12345,
    'PRV2025/0010', 1, '2025-12-11',
    5,  -- Prevod IN
    100050,  -- Nová FIFO karta v Sklade 2
    20.000, 1040.00,
    1,  -- Zo skladu 1
    'user3', 'user3'
);

-- Príklad 6: Korekcia + (inventúra)
INSERT INTO stock_card_movements (
    movement_id, stock_id, product_id,
    document_number, document_line_number, document_date,
    movement_type_code,
    quantity, cost_value,
    created_by, updated_by
) VALUES (
    200007, 1, 12345,
    'INV2025/0001', 1, '2025-12-11',
    21,  -- Korekcia +
    5.000, 250.00,  -- Našli sme 5 ks navyše
    'user4', 'user4'
);

-- Príklad 7: Počiatočný stav
INSERT INTO stock_card_movements (
    movement_id, stock_id, product_id,
    document_number, document_line_number, document_date,
    movement_type_code,
    fifo_id,
    quantity, cost_value,
    is_beginning_balance,
    created_by, updated_by
) VALUES (
    100000, 1, 67890,
    'BEGIN2025', 1, '2025-01-01',
    31,  -- Počiatočný stav
    90000,  -- FIFO karta počiatočného stavu
    150.000, 6750.00,
    true,  -- ⭐ Počiatočný stav
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
import glob

def migrate_stock_card_movements():
    conn = psycopg2.connect(
        host="localhost",
        database="nex_automat",
        user="postgres",
        password="password"
    )
    cur = conn.cursor()
    
    # Nájsť všetky STM súbory (STM00001.BTR, STM00002.BTR, ...)
    stm_files = glob.glob('STM?????.BTR')
    
    print(f"Našiel som {len(stm_files)} movement súborov")
    
    for stm_file in sorted(stm_files):
        # Extrahovať číslo skladu z názvu súboru
        # STM00001.BTR → stock_id = 1
        stock_id = int(stm_file[3:8])
        
        print(f"Migrujem {stm_file} (stock_id={stock_id})...")
        
        # Otvoriť Btrieve súbor
        btr = Btrieve()
        btr.open(stm_file, 'r')
        
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
                INSERT INTO stock_card_movements (
                    movement_id, stock_id, product_id,
                    document_number, document_line_number, document_date,
                    movement_type_code,
                    fifo_id,
                    quantity, cost_value,
                    partner_id, supplier_id,
                    contra_stock_id,
                    is_beginning_balance,
                    updated_at, updated_by
                ) VALUES (
                    %s, %s, %s,
                    %s, %s, %s,
                    %s,
                    %s,
                    %s, %s,
                    %s, %s,
                    %s,
                    %s,
                    %s, %s
                )
                ON CONFLICT (movement_id) DO NOTHING
            """, (
                record['StmNum'], stock_id, record['GsCode'],
                record['DocNum'], record['ItmNum'], record['DocDate'],
                record['SmCode'],
                record.get('FifNum') if record.get('FifNum') else None,
                record['GsQnt'], record['CValue'],
                record.get('PaCode') if record.get('PaCode') else None,
                record.get('SpaCode') if record.get('SpaCode') else None,
                record.get('ConStk') if record.get('ConStk') else None,
                record.get('BegStat') == 'B',
                updated_at, record.get('ModUser')
            ))
        
        btr.close()
        print(f"  → Hotovo: {stm_file}")
    
    conn.commit()
    cur.close()
    conn.close()
    
    print("Migrácia stock_card_movements dokončená!")

if __name__ == '__main__':
    migrate_stock_card_movements()
```

### Dôležité upozornenia

1. **Multi-sklad architektúra:**
   - Btrieve: Viacero súborov (STM00001.BTR, STM00002.BTR, ...)
   - PostgreSQL: Jedna tabuľka + stock_id
   - PK: movement_id (unique naprieč skladmi)

2. **Neprenášané polia:**
   - `MgCode`, `GsName` - v products tabuľke
   - `BValue` - predajná hodnota s DPH (vypočítaná)
   - `Sended` - technický príznak replikácie
   - `OcdNum`, `OcdItm` - objednávky (samostatná tabuľka?)
   - `Bprice` - predajná cena (v products/price_lists)
   - `AcqStat` - príznak obstarania (nepotrebné)

3. **Triggery aktualizujú:**
   - `stock_cards`: quantity_on_hand, value_total, average_price
   - `stock_card_fifos`: issued_quantity, remaining_quantity, status

4. **Validácie:**
   - Množstvo != 0
   - Príjem → musí mať fifo_id
   - Výdaj → kontrola dostatku v FIFO
   - Prevody → contra_stock_id

5. **Výdaj cez viacero FIFO:**
   - Jeden doklad = viacero STM záznamov
   - Každý s iným fifo_id
   - Rovnaký document_number a document_line_number

6. **Typy pohybov (SmCode):**
   - Závisia od NEX Genesis konfigurácie
   - Potrebné mapovať konkrétne kódy

7. **Prevody medzi skladmi:**
   - 2 movements (OUT + IN)
   - contra_stock_id pre prepojenie
   - Rovnaký document_number

8. **Počiatočný stav:**
   - `is_beginning_balance = true`
   - Špeciálny doklad "BEGIN2025"
   - Vytvorí FIFO kartu

---

## 10. VERZIA A ZMENY

| Verzia | Dátum | Autor | Zmeny |
|--------|-------|-------|-------|
| 1.0 | 2025-12-11 | Zoltán + Claude | Prvá verzia dokumentácie stock_card_movements |

**Status:** ✅ Kompletný  
**Session:** 5  
**Súbor:** `docs/architecture/database/stock/cards/tables/STM-stock_card_movements.md`