# PLSnnnnn.BTR → price_list_items

**Kategória:** Catalogs - Predajné cenníky  
**NEX Genesis:** PLSnnnnn.BTR (kde nnnnn = číslo cenníka)  
**NEX Automat:** `price_list_items`  
**Vytvorené:** 2025-12-10  
**Status:** ✅ Pripravené na review

---

## PREHĽAD

### Historický vývoj cenníkov

**NEX Genesis (Btrieve obmedzenia):**
- Každý cenník = samostatná tabuľka PLSnnnnn.BTR
- Príklady: PLS00001.BTR, PLS00002.BTR, PLS00003.BTR
- Obsahuje duplikované údaje z GSCAT (kvôli chýbajúcemu JOIN)

**NEX Automat (PostgreSQL):**
- JEDNA tabuľka `price_list_items` pre všetky cenníky
- Rozlíšenie cez `price_list_id`
- Bez duplikácie údajov (použijeme JOIN)

**Príklad použitia:**
- PLS00001.BTR = "Cenník pre koncových zákazníkov"
- PLS00002.BTR = "Cenník pre veľkoodberateľov"
- PLS00003.BTR = "Akciový cenník"

---

## KOMPLETNÁ SQL SCHÉMA

### price_list_items

**Tabuľka:** `price_list_items`  
**Popis:** Predajné ceny produktov v jednotlivých cenníkoch

