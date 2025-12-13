# TSI.BTR → supplier_delivery_items

**Pre všeobecné zásady pozri:** [COMMON_DOCUMENT_PRINCIPLES.md](../../COMMON_DOCUMENT_PRINCIPLES.md)

Tento dokument popisuje **ŠPECIFICKÉ vlastnosti** položiek dodávateľských dodacích listov.

---

## 1. PREHĽAD

### Účel
Položky dodávateľských dodacích listov (Supplier Delivery Note Items) obsahujú detailné informácie o prijatých produktoch. Každá položka reprezentuje jeden riadok dodávky s množstvom, cenami a stavmi spracovania.

### Btrieve súbory
**Starý systém (NEX Genesis):**
```
TSI25001.BTR  - Položky knihy č. 1, rok 2025
TSI25002.BTR  - Položky knihy č. 2, rok 2025
TSI24001.BTR  - Položky knihy č. 1, rok 2024
```

**Nový systém (NEX Automat):**
```
supplier_delivery_items - jedna tabuľka pre všetky knihy
```

### Vzťahy
```
supplier_delivery_heads (1 hlavička)
    └──< supplier_delivery_items (N položiek)
            ├──< supplier_delivery_invoices (N faktúr - M:N)
            └──< supplier_delivery_orders (N objednávok - M:N)
```

### Kľúčové entity
- **Hlavička:** delivery_head_id (FK na supplier_delivery_heads)
- **Produkt:** product_id + product_modify_id (versioning systém)
- **Dodávateľ:** supplier_id (z hlavičky, pre index)
- **Sklad:** stock_id (kam sa prijíma)
- **Faktúry:** M:N párovanie cez supplier_delivery_invoices
- **Objednávky:** M:N párovanie cez supplier_delivery_orders

---

## 2. SQL SCHÉMA

