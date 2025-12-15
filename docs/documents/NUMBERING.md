# Document Numbering

**Category:** Documents  
**Status:** 🟢 Complete  
**Created:** 2024-12-12  
**Updated:** 2025-12-15  
**Source:** COMMON_DOCUMENT_PRINCIPLES.md

---

## Overview

Document numbering system with three number types:
- System number (document_number)
- Global sequence (global_sequence)  
- Book sequence (book_sequence)

---

## 1. ČÍSLOVANIE DOKLADOV

### 1.1 Koncept

Každý doklad v systéme má **tri typy čísel**:

```
┌───────────────────────────────────────────────────┐
│ 1. SYSTÉMOVÉ ČÍSLO (document_number)               │
│    DD2500000123                                     │
│    - Jedinečné v celom systéme                      │
│    - Používa sa v účtovníctve a sklade              │
│    - NIKDY sa nemení                                │
└───────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────┐
│ 2. GLOBÁLNE PORADIE (global_sequence)              │
│    123                                              │
│    - Poradové číslo v rámci typu a roku             │
│    - Bez medzier (1, 2, 3, 4, 5...)                 │
│    - NIKDY sa nemení                                │
└───────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────┐
│ 3. PORADIE V KNIHE (book_sequence)                 │
│    1, 2, 3, 4...                                    │
│    - Poradové číslo v rámci knihy a roku            │
│    - Bez medzier v rámci knihy                      │
│    - MENÍ SA pri presune medzi knihami              │
└───────────────────────────────────────────────────┘
```

---

### 1.2 Systémové číslo (document_number)

#### Formát
```
TTyy000nnnnn

TT   = Typ dokladu (DD, DF, OD, OF)
yy   = Rok (25 = 2025)
000  = Tri nuly (namiesto čísla knihy v starom systéme)
nnnnn = Globálne poradové číslo (00001-99999)
```

#### Príklady
```
DD2500000001  - Dodávateľský dodací list, rok 2025, poradie 1
DD2500000123  - Dodávateľský dodací list, rok 2025, poradie 123
DF2500000001  - Dodávateľská faktúra, rok 2025, poradie 1
OD2500000001  - Odberateľský dodací list, rok 2025, poradie 1
OF2500000001  - Odberateľská faktúra, rok 2025, poradie 1
```

#### SQL štruktúra
```sql
document_number VARCHAR(13) NOT NULL UNIQUE,
document_type VARCHAR(2) NOT NULL CHECK (document_type IN ('DD', 'DF', 'OD', 'OF')),
year SMALLINT NOT NULL,
global_sequence INTEGER NOT NULL,

CONSTRAINT uq_year_global_sequence UNIQUE (year, global_sequence)
```

#### Generovanie
```python
def generate_document_number(document_type: str, year: int) -> tuple[str, int]:
    """
    Generuj systémové číslo dokladu.
    
    Returns:
        (document_number, global_sequence)
    """
    # Získať ďalšie globálne poradie
    sequence = get_next_global_sequence(document_type, year)
    
    # Format: TTyy000nnnnn
    document_number = f"{document_type}{year:02d}000{sequence:05d}"
    
    return (document_number, sequence)

# Príklad použitia
doc_num, seq = generate_document_number('DD', 2025)
# doc_num = 'DD2500000123'
# seq = 123
```

---

### 1.3 Globálne poradie (global_sequence)

#### Koncept
- Jedinečné v rámci **typu dokladu** a **roku**
- Začína od 1 každý rok
- Bez medzier: 1, 2, 3, 4, 5...
- Nikdy sa nemení (ani pri presune medzi knihami)

#### SQL štruktúra
```sql
global_sequence INTEGER NOT NULL,

CONSTRAINT uq_year_global_sequence UNIQUE (year, global_sequence)
```