```sql
CREATE TABLE price_list_items (
    id SERIAL PRIMARY KEY,
    price_list_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    stock_list_id INTEGER,
    
    -- Cenové údaje
    purchase_price DECIMAL(12,2),
    profit_margin DECIMAL(5,2),
    price_excl_vat DECIMAL(12,2),
    price_incl_vat DECIMAL(12,2) NOT NULL,
    
    -- Predajné podmienky
    min_quantity DECIMAL(12,4) DEFAULT 1.0,
    allow_price_override BOOLEAN DEFAULT FALSE,
    
    -- Príznaky
    is_promotional BOOLEAN DEFAULT FALSE,
    requires_label_print BOOLEAN DEFAULT FALSE,
    is_disabled BOOLEAN DEFAULT FALSE,
    
    -- Audit záznamu
    created_by VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(30),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (product_id) REFERENCES product_catalog(product_id) ON DELETE RESTRICT,
    FOREIGN KEY (stock_list_id) REFERENCES stock_lists(stock_list_id) ON DELETE RESTRICT,
    UNIQUE(price_list_id, product_id, stock_list_id)
);

CREATE INDEX idx_price_list_items_list ON price_list_items(price_list_id);
CREATE INDEX idx_price_list_items_product ON price_list_items(product_id);
CREATE INDEX idx_price_list_items_stock ON price_list_items(stock_list_id);
CREATE INDEX idx_price_list_items_promotional ON price_list_items(is_promotional) WHERE is_promotional = TRUE;
CREATE INDEX idx_price_list_items_disabled ON price_list_items(is_disabled);
CREATE INDEX idx_price_list_items_label ON price_list_items(requires_label_print) WHERE requires_label_print = TRUE;

-- Trigger pre automatickú aktualizáciu updated_at
CREATE TRIGGER update_price_list_items_updated_at
    BEFORE UPDATE ON price_list_items
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

## MAPPING POLÍ

### Polia ktoré SA PRENÁŠAJÚ

| NEX Genesis | Typ | NEX Automat | Typ | Popis |
|-------------|-----|-------------|-----|-------|
| nnnnn (názov súboru) | - | price_list_id | INTEGER | Číslo cenníka z PLSnnnnn.BTR |
| GsCode | longint | product_id | INTEGER | Tovarové číslo (PLU) |
| StkNum | word | stock_list_id | INTEGER | Číslo skladu |
| Profit | double | profit_margin | DECIMAL(5,2) | Percentuálna sadzba zisku |
| - | - | purchase_price | DECIMAL(12,2) | **NOVÉ!** Nákupná cena základňa |
| APrice | double | price_excl_vat | DECIMAL(12,2) | Predajná cena bez DPH |
| BPrice | double | price_incl_vat | DECIMAL(12,2) | Predajná cena s DPH |
| MinQnt | double | min_quantity | DECIMAL(12,4) | Minimálne predajné množstvo |
| OpenGs | byte | allow_price_override | BOOLEAN | Otvorené PLU (1=možno meniť cenu) |
| Action | Str1 | is_promotional | BOOLEAN | Príznak akcie (A=akciový tovar) |
| ChgItm | Str1 | requires_label_print | BOOLEAN | Príznak zmeny (P=tlačiť etiketu) |
| DisFlag | byte | is_disabled | BOOLEAN | Vyradený (1=vyradený) |
| ModUser | Str8 | created_by, updated_by | VARCHAR(30) | Audit údaje |
| ModDate | DateType | created_at, updated_at | TIMESTAMP | Audit údaje |
| ModTime | TimeType | created_at, updated_at | TIMESTAMP | Audit údaje |

### Polia ktoré SA NEPRENÁŠAJÚ - Duplikácia z GSCAT

| NEX Genesis | Typ | Dôvod neprenášania |
|-------------|-----|--------------------|
| GsName | Str30 | Z product_catalog cez JOIN |
| _GsName | Str20 | Vyhľadávacie pole - nepotrebné |
| MgCode | longint | Z product_catalog_categories |
| FgCode | longint | Z product_catalog_categories |
| BarCode | Str15 | Z product_catalog_identifiers |
| StkCode | Str15 | Z product_catalog_identifiers |
| MsName | Str10 | Z product_catalog.unit_name |
| PackGs | longint | Z product_catalog.package_product_id |
| VatPrc | byte | Použije sa vat_group_id z product_catalog |
| GsType | Str1 | Z product_catalog.product_type |
| DrbMust | byte | Z product_catalog_extensions |
| PdnMust | byte | Z product_catalog_extensions |
| GrcMth | word | Z product_catalog.warranty_months |
| GaName | Str60 | Z product_catalog_texts |
| _GaName | Str60 | Vyhľadávacie pole - nepotrebné |
| OsdCode | Str30 | Z product_catalog_identifiers |

### Polia ktoré SA NEPRENÁŠAJÚ - Zastarané/Nepoužité

| NEX Genesis | Typ | Dôvod neprenášania |
|-------------|-----|--------------------|
| UPrice | double | História cien - riešime cez price_history tabuľku |
| OvsUser | Str8 | História cien - riešime cez price_history tabuľku |
| OvsDate | DateType | História cien - riešime cez price_history tabuľku |
| DscPrc1-3 | double | Alternatívne ceny D1-D3 - nepoužívame |
| PrfPrc1-3 | double | Alternatívne zisky D1-D3 - nepoužívame |
| APrice1-3 | double | Alternatívne ceny D1-D3 - nepoužívame |
| BPrice1-3 | double | Alternatívne ceny D1-D3 - nepoužívame |
| OrdPrn | byte | Číslo oddelenia reštaurácie - špecifické |
| CpcSrc | Str1 | Zdroj nákupnej ceny - nepotrebujeme |
| Sended | byte | Sync flag - zastarané |
| ModNum | word | Verzia záznamu - PostgreSQL trigger |

---

## MIGRAČNÝ SCRIPT

### INSERT do price_list_items

```sql
-- Migrácia z PLSnnnnn.BTR
-- Tento script sa spustí pre každú tabuľku PLSnnnnn.BTR

