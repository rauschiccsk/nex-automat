# FIFnnnnn.BTR → stock_card_fifos

## 1. PREHĽAD

**Účel:** FIFO karty zásob - sledovanie jednotlivých príjmov a ich postupné vyskladnenie.

**Charakteristika:**
- Každý príjem tovaru vytvorí novú FIFO kartu
- Výdaj sa realizuje z najstaršej aktívnej karty (FIFO princíp)
- Sleduje bilanciu: Prijaté - Vydané = Zostatok
- Statusy: A (aktívna), W (čakajúca), X (spotrebovaná)
- Eviduje trvanlivosť (DrbDate), šarže (RbaCode)
- Prepojené so skladovými pohybmi (STM) cez FifNum

**Btrieve architektúra:**
- NEX Genesis: `FIF00001.BTR` (sklad 1), `FIF00002.BTR` (sklad 2), ...
- Samostatný súbor pre každý sklad

**PostgreSQL architektúra:**
- `stock_card_fifos` - jedna tabuľka pre všetky sklady
- Pridané pole: `stock_id` (číslo skladu)
- PK: `fifo_id` (z FifNum, ale musí byť unique naprieč skladmi)

**Vzťahy:**
- Parent: `stock_cards` (N:1), `partners` (N:1, dodávateľ)
- Child: `stock_card_movements` (1:N)
- Related: `stock_batches` (1:N, šarže)

**Btrieve súbor:** `FIFnnnnn.BTR` (n = číslo skladu)  
**Primárny kľúč:** FifNum (LONGINT)  
**PostgreSQL PK:** fifo_id (BIGINT)

---

## 2. KOMPLEXNÁ SQL SCHÉMA

