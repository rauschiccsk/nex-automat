# ISH → supplier_invoice_heads

**Verzia:** 1.1  
**Dátum:** 2025-12-15  
**Batch:** 6 (Accounting - dokument 1/3)  
**Status:** ✅ Pripravené na migráciu

---

## PREHĽAD

### Účel
Hlavičky dodávateľských faktúr (Supplier Invoice Headers) obsahujú základné informácie o prijatých faktúrach od dodávateľov. Slúžia ako master záznamy pre detail položky, texty a platby.

### Btrieve súbor
- **Názov:** ISH[YY][NNN].BTR (multi-file architektúra)
- **Umiestnenie:** `C:\NEX\YEARACT\LEDGER\ISH[YY][NNN].BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\LEDGER\`
  - [YY] = rok (25 = 2025)
  - [NNN] = číslo knihy (001, 002...)
- **Účel:** Hlavičky dodávateľských faktúr pre konkrétnu knihu a rok
- **Príklad:** `ISH25001.BTR` = Kniha 1, rok 2025

### PostgreSQL migrácia
**Nový systém (NEX Automat):**
```
supplier_invoice_heads - jedna tabuľka pre všetky knihy
```

**Mapping:** `ISH25001.BTR` → `supplier_invoice_heads` WHERE `book_num=1` AND `year=2025`

### Vzťahy
```
supplier_invoice_heads (1 hlavička)
    ├──< supplier_invoice_items (N položiek)
    ├──< document_texts (N textov) - univerzálna tabuľka
    ├──< supplier_invoice_payments (N platieb)
    └──< supplier_invoice_vat_groups (N DPH skupín)
