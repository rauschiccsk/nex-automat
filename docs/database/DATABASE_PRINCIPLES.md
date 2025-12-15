# Database Design Principles

**Category:** Database  
**Status:** 🟢 Complete  
**Created:** 2024-12-12  
**Updated:** 2025-12-15  
**Source:** COMMON_DOCUMENT_PRINCIPLES.md

---

## Overview

Common database design principles for NEX Automat:
- Versioning system for catalogs
- Universal document texts table
- Audit fields and triggers
- Naming conventions
- Migration rules
- Validation rules

---

## 2. VERSIONING SYSTÉM

### 2.1 Koncept

**Problém:** Ak sa zmení partner alebo produkt (názov, adresa, cena...), staré doklady by mali zachovať **pôvodné údaje**.

**Staré riešenie (NEX Genesis):** Snapshot - skopírovať všetky údaje do dokladu
```
Hlavička dodacieho listu:
  PaCode = 123
  PaName = "ABC s.r.o."      ← KÓPIA
  RegAddr = "Hlavná 123"     ← KÓPIA
  RegIno = "12345678"        ← KÓPIA
  ... (20+ polí)
```
**Problém:** Mŕňanie priestoru - tisíce dokladov = tisíce kópií rovnakých údajov.

**Nové riešenie (NEX Automat):** Versioning - referencovať správnu verziu
```
Hlavička dodacieho listu:
  supplier_id = 123
  supplier_modify_id = 0     ← Verzia partnera
  
Údaje sa získajú z:
  partner_catalog_history WHERE partner_id=123 AND modify_id=0
```

---

### 2.2 Architektúra

#### Aktuálny katalóg (len ID + verzia)
```sql
partner_catalog (
    partner_id INTEGER PRIMARY KEY,
    modify_id INTEGER DEFAULT 0,        -- Aktuálna verzia
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
```

#### História verzií (všetky údaje)
```sql
partner_catalog_history (
    history_id SERIAL PRIMARY KEY,
    partner_id INTEGER NOT NULL,
    modify_id INTEGER NOT NULL,         -- Verzia
    
    -- VŠETKY polia partnera
    name VARCHAR(100),
    reg_name VARCHAR(100),
    ino VARCHAR(15),
    tin VARCHAR(15),
    vin VARCHAR(15),
    street VARCHAR(100),
    city VARCHAR(100),
    zip VARCHAR(20),
    country_code VARCHAR(2),
    is_supplier BOOLEAN,
    is_customer BOOLEAN,
    ...
    
    valid_from TIMESTAMP NOT NULL,
    valid_to TIMESTAMP,                  -- NULL = aktuálna verzia
    
    CONSTRAINT uq_partner_modify UNIQUE (partner_id, modify_id)
)
```

---

### 2.3 Používanie versioning systému

#### Pri vytvorení dokladu
```python
def create_delivery_note(supplier_id: int, ...):
    # 1. Získaj aktuálnu verziu partnera
    partner = get_current_partner(supplier_id)
    # partner.modify_id = aktuálna verzia (napr. 5)
    
    # 2. Ulož do dokladu
    delivery = insert_delivery_head(
        supplier_id=supplier_id,
        supplier_modify_id=partner.modify_id,  # Zachytí verziu!
        ...
    )
    
    return delivery

def get_current_partner(partner_id: int):
    """Získaj aktuálnu verziu partnera."""
    return db.query("""
        SELECT *
        FROM partner_catalog_history
        WHERE partner_id = %s
          AND valid_to IS NULL
    """, [partner_id]).first()
```

#### Pri zobrazení dokladu
```sql
-- Zobraz doklad so správnou verziou partnera
SELECT 
    d.document_number,
    d.document_date,
    
    -- Partner z history (správna verzia!)
    ph.name AS supplier_name,
    ph.reg_name AS supplier_reg_name,
    ph.ino AS supplier_ino,
    ph.tin AS supplier_tin,
    ph.street AS supplier_street,
    ph.city AS supplier_city,
    ph.zip AS supplier_zip
    
FROM supplier_delivery_heads d
LEFT JOIN partner_catalog_history ph
    ON ph.partner_id = d.supplier_id
    AND ph.modify_id = d.supplier_modify_id  -- KĽÚČOVÉ!
WHERE d.document_id = $1;
```

---

### 2.4 Zmena partnera (nová verzia)

