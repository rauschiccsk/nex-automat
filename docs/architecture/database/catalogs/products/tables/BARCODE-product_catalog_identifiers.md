# BARCODE.BTR + GSCAT.BTR → product_catalog_identifiers

**Kategória:** Catalogs - Identifikačné kódy  
**NEX Genesis:** BARCODE.BTR + GSCAT.BTR (polia: BarCode, StkCode, SpcCode, OsdCode)  
**NEX Automat:** `product_catalog_identifiers`  
**Vytvorené:** 2025-12-10  
**Status:** ✅ Pripravené na review

---

## PREHĽAD

### Historický vývoj identifikačných kódov

**Fáza 1 - Začiatok:**
- Jeden čiarový kód priamo v GSCAT.BTR (pole `BarCode`)

**Fáza 2 - Viacnásobné čiarové kódy:**
- Nová tabuľka BARCODE.BTR pre ďalšie čiarové kódy
- Prvý zostal v GSCAT.BTR
- Dôvod: Ten istý tovar môže mať rôzne EAN kódy podľa výrobcu/krajiny

**Fáza 3 - "Zneužitie" BARCODE.BTR:**
- Zákazníci začali do BARCODE.BTR dávať aj iné druhy kódov (nie len čiarové)
- Chceli ich vidieť v samostatných stĺpcoch v gride
- Dôvod: Umožnilo to rýchle vyhľadávanie produktu

**Fáza 4 - Riešenie bez JOIN (Btrieve obmedzenia):**
- Do GSCAT.BTR pridané špecializované polia:
  - `StkCode` - skladový kód (interný)
  - `SpcCode` - špecifikačný kód
  - `OsdCode` - kód dodávateľa
- Dôvod: Btrieve nemal JOIN operáciu

**Fáza 5 - Migrácia do NEX Automat (PostgreSQL):**
- ✅ Všetko zlúčiť do `product_catalog_identifiers`
- ✅ Použiť `identifier_type` pre rozlíšenie
- ✅ Podpora neobmedzeného počtu identifikátorov
- ✅ Využiť PostgreSQL indexy pre rýchle vyhľadávanie

**Štandardné audit polia:**
- ✅ `created_by`, `created_at` - kto a kedy vytvoril záznam
- ✅ `updated_by`, `updated_at` - kto a kedy naposledy modifikoval záznam
- ⚠️ Toto sa používa vo **všetkých** tabuľkách NEX Automat

---

## 1. KOMPLETNÁ SQL SCHÉMA

### product_catalog_identifiers

**Tabuľka:** `product_catalog_identifiers`  
**Popis:** Všetky identifikačné kódy produktu (EAN, skladový, špecifikačný, dodávateľský)

```sql
CREATE TABLE product_catalog_identifiers (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    identifier_type VARCHAR(20) NOT NULL CHECK (identifier_type IN ('barcode', 'stock', 'spec', 'supplier')),
    identifier_code VARCHAR(50) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    created_by VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(30),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (product_id) REFERENCES product_catalog(product_id) ON DELETE CASCADE,
    UNIQUE(product_id, identifier_type, identifier_code)
);

CREATE INDEX idx_identifiers_product ON product_catalog_identifiers(product_id);
CREATE INDEX idx_identifiers_type ON product_catalog_identifiers(identifier_type);
CREATE INDEX idx_identifiers_code ON product_catalog_identifiers(identifier_code);
CREATE INDEX idx_identifiers_type_code ON product_catalog_identifiers(identifier_type, identifier_code);
CREATE INDEX idx_identifiers_primary ON product_catalog_identifiers(product_id, identifier_type) WHERE is_primary = TRUE;
```

**Hodnoty identifier_type:**
- `'barcode'` - čiarový kód (EAN-13, EAN-8, UPC-A, Code128...)
- `'stock'` - skladový kód (interný identifikátor pre sklady)
- `'spec'` - špecifikačný kód (technický/katalógový kód)
- `'supplier'` - kód dodávateľa (objednávací kód u dodávateľa)