```

**POZNÁMKA:** Párovanie s dodacími listami (`supplier_delivery_invoices`) je na úrovni **POLOŽIEK** (ISI), nie hlavičiek!

### Kľúčové entity
- **Dodávateľ:** Partner (supplier_id + supplier_modify_id) - versioning systém
- **Prevádzka dodávateľa:** Facility (supplier_facility_id + supplier_facility_modify_id) - versioning systém
- **Bankové údaje:** Snapshot (iban_code, swift_code, bank_code...) - dôležité pre faktúry
- **Sklad:** Stock (stock_id)
- **Kniha dokladov:** book_num
- **Platobný spôsob:** payment_method_id
- **Dopravný spôsob:** transport_method_id

---

## MAPPING POLÍ

### Číslovanie dokladov
**Pre všeobecné zásady pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 1

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| Year | Str2 | year | SMALLINT | 25 → 2025 |
| SerNum | longint | global_sequence | INTEGER | Globálne poradie |
| DocNum | Str12 | document_number | VARCHAR(13) | DF2500000123 |
| ExtNum | Str12 | variable_symbol | VARCHAR(12) | Variabilný symbol (platby) |
| IncNum | Str32 | supplier_invoice_number | VARCHAR(32) | Číslo faktúry od dodávateľa |
| - | - | book_num | INTEGER | Z ISH25001 → 1 |
| - | - | book_sequence | INTEGER | Auto-trigger |
| - | - | old_document_number | VARCHAR(13) | Migrácia |
| - | - | document_type | VARCHAR(2) | 'DF' |

### Dátumy (ŠPECIFICKÉ PRE DF!)

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| DocDate | DateType | received_date | DATE | Kedy došla faktúra |
| SndDate | DateType | issue_date | DATE | Dátum vystavenia u dodávateľa |
| ExpDate | DateType | due_date | DATE | Dátum splatnosti |
| VatDate | DateType | vat_date | DATE | DPH dátum |
| TaxDate | DateType | tax_period_date | DATE | Zdaniteľné obdobie |
| PayDate | DateType | payment_date | DATE | Dátum poslednej úhrady |
| AccDate | DateType | posting_date | DATE | Dátum zaúčtovania |
| PmqDate | DateType | payment_order_date | DATE | Dátum posledného prevodného príkazu |
| WrnDate | DateType | warning_date | DATE | Dátum poslednej upomienky |

### Základné údaje

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| StkNum | word | stock_id | INTEGER |
| WriNum | word | facility_id | INTEGER |
| CsyCode | Str4 | constant_symbol | VARCHAR(4) |

### Dodávateľ (Versioning)
**Pre všeobecné zásady pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 2

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| PaCode | longint | supplier_id | INTEGER | ID partnera |
| - | - | supplier_modify_id | INTEGER | Verzia (NOVÉ) |
| PaName, RegName, RegIno... | - | - | - | V partner_catalog_history |
| SpaCode | longint | supplier_id | INTEGER | Duplicita PaCode |
| WpaCode | word | supplier_facility_id | INTEGER | ID prevádzky |
| - | - | supplier_facility_modify_id | INTEGER | Verzia (NOVÉ) |
| WpaName, WpaAddr... | - | - | - | V partner_facilities_history |

### Bankové údaje (SNAPSHOT - DÔLEŽITÉ PRE FAKTÚRY!)

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| IbanCode | Str34 | iban_code | VARCHAR(34) | SNAPSHOT - uložené v DF |
| SwftCode | Str20 | swift_code | VARCHAR(20) | SNAPSHOT - uložené v DF |
| BankCode | Str15 | bank_code | VARCHAR(15) | SNAPSHOT - uložené v DF |
| BankSeat | Str30 | bank_name | VARCHAR(30) | SNAPSHOT - uložené v DF |
| ContoNum | Str30 | account_number | VARCHAR(30) | SNAPSHOT - uložené v DF |

**DÔLEŽITÉ:** Bankové údaje sú uložené priamo v hlavičke faktúry (snapshot) - nie sú viazané len na partnera!

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

### Hodnoty v účtovnej mene (AC)
**Pre všeobecné zásady pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 5

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| AcDvzName | Str3 | accounting_currency | VARCHAR(3) | Default 'EUR' |
| AcDValue | double | list_value_ac | DECIMAL(15,2) | Predajná cena |
| AcDscVal | double | discount_value_ac | DECIMAL(15,2) | Zľava |
| AcAValue | double | sales_base_value_ac | DECIMAL(15,2) | Predajná cena po zľave |
| AcBValue | double | sales_total_value_ac | DECIMAL(15,2) | Predajná cena s DPH |
| AcCValue | double | purchase_base_value_ac | DECIMAL(15,2) | **Nákupná cena** |
| AcVatVal | double | purchase_vat_value_ac | DECIMAL(15,2) | **DPH** |
| AcEValue | double | purchase_total_value_ac | DECIMAL(15,2) | **Nákupná cena s DPH** |
| AcPrvPay | double | previous_year_paid_ac | DECIMAL(15,2) | Úhrady z minulých rokov |
| AcPayVal | double | total_paid_ac | DECIMAL(15,2) | Celková úhrada |
| AcEndVal | double | remaining_ac | DECIMAL(15,2) | Zostatok k úhrade |

### Hodnoty vo vyúčtovacej mene (FC)
**Pre všeobecné zásady pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 5

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| FgDvzName | Str3 | foreign_currency | VARCHAR(3) |
| FgCourse | double | foreign_currency_rate | DECIMAL(15,6) |
| EyCourse | double | year_end_rate | DECIMAL(15,6) |
| EyCrdVal | double | exchange_difference_ac | DECIMAL(15,2) |
| FgDValue | double | list_value_fc | DECIMAL(15,2) |
| FgDscVal | double | discount_value_fc | DECIMAL(15,2) |
| FgCValue | double | purchase_base_value_fc | DECIMAL(15,2) |
| FgVatVal | double | purchase_vat_value_fc | DECIMAL(15,2) |
| FgEValue | double | purchase_total_value_fc | DECIMAL(15,2) |
| FgPrvPay | double | previous_year_paid_fc | DECIMAL(15,2) |
| FgPayVal | double | total_paid_fc | DECIMAL(15,2) |
| FgEndVal | double | remaining_fc | DECIMAL(15,2) |

### DPH skupiny (Multi-row → EAV)

**V Btrieve:** Fixné polia (VatPrc1-5, AcCValue1-5...)  
**V PostgreSQL:** Dynamické riadky v `supplier_invoice_vat_groups` + `supplier_invoice_vat_amounts`

| Btrieve | PostgreSQL Tabuľka | Amount Type |
|---------|-------------------|-------------|
| VatPrc1-5 | supplier_invoice_vat_groups | vat_rate |
| AcCValue1-5 | supplier_invoice_vat_amounts | base_ac |
| AcEValue1-5 | supplier_invoice_vat_amounts | total_ac |
| FgCValue1-5 | supplier_invoice_vat_amounts | base_fc |
| FgEValue1-5 | supplier_invoice_vat_amounts | total_fc |

### Stavy dokladu

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| DstAcc | Str1 | posting_status | VARCHAR(20) | ''→unposted, 'A'→posted |
| DstPair | Str1 | paired_status | VARCHAR(1) | N/P/Q |
| - | - | payment_status | VARCHAR(20) | Vypočítané z platieb |
| VatDoc | byte | is_vat_document | BOOLEAN | Daňový doklad |
| DstLck | byte | vat_close_id | INTEGER | >0 = blokovaný |
| VatCls | byte | vat_close_id | INTEGER | Číslo uzávierky DPH |

### Opravné faktúry

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| IodNum | Str15 | original_invoice_id | BIGINT |
| IoeNum | Str32 | original_external_number | VARCHAR(32) |

### Upomienky

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| WrnNum | byte | warning_number | SMALLINT |
| WrnDate | DateType | warning_date | DATE |

### Účtovanie

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| DocSnt | Str3 | synthetic_account | VARCHAR(3) |
| DocAnl | Str6 | analytical_account | VARCHAR(6) |

### Špecifikácia a štatistika

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| DocSpc | byte | document_specification | SMALLINT |
| ItmQnt | word | item_count | INTEGER |
| PrnCnt | byte | print_count | INTEGER |
| ModNum | word | modification_number | INTEGER |

### Audit
**Pre všeobecné zásady pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 7

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| CrtUser | Str8 | created_by | VARCHAR(8) | - |
| CrtDate + CrtTime | Date + Time | created_at | TIMESTAMP | Zlúčené |
| ModUser | Str8 | updated_by | VARCHAR(8) | - |
| ModDate + ModTime | Date + Time | updated_at | TIMESTAMP | Zlúčené |

### NEPRENESENÉ POLIA

**Zastaralé/Nepoužívané:**
- TsdNum (číslo DD - namiesto M:N párovanie)
- CctVal (prenesená daňová povinnosť)
- DstCls (ukončenosť)
- DstLiq (likvidácia - neskôr validačný systém)
- Sended, SndStat (internet prenos)

---

## BIZNIS LOGIKA

### Lifecycle dokladu

```
┌──────────┐  Zaúčtovať   ┌─────────┐
│ UNPOSTED │  do denníka  │ POSTED  │
│          │ ──────────>  │         │
└──────────┘              └─────────┘

