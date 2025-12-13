# TSH.BTR → supplier_delivery_heads

**Pre všeobecné zásady pozri:** [COMMON_DOCUMENT_PRINCIPLES.md](../../COMMON_DOCUMENT_PRINCIPLES.md)

Tento dokument popisuje **ŠPECIFICKÉ vlastnosti** dodávateľských dodacích listov (hlavičky).

---

## 1. PREHĽAD

### Účel
Hlavičky dodávateľských dodacích listov (Supplier Delivery Note Headers) obsahují základné informácie o prijatých dodávkach od dodávateľov. Slúžia ako master záznamy pre detail položky, texty a platby.

### Btrieve súbory
**Starý systém (NEX Genesis):**
```
TSH25001.BTR  - Kniha č. 1, rok 2025
TSH25002.BTR  - Kniha č. 2, rok 2025
TSH24001.BTR  - Kniha č. 1, rok 2024
```

**Nový systém (NEX Automat):**
```
supplier_delivery_heads - jedna tabuľka pre všetky knihy
```

### Vzťahy
```
supplier_delivery_heads (1 hlavička)
    ├──< supplier_delivery_items (N položiek)
    ├──< document_texts (N textov) - univerzálna tabuľka
    ├──< supplier_delivery_payments (N platieb)
    └──< supplier_delivery_vat_groups (N DPH skupín)
```

**POZNÁMKA:** Párovanie s faktúrami (`supplier_delivery_invoices`) je na úrovni **POLOŽIEK** (TSI), nie hlavičiek!

### Kľúčové entity
- **Dodávateľ:** Partner (supplier_id + supplier_modify_id) - versioning systém
- **Prevádzka dodávateľa:** Facility (supplier_facility_id + supplier_facility_modify_id) - versioning systém
- **Sklad:** Stock (stock_id)
- **Kniha dokladov:** book_num
- **Platobný spôsob:** payment_method_id
- **Dopravný spôsob:** transport_method_id

---

## 2. SQL SCHÉMA