**Pole is_primary:**
- Označuje primárny identifikátor daného typu
- Pre `'barcode'`: primárny = z GSCAT.BTR, ostatné = z BARCODE.BTR
- Pre `'stock'`, `'spec'`, `'supplier'`: primárny = vždy z GSCAT.BTR
- Používa sa pre zobrazenie v gridoch, preferovaný kód

---

## 2. MAPPING GSCAT.BTR → product_catalog_identifiers

### Zdroj: GSCAT.BTR - Primárne identifikátory

| NEX Genesis | Typ | NEX Automat | Typ | Identifier Type | is_primary |
|-------------|-----|-------------|-----|-----------------|------------|
| GsCode | longint | product_id | INTEGER | - | - |
| BarCode | Str15 | identifier_code | VARCHAR(50) | 'barcode' | TRUE |
| StkCode | Str15 | identifier_code | VARCHAR(50) | 'stock' | TRUE |
| SpcCode | Str30 | identifier_code | VARCHAR(50) | 'spec' | TRUE |
| OsdCode | Str15 | identifier_code | VARCHAR(50) | 'supplier' | TRUE |
| CrtUser | Str8 | created_by | VARCHAR(20) | - | - |
| CrtDate | DateType | created_at | TIMESTAMP | - | - |
| CrtTime | TimeType | created_at | TIMESTAMP | - | - |
| ModUser | Str8 | updated_by | VARCHAR(20) | - | - |
| ModDate | DateType | updated_at | TIMESTAMP | - | - |
| ModTime | TimeType | updated_at | TIMESTAMP | - | - |

**Poznámka:** 
- Všetky identifikátory z GSCAT.BTR majú `is_primary = TRUE`
- Ak pole je prázdne (NULL), záznam sa nevkladá
- `CrtUser/CrtDate/CrtTime` = kedy bol produkt vytvorený
- `ModUser/ModDate/ModTime` = kedy bol produkt naposledy modifikovaný (ak neexistuje, použije sa CrtUser)

**Migračný script pre GSCAT.BTR:**
```sql
-- 1. BarCode (čiarový kód)
INSERT INTO product_catalog_identifiers (product_id, identifier_type, identifier_code, is_primary, created_by, created_at, updated_by, updated_at)
SELECT 
    GsCode AS product_id,
    'barcode' AS identifier_type,
    TRIM(BarCode) AS identifier_code,
    TRUE AS is_primary,
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
FROM GSCAT
WHERE BarCode IS NOT NULL 
  AND TRIM(BarCode) != ''
  AND DisFlag = 0;  -- Len aktívne produkty

-- 2. StkCode (skladový kód)
INSERT INTO product_catalog_identifiers (product_id, identifier_type, identifier_code, is_primary, created_by, created_at, updated_by, updated_at)
SELECT 
    GsCode AS product_id,
    'stock' AS identifier_type,
    TRIM(StkCode) AS identifier_code,
    TRUE AS is_primary,
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
FROM GSCAT
WHERE StkCode IS NOT NULL 
  AND TRIM(StkCode) != ''
  AND DisFlag = 0;

-- 3. SpcCode (špecifikačný kód)
INSERT INTO product_catalog_identifiers (product_id, identifier_type, identifier_code, is_primary, created_by, created_at, updated_by, updated_at)
SELECT 
    GsCode AS product_id,
    'spec' AS identifier_type,
    TRIM(SpcCode) AS identifier_code,
    TRUE AS is_primary,
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
FROM GSCAT
WHERE SpcCode IS NOT NULL 
  AND TRIM(SpcCode) != ''
  AND DisFlag = 0;

-- 4. OsdCode (kód dodávateľa)
INSERT INTO product_catalog_identifiers (product_id, identifier_type, identifier_code, is_primary, created_by, created_at, updated_by, updated_at)
SELECT 
    GsCode AS product_id,
    'supplier' AS identifier_type,
    TRIM(OsdCode) AS identifier_code,
    TRUE AS is_primary,
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
FROM GSCAT
WHERE OsdCode IS NOT NULL 
  AND TRIM(OsdCode) != ''
  AND DisFlag = 0;
```

