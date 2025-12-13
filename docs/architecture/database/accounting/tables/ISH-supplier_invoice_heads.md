# ISH.BTR → supplier_invoice_heads

**Pre všeobecné zásady pozri:** [COMMON_DOCUMENT_PRINCIPLES.md](../../COMMON_DOCUMENT_PRINCIPLES.md)

Tento dokument popisuje **ŠPECIFICKÉ vlastnosti** dodávateľských faktúr (hlavičky).

---

## 1. PREHĽAD

### Účel
Hlavičky dodávateľských faktúr (Supplier Invoice Headers) obsahujú základné informácie o prijatých faktúrach od dodávateľov. Slúžia ako master záznamy pre detail položky, texty a platby.

### Btrieve súbory
**Starý systém (NEX Genesis):**
```
ISH25001.BTR  - Kniha č. 1, rok 2025
ISH25002.BTR  - Kniha č. 2, rok 2025
ISH24001.BTR  - Kniha č. 1, rok 2024
```

**Nový systém (NEX Automat):**
```
supplier_invoice_heads - jedna tabuľka pre všetky knihy
```

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

## 2. SQL SCHÉMA

```sql
-- =====================================================
-- HLAVIČKA DODÁVATEĽSKÝCH FAKTÚR
-- =====================================================

CREATE TABLE supplier_invoice_heads (
    -- Technický primárny kľúč
    document_id BIGSERIAL PRIMARY KEY,
    
    -- ========================================
    -- ČÍSLOVANIE DOKLADOV
    -- Detaily v COMMON_DOCUMENT_PRINCIPLES.md
    -- ========================================
    
    document_number VARCHAR(13) NOT NULL UNIQUE,
    document_type VARCHAR(2) NOT NULL DEFAULT 'DF',
    year SMALLINT NOT NULL,
    global_sequence INTEGER NOT NULL,
    book_num INTEGER NOT NULL,
    book_sequence INTEGER NOT NULL,
    variable_symbol VARCHAR(12),
    supplier_invoice_number VARCHAR(32),
    old_document_number VARCHAR(13),
    
    -- ========================================
    -- DÁTUMY (ŠPECIFICKÉ PRE DF)
    -- ========================================
    
    received_date DATE NOT NULL,
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    vat_date DATE NOT NULL,
    tax_period_date DATE,
    payment_date DATE,
    posting_date DATE,
    payment_order_date DATE,
    warning_date DATE,
    
    -- ========================================
    -- ZÁKLADNÉ ÚDAJE
    -- ========================================
    
    stock_id INTEGER NOT NULL,
    facility_id INTEGER,
    constant_symbol VARCHAR(4),
    
    -- ========================================
    -- DODÁVATEĽ (VERSIONING SYSTÉM)
    -- Detaily v COMMON_DOCUMENT_PRINCIPLES.md
    -- ========================================
    
    supplier_id INTEGER NOT NULL,
    supplier_modify_id INTEGER NOT NULL,
    supplier_facility_id INTEGER,
    supplier_facility_modify_id INTEGER,
    
    -- ========================================
    -- BANKOVÉ ÚDAJE (SNAPSHOT - DÔLEŽITÉ PRE FAKTÚRY!)
    -- ========================================
    
    iban_code VARCHAR(34),
    swift_code VARCHAR(20),
    bank_code VARCHAR(15),
    bank_name VARCHAR(30),
    account_number VARCHAR(30),
    
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
    
    -- ========================================
    -- HODNOTY V ÚČTOVNEJ MENE (AC)
    -- Detaily v COMMON_DOCUMENT_PRINCIPLES.md
    -- ========================================
    
    accounting_currency VARCHAR(3) NOT NULL DEFAULT 'EUR',
    
    -- Predajné ceny (PC)
    list_value_ac DECIMAL(15,2),
    discount_value_ac DECIMAL(15,2),
    sales_base_value_ac DECIMAL(15,2),
    sales_total_value_ac DECIMAL(15,2),
    
    -- Nákupné ceny (NC)
    purchase_base_value_ac DECIMAL(15,2),
    purchase_vat_value_ac DECIMAL(15,2),
    purchase_total_value_ac DECIMAL(15,2),
    
    -- Platby
    previous_year_paid_ac DECIMAL(15,2) DEFAULT 0,
    total_paid_ac DECIMAL(15,2) DEFAULT 0,
    remaining_ac DECIMAL(15,2),
    
    -- ========================================
    -- HODNOTY VO VYÚČTOVACEJ MENE (FC)
    -- Detaily v COMMON_DOCUMENT_PRINCIPLES.md
    -- ========================================
    
    foreign_currency VARCHAR(3),
    foreign_currency_rate DECIMAL(15,6),
    year_end_rate DECIMAL(15,6),
    exchange_difference_ac DECIMAL(15,2),
    
    -- Predajné ceny (PC)
    list_value_fc DECIMAL(15,2),
    discount_value_fc DECIMAL(15,2),
    
    -- Nákupné ceny (NC)
    purchase_base_value_fc DECIMAL(15,2),
    purchase_vat_value_fc DECIMAL(15,2),
    purchase_total_value_fc DECIMAL(15,2),
    
    -- Platby
    previous_year_paid_fc DECIMAL(15,2) DEFAULT 0,
    total_paid_fc DECIMAL(15,2) DEFAULT 0,
    remaining_fc DECIMAL(15,2),
    
    -- ========================================
    -- STAVY DOKLADU (ŠPECIFICKÉ PRE DF)
    -- ========================================
    
    posting_status VARCHAR(20) NOT NULL DEFAULT 'unposted',
    paired_status VARCHAR(1) NOT NULL DEFAULT 'N',
    payment_status VARCHAR(20) NOT NULL DEFAULT 'unpaid',
    is_vat_document BOOLEAN DEFAULT true,
    vat_close_id INTEGER DEFAULT 0,
    
    -- ========================================
    -- OPRAVNÉ FAKTÚRY
    -- ========================================
    
    original_invoice_id BIGINT,
    original_external_number VARCHAR(32),
    
    -- ========================================
    -- UPOMIENKY
    -- ========================================
    
    warning_number SMALLINT DEFAULT 0,
    
    -- ========================================
    -- ÚČTOVANIE
    -- ========================================
    
    synthetic_account VARCHAR(3),
    analytical_account VARCHAR(6),
    
    -- ========================================
    -- ŠPECIFIKÁCIA A ŠTATISTIKA
    -- ========================================
    
    document_specification SMALLINT,
    item_count INTEGER DEFAULT 0,
    print_count INTEGER DEFAULT 0,
    modification_number INTEGER DEFAULT 0,
    
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
    CONSTRAINT chk_document_type CHECK (document_type = 'DF'),
    CONSTRAINT chk_posting_status CHECK (posting_status IN ('unposted', 'posted')),
    CONSTRAINT chk_paired_status CHECK (paired_status IN ('N', 'P', 'Q')),
    CONSTRAINT chk_payment_status CHECK (payment_status IN ('unpaid', 'partially_paid', 'paid')),
    CONSTRAINT fk_original_invoice FOREIGN KEY (original_invoice_id) 
        REFERENCES supplier_invoice_heads(document_id) ON DELETE RESTRICT
);

-- ========================================
-- INDEXY
-- ========================================

CREATE INDEX idx_supplier_invoice_heads_book ON supplier_invoice_heads(book_num);
CREATE INDEX idx_supplier_invoice_heads_supplier ON supplier_invoice_heads(supplier_id);
CREATE INDEX idx_supplier_invoice_heads_stock ON supplier_invoice_heads(stock_id);
CREATE INDEX idx_supplier_invoice_heads_received_date ON supplier_invoice_heads(received_date);
CREATE INDEX idx_supplier_invoice_heads_due_date ON supplier_invoice_heads(due_date);
CREATE INDEX idx_supplier_invoice_heads_posting_status ON supplier_invoice_heads(posting_status);
CREATE INDEX idx_supplier_invoice_heads_paired ON supplier_invoice_heads(paired_status);
CREATE INDEX idx_supplier_invoice_heads_payment ON supplier_invoice_heads(payment_status);
CREATE INDEX idx_supplier_invoice_heads_year_type ON supplier_invoice_heads(year, document_type);
CREATE INDEX idx_supplier_invoice_heads_vat_close ON supplier_invoice_heads(vat_close_id);
CREATE INDEX idx_supplier_invoice_heads_variable_symbol ON supplier_invoice_heads(variable_symbol);

-- ========================================
-- TRIGGERY
-- Funkcie definované v COMMON_DOCUMENT_PRINCIPLES.md
-- ========================================

CREATE TRIGGER trg_supplier_invoice_heads_updated_at
    BEFORE UPDATE ON supplier_invoice_heads
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_supplier_invoice_heads_book_sequence
    BEFORE INSERT OR UPDATE ON supplier_invoice_heads
    FOR EACH ROW
    EXECUTE FUNCTION recalculate_book_sequence();

-- =====================================================
-- DPH SKUPINY (ŠPECIFICKÉ PRE DOKLADY)
-- =====================================================

CREATE TABLE supplier_invoice_vat_groups (
    vat_group_id SERIAL PRIMARY KEY,
    invoice_head_id BIGINT NOT NULL REFERENCES supplier_invoice_heads(document_id) ON DELETE CASCADE,
    vat_rate DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT uq_invoice_vat_rate UNIQUE (invoice_head_id, vat_rate)
);

CREATE INDEX idx_supplier_invoice_vat_groups_invoice ON supplier_invoice_vat_groups(invoice_head_id);

-- =====================================================
-- DPH HODNOTY (EAV PATTERN)
-- =====================================================

CREATE TABLE supplier_invoice_vat_amounts (
    amount_id SERIAL PRIMARY KEY,
    vat_group_id INTEGER NOT NULL REFERENCES supplier_invoice_vat_groups(vat_group_id) ON DELETE CASCADE,
    amount_type VARCHAR(30) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    
    CONSTRAINT uq_vat_group_amount_type UNIQUE (vat_group_id, amount_type),
    CONSTRAINT chk_amount_type CHECK (
        amount_type IN (
            'base_ac',
            'total_ac',
            'base_fc',
            'total_fc'
        )
    )
);

CREATE INDEX idx_supplier_invoice_vat_amounts_group ON supplier_invoice_vat_amounts(vat_group_id);
```

