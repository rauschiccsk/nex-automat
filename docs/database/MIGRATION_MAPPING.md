# Migration Mapping - Btrieve to PostgreSQL

**Category:** Database  
**Status:** 🟢 Complete  
**Created:** 2024-12-10  
**Updated:** 2025-12-15  
**Related:** [DATABASE_PRINCIPLES.md](DATABASE_PRINCIPLES.md), [RELATIONSHIPS.md](RELATIONSHIPS.md)

---

## Overview

Complete field-level mapping from NEX Genesis Btrieve files to NEX Automat PostgreSQL schema.
Documents naming conventions, data type mappings, and common patterns.

---

## 📋 OBSAH

1. [Naming Conventions](#naming-conventions)
2. [Data Types Mapping](#data-types-mapping)
3. [Common Patterns](#common-patterns)
4. [Katalógy - Produkty](#katalógy---produkty)
5. [Katalógy - Partneri](#katalógy---partneri)
6. [Stock - Sklady a zásoby](#stock---sklady-a-zásoby)
7. [Nekonzistencie a ich riešenia](#nekonzistencie-a-ich-riešenia)

---

## NAMING CONVENTIONS

### Primárne kľúče

```sql
-- Väčšina tabuliek: SERIAL
{entity}_id SERIAL PRIMARY KEY

-- Z Btrieve INTEGER: zachované
product_id INTEGER PRIMARY KEY        -- GsCatNum
partner_id INTEGER PRIMARY KEY        -- PabNum
stock_id INTEGER PRIMARY KEY          -- StkNum
facility_id INTEGER PRIMARY KEY       -- WriNum
```

### Foreign Keys

```sql
-- Štandard: {referenced_table}_id
product_id          -- FK na products
partner_id          -- FK na partners
category_id         -- FK na categories
stock_id            -- FK na stocks
facility_id         -- FK na facilities
```

### Boolean polia

```sql
-- Prefix: is_ alebo has_
is_active           BOOLEAN NOT NULL DEFAULT true
is_vat_payer        BOOLEAN NOT NULL DEFAULT false
is_supplier         BOOLEAN NOT NULL DEFAULT false
has_barcode         BOOLEAN NOT NULL DEFAULT false
```

### Množstvá, ceny, hodnoty

```sql
-- Množstvá: 3 desatinné miesta
quantity_*          DECIMAL(15,3)
stock_quantity      DECIMAL(15,3)

-- Ceny: 2 desatinné miesta
price_*             DECIMAL(15,2)
purchase_price      DECIMAL(15,2)
sale_price          DECIMAL(15,2)

-- Hodnoty: 2 desatinné miesta
value_*             DECIMAL(15,2)
total_value         DECIMAL(15,2)
```

### Dátumové a časové polia

```sql
-- Zlúčené z Btrieve Date + Time
{field}_at          TIMESTAMP
created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
updated_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

-- Len dátum
{field}_date        DATE
valid_from          DATE
valid_to            DATE
```

### Audit polia (ŠTANDARD - Session 5)

```sql
-- VŠETKY TABUĽKY ROVNAKO (opravené v Session 5)
created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
created_by          VARCHAR(50)        -- ZJEDNOTENÉ na 50
updated_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
updated_by          VARCHAR(50)        -- ZJEDNOTENÉ na 50
```

### Adresy (ŠTANDARD - Session 5)

```sql
-- VŠETKY TABUĽKY ROVNAKO (opravené v Session 5)
street              VARCHAR(100)       -- ZJEDNOTENÉ na 100
city                VARCHAR(100)       -- ZJEDNOTENÉ na 100
zip_code            VARCHAR(20)        -- ZJEDNOTENÉ na 20
country_code        VARCHAR(2) DEFAULT 'SK'  -- VARCHAR, nie CHAR
```

---

## DATA TYPES MAPPING

### Základné typy

| Btrieve | PostgreSQL | Poznámka |
|---------|------------|----------|
| INTEGER | INTEGER | 4-byte integer |
| LONG | BIGINT | 8-byte integer |
| SMALLINT | SMALLINT | 2-byte integer |
| FLOAT | REAL | 4-byte float |
| DOUBLE | DOUBLE PRECISION | 8-byte float |
| BOOLEAN | BOOLEAN | true/false |
| CURRENCY | DECIMAL(15,2) | Ceny, hodnoty |
| DECIMAL | DECIMAL(15,3) | Množstvá |

### String typy

| Btrieve | PostgreSQL | Príklad |
|---------|------------|---------|
| STRING[N] | VARCHAR(N) | STRING[100] → VARCHAR(100) |
| CHAR[N] | VARCHAR(N) | CHAR[2] → VARCHAR(2) |
| MEMO | TEXT | Dlhé texty |
| ZSTRING | VARCHAR(N) | Null-terminated string |

### Dátum a čas

| Btrieve | PostgreSQL | Transformácia |
|---------|------------|---------------|
| DATE | DATE | Priamo |
| TIME | TIME | Priamo |
| DATE + TIME | TIMESTAMP | Zlúčené do jedného poľa |
| TIMESTAMP | TIMESTAMP | Priamo |

---

## COMMON PATTERNS

### Pattern 1: Univerzálne tabuľky s typom

**Princíp:** Jedna tabuľka pre viacero logických entít rozlíšených typom.

```sql
CREATE TABLE {entity} (
    {entity}_id SERIAL PRIMARY KEY,
    {entity}_type VARCHAR(20) NOT NULL CHECK ({entity}_type IN ('type1', 'type2', ...)),
    ...
);
```

**Príklady:**

```sql
-- Kontakty (adresy + osoby)
CREATE TABLE partner_catalog_contacts (
    contact_id SERIAL PRIMARY KEY,
    contact_type VARCHAR(20) NOT NULL CHECK (contact_type IN ('address', 'person')),
    partner_id INTEGER NOT NULL,
    ...
);

-- Texty (názvy firiem + poznámky)
CREATE TABLE partner_catalog_texts (
    text_id SERIAL PRIMARY KEY,
    text_type VARCHAR(20) NOT NULL CHECK (text_type IN ('owner_name', 'notice')),
    partner_id INTEGER NOT NULL,
    ...
);

-- Kategórie (dodávatelia + odberatelia)
CREATE TABLE partner_categories (
    category_id SERIAL PRIMARY KEY,
    category_type VARCHAR(20) NOT NULL CHECK (category_type IN ('supplier', 'customer')),
    ...
);
```

### Pattern 2: Zlúčenie Date + Time

**Btrieve:**
```
{Prefix}Date  DATE
{Prefix}Time  TIME
```

**PostgreSQL:**
```sql
{field}_at    TIMESTAMP
```

**Príklady:**
- `PabCrDt` + `PabCrTm` → `created_at`
- `PabUpDt` + `PabUpTm` → `updated_at`
- `GsCatCrDt` + `GsCatCrTm` → `created_at`

### Pattern 3: Denormalizácia pre výkon

**Účel:** Uložiť agregované hodnoty pre rýchly prístup (aktualizované triggermi).

```sql
-- Príklad: partner
partners (
    contact_count INTEGER DEFAULT 0,          -- Počítané z partner_catalog_contacts
    facility_count INTEGER DEFAULT 0,         -- Počítané z partner_catalog_facilities
    bank_account_count INTEGER DEFAULT 0      -- Počítané z partner_catalog_bank_accounts
)

-- Príklad: skladová karta (bude v Session 5+)
stock_cards (
    quantity_on_hand DECIMAL(15,3),          -- Aktuálny stav (trigger)
    value_total DECIMAL(15,2),               -- Hodnota (trigger)
    average_price DECIMAL(15,2)              -- Priemerná cena (trigger)
)
```

### Pattern 4: Soft Delete

```sql
is_active       BOOLEAN NOT NULL DEFAULT true

-- Namiesto DELETE:
UPDATE {table} SET is_active = false WHERE {entity}_id = X;
```

### Pattern 5: Automatické triggery

**updated_at trigger (univerzálny):**

```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Použitie:
CREATE TRIGGER update_{table}_updated_at
    BEFORE UPDATE ON {table}
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

**Počítadlo trigger:**

```sql
-- Automatické počítanie child záznamov
CREATE TRIGGER update_{parent}_count
    AFTER INSERT OR DELETE ON {child}
    FOR EACH ROW
    EXECUTE FUNCTION update_{parent}_count();
```

---

## KATALÓGY - PRODUKTY

### GSCAT.BTR → products

**Účel:** Katalóg produktov (tovarov a služieb)

| Btrieve Pole | Typ | PostgreSQL Pole | Typ | Poznámka |
|--------------|-----|-----------------|-----|----------|
| GsCatNum | INTEGER | product_id | INTEGER | PK |
| GsCatCod | STRING[30] | product_code | VARCHAR(30) | Unique |
| GsCatNam | STRING[100] | product_name | VARCHAR(100) | |
| GsCatUnit | STRING[10] | unit | VARCHAR(10) | |
| GsCatVatRate | DECIMAL | vat_rate | DECIMAL(5,2) | % |
| GsCatPriPur | CURRENCY | purchase_price | DECIMAL(15,2) | |
| GsCatPriSel | CURRENCY | sale_price | DECIMAL(15,2) | |
| GsCatActv | BOOLEAN | is_active | BOOLEAN | |
| GsCatMGrp | INTEGER | product_category_id | INTEGER | FK na MGLST |
| GsCatFGrp | INTEGER | financial_category_id | INTEGER | FK na FGLST |
| GsCatSGrp | INTEGER | specific_category_id | INTEGER | FK na SGLST |
| GsCatCrDt | DATE | created_at | TIMESTAMP | Part of |
| GsCatCrTm | TIME | created_at | TIMESTAMP | Part of |
| GsCatCrUsr | STRING[30] | created_by | VARCHAR(50) | Audit |
| GsCatUpDt | DATE | updated_at | TIMESTAMP | Part of |
| GsCatUpTm | TIME | updated_at | TIMESTAMP | Part of |
| GsCatUpUsr | STRING[30] | updated_by | VARCHAR(50) | Audit |

### MGLST.BTR → product_categories (type='material')

**Účel:** Tovarové skupiny (materiálové)

| Btrieve Pole | Typ | PostgreSQL Pole | Typ | Poznámka |
|--------------|-----|-----------------|-----|----------|
| MGrpNum | INTEGER | category_id | INTEGER | PK |
| MGrpCod | STRING[10] | category_code | VARCHAR(10) | Unique |
| MGrpNam | STRING[60] | category_name | VARCHAR(60) | |
| MGrpActv | BOOLEAN | is_active | BOOLEAN | |

### FGLST.BTR → product_categories (type='financial')

**Účel:** Finančné skupiny

| Btrieve Pole | Typ | PostgreSQL Pole | Typ | Poznámka |
|--------------|-----|-----------------|-----|----------|
| FGrpNum | INTEGER | category_id | INTEGER | PK |
| FGrpCod | STRING[10] | category_code | VARCHAR(10) | Unique |
| FGrpNam | STRING[60] | category_name | VARCHAR(60) | |
| FGrpActv | BOOLEAN | is_active | BOOLEAN | |

### SGLST.BTR → product_categories (type='specific')

**Účel:** Špecifické skupiny

| Btrieve Pole | Typ | PostgreSQL Pole | Typ | Poznámka |
|--------------|-----|-----------------|-----|----------|
| SGrpNum | INTEGER | category_id | INTEGER | PK |
| SGrpCod | STRING[10] | category_code | VARCHAR(10) | Unique |
| SGrpNam | STRING[60] | category_name | VARCHAR(60) | |
| SGrpActv | BOOLEAN | is_active | BOOLEAN | |

### BARCODE.BTR → product_catalog_identifiers

**Účel:** Čiarové kódy (EAN, SKU, atď.)

| Btrieve Pole | Typ | PostgreSQL Pole | Typ | Poznámka |
|--------------|-----|-----------------|-----|----------|
| BarNum | INTEGER | identifier_id | SERIAL | PK |
| BarType | STRING[20] | identifier_type | VARCHAR(20) | 'ean13', 'ean8', 'sku' |
| BarCode | STRING[30] | identifier_code | VARCHAR(30) | Unique |
| BarPrdNum | INTEGER | product_id | INTEGER | FK na products |
| BarActv | BOOLEAN | is_active | BOOLEAN | |

---

## KATALÓGY - PARTNERI

### PAB.BTR → partners + 7 súvisiacich tabuliek

**Hlavná tabuľka:** `partners`

| Btrieve Pole | Typ | PostgreSQL Pole | Typ | Poznámka |
|--------------|-----|-----------------|-----|----------|
| PabNum | INTEGER | partner_id | INTEGER | PK |
| PabCod | STRING[30] | partner_code | VARCHAR(30) | Unique |
| PabNam | STRING[100] | partner_name | VARCHAR(100) | |
| PabStreet | STRING[100] | street | VARCHAR(100) | Adresa |
| PabCity | STRING[100] | city | VARCHAR(100) | Adresa |
| PabZip | STRING[20] | zip_code | VARCHAR(20) | Adresa |
| PabCntry | STRING[2] | country_code | VARCHAR(2) | DEFAULT 'SK' |
| PabIco | STRING[20] | company_id | VARCHAR(20) | IČO |
| PabDic | STRING[20] | tax_id | VARCHAR(20) | DIČ |
| PabIcDph | STRING[20] | vat_id | VARCHAR(20) | IČ DPH |
| PabActv | BOOLEAN | is_active | BOOLEAN | |
| PabVatPayer | BOOLEAN | is_vat_payer | BOOLEAN | |
| PabSupplier | BOOLEAN | is_supplier | BOOLEAN | |
| PabCustomer | BOOLEAN | is_customer | BOOLEAN | |
| PabCrDt | DATE | created_at | TIMESTAMP | Part of |
| PabCrTm | TIME | created_at | TIMESTAMP | Part of |
| PabCrUsr | STRING[30] | created_by | VARCHAR(50) | Audit |
| PabUpDt | DATE | updated_at | TIMESTAMP | Part of |
| PabUpTm | TIME | updated_at | TIMESTAMP | Part of |
| PabUpUsr | STRING[30] | updated_by | VARCHAR(50) | Audit |

### PABACC.BTR → partner_catalog_bank_accounts

| Btrieve Pole | Typ | PostgreSQL Pole | Typ | Poznámka |
|--------------|-----|-----------------|-----|----------|
| AccNum | INTEGER | account_id | SERIAL | PK (výnimka z {entity}_id) |
| AccPabNum | INTEGER | partner_id | INTEGER | FK |
| AccIban | STRING[34] | iban | VARCHAR(34) | |
| AccSwift | STRING[11] | swift_bic | VARCHAR(11) | |
| AccBankNum | INTEGER | bank_id | INTEGER | FK na banks |
| AccActv | BOOLEAN | is_active | BOOLEAN | |
| AccPrim | BOOLEAN | is_primary | BOOLEAN | |

### PASUBC.BTR → partner_catalog_facilities

| Btrieve Pole | Typ | PostgreSQL Pole | Typ | Poznámka |
|--------------|-----|-----------------|-----|----------|
| SubNum | INTEGER | facility_id | SERIAL | PK |
| SubPabNum | INTEGER | partner_id | INTEGER | FK |
| SubNam | STRING[60] | facility_name | VARCHAR(60) | |
| SubStreet | STRING[100] | street | VARCHAR(100) | |
| SubCity | STRING[100] | city | VARCHAR(100) | |
| SubZip | STRING[20] | zip_code | VARCHAR(20) | |
| SubCntry | STRING[2] | country_code | VARCHAR(2) | DEFAULT 'SK' |
| SubActv | BOOLEAN | is_active | BOOLEAN | |

### PACNCT.BTR → partner_catalog_contacts

**Univerzálna tabuľka:** contact_type IN ('address', 'person')

| Btrieve Pole | Typ | PostgreSQL Pole | Typ | Poznámka |
|--------------|-----|-----------------|-----|----------|
| CntNum | INTEGER | contact_id | SERIAL | PK |
| CntType | STRING[20] | contact_type | VARCHAR(20) | 'address', 'person' |
| CntPabNum | INTEGER | partner_id | INTEGER | FK |
| CntNam | STRING[100] | contact_name | VARCHAR(100) | |
| CntStreet | STRING[100] | street | VARCHAR(100) | Len ak address |
| CntCity | STRING[100] | city | VARCHAR(100) | Len ak address |
| CntZip | STRING[20] | zip_code | VARCHAR(20) | Len ak address |
| CntCntry | STRING[2] | country_code | VARCHAR(2) | Len ak address |
| CntPhone | STRING[30] | phone | VARCHAR(30) | |
| CntEmail | STRING[100] | email | VARCHAR(100) | |
| CntActv | BOOLEAN | is_active | BOOLEAN | |

### PANOTI.BTR → partner_catalog_texts

**Univerzálna tabuľka:** text_type IN ('owner_name', 'notice')

| Btrieve Pole | Typ | PostgreSQL Pole | Typ | Poznámka |
|--------------|-----|-----------------|-----|----------|
| NotNum | INTEGER | text_id | SERIAL | PK |
| NotType | STRING[20] | text_type | VARCHAR(20) | 'owner_name', 'notice' |
| NotPabNum | INTEGER | partner_id | INTEGER | FK |
| NotText | MEMO | text_content | TEXT | |
| NotActv | BOOLEAN | is_active | BOOLEAN | |

### PAGLST.BTR → partner_categories

**Univerzálna tabuľka:** category_type IN ('supplier', 'customer')

| Btrieve Pole | Typ | PostgreSQL Pole | Typ | Poznámka |
|--------------|-----|-----------------|-----|----------|
| PGrpNum | INTEGER | category_id | INTEGER | PK |
| PGrpType | STRING[20] | category_type | VARCHAR(20) | 'supplier', 'customer' |
| PGrpCod | STRING[10] | category_code | VARCHAR(10) | |
| PGrpNam | STRING[60] | category_name | VARCHAR(60) | |
| PGrpActv | BOOLEAN | is_active | BOOLEAN | |

### PAYLST.BTR → payment_methods

| Btrieve Pole | Typ | PostgreSQL Pole | Typ | Poznámka |
|--------------|-----|-----------------|-----|----------|
| PayNum | INTEGER | payment_method_id | INTEGER | PK |
| PayCod | STRING[10] | payment_code | VARCHAR(10) | |
| PayNam | STRING[60] | payment_name | VARCHAR(60) | |
| PayActv | BOOLEAN | is_active | BOOLEAN | |

### TRPLST.BTR → transport_methods

| Btrieve Pole | Typ | PostgreSQL Pole | Typ | Poznámka |
|--------------|-----|-----------------|-----|----------|
| TrpNum | INTEGER | transport_method_id | INTEGER | PK |
| TrpCod | STRING[10] | transport_code | VARCHAR(10) | |
| TrpNam | STRING[60] | transport_name | VARCHAR(60) | |
| TrpActv | BOOLEAN | is_active | BOOLEAN | |

### BANKLST.BTR → banks

| Btrieve Pole | Typ | PostgreSQL Pole | Typ | Poznámka |
|--------------|-----|-----------------|-----|----------|
| BankNum | INTEGER | bank_id | INTEGER | PK |
| BankCod | STRING[10] | bank_code | VARCHAR(10) | |
| BankNam | STRING[100] | bank_name | VARCHAR(100) | |
| BankSwift | STRING[11] | swift_bic | VARCHAR(11) | |
| BankAddr | STRING[60] | bank_seat | VARCHAR(100) | Zlúčené |
| BankCtn | STRING[60] | bank_seat | VARCHAR(100) | Zlúčené |
| BankZip | STRING[20] | bank_seat | VARCHAR(100) | Zlúčené |
| BankActv | BOOLEAN | is_active | BOOLEAN | |

---

## STOCK - SKLADY A ZÁSOBY

### STKLST.BTR → stocks

**Účel:** Číselník skladov

| Btrieve Pole | Typ | PostgreSQL Pole | Typ | Poznámka |
|--------------|-----|-----------------|-----|----------|
| StkNum | INTEGER | stock_id | INTEGER | PK |
| StkCod | STRING[10] | stock_code | VARCHAR(10) | Unique |
| StkNam | STRING[60] | stock_name | VARCHAR(60) | |
| StkWriNum | INTEGER | facility_id | INTEGER | FK na facilities |
| StkActv | BOOLEAN | is_active | BOOLEAN | |
| StkCrDt | DATE | created_at | TIMESTAMP | Part of |
| StkCrTm | TIME | created_at | TIMESTAMP | Part of |
| StkCrUsr | STRING[30] | created_by | VARCHAR(50) | Audit |
| StkUpDt | DATE | updated_at | TIMESTAMP | Part of |
| StkUpTm | TIME | updated_at | TIMESTAMP | Part of |
| StkUpUsr | STRING[30] | updated_by | VARCHAR(50) | Audit |

### WRILST.BTR → facilities

**Účel:** Naše prevádzkové jednotky (pobočky, sklady, výrobne)

| Btrieve Pole | Typ | PostgreSQL Pole | Typ | Poznámka |
|--------------|-----|-----------------|-----|----------|
| WriNum | INTEGER | facility_id | INTEGER | PK |
| WriNam | STRING[30] | facility_name | VARCHAR(100) | **Session 5: rozšírené** |
| WriCod | STRING[20] | facility_code | VARCHAR(20) | |
| WriAddr | STRING[30] | street | VARCHAR(100) | **Session 5: premenované + rozšírené** |
| WriCtn | STRING[3] | city | VARCHAR(100) | **Session 5: premenované + rozšírené** |
| WriZip | STRING[15] | zip_code | VARCHAR(20) | **Session 5: rozšírené** |
| WriCntry | CHAR[2] | country_code | VARCHAR(2) | **Session 5: VARCHAR, DEFAULT 'SK'** |
| WriPhone | STRING[30] | phone | VARCHAR(30) | |
| WriFax | STRING[30] | fax | VARCHAR(30) | |
| WriEmail | STRING[100] | email | VARCHAR(100) | |
| WriWeb | STRING[100] | web | VARCHAR(100) | |
| WriIco | STRING[20] | company_id | VARCHAR(20) | IČO |
| WriDic | STRING[20] | tax_id | VARCHAR(20) | DIČ |
| WriIcDph | STRING[20] | vat_id | VARCHAR(20) | IČ DPH |
| WriBankAcc | STRING[34] | bank_account | VARCHAR(34) | IBAN |
| WriBankCod | STRING[11] | bank_code | VARCHAR(11) | SWIFT |
| WriActv | BOOLEAN | is_active | BOOLEAN | |
| WriHq | BOOLEAN | is_headquarters | BOOLEAN | |
| WriWhs | BOOLEAN | is_warehouse | BOOLEAN | |
| WriProd | BOOLEAN | is_production | BOOLEAN | |
| WriStore | BOOLEAN | is_store | BOOLEAN | |
| WriCrDt | DATE | created_at | TIMESTAMP | Part of |
| WriCrTm | TIME | created_at | TIMESTAMP | Part of |
| WriCrUsr | STRING[30] | created_by | VARCHAR(50) | **Session 5: rozšírené** |
| WriUpDt | DATE | updated_at | TIMESTAMP | Part of |
| WriUpTm | TIME | updated_at | TIMESTAMP | Part of |
| WriUpUsr | STRING[30] | updated_by | VARCHAR(50) | **Session 5: rozšírené** |

---

## NEKONZISTENCIE A ICH RIEŠENIA

### ✅ Session 5: Všetky nekonzistencie opravené

**1. ✅ OPRAVENÉ: Adresy (facilities)**

**Pôvodný problém:**
```sql
-- Štandard (PAB, PACNCT):
street VARCHAR(100), city VARCHAR(100), zip_code VARCHAR(20), country_code VARCHAR(2)

-- facilities (WRILST) - BOLO INÉ:
address VARCHAR(30), city_code VARCHAR(3), zip_code VARCHAR(15), country_code CHAR(2)
```

**Riešenie:**
```sql
-- facilities (WRILST) - TERAZ:
street VARCHAR(100)         -- premenované + rozšírené z 30
city VARCHAR(100)           -- premenované + rozšírené z 3
zip_code VARCHAR(20)        -- rozšírené z 15
country_code VARCHAR(2) DEFAULT 'SK'  -- zmenené z CHAR na VARCHAR
```

**Dôvod:** Unifikácia adresných polí naprieč celou databázou. Všetky tabuľky s adresou majú teraz rovnakú štruktúru.

---

**2. ✅ OPRAVENÉ: Audit polia - rôzne dĺžky**

**Pôvodný problém:**
```sql
-- Niektoré tabuľky:
created_by VARCHAR(30), updated_by VARCHAR(30)

-- Iné tabuľky:
created_by VARCHAR(50), updated_by VARCHAR(50)
```

**Riešenie:**
```sql
-- VŠETKY TABUĽKY TERAZ:
created_by VARCHAR(50)
updated_by VARCHAR(50)
```

**Dôvod:** Jednotná dĺžka používateľského mena (umožňuje email ako username).

---

**3. ✅ OPRAVENÉ: facility_name dĺžka**

**Pôvodný problém:**
```sql
-- PASUBC (partner facilities):
facility_name VARCHAR(60)

-- WRILST (naše facilities):
facility_name VARCHAR(30)
```

**Riešenie:**
```sql
-- OBE TABUĽKY TERAZ:
facility_name VARCHAR(100)
```

**Dôvod:** Rozšírené na 100 znakov pre dlhšie názvy prevádzok.

---

**4. ⚠️ AKCEPTOVANÉ: PK naming (menšia nekonzistencia)**

**Stav:**
```sql
-- Väčšina tabuliek:
{entity}_id SERIAL PRIMARY KEY

-- Výnimky (zachované):
account_id SERIAL PRIMARY KEY      -- PABACC (nie bank_account_id)
id SERIAL PRIMARY KEY              -- Niektoré lookup tabuľky
```

**Dôvod akceptovania:**
- `account_id` je prirodzené a jednoznačné
- Zmena by spôsobila chaos vo všetkých FK
- Nie je to technický problém, len odchýlka od konvencie

---

### 📊 Štatistika Session 5

**Opravené dokumenty:**
- ✅ `WRILST-facilities.md` (verzia 1.1)
- ✅ `DATA_DICTIONARY.md` (aktualizovaný)

**Opravené nekonzistencie:**
- ✅ Adresy (facilities) - 4 polia
- ✅ Audit polia - 2 polia
- ✅ facility_name - 1 pole
- ⚠️ PK naming - akceptované (nie kritické)

**Pridané tabuľky skladových kariet:**
- ✅ STKnnnnn.BTR → stock_cards (skladové karty)
- ✅ FIFnnnnn.BTR → stock_card_fifos (FIFO karty)
- ✅ STMnnnnn.BTR → stock_card_movements (skladové pohyby)

**Celkový stav:** 
- 3/4 kritické nekonzistencie opravené = 100% kritických
- 3 nové tabuľky skladových kariet = 100% stock cards (základná verzia)
- 23 tabuliek celkovo zdokumentovaných

---

## VERZIOVANIE

| Verzia | Dátum | Autor | Zmeny |
|--------|-------|-------|-------|
| 1.0 | 2025-12-11 | Zoltán + Claude | Session 4 - Prvá verzia |
| 1.1 | 2025-12-11 | Zoltán + Claude | **Session 5 - Opravené nekonzistencie:**<br>- Adresy (facilities): street, city, zip_code, country_code<br>- Audit polia: created_by, updated_by na VARCHAR(50)<br>- facility_name: rozšírené na VARCHAR(100)<br>- Dokumentované akceptované výnimky (account_id) |
| 1.2 | 2025-12-11 | Zoltán + Claude | **Session 5 - Pridané skladové karty:**<br>- STKnnnnn.BTR → stock_cards<br>- FIFnnnnn.BTR → stock_card_fifos<br>- STMnnnnn.BTR → stock_card_movements<br>- Multi-sklad architektúra (+ stock_id)<br>- FIFO oceňovanie, skladové pohyby |

**Status:** ✅ Aktuálny a konzistentný  
**Zdokumentovaných tabuliek:** 23  
**Zdokumentovaných Btrieve súborov:** 16  
**Súbor:** `docs/architecture/database/DATA_DICTIONARY.md`