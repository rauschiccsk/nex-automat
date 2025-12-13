# ISI.BTR → supplier_invoice_items

**Pre všeobecné zásady pozri:** [COMMON_DOCUMENT_PRINCIPLES.md](../../COMMON_DOCUMENT_PRINCIPLES.md)

Tento dokument popisuje **ŠPECIFICKÉ vlastnosti** dodávateľských faktúr (položky).

---

## 1. PREHĽAD

### Účel
Položky dodávateľských faktúr (Supplier Invoice Items) obsahujú detail jednotlivých produktov/služieb na faktúre. Každá položka reprezentuje jeden riadok faktúry s množstvom, cenou a DPH.

### Btrieve súbory
**Starý systém (NEX Genesis):**
```
ISI25001.BTR  - Kniha č. 1, rok 2025
ISI25002.BTR  - Kniha č. 2, rok 2025
ISI24001.BTR  - Kniha č. 1, rok 2024
```

**Nový systém (NEX Automat):**
```
supplier_invoice_items - jedna tabuľka pre všetky knihy
```

### Vzťahy
```
supplier_invoice_heads (1 hlavička)
    └──< supplier_invoice_items (N položiek)
        ├──< supplier_order_invoices (M:N s objednávkami) - NOVÁ!
        └──< supplier_delivery_invoices (M:N s dodacími listami) - existuje
```

**KRITICKÉ:** Párovanie s dodacími listami a objednávkami je na úrovni **POLOŽIEK**, nie hlavičiek!

### Kľúčové entity
- **Hlavička faktúry:** supplier_invoice_heads (invoice_head_id)
- **Produkt:** Product (product_id + product_modify_id) - versioning systém
- **Tovarová skupina:** Product Category (product_category_id)
- **Sklad:** Stock (stock_id)
- **Prevádzka:** Facility (facility_id)

---

## 2. SQL SCHÉMA