INSERT INTO price_list_items (
    price_list_id,
    product_id,
    stock_list_id,
    profit_margin,
    purchase_price,
    price_excl_vat,
    price_incl_vat,
    min_quantity,
    allow_price_override,
    is_promotional,
    requires_label_print,
    is_disabled,
    created_by,
    created_at,
    updated_by,
    updated_at
)
SELECT 
    :price_list_id AS price_list_id,  -- číslo z názvu súboru PLSnnnnn
    GsCode AS product_id,
    NULLIF(StkNum, 0) AS stock_list_id,  -- 0 → NULL
    Profit AS profit_margin,
    NULL AS purchase_price,  -- NOVÉ POLE - zatiaľ NULL, dopočítame
    APrice AS price_excl_vat,
    BPrice AS price_incl_vat,
    COALESCE(NULLIF(MinQnt, 0), 1.0) AS min_quantity,  -- 0 → 1.0
    CASE WHEN OpenGs = 1 THEN TRUE ELSE FALSE END AS allow_price_override,
    CASE WHEN Action = 'A' THEN TRUE ELSE FALSE END AS is_promotional,
    CASE WHEN ChgItm = 'P' THEN TRUE ELSE FALSE END AS requires_label_print,
    CASE WHEN DisFlag = 1 THEN TRUE ELSE FALSE END AS is_disabled,
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
FROM PLSnnnnn  -- názov tabuľky sa mení podľa čísla cenníka
WHERE GsCode IN (SELECT product_id FROM product_catalog WHERE is_disabled = FALSE);

-- Dopočítanie purchase_price zo zisku
UPDATE price_list_items
SET purchase_price = CASE 
    WHEN profit_margin > 0 THEN price_excl_vat / (1 + profit_margin / 100)
    ELSE NULL
END
WHERE price_list_id = :price_list_id
  AND purchase_price IS NULL
  AND price_excl_vat > 0;
```

**Poznámka:** 
- `:price_list_id` sa extrahuje z názvu súboru (napr. PLS00001.BTR → 1)
- `purchase_price` sa vypočíta spätne zo zisku: `purchase_price = price_excl_vat / (1 + profit_margin / 100)`

---

## BIZNIS LOGIKA

### 1. Číslo cenníka (price_list_id)

**Extrakcia z názvu súboru:**
```python
# Príklad: PLS00001.BTR → 1
filename = "PLS00001.BTR"
price_list_id = int(filename[3:8])  # "00001" → 1
```

**Použitie:**
- price_list_id = 1 → "Cenník pre koncových zákazníkov"
- price_list_id = 2 → "Cenník pre veľkoodberateľov"
- price_list_id = 3 → "Akciový cenník"

**Názvy cenníkov:** Samostatný číselník `price_lists` (vytvoríme neskôr)

---

### 2. Výpočet cien

**Vzorce:**
```sql
-- Nákupná cena → Predajná cena bez DPH
price_excl_vat = purchase_price * (1 + profit_margin / 100)

-- Predajná cena bez DPH → Predajná cena s DPH
price_incl_vat = price_excl_vat * (1 + vat_rate / 100)

-- Spätný výpočet nákupnej ceny
purchase_price = price_excl_vat / (1 + profit_margin / 100)
```

**Príklad:**
- purchase_price = 10.00 €
- profit_margin = 25%
- vat_rate = 20%

```
price_excl_vat = 10.00 * 1.25 = 12.50 €
price_incl_vat = 12.50 * 1.20 = 15.00 €
```

---

### 3. Minimálne predajné množstvo (min_quantity)

**Použitie:**
- `min_quantity = 1.0` → Produkt sa predáva po kusoch
- `min_quantity = 6.0` → Minimálny nákup 6 kusov (napr. pivo po sixpackoch)
- `min_quantity = 0.5` → Možno kúpiť aj polovicu (napr. meter látky)

**Validácia pri predaji:**
```sql
-- Kontrola minimálneho množstva
IF (sold_quantity < min_quantity) THEN
    RAISE EXCEPTION 'Minimálne predajné množstvo je %', min_quantity;
END IF;
```

---

### 4. Otvorené PLU (allow_price_override)

**Použitie:**
- `allow_price_override = TRUE` → Pokladníčka môže zmeniť cenu na pokladni
- `allow_price_override = FALSE` → Cena je fixná

**Príklady:**
- Zelenina/ovocie na váhu → TRUE
- Balené potraviny → FALSE
- Služby → TRUE

---

### 5. Akciový tovar (is_promotional)

**Použitie:**
- Označenie akčných cien
- Filter pre akciový letáK
- Špeciálne zobrazenie v e-shope

**Query:**
```sql
-- Akciový tovar
SELECT p.product_name, pli.price_incl_vat, pli.previous_price_incl_vat
FROM price_list_items pli
INNER JOIN product_catalog p ON pli.product_id = p.product_id
WHERE pli.price_list_id = 1
  AND pli.is_promotional = TRUE
  AND pli.is_disabled = FALSE