posting_status: unposted → posted
```

**Pravidlá:**
1. **Unposted → Posted:** Vytvorenie záznamov v denníku účtovných zápisov
2. **Nie je možné zmeniť faktúru v stave Posted** (ak vat_close_id > 0)
3. **Párovanie s DD** môže byť kedykoľvek (nezávisle od posting_status)

### Paired status (Vyparovanie s dodacími listami)

**Párovanie na úrovni POLOŽIEK!**
```
N (nič) → P (čiastočne) → Q (celé)
```

**Stavy:**
- **N** - Not paired: Nič nie je vypárované
- **P** - Partially paired: Časť položiek je vypárovaná s DD
- **Q** - Queued/Paired: Celý doklad vypárovaný s DD

**KRITICKÉ:** 
- Párovanie s dodacími listami je na úrovni **POLOŽIEK** (ISI), nie hlavičiek!
- `paired_status` v hlavičke je agregovaný stav z položiek
- M:N tabuľka: `supplier_delivery_invoices` (delivery_item_id ↔ invoice_item_id)

### Payment status (Stav úhrad)

**Vypočítané z platobných polí:**
```
unpaid → partially_paid → paid
```

**Pravidlá:**
```python
if total_paid_ac == 0:
    payment_status = 'unpaid'
elif total_paid_ac < purchase_total_value_ac:
    payment_status = 'partially_paid'