```sql
-- =====================================================
-- Table: stock_card_fifos
-- Purpose: FIFO karty zásob (sledovanie príjmov a ich vyskladnenia)
-- =====================================================

CREATE TABLE stock_card_fifos (
    -- Primárny kľúč (musí byť unique naprieč skladmi)
    fifo_id                 BIGSERIAL PRIMARY KEY,
    
    -- Sklad (pridané pre PostgreSQL)
    stock_id                INTEGER NOT NULL,
    
    -- Produkt
    product_id              INTEGER NOT NULL,
    
    -- Príjmový doklad
    document_number         VARCHAR(12) NOT NULL,
    document_line_number    INTEGER NOT NULL,
    document_date           DATE NOT NULL,
    
    -- Dodávateľ
    supplier_id             INTEGER,
    
    -- Množstvá
    received_quantity       DECIMAL(15,3) NOT NULL,      -- InQnt (prijaté)
    issued_quantity         DECIMAL(15,3) NOT NULL DEFAULT 0, -- OutQnt (vydané)
    remaining_quantity      DECIMAL(15,3) NOT NULL,      -- ActQnt (zostatok)
    
    -- Nákupná cena (bez DPH)
    purchase_price          DECIMAL(15,2) NOT NULL,      -- InPrice
    
    -- Trvanlivosť
    expiration_date         DATE,                        -- DrbDate
    
    -- Šarža
    batch_code              VARCHAR(30),                 -- RbaCode
    batch_date              DATE,                        -- RbaDate
    
    -- Status FIFO karty
    status                  VARCHAR(1) NOT NULL CHECK (status IN ('A', 'W', 'X')),
    -- A = Active (aktívna - možno z nej vydávať)
    -- W = Waiting (čakajúca - čaká na aktiváciu)
    -- X = eXhausted (spotrebovaná - už vydané všetko)
    
    -- Príznak počiatočného stavu
    is_beginning_balance    BOOLEAN NOT NULL DEFAULT false, -- BegStat = 'B'
    
    -- Audit polia
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by              VARCHAR(50),
    updated_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by              VARCHAR(50),
    
    -- Foreign Keys
    CONSTRAINT fk_stock_card_fifos_stock
        FOREIGN KEY (stock_id) 
        REFERENCES stocks(stock_id)
        ON DELETE RESTRICT,
    
    CONSTRAINT fk_stock_card_fifos_product
        FOREIGN KEY (product_id) 
        REFERENCES products(product_id)
        ON DELETE RESTRICT,
    
    CONSTRAINT fk_stock_card_fifos_supplier
        FOREIGN KEY (supplier_id) 
        REFERENCES partners(partner_id)
        ON DELETE SET NULL,
    
    -- Composite FK na stock_cards
    CONSTRAINT fk_stock_card_fifos_stock_card
        FOREIGN KEY (stock_id, product_id) 
        REFERENCES stock_cards(stock_id, product_id)
        ON DELETE RESTRICT
);

-- Indexy pre výkon
CREATE INDEX idx_stock_card_fifos_stock ON stock_card_fifos(stock_id);
CREATE INDEX idx_stock_card_fifos_product ON stock_card_fifos(product_id);
CREATE INDEX idx_stock_card_fifos_stock_card ON stock_card_fifos(stock_id, product_id);
CREATE INDEX idx_stock_card_fifos_document ON stock_card_fifos(document_number, document_line_number);
CREATE INDEX idx_stock_card_fifos_status ON stock_card_fifos(status);
CREATE INDEX idx_stock_card_fifos_supplier ON stock_card_fifos(supplier_id);
CREATE INDEX idx_stock_card_fifos_doc_date ON stock_card_fifos(document_date);
CREATE INDEX idx_stock_card_fifos_expiration ON stock_card_fifos(expiration_date);
CREATE INDEX idx_stock_card_fifos_batch ON stock_card_fifos(batch_code);

-- Composite indexy pre FIFO logiku (najstaršie aktívne karty)
CREATE INDEX idx_stock_card_fifos_active ON stock_card_fifos(stock_id, product_id, status, document_date)
    WHERE status = 'A';

CREATE INDEX idx_stock_card_fifos_product_status_date ON stock_card_fifos(product_id, status, document_date)
    WHERE status IN ('A', 'W');

CREATE INDEX idx_stock_card_fifos_expiration_active ON stock_card_fifos(expiration_date, status)
    WHERE status = 'A' AND expiration_date IS NOT NULL;

CREATE INDEX idx_stock_card_fifos_batch_product ON stock_card_fifos(product_id, batch_code)
    WHERE batch_code IS NOT NULL;

-- Komentáre
COMMENT ON TABLE stock_card_fifos IS 'FIFO karty zásob - sledovanie príjmov a ich vyskladnenia podľa FIFO princípu';
COMMENT ON COLUMN stock_card_fifos.fifo_id IS 'ID FIFO karty (z Btrieve FifNum, unique naprieč skladmi)';
COMMENT ON COLUMN stock_card_fifos.stock_id IS 'ID skladu (pridané pre PostgreSQL multi-sklad)';
COMMENT ON COLUMN stock_card_fifos.product_id IS 'ID produktu';
COMMENT ON COLUMN stock_card_fifos.received_quantity IS 'Prijaté množstvo pri príjme';
COMMENT ON COLUMN stock_card_fifos.issued_quantity IS 'Celkovo vydané množstvo z tejto karty';
COMMENT ON COLUMN stock_card_fifos.remaining_quantity IS 'Zostatok k výdaju (received - issued)';
COMMENT ON COLUMN stock_card_fifos.status IS 'A=Active(aktívna), W=Waiting(čakajúca), X=eXhausted(spotrebovaná)';
COMMENT ON COLUMN stock_card_fifos.expiration_date IS 'Dátum ukončenia trvanlivosti tovaru';
COMMENT ON COLUMN stock_card_fifos.batch_code IS 'Kód výrobnej šarže';
COMMENT ON COLUMN stock_card_fifos.is_beginning_balance IS 'Príznak počiatočného stavu (začiatok roka)';

-- Trigger pre updated_at
CREATE TRIGGER update_stock_card_fifos_updated_at
    BEFORE UPDATE ON stock_card_fifos
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger pre automatický prepočet remaining_quantity
CREATE OR REPLACE FUNCTION calculate_fifo_remaining_quantity()
RETURNS TRIGGER AS $$
BEGIN
    NEW.remaining_quantity = NEW.received_quantity - NEW.issued_quantity;
    
    -- Automatická zmena statusu na X ak je zostatok 0
    IF NEW.remaining_quantity <= 0 THEN
        NEW.status = 'X';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_stock_card_fifos_remaining
    BEFORE INSERT OR UPDATE ON stock_card_fifos
    FOR EACH ROW
    EXECUTE FUNCTION calculate_fifo_remaining_quantity();

-- Check constraints
ALTER TABLE stock_card_fifos
ADD CONSTRAINT chk_stock_card_fifos_quantities_positive
CHECK (
    received_quantity > 0 AND
    issued_quantity >= 0 AND
    remaining_quantity >= 0
);

ALTER TABLE stock_card_fifos
ADD CONSTRAINT chk_stock_card_fifos_balance
CHECK (remaining_quantity = received_quantity - issued_quantity);

ALTER TABLE stock_card_fifos
ADD CONSTRAINT chk_stock_card_fifos_price_positive
CHECK (purchase_price >= 0);

ALTER TABLE stock_card_fifos
ADD CONSTRAINT chk_stock_card_fifos_status_logic
CHECK (
    (status = 'X' AND remaining_quantity = 0) OR
    (status IN ('A', 'W') AND remaining_quantity > 0)
);
```