```python
def update_partner(partner_id: int, new_data: dict):
    # 1. Získaj aktuálnu verziu
    current = get_current_partner(partner_id)
    
    # 2. Uzavri aktuálnu verziu
    db.execute("""
        UPDATE partner_catalog_history
        SET valid_to = CURRENT_TIMESTAMP
        WHERE partner_id = %s
          AND modify_id = %s
    """, [partner_id, current.modify_id])
    
    # 3. Vytvor novú verziu
    new_modify_id = current.modify_id + 1
    
    db.insert("""
        INSERT INTO partner_catalog_history (
            partner_id, modify_id,
            name, street, city, ...,
            valid_from
        ) VALUES (
            %s, %s,
            %s, %s, %s, ...,
            CURRENT_TIMESTAMP
        )
    """, [partner_id, new_modify_id, new_data.name, ...])
    
    # 4. Aktualizuj katalóg
    db.execute("""
        UPDATE partner_catalog
        SET modify_id = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE partner_id = %s
    """, [new_modify_id, partner_id])
```

---

### 2.5 Príklad - História partnera

```sql
-- Partner 123 má 3 verzie
SELECT * FROM partner_catalog_history WHERE partner_id = 123;

history_id | partner_id | modify_id | name        | street      | valid_from          | valid_to
-----------|------------|-----------|-------------|-------------|---------------------|---------------------
1          | 123        | 0         | ABC s.r.o.  | Hlavná 123  | 2024-01-01 10:00:00 | 2024-06-15 14:00:00
2          | 123        | 1         | ABC s.r.o.  | Nová 456    | 2024-06-15 14:00:00 | 2024-12-01 09:00:00
3          | 123        | 2         | ABC Group   | Nová 456    | 2024-12-01 09:00:00 | NULL

-- Doklad vytvorený 2024-03-15 má supplier_modify_id = 0
SELECT ph.street 
FROM partner_catalog_history ph
WHERE ph.partner_id = 123 AND ph.modify_id = 0;
-- Výsledok: "Hlavná 123" ✓ (správna adresa v čase vytvorenia)

-- Doklad vytvorený 2024-11-20 má supplier_modify_id = 1
SELECT ph.street 
FROM partner_catalog_history ph
WHERE ph.partner_id = 123 AND ph.modify_id = 1;
-- Výsledok: "Nová 456" ✓ (správna adresa v čase vytvorenia)
```

---

### 2.6 Versioning pre rôzne entity

**Rovnaký princíp pre:**

#### Partneri
```sql
partner_catalog + partner_catalog_history
supplier_id + supplier_modify_id
```

#### Prevádzky partnerov
```sql
partner_facilities + partner_facilities_history
supplier_facility_id + supplier_facility_modify_id
```

#### Produkty
```sql
product_catalog + product_catalog_history
product_id + product_modify_id
```

---

---

## 6. DOCUMENT TEXTS (UNIVERSAL)

### 6.1 Koncept

**Namiesto** samostatných tabuliek pre každý typ dokladu:
```
supplier_delivery_texts
supplier_invoice_texts
customer_delivery_texts
customer_invoice_texts
... (22 identických tabuliek!)
```

**Používame jednu univerzálnu tabuľku:**
```
document_texts
```

Táto tabuľka obsahuje textové riadky pre **všetky typy dokladov**.

---

### 6.2 SQL štruktúra

```sql
CREATE TABLE document_texts (
    text_id BIGSERIAL PRIMARY KEY,
    
    -- Identifikácia dokladu
    document_type VARCHAR(20) NOT NULL,     -- 'supplier_delivery', 'supplier_invoice'...
    document_id BIGINT NOT NULL,            -- ID hlavičky dokladu
    
    -- Typ textu a poradie
    text_type VARCHAR(20) NOT NULL,         -- 'text', 'attachment'
    line_number INTEGER NOT NULL,           -- Číslo riadku (nezávislé per text_type)
    
    -- Obsah
    text_content TEXT,                      -- Textový obsah
    
    -- Audit
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(8) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(8),
    
    -- Indexy a obmedzenia
    CONSTRAINT uq_document_text_line UNIQUE (document_type, document_id, text_type, line_number),
    
    CHECK (text_type IN ('text', 'attachment')),
    CHECK (line_number > 0),
    CHECK (document_type IN (
        'supplier_delivery', 'supplier_invoice', 'supplier_order',
        'customer_delivery', 'customer_invoice', 'customer_order', 'customer_quote',
        'internal_accounting', 'bank_statement', 'payment_order', 'cash_withdrawal', 'cash_receipt',
        'stock_issue', 'stock_receipt', 'stock_transfer', 'stock_repackaging', 
        'stock_assembly', 'cash_register_stock_issue', 'stock_inventory',
        'production',
        'asset_management'
    ))
);

-- Indexy
CREATE INDEX idx_document_texts_document 
    ON document_texts(document_type, document_id);

CREATE INDEX idx_document_texts_type 
    ON document_texts(document_type, document_id, text_type);

-- Trigger pre updated_at
CREATE TRIGGER trg_document_texts_updated_at
    BEFORE UPDATE ON document_texts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

### 6.3 Číslovanie line_number

**line_number je NEZÁVISLÉ pre každý text_type:**

```sql
-- Dodací list DD2500000123
document_type='supplier_delivery', document_id=1, text_type='text', line_number=1
document_type='supplier_delivery', document_id=1, text_type='text', line_number=2
document_type='supplier_delivery', document_id=1, text_type='text', line_number=3