```sql
-- =====================================================
-- POLOŽKY DODÁVATEĽSKÝCH FAKTÚR
-- =====================================================

CREATE TABLE supplier_invoice_items (
    -- Technický primárny kľúč
    item_id BIGSERIAL PRIMARY KEY,
    
    -- ========================================
    -- HLAVIČKA FAKTÚRY
    -- ========================================
    
    invoice_head_id BIGINT NOT NULL REFERENCES supplier_invoice_heads(document_id) ON DELETE CASCADE,
    line_number INTEGER NOT NULL,
    
    -- ========================================
    -- PRODUKT (VERSIONING SYSTÉM)
    -- Detaily v COMMON_DOCUMENT_PRINCIPLES.md
    -- ========================================
    
    product_id INTEGER NOT NULL,
    product_modify_id INTEGER NOT NULL,
    product_category_id INTEGER,
    
    -- ========================================
    -- ZÁKLADNÉ ÚDAJE
    -- ========================================
    
    facility_id INTEGER,
    stock_id INTEGER NOT NULL,
    unit_of_measure VARCHAR(10),
    quantity DECIMAL(15,3) NOT NULL,
    vat_rate DECIMAL(5,2) NOT NULL,
    discount_percent DECIMAL(5,2) DEFAULT 0,
    
    -- ========================================
    -- CENY V ÚČTOVNEJ MENE (AC)
    -- Detaily v COMMON_DOCUMENT_PRINCIPLES.md
    -- ========================================
    
    -- Pred zľavou
    list_unit_price_ac DECIMAL(15,2),
    list_value_ac DECIMAL(15,2),
    discount_value_ac DECIMAL(15,2),
    
    -- Po zľave (nákupné ceny - NC)
    purchase_unit_price_ac DECIMAL(15,2),
    purchase_base_value_ac DECIMAL(15,2),
    purchase_total_value_ac DECIMAL(15,2),
    
    -- Predajné ceny (PC)
    sales_base_value_ac DECIMAL(15,2),
    sales_total_value_ac DECIMAL(15,2),
    
    -- ========================================
    -- CENY VO VYÚČTOVACEJ MENE (FC)
    -- Detaily v COMMON_DOCUMENT_PRINCIPLES.md
    -- ========================================
    
    -- Pred zľavou
    list_unit_price_fc DECIMAL(15,2),
    list_value_fc DECIMAL(15,2),
    discount_value_fc DECIMAL(15,2),
    
    -- Po zľave (nákupné ceny - NC)
    purchase_unit_price_fc DECIMAL(15,2),
    purchase_base_value_fc DECIMAL(15,2),
    purchase_total_value_fc DECIMAL(15,2),
    
    -- ========================================
    -- ÚČTOVANIE (ŠPECIFICKÉ PRE FAKTÚRY)
    -- ========================================
    
    synthetic_account VARCHAR(3),
    analytical_account VARCHAR(6),
    
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
    
    CONSTRAINT uq_invoice_line UNIQUE (invoice_head_id, line_number),
    CONSTRAINT chk_quantity CHECK (quantity > 0),
    CONSTRAINT chk_vat_rate CHECK (vat_rate >= 0 AND vat_rate <= 100),
    CONSTRAINT chk_discount CHECK (discount_percent >= 0 AND discount_percent <= 100)
);

-- ========================================
-- INDEXY
-- ========================================

CREATE INDEX idx_supplier_invoice_items_invoice ON supplier_invoice_items(invoice_head_id);
CREATE INDEX idx_supplier_invoice_items_product ON supplier_invoice_items(product_id);
CREATE INDEX idx_supplier_invoice_items_category ON supplier_invoice_items(product_category_id);
CREATE INDEX idx_supplier_invoice_items_stock ON supplier_invoice_items(stock_id);

-- ========================================
-- TRIGGERY
-- Funkcie definované v COMMON_DOCUMENT_PRINCIPLES.md
-- ========================================

CREATE TRIGGER trg_supplier_invoice_items_updated_at
    BEFORE UPDATE ON supplier_invoice_items
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Aktualizácia item_count v hlavičke
CREATE TRIGGER trg_supplier_invoice_items_count
    AFTER INSERT OR DELETE ON supplier_invoice_items
    FOR EACH ROW
    EXECUTE FUNCTION update_invoice_head_item_count();

-- =====================================================
-- M:N PÁROVANIE S OBJEDNÁVKAMI (NOVÁ TABUĽKA!)
-- =====================================================

CREATE TABLE supplier_order_invoices (
    pairing_id SERIAL PRIMARY KEY,
    order_item_id BIGINT NOT NULL,
    invoice_item_id BIGINT NOT NULL REFERENCES supplier_invoice_items(item_id) ON DELETE CASCADE,
    paired_quantity DECIMAL(15,3) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(8) NOT NULL,
    
    CONSTRAINT uq_order_invoice_pairing UNIQUE (order_item_id, invoice_item_id),
    CONSTRAINT chk_paired_quantity CHECK (paired_quantity > 0)
);

CREATE INDEX idx_supplier_order_invoices_order ON supplier_order_invoices(order_item_id);
CREATE INDEX idx_supplier_order_invoices_invoice ON supplier_order_invoices(invoice_item_id);

-- =====================================================
-- M:N PÁROVANIE S DODACÍMI LISTAMI (UŽ EXISTUJE V TSI!)
-- =====================================================

-- POZNÁMKA: Tabuľka supplier_delivery_invoices už existuje z TSI Session 7
-- Tu len pripomíname jej použitie:

-- supplier_delivery_invoices (
--     pairing_id SERIAL PRIMARY KEY,
--     delivery_item_id BIGINT NOT NULL REFERENCES supplier_delivery_items(item_id),
--     invoice_item_id BIGINT NOT NULL REFERENCES supplier_invoice_items(item_id),
--     paired_quantity DECIMAL(15,3) NOT NULL,
--     created_at TIMESTAMP,
--     created_by VARCHAR(8)
-- );
```

---

## 3. MAPPING POLÍ

### Hlavička a číslovanie

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| DocNum | Str12 | invoice_head_id | BIGINT | FK na supplier_invoice_heads |
| ItmNum | word | line_number | INTEGER | 1, 2, 3... |