```sql
-- =====================================================
-- HLAVIČKA DODÁVATEĽSKÝCH DODACÍCH LISTOV
-- =====================================================

CREATE TABLE supplier_delivery_heads (
    -- Technický primárny kľúč
    document_id BIGSERIAL PRIMARY KEY,
    
    -- ========================================
    -- ČÍSLOVANIE DOKLADOV
    -- Detaily v COMMON_DOCUMENT_PRINCIPLES.md
    -- ========================================
    
    document_number VARCHAR(13) NOT NULL UNIQUE,
    document_type VARCHAR(2) NOT NULL DEFAULT 'DD',
    year SMALLINT NOT NULL,
    global_sequence INTEGER NOT NULL,
    book_num INTEGER NOT NULL,
    book_sequence INTEGER NOT NULL,
    external_number VARCHAR(12),
    old_document_number VARCHAR(13),
    
    -- ========================================
    -- ZÁKLADNÉ ÚDAJE
    -- ========================================
    
    document_date DATE NOT NULL,
    stock_id INTEGER NOT NULL,
    
    -- ========================================
    -- DODÁVATEĽ (VERSIONING SYSTÉM)
    -- Detaily v COMMON_DOCUMENT_PRINCIPLES.md
    -- ========================================
    
    supplier_id INTEGER NOT NULL,
    supplier_modify_id INTEGER NOT NULL,
    supplier_facility_id INTEGER,
    supplier_facility_modify_id INTEGER,
    
    -- ========================================
    -- PLATBA A DOPRAVA
    -- ========================================
    
    payment_method_id INTEGER,
    payment_method_name VARCHAR(20),
    transport_method_id INTEGER,
    transport_method_name VARCHAR(20),
    
    -- ========================================
    -- CENNÍK A ZĽAVY
    -- ========================================
    
    price_list_id INTEGER,
    discount_percent DECIMAL(5,2),
    margin_percent DECIMAL(5,2),
    
    -- ========================================
    -- NSO (NÁKLADY SÚVISIACE S OBSTARANÍM)
    -- ========================================
    
    customs_cost_ac DECIMAL(15,2) DEFAULT 0,
    transport_cost_ac DECIMAL(15,2) DEFAULT 0,
    other_cost_ac DECIMAL(15,2) DEFAULT 0,
    acquisition_value_ac DECIMAL(15,2),
    
    -- ========================================
    -- HODNOTY V ÚČTOVNEJ MENE (AC)
    -- Detaily v COMMON_DOCUMENT_PRINCIPLES.md
    -- ========================================
    
    accounting_currency VARCHAR(3) NOT NULL DEFAULT 'EUR',
    
    -- Predajné ceny (PC)
    list_value_ac DECIMAL(15,2),
    discount_value_ac DECIMAL(15,2),
    rounding_value_ac DECIMAL(15,2),
    sales_base_value_ac DECIMAL(15,2),
    sales_total_value_ac DECIMAL(15,2),
    
    -- Nákupné ceny (NC)
    purchase_base_value_ac DECIMAL(15,2),
    purchase_vat_value_ac DECIMAL(15,2),
    purchase_total_value_ac DECIMAL(15,2),
    
    -- Marža
    margin_value_ac DECIMAL(15,2),
    
    -- ========================================
    -- HODNOTY VO VYÚČTOVACEJ MENE (FC)
    -- Detaily v COMMON_DOCUMENT_PRINCIPLES.md
    -- ========================================
    
    foreign_currency VARCHAR(3),
    foreign_currency_rate DECIMAL(15,6),
    
    -- Predajné ceny (PC)
    list_value_fc DECIMAL(15,2),
    discount_value_fc DECIMAL(15,2),
    rounding_value_fc DECIMAL(15,2),
    
    -- Nákupné ceny (NC)
    purchase_base_value_fc DECIMAL(15,2),
    purchase_vat_value_fc DECIMAL(15,2),
    purchase_total_value_fc DECIMAL(15,2),
    
    -- ========================================
    -- STAVY DOKLADU (ŠPECIFICKÉ PRE DD)
    -- ========================================
    
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    paired_status VARCHAR(1) NOT NULL DEFAULT 'N',
    is_vat_document BOOLEAN DEFAULT true,
    
    -- ========================================
    -- ŠTATISTIKA A ODKAZY
    -- ========================================
    
    item_count INTEGER DEFAULT 0,
    print_count INTEGER DEFAULT 0,
    stock_movement_id INTEGER,
    
    -- ========================================
    -- AUDIT
    -- Detaily v COMMON_DOCUMENT_PRINCIPLES.md
    -- ========================================
    
    created_by VARCHAR(8) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_by VARCHAR(8),
    updated_at TIMESTAMP,
    
    -- ========================================
    -- CONSTRAINTS
    -- ========================================
    
    CONSTRAINT uq_year_global_sequence UNIQUE (year, global_sequence),
    CONSTRAINT uq_book_sequence UNIQUE (book_num, year, book_sequence),
    CONSTRAINT chk_document_type CHECK (document_type = 'DD'),
    CONSTRAINT chk_status CHECK (status IN ('draft', 'received', 'posted')),
    CONSTRAINT chk_paired_status CHECK (paired_status IN ('N', 'P', 'Q', 'H', 'C'))
);

-- ========================================
-- INDEXY
-- ========================================

CREATE INDEX idx_supplier_delivery_heads_book ON supplier_delivery_heads(book_num);
CREATE INDEX idx_supplier_delivery_heads_supplier ON supplier_delivery_heads(supplier_id);
CREATE INDEX idx_supplier_delivery_heads_stock ON supplier_delivery_heads(stock_id);
CREATE INDEX idx_supplier_delivery_heads_date ON supplier_delivery_heads(document_date);
CREATE INDEX idx_supplier_delivery_heads_status ON supplier_delivery_heads(status);
CREATE INDEX idx_supplier_delivery_heads_paired ON supplier_delivery_heads(paired_status);
CREATE INDEX idx_supplier_delivery_heads_year_type ON supplier_delivery_heads(year, document_type);

-- ========================================
-- TRIGGERY
-- Funkcie definované v COMMON_DOCUMENT_PRINCIPLES.md
-- ========================================

CREATE TRIGGER trg_supplier_delivery_heads_updated_at
    BEFORE UPDATE ON supplier_delivery_heads
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_supplier_delivery_heads_book_sequence
    BEFORE INSERT OR UPDATE ON supplier_delivery_heads
    FOR EACH ROW
    EXECUTE FUNCTION recalculate_book_sequence();

-- =====================================================
-- DPH SKUPINY (ŠPECIFICKÉ PRE DOKLADY)
-- =====================================================

CREATE TABLE supplier_delivery_vat_groups (
    vat_group_id SERIAL PRIMARY KEY,
    delivery_head_id BIGINT NOT NULL REFERENCES supplier_delivery_heads(document_id) ON DELETE CASCADE,
    vat_rate DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT uq_delivery_vat_rate UNIQUE (delivery_head_id, vat_rate)
);

CREATE INDEX idx_supplier_delivery_vat_groups_delivery ON supplier_delivery_vat_groups(delivery_head_id);

-- =====================================================
-- DPH HODNOTY (EAV PATTERN)
-- =====================================================

CREATE TABLE supplier_delivery_vat_amounts (
    amount_id SERIAL PRIMARY KEY,
    vat_group_id INTEGER NOT NULL REFERENCES supplier_delivery_vat_groups(vat_group_id) ON DELETE CASCADE,
    amount_type VARCHAR(30) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    
    CONSTRAINT uq_vat_group_amount_type UNIQUE (vat_group_id, amount_type),
    CONSTRAINT chk_amount_type CHECK (
        amount_type IN (
            'base_ac',
            'total_ac',
            'base_fc',
            'total_fc',
            'cash_register_base_fc'
        )
    )
);

CREATE INDEX idx_supplier_delivery_vat_amounts_group ON supplier_delivery_vat_amounts(vat_group_id);
```