---

## 3. MAPPING POLÍ

### Stock Card FIFOs

| Btrieve Pole | Typ Btrieve | PostgreSQL Pole | Typ PostgreSQL | Transformácia | Poznámka |
|--------------|-------------|-----------------|----------------|---------------|----------|
| **PRIDANÉ** | - | stock_id | INTEGER | - | Číslo skladu |
| FifNum | LONGINT | fifo_id | BIGSERIAL | Priamo | PK (unique naprieč skladmi) |
| DocNum | STRING[12] | document_number | VARCHAR(12) | Priamo | Číslo príjmového dokladu |
| ItmNum | LONGINT | document_line_number | INTEGER | Priamo | Riadok dokladu |
| GsCode | LONGINT | product_id | INTEGER | Priamo | FK na products |
| DocDate | DATE | document_date | DATE | Priamo | Dátum dokladu |
| DrbDate | DATE | expiration_date | DATE | Priamo | Trvanlivosť |
| InPrice | DOUBLE | purchase_price | DECIMAL(15,2) | Priamo | Nákupná cena bez DPH |
| InQnt | DOUBLE | received_quantity | DECIMAL(15,3) | Priamo | Prijaté množstvo |
| OutQnt | DOUBLE | issued_quantity | DECIMAL(15,3) | Priamo | Vydané množstvo |
| ActQnt | DOUBLE | remaining_quantity | DECIMAL(15,3) | Vypočítané | InQnt - OutQnt |
| Status | STRING[1] | status | VARCHAR(1) | Priamo | A/W/X |
| PaCode | LONGINT | supplier_id | INTEGER | Priamo | FK na partners |
| BegStat | STRING[1] | is_beginning_balance | BOOLEAN | 'B'→true | Počiatočný stav |
| RbaCode | STRING[30] | batch_code | VARCHAR(30) | Priamo | Výrobná šarža |
| RbaDate | DATE | batch_date | DATE | Priamo | Dátum výroby šarže |

### Polia ktoré SA NEPRENÁŠAJÚ

| Btrieve Pole | Dôvod neprenášania |
|--------------|-------------------|
| Sended | Technický príznak (NEX Genesis replikácia) |
| PdnQnt | Množstvo s výrobnými číslami (stock_serial_numbers tabuľka) |
| AcqStat | Príznak obstarania R/K (nepotrebné v NEX Automat) |

**Vypočítané polia:**
- `remaining_quantity` = `received_quantity` - `issued_quantity` (trigger)
- Status automaticky 'X' ak `remaining_quantity` = 0

---

## 4. BIZNIS LOGIKA

### 1. FIFO Princíp (First In, First Out)

**Základné pravidlo:**
- Výdaj sa realizuje vždy z **najstaršej aktívnej** FIFO karty
- Poradie: `document_date` ASC (najstarší dátum príjmu)