ORDER BY p.product_name;
```

---

### 6. Tlač etikiet (requires_label_print)

**Použitie:**
- Po zmene ceny sa nastaví `requires_label_print = TRUE`
- Systém vytlačí nové cenovky
- Po vytlačení sa nastaví späť na FALSE

**Workflow:**
```sql
-- 1. Zmena ceny
UPDATE price_list_items 
SET price_incl_vat = 15.99,
    requires_label_print = TRUE,
    last_price_change_by = 'admin',
    last_price_change_at = CURRENT_TIMESTAMP,
    updated_by = 'admin',
    updated_at = CURRENT_TIMESTAMP
WHERE id = 123;

-- 2. Výber položiek na tlač
SELECT * FROM price_list_items 
WHERE requires_label_print = TRUE;

-- 3. Po vytlačení
UPDATE price_list_items 
SET requires_label_print = FALSE,
    updated_by = 'PRINT_SERVICE',
    updated_at = CURRENT_TIMESTAMP
WHERE id = 123;
```

---

### 7. Sklad (stock_list_id)

**Použitie:**
- Produkt môže mať rôzne ceny na rôznych skladoch
- `stock_list_id = NULL` → Univerzálna cena pre všetky sklady
- `stock_list_id = 1` → Cena špecifická pre sklad 1

**Príklad:**
```sql
-- Produkt má univerzálnu cenu
INSERT INTO price_list_items (price_list_id, product_id, stock_list_id, price_incl_vat) 
VALUES (1, 1001, NULL, 15.00);

-- Produkt má špeciálnu cenu na sklade 2
INSERT INTO price_list_items (price_list_id, product_id, stock_list_id, price_incl_vat) 
VALUES (1, 1001, 2, 14.00);
```

**Poznámka:** Detailná dokumentácia skladového hospodárstva (stock_lists, stock_card_items, stock_card_fifo, stock_card_movements) bude vytvorená neskôr.

---

## VZŤAHY S INÝMI TABUĽKAMI

### price_list_items → product_catalog

```sql
-- Získať cenu produktu
SELECT 
    p.product_name,
    pli.price_excl_vat,
    pli.price_incl_vat,
    pli.profit_margin,
    pli.min_quantity
FROM price_list_items pli
INNER JOIN product_catalog p ON pli.product_id = p.product_id
WHERE pli.price_list_id = 1
  AND p.product_id = 1001;
```

### price_list_items → stock_lists

```sql
-- Ceny produktu na rôznych skladoch
SELECT 
    sl.stock_name,
    pli.price_incl_vat,
    pli.min_quantity
FROM price_list_items pli
LEFT JOIN stock_lists sl ON pli.stock_list_id = sl.stock_list_id
WHERE pli.price_list_id = 1
  AND pli.product_id = 1001
ORDER BY sl.stock_name NULLS FIRST;
```

### price_list_items → vat_groups (cez product_catalog)

```sql
-- Produkt s DPH sadzbou
SELECT 
    p.product_name,
    vg.vat_rate,
    pli.price_excl_vat,
    pli.price_incl_vat