```sql
-- =====================================================
-- POLOŽKY DODÁVATEĽSKÝCH DODACÍCH LISTOV
-- =====================================================

CREATE TABLE supplier_delivery_items (
    -- Technický primárny kľúč
    item_id BIGSERIAL PRIMARY KEY,
    
    -- ========================================
    -- PREPOJENIE NA HLAVIČKU
    -- ========================================
    
    delivery_head_id BIGINT NOT NULL REFERENCES supplier_delivery_heads(document_id) ON DELETE CASCADE,
    item_number INTEGER NOT NULL,
    
    -- ========================================
    -- PRODUKT (VERSIONING SYSTÉM)
    -- Detaily v COMMON_DOCUMENT_PRINCIPLES.md
    -- ========================================
    
    product_id INTEGER NOT NULL,
    product_modify_id INTEGER NOT NULL,
    
    -- ========================================
    -- SKLAD A MNOŽSTVO
    -- ========================================
    
    stock_id INTEGER NOT NULL,
    quantity DECIMAL(15,3) NOT NULL,
    
    -- ========================================
    -- DPH A ZĽAVY
    -- ========================================
    
    vat_rate DECIMAL(5,2) NOT NULL,
    discount_percent DECIMAL(5,2) DEFAULT 0,
    
    -- ========================================
    -- NSO (ALIQUOTNE Z HLAVIČKY)
    -- ========================================
    
    customs_cost_ac DECIMAL(15,2) DEFAULT 0,
    transport_cost_ac DECIMAL(15,2) DEFAULT 0,
    other_cost_ac DECIMAL(15,2) DEFAULT 0,
    
    -- ========================================
    -- CENY V ÚČTOVNEJ MENE (AC)
    -- Detaily v COMMON_DOCUMENT_PRINCIPLES.md
    -- ========================================
    
    unit_price_ac DECIMAL(15,2),
    list_value_ac DECIMAL(15,2),
    discount_value_ac DECIMAL(15,2) DEFAULT 0,
    rounding_value_ac DECIMAL(15,2) DEFAULT 0,
    purchase_base_value_ac DECIMAL(15,2),
    purchase_total_value_ac DECIMAL(15,2),
    acquisition_value_ac DECIMAL(15,2),
    sales_base_value_ac DECIMAL(15,2),
    sales_total_value_ac DECIMAL(15,2),
    
    -- ========================================
    -- CENY VO VYÚČTOVACEJ MENE (FC)
    -- Detaily v COMMON_DOCUMENT_PRINCIPLES.md
    -- ========================================
    
    unit_list_price_fc DECIMAL(15,2),
    unit_base_price_fc DECIMAL(15,2),
    unit_total_price_fc DECIMAL(15,2),
    list_value_fc DECIMAL(15,2),
    discount_value_fc DECIMAL(15,2) DEFAULT 0,
    rounding_value_fc DECIMAL(15,2) DEFAULT 0,
    purchase_base_value_fc DECIMAL(15,2),
    purchase_total_value_fc DECIMAL(15,2),
    
    -- ========================================
    -- TRVANLIVOSŤ A ŠARŽA (PODMIENENÉ)
    -- ========================================
    
    expiry_date DATE,
    batch_code VARCHAR(30),
    batch_date DATE,
    
    -- ========================================
    -- STAVY POLOŽKY (ŠPECIFICKÉ PRE TSI)
    -- ========================================
    
    stock_status VARCHAR(20) NOT NULL DEFAULT 'recorded',
    financial_status VARCHAR(20) NOT NULL DEFAULT 'unpaired',
    
    -- ========================================
    -- DODÁVATEĽ (Z HLAVIČKY, PRE INDEX)
    -- ========================================
    
    supplier_id INTEGER NOT NULL,
    
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
    
    CONSTRAINT uq_delivery_item_number UNIQUE (delivery_head_id, item_number),
    CONSTRAINT chk_quantity CHECK (quantity > 0),
    CONSTRAINT chk_vat_rate CHECK (vat_rate >= 0 AND vat_rate <= 100),
    CONSTRAINT chk_discount_percent CHECK (discount_percent >= 0 AND discount_percent <= 100),
    CONSTRAINT chk_stock_status CHECK (stock_status IN ('recorded', 'stocked')),
    CONSTRAINT chk_financial_status CHECK (financial_status IN ('unpaired', 'invoiced', 'cash_register'))
);

-- ========================================
-- INDEXY
-- ========================================

CREATE INDEX idx_supplier_delivery_items_head ON supplier_delivery_items(delivery_head_id);
CREATE INDEX idx_supplier_delivery_items_product ON supplier_delivery_items(product_id);
CREATE INDEX idx_supplier_delivery_items_stock ON supplier_delivery_items(stock_id);
CREATE INDEX idx_supplier_delivery_items_supplier ON supplier_delivery_items(supplier_id);
CREATE INDEX idx_supplier_delivery_items_stock_status ON supplier_delivery_items(stock_status);
CREATE INDEX idx_supplier_delivery_items_financial_status ON supplier_delivery_items(financial_status);
CREATE INDEX idx_supplier_delivery_items_expiry ON supplier_delivery_items(expiry_date) WHERE expiry_date IS NOT NULL;
CREATE INDEX idx_supplier_delivery_items_batch ON supplier_delivery_items(batch_code) WHERE batch_code IS NOT NULL;

-- ========================================
-- TRIGGERY
-- Funkcie definované v COMMON_DOCUMENT_PRINCIPLES.md
-- ========================================

CREATE TRIGGER trg_supplier_delivery_items_updated_at
    BEFORE UPDATE ON supplier_delivery_items
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_supplier_delivery_items_count
    AFTER INSERT OR DELETE ON supplier_delivery_items
    FOR EACH ROW
    EXECUTE FUNCTION update_delivery_head_item_count();

-- =====================================================
-- PÁROVANIE S FAKTÚRAMI (M:N) - SPRÁVNE NA ÚROVNI POLOŽIEK!
-- =====================================================

CREATE TABLE supplier_delivery_invoices (
    pairing_id SERIAL PRIMARY KEY,
    delivery_item_id BIGINT NOT NULL REFERENCES supplier_delivery_items(item_id) ON DELETE CASCADE,
    invoice_item_id BIGINT NOT NULL,  -- FK na supplier_invoice_items (neskôr)
    
    paired_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    paired_by VARCHAR(8) NOT NULL,
    note TEXT,
    
    CONSTRAINT uq_delivery_invoice_items UNIQUE (delivery_item_id, invoice_item_id)
);

CREATE INDEX idx_supplier_delivery_invoices_delivery ON supplier_delivery_invoices(delivery_item_id);
CREATE INDEX idx_supplier_delivery_invoices_invoice ON supplier_delivery_invoices(invoice_item_id);

-- =====================================================
-- PÁROVANIE S OBJEDNÁVKAMI (M:N)
-- =====================================================

CREATE TABLE supplier_delivery_orders (
    pairing_id SERIAL PRIMARY KEY,
    delivery_item_id BIGINT NOT NULL REFERENCES supplier_delivery_items(item_id) ON DELETE CASCADE,
    order_item_id BIGINT NOT NULL,  -- FK na supplier_order_items (neskôr)
    
    paired_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    paired_by VARCHAR(8) NOT NULL,
    note TEXT,
    
    CONSTRAINT uq_delivery_order_items UNIQUE (delivery_item_id, order_item_id)
);

CREATE INDEX idx_supplier_delivery_orders_delivery ON supplier_delivery_orders(delivery_item_id);
CREATE INDEX idx_supplier_delivery_orders_order ON supplier_delivery_orders(order_item_id);
```