### Produkt (Versioning)
**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 2

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| GsCode | longint | product_id | INTEGER | ID produktu |
| - | - | product_modify_id | INTEGER | Verzia (NOVÉ) |
| GsName, BarCode, StkCode | - | - | - | V product_catalog_history |
| MgCode | word | product_category_id | INTEGER | Tovarová skupina |

### Základné údaje

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| WriNum | word | facility_id | INTEGER |
| StkNum | word | stock_id | INTEGER |
| MsName | Str10 | unit_of_measure | VARCHAR(10) |
| GsQnt | double | quantity | DECIMAL(15,3) |
| VatPrc | byte | vat_rate | DECIMAL(5,2) |
| DscPrc | double | discount_percent | DECIMAL(5,2) |

### Ceny v účtovnej mene (AC)
**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 5

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| AcDValue | double | list_value_ac | DECIMAL(15,2) | NC pred zľavou |
| AcDscVal | double | discount_value_ac | DECIMAL(15,2) | Hodnota zľavy |
| AcCValue | double | purchase_base_value_ac | DECIMAL(15,2) | NC bez DPH |
| AcEValue | double | purchase_total_value_ac | DECIMAL(15,2) | NC s DPH |
| AcAValue | double | sales_base_value_ac | DECIMAL(15,2) | PC bez DPH |
| AcBValue | double | sales_total_value_ac | DECIMAL(15,2) | PC s DPH |
| - | - | list_unit_price_ac | DECIMAL(15,2) | NC/MJ pred zľavou (vypočítané) |
| - | - | purchase_unit_price_ac | DECIMAL(15,2) | NC/MJ po zľave (vypočítané) |

### Ceny vo vyúčtovacej mene (FC)
**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 5

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| FgDPrice | double | list_unit_price_fc | DECIMAL(15,2) |
| FgCPrice | double | purchase_unit_price_fc | DECIMAL(15,2) |
| FgEPrice | double | - | - |
| FgDValue | double | list_value_fc | DECIMAL(15,2) |
| FgDscVal | double | discount_value_fc | DECIMAL(15,2) |
| FgCValue | double | purchase_base_value_fc | DECIMAL(15,2) |
| FgEValue | double | purchase_total_value_fc | DECIMAL(15,2) |

### Účtovanie (ŠPECIFICKÉ PRE FAKTÚRY)

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| AccSnt | Str3 | synthetic_account | VARCHAR(3) |
| AccAnl | Str8 | analytical_account | VARCHAR(6) |

### Párovanie (M:N tabuľky)

| Btrieve | Typ | PostgreSQL Tabuľka | Poznámka |
|---------|-----|-------------------|----------|
| OsdNum | Str12 | supplier_order_invoices | M:N s objednávkami |
| OsdItm | word | supplier_order_invoices | - |
| TsdNum | Str12 | supplier_delivery_invoices | M:N s dodacími listami |
| TsdItm | word | supplier_delivery_invoices | - |

### Audit
**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 7

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| CrtUser | Str8 | created_by | VARCHAR(8) | - |
| CrtDate + CrtTime | Date + Time | created_at | TIMESTAMP | Zlúčené |
| ModUser | Str8 | updated_by | VARCHAR(8) | - |
| ModDate + ModTime | Date + Time | updated_at | TIMESTAMP | Zlúčené |

### NEPRENESENÉ POLIA

**Duplicity z hlavičky:**
- DocDate, PaCode (sú v supplier_invoice_heads)

**Zastaralé/Nepoužívané:**
- Status (zastaralé)
- Cctvat (prenesená daňová povinnosť)
- TsdDate (duplicita z TSH.document_date)
- Notice (ide do document_texts)

**Nepotrebné pre faktúry:**
- ExpDate, BatNum (šarža/trvanlivosť - faktúry neskladníme)
- NSO rozdelenie (len na dodacích listoch)
- stock_status, financial_status (len na dodacích listoch)

---

## 4. BIZNIS LOGIKA (ŠPECIFICKÉ PRE ISI)

### Výpočet cien