---

## 3. MAPPING BARCODE.BTR → product_catalog_identifiers

### Zdroj: BARCODE.BTR - Sekundárne čiarové kódy

| NEX Genesis | Typ | NEX Automat | Typ | Identifier Type | is_primary |
|-------------|-----|-------------|-----|-----------------|------------|
| GsCode | longint | product_id | INTEGER | - | - |
| BarCode | Str15 | identifier_code | VARCHAR(50) | 'barcode' | FALSE |
| ModUser | Str8 | created_by, updated_by | VARCHAR(30) | - | - |
| ModDate | DateType | created_at, updated_at | TIMESTAMP | - | - |
| ModTime | TimeType | created_at, updated_at | TIMESTAMP | - | - |

**Poznámka:**
- Všetky záznamy z BARCODE.BTR majú `identifier_type = 'barcode'` a `is_primary = FALSE`
- ModDate + ModTime sa kombinujú do jedného TIMESTAMP

**Migračný script pre BARCODE.BTR:**
```sql
INSERT INTO product_catalog_identifiers (product_id, identifier_type, identifier_code, is_primary, created_by, created_at, updated_by, updated_at)
SELECT 
    b.GsCode AS product_id,
    'barcode' AS identifier_type,
    TRIM(b.BarCode) AS identifier_code,
    FALSE AS is_primary,
    COALESCE(b.ModUser, 'MIGRATION') AS created_by,
    COALESCE(
        CAST(b.ModDate AS TIMESTAMP) + CAST(b.ModTime AS INTERVAL),
        CURRENT_TIMESTAMP
    ) AS created_at,
    COALESCE(b.ModUser, 'MIGRATION') AS updated_by,
    COALESCE(
        CAST(b.ModDate AS TIMESTAMP) + CAST(b.ModTime AS INTERVAL),
        CURRENT_TIMESTAMP
    ) AS updated_at
FROM BARCODE b
INNER JOIN GSCAT g ON b.GsCode = g.GsCode
WHERE b.BarCode IS NOT NULL 
  AND TRIM(b.BarCode) != ''
  AND g.DisFlag = 0  -- Len aktívne produkty
ON CONFLICT (product_id, identifier_type, identifier_code) DO NOTHING;  -- Ignorovať duplicity
```

**Vysvetlenie ON CONFLICT:**
- Môže sa stať že ten istý BarCode je v GSCAT aj BARCODE
- UNIQUE constraint (product_id, identifier_type, identifier_code) zabráni duplicite
- DO NOTHING = ak už existuje, preskočíme

---

## 4. POLIA KTORÉ SA NEPRENÁŠAJÚ

### Z BARCODE.BTR

| NEX Genesis | Typ | Dôvod neprenášania |
|-------------|-----|--------------------|
| - | - | Všetky polia sa prenášajú |

**Poznámka:** BARCODE.BTR má len 5 polí a všetky sú potrebné.

---

## 5. BIZNIS LOGIKA

### 5.1 Typy identifikátorov - Použitie

**barcode (čiarový kód):**
- EAN-13, EAN-8, UPC-A, Code128, QR kód
- Použitie: pokladnice, čítačky čiarových kódov, e-shopy
- Primárny: z GSCAT.BTR (najčastejšie používaný)
- Sekundárne: z BARCODE.BTR (alternatívne kódy)

**stock (skladový kód):**
- Interný identifikátor pre sklady
- Použitie: skladové operácie, inventúra, etikety
- Často kratší než EAN (napr. "SK-12345")

**spec (špecifikačný kód):**
- Technický/katalógový kód
- Použitie: technická dokumentácia, katalógy
- Môže obsahovať verziu/variant (napr. "MT-100-V2")