---

## 3. MAPPING POLÍ

### Prepojenie

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| DocNum | Str12 | delivery_head_id | BIGINT | FK na supplier_delivery_heads |
| ItmNum | word | item_number | INTEGER | Poradové číslo |

### Produkt (Versioning)
**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 2

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| GsCode | longint | product_id | INTEGER | ID produktu |
| - | - | product_modify_id | INTEGER | Verzia (NOVÉ) |
| MgCode, GsName, BarCode... | - | - | - | V product_catalog_history |

### Sklad a množstvo

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| StkNum | word | stock_id | INTEGER |
| GsQnt | double | quantity | DECIMAL(15,3) |

### DPH a zľavy

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| VatPrc | double | vat_rate | DECIMAL(5,2) |
| DscPrc | double | discount_percent | DECIMAL(5,2) |

### NSO (Aliquotne rozdelené)

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| AcZValue | double | customs_cost_ac | DECIMAL(15,2) | Colné náklady |
| AcTValue | double | transport_cost_ac | DECIMAL(15,2) | Doprava |
| AcOValue | double | other_cost_ac | DECIMAL(15,2) | Ostatné |

### Ceny v účtovnej mene (AC)

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| AcSPrice | double | unit_price_ac | DECIMAL(15,2) | NC/MJ s NSO |
| AcDValue | double | list_value_ac | DECIMAL(15,2) | Pred zľavou |
| AcDscVal | double | discount_value_ac | DECIMAL(15,2) | Zľava |
| AcRndVal | double | rounding_value_ac | DECIMAL(15,2) | Zaokrúhlenie |
| AcCValue | double | purchase_base_value_ac | DECIMAL(15,2) | NC bez DPH, bez NSO |
| AcEValue | double | purchase_total_value_ac | DECIMAL(15,2) | NC s DPH, s NSO |
| AcSValue | double | acquisition_value_ac | DECIMAL(15,2) | OC s NSO |
| AcAValue | double | sales_base_value_ac | DECIMAL(15,2) | PC bez DPH |
| AcBValue | double | sales_total_value_ac | DECIMAL(15,2) | PC s DPH |