FROM price_list_items pli
INNER JOIN product_catalog p ON pli.product_id = p.product_id
LEFT JOIN vat_groups vg ON p.vat_group_id = vg.vat_group_id
WHERE pli.price_list_id = 1;
```

---

## VALIDAČNÉ PRAVIDLÁ

### 1. Ceny musia byť konzistentné

```sql
-- Trigger pre validáciu cien
CREATE OR REPLACE FUNCTION validate_price_list_item_prices()
RETURNS TRIGGER AS $$
BEGIN
    -- Cena s DPH musí byť vyššia alebo rovná cene bez DPH
    IF NEW.price_incl_vat < NEW.price_excl_vat THEN
        RAISE EXCEPTION 'Cena s DPH (%) nemôže byť nižšia ako cena bez DPH (%)', 
            NEW.price_incl_vat, NEW.price_excl_vat;
    END IF;
    
    -- Marža musí byť rozumná (0-1000%)
    IF NEW.profit_margin IS NOT NULL AND (NEW.profit_margin < 0 OR NEW.profit_margin > 1000) THEN
        RAISE EXCEPTION 'Marža (%) musí byť medzi 0 a 1000', NEW.profit_margin;
    END IF;
    
    -- Minimálne množstvo musí byť kladné
    IF NEW.min_quantity <= 0 THEN
        RAISE EXCEPTION 'Minimálne množstvo musí byť väčšie ako 0';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_price_list_item_prices
    BEFORE INSERT OR UPDATE ON price_list_items
    FOR EACH ROW
    EXECUTE FUNCTION validate_price_list_item_prices();
```

### 2. Produkt musí existovať

```sql
FOREIGN KEY (product_id) REFERENCES product_catalog(product_id) ON DELETE RESTRICT
```

### 3. Sklad musí existovať (ak je zadaný)

```sql
FOREIGN KEY (stock_list_id) REFERENCES stock_lists(stock_list_id) ON DELETE RESTRICT
```

### 4. Unikátnosť

```sql
UNIQUE(price_list_id, product_id, stock_list_id)
```

**Znamená:**
- V jednom cenníku môže byť produkt len raz pre daný sklad
- Ale môže byť viac krát pre rôzne sklady

---

## QUERY PATTERNS

### Získať aktuálnu cenu produktu

```sql
-- Cena produktu v cenníku 1
SELECT 
    p.product_name,
    pli.price_incl_vat,
    pli.min_quantity,
    pli.is_promotional
FROM price_list_items pli
INNER JOIN product_catalog p ON pli.product_id = p.product_id
WHERE pli.price_list_id = 1
  AND pli.product_id = 1001
  AND pli.is_disabled = FALSE
  AND (pli.stock_list_id IS NULL OR pli.stock_list_id = :current_stock_list_id)
ORDER BY pli.stock_list_id NULLS LAST
LIMIT 1;
```

### Porovnať ceny v rôznych cenníkoch

```sql
-- Porovnanie cien
SELECT 
    p.product_name,
    pli1.price_incl_vat AS price_retail,
    pli2.price_incl_vat AS price_wholesale,
    pli1.price_incl_vat - pli2.price_incl_vat AS difference
FROM product_catalog p
LEFT JOIN price_list_items pli1 ON p.product_id = pli1.product_id AND pli1.price_list_id = 1
LEFT JOIN price_list_items pli2 ON p.product_id = pli2.product_id AND pli2.price_list_id = 2
WHERE p.is_disabled = FALSE
ORDER BY difference DESC;
```

### Akciový letáK

```sql
-- Akciové produkty (len označené ako is_promotional)
SELECT 
    p.product_name,
    pli.price_incl_vat,
    pli.profit_margin
FROM price_list_items pli
INNER JOIN product_catalog p ON pli.product_id = p.product_id
WHERE pli.price_list_id = 1
  AND pli.is_promotional = TRUE
  AND pli.is_disabled = FALSE
ORDER BY p.product_name;

-- Poznámka: Predchádzajúce ceny a % zľavu získame z price_history tabuľky (JOIN)
```

### Produkty ktoré treba preceniť

```sql
-- Produkty s nízkou maržou
SELECT 
    p.product_name,
    pli.profit_margin,
    pli.price_excl_vat,
    pli.price_incl_vat
FROM price_list_items pli
INNER JOIN product_catalog p ON pli.product_id = p.product_id
WHERE pli.price_list_id = 1
  AND pli.profit_margin < 15.0
  AND pli.is_disabled = FALSE