```sql
-- Získať najstaršiu aktívnu FIFO kartu pre produkt
SELECT *
FROM stock_card_fifos
WHERE stock_id = 1
  AND product_id = 12345
  AND status = 'A'
ORDER BY document_date ASC, fifo_id ASC
LIMIT 1;
```

### 2. Stavy FIFO karty

**A (Active) - Aktívna:**
```sql
-- Karta z ktorej sa aktuálne vydáva
-- remaining_quantity > 0
-- Najstaršia aktívna karta je na rade
```

**W (Waiting) - Čakajúca:**
```sql
-- Karta čaká na svoj rad
-- remaining_quantity > 0
-- Staršie karty sú ešte aktívne
```

**X (eXhausted) - Spotrebovaná:**
```sql
-- Všetko už bolo vydané
-- remaining_quantity = 0
-- Automatická zmena cez trigger
```

### 3. Proces výdaja

**Scenár 1: Výdaj z jednej FIFO karty**
```sql
-- Dostupné: FIFO #1 = 100 ks
-- Výdaj: 50 ks
-- Výsledok:
UPDATE stock_card_fifos
SET issued_quantity = issued_quantity + 50,
    remaining_quantity = remaining_quantity - 50
WHERE fifo_id = 1;
-- Status ostáva 'A', remaining = 50
```

**Scenár 2: Výdaj spotrebuje celú FIFO kartu**
```sql
-- Dostupné: FIFO #1 = 100 ks
-- Výdaj: 100 ks
-- Výsledok:
UPDATE stock_card_fifos
SET issued_quantity = issued_quantity + 100,
    remaining_quantity = 0,
    status = 'X'  -- Automaticky cez trigger
WHERE fifo_id = 1;
```

**Scenár 3: Výdaj cez viacero FIFO kariet** ⭐
```sql
-- Dostupné: 
--   FIFO #1 (2025-01-01) = 50 ks
--   FIFO #2 (2025-01-15) = 100 ks
-- Výdaj: 120 ks

-- Krok 1: Výdaj z FIFO #1 (najstaršia)
UPDATE stock_card_fifos
SET issued_quantity = issued_quantity + 50,
    remaining_quantity = 0,
    status = 'X'
WHERE fifo_id = 1;
-- Vytvorí sa stock_card_movements záznam: -50 ks, fifo_id = 1

-- Krok 2: Výdaj z FIFO #2 (ďalšia v poradí)
UPDATE stock_card_fifos
SET issued_quantity = issued_quantity + 70,
    remaining_quantity = 30
WHERE fifo_id = 2;
-- Vytvorí sa stock_card_movements záznam: -70 ks, fifo_id = 2

-- Výsledok: 2 záznamy v stock_card_movements!
```

### 4. Výpočet aktuálnej FIFO ceny

**Aktuálna FIFO cena = cena najstaršej aktívnej karty**

```sql
-- Získať aktuálnu FIFO cenu produktu
SELECT purchase_price as current_fifo_price
FROM stock_card_fifos
WHERE stock_id = 1
  AND product_id = 12345
  AND status = 'A'
ORDER BY document_date ASC, fifo_id ASC
LIMIT 1;

-- Aktualizovať stock_cards.current_fifo_price
UPDATE stock_cards sc
SET current_fifo_price = (
    SELECT purchase_price
    FROM stock_card_fifos
    WHERE stock_id = sc.stock_id
      AND product_id = sc.product_id
      AND status = 'A'
    ORDER BY document_date ASC, fifo_id ASC
    LIMIT 1
)
WHERE stock_id = 1 AND product_id = 12345;
```

### 5. Sledovanie trvanlivosti (FEFO - First Expired, First Out)

**Možná úprava FIFO → FEFO:**
```sql
-- Pri výdaji uprednostniť produkty s blížiacou sa expiráciou
SELECT *
FROM stock_card_fifos
WHERE stock_id = 1
  AND product_id = 12345
  AND status = 'A'
ORDER BY 
    CASE WHEN expiration_date IS NULL THEN 1 ELSE 0 END,  -- Bez expirácie na koniec
    expiration_date ASC,  -- Najskôr expirujúce
    document_date ASC     -- Potom podľa FIFO
LIMIT 1;
```

### 6. Šarže (Batches)