### Ceny vo vyúčtovacej mene (FC)

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| FgDPrice | double | unit_list_price_fc | DECIMAL(15,2) |
| FgCPrice | double | unit_base_price_fc | DECIMAL(15,2) |
| FgEPrice | double | unit_total_price_fc | DECIMAL(15,2) |
| FgDValue | double | list_value_fc | DECIMAL(15,2) |
| FgDscVal | double | discount_value_fc | DECIMAL(15,2) |
| FgRndVal | double | rounding_value_fc | DECIMAL(15,2) |
| FgCValue | double | purchase_base_value_fc | DECIMAL(15,2) |
| FgEValue | double | purchase_total_value_fc | DECIMAL(15,2) |

### Trvanlivosť a šarža

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| DrbDate | DateType | expiry_date | DATE | NULL ak nevyžaduje |
| RbaCode | Str30 | batch_code | VARCHAR(30) | NULL ak nevyžaduje |
| RbaDate | DateType | batch_date | DATE | NULL ak nevyžaduje |

### Stavy položky

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| StkStat | Str1 | stock_status | VARCHAR(20) | N→recorded, S→stocked |
| FinStat | Str1 | financial_status | VARCHAR(20) | ''→unpaired, F→invoiced, C→cash_register |

### Dodávateľ

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| PaCode | longint | supplier_id | INTEGER | Z hlavičky (pre index) |

### Audit
**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 7

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| CrtUser | Str8 | created_by | VARCHAR(8) | - |
| CrtDate + CrtTime | Date + Time | created_at | TIMESTAMP | Zlúčené |
| ModUser | Str8 | updated_by | VARCHAR(8) | - |
| ModDate + ModTime | Date + Time | updated_at | TIMESTAMP | Zlúčené |

### Párovanie s faktúrou (M:N tabuľka)

| Btrieve | PostgreSQL |
|---------|------------|
| IsdNum, IsdItm, IsdDate | supplier_delivery_invoices |

### Párovanie s objednávkou (M:N tabuľka)

| Btrieve | PostgreSQL |
|---------|------------|
| OsdNum, OsdItm | supplier_delivery_orders |

### NEPRENESENÉ POLIA
**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 9.3

Pracovné polia, staré odkazy, zastarané funkcie.

---

## 4. BIZNIS LOGIKA (ŠPECIFICKÉ PRE TSI)

### Aliquotné rozdelenie NSO

**KĽÚČOVÁ FUNKCIA:** NSO náklady sa zadávajú v **hlavičke**, automaticky sa rozdeľujú na **položky**.

**Pri zmene NSO v hlavičke → prepočítať všetky položky:**
```python
def recalculate_nso_costs(delivery_head_id):
    """
    Prepočítaj NSO náklady z hlavičky na položky aliquotne.
    """
    head = get_delivery_head(delivery_head_id)
    items = get_delivery_items(delivery_head_id)
    
    # Celková hodnota položiek (základ pre prepočet)
    total_value = sum(item.purchase_base_value_ac for item in items)
    
    if total_value == 0:
        return
    
    # Prepočítaj každú položku
    for item in items:
        ratio = item.purchase_base_value_ac / total_value
        
        item.customs_cost_ac = head.customs_cost_ac * ratio
        item.transport_cost_ac = head.transport_cost_ac * ratio
        item.other_cost_ac = head.other_cost_ac * ratio
        
        # Obstarávacia cena = NC + NSO
        item.acquisition_value_ac = (
            item.purchase_base_value_ac +
            item.customs_cost_ac +
            item.transport_cost_ac +
            item.other_cost_ac
        )
        
        update_item(item)
```

**Vzorec:**
```
ratio = položka.NC / celková_NC_všetkých_položiek

položka.colné = hlavička.colné × ratio
položka.doprava = hlavička.doprava × ratio
položka.ostatné = hlavička.ostatné × ratio

položka.OC = položka.NC + položka.colné + položka.doprava + položka.ostatné
```