---

## 3. MAPPING POLÍ

### Číslovanie dokladov
**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 1

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| Year | Str2 | year | SMALLINT | 25 → 2025 |
| SerNum | longint | global_sequence | INTEGER | Globálne poradie |
| DocNum | Str12 | document_number | VARCHAR(13) | DD2500000123 |
| ExtNum | Str12 | external_number | VARCHAR(12) | Číslo dodávateľa |
| - | - | book_num | INTEGER | Z TSH25001 → 1 |
| - | - | book_sequence | INTEGER | Auto-trigger |
| - | - | old_document_number | VARCHAR(13) | Migrácia |

### Základné údaje

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| DocDate | DateType | document_date | DATE |
| StkNum | word | stock_id | INTEGER |

### Dodávateľ (Versioning)
**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 2

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| PaCode | longint | supplier_id | INTEGER | ID partnera |
| - | - | supplier_modify_id | INTEGER | Verzia (NOVÉ) |
| PaName, RegName, RegIno... | - | - | - | V partner_catalog_history |
| WpaCode | word | supplier_facility_id | INTEGER | ID prevádzky |
| - | - | supplier_facility_modify_id | INTEGER | Verzia (NOVÉ) |
| WpaName, WpaAddr... | - | - | - | V partner_facilities_history |

### Platba a doprava

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| PayCode | Str3 | payment_method_id | INTEGER |
| PayName | Str20 | payment_method_name | VARCHAR(20) |
| TrsCode | Str3 | transport_method_id | INTEGER |
| TrsName | Str20 | transport_method_name | VARCHAR(20) |

### Cenník a zľavy

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| PlsNum | word | price_list_id | INTEGER |
| DscPrc | double | discount_percent | DECIMAL(5,2) |
| PrfPrc | double | margin_percent | DECIMAL(5,2) |

### NSO (Náklady súvisiace s obstaraním)

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| AcZValue | double | customs_cost_ac | DECIMAL(15,2) | Colné náklady |
| AcTValue | double | transport_cost_ac | DECIMAL(15,2) | Doprava |
| AcOValue | double | other_cost_ac | DECIMAL(15,2) | Ostatné |
| AcSValue | double | acquisition_value_ac | DECIMAL(15,2) | OC s NSO |