else:
    payment_status = 'paid'
```

**Vzorce:**
```
remaining_ac = purchase_total_value_ac - total_paid_ac
remaining_fc = purchase_total_value_fc - total_paid_fc

current_year_paid_ac = total_paid_ac - previous_year_paid_ac
current_year_paid_fc = total_paid_fc - previous_year_paid_fc
```

### VAT Close ID (Uzávierka DPH)

**Namiesto DstLck používame vat_close_id:**

```python
if vat_close_id > 0:
    # Faktúra je blokovaná proti úpravám
    # Bola započítaná do uzávierky DPH č. {vat_close_id}
    is_locked = True
else:
    is_locked = False
```

**Pravidlá:**
- `vat_close_id = 0` → faktúra nie je uzavretá
- `vat_close_id > 0` → faktúra je uzavretá (číslo uzávierky)
- Uzavreté faktúry nie je možné editovať

### Opravné faktúry

**Koncept:**
```
Pôvodná faktúra (document_id = 123)
    ↓
Opravná faktúra (
    document_id = 456,
    original_invoice_id = 123,
    original_external_number = "FA-2025-100"
)
```

**Pravidlá:**
- Opravná faktúra musí mať `original_invoice_id`
- `original_external_number` je číslo pôvodnej faktúry od dodávateľa
- Pôvodnú faktúru nie je možné zmazať, ak existuje opravná

### DPH skupiny (EAV Pattern)

**Rovnaký pattern ako TSH:**
- V Btrieve: fixné polia VatPrc1-5, AcCValue1-3...
- V PostgreSQL: dynamické riadky pre každú DPH sadzbu
- Flexibilita: ľahko pridať nové typy hodnôt

**Príklad:**
```python
# Vytvor faktúru
invoice = create_invoice_head(...)

# Vytvor DPH skupiny
vat_group_1 = create_vat_group(invoice_id, vat_rate=20.00)
vat_group_2 = create_vat_group(invoice_id, vat_rate=10.00)

# Vytvor hodnoty pre každú skupinu
create_vat_amount(vat_group_1, 'base_ac', 1000.00)
create_vat_amount(vat_group_1, 'total_ac', 1200.00)
create_vat_amount(vat_group_2, 'base_ac', 500.00)
create_vat_amount(vat_group_2, 'total_ac', 550.00)
```

### Upomienky

**Koncept:**
```
warning_number = 0 → žiadna upomienka
warning_number = 1 → prvá upomienka (warning_date)
warning_number = 2 → druhá upomienka (warning_date)
...
```

**Pravidlá:**
- `warning_date` = dátum poslednej upomienky
- `warning_number` sa inkrementuje pri každej upomienke

---

## VZŤAHY S INÝMI TABUĽKAMI

### Master-Detail vzťahy

```sql
-- Položky (1:N) - CASCADE
supplier_invoice_heads (1) ──< (N) supplier_invoice_items
    ON DELETE CASCADE

-- Texty (1:N) - CASCADE - UNIVERZÁLNA TABUĽKA!
supplier_invoice_heads (1) ──< (N) document_texts
    WHERE document_type = 'supplier_invoice'
    ON DELETE CASCADE

-- Platby (1:N) - CASCADE
supplier_invoice_heads (1) ──< (N) supplier_invoice_payments
    ON DELETE CASCADE

-- DPH skupiny (1:N) - CASCADE
supplier_invoice_heads (1) ──< (N) supplier_invoice_vat_groups
    ON DELETE CASCADE