**Vzorce (rovnaké ako TSI):**
```python
# Jednotková cena pred zľavou
list_unit_price_ac = list_value_ac / quantity

# Hodnota zľavy
discount_value_ac = list_value_ac * (discount_percent / 100)

# Nákupná cena bez DPH
purchase_base_value_ac = list_value_ac - discount_value_ac

# Jednotková nákupná cena
purchase_unit_price_ac = purchase_base_value_ac / quantity

# Nákupná cena s DPH
purchase_total_value_ac = purchase_base_value_ac * (1 + vat_rate / 100)
```

---

### Párovanie s objednávkami (M:N) - NOVÉ! ⭐

**Koncept:**
```
Objednávka (100 ks)
    ↓ M:N supplier_order_invoices
Faktúra položka 1 (60 ks)
Faktúra položka 2 (40 ks)
```

**Tabuľka supplier_order_invoices:**
```sql
CREATE TABLE supplier_order_invoices (
    pairing_id SERIAL PRIMARY KEY,
    order_item_id BIGINT NOT NULL,           -- Položka objednávky
    invoice_item_id BIGINT NOT NULL,         -- Položka faktúry
    paired_quantity DECIMAL(15,3) NOT NULL,  -- Vypárované množstvo
    created_at TIMESTAMP,
    created_by VARCHAR(8)
);
```

**Pravidlá:**
1. Jedna položka objednávky môže byť vypárovaná s viacerými položkami faktúr
2. Jedna položka faktúry môže byť vypárovaná s viacerými položkami objednávok
3. Suma `paired_quantity` nesmie presiahnuť `quantity` v objednávke
4. Suma `paired_quantity` nesmie presiahnuť `quantity` vo faktúre

**Príklad párovanie:**
```python
def pair_invoice_with_order(
    invoice_item_id: int,
    order_item_id: int,
    paired_quantity: Decimal,
    created_by: str
):
    """Vypáruj položku faktúry s položkou objednávky."""
    
    # Validácia
    invoice_item = get_invoice_item(invoice_item_id)
    order_item = get_order_item(order_item_id)
    
    # Kontrola množstva
    already_paired = sum_paired_quantity_invoice(invoice_item_id)
    if already_paired + paired_quantity > invoice_item.quantity:
        raise ValueError("Prekročené množstvo faktúry")
    
    # Vytvor párovanie
    db.execute("""
        INSERT INTO supplier_order_invoices (
            order_item_id, invoice_item_id,
            paired_quantity, created_by
        ) VALUES (%s, %s, %s, %s)
    """, [order_item_id, invoice_item_id, paired_quantity, created_by])
    
    # Aktualizuj paired_status v hlavičke (agregovaný)
    update_invoice_paired_status(invoice_item.invoice_head_id)
```

---

### Párovanie s dodacími listami (M:N) - EXISTUJE! ⭐

**POZNÁMKA:** Tabuľka `supplier_delivery_invoices` už existuje z TSI Session 7!

**Koncept:**
```
Dodací list (60 ks)
    ↓ M:N supplier_delivery_invoices
Faktúra položka (60 ks)
```

**Tabuľka supplier_delivery_invoices:**
```sql
-- UŽ EXISTUJE v TSI!
CREATE TABLE supplier_delivery_invoices (
    pairing_id SERIAL PRIMARY KEY,
    delivery_item_id BIGINT NOT NULL,        -- Položka DD
    invoice_item_id BIGINT NOT NULL,         -- Položka DF
    paired_quantity DECIMAL(15,3) NOT NULL,  -- Vypárované množstvo
    created_at TIMESTAMP,
    created_by VARCHAR(8)
);
```

**Pravidlá:** Rovnaké ako pri objednávkach.

---

### Agregovaný paired_status v hlavičke

**paired_status v supplier_invoice_heads je VYPOČÍTANÝ z položiek:**