### Hodnoty v účtovnej mene (AC)
**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 5

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| AcDvzName | Str3 | accounting_currency | VARCHAR(3) |
| AcDValue | double | list_value_ac | DECIMAL(15,2) |
| AcDscVal | double | discount_value_ac | DECIMAL(15,2) |
| AcRndVal | double | rounding_value_ac | DECIMAL(15,2) |
| AcAValue | double | sales_base_value_ac | DECIMAL(15,2) |
| AcBValue | double | sales_total_value_ac | DECIMAL(15,2) |
| AcCValue | double | purchase_base_value_ac | DECIMAL(15,2) |
| AcVatVal | double | purchase_vat_value_ac | DECIMAL(15,2) |
| AcEValue | double | purchase_total_value_ac | DECIMAL(15,2) |
| AcPrfVal | double | margin_value_ac | DECIMAL(15,2) |

### Hodnoty vo vyúčtovacej mene (FC)
**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 5

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| FgDvzName | Str3 | foreign_currency | VARCHAR(3) |
| FgCourse | double | foreign_currency_rate | DECIMAL(15,6) |
| FgDValue | double | list_value_fc | DECIMAL(15,2) |
| FgDscVal | double | discount_value_fc | DECIMAL(15,2) |
| FgRndVal | double | rounding_value_fc | DECIMAL(15,2) |
| FgCValue | double | purchase_base_value_fc | DECIMAL(15,2) |
| FgVatVal | double | purchase_vat_value_fc | DECIMAL(15,2) |
| FgEValue | double | purchase_total_value_fc | DECIMAL(15,2) |

### DPH skupiny (Multi-row → EAV)

| Btrieve | PostgreSQL Tabuľka | Amount Type |
|---------|-------------------|-------------|
| VatPrc1-5 | supplier_delivery_vat_groups | vat_rate |
| AcCValue1-5 | supplier_delivery_vat_amounts | base_ac |
| AcEValue1-5 | supplier_delivery_vat_amounts | total_ac |
| FgCValue1-5 | supplier_delivery_vat_amounts | base_fc |
| FgEValue1-5 | supplier_delivery_vat_amounts | total_fc |
| FgCsdVal1-5 | supplier_delivery_vat_amounts | cash_register_base_fc |

### Stavy dokladu

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| DstStk | Str1 | status | VARCHAR(20) | N→draft, S→received/posted |
| DstAcc | Str1 | status | VARCHAR(20) | ''→draft/received, A→posted |
| DstPair | Str1 | paired_status | VARCHAR(1) | N/P/Q/H/C |
| VatDoc | byte | is_vat_document | BOOLEAN | Daňový doklad |

### Štatistika

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| ItmQnt | word | item_count | INTEGER |
| PrnCnt | byte | print_count | INTEGER |
| SmCode | word | stock_movement_id | INTEGER |

### Audit
**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 7

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| CrtUser | Str8 | created_by | VARCHAR(8) | - |
| CrtDate + CrtTime | Date + Time | created_at | TIMESTAMP | Zlúčené |
| ModUser | Str8 | updated_by | VARCHAR(8) | - |
| ModDate + ModTime | Date + Time | updated_at | TIMESTAMP | Zlúčené |

### NEPRENESENÉ POLIA
**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 9.3

Pracovné polia, staré odkazy, zastarané funkcie - kompletný zoznam v COMMON.

---

## 4. BIZNIS LOGIKA (ŠPECIFICKÉ PRE DD)

### Lifecycle dokladu

```
┌─────────┐   Prijať    ┌──────────┐   Zaúčtovať   ┌────────┐
│  DRAFT  │  na sklad   │ RECEIVED │   do účt.     │ POSTED │
│ (N, '') │ ─────────> │ (S, '')  │ ──────────>  │ (S, A) │
└─────────┘             └──────────┘               └────────┘

DstStk: N = Not received, S = Stocked
DstAcc: '' = Not posted, A = Accounted
```