---

## 3. MAPPING POLÍ

### Číslovanie dokladov
**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 1

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
**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 2

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

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| IbanCode | Str34 | iban_code | VARCHAR(34) |
| SwftCode | Str20 | swift_code | VARCHAR(20) |
| BankCode | Str15 | bank_code | VARCHAR(15) |
| BankSeat | Str30 | bank_name | VARCHAR(30) |
| ContoNum | Str30 | account_number | VARCHAR(30) |

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
**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 5

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| AcDvzName | Str3 | accounting_currency | VARCHAR(3) |
| AcDValue | double | list_value_ac | DECIMAL(15,2) |
| AcDscVal | double | discount_value_ac | DECIMAL(15,2) |
| AcAValue | double | sales_base_value_ac | DECIMAL(15,2) |
| AcBValue | double | sales_total_value_ac | DECIMAL(15,2) |
| AcCValue | double | purchase_base_value_ac | DECIMAL(15,2) |
| AcVatVal | double | purchase_vat_value_ac | DECIMAL(15,2) |
| AcEValue | double | purchase_total_value_ac | DECIMAL(15,2) |
| AcPrvPay | double | previous_year_paid_ac | DECIMAL(15,2) |
| AcPayVal | double | total_paid_ac | DECIMAL(15,2) |
| AcEndVal | double | remaining_ac | DECIMAL(15,2) |