```sql
-- Vyhľadanie FIFO kariet podľa šarže
SELECT 
    fifo_id,
    batch_code,
    batch_date,
    received_quantity,
    remaining_quantity,
    status
FROM stock_card_fifos
WHERE product_id = 12345
  AND batch_code = 'BATCH2025001'
ORDER BY document_date;

-- Aktuálny stav šarže
SELECT 
    batch_code,
    SUM(remaining_quantity) as batch_remaining_quantity,
    SUM(issued_quantity) as batch_issued_quantity
FROM stock_card_fifos
WHERE product_id = 12345
  AND batch_code = 'BATCH2025001'
GROUP BY batch_code;
```

---

## 5. VZŤAHY S INÝMI TABUĽKAMI

```sql
-- Stock Card FIFOs → Stocks (N:1)
ALTER TABLE stock_card_fifos
ADD CONSTRAINT fk_stock_card_fifos_stock
FOREIGN KEY (stock_id) 
REFERENCES stocks(stock_id)
ON DELETE RESTRICT;

-- Stock Card FIFOs → Products (N:1)
ALTER TABLE stock_card_fifos
ADD CONSTRAINT fk_stock_card_fifos_product
FOREIGN KEY (product_id) 
REFERENCES products(product_id)
ON DELETE RESTRICT;

-- Stock Card FIFOs → Partners (N:1, optional)
-- Dodávateľ
ALTER TABLE stock_card_fifos
ADD CONSTRAINT fk_stock_card_fifos_supplier
FOREIGN KEY (supplier_id) 
REFERENCES partners(partner_id)
ON DELETE SET NULL;

-- Stock Card FIFOs → Stock Cards (N:1)
-- Composite FK
ALTER TABLE stock_card_fifos
ADD CONSTRAINT fk_stock_card_fifos_stock_card
FOREIGN KEY (stock_id, product_id) 
REFERENCES stock_cards(stock_id, product_id)
ON DELETE RESTRICT;

-- Stock Card FIFOs ← Stock Card Movements (1:N)
-- Každý výdaj z FIFO karty je zaznamenaný v movements
-- Poznámka: Bude definované v stock_card_movements tabuľke
```

### Diagram vzťahov

```
stocks (1) ----< (N) stock_card_fifos (N) >---- (1) products
                         |
                         +---- (N) >---- (1) partners (supplier)
                         |
                         +---- (N) >---- (1) stock_cards (composite FK)
                         |
                         +----< (1:N) stock_card_movements
```

---

## 6. VALIDAČNÉ PRAVIDLÁ

```sql
-- 1. Množstvá musia byť logické
ALTER TABLE stock_card_fifos
ADD CONSTRAINT chk_stock_card_fifos_quantities_positive
CHECK (
    received_quantity > 0 AND
    issued_quantity >= 0 AND
    remaining_quantity >= 0
);

-- 2. Bilancia musí sedieť
ALTER TABLE stock_card_fifos
ADD CONSTRAINT chk_stock_card_fifos_balance
CHECK (remaining_quantity = received_quantity - issued_quantity);

-- 3. Cena musí byť nezáporná
ALTER TABLE stock_card_fifos
ADD CONSTRAINT chk_stock_card_fifos_price_positive
CHECK (purchase_price >= 0);

-- 4. Status logika
ALTER TABLE stock_card_fifos
ADD CONSTRAINT chk_stock_card_fifos_status_logic
CHECK (
    (status = 'X' AND remaining_quantity = 0) OR
    (status IN ('A', 'W') AND remaining_quantity > 0)
);

-- 5. Jedinečnosť dokladu
CREATE UNIQUE INDEX idx_stock_card_fifos_unique_document
ON stock_card_fifos(stock_id, document_number, document_line_number);

-- 6. Trigger pre kontrolu expirácie
CREATE OR REPLACE FUNCTION check_fifo_expiration()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.expiration_date IS NOT NULL AND NEW.expiration_date < CURRENT_DATE THEN
        RAISE WARNING 'FIFO karta % má expirovaný produkt (%)!', 
            NEW.fifo_id, NEW.expiration_date;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_stock_card_fifos_expiration
    AFTER INSERT OR UPDATE ON stock_card_fifos
    FOR EACH ROW
    EXECUTE FUNCTION check_fifo_expiration();
```