```python
def calculate_paired_status(invoice_head_id: int) -> str:
    """
    Vypočítaj paired_status hlavičky z položiek.
    
    Returns:
        'N' - Not paired (nič nevypárované)
        'P' - Partially paired (časť vypárovaná)
        'Q' - Queued/Paired (celé vypárované)
    """
    items = get_invoice_items(invoice_head_id)
    
    total_quantity = sum(item.quantity for item in items)
    paired_quantity = 0
    
    for item in items:
        # Spočítaj vypárované množstvo z delivery_invoices
        paired = db.query("""
            SELECT SUM(paired_quantity)
            FROM supplier_delivery_invoices
            WHERE invoice_item_id = %s
        """, [item.item_id]).scalar() or 0
        
        paired_quantity += paired
    
    if paired_quantity == 0:
        return 'N'  # Nič
    elif paired_quantity < total_quantity:
        return 'P'  # Čiastočne
    else:
        return 'Q'  # Celé
```

---

### Účtovanie položiek

**Každá položka môže mať vlastné účtovanie:**

```sql
SELECT 
    i.line_number,
    i.synthetic_account,
    i.analytical_account,
    i.purchase_base_value_ac,
    i.purchase_total_value_ac
FROM supplier_invoice_items i
WHERE i.invoice_head_id = $1
ORDER BY i.line_number;
```

**Použitie:**
- Rozúčtovanie faktúry na rôzne účty
- Analytické účtovníctvo
- Strediskové účtovníctvo

---

## 5. VZŤAHY S INÝMI TABUĽKAMI

### Master-Detail vzťahy

```sql
-- Hlavička (1:N) - CASCADE
supplier_invoice_heads (1) ──< (N) supplier_invoice_items
    ON DELETE CASCADE
```

### Reference na katalógy (Versioning)
**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 2

```sql
-- Produkt + Verzia
product_id + product_modify_id → product_catalog_history

-- Ostatné katalógy
product_category_id → product_categories (RESTRICT)
stock_id → stocks (RESTRICT)
facility_id → facilities (RESTRICT)
```

### M:N Párovanie

```sql
-- Párovanie s objednávkami (M:N) - NOVÁ!
supplier_order_items (M) ──< supplier_order_invoices >── (N) supplier_invoice_items

-- Párovanie s dodacími listami (M:N) - EXISTUJE!
supplier_delivery_items (M) ──< supplier_delivery_invoices >── (N) supplier_invoice_items
```

---

## 6. QUERY PATTERNS

### Zobrazenie položiek faktúry s produktom

```sql
SELECT 
    i.line_number,
    i.quantity,
    i.unit_of_measure,
    i.vat_rate,
    
    -- Produkt z history (správna verzia!)
    ph.code AS product_code,
    ph.name AS product_name,
    ph.barcode AS product_barcode,
    
    -- Ceny
    i.purchase_unit_price_ac,
    i.purchase_base_value_ac,
    i.purchase_total_value_ac,
    
    -- Účtovanie
    i.synthetic_account,
    i.analytical_account
    
FROM supplier_invoice_items i
LEFT JOIN product_catalog_history ph
    ON ph.product_id = i.product_id
    AND ph.modify_id = i.product_modify_id
WHERE i.invoice_head_id = $1
ORDER BY i.line_number;
```

### Celková hodnota faktúry (agregácia)

```sql
SELECT 
    h.document_number,
    SUM(i.purchase_base_value_ac) AS total_base,
    SUM(i.purchase_total_value_ac) AS total_with_vat,
    COUNT(*) AS item_count
FROM supplier_invoice_heads h
JOIN supplier_invoice_items i ON i.invoice_head_id = h.document_id
WHERE h.document_id = $1
GROUP BY h.document_id, h.document_number;
```

### Párovanie s dodacími listami

```sql
SELECT 
    i.line_number AS invoice_line,
    ph.name AS product_name,
    i.quantity AS invoice_quantity,
    
    -- Vypárované dodacie listy
    d.document_number AS delivery_number,
    di.line_number AS delivery_line,
    p.paired_quantity
    
FROM supplier_invoice_items i
LEFT JOIN product_catalog_history ph
    ON ph.product_id = i.product_id
    AND ph.modify_id = i.product_modify_id
LEFT JOIN supplier_delivery_invoices p ON p.invoice_item_id = i.item_id
LEFT JOIN supplier_delivery_items di ON di.item_id = p.delivery_item_id
LEFT JOIN supplier_delivery_heads d ON d.document_id = di.delivery_head_id
WHERE i.invoice_head_id = $1
ORDER BY i.line_number, d.document_number;
```