---

### Výpočet hodnôt položky

```python
def calculate_item_values(item):
    """
    Vypočítaj všetky hodnoty položky.
    """
    # Základná hodnota pred zľavou
    item.list_value_ac = item.unit_list_price_ac * item.quantity
    
    # Zľava
    item.discount_value_ac = item.list_value_ac * (item.discount_percent / 100)
    
    # Hodnota bez DPH (bez NSO)
    item.purchase_base_value_ac = item.list_value_ac - item.discount_value_ac
    
    # DPH
    vat_amount = item.purchase_base_value_ac * (item.vat_rate / 100)
    
    # Hodnota s DPH (s NSO)
    item.purchase_total_value_ac = (
        item.purchase_base_value_ac + 
        vat_amount +
        item.customs_cost_ac +
        item.transport_cost_ac +
        item.other_cost_ac
    )
    
    # Obstarávacia cena s NSO
    item.acquisition_value_ac = (
        item.purchase_base_value_ac +
        item.customs_cost_ac +
        item.transport_cost_ac +
        item.other_cost_ac
    )
    
    # Jednotková cena s NSO
    item.unit_price_ac = item.acquisition_value_ac / item.quantity
```

---

### Stavy položky - Lifecycle

```
┌──────────┐   Naskladniť   ┌─────────┐
│ RECORDED │  ───────────>  │ STOCKED │
│  (N)     │                │  (S)    │
└──────────┘                └─────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
            ┌──────────────┐         ┌───────────────┐
            │   INVOICED   │         │ CASH_REGISTER │
            │     (F)      │         │      (C)      │
            └──────────────┘         └───────────────┘

stock_status: recorded → stocked
financial_status: unpaired → invoiced/cash_register
```

**Pravidlá:**
1. **Nová položka:** stock_status='recorded', financial_status='unpaired'
2. **Naskladnenie:** stock_status='stocked' (vytvorí STM záznamy)
3. **Faktúra:** financial_status='invoiced' (vytvorí supplier_delivery_invoices)
4. **Pokladnica:** financial_status='cash_register'

---

### Trvanlivosť a šarža (Podmienené!)

**Kľúčový koncept:** Sleduje sa **LEN** pre produkty s `product_catalog.track_expiry = true`

**Validácia pri uložení:**
```python
def validate_item(item):
    # Získaj produkt z history
    product = get_product_history(item.product_id, item.product_modify_id)
    
    # Ak produkt vyžaduje sledovanie
    if product.track_expiry:
        # expiry_date, batch_code, batch_date môžu byť vyplnené
        pass
    else:
        # Musia byť NULL
        if item.expiry_date or item.batch_code or item.batch_date:
            raise ValidationError("Produkt nevyžaduje sledovanie expirácie")
```

**Pravidlá:**
- `track_expiry = true` → polia môžu byť vyplnené
- `track_expiry = false` → polia MUSIA byť NULL
- Ak je `batch_code` vyplnený → `batch_date` musí byť tiež vyplnený

---

### Párovanie s faktúrou (M:N na úrovni POLOŽIEK!)

**KRITICKÉ:** Párovanie je na úrovni **POLOŽIEK**, nie hlavičiek!

**Pri vytvorení faktúry:**
```python
def pair_with_invoice(delivery_item_id, invoice_item_id, user):
    # Vytvor párovanie
    insert_delivery_invoice_pairing(
        delivery_item_id=delivery_item_id,
        invoice_item_id=invoice_item_id,
        paired_by=user
    )
    
    # Aktualizuj stav položky
    update_item_financial_status(delivery_item_id, 'invoiced')
    
    # Aktualizuj stav hlavičky (ak všetky položky vyfakturované)
    check_and_update_head_paired_status(delivery_head_id)
```

