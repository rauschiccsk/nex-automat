# GSCAT.BTR → product_catalog

**Kategória:** Catalogs  
**NEX Genesis:** GSCAT.BTR (Goods Catalog)  
**NEX Automat:** `product_catalog`, `product_catalog_extensions`, `product_catalog_identifiers`, `product_catalog_categories`, `product_catalog_texts`, `vat_groups`  
**Vytvorené:** 2025-12-10  
**Status:** ✅ Finalizované

---

## 1. PRODUCT_CATALOG - Základný bázový katalóg

**Tabuľka:** `product_catalog`  
**Popis:** Základné údaje o produkte (tovar, materiál, služba)

| NEX Genesis | Typ | NEX Automat | Typ | Popis | Index |
|-------------|-----|-------------|-----|-------|-------|
| GsCode | longint | product_id | INTEGER | Numerický identifikátor produktu (PLU) | PK |
| GsName | Str30 | product_name | VARCHAR(100) | Názov produktu | ✓ |
| ProTyp | Str1 | business_type | VARCHAR(1) | M=materiál, T=tovar, S=služba | ✓ |
| GsType | Str1 | product_type | VARCHAR(1) | T=riadny, W=váhový, O=obal | ✓ |
| MsName | Str10 | unit_name | VARCHAR(20) | Názov mernej jednotky (ks, kg, l) | - |
| MsuName | Str5 | base_unit | VARCHAR(10) | Základná jednotka (kg, m, l, m2, m3) | - |
| MsuQnt | double | base_unit_quantity | DECIMAL(12,4) | Množstvo v základnej jednotke | - |
| PackGs | longint | package_product_id | INTEGER | Tovarové číslo pripojeného obalu | FK |
| GrcMth | word | warranty_months | SMALLINT | Záručná doba (počet mesiacov) | - |
| DivSet | byte | divisibility | SMALLINT | 0=deliteľný, 1=nedeliteľný, 2=1/2... | - |
| DisFlag | byte | is_disabled | BOOLEAN | Vyradený z evidencie (1=vyradený) | ✓ |
| CrtUser | Str8 | created_by | VARCHAR(30) | Užívateľ ktorý vytvoril záznam | - |
| CrtDate | DateType | created_at | TIMESTAMP | Dátum a čas vytvorenia | - |
| CrtTime | TimeType | created_at | TIMESTAMP | Zahrnuté v created_at | - |
| ModUser | Str8 | updated_by | VARCHAR(30) | Kto naposledy modifikoval | - |
| ModDate | DateType | updated_at | TIMESTAMP | Kedy naposledy modifikované | - |
| ModTime | TimeType | updated_at | TIMESTAMP | Zahrnuté v updated_at | - |

