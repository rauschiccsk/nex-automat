# ISI → supplier_invoice_items

**Verzia:** 1.1  
**Dátum:** 2025-12-15  
**Batch:** 6 (Accounting - dokument 2/3)  
**Status:** ✅ Pripravené na migráciu

---

## PREHĽAD

### Účel
Položky dodávateľských faktúr (Supplier Invoice Items) obsahujú detail jednotlivých produktov/služieb na faktúre. Každá položka reprezentuje jeden riadok faktúry s množstvom, cenou a DPH.

### Btrieve súbor
- **Názov:** ISI[YY][NNN].BTR (multi-file architektúra)
- **Umiestnenie:** `C:\NEX\YEARACT\LEDGER\ISI[YY][NNN].BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\LEDGER\`
  - [YY] = rok (25 = 2025)
  - [NNN] = číslo knihy (001, 002...)
- **Účel:** Položky dodávateľských faktúr pre konkrétnu knihu a rok
- **Príklad:** `ISI25001.BTR` = Kniha 1, rok 2025

### PostgreSQL migrácia
**Nový systém (NEX Automat):**
```
supplier_invoice_items - jedna tabuľka pre všetky knihy
```

**Mapping:** `ISI25001.BTR` → `supplier_invoice_items` WHERE `invoice_head_id` IN (SELECT document_id FROM supplier_invoice_heads WHERE book_num=1 AND year=2025)

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

## MAPPING POLÍ

### Hlavička a číslovanie

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| DocNum | Str12 | invoice_head_id | BIGINT | FK na supplier_invoice_heads |
| ItmNum | word | line_number | INTEGER | 1, 2, 3... |

### Produkt (Versioning)
**Pre všeobecné zásady pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 2

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
**Pre všeobecné zásady pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 5

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
**Pre všeobecné zásady pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 5

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| FgDPrice | double | list_unit_price_fc | DECIMAL(15,2) |
| FgCPrice | double | purchase_unit_price_fc | DECIMAL(15,2) |
| FgDValue | double | list_value_fc | DECIMAL(15,2) |
| FgDscVal | double | discount_value_fc | DECIMAL(15,2) |
| FgCValue | double | purchase_base_value_fc | DECIMAL(15,2) |
| FgEValue | double | purchase_total_value_fc | DECIMAL(15,2) |

### Účtovanie (ŠPECIFICKÉ PRE FAKTÚRY)

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| AccSnt | Str3 | synthetic_account | VARCHAR(3) | Syntetický účet |
| AccAnl | Str8 | analytical_account | VARCHAR(6) | Analytický účet |

**POZNÁMKA:** Účtovanie položiek je špecifické pre faktúry (v TSI to nie je).

### Párovanie (M:N tabuľky)

| Btrieve | Typ | PostgreSQL Tabuľka | Poznámka |
|---------|-----|-------------------|----------|
| OsdNum | Str12 | supplier_order_invoices | M:N s objednávkami (NOVÁ!) |
| OsdItm | word | supplier_order_invoices | - |
| TsdNum | Str12 | supplier_delivery_invoices | M:N s DD (existuje v TSI!) |
| TsdItm | word | supplier_delivery_invoices | - |

### Audit
**Pre všeobecné zásady pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 7

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

## BIZNIS LOGIKA

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

**Tabuľka supplier_order_invoices (NOVÁ!):**
```
- pairing_id: SERIAL PRIMARY KEY
- order_item_id: BIGINT (položka objednávky)
- invoice_item_id: BIGINT (položka faktúry)
- paired_quantity: DECIMAL(15,3) (vypárované množstvo)
- created_at: TIMESTAMP
- created_by: VARCHAR(8)
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
    insert_order_invoice_pairing(
        order_item_id=order_item_id,
        invoice_item_id=invoice_item_id,
        paired_quantity=paired_quantity,
        created_by=created_by
    )
    
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

**Tabuľka supplier_delivery_invoices (UŽ EXISTUJE):**
```
- pairing_id: SERIAL PRIMARY KEY
- delivery_item_id: BIGINT (položka DD)
- invoice_item_id: BIGINT (položka DF)
- paired_quantity: DECIMAL(15,3) (vypárované množstvo)
- created_at: TIMESTAMP
- created_by: VARCHAR(8)
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

## VZŤAHY S INÝMI TABUĽKAMI

### Master-Detail vzťahy

```sql
-- Hlavička (1:N) - CASCADE
supplier_invoice_heads (1) ──< (N) supplier_invoice_items
    ON DELETE CASCADE
```

### Reference na katalógy (Versioning)
**Pre všeobecné zásady pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 2

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

## PRÍKLAD DÁT

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

## MIGRÁCIA

### Extrahovanie book_num z názvu súboru

```python
def extract_book_info(filename):
    """
    ISI25001.BTR → year=2025, book_num=1
    ISI24002.BTR → year=2024, book_num=2
    """
    match = re.match(r'ISI(\d{2})(\d{3})\.BTR', filename)
    if match:
        year = 2000 + int(match.group(1))
        book_num = int(match.group(2))
        return year, book_num
    raise ValueError(f"Invalid filename: {filename}")
```

### Versioning pri migrácii
**Pre všeobecné zásady pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 9.2

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
```

---

## POZNÁMKY PRE MIGRÁCIU

### Kľúčové body

1. **Multi-file architektúra:**
   - `ISI25001.BTR` → položky pre `book_num=1, year=2025`
   - Všetky knihy migrujú do jednej tabuľky

2. **M:N tabuľky:**
   - `supplier_delivery_invoices` - UŽ EXISTUJE z TSI Session 7
   - `supplier_order_invoices` - NOVÁ tabuľka

3. **Paired status:**
   - Párovanie s DD/objednávkami je na úrovni **položiek**
   - Hlavička má agregovaný stav

4. **Notice → document_texts:**
   - Notice sa migruje do univerzálnej tabuľky `document_texts`
   - Nie je ako pole v položke

5. **Účtovanie položiek:**
   - `synthetic_account`, `analytical_account`
   - NOVÉ oproti TSI (dodacie listy nemajú)

6. **Versioning systém:**
   - Pri migrácii: `product_modify_id = 0`
   - Reference do `product_catalog_history`

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

---

**Koniec dokumentu ISI-supplier_invoice_items.md v1.1**