### Párovanie s objednávkami

```sql
SELECT 
    i.line_number AS invoice_line,
    ph.name AS product_name,
    i.quantity AS invoice_quantity,
    
    -- Vypárované objednávky
    o.document_number AS order_number,
    oi.line_number AS order_line,
    p.paired_quantity
    
FROM supplier_invoice_items i
LEFT JOIN product_catalog_history ph
    ON ph.product_id = i.product_id
    AND ph.modify_id = i.product_modify_id
LEFT JOIN supplier_order_invoices p ON p.invoice_item_id = i.item_id
LEFT JOIN supplier_order_items oi ON oi.item_id = p.order_item_id
LEFT JOIN supplier_order_heads o ON o.document_id = oi.order_head_id
WHERE i.invoice_head_id = $1
ORDER BY i.line_number, o.document_number;
```

### Nevypárované položky faktúr

```sql
SELECT 
    h.document_number,
    h.supplier_invoice_number,
    i.line_number,
    ph.name AS product_name,
    i.quantity,
    COALESCE(SUM(p.paired_quantity), 0) AS paired_quantity,
    i.quantity - COALESCE(SUM(p.paired_quantity), 0) AS remaining_quantity
FROM supplier_invoice_items i
JOIN supplier_invoice_heads h ON h.document_id = i.invoice_head_id
LEFT JOIN product_catalog_history ph
    ON ph.product_id = i.product_id
    AND ph.modify_id = i.product_modify_id
LEFT JOIN supplier_delivery_invoices p ON p.invoice_item_id = i.item_id
GROUP BY h.document_id, h.document_number, h.supplier_invoice_number,
         i.item_id, i.line_number, ph.name, i.quantity
HAVING i.quantity > COALESCE(SUM(p.paired_quantity), 0)
ORDER BY h.document_number, i.line_number;
```

---

## 7. PRÍKLAD DÁT

### Položky faktúry

```sql
INSERT INTO supplier_invoice_items (
    invoice_head_id, line_number,
    product_id, product_modify_id, product_category_id,
    stock_id, unit_of_measure,
    quantity, vat_rate, discount_percent,
    list_value_ac, discount_value_ac,
    purchase_base_value_ac, purchase_total_value_ac,
    sales_base_value_ac, sales_total_value_ac,
    synthetic_account, analytical_account,
    created_by, created_at
) VALUES
-- Položka 1: Notebook
(1, 1,
 1001, 0, 10,
 1, 'ks',
 10, 20.00, 5.00,
 10000.00, 500.00,
 9500.00, 11400.00,
 12000.00, 14400.00,
 '321', '001001',
 'zoltan', '2025-01-15 10:30:00'),

-- Položka 2: Myš
(1, 2,
 1002, 0, 10,
 1, 'ks',
 50, 20.00, 0.00,
 2500.00, 0.00,
 2500.00, 3000.00,
 3000.00, 3600.00,
 '321', '001001',
 'zoltan', '2025-01-15 10:30:00');
```

### Párovanie s dodacím listom

```sql
-- Faktúra položka 1 (10 ks) vypárovaná s DD položkou 1 (10 ks)
INSERT INTO supplier_delivery_invoices (
    delivery_item_id, invoice_item_id,
    paired_quantity, created_by
) VALUES (1, 1, 10, 'zoltan');

-- Faktúra položka 2 (50 ks) vypárovaná s dvoma DD položkami
INSERT INTO supplier_delivery_invoices (
    delivery_item_id, invoice_item_id,
    paired_quantity, created_by
) VALUES 
(2, 2, 30, 'zoltan'),  -- DD položka 2: 30 ks
(3, 2, 20, 'zoltan');  -- DD položka 3: 20 ks
```

### Párovanie s objednávkou