**SQL CREATE TABLE:**
```sql
CREATE TABLE product_catalog (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    business_type VARCHAR(1) NOT NULL CHECK (business_type IN ('M', 'T', 'S')),
    product_type VARCHAR(1) NOT NULL CHECK (product_type IN ('T', 'W', 'O')),
    unit_name VARCHAR(20),
    base_unit VARCHAR(10),
    base_unit_quantity DECIMAL(12,4),
    package_product_id INTEGER,
    warranty_months SMALLINT,
    divisibility SMALLINT DEFAULT 0,
    is_disabled BOOLEAN DEFAULT FALSE,
    vat_group_id INTEGER,
    created_by VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(30),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (package_product_id) REFERENCES product_catalog(product_id) ON DELETE SET NULL,
    FOREIGN KEY (vat_group_id) REFERENCES vat_groups(vat_group_id) ON DELETE RESTRICT
);

CREATE INDEX idx_product_catalog_name ON product_catalog(product_name);
CREATE INDEX idx_product_catalog_business_type ON product_catalog(business_type);
CREATE INDEX idx_product_catalog_product_type ON product_catalog(product_type);
CREATE INDEX idx_product_catalog_vat_group ON product_catalog(vat_group_id);
CREATE INDEX idx_product_catalog_disabled ON product_catalog(is_disabled);

-- Trigger pre automatickú aktualizáciu updated_at
CREATE TRIGGER update_product_catalog_updated_at
    BEFORE UPDATE ON product_catalog
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

**Poznámka:** MgCode (tovarová skupina) sa mapuje cez `product_catalog_categories`, nie priamo v product_catalog!

---

## 2. PRODUCT_CATALOG_EXTENSIONS - Rozšírenie katalógu

**Tabuľka:** `product_catalog_extensions`  
**Popis:** Dodatočné údaje, ktoré nie každý zákazník používa

| NEX Genesis | Typ | NEX Automat | Typ | Popis |
|-------------|-----|-------------|-----|-------|
| GsCode | longint | product_id | INTEGER | Väzba na products (PK, FK) |
| Volume | double | volume_m3 | DECIMAL(12,4) | Objem (množstvo MJ na 1 m3) |
| Weight | double | weight_kg | DECIMAL(12,4) | Váha jednej MJ |
| SpirGs | byte | is_alcoholic | BOOLEAN | Liehový výrobok (1=áno) |
| DrbMust | byte | track_expiry | BOOLEAN | Povinné zadávanie trvanlivosti |
| DrbDay | word | expiry_days | SMALLINT | Počet dní trvanlivosti |
| PdnMust | byte | track_serial | BOOLEAN | Sledovanie výrobných čísiel |
| RbaTrc | byte | track_batch | BOOLEAN | Sledovanie výrobnej šarže |
| SecNum | byte | scale_section | SMALLINT | Číslo váhovej sekcie |
| WgCode | word | scale_plu | SMALLINT | Váhové PLU číslo |
| ShpNum | byte | eshop_id | SMALLINT | Číslo e-shopu |
| SndShp | byte | synced_to_eshop | BOOLEAN | Uložené do e-shopu |
| LinPrice | double | last_purchase_price | DECIMAL(12,2) | Posledná nákupná cena |
| LinDate | DateType | last_receipt_date | DATE | Dátum posledného príjmu |
| LinStk | word | last_receipt_stock | SMALLINT | Číslo skladu príjmu |
| LinPac | longint | last_supplier_id | INTEGER | Kód posledného dodávateľa |
| GscKfc | word | carton_quantity | SMALLINT | Počet kusov v kartóne |
| GspKfc | word | pallet_cartons | SMALLINT | Počet kartónov v palete |
| QliKfc | double | carton_weight | DECIMAL(10,4) | Hmotnosť kartónu |

**SQL CREATE TABLE:**
```sql
CREATE TABLE product_catalog_extensions (
    product_id INTEGER PRIMARY KEY,
    volume_m3 DECIMAL(12,4),
    weight_kg DECIMAL(12,4),
    is_alcoholic BOOLEAN DEFAULT FALSE,
    track_expiry BOOLEAN DEFAULT FALSE,
    expiry_days SMALLINT,
    track_serial BOOLEAN DEFAULT FALSE,
    track_batch BOOLEAN DEFAULT FALSE,
    scale_section SMALLINT,
    scale_plu SMALLINT,
    eshop_id SMALLINT,
    synced_to_eshop BOOLEAN DEFAULT FALSE,
    last_purchase_price DECIMAL(12,2),
    last_receipt_date DATE,
    last_receipt_stock SMALLINT,
    last_supplier_id INTEGER,
    carton_quantity SMALLINT,
    pallet_cartons SMALLINT,
    carton_weight DECIMAL(10,4),
    
    FOREIGN KEY (product_id) REFERENCES product_catalog(product_id) ON DELETE CASCADE
);
```

**Poznámka:** Extensions tabuľka nemá audit polia (created_by, updated_by), pretože je to 1:1 väzba s product_catalog a audit je na hlavnej tabuľke.

---

## 3. PRODUCT_CATALOG_IDENTIFIERS - Identifikačné kódy

**Tabuľka:** `product_catalog_identifiers`  
**Popis:** Všetky identifikačné kódy produktu (EAN, skladový, špecifikačný, dodávateľský) + obsah BARCODE.BTR

| NEX Genesis | Typ | NEX Automat | Typ | Identifier Type |
|-------------|-----|-------------|-----|-----------------|
| BarCode | Str15 | identifier_code | VARCHAR(50) | 'barcode' |
| StkCode | Str15 | identifier_code | VARCHAR(50) | 'stock' |
| SpcCode | Str30 | identifier_code | VARCHAR(50) | 'spec' |
| OsdCode | Str15 | identifier_code | VARCHAR(50) | 'supplier' |

**Štruktúra:**
- `product_id` - numerický identifikátor produktu
- `identifier_type` - typ kódu ('barcode', 'stock', 'spec', 'supplier')
- `identifier_code` - samotný identifikačný kód
- `is_primary` - primárny identifikátor daného typu
- `created_by`, `created_at` - audit polia
- `updated_by`, `updated_at` - audit polia

**SQL CREATE TABLE:**
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

-- Trigger pre automatickú aktualizáciu updated_at
CREATE TRIGGER update_product_catalog_identifiers_updated_at
    BEFORE UPDATE ON product_catalog_identifiers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

**Hodnoty identifier_type:**
- `barcode` = čiarový kód (EAN-13, EAN-8, UPC-A, Code128...)
- `stock` = skladový kód (interný identifikátor)
- `spec` = špecifikačný kód (technický/katalógový kód)
- `supplier` = kód dodávateľa (objednávací kód u dodávateľa)

**Poznámka:** Do tejto tabuľky bude presunutý aj obsah `BARCODE.BTR` - sekundárne čiarové kódy produktu. Viac info v `BARCODE-GSCAT-product_catalog_identifiers.md`.

---

## 4. PRODUCT_CATALOG_CATEGORIES - Kategorizácia

**Tabuľka:** Mapovacia tabuľka medzi produktmi a kategóriami

| NEX Genesis | NEX Automat | Category Type | Číselník |
|-------------|-------------|---------------|----------|
| MgCode | category_id | 'product' | product_categories |
| FgCode | category_id | 'financial' | product_categories |
| SgCode | category_id | 'specific' | product_categories |

**Štruktúra:**
- `product_id` - numerický identifikátor produktu
- `category_type` - typ kategórie ('product', 'financial', 'specific')
- `category_id` - numerický identifikátor skupiny (kategórie)

**SQL CREATE TABLE:**
```sql
-- Číselník kategórií (obsahuje MGLST, FGLST, SGLST)
CREATE TABLE product_categories (
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
    profit_margin DECIMAL(5,2),
    
    -- Polia pre finančné skupiny (FGLST)
    category_description TEXT,
    max_discount DECIMAL(5,2),
    min_profit_margin DECIMAL(5,2),
    account_number VARCHAR(10),
    
    FOREIGN KEY (parent_category_id) REFERENCES product_categories(category_id) ON DELETE RESTRICT
);