**Agregácia stavu hlavičky:**
```python
def check_and_update_head_paired_status(delivery_head_id):
    """
    Aktualizuj paired_status hlavičky na základe položiek.
    """
    items = get_delivery_items(delivery_head_id)
    
    invoiced_count = sum(1 for i in items if i.financial_status == 'invoiced')
    total_count = len(items)
    
    if invoiced_count == 0:
        head_status = 'N'  # Not paired
    elif invoiced_count == total_count:
        head_status = 'Q'  # Queued/Paired
    else:
        head_status = 'P'  # Partially paired
    
    update_head_paired_status(delivery_head_id, head_status)
```

---

### Párovanie s objednávkou

**Pri vytvorení dodacieho listu z objednávky:**
```python
def create_delivery_from_order(order_id):
    order_items = get_order_items(order_id)
    
    delivery = create_delivery_head(...)
    
    for order_item in order_items:
        # Vytvor položku dodacieho listu
        delivery_item = create_delivery_item(
            delivery_head_id=delivery.document_id,
            product_id=order_item.product_id,
            quantity=order_item.quantity,
            ...
        )
        
        # Spáruj s objednávkou
        insert_delivery_order_pairing(
            delivery_item_id=delivery_item.item_id,
            order_item_id=order_item.item_id
        )
```

---

## 5. VZŤAHY S INÝMI TABUĽKAMI

### Master-Detail vzťah

```sql
-- Hlavička → Položky (1:N) - CASCADE
supplier_delivery_heads (1) ──< (N) supplier_delivery_items
    ON DELETE CASCADE
```

### M:N vzťahy (SPRÁVNE NA ÚROVNI POLOŽIEK!)

```sql
-- Položky → Faktúry (M:N)
supplier_delivery_items (M) ──< supplier_delivery_invoices >── (N) supplier_invoice_items

-- Položky → Objednávky (M:N)
supplier_delivery_items (M) ──< supplier_delivery_orders >── (N) supplier_order_items
```

### Reference na katalógy (Versioning)
**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 2

```sql
-- Produkt + Verzia
product_id + product_modify_id → product_catalog_history

-- Ostatné katalógy
stock_id → stocks (RESTRICT)
supplier_id → partners (z hlavičky, pre index)
```

### Reference na skladové systémy

```sql
-- Skladové pohyby (vytvorené pri naskladnení)
item_id → stock_card_movements.source_item_id

-- FIFO karty (vytvorené pri naskladnení)
item_id → stock_card_fifos.source_item_id
```

---

## 6. QUERY PATTERNS

### Položky dodacieho listu s produktami

```sql
SELECT 
    i.item_number,
    ph.code AS product_code,
    ph.name AS product_name,
    ph.ean AS product_ean,
    i.quantity,
    i.unit_price_ac,
    i.purchase_total_value_ac,
    i.stock_status,
    i.financial_status,
    i.expiry_date,
    i.batch_code
FROM supplier_delivery_items i
LEFT JOIN product_catalog_history ph
    ON ph.product_id = i.product_id
    AND ph.modify_id = i.product_modify_id
WHERE i.delivery_head_id = $1
ORDER BY i.item_number;
```

### Položky s párovanimi

```sql
SELECT 
    i.item_number,
    ph.name AS product_name,
    i.quantity,
    
    -- Faktúry
    ARRAY_AGG(DISTINCT di.invoice_item_id) AS invoice_items,
    
    -- Objednávky
    ARRAY_AGG(DISTINCT do.order_item_id) AS order_items
    
FROM supplier_delivery_items i
LEFT JOIN product_catalog_history ph
    ON ph.product_id = i.product_id
    AND ph.modify_id = i.product_modify_id
LEFT JOIN supplier_delivery_invoices di ON di.delivery_item_id = i.item_id
LEFT JOIN supplier_delivery_orders do ON do.delivery_item_id = i.item_id
WHERE i.delivery_head_id = $1
GROUP BY i.item_id, i.item_number, ph.name, i.quantity
ORDER BY i.item_number;
```