---

## 7. QUERY PATTERNS

### Základné queries

```sql
-- 1. Najstaršia aktívna FIFO karta (na výdaj)
SELECT *
FROM stock_card_fifos
WHERE stock_id = 1
  AND product_id = 12345
  AND status = 'A'
ORDER BY document_date ASC, fifo_id ASC
LIMIT 1;

-- 2. Všetky aktívne FIFO karty produktu
SELECT 
    fifo_id,
    document_number,
    document_date,
    remaining_quantity,
    purchase_price
FROM stock_card_fifos
WHERE stock_id = 1
  AND product_id = 12345
  AND status = 'A'
ORDER BY document_date ASC;

-- 3. História FIFO kariet (spotrebované)
SELECT 
    fifo_id,
    document_date,
    received_quantity,
    issued_quantity,
    purchase_price,
    status
FROM stock_card_fifos
WHERE stock_id = 1
  AND product_id = 12345
  AND status = 'X'
ORDER BY document_date DESC;

-- 4. FIFO karty blízko expirácie
SELECT 
    f.fifo_id,
    f.stock_id,
    f.product_id,
    p.product_name,
    f.remaining_quantity,
    f.expiration_date,
    CURRENT_DATE - f.expiration_date as days_to_expiration
FROM stock_card_fifos f
JOIN products p ON f.product_id = p.product_id
WHERE f.status = 'A'
  AND f.expiration_date IS NOT NULL
  AND f.expiration_date <= CURRENT_DATE + INTERVAL '30 days'
ORDER BY f.expiration_date ASC;

-- 5. Agregácia FIFO kariet podľa produktu
SELECT 
    stock_id,
    product_id,
    COUNT(*) as fifo_count,
    SUM(remaining_quantity) as total_remaining,
    AVG(purchase_price) as avg_price
FROM stock_card_fifos
WHERE status IN ('A', 'W')
GROUP BY stock_id, product_id
ORDER BY total_remaining DESC;
```

### Pokročilé queries

```sql
-- 6. Výpočet vážnej priemernej FIFO ceny
SELECT 
    stock_id,
    product_id,
    SUM(remaining_quantity * purchase_price) / SUM(remaining_quantity) as weighted_avg_fifo_price
FROM stock_card_fifos
WHERE status = 'A'
GROUP BY stock_id, product_id;

-- 7. Produkty s viacerými aktívnymi FIFO kartami
SELECT 
    stock_id,
    product_id,
    COUNT(*) as active_fifos,
    MIN(document_date) as oldest_receipt,
    MAX(document_date) as newest_receipt,
    SUM(remaining_quantity) as total_quantity
FROM stock_card_fifos
WHERE status = 'A'
GROUP BY stock_id, product_id
HAVING COUNT(*) > 1
ORDER BY COUNT(*) DESC;

-- 8. FIFO karty podľa dodávateľa
SELECT 
    s.partner_name as supplier_name,
    COUNT(f.fifo_id) as fifo_count,
    SUM(f.remaining_quantity) as total_quantity,
    SUM(f.remaining_quantity * f.purchase_price) as total_value
FROM stock_card_fifos f
JOIN partners s ON f.supplier_id = s.partner_id
WHERE f.status = 'A'
GROUP BY s.partner_id, s.partner_name
ORDER BY total_value DESC;

-- 9. Stav šarží
SELECT 
    batch_code,
    batch_date,
    COUNT(*) as fifo_count,
    SUM(received_quantity) as total_received,
    SUM(issued_quantity) as total_issued,
    SUM(remaining_quantity) as total_remaining
FROM stock_card_fifos
WHERE batch_code IS NOT NULL
GROUP BY batch_code, batch_date
ORDER BY batch_date DESC;

-- 10. FIFO analýza - staré zásoby
SELECT 
    f.stock_id,
    f.product_id,
    p.product_name,
    f.document_date,
    f.remaining_quantity,
    CURRENT_DATE - f.document_date as age_days
FROM stock_card_fifos f
JOIN products p ON f.product_id = p.product_id
WHERE f.status = 'A'
  AND CURRENT_DATE - f.document_date > 180  -- Staršie ako 6 mesiacov
ORDER BY age_days DESC;
```