**Pravidlá:**
1. **Draft → Received:** Vytvorenie STM záznamov, aktualizácia stock_cards
2. **Received → Posted:** Zaúčtovanie do podvojného účtovníctva
3. **Nie je možné zmeniť doklad v stave Posted**

---

### Paired status (Vypárovanie)

**Cesta A: Faktúry** (vypárovanie na úrovni POLOŽIEK!)
```
N (nič) → P (čiastočne) → Q (celé)
```

**Cesta B: Pokladnica**
```
N (nič) → H (čiastočne) → C (celé)
```

**Stavy:**
- **N** - Not paired: Nič nie je vypárované ani uhradené
- **P** - Partially paired: Časť položiek je na faktúre/ách
- **Q** - Queued/Paired: Celý doklad vypárovaný s faktúrou/ami
- **H** - Half paid: Časť hodnoty cez pokladnicu
- **C** - Cash register paid: Celá hodnota cez pokladnicu

**KRITICKÉ:** 
- Párovanie s faktúrami je na úrovni **POLOŽIEK** (TSI), nie hlavičiek!
- `paired_status` v hlavičke je agregovaný stav z položiek
- Nemôže byť zmiešané (buď faktúra alebo pokladnica)

---

### NSO (Náklady súvisiace s obstaraním)

**Koncept:**
```
Obstarávacia cena = Nákupná cena + NSO náklady

acquisition_value_ac = purchase_base_value_ac + 
                       customs_cost_ac + 
                       transport_cost_ac + 
                       other_cost_ac
```

**Rozdelenie NSO:**
- NSO náklady sa zadávajú na úrovni **hlavičky**
- Aliquotne sa rozdeľujú na **položky** (podľa pomeru NC položky)
- Detail rozdelenia je v TSI-supplier_delivery_items.md

---

### Výpočet marže

```
Marža = Predajná cena - Nákupná cena
margin_value_ac = sales_base_value_ac - purchase_base_value_ac

Marža % = (Marža / Nákupná cena) × 100
margin_percent = (margin_value_ac / purchase_base_value_ac) × 100
```

---

### DPH skupiny (EAV Pattern)

**Prečo EAV pattern?**
- V Btrieve: fixné polia VatPrc1-5, AcCValue1-5, FgCValue1-5...
- V PostgreSQL: dynamické riadky pre každú DPH sadzbu
- Flexibilita: ľahko pridať nové typy hodnôt

**Príklad:**
```python
# Vytvor doklad
delivery = create_delivery_head(...)

# Vytvor DPH skupiny
vat_group_1 = create_vat_group(delivery_id, vat_rate=20.00)
vat_group_2 = create_vat_group(delivery_id, vat_rate=10.00)

# Vytvor hodnoty pre každú skupinu
create_vat_amount(vat_group_1, 'base_ac', 1000.00)
create_vat_amount(vat_group_1, 'total_ac', 1200.00)
create_vat_amount(vat_group_2, 'base_ac', 500.00)
create_vat_amount(vat_group_2, 'total_ac', 550.00)
```

---

## 5. VZŤAHY S INÝMI TABUĽKAMI

### Master-Detail vzťahy

```sql
-- Položky (1:N) - CASCADE
supplier_delivery_heads (1) ──< (N) supplier_delivery_items
    ON DELETE CASCADE

-- Texty (1:N) - CASCADE - UNIVERZÁLNA TABUĽKA!
supplier_delivery_heads (1) ──< (N) document_texts
    WHERE document_type = 'supplier_delivery'
    ON DELETE CASCADE

-- Platby (1:N) - CASCADE
supplier_delivery_heads (1) ──< (N) supplier_delivery_payments
    ON DELETE CASCADE

-- DPH skupiny (1:N) - CASCADE
supplier_delivery_heads (1) ──< (N) supplier_delivery_vat_groups
    ON DELETE CASCADE
```

### Reference na katalógy (Versioning)
**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 2