### Nevypárované položky

```sql
SELECT 
    d.document_number,
    i.item_number,
    ph.name AS product_name,
    i.quantity,
    i.purchase_total_value_ac
FROM supplier_delivery_items i
JOIN supplier_delivery_heads d ON d.document_id = i.delivery_head_id
LEFT JOIN product_catalog_history ph
    ON ph.product_id = i.product_id
    AND ph.modify_id = i.product_modify_id
WHERE i.stock_status = 'stocked'
  AND i.financial_status = 'unpaired'
ORDER BY d.document_date, i.item_number;
```

### Položky s expirujúcou trvanlivosťou

```sql
SELECT 
    d.document_number,
    ph.name AS product_name,
    i.batch_code,
    i.expiry_date,
    i.expiry_date - CURRENT_DATE AS days_to_expiry
FROM supplier_delivery_items i
JOIN supplier_delivery_heads d ON d.document_id = i.delivery_head_id
LEFT JOIN product_catalog_history ph
    ON ph.product_id = i.product_id
    AND ph.modify_id = i.product_modify_id
WHERE i.expiry_date IS NOT NULL
  AND i.expiry_date <= CURRENT_DATE + INTERVAL '30 days'
  AND i.stock_status = 'stocked'
ORDER BY i.expiry_date;
```

### NSO náklady - kontrola rozdelenia

```sql
-- Kontrola, či súčet NSO položiek = NSO hlavičky
SELECT 
    d.document_number,
    d.customs_cost_ac AS head_customs,
    SUM(i.customs_cost_ac) AS items_customs,
    ABS(d.customs_cost_ac - SUM(i.customs_cost_ac)) AS customs_diff
FROM supplier_delivery_heads d
JOIN supplier_delivery_items i ON i.delivery_head_id = d.document_id
GROUP BY d.document_id, d.document_number, d.customs_cost_ac
HAVING ABS(d.customs_cost_ac - SUM(i.customs_cost_ac)) > 0.01;
```

---

## 7. PRÍKLAD DÁT

### Vytvorenie položky

```sql
INSERT INTO supplier_delivery_items (
    delivery_head_id, item_number,
    product_id, product_modify_id,
    stock_id, quantity,
    vat_rate, discount_percent,
    customs_cost_ac, transport_cost_ac, other_cost_ac,
    unit_price_ac,
    purchase_base_value_ac, purchase_total_value_ac,
    acquisition_value_ac,
    stock_status, financial_status,
    supplier_id,
    created_by, created_at
) VALUES (
    1, 1,
    789, 0,
    1, 10.000,
    20.00, 5.00,
    6.00, 3.00, 1.80,
    10.88,
    95.00, 124.80,
    108.80,
    'recorded', 'unpaired',
    456,
    'zoltan', '2025-01-15 10:35:00'
);
```

### Položka s trvanlivosťou a šaržou

```sql
INSERT INTO supplier_delivery_items (
    delivery_head_id, item_number,
    product_id, product_modify_id,
    stock_id, quantity, vat_rate,
    purchase_base_value_ac, purchase_total_value_ac,
    expiry_date, batch_code, batch_date,
    stock_status, financial_status,
    supplier_id, created_by, created_at
) VALUES (
    1, 2,
    890, 0,
    1, 50.000, 10.00,
    200.00, 220.00,
    '2026-06-30', 'BATCH-2025-001', '2025-01-10',
    'recorded', 'unpaired',
    456, 'zoltan', '2025-01-15 10:40:00'
);
```

### Párovanie s faktúrou

```sql
-- Vytvor párovanie
INSERT INTO supplier_delivery_invoices (
    delivery_item_id, invoice_item_id, paired_by
) VALUES (1, 555, 'zoltan');

-- Aktualizuj stav
UPDATE supplier_delivery_items
SET financial_status = 'invoiced',
    updated_by = 'zoltan',
    updated_at = '2025-01-16 09:00:00'
WHERE item_id = 1;
```