**supplier (kód dodávateľa):**
- Kód produktu u dodávateľa
- Použitie: objednávky, príjemky
- Každý dodávateľ môže mať vlastný kód pre ten istý produkt

### 5.2 Primárny vs sekundárny identifikátor

**is_primary = TRUE:**
- Preferovaný identifikátor daného typu
- Zobrazuje sa v gridoch ako hlavný
- Z GSCAT.BTR

**is_primary = FALSE:**
- Alternatívne identifikátory
- Používajú sa pri vyhľadávaní
- Z BARCODE.BTR

**Pravidlo:** Produkt môže mať **max. 1 primárny** identifikátor každého typu, ale **neobmedzený počet sekundárnych**.

### 5.3 Viacnásobnosť

| Typ | Primárny (GSCAT) | Sekundárne (BARCODE) | Celkom |
|-----|------------------|----------------------|--------|
| barcode | 0-1 | 0-N | 0-N |
| stock | 0-1 | 0 | 0-1 |
| spec | 0-1 | 0 | 0-1 |
| supplier | 0-1 | 0 | 0-1 |

**Vysvetlenie:**
- Len `barcode` môže mať viacero hodnôt (BARCODE.BTR)
- `stock`, `spec`, `supplier` majú max. 1 hodnotu (len z GSCAT.BTR)

---

## 6. VALIDAČNÉ PRAVIDLÁ

### 6.1 UNIQUE Constraint

```sql
UNIQUE(product_id, identifier_type, identifier_code)
```

**Pravidlo:** Ten istý kód nemôže byť priradený k tomu istému produktu a typu viackrát.

**Príklad chyby:**
```sql
-- CHYBA - duplicita
INSERT INTO product_catalog_identifiers VALUES (100, 'barcode', '8588006123456', TRUE);
INSERT INTO product_catalog_identifiers VALUES (100, 'barcode', '8588006123456', FALSE);  -- ❌ DUPLICATE
```

### 6.2 CHECK Constraint

```sql
CHECK (identifier_type IN ('barcode', 'stock', 'spec', 'supplier'))
```

**Pravidlo:** Len povolené typy identifikátorov.

### 6.3 Foreign Key Constraint

```sql
FOREIGN KEY (product_id) REFERENCES product_catalog(product_id) ON DELETE CASCADE
```

**Pravidlo:** Ak zmažem produkt → zmažú sa všetky jeho identifikátory.

### 6.4 Aplikačné pravidlá

**Audit polia (štandard pre všetky tabuľky):**
- `created_by`, `created_at` - kto a kedy vytvoril záznam (nemenné)
- `updated_by`, `updated_at` - kto a kedy naposledy modifikoval (aktualizuje sa pri každej zmene)

**Pri migrácii z NEX Genesis:**
- `CrtUser/CrtDate/CrtTime` → `created_by/created_at`
- `ModUser/ModDate/ModTime` → `updated_by/updated_at`
- Ak ModUser neexistuje → použiť CrtUser

**Max. 1 primárny identifikátor daného typu:**
```sql
-- Trigger alebo aplikačná logika
SELECT COUNT(*) 
FROM product_catalog_identifiers 
WHERE product_id = ? 
  AND identifier_type = ? 
  AND is_primary = TRUE;
-- Musí byť 0 alebo 1
```

**Prázdne kódy:**
```sql
-- Nepovoliť prázdne stringy
CHECK (TRIM(identifier_code) != '')
```

---

## 7. QUERY PATTERNS

### 7.1 Vyhľadať produkt podľa ľubovoľného identifikátora

```sql
-- Universal search
SELECT DISTINCT p.*
FROM product_catalog p
INNER JOIN product_catalog_identifiers pi ON p.product_id = pi.product_id
WHERE pi.identifier_code = ?;
```

### 7.2 Vyhľadať produkt podľa konkrétneho typu