---

## 8. PRÍKLAD DÁT

```sql
-- Príklad 1: Aktívna FIFO karta
INSERT INTO stock_card_fifos (
    fifo_id, stock_id, product_id,
    document_number, document_line_number, document_date,
    supplier_id,
    received_quantity, issued_quantity, remaining_quantity,
    purchase_price,
    expiration_date,
    batch_code, batch_date,
    status,
    created_by, updated_by
) VALUES (
    100001, 1, 12345,                                -- FIFO #100001, Sklad 1, Produkt 12345
    'PRI2025/0001', 1, '2025-01-15',                -- Doklad príjmu
    5001,                                            -- Dodávateľ
    100.000, 30.000, 70.000,                        -- Prijaté: 100, Vydané: 30, Zostatok: 70
    50.00,                                           -- Nákupná cena
    '2025-12-31',                                    -- Expirácia
    'BATCH2025001', '2025-01-10',                   -- Šarža
    'A',                                             -- Aktívna
    'system', 'system'
);

-- Príklad 2: Spotrebovaná FIFO karta
INSERT INTO stock_card_fifos (
    fifo_id, stock_id, product_id,
    document_number, document_line_number, document_date,
    supplier_id,
    received_quantity, issued_quantity, remaining_quantity,
    purchase_price,
    status,
    created_by, updated_by
) VALUES (
    99999, 1, 12345,                                 -- FIFO #99999, Sklad 1, Produkt 12345
    'PRI2025/0001', 1, '2025-01-01',                -- Starší doklad
    5001,                                            -- Ten istý dodávateľ
    50.000, 50.000, 0.000,                          -- Všetko vydané
    48.00,                                           -- Nižšia cena (starší príjem)
    'X',                                             -- Spotrebovaná
    'system', 'system'
);

-- Príklad 3: Čakajúca FIFO karta
INSERT INTO stock_card_fifos (
    fifo_id, stock_id, product_id,
    document_number, document_line_number, document_date,
    supplier_id,
    received_quantity, issued_quantity, remaining_quantity,
    purchase_price,
    status,
    created_by, updated_by
) VALUES (
    100002, 1, 12345,                                -- FIFO #100002, Sklad 1, Produkt 12345
    'PRI2025/0002', 1, '2025-02-01',                -- Novší doklad
    5002,                                            -- Iný dodávateľ
    200.000, 0.000, 200.000,                        -- Zatiaľ nič nevydané
    52.00,                                           -- Vyššia cena (nový príjem)
    'W',                                             -- Čaká na rad (staršia FIFO #100001 je aktívna)
    'system', 'system'
);

-- Príklad 4: Počiatočný stav (začiatok roka)
INSERT INTO stock_card_fifos (
    fifo_id, stock_id, product_id,
    document_number, document_line_number, document_date,
    received_quantity, issued_quantity, remaining_quantity,
    purchase_price,
    is_beginning_balance,
    status,
    created_by, updated_by
) VALUES (
    90000, 1, 67890,                                 -- FIFO #90000, Sklad 1, Produkt 67890
    'BEGIN2025', 1, '2025-01-01',                   -- Počiatočný doklad
    150.000, 0.000, 150.000,                        -- Počiatočný stav
    45.00,                                           -- Odhadovaná priemerná cena
    true,                                            -- ⭐ Počiatočný stav
    'A',                                             -- Aktívna
    'system', 'system'
);
```

---

## 9. POZNÁMKY PRE MIGRÁCIU

### Python príklad načítania z viacerých Btrieve súborov