document_type='supplier_delivery', document_id=1, text_type='attachment', line_number=1
document_type='supplier_delivery', document_id=1, text_type='attachment', line_number=2
```

**Každý text_type má svoje vlastné číslovanie od 1.**

---

### 6.4 Príklad použitia

#### Vloženie textu
```python
def add_document_text(
    document_type: str,
    document_id: int,
    text_type: str,
    text_content: str,
    created_by: str
):
    """Pridaj textový riadok k dokladu."""
    
    # Získaj ďalšie line_number pre daný text_type
    next_line = db.query("""
        SELECT COALESCE(MAX(line_number), 0) + 1
        FROM document_texts
        WHERE document_type = %s
          AND document_id = %s
          AND text_type = %s
    """, [document_type, document_id, text_type]).scalar()
    
    # Vlož nový riadok
    db.execute("""
        INSERT INTO document_texts (
            document_type, document_id,
            text_type, line_number,
            text_content, created_by
        ) VALUES (
            %s, %s, %s, %s, %s, %s
        )
    """, [
        document_type, document_id,
        text_type, next_line,
        text_content, created_by
    ])

# Príklad
add_document_text(
    document_type='supplier_delivery',
    document_id=123,
    text_type='text',
    text_content='Továr doručiť na hlavnú prevadzku',
    created_by='ZOLTAN'
)
```

#### Načítanie textov
```sql
-- Všetky texty dokladu
SELECT 
    text_type,
    line_number,
    text_content
FROM document_texts
WHERE document_type = 'supplier_delivery'
  AND document_id = 123
ORDER BY text_type, line_number;

-- Len hlavná časť
SELECT text_content
FROM document_texts
WHERE document_type = 'supplier_delivery'
  AND document_id = 123
  AND text_type = 'text'
ORDER BY line_number;

-- Len prílohy
SELECT text_content
FROM document_texts
WHERE document_type = 'supplier_delivery'
  AND document_id = 123
  AND text_type = 'attachment'
ORDER BY line_number;
```

---

### 6.5 Migrácia z Btrieve

#### Starý systém (NEX Genesis)
```
TSN25001.BTR  -- Texty pre knihu 1, rok 2025
  DocNum = DD2500100123
  LineNum = 1, 2, 3...
  TextType = 'T' (text) alebo 'A' (attachment)
  Text = "Obsah riadku"
```

#### Migračný kód
```python
def migrate_document_text(btrieve_record, new_document_id: int):
    """
    Migruj text z Btrieve do PostgreSQL.
    
    Args:
        btrieve_record: Záznam z TSN.BTR
        new_document_id: Nové ID dokladu v PostgreSQL
    """
    # Mapovanie typu
    text_type_map = {
        'T': 'text',
        'A': 'attachment'
    }
    
    # Extrakcia typu dokladu z DocNum
    doc_type_code = btrieve_record.DocNum[0:2]  # 'DD'
    doc_type_map = {
        'DD': 'supplier_delivery',
        'DF': 'supplier_invoice',
        'OD': 'customer_delivery',
        'OF': 'customer_invoice',
        # ... všetky typy
    }
    
    insert_document_text(
        document_type=doc_type_map[doc_type_code],
        document_id=new_document_id,
        text_type=text_type_map[btrieve_record.TextType],
        line_number=btrieve_record.LineNum,
        text_content=btrieve_record.Text,
        created_by=btrieve_record.CrtUser,
        created_at=combine_datetime(
            btrieve_record.CrtDate,
            btrieve_record.CrtTime
        )
    )