```sql
-- Partner + Verzia
supplier_id + supplier_modify_id → partner_catalog_history

-- Prevádzka + Verzia
supplier_facility_id + supplier_facility_modify_id → partner_facilities_history

-- Ostatné katalógy
stock_id → stocks (RESTRICT)
payment_method_id → payment_methods (RESTRICT)
transport_method_id → transport_methods (RESTRICT)
```

### Reference na skladové systémy

```sql
stock_movement_id → stock_card_movements.movement_id
```

---

## 6. QUERY PATTERNS

### Zobrazenie dokladu s partnerom

```sql
SELECT 
    d.document_number,
    d.document_date,
    d.status,
    d.paired_status,
    
    -- Partner z history (správna verzia!)
    ph.name AS supplier_name,
    ph.reg_name AS supplier_reg_name,
    ph.ino AS supplier_ino,
    ph.street AS supplier_street,
    
    -- Hodnoty
    d.purchase_base_value_ac,
    d.purchase_vat_value_ac,
    d.purchase_total_value_ac,
    d.margin_value_ac
    
FROM supplier_delivery_heads d
LEFT JOIN partner_catalog_history ph
    ON ph.partner_id = d.supplier_id
    AND ph.modify_id = d.supplier_modify_id
WHERE d.document_id = $1;
```

### Zobrazenie DPH skupín

```sql
SELECT 
    g.vat_rate,
    MAX(CASE WHEN a.amount_type = 'base_ac' THEN a.amount END) AS base_ac,
    MAX(CASE WHEN a.amount_type = 'total_ac' THEN a.amount END) AS total_ac
FROM supplier_delivery_vat_groups g
LEFT JOIN supplier_delivery_vat_amounts a ON a.vat_group_id = g.vat_group_id
WHERE g.delivery_head_id = $1
GROUP BY g.vat_rate
ORDER BY g.vat_rate DESC;
```

### Nevypárované dodacie listy

```sql
SELECT 
    d.document_number,
    d.document_date,
    ph.name AS supplier_name,
    d.purchase_total_value_ac
FROM supplier_delivery_heads d
LEFT JOIN partner_catalog_history ph
    ON ph.partner_id = d.supplier_id
    AND ph.modify_id = d.supplier_modify_id
WHERE d.paired_status = 'N'
  AND d.status = 'received'
ORDER BY d.document_date;
```

### Doklady s maržou nad X %

```sql
SELECT 
    d.document_number,
    ph.name AS supplier_name,
    d.margin_percent,
    d.margin_value_ac
FROM supplier_delivery_heads d
LEFT JOIN partner_catalog_history ph
    ON ph.partner_id = d.supplier_id
    AND ph.modify_id = d.supplier_modify_id
WHERE d.margin_percent > $1
  AND d.status = 'posted'
ORDER BY d.margin_percent DESC;
```

---

## 7. PRÍKLAD DÁT

### Doklad - Draft

```sql
INSERT INTO supplier_delivery_heads (
    document_number, year, global_sequence,
    book_num, external_number,
    document_date, stock_id,
    supplier_id, supplier_modify_id,
    accounting_currency,
    purchase_base_value_ac, purchase_vat_value_ac, purchase_total_value_ac,
    status, paired_status,
    created_by, created_at
) VALUES (
    'DD2500000123', 2025, 123,
    1, 'DL-2025-456',
    '2025-01-15', 1,
    456, 0,
    'EUR',
    1500.00, 315.00, 1815.00,
    'draft', 'N',
    'zoltan', '2025-01-15 10:30:00'
);
```

### DPH skupiny

```sql
-- DPH 20%
INSERT INTO supplier_delivery_vat_groups (delivery_head_id, vat_rate)
VALUES (1, 20.00);

INSERT INTO supplier_delivery_vat_amounts (vat_group_id, amount_type, amount)
VALUES 
    (1, 'base_ac', 1000.00),
    (1, 'total_ac', 1200.00);

-- DPH 10%
INSERT INTO supplier_delivery_vat_groups (delivery_head_id, vat_rate)
VALUES (1, 10.00);

INSERT INTO supplier_delivery_vat_amounts (vat_group_id, amount_type, amount)
VALUES 
    (2, 'base_ac', 500.00),
    (2, 'total_ac', 550.00);
```