ORDER BY pli.profit_margin ASC;
```

---

## PRÍKLAD DÁT

```sql
-- Cenník 1: Maloobchod
INSERT INTO price_list_items (price_list_id, product_id, stock_list_id, purchase_price, profit_margin, price_excl_vat, price_incl_vat, min_quantity, created_by, created_at, updated_by, updated_at) VALUES
(1, 1001, NULL, 10.00, 25.00, 12.50, 15.00, 1.0, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00'),
(1, 1002, NULL, 5.00, 30.00, 6.50, 7.80, 1.0, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00'),
(1, 1003, NULL, 8.00, 40.00, 11.20, 13.44, 6.0, 'admin', '2025-01-01 10:00:00', 'manager', '2025-02-15 14:30:00');

-- Cenník 2: Veľkoobchod
INSERT INTO price_list_items (price_list_id, product_id, stock_list_id, purchase_price, profit_margin, price_excl_vat, price_incl_vat, min_quantity, created_by, created_at, updated_by, updated_at) VALUES
(2, 1001, NULL, 10.00, 15.00, 11.50, 13.80, 10.0, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00'),
(2, 1002, NULL, 5.00, 20.00, 6.00, 7.20, 20.0, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00');

-- Akciový tovar
INSERT INTO price_list_items (price_list_id, product_id, stock_list_id, purchase_price, profit_margin, price_excl_vat, price_incl_vat, is_promotional, min_quantity, created_by, created_at, updated_by, updated_at) VALUES
(1, 1004, NULL, 12.00, 10.00, 13.20, 15.84, TRUE, 1.0, 'admin', '2025-01-01 10:00:00', 'admin', '2025-03-01 08:00:00');

-- Produkt s rôznou cenou na rôznych skladoch
INSERT INTO price_list_items (price_list_id, product_id, stock_list_id, purchase_price, profit_margin, price_excl_vat, price_incl_vat, min_quantity, created_by, created_at, updated_by, updated_at) VALUES
(1, 1005, NULL, 20.00, 25.00, 25.00, 30.00, 1.0, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00'),
(1, 1005, 2, 20.00, 20.00, 24.00, 28.80, 1.0, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00');
```

---

## MIGRAČNÉ POZNÁMKY

### 1. Číslo cenníka z názvu súboru

```python
import os
import re

# Získať všetky PLS súbory
pls_files = [f for f in os.listdir() if re.match(r'PLS\d{5}\.BTR', f)]

# Pre každý súbor
for filename in pls_files:
    price_list_id = int(filename[3:8])  # "PLS00001.BTR" → 1
    print(f"Migrácia cenníka {price_list_id} z {filename}")
```

### 2. VatPrc vs vat_group_id

**Pri migrácii:**
- VatPrc z PLSnnnnn.BTR slúži len na validáciu
- Skutočný vat_group_id sa berie z product_catalog
- Ak sa líši → warning, ale použije sa z product_catalog

```sql
-- Validácia po migrácii
SELECT 
    pls.GsCode,
    pls.VatPrc AS pls_vat,
    vg.vat_rate AS catalog_vat
FROM PLSnnnnn pls
INNER JOIN product_catalog p ON pls.GsCode = p.product_id
INNER JOIN vat_groups vg ON p.vat_group_id = vg.vat_group_id
WHERE pls.VatPrc != vg.vat_rate;
```

### 3. Dopočítanie purchase_price

**Spätný výpočet:**
```sql
UPDATE price_list_items
SET purchase_price = price_excl_vat / (1 + profit_margin / 100)
WHERE purchase_price IS NULL
  AND profit_margin > 0
  AND price_excl_vat > 0;
```

---

## SÚVISIACE DOKUMENTY

- **product_catalog** → `GSCAT-product_catalog.md`
- **product_catalog_identifiers** → `BARCODE-GSCAT-product_catalog_identifiers.md`
- **warehouses** → ⏳ Todo (tabuľka skladov)
- **price_lists** → ⏳ Todo (číselník cenníkov)

---

**Vytvoril:** Claude & Zoltán  
**Dátum:** 2025-12-10  
**Verzia:** 1.0  
**Status:** ✅ Pripravené na review