```

---

### 6.6 Výhody univerzálnej tabuľky

**1. Jednoduchosť**
- Jedna tabuľka namiesto 22 identických
- Jeden kód pre všetky typy dokladov
- Jednoduché údržba a rozširovanie

**2. Flexibilita**
- Ľahko pridať nový typ dokladu
- Ľahko pridať nový typ textu
- Jednotné API pre všetky doklady

**3. Konzistencia**
- Rovnaká štruktúra pre všetky doklady
- Rovnaké číslovanie
- Rovnaké validácie

**4. Výkon**
- Jeden index namiesto 22
- Efektívnejšie dotazy
- Centralizovaná správa

---

---

## 7. AUDIT A TRIGGERY

### 7.1 Audit polia

**Každá hlavná tabuľka musí mať:**

```sql
created_by VARCHAR(8) NOT NULL,      -- Kto vytvoril
created_at TIMESTAMP NOT NULL,       -- Kedy vytvoril
updated_by VARCHAR(8),               -- Kto naposledy zmenil
updated_at TIMESTAMP                 -- Kedy naposledy zmenil
```

---

### 7.2 Zlúčené Date + Time polia

**Btrieve:**
```
CrtDate DateType  ;Datum vytvorenia
CrtTime TimeType  ;Cas vytvorenia
ModDate DateType  ;Datum zmeny
ModTime TimeType  ;Cas zmeny
```

**PostgreSQL:**
```sql
created_at TIMESTAMP NOT NULL  -- CrtDate + CrtTime
updated_at TIMESTAMP           -- ModDate + ModTime
```

**Migračný kód:**
```python
def combine_datetime(date_val, time_val):
    """
    Zlúč Btrieve Date a Time na PostgreSQL TIMESTAMP.
    """
    if not date_val:
        return None
    
    # Predpokladáme date_val = datetime.date, time_val = datetime.time
    if time_val:
        return datetime.combine(date_val, time_val)
    else:
        return datetime.combine(date_val, datetime.min.time())

# Použitie
created_at = combine_datetime(record.CrtDate, record.CrtTime)
updated_at = combine_datetime(record.ModDate, record.ModTime)
```

---

### 7.3 Automatický updated_at trigger

**Funkcia:**
```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

**Trigger (rovnaký pre všetky tabuľky):**
```sql
CREATE TRIGGER trg_{table}_updated_at
    BEFORE UPDATE ON {table}
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

**Príklad:**
```sql
CREATE TRIGGER trg_supplier_delivery_heads_updated_at
    BEFORE UPDATE ON supplier_delivery_heads
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

### 7.4 Denormalizované počítadlá

**V hlavičke dokladu:**
```sql
item_count INTEGER DEFAULT 0  -- Počet položiek (trigger)
```

**Trigger funkcia:**
```sql
CREATE OR REPLACE FUNCTION update_delivery_head_item_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE supplier_delivery_heads
        SET item_count = item_count + 1
        WHERE document_id = NEW.delivery_head_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE supplier_delivery_heads
        SET item_count = item_count - 1
        WHERE document_id = OLD.delivery_head_id;
    END IF;
    
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_supplier_delivery_items_count
    AFTER INSERT OR DELETE ON supplier_delivery_items
    FOR EACH ROW
    EXECUTE FUNCTION update_delivery_head_item_count();
```

---

---

## 8. NAMING CONVENTIONS

### 8.1 Tabuľky

**Pattern:**
```
{supplier|customer}_{document_type}_{entity}
```

**Príklady:**
```sql
supplier_delivery_heads      -- Hlavičky dodávateľských dodacích listov
supplier_delivery_items      -- Položky dodávateľských dodacích listov
supplier_invoice_heads       -- Hlavičky dodávateľských faktúr
customer_delivery_heads      -- Hlavičky odberateľských dodacích listov
```

**Univerzálne tabuľky:**
```sql
document_texts               -- Texty pre VŠETKY typy dokladov
```

---

### 8.2 Primárne kľúče

**Pattern:**
```sql
{entity}_id BIGSERIAL PRIMARY KEY
```

**Príklady:**
```sql
document_id BIGSERIAL PRIMARY KEY
item_id BIGSERIAL PRIMARY KEY
partner_id INTEGER PRIMARY KEY
product_id INTEGER PRIMARY KEY
```

**Výnimka:** Ak existuje natural key z Btrieve
```sql
document_id INTEGER PRIMARY KEY  -- Z Btrieve DocNum
```

---

### 8.3 Foreign Keys

**Pattern:**
```sql
{referenced_table}_id
```