---

## 8. MIGRÁCIA

### Versioning pri migrácii
**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 9.2

**Pred migráciou dokladov:**
1. Migruj partnerov do `partner_catalog_history` s `modify_id = 0`
2. Migruj prevádzky do `partner_facilities_history` s `modify_id = 0`

**Pri migrácii dokladu:**
```python
insert_delivery_head(
    supplier_id=record.PaCode,
    supplier_modify_id=0,  # Prvá verzia
    supplier_facility_id=record.WpaCode,
    supplier_facility_modify_id=0,
    ...
)
```

### DPH skupiny

```python
def migrate_vat_groups(record, delivery_head_id):
    for i in range(1, 6):
        vat_rate = getattr(record, f'VatPrc{i}')
        if vat_rate > 0:
            vat_group_id = insert_vat_group(delivery_head_id, vat_rate)
            
            insert_vat_amount(vat_group_id, 'base_ac', getattr(record, f'AcCValue{i}'))
            insert_vat_amount(vat_group_id, 'total_ac', getattr(record, f'AcEValue{i}'))
            insert_vat_amount(vat_group_id, 'base_fc', getattr(record, f'FgCValue{i}'))
            insert_vat_amount(vat_group_id, 'total_fc', getattr(record, f'FgEValue{i}'))
```

### Stavy dokladu

```python
def get_status(record):
    if record.DstAcc == 'A':
        return 'posted'
    elif record.DstStk == 'S':
        return 'received'
    else:
        return 'draft'

paired_status = record.DstPair  # N, P, Q, H, C
```

### Validácia po migrácii

```sql
-- Kontrola počtu záznamov
SELECT book_num, year, COUNT(*) 
FROM supplier_delivery_heads
GROUP BY book_num, year;

-- Kontrola DPH skupín
SELECT 
    COUNT(DISTINCT d.document_id) AS delivery_count,
    COUNT(g.vat_group_id) AS vat_group_count,
    COUNT(a.amount_id) AS vat_amount_count
FROM supplier_delivery_heads d
LEFT JOIN supplier_delivery_vat_groups g ON g.delivery_head_id = d.document_id
LEFT JOIN supplier_delivery_vat_amounts a ON a.vat_group_id = g.vat_group_id;
```

---

## 9. VERZIA A ZMENY

### Verzia dokumentu
**Verzia:** 2.0  
**Dátum:** 2025-12-13  
**Autor:** Zoltán + Claude  
**Session:** 6-7

### História zmien

| Verzia | Dátum | Zmeny |
|--------|-------|-------|
| 2.0 | 2025-12-13 | Optimalizácia: odstránené duplicity z COMMON, odstránené supplier_delivery_invoices, aktualizácia na document_texts |
| 1.0 | 2025-12-12 | Vytvorenie prvej verzie |

### Závislosti

**Tento dokument vyžaduje:**
- `COMMON_DOCUMENT_PRINCIPLES.md` - všeobecné zásady
- `partner_catalog` + `partner_catalog_history` - versioning
- `partner_facilities` + `partner_facilities_history` - versioning
- `stocks`, `payment_methods`, `transport_methods` - číselníky

**Súvisiace dokumenty:**
- `TSI-supplier_delivery_items.md` - položky dodacích listov
- `document_texts` - texty (univerzálna tabuľka)
- `TSP-supplier_delivery_payments.md` - platby

### Poznámky

1. **supplier_delivery_invoices** je v TSI (M:N medzi položkami a faktúrami), NIE v TSH!
2. **document_texts** je univerzálna tabuľka pre všetky typy dokladov
3. **paired_status** v hlavičke je agregovaný z položiek
4. **NSO náklady** sa rozdeľujú aliquotne na položky (detail v TSI)

---

**Koniec dokumentu TSH-supplier_delivery_heads.md v2.0**