### Hodnoty vo vyúčtovacej mene (FC)
**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 5

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

| Btrieve | PostgreSQL Tabuľka | Amount Type |
|---------|-------------------|-------------|
| VatPrc1-5 | supplier_invoice_vat_groups | vat_rate |
| AcCValue1-3 | supplier_invoice_vat_amounts | base_ac |
| AcEValue1-3 | supplier_invoice_vat_amounts | total_ac |
| FgCValue1-3 | supplier_invoice_vat_amounts | base_fc |
| FgEValue1-3 | supplier_invoice_vat_amounts | total_fc |

### Stavy dokladu

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| DstAcc | Str1 | posting_status | VARCHAR(20) | ''→unposted, A→posted |
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
**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 7

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

## 4. BIZNIS LOGIKA (ŠPECIFICKÉ PRE DF)

### Lifecycle dokladu

```
┌──────────┐  Zaúčtovať   ┌─────────┐
│ UNPOSTED │  do denníka  │ POSTED  │
│          │ ──────────>  │         │
└──────────┘              └─────────┘

posting_status: unposted → posted
```

**Pravidlá:**
1. **Unposted → Posted:** Vytvorenie záznamov v denníku účtovných zápisov (accounting journal)
2. **Nie je možné zmeniť faktúru v stave Posted** (ak vat_close_id > 0)
3. **Párovanie s DD** môže byť kedykoľvek (nezávisle od posting_status)