-- Trigger pre automatickú aktualizáciu updated_at
CREATE TRIGGER update_product_categories_updated_at
    BEFORE UPDATE ON product_categories
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Mapovacia tabuľka
CREATE TABLE product_catalog_categories (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    category_type VARCHAR(20) NOT NULL,
    category_id INTEGER NOT NULL,
    
    FOREIGN KEY (product_id) REFERENCES product_catalog(product_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES product_categories(category_id) ON DELETE RESTRICT,
    UNIQUE(product_id, category_type)
);

CREATE INDEX idx_product_catalog_categories_product ON product_catalog_categories(product_id);
CREATE INDEX idx_product_catalog_categories_type ON product_catalog_categories(category_type);
CREATE INDEX idx_product_catalog_categories_category ON product_catalog_categories(category_id);
```

**Hodnoty category_type:**
- `product` = tovarová skupina (MgCode) → MGLST.BTR
- `financial` = finančná skupina (FgCode) → FGLST.BTR
- `specific` = špecifická skupina (SgCode) → SGLST.BTR

**Potrebné číselníky:**
- `product_categories` - univerzálny číselník všetkých typov kategórií

**Poznámka pre výrobcov a dodávateľov:**
- PrdPac (výrobca) a SupPac (dodávateľ) sa mapujú cez samostatnú tabuľku `product_catalog_partners` → `partner_catalog`

---

## 5. VAT_GROUPS - Skupiny DPH

**Tabuľka:** `vat_groups`  
**Popis:** Percentuálne sadzby DPH s históriou platnosti

| NEX Genesis | Typ | NEX Automat | Typ | Popis |
|-------------|-----|-------------|-----|-------|
| VatPrc | byte | vat_rate | DECIMAL(5,2) | Percentuálna sadzba DPH |
| - | - | vat_name | VARCHAR(50) | Názov sadzby |
| - | - | is_active | BOOLEAN | Aktívna/archivovaná sadzba |
| - | - | valid_from | DATE | Platnosť od |
| - | - | valid_to | DATE | Platnosť do |

**SQL CREATE TABLE:**
```sql
CREATE TABLE vat_groups (
    vat_group_id SERIAL PRIMARY KEY,
    vat_rate DECIMAL(5,2) NOT NULL,
    vat_name VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    valid_from DATE NOT NULL,
    valid_to DATE,
    created_by VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(30),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(vat_rate, valid_from)
);

CREATE INDEX idx_vat_groups_active ON vat_groups(is_active);
CREATE INDEX idx_vat_groups_valid ON vat_groups(valid_from, valid_to);

-- Trigger pre automatickú aktualizáciu updated_at
CREATE TRIGGER update_vat_groups_updated_at
    BEFORE UPDATE ON vat_groups
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

**Príklad dát:**
```sql
INSERT INTO vat_groups (vat_group_id, vat_rate, vat_name, is_active, valid_from, created_by, created_at, updated_by, updated_at) VALUES
(1, 20.00, 'Základná sadzba 20%', TRUE, '2023-01-01', 'admin', '2023-01-01 10:00:00', 'admin', '2023-01-01 10:00:00'),
(2, 10.00, 'Znížená sadzba 10%', TRUE, '2023-01-01', 'admin', '2023-01-01 10:00:00', 'admin', '2023-01-01 10:00:00'),
(3, 0.00, 'Oslobodené od DPH', TRUE, '2023-01-01', 'admin', '2023-01-01 10:00:00', 'admin', '2023-01-01 10:00:00');

-- Historická sadzba (archivovaná)
INSERT INTO vat_groups (vat_group_id, vat_rate, vat_name, is_active, valid_from, valid_to, created_by, created_at, updated_by, updated_at) VALUES
(4, 19.00, 'Základná sadzba 19% (archív)', FALSE, '2020-01-01', '2022-12-31', 'admin', '2020-01-01 10:00:00', 'admin', '2022-12-31 23:59:59');
```

---

## 6. PRODUCT_CATALOG_TEXTS - Textové informácie

**Tabuľka:** `product_catalog_texts`  
**Popis:** Rôzne typy textových informácií (dlhé názvy, poznámky...)

| NEX Genesis | Typ | NEX Automat | Typ | Text Type |
|-------------|-----|-------------|-----|-----------|
| GaName | Str60 | text | TEXT | 'extended_name' |
| Notice | Str240 | text | TEXT | 'notes' |

**Štruktúra:**
- `product_id` - numerický identifikátor produktu
- `text_type` - typ textu ('extended_name', 'notes', 'description', ...)
- `text` - samotný text
- `language` - jazyk (pre budúcu lokalizáciu)

**SQL CREATE TABLE:**
```sql
CREATE TABLE product_catalog_texts (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    text_type VARCHAR(20) NOT NULL,
    text TEXT,
    language VARCHAR(5) DEFAULT 'sk',
    created_by VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(30),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (product_id) REFERENCES product_catalog(product_id) ON DELETE CASCADE,
    UNIQUE(product_id, text_type, language)
);

CREATE INDEX idx_product_catalog_texts_product ON product_catalog_texts(product_id);
CREATE INDEX idx_product_catalog_texts_type ON product_catalog_texts(text_type);

-- Trigger pre automatickú aktualizáciu updated_at
CREATE TRIGGER update_product_catalog_texts_updated_at
    BEFORE UPDATE ON product_catalog_texts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

**Hodnoty text_type:**
- `extended_name` = doplnkový názov pre tlač (GaName)
- `notes` = poznámkový riadok (Notice)
- `description` = dlhý popis pre e-shop
- `short_description` = krátky popis
- `technical_specs` = technické parametre

---

## POLIA KTORÉ SA NEPRENÁŠAJÚ

**Dôvod:** Zastarané, nepoužité alebo nahradené lepším riešením

| NEX Genesis | Typ | Dôvod neprenášania |
|-------------|-----|--------------------|
| _GsName | Str15 | Vyhľadávacie pole - PostgreSQL full-text search |
| _GaName | Str60 | Vyhľadávacie pole - PostgreSQL full-text search |
| MinOsq | double | Nepoužité |
| BasGsc | longint | Nepoužité (väzba na základný tovar) |
| CctCod | Str10 | Nepoužité (colný kód) |
| Reserve | Str4 | Rezervované pole |
| SbcCnt | word | Počet kódov - PostgreSQL COUNT() |
| Sended | byte | Zastarané (sync flag) |
| ModNum | word | PostgreSQL má verziu cez trigger |
| IsiSnt | Str3 | Účtovné prerozúčtovanie - zastarané |
| IsiAnl | Str6 | Účtovné prerozúčtovanie - zastarané |
| IciSnt | Str3 | Účtovné prerozúčtovanie - zastarané |
| IciAnl | Str6 | Účtovné prerozúčtovanie - zastarané |
| PlsNum1-5 | word | Cenníky - nové riešenie cez tabuľku |
| NewVatPrc | Str2 | Pripravená sadzba - vat_groups.valid_from |

**Poznámka:** ModUser/ModDate/ModTime sa prenášajú ako updated_by/updated_at (viď mapping tabuľka v sekcii 1).

---

## BIZNIS LOGIKA

### business_type (ProTyp) vs product_type (GsType)
- **business_type** (M/T/S) = ČO to je z hľadiska účtovníctva a účelu:
  - M = Materiál (vstupy do výroby)
  - T = Tovar (nákup-predaj bez zmeny)
  - S = Služba (nehmotný produkt)
  
- **product_type** (T/W/O) = AKO sa to predáva/obsluhuje:
  - T = Riadny tovar (kusový predaj)
  - W = Váhový tovar (predaj na váhu)
  - O = Obal (vratné obaly)

### Trvanlivosť
- **DrbMust** = Sledovať trvanlivosť áno/nie
- **DrbDay** = Počet dní do expirácie
- **GrcMth** = Záručná doba v mesiacoch (garancie)

### Výrobné čísla vs šarže
- **PdnMust** = Výrobné/sériové číslo (unique per kus)
- **RbaTrc** = Výrobná šarža (batch, viac kusov)

### Váhové položky
- **SecNum** = Sekcia na elektronickej váhe
- **WgCode** = PLU číslo na váhe (pre integráciu)

---

## MIGRAČNÉ POZNÁMKY

### 1. Duplicitné identifikátory
V GSCAT môže byť jeden BarCode pre viac produktov. V `product_catalog_identifiers` je UNIQUE constraint. Riešenie:
```sql
-- Nájsť duplicity
SELECT identifier_code, COUNT(*) 
FROM product_catalog_identifiers 
WHERE identifier_type = 'barcode' 
GROUP BY identifier_code 
HAVING COUNT(*) > 1;
```

### 2. Merné jednotky
MsName a MsuName sú text - potrebujeme číselník `units`:
```sql
CREATE TABLE units (
    unit_id SERIAL PRIMARY KEY,
    unit_code VARCHAR(10) UNIQUE,
    unit_name VARCHAR(50),
    unit_type VARCHAR(20),  -- 'sale', 'base', 'transport'
    created_by VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(30),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Kategórie
Všetky skupiny (MgCode, FgCode, SgCode, PrdPac, SupPac) potrebujú vlastné číselníky.

---

## AUTOMATICKÁ AKTUALIZÁCIA updated_at

### Trigger funkcia (spoločná pre všetky tabuľky)

```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

**Vysvetlenie:**
- Pri každom UPDATE sa automaticky nastaví `updated_at = CURRENT_TIMESTAMP`
- `updated_by` sa musí nastaviť manuálne v aplikácii (user context)
- Toto je štandardný pattern pre všetky tabuľky NEX Automat
- Funkcia sa volá triggermi na jednotlivých tabuľkách

---

## DOKUMENTY SÚVISIACICH TABULIEK

- **product_catalog_identifiers** → `BARCODE-GSCAT-product_catalog_identifiers.md` (detailný mapping BARCODE.BTR)
- **product_categories** - Všetky typy kategórií:
  - `MGLST-product_categories.md` (tovarové skupiny)
  - `FGLST-product_categories.md` (finančné skupiny)
  - `SGLST-product_categories.md` (špecifické skupiny)
- **partner_catalog** - Partneri/Dodávatelia/Výrobcovia → `PAB-partner_catalog.md`
- **units** - Merné jednotky → `catalogs/UNITS.md`
- **DATABASE_RELATIONSHIPS** → `DATABASE_RELATIONSHIPS.md`

---

**Vytvoril:** Claude & Zoltán  
**Dátum:** 2025-12-10  
**Verzia:** 1.1  
**Status:** ✅ Schválené - aktualizované audit polia a typy identifikátorov