```sql
-- Hľadať len podľa EAN
SELECT p.*
FROM product_catalog p
INNER JOIN product_catalog_identifiers pi ON p.product_id = pi.product_id
WHERE pi.identifier_type = 'barcode'
  AND pi.identifier_code = '8588006123456';
```

### 7.3 Získať primárny identifikátor

```sql
-- Primárny čiarový kód
SELECT identifier_code
FROM product_catalog_identifiers
WHERE product_id = ?
  AND identifier_type = 'barcode'
  AND is_primary = TRUE;
```

### 7.4 Získať všetky identifikátory produktu

```sql
-- Všetky identifikátory produktu
SELECT 
    identifier_type,
    identifier_code,
    is_primary,
    created_by,
    created_at,
    updated_by,
    updated_at
FROM product_catalog_identifiers
WHERE product_id = ?
ORDER BY 
    identifier_type,
    is_primary DESC,  -- Primárne prvé
    identifier_code;
```

### 7.5 Zoznam produktov s viacerými čiarovými kódmi

```sql
-- Produkty s viac ako 1 čiarovým kódom
SELECT 
    p.product_id,
    p.product_name,
    COUNT(*) AS barcode_count
FROM product_catalog p
INNER JOIN product_catalog_identifiers pi ON p.product_id = pi.product_id
WHERE pi.identifier_type = 'barcode'
GROUP BY p.product_id, p.product_name
HAVING COUNT(*) > 1
ORDER BY barcode_count DESC;
```

### 7.6 Nájsť produkty podľa čiastočného kódu (LIKE)

```sql
-- Fuzzy search
SELECT DISTINCT p.*
FROM product_catalog p
INNER JOIN product_catalog_identifiers pi ON p.product_id = pi.product_id
WHERE pi.identifier_code ILIKE '%' || ? || '%';
```

### 7.7 Full-text search na identifikátoroch

```sql
-- Vytvoriť GIN index pre rýchle vyhľadávanie
CREATE INDEX idx_identifiers_code_gin ON product_catalog_identifiers 
USING gin(identifier_code gin_trgm_ops);

-- Vyhľadať podobné kódy
SELECT 
    p.product_name,
    pi.identifier_type,
    pi.identifier_code,
    similarity(pi.identifier_code, ?) AS sim
FROM product_catalog p
INNER JOIN product_catalog_identifiers pi ON p.product_id = pi.product_id
WHERE pi.identifier_code % ?  -- Similarity operator
ORDER BY sim DESC
LIMIT 10;
```

---

## 8. PRÍKLADY DÁT

### Príklad 1 - Produkt s jedným čiarovým kódom

```sql
-- GSCAT.BTR
GsCode: 1001
BarCode: '8588006123456'
StkCode: 'SK-1001'
SpcCode: 'MT-100-V1'
OsdCode: 'SUP-A123'

-- Výsledok v product_catalog_identifiers
INSERT INTO product_catalog_identifiers VALUES
(1, 1001, 'barcode', '8588006123456', TRUE, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00'),
(2, 1001, 'stock', 'SK-1001', TRUE, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00'),
(3, 1001, 'spec', 'MT-100-V1', TRUE, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00'),
(4, 1001, 'supplier', 'SUP-A123', TRUE, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00');
```

### Príklad 2 - Produkt s viacerými čiarovými kódmi

```sql
-- GSCAT.BTR
GsCode: 2002
BarCode: '8588006789012'  -- Primárny
StkCode: 'SK-2002'

-- BARCODE.BTR (sekundárne EAN kódy)
GsCode: 2002, BarCode: '4006381333627'  -- Nemecký EAN
GsCode: 2002, BarCode: '5901234123457'  -- Poľský EAN

-- Výsledok v product_catalog_identifiers
INSERT INTO product_catalog_identifiers VALUES
(5, 2002, 'barcode', '8588006789012', TRUE, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00'),    -- Primárny
(6, 2002, 'barcode', '4006381333627', FALSE, 'operator', '2025-01-15 14:30:00', 'operator', '2025-01-15 14:30:00'), -- Sekundárny
(7, 2002, 'barcode', '5901234123457', FALSE, 'operator', '2025-01-20 09:15:00', 'operator', '2025-01-20 09:15:00'), -- Sekundárny
(8, 2002, 'stock', 'SK-2002', TRUE, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00');
```