```

### Reference na katalógy (Versioning)
**Pre všeobecné zásady pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 2

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

### Opravné faktúry

```sql
-- Self-reference
original_invoice_id → supplier_invoice_heads.document_id (RESTRICT)
```

---

## PRÍKLAD DÁT

### Faktúra - Unposted

```sql
INSERT INTO supplier_invoice_heads (
    document_number, year, global_sequence,
    book_num, variable_symbol, supplier_invoice_number,
    received_date, issue_date, due_date, vat_date,
    stock_id,
    supplier_id, supplier_modify_id,
    iban_code, swift_code, bank_code, bank_name, account_number,
    accounting_currency,
    purchase_base_value_ac, purchase_vat_value_ac, purchase_total_value_ac,
    posting_status, paired_status, payment_status,
    created_by, created_at
) VALUES (
    'DF2500000123', 2025, 123,
    1, '2025000456', 'FA-2025-100',
    '2025-01-15', '2025-01-10', '2025-02-10', '2025-01-10',
    1,
    456, 0,
    'SK1234567890123456789012', 'TATRSKBX', '1100', 'Tatra banka', 'SK1234567890123456789012',
    'EUR',
    1500.00, 315.00, 1815.00,
    'unposted', 'N', 'unpaid',
    'zoltan', '2025-01-15 10:30:00'
);
```

### DPH skupiny

```sql
-- DPH 20%
INSERT INTO supplier_invoice_vat_groups (invoice_head_id, vat_rate)
VALUES (1, 20.00);

INSERT INTO supplier_invoice_vat_amounts (vat_group_id, amount_type, amount)
VALUES 
    (1, 'base_ac', 1000.00),
    (1, 'total_ac', 1200.00);

-- DPH 10%
INSERT INTO supplier_invoice_vat_groups (invoice_head_id, vat_rate)
VALUES (1, 10.00);

INSERT INTO supplier_invoice_vat_amounts (vat_group_id, amount_type, amount)
VALUES 
    (2, 'base_ac', 500.00),
    (2, 'total_ac', 550.00);
```

---

## MIGRÁCIA

### Extrahovanie book_num z názvu súboru

```python
def extract_book_info(filename):
    """
    ISH25001.BTR → year=2025, book_num=1
    ISH24002.BTR → year=2024, book_num=2
    """
    match = re.match(r'ISH(\d{2})(\d{3})\.BTR', filename)
    if match:
        year = 2000 + int(match.group(1))
        book_num = int(match.group(2))
        return year, book_num
    raise ValueError(f"Invalid filename: {filename}")
```

### Versioning pri migrácii
**Pre všeobecné zásady pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 9.2

**Pred migráciou dokladov:**
1. Migruj partnerov do `partner_catalog_history` s `modify_id = 0`
2. Migruj prevádzky do `partner_facilities_history` s `modify_id = 0`

**Pri migrácii dokladu:**
```python
year, book_num = extract_book_info('ISH25001.BTR')

insert_invoice_head(
    year=year,
    book_num=book_num,
    supplier_id=record.PaCode,
    supplier_modify_id=0,  # Prvá verzia
    supplier_facility_id=record.WpaCode,
    supplier_facility_modify_id=0,
    # Bankové údaje - SNAPSHOT
    iban_code=record.IbanCode,
    swift_code=record.SwftCode,
    bank_code=record.BankCode,
    bank_name=record.BankSeat,
    account_number=record.ContoNum,
    ...
)
```

### Dátumy

```python
def migrate_dates(record):
    return {
        'received_date': record.DocDate,
        'issue_date': record.SndDate,
        'due_date': record.ExpDate,
        'vat_date': record.VatDate,
        'tax_period_date': record.TaxDate if record.TaxDate else None,
        'payment_date': record.PayDate if record.PayDate else None,
        'posting_date': record.AccDate if record.AccDate else None,
        'payment_order_date': record.PmqDate if record.PmqDate else None,
        'warning_date': record.WrnDate if record.WrnDate else None,
    }
```

### Stavy dokladu

```python
def get_posting_status(record):
    return 'posted' if record.DstAcc == 'A' else 'unposted'