---

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

---

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

---

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

---

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

---

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

---

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

## 5. VZŤAHY S INÝMI TABUĽKAMI

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

### Opravné faktúry

```sql
-- Self-reference
original_invoice_id → supplier_invoice_heads.document_id (RESTRICT)
```

---

## 6. QUERY PATTERNS

### Zobrazenie faktúry s partnerom

```sql
SELECT 
    i.document_number,
    i.supplier_invoice_number,
    i.variable_symbol,
    i.received_date,
    i.issue_date,
    i.due_date,
    i.posting_status,
    i.paired_status,
    i.payment_status,
    
    -- Partner z history (správna verzia!)
    ph.name AS supplier_name,
    ph.reg_name AS supplier_reg_name,
    ph.ino AS supplier_ino,
    ph.street AS supplier_street,
    
    -- Bankové údaje (snapshot)
    i.iban_code,
    i.swift_code,
    i.bank_name,
    i.account_number,
    
    -- Hodnoty
    i.purchase_base_value_ac,
    i.purchase_vat_value_ac,
    i.purchase_total_value_ac,
    i.total_paid_ac,
    i.remaining_ac
    
FROM supplier_invoice_heads i
LEFT JOIN partner_catalog_history ph
    ON ph.partner_id = i.supplier_id
    AND ph.modify_id = i.supplier_modify_id
WHERE i.document_id = $1;
```

### Zobrazenie DPH skupín

```sql
SELECT 
    g.vat_rate,
    MAX(CASE WHEN a.amount_type = 'base_ac' THEN a.amount END) AS base_ac,
    MAX(CASE WHEN a.amount_type = 'total_ac' THEN a.amount END) AS total_ac
FROM supplier_invoice_vat_groups g
LEFT JOIN supplier_invoice_vat_amounts a ON a.vat_group_id = g.vat_group_id
WHERE g.invoice_head_id = $1
GROUP BY g.vat_rate
ORDER BY g.vat_rate DESC;
```

### Nezaúčtované faktúry

```sql
SELECT 
    i.document_number,
    i.supplier_invoice_number,
    i.received_date,
    i.due_date,
    ph.name AS supplier_name,
    i.purchase_total_value_ac
FROM supplier_invoice_heads i
LEFT JOIN partner_catalog_history ph
    ON ph.partner_id = i.supplier_id
    AND ph.modify_id = i.supplier_modify_id
WHERE i.posting_status = 'unposted'
ORDER BY i.received_date;
```

### Faktúry po splatnosti

```sql
SELECT 
    i.document_number,
    i.supplier_invoice_number,
    i.due_date,
    CURRENT_DATE - i.due_date AS days_overdue,
    ph.name AS supplier_name,
    i.remaining_ac
FROM supplier_invoice_heads i
LEFT JOIN partner_catalog_history ph
    ON ph.partner_id = i.supplier_id
    AND ph.modify_id = i.supplier_modify_id
WHERE i.payment_status != 'paid'
  AND i.due_date < CURRENT_DATE
ORDER BY days_overdue DESC;
```