### Príklad 3 - Produkt bez čiarového kódu

```sql
-- GSCAT.BTR
GsCode: 3003
BarCode: NULL  -- Žiadny čiarový kód
StkCode: 'SK-3003'

-- Výsledok v product_catalog_identifiers
INSERT INTO product_catalog_identifiers VALUES
(9, 3003, 'stock', 'SK-3003', TRUE, 'admin', '2025-01-01 10:00:00', 'admin', '2025-01-01 10:00:00');
-- Žiadny barcode záznam!
```

---

## 9. MIGRAČNÉ POZNÁMKY

### 9.1 Duplicitné identifikátory

**Problém:** V GSCAT alebo BARCODE môže byť ten istý kód pre rôzne produkty.

**Detekcia duplicít:**
```sql
-- Nájsť duplicitné čiarové kódy v GSCAT
SELECT BarCode, COUNT(*) AS cnt
FROM GSCAT
WHERE BarCode IS NOT NULL 
  AND TRIM(BarCode) != ''
GROUP BY BarCode
HAVING COUNT(*) > 1;

-- Nájsť duplicitné čiarové kódy v BARCODE
SELECT BarCode, COUNT(DISTINCT GsCode) AS product_cnt
FROM BARCODE
WHERE BarCode IS NOT NULL 
  AND TRIM(BarCode) != ''
GROUP BY BarCode
HAVING COUNT(DISTINCT GsCode) > 1;
```

**Riešenie:**
1. Manuálna kontrola a oprava pred migráciou
2. Alebo: Povoliť duplicity (odstrániť UNIQUE na identifier_code)
3. Alebo: Pridať product_id do vyhľadávania (vrátiť všetky matches)

### 9.2 Whitespace a veľké/malé písmená

**Problém:** Kódy môžu obsahovať medzery alebo mať rôznu veľkosť písmen.

**Riešenie:**
```sql
-- Normalizácia pri migrácii
UPPER(TRIM(BarCode))  -- Všetko veľké, bez medzier
```

### 9.3 Poradie migrácie

**Správne poradie:**
1. Najprv GSCAT.BTR (primárne identifikátory)
2. Potom BARCODE.BTR (sekundárne čiarové kódy)
3. Dôvod: ON CONFLICT DO NOTHING zabezpečí že primárne ostanú is_primary=TRUE

---

## 10. VZŤAHY S INÝMI TABUĽKAMI

### 10.1 product_catalog → product_catalog_identifiers

**Vzťah:** 1:N (One-to-Many)
- Jeden produkt môže mať viacero identifikátorov
- Identifikátor patrí práve jednému produktu

**FK Constraint:**
```sql
FOREIGN KEY (product_id) REFERENCES product_catalog(product_id) ON DELETE CASCADE
```

**Cascading:**
- Ak zmažem produkt → automaticky sa zmažú všetky jeho identifikátory

---

## 11. PERFORMANCE OPTIMALIZÁCIA

### 11.1 Indexy

**Už vytvorené:**
```sql
CREATE INDEX idx_identifiers_product ON product_catalog_identifiers(product_id);
CREATE INDEX idx_identifiers_type ON product_catalog_identifiers(identifier_type);
CREATE INDEX idx_identifiers_code ON product_catalog_identifiers(identifier_code);
CREATE INDEX idx_identifiers_type_code ON product_catalog_identifiers(identifier_type, identifier_code);
CREATE INDEX idx_identifiers_primary ON product_catalog_identifiers(product_id, identifier_type) WHERE is_primary = TRUE;
```