```python
from btrieve import Btrieve
import psycopg2
import glob

def migrate_stock_card_fifos():
    conn = psycopg2.connect(
        host="localhost",
        database="nex_automat",
        user="postgres",
        password="password"
    )
    cur = conn.cursor()
    
    # Nájsť všetky FIF súbory (FIF00001.BTR, FIF00002.BTR, ...)
    fif_files = glob.glob('FIF?????.BTR')
    
    print(f"Našiel som {len(fif_files)} FIFO súborov")
    
    for fif_file in sorted(fif_files):
        # Extrahovať číslo skladu z názvu súboru
        # FIF00001.BTR → stock_id = 1
        stock_id = int(fif_file[3:8])
        
        print(f"Migrujem {fif_file} (stock_id={stock_id})...")
        
        # Otvoriť Btrieve súbor
        btr = Btrieve()
        btr.open(fif_file, 'r')
        
        # Prechádzať záznamy
        for record in btr:
            # INSERT do PostgreSQL
            cur.execute("""
                INSERT INTO stock_card_fifos (
                    fifo_id, stock_id, product_id,
                    document_number, document_line_number, document_date,
                    supplier_id,
                    received_quantity, issued_quantity, remaining_quantity,
                    purchase_price,
                    expiration_date,
                    batch_code, batch_date,
                    status,
                    is_beginning_balance
                ) VALUES (
                    %s, %s, %s,
                    %s, %s, %s,
                    %s,
                    %s, %s, %s,
                    %s,
                    %s,
                    %s, %s,
                    %s,
                    %s
                )
                ON CONFLICT (fifo_id) DO UPDATE SET
                    issued_quantity = EXCLUDED.issued_quantity,
                    remaining_quantity = EXCLUDED.remaining_quantity,
                    status = EXCLUDED.status
            """, (
                record['FifNum'], stock_id, record['GsCode'],
                record['DocNum'], record['ItmNum'], record['DocDate'],
                record.get('PaCode') if record.get('PaCode') else None,
                record['InQnt'], record['OutQnt'], record['ActQnt'],
                record['InPrice'],
                record.get('DrbDate'),
                record.get('RbaCode'), record.get('RbaDate'),
                record['Status'],
                record.get('BegStat') == 'B'
            ))
        
        btr.close()
        print(f"  → Hotovo: {fif_file}")
    
    conn.commit()
    cur.close()
    conn.close()
    
    print("Migrácia stock_card_fifos dokončená!")

if __name__ == '__main__':
    migrate_stock_card_fifos()
```

### Dôležité upozornenia

1. **Multi-sklad architektúra:**
   - Btrieve: Viacero súborov (FIF00001.BTR, FIF00002.BTR, ...)
   - PostgreSQL: Jedna tabuľka + stock_id
   - PK: fifo_id (musí byť unique naprieč skladmi!)

2. **Neprenášané polia:**
   - `Sended` - technický príznak replikácie
   - `PdnQnt` - výrobné čísla (stock_serial_numbers tabuľka)
   - `AcqStat` - príznak obstarania (nepotrebné)

3. **Vypočítané polia:**
   - `remaining_quantity` = `received_quantity` - `issued_quantity` (trigger)
   - Status automaticky 'X' ak zostatok = 0

4. **Validácie:**
   - Bilancia: received - issued = remaining
   - Status logika: 'X' ↔ remaining = 0
   - Ceny ≥ 0
   - Množstvá ≥ 0

5. **FIFO logika:**
   - Výdaj vždy z najstaršej aktívnej karty (ORDER BY document_date ASC)
   - Ak výdaj > zostatok → rozdeliť na viacero movements záznamov

6. **Trvanlivosť:**
   - `expiration_date` → možnosť FEFO (First Expired, First Out)
   - Trigger upozornenie na expirované produkty

7. **Šarže:**
   - `batch_code`, `batch_date` → sledovanie výrobných šarží
   - Možnosť agregácie stavu šarží

8. **Počiatočný stav:**
   - `is_beginning_balance = true` → začiatok roka
   - Špeciálny doklad napr. "BEGIN2025"

---

## 10. VERZIA A ZMENY

| Verzia | Dátum | Autor | Zmeny |
|--------|-------|-------|-------|
| 1.0 | 2025-12-11 | Zoltán + Claude | Prvá verzia dokumentácie stock_card_fifos |

**Status:** ✅ Kompletný  
**Session:** 5  
**Súbor:** `docs/architecture/database/stock/cards/tables/FIF-stock_card_fifos.md`