### Nevypárované faktúry

```sql
SELECT 
    i.document_number,
    i.supplier_invoice_number,
    i.received_date,
    ph.name AS supplier_name,
    i.purchase_total_value_ac
FROM supplier_invoice_heads i
LEFT JOIN partner_catalog_history ph
    ON ph.partner_id = i.supplier_id
    AND ph.modify_id = i.supplier_modify_id
WHERE i.paired_status = 'N'
ORDER BY i.received_date;
```

### Opravné faktúry

```sql
SELECT 
    i.document_number AS correction_number,
    o.document_number AS original_number,
    i.original_external_number,
    i.received_date,
    ph.name AS supplier_name,
    i.purchase_total_value_ac
FROM supplier_invoice_heads i
LEFT JOIN supplier_invoice_heads o ON o.document_id = i.original_invoice_id
LEFT JOIN partner_catalog_history ph
    ON ph.partner_id = i.supplier_id
    AND ph.modify_id = i.supplier_modify_id
WHERE i.original_invoice_id IS NOT NULL
ORDER BY i.received_date DESC;
```

---

## 7. PRÍKLAD DÁT

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

### Opravná faktúra

```sql
INSERT INTO supplier_invoice_heads (
    document_number, year, global_sequence,
    book_num, supplier_invoice_number,
    original_invoice_id, original_external_number,
    received_date, issue_date, due_date, vat_date,
    stock_id,
    supplier_id, supplier_modify_id,
    accounting_currency,
    purchase_base_value_ac, purchase_vat_value_ac, purchase_total_value_ac,
    posting_status, paired_status, payment_status,
    created_by, created_at
) VALUES (
    'DF2500000124', 2025, 124,
    1, 'FA-2025-100-OPRAVA',
    1, 'FA-2025-100',
    '2025-01-20', '2025-01-18', '2025-02-18', '2025-01-18',
    1,
    456, 0,
    'EUR',
    -100.00, -21.00, -121.00,
    'unposted', 'N', 'unpaid',
    'zoltan', '2025-01-20 11:00:00'
);
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
insert_invoice_head(
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

### Platobné polia

```python
def migrate_payment_fields(record):
    return {
        'previous_year_paid_ac': record.AcPrvPay,
        'total_paid_ac': record.AcPayVal,
        'remaining_ac': record.AcEndVal,
        'previous_year_paid_fc': record.FgPrvPay,
        'total_paid_fc': record.FgPayVal,
        'remaining_fc': record.FgEndVal,
    }
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

-- Kontrola súm
SELECT 
    COUNT(*) AS total_invoices,
    SUM(purchase_total_value_ac) AS total_value,
    SUM(total_paid_ac) AS total_paid,
    SUM(remaining_ac) AS total_remaining
FROM supplier_invoice_heads;
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
- `partner_catalog` + `partner_catalog_history` - versioning
- `partner_facilities` + `partner_facilities_history` - versioning
- `stocks`, `payment_methods`, `transport_methods` - číselníky

**Súvisiace dokumenty:**
- `ISI-supplier_invoice_items.md` - položky faktúr
- `document_texts` - texty (univerzálna tabuľka)
- `ISP-supplier_invoice_payments.md` - platby
- `TSH-supplier_delivery_heads.md`, `TSI-supplier_delivery_items.md` - dodacie listy (párovanie)

### Poznámky

1. **supplier_delivery_invoices** je v ISI (M:N medzi položkami DD a položkami DF), NIE v ISH!
2. **document_texts** je univerzálna tabuľka pre všetky typy dokladov
3. **paired_status** v hlavičke je agregovaný z položiek
4. **payment_status** sa vypočítava z platobných polí
5. **vat_close_id** nahrádza DstLck a VatCls (nový prístup)
6. **Bankové účty** - SNAPSHOT (iban_code, swift_code...) - veľmi dôležité pre faktúry!

---

**Koniec dokumentu ISH-supplier_invoice_heads.md v1.0**