**Príklady:**
```sql
delivery_head_id BIGINT REFERENCES supplier_delivery_heads(document_id)
supplier_id INTEGER REFERENCES partners(partner_id)
product_id INTEGER REFERENCES products(product_id)
stock_id INTEGER REFERENCES stocks(stock_id)
```

---

### 8.4 Polia s menou

**Pattern:**
```sql
{field}_ac   -- Účtovná mena (Accounting Currency)
{field}_fc   -- Vyúčtovacia mena (Foreign Currency)
```

**Príklady:**
```sql
purchase_base_value_ac DECIMAL(15,2)    -- NC bez DPH v účtovnej mene
purchase_base_value_fc DECIMAL(15,2)    -- NC bez DPH vo vyúčtovacej mene

sales_total_value_ac DECIMAL(15,2)      -- PC s DPH v účtovnej mene
sales_total_value_fc DECIMAL(15,2)      -- PC s DPH vo vyúčtovacej mene
```

---

### 8.5 Dátumové polia

**Pattern:**
```sql
{field}_date   -- Len dátum
{field}_at     -- Dátum + čas (zlúčené z Btrieve Date+Time)
```

**Príklady:**
```sql
document_date DATE               -- Dátum vystavenia dokladu
expiry_date DATE                 -- Dátum expirácie

created_at TIMESTAMP             -- Kedy vytvorené (Date+Time)
updated_at TIMESTAMP             -- Kedy zmenené (Date+Time)
paired_at TIMESTAMP              -- Kedy vypárované (Date+Time)
```

---

### 8.6 Dátové typy

**Štandard:**
```sql
-- Ceny, hodnoty
DECIMAL(15,2)     -- 2 desatinné miesta

-- Množstvá
DECIMAL(15,3)     -- 3 desatinné miesta

-- Percentá
DECIMAL(5,2)      -- 0.00 - 100.00

-- Kurzy mien
DECIMAL(15,6)     -- 6 desatinných miest

-- Texty
VARCHAR(n)        -- Fixná dĺžka
TEXT              -- Neobmedzené

-- Celé čísla
INTEGER           -- Štandard
BIGINT            -- Veľké čísla (ID)
SMALLINT          -- Malé čísla (rok, počty)

-- Dátumy
DATE              -- Len dátum
TIMESTAMP         -- Dátum + čas

-- Boolean
BOOLEAN           -- true/false
```

---

---

## 9. MIGRÁCIA - VŠEOBECNÉ ZÁSADY

### 9.1 Workflow

```
1. PRÍPRAVA
   - Migruj katalógy (partners, products, stocks...)
   - Vytvor všetky history verzie s modify_id=0

2. MIGRÁCIA DOKLADOV
   - Migruj hlavičky (heads)
   - Migruj položky (items)
   - Migruj texty (texts - do document_texts!)
   - Migruj platby (payments)

3. VALIDÁCIA
   - Skontroluj počty
   - Skontroluj unikátnosť
   - Skontroluj referencie
   - Skontroluj sumy
```

---

### 9.2 Versioning pri migrácii

**Pred migráciou dokladov:**
```python
# 1. Migruj všetkých partnerov s modify_id = 0
for partner in get_all_btrieve_partners():
    insert_partner_history(
        partner_id=partner.Code,
        modify_id=0,  # Prvá verzia
        name=partner.Name,
        ...,
        valid_from='1970-01-01',  # Pôvodná verzia
        valid_to=None             # Aktuálna
    )

# 2. Migruj všetky produkty s modify_id = 0
for product in get_all_btrieve_products():
    insert_product_history(
        product_id=product.Code,
        modify_id=0,  # Prvá verzia
        code=product.Code,
        name=product.Name,
        ...,
        valid_from='1970-01-01',
        valid_to=None
    )
```

**Pri migrácii dokladu:**
```python
def migrate_delivery_head(record):
    insert_delivery_head(
        supplier_id=record.PaCode,
        supplier_modify_id=0,  # Používame prvú verziu
        product_id=record.GsCode,
        product_modify_id=0,   # Používame prvú verziu
        ...
    )
```

---

### 9.3 Neprenesené polia

**Typy polí, ktoré sa NEPRENÁŠAJÚ:**

1. **Pracovné polia** (vyhľadávanie, cache)
   ```
   _PaName  ;Pracovny nazov pre vyhladavanie
   ```