```sql
-- Faktúra položka 1 (10 ks) vypárovaná s objednávkou položkou 1 (100 ks)
INSERT INTO supplier_order_invoices (
    order_item_id, invoice_item_id,
    paired_quantity, created_by
) VALUES (1, 1, 10, 'zoltan');
```

---

## 8. MIGRÁCIA

### Versioning pri migrácii
**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 9.2

**Pred migráciou položiek:**
1. Migruj produkty do `product_catalog_history` s `modify_id = 0`

**Pri migrácii položky:**
```python
def migrate_invoice_item(record, new_invoice_head_id: int):
    """
    Migruj položku faktúry z Btrieve do PostgreSQL.
    """
    insert_invoice_item(
        invoice_head_id=new_invoice_head_id,
        line_number=record.ItmNum,
        
        # Produkt - VERSIONING
        product_id=record.GsCode,
        product_modify_id=0,  # Prvá verzia
        
        product_category_id=record.MgCode,
        facility_id=record.WriNum,
        stock_id=record.StkNum,
        
        # Množstvo a jednotky
        unit_of_measure=record.MsName,
        quantity=record.GsQnt,
        vat_rate=record.VatPrc,
        discount_percent=record.DscPrc,
        
        # Ceny AC
        list_value_ac=record.AcDValue,
        discount_value_ac=record.AcDscVal,
        purchase_base_value_ac=record.AcCValue,
        purchase_total_value_ac=record.AcEValue,
        sales_base_value_ac=record.AcAValue,
        sales_total_value_ac=record.AcBValue,
        
        # Ceny FC
        list_unit_price_fc=record.FgDPrice,
        purchase_unit_price_fc=record.FgCPrice,
        list_value_fc=record.FgDValue,
        discount_value_fc=record.FgDscVal,
        purchase_base_value_fc=record.FgCValue,
        purchase_total_value_fc=record.FgEValue,
        
        # Účtovanie
        synthetic_account=record.AccSnt,
        analytical_account=record.AccAnl,
        
        # Audit
        created_by=record.CrtUser,
        created_at=combine_datetime(record.CrtDate, record.CrtTime),
        updated_by=record.ModUser if record.ModUser else None,
        updated_at=combine_datetime(record.ModDate, record.ModTime) if record.ModDate else None
    )
```

### Migrácia Notice do document_texts

```python
def migrate_invoice_item_notice(record, invoice_head_id: int, item_id: int):
    """
    Migruj Notice do document_texts.
    """
    if record.Notice and record.Notice.strip():
        # Zisti line_number pre text_type='text'
        next_line = get_next_text_line_number(
            document_type='supplier_invoice',
            document_id=invoice_head_id,
            text_type='text'
        )
        
        insert_document_text(
            document_type='supplier_invoice',
            document_id=invoice_head_id,
            text_type='text',
            line_number=next_line,
            text_content=f"Položka {record.ItmNum}: {record.Notice}",
            created_by=record.CrtUser,
            created_at=combine_datetime(record.CrtDate, record.CrtTime)
        )
```

### Migrácia párovacích údajov

**Párovanie s objednávkami:**
```python
def migrate_order_invoice_pairing(record, new_invoice_item_id: int):
    """
    Migruj párovanie s objednávkami.
    """
    if record.OsdNum and record.OsdItm:
        # Nájdi order_item_id v novej databáze
        order_item_id = find_order_item_by_old_number(
            record.OsdNum,
            record.OsdItm
        )
        
        if order_item_id:
            insert_order_invoice_pairing(
                order_item_id=order_item_id,
                invoice_item_id=new_invoice_item_id,
                paired_quantity=record.GsQnt,  # Celé množstvo
                created_by=record.CrtUser
            )
```

**Párovanie s dodacími listami:**
```python
def migrate_delivery_invoice_pairing(record, new_invoice_item_id: int):
    """
    Migruj párovanie s dodacími listami.
    """
    if record.TsdNum and record.TsdItm:
        # Nájdi delivery_item_id v novej databáze
        delivery_item_id = find_delivery_item_by_old_number(
            record.TsdNum,
            record.TsdItm
        )
        
        if delivery_item_id:
            insert_delivery_invoice_pairing(
                delivery_item_id=delivery_item_id,
                invoice_item_id=new_invoice_item_id,
                paired_quantity=record.GsQnt,  # Celé množstvo
                created_by=record.CrtUser
            )
```