def get_paired_status(record):
    return record.DstPair  # N, P, Q

def get_payment_status(record):
    if record.AcPayVal == 0:
        return 'unpaid'
    elif record.AcPayVal < record.AcEValue:
        return 'partially_paid'
    else:
        return 'paid'

def get_vat_close_id(record):
    # DstLck=1 alebo VatCls>0 → vat_close_id
    if record.VatCls > 0:
        return record.VatCls
    elif record.DstLck == 1:
        return 1  # Default uzávierka
    else:
        return 0
```

### DPH skupiny

```python
def migrate_vat_groups(record, invoice_head_id):
    # Prvé 4 skupiny (VatPrc1-4), piata je rezerva
    for i in range(1, 5):
        vat_rate = getattr(record, f'VatPrc{i}')
        if vat_rate > 0:
            vat_group_id = insert_vat_group(invoice_head_id, vat_rate)
            
            insert_vat_amount(vat_group_id, 'base_ac', getattr(record, f'AcCValue{i}'))
            insert_vat_amount(vat_group_id, 'total_ac', getattr(record, f'AcEValue{i}'))
            insert_vat_amount(vat_group_id, 'base_fc', getattr(record, f'FgCValue{i}'))
            insert_vat_amount(vat_group_id, 'total_fc', getattr(record, f'FgEValue{i}'))
```

### Validácia po migrácii

```sql
-- Kontrola počtu záznamov
SELECT book_num, year, COUNT(*) 
FROM supplier_invoice_heads
GROUP BY book_num, year;

-- Kontrola DPH skupín
SELECT 
    COUNT(DISTINCT i.document_id) AS invoice_count,
    COUNT(g.vat_group_id) AS vat_group_count,
    COUNT(a.amount_id) AS vat_amount_count
FROM supplier_invoice_heads i
LEFT JOIN supplier_invoice_vat_groups g ON g.invoice_head_id = i.document_id
LEFT JOIN supplier_invoice_vat_amounts a ON a.vat_group_id = g.vat_group_id;

-- Kontrola stavov
SELECT 
    posting_status,
    paired_status,
    payment_status,
    COUNT(*)
FROM supplier_invoice_heads
GROUP BY posting_status, paired_status, payment_status;
```

---

## POZNÁMKY PRE MIGRÁCIU

### Kľúčové body

1. **Multi-file architektúra:**
   - `ISH25001.BTR` → `book_num=1, year=2025`
   - Všetky knihy migrujú do jednej tabuľky

2. **Bankové údaje - SNAPSHOT:**
   - Uložené priamo v hlavičke faktúry (nie len v partnera)
   - Dôležité pre evidenciu úhrad

3. **Paired status:**
   - Párovanie s DD je na úrovni **položiek** (ISI)
   - Hlavička má agregovaný stav

4. **Payment status:**
   - Vypočítaný z platobných polí
   - `total_paid_ac` vs `purchase_total_value_ac`

5. **VAT Close ID:**
   - Nahrádza `DstLck` a `VatCls`
   - Blokuje úpravy po uzávierke DPH

6. **Versioning systém:**
   - Pri migrácii: `supplier_modify_id = 0`
   - Reference do `partner_catalog_history`

### Závislosti

**Tento dokument vyžaduje:**
- `COMMON_DOCUMENT_PRINCIPLES.md` - všeobecné zásady
- `partner_catalog` + `partner_catalog_history` - versioning
- `partner_facilities` + `partner_facilities_history` - versioning
- `stocks`, `payment_methods`, `transport_methods` - číselníky

**Súvisiace dokumenty:**
- `ISI-supplier_invoice_items.md` - položky faktúr
- `document_texts` - texty (univerzálna tabuľka)
- `supplier_invoice_payments` - platby
- `TSH-supplier_delivery_heads.md`, `TSI-supplier_delivery_items.md` - dodacie listy (párovanie)

---

**Koniec dokumentu ISH-supplier_invoice_heads.md v1.1**