2. **Staré odkazy** (nahradené M:N tabuľkami)
   ```
   IsdNum   ;Cislo faktury (teraz cez supplier_delivery_invoices)
   OsdNum   ;Cislo objednavky (teraz cez supplier_delivery_orders)
   ```

3. **Zastarané funkcie**
   ```
   Sended   ;Priznak odoslania (internet, nepoužíva sa)
   SndNum   ;Poradove cislo odoslania
   SndStat  ;Stav prenosu
   ```

4. **Interné technické**
   ```
   ModNum   ;Poradove cislo modifikacie
   ```

5. **Špecifické funkcie** (mimo core)
   ```
   RbaCode  ;Vyrobna sarza (len ak sa nepoužíva)
   PkdNum   ;Prebalenie (len ak sa nepoužíva)
   ```

---

### 9.4 Validácia po migrácii

**Kontrolné dotazy (rovnaké pre všetky typy dokladov):**

```sql
-- 1. Kontrola počtu záznamov
SELECT 
    'Btrieve' AS source,
    COUNT(*) AS count
FROM btrieve_import_temp
UNION ALL
SELECT 
    'PostgreSQL' AS source,
    COUNT(*) AS count
FROM supplier_delivery_heads;

-- 2. Kontrola unikátnosti document_number
SELECT document_number, COUNT(*)
FROM supplier_delivery_heads
GROUP BY document_number
HAVING COUNT(*) > 1;

-- 3. Kontrola unikátnosti book_sequence
SELECT book_num, year, book_sequence, COUNT(*)
FROM supplier_delivery_heads
GROUP BY book_num, year, book_sequence
HAVING COUNT(*) > 1;

-- 4. Kontrola FK integrity
SELECT COUNT(*)
FROM supplier_delivery_heads h
LEFT JOIN partner_catalog_history ph
    ON ph.partner_id = h.supplier_id
    AND ph.modify_id = h.supplier_modify_id
WHERE ph.history_id IS NULL;

-- 5. Kontrola item_count
SELECT 
    h.document_number,
    h.item_count AS head_count,
    COUNT(i.item_id) AS actual_count
FROM supplier_delivery_heads h
LEFT JOIN supplier_delivery_items i ON i.delivery_head_id = h.document_id
GROUP BY h.document_id, h.document_number, h.item_count
HAVING h.item_count != COUNT(i.item_id);

-- 6. Kontrola textov v document_texts
SELECT 
    document_type,
    COUNT(*) as text_count
FROM document_texts
GROUP BY document_type;
```

---

---

## 10. VALIDAČNÉ PRAVIDLÁ

### 10.1 Povinné polia

**Minimálna sada pre každý doklad:**
```sql
CHECK (document_number IS NOT NULL)
CHECK (document_date IS NOT NULL)
CHECK (year IS NOT NULL)
CHECK (global_sequence IS NOT NULL)
CHECK (book_num IS NOT NULL)
CHECK (created_by IS NOT NULL)
CHECK (created_at IS NOT NULL)
```

---

### 10.2 Číselné hodnoty

```sql
-- Kladné hodnoty
CHECK (global_sequence > 0)
CHECK (book_sequence > 0)

-- Percentá 0-100
CHECK (vat_rate >= 0 AND vat_rate <= 100)
CHECK (discount_percent >= 0 AND discount_percent <= 100)

-- Množstvo > 0
CHECK (quantity > 0)

-- Kurz > 0
CHECK (foreign_currency_rate IS NULL OR foreign_currency_rate > 0)
```

---

### 10.3 Referenčná integrita

```sql
-- Master data - RESTRICT
FOREIGN KEY (supplier_id) REFERENCES partners(partner_id) ON DELETE RESTRICT
FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT
FOREIGN KEY (stock_id) REFERENCES stocks(stock_id) ON DELETE RESTRICT

-- Detail data - CASCADE
FOREIGN KEY (delivery_head_id) REFERENCES supplier_delivery_heads(document_id) ON DELETE CASCADE
```

---

### 10.4 Stavy

```sql
-- Status lifecycle
CHECK (status IN ('draft', 'received', 'posted'))

-- Paired status
CHECK (paired_status IN ('N', 'P', 'Q', 'H', 'C'))

-- Logika: draft musí byť unpaired
CHECK (
    (status = 'draft' AND paired_status = 'N') OR
    (status IN ('received', 'posted'))
)
```

---

---

**See Also:**
- [00_DATABASE_INDEX.md](00_DATABASE_INDEX.md) - Database documentation index
- [../documents/NUMBERING.md](../documents/NUMBERING.md) - Document numbering