**Dodatočné pre fuzzy search:**
```sql
-- Potrebné rozšírenie
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- GIN index pre LIKE queries
CREATE INDEX idx_identifiers_code_gin ON product_catalog_identifiers 
USING gin(identifier_code gin_trgm_ops);
```

### 11.2 Partition by identifier_type

**Pre veľké databázy (>1M produktov):**
```sql
-- Rozdeliť tabuľku podľa typu
CREATE TABLE product_catalog_identifiers (
    ...
) PARTITION BY LIST (identifier_type);

CREATE TABLE identifiers_barcode PARTITION OF product_catalog_identifiers
    FOR VALUES IN ('barcode');
    
CREATE TABLE identifiers_stock PARTITION OF product_catalog_identifiers
    FOR VALUES IN ('stock');
    
CREATE TABLE identifiers_spec PARTITION OF product_catalog_identifiers
    FOR VALUES IN ('spec');
    
CREATE TABLE identifiers_supplier PARTITION OF product_catalog_identifiers
    FOR VALUES IN ('supplier');
```

---

## 12. AUTOMATICKÁ AKTUALIZÁCIA updated_at

### Trigger pre automatickú aktualizáciu

**Funkcia:**
```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$ LANGUAGE plpgsql;
```

**Trigger:**
```sql
CREATE TRIGGER update_product_catalog_identifiers_updated_at
    BEFORE UPDATE ON product_catalog_identifiers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

**Vysvetlenie:**
- Pri každom UPDATE sa automaticky nastaví `updated_at = CURRENT_TIMESTAMP`
- `updated_by` sa musí nastaviť manuálne v aplikácii (user context)
- Toto je štandardný pattern pre všetky tabuľky NEX Automat

---

## 13. TESTOVANIE PO MIGRÁCII

### 12.1 Kontrola počtu záznamov

```sql
-- Počet identifikátorov z GSCAT
SELECT 
    'barcode' AS type, COUNT(*) AS cnt FROM GSCAT WHERE BarCode IS NOT NULL AND TRIM(BarCode) != ''
UNION ALL
SELECT 'stock', COUNT(*) FROM GSCAT WHERE StkCode IS NOT NULL AND TRIM(StkCode) != ''
UNION ALL
SELECT 'spec', COUNT(*) FROM GSCAT WHERE SpcCode IS NOT NULL AND TRIM(SpcCode) != ''
UNION ALL
SELECT 'supplier', COUNT(*) FROM GSCAT WHERE OsdCode IS NOT NULL AND TRIM(OsdCode) != '';

-- Počet identifikátorov v NEX Automat
SELECT identifier_type, COUNT(*) AS cnt
FROM product_catalog_identifiers
WHERE is_primary = TRUE
GROUP BY identifier_type;

-- Počet sekundárnych čiarových kódov
SELECT COUNT(*) FROM BARCODE WHERE BarCode IS NOT NULL AND TRIM(BarCode) != '';

SELECT COUNT(*) FROM product_catalog_identifiers 
WHERE identifier_type = 'barcode' AND is_primary = FALSE;
```

### 13.2 Kontrola primárnych identifikátorov

```sql
-- Produkty s viacerými primárnymi identifikátormi (chyba!)
SELECT product_id, identifier_type, COUNT(*) AS cnt
FROM product_catalog_identifiers
WHERE is_primary = TRUE
GROUP BY product_id, identifier_type
HAVING COUNT(*) > 1;
-- Malo by vrátiť 0 riadkov
```

### 13.3 Test vyhľadávania

```sql
-- Vybrať náhodný produkt z GSCAT
SELECT GsCode, BarCode, StkCode FROM GSCAT WHERE BarCode IS NOT NULL LIMIT 1;

-- Otestovať vyhľadávanie v NEX Automat
SELECT * FROM product_catalog_identifiers WHERE identifier_code = '<BarCode z testu>';
```

---

**Vytvoril:** Claude & Zoltán  
**Dátum:** 2025-12-10  
**Verzia:** 1.0  
**Status:** ✅ Pripravené na review