---

## 8. MIGRÁCIA

### Versioning pri migrácii
**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 9.2

**Pred migráciou dokladov:**
1. Migruj produkty do `product_catalog_history` s `modify_id = 0`

**Pri migrácii položky:**
```python
insert_delivery_item(
    product_id=record.GsCode,
    product_modify_id=0,  # Prvá verzia
    ...
)
```

### Párovanie s faktúrou

```python
def migrate_invoice_pairing(record, item_id):
    if record.IsdNum and record.IsdItm:
        invoice_item = find_invoice_item(record.IsdNum, record.IsdItm)
        
        if invoice_item:
            insert_delivery_invoice_pairing(
                delivery_item_id=item_id,
                invoice_item_id=invoice_item.item_id,
                paired_by='MIGRATION'
            )
            
            update_item_financial_status(item_id, 'invoiced')
```

### Stavy položky

```python
def get_stock_status(record):
    return 'stocked' if record.StkStat == 'S' else 'recorded'

def get_financial_status(record):
    if record.FinStat == 'F':
        return 'invoiced'
    elif record.FinStat == 'C':
        return 'cash_register'
    else:
        return 'unpaired'
```

### Validácia po migrácii

```sql
-- Kontrola počtu položiek
SELECT d.document_number, d.item_count, COUNT(i.item_id)
FROM supplier_delivery_heads d
LEFT JOIN supplier_delivery_items i ON i.delivery_head_id = d.document_id
GROUP BY d.document_id, d.document_number, d.item_count
HAVING d.item_count != COUNT(i.item_id);

-- Kontrola NSO rozdelenia
SELECT d.document_number,
    ABS(d.customs_cost_ac - SUM(i.customs_cost_ac)) AS customs_diff
FROM supplier_delivery_heads d
JOIN supplier_delivery_items i ON i.delivery_head_id = d.document_id
GROUP BY d.document_id, d.document_number, d.customs_cost_ac
HAVING ABS(d.customs_cost_ac - SUM(i.customs_cost_ac)) > 0.01;
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
| 2.0 | 2025-12-13 | Optimalizácia: odstránené duplicity z COMMON, aktualizácia na document_texts |
| 1.0 | 2025-12-12 | Vytvorenie prvej verzie |

### Závislosti

**Tento dokument vyžaduje:**
- `COMMON_DOCUMENT_PRINCIPLES.md` - všeobecné zásady
- `supplier_delivery_heads` - hlavičky
- `product_catalog` + `product_catalog_history` - versioning
- `stocks`, `partners` - číselníky

**Súvisiace dokumenty:**
- `TSH-supplier_delivery_heads.md` - hlavičky
- `document_texts` - texty (univerzálna tabuľka)
- `TSP-supplier_delivery_payments.md` - platby
- `supplier_invoice_items.md` - párovanie s faktúrami
- `supplier_order_items.md` - párovanie s objednávkami

### Kľúčové inovácie

1. **Versioning systém produktov** - `product_modify_id` namiesto kopírovania
2. **M:N párovanie** - `supplier_delivery_invoices` a `supplier_delivery_orders` **NA ÚROVNI POLOŽIEK**
3. **Aliquotné rozdelenie NSO** - náklady v hlavičke → automaticky na položky
4. **Podmienená trvanlivosť** - len pre `product_catalog.track_expiry = true`
5. **Dva nezávislé stavy** - `stock_status` + `financial_status`

### Poznámky

- **supplier_delivery_invoices je SPRÁVNE v TSI** (M:N medzi položkami!)
- **paired_status hlavičky** je agregovaný z položiek
- **NSO náklady** sa zadávajú v hlavičke, prepočítavajú na položky
- **Trvanlivosť a šarža** sú podmienené podľa produktu

---

**Koniec dokumentu TSI-supplier_delivery_items.md v2.0**