### Validácia po migrácii

```sql
-- Kontrola počtu položiek
SELECT 
    h.document_number,
    h.item_count AS head_count,
    COUNT(i.item_id) AS actual_count
FROM supplier_invoice_heads h
LEFT JOIN supplier_invoice_items i ON i.invoice_head_id = h.document_id
GROUP BY h.document_id, h.document_number, h.item_count
HAVING h.item_count != COUNT(i.item_id);

-- Kontrola súm
SELECT 
    h.document_number,
    h.purchase_total_value_ac AS head_total,
    SUM(i.purchase_total_value_ac) AS items_total,
    h.purchase_total_value_ac - SUM(i.purchase_total_value_ac) AS difference
FROM supplier_invoice_heads h
JOIN supplier_invoice_items i ON i.invoice_head_id = h.document_id
GROUP BY h.document_id, h.document_number, h.purchase_total_value_ac
HAVING ABS(h.purchase_total_value_ac - SUM(i.purchase_total_value_ac)) > 0.01;

-- Kontrola párovacích údajov
SELECT 
    COUNT(*) AS total_items,
    COUNT(DISTINCT p.invoice_item_id) AS paired_with_delivery,
    COUNT(DISTINCT po.invoice_item_id) AS paired_with_order
FROM supplier_invoice_items i
LEFT JOIN supplier_delivery_invoices p ON p.invoice_item_id = i.item_id
LEFT JOIN supplier_order_invoices po ON po.invoice_item_id = i.item_id;

-- Kontrola množstiev v párovaní
SELECT 
    i.item_id,
    i.quantity AS item_quantity,
    COALESCE(SUM(p.paired_quantity), 0) AS paired_quantity,
    i.quantity - COALESCE(SUM(p.paired_quantity), 0) AS difference
FROM supplier_invoice_items i
LEFT JOIN supplier_delivery_invoices p ON p.invoice_item_id = i.item_id
GROUP BY i.item_id, i.quantity
HAVING i.quantity < COALESCE(SUM(p.paired_quantity), 0);
```

---

## 9. VERZIA A ZMENY

### Verzia dokumentu
**Verzia:** 1.0  
**Dátum:** 2025-12-13  
**Autor:** Zoltán + Claude  
**Session:** 8

### História zmien

| Verzia | Dátum | Zmeny |
|--------|-------|-------|
| 1.0 | 2025-12-13 | Vytvorenie prvej verzie |

### Závislosti

**Tento dokument vyžaduje:**
- `COMMON_DOCUMENT_PRINCIPLES.md` - všeobecné zásady
- `ISH-supplier_invoice_heads.md` - hlavičky faktúr
- `product_catalog` + `product_catalog_history` - versioning
- `product_categories`, `stocks`, `facilities` - číselníky
- `document_texts` - texty (univerzálna tabuľka)

**Súvisiace dokumenty:**
- `TSI-supplier_delivery_items.md` - položky dodacích listov (párovanie)
- `supplier_order_items.md` - položky objednávok (párovanie)

**M:N tabuľky:**
- `supplier_delivery_invoices` - párovanie s dodacími listami (existuje v TSI!)
- `supplier_order_invoices` - párovanie s objednávkami (NOVÁ!)

### Poznámky

1. **supplier_delivery_invoices** už existuje z TSI Session 7!
2. **supplier_order_invoices** je NOVÁ tabuľka vytvorená v ISI
3. **paired_status** v hlavičke je agregovaný z položiek
4. **Notice** ide do `document_texts`, nie ako pole v položke
5. **Produkt versioning** - product_id + product_modify_id
6. **Účtovanie položiek** - synthetic_account, analytical_account (NOVÉ oproti TSI)

---

**Koniec dokumentu ISI-supplier_invoice_items.md v1.0**