#### Generovanie
```sql
-- Funkcia na získanie ďalšieho global_sequence
CREATE FUNCTION get_next_global_sequence(
    p_document_type VARCHAR(2),
    p_year SMALLINT
) RETURNS INTEGER AS $$
DECLARE
    v_sequence INTEGER;
BEGIN
    SELECT COALESCE(MAX(global_sequence), 0) + 1
    INTO v_sequence
    FROM supplier_delivery_heads  -- alebo iná tabuľka
    WHERE document_type = p_document_type
      AND year = p_year;
    
    RETURN v_sequence;
END;
$$ LANGUAGE plpgsql;
```

---

### 1.4 Poradie v knihe (book_sequence)

#### Koncept
- Jedinečné v rámci **knihy**, **typu dokladu** a **roku**
- Začína od 1 v každej knihe
- Bez medzier v rámci knihy: 1, 2, 3, 4, 5...
- **Automaticky prepočítané** pri presune medzi knihami
- Len **informatívne pre používateľov**

#### SQL štruktúra
```sql
book_num INTEGER NOT NULL,
book_sequence INTEGER NOT NULL,

CONSTRAINT uq_book_sequence UNIQUE (book_num, year, book_sequence)
```

#### Automatické generovanie (Trigger)
```sql
CREATE OR REPLACE FUNCTION recalculate_book_sequence()
RETURNS TRIGGER AS $$
BEGIN
    -- Pri INSERT - priradiť ďalšie poradové číslo v knihe
    IF TG_OP = 'INSERT' THEN
        SELECT COALESCE(MAX(book_sequence), 0) + 1
        INTO NEW.book_sequence
        FROM supplier_delivery_heads  -- alebo iná tabuľka
        WHERE book_num = NEW.book_num
          AND document_type = NEW.document_type
          AND year = NEW.year;
        
        RETURN NEW;
    END IF;
    
    -- Pri UPDATE (zmena book_num) - prepočítať v oboch knihách
    IF TG_OP = 'UPDATE' AND OLD.book_num != NEW.book_num THEN
        -- Prepočítať starú knihu (uzavrieť medzeru)
        UPDATE supplier_delivery_heads
        SET book_sequence = book_sequence - 1
        WHERE book_num = OLD.book_num
          AND document_type = OLD.document_type
          AND year = OLD.year
          AND book_sequence > OLD.book_sequence;
        
        -- Priradiť nové poradie v novej knihe
        SELECT COALESCE(MAX(book_sequence), 0) + 1
        INTO NEW.book_sequence
        FROM supplier_delivery_heads
        WHERE book_num = NEW.book_num
          AND document_type = NEW.document_type
          AND year = NEW.year;
        
        RETURN NEW;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger
CREATE TRIGGER trg_recalculate_book_sequence
    BEFORE INSERT OR UPDATE ON supplier_delivery_heads
    FOR EACH ROW
    EXECUTE FUNCTION recalculate_book_sequence();
```

#### Príklad presunu dokladu
```
PRED PRESUNOM:
Kniha 1 (Košice):           Kniha 2 (Komárno):
  DD2500000001  #1            DD2500000002  #1
  DD2500000005  #2  ← tento  DD2500000003  #2
  DD2500000009  #3            DD2500000007  #3

PO PRESUNE DD2500000005 z Košíc do Komárna:
Kniha 1 (Košice):           Kniha 2 (Komárno):
  DD2500000001  #1            DD2500000002  #1
  DD2500000009  #2 (prepočítané) DD2500000003  #2
                              DD2500000005  #3 (nové)
                              DD2500000007  #4 (prepočítané)

Systémové číslo DD2500000005 zostalo NEZMENENÉ!
```

---

### 1.5 Migrácia starých čísel

#### Starý systém (NEX Genesis)
```
TSH25001.BTR → Kniha 1, rok 2025
  DocNum = DD2500100123
           ││││││└─────── Poradie v knihe (123)
           │││││└──────── Číslo knihy (001)
           ││││└───────── Rok (25)
           ││└─────────── Typ (DD)
```

#### Nový systém (NEX Automat)
```sql
CREATE TABLE supplier_delivery_heads (
    document_number VARCHAR(13),      -- DD2500000123 (nové)
    old_document_number VARCHAR(13),  -- DD2500100123 (staré, pre históriu)
    
    year SMALLINT,                    -- 2025
    global_sequence INTEGER,          -- 123
    book_num INTEGER,                 -- 1
    book_sequence INTEGER,            -- Auto-generované
    ...
)
```

#### Migračný kód
```python
def migrate_document_number(old_doc_num: str, year: int, book_num: int):
    """
    Migruj staré číslo dokladu na nové.
    
    Args:
        old_doc_num: DD2500100123 (staré číslo)
        year: 2025
        book_num: 1
    
    Returns:
        (new_doc_num, global_sequence)
    """
    # Parse staré číslo
    # DD2500100123
    doc_type = old_doc_num[0:2]      # DD
    old_year = int(old_doc_num[2:4])  # 25
    old_book = int(old_doc_num[4:7])  # 001
    old_seq = int(old_doc_num[7:12])  # 00123
    
    # Získať ďalší global_sequence
    global_seq = get_next_global_sequence(doc_type, year)
    
    # Generuj nové číslo
    new_doc_num = f"{doc_type}{year:02d}000{global_seq:05d}"
    
    return (new_doc_num, global_seq, old_doc_num)

# Príklad
new, seq, old = migrate_document_number('DD2500100123', 2025, 1)
# new = 'DD2500000456'  (nové globálne poradie)
# seq = 456
# old = 'DD2500100123'  (zachované pre históriu)
```

---

---

## 3. KNIHY DOKLADOV

### 3.1 Koncept

**Kniha dokladov** = logická organizačná jednotka, podobná šanónu alebo zložke.

**Použitie:**
- Oddelenie dokladov podľa prevádzok (Košice, Komárno, Bratislava)
- Oddelenie dokladov podľa typu činnosti
- Centrálne číslovanie v rámci viacerých prevádzok

---

### 3.2 Starý systém (NEX Genesis)

```
Každá kniha = samostatný súbor

TSH25001.BTR  ← Kniha č. 1, rok 2025
TSH25002.BTR  ← Kniha č. 2, rok 2025
TSH25003.BTR  ← Kniha č. 3, rok 2025
TSH24001.BTR  ← Kniha č. 1, rok 2024
```

**Číslovanie:**
```
Kniha 1: DocNum = DD2500100001, DD2500100002, DD2500100003
                         ↑↑↑
                    číslo knihy v systémovom čísle
```

---

### 3.3 Nový systém (NEX Automat)

```
Jedna tabuľka + stĺpec book_num

supplier_delivery_heads (
    book_num INTEGER NOT NULL,
    ...
)
```

**Číslovanie:**
```
Kniha 1: DocNum = DD2500000001, DD2500000005, DD2500000009
Kniha 2: DocNum = DD2500000002, DD2500000006, DD2500000010
                         ↑↑↑
                    tri nuly (globálne číslovanie)
```

---

### 3.4 SQL štruktúra

```sql
CREATE TABLE supplier_delivery_heads (
    book_num INTEGER NOT NULL,                -- Číslo knihy
    book_sequence INTEGER NOT NULL,           -- Poradie v knihe
    
    CONSTRAINT uq_book_sequence UNIQUE (book_num, year, book_sequence),
    
    -- FK na číselník kníh (neskôr)
    -- FOREIGN KEY (book_num) REFERENCES document_books(book_num)
)
```

---

### 3.5 Migrácia z Btrieve

```python
def migrate_tsh_file(filename: str):
    """
    Migruj TSH súbor.
    
    Args:
        filename: TSH25001.BTR
    """
    # Parse názov súboru
    match = re.match(r'TSH(\d{2})(\d{3})\.BTR', filename)
    year = 2000 + int(match.group(1))  # 25 → 2025
    book_num = int(match.group(2))      # 001 → 1
    
    # Migruj všetky záznamy z tohto súboru
    for record in read_btrieve_file(filename):
        migrate_delivery_head(record, year, book_num)
```

---

### 3.6 Konfiguračné parametre kníh

**[NEVIEM]** Podrobná štruktúra číselníka `document_books` bude definovaná v samostatnej dokumentácii.

**Základná štruktúra (orientačne):**
```sql
document_books (
    book_num INTEGER PRIMARY KEY,
    book_name VARCHAR(100),
    document_type VARCHAR(2),
    year SMALLINT,
    facility_id INTEGER,
    is_active BOOLEAN,
    settings JSONB
)
```

---

---

## 4. LIFECYCLE DOKLADOV (VŠEOBECNÝ KONCEPT)

### 4.1 Princíp

Každý typ dokladu má **vlastný lifecycle** a **špecifické stavy**.

Stavy sú ŠPECIFICKÉ pre každý typ dokladu a sú podrobne popísané v príslušnom dokumente (TSH.md, TSI.md, DF.md, OD.md...).

---

### 4.2 Príklady lifecycles

**Dodávateľské dodacie listy:**
```
draft → received → posted
```

**Dodávateľské faktúry:**
```
draft → confirmed → paid → posted
```

**Odberateľské dodacie listy:**
```
draft → confirmed → shipped → delivered
```

**Objednávky:**
```
draft → confirmed → partially_delivered → delivered → closed
```

---

### 4.3 Kde nájsť detail

**Detail stavov a lifecycle pre konkrétny typ dokladu pozri v:**
- `TSH-supplier_delivery_heads.md` (dodávateľské dodacie listy)
- `DF-supplier_invoice_heads.md` (dodávateľské faktúry)
- `OD-customer_delivery_heads.md` (odberateľské dodacie listy)
- atď.

---

---

## 5. DVOJMENNÁ ARCHITEKTÚRA (AC/FC)

### 5.1 Koncept

Každá hodnota existuje v **dvoch menách**:
- **AC** (Accounting Currency) - Účtovná mena (EUR)
- **FC** (Foreign Currency) - Vyúčtovacia mena (USD, CZK...)

---

### 5.2 Štruktúra

```sql
-- Meny
accounting_currency VARCHAR(3) NOT NULL DEFAULT 'EUR',  -- AC
foreign_currency VARCHAR(3),                            -- FC
foreign_currency_rate DECIMAL(15,6),                    -- Kurz

-- Hodnoty v účtovnej mene (AC)
purchase_base_value_ac DECIMAL(15,2),
purchase_total_value_ac DECIMAL(15,2),

-- Hodnoty vo vyúčtovacej mene (FC)
purchase_base_value_fc DECIMAL(15,2),
purchase_total_value_fc DECIMAL(15,2)
```

---

### 5.3 Validácia

```sql
-- Vyúčtovacia mena len ak je zadaná
CHECK (
    (foreign_currency IS NULL AND foreign_currency_rate IS NULL) OR
    (foreign_currency IS NOT NULL AND foreign_currency_rate IS NOT NULL)
)

-- Hodnoty vo vyúčtovacej mene len ak je mena zadaná
CHECK (
    foreign_currency IS NULL OR
    (purchase_base_value_fc IS NOT NULL AND purchase_total_value_fc IS NOT NULL)
)

-- Kurz meny > 0
CHECK (foreign_currency_rate IS NULL OR foreign_currency_rate > 0)
```

---

### 5.4 Prepočet

```python
def calculate_fc_values(ac_value: Decimal, rate: Decimal) -> Decimal:
    """
    Prepočítaj hodnotu z AC na FC.
    
    Args:
        ac_value: Hodnota v účtovnej mene (EUR)
        rate: Kurz meny (napr. 1.1 pre USD)
    
    Returns:
        Hodnota vo vyúčtovacej mene
    """
    return ac_value * rate

# Príklad
ac_value = Decimal('1000.00')  # EUR
rate = Decimal('1.10')          # USD kurz
fc_value = calculate_fc_values(ac_value, rate)
# fc_value = 1100.00 USD
```

---

---

**See Also:**
- [DOCUMENT_TYPES.md](DOCUMENT_TYPES.md) - Document types
- [../database/DATABASE_PRINCIPLES.md](../database/DATABASE_PRINCIPLES.md) - Database design
