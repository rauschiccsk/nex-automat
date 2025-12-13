# WRILST.BTR → facilities

## 1. PREHĽAD

**Účel:** Číselník prevádzkových jednotiek (facilities) vlastnej firmy.

**Charakteristika:**
- Master data tabuľka pre naše vlastné prevádzky/pobočky
- Každá prevádzkárňa má jedinečné číslo (WriNum)
- Obsahuje úplné kontaktné údaje a nastavenia
- Prepojenie na výrobné prevádzky, sklady, predajne
- Používa sa pri tlači dokumentov (hlavičky faktúr, dodacích listov)

**PostgreSQL tabuľky:**
- `facilities` - jedna tabuľka (1:1 mapping s Btrieve)

**Vzťahy:**
- Súvisí s `stocks` (každý sklad môže patriť prevádzke)
- Používa sa v dokumentoch (faktúry, dodacie listy)
- Kľúčové pre multi-facility operácie

**Btrieve súbor:** `WRILST.BTR`  
**Primárny kľúč:** WriNum (INTEGER)  
**Indexy:** WriNum (unique)

---

## 2. KOMPLEXNÁ SQL SCHÉMA

```sql
-- =====================================================
-- Table: facilities
-- Purpose: Prevádzkové jednotky vlastnej firmy
-- =====================================================

CREATE TABLE facilities (
    -- Primárny kľúč (z Btrieve WriNum)
    facility_id             INTEGER PRIMARY KEY,
    
    -- Základné údaje
    facility_name           VARCHAR(100) NOT NULL,
    facility_code           VARCHAR(20),
    
    -- Adresa (ŠTANDARD - zjednotené)
    street                  VARCHAR(100),
    city                    VARCHAR(100),
    zip_code                VARCHAR(20),
    country_code            VARCHAR(2) DEFAULT 'SK',
    
    -- Kontaktné údaje
    phone                   VARCHAR(30),
    fax                     VARCHAR(30),
    email                   VARCHAR(100),
    web                     VARCHAR(100),
    
    -- Identifikačné čísla
    company_id              VARCHAR(20),        -- IČO
    tax_id                  VARCHAR(20),        -- DIČ
    vat_id                  VARCHAR(20),        -- IČ DPH
    
    -- Bankové spojenie
    bank_account            VARCHAR(34),        -- IBAN
    bank_code               VARCHAR(11),        -- SWIFT/BIC
    
    -- Štatistické údaje
    statistical_number      VARCHAR(20),
    
    -- Príznaky
    is_active               BOOLEAN NOT NULL DEFAULT true,
    is_headquarters         BOOLEAN NOT NULL DEFAULT false,
    is_warehouse            BOOLEAN NOT NULL DEFAULT false,
    is_production           BOOLEAN NOT NULL DEFAULT false,
    is_store                BOOLEAN NOT NULL DEFAULT false,
    
    -- Poznámky
    note                    TEXT,
    
    -- Audit polia (ŠTANDARD - VARCHAR(50))
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by              VARCHAR(50),
    updated_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by              VARCHAR(50)
);

-- Indexy
CREATE INDEX idx_facilities_code ON facilities(facility_code);
CREATE INDEX idx_facilities_name ON facilities(facility_name);
CREATE INDEX idx_facilities_active ON facilities(is_active);

-- Komentáre
COMMENT ON TABLE facilities IS 'Prevádzkové jednotky vlastnej firmy (pobočky, sklady, výrobne)';
COMMENT ON COLUMN facilities.facility_id IS 'ID prevádzky (z Btrieve WriNum)';
COMMENT ON COLUMN facilities.facility_name IS 'Názov prevádzky';
COMMENT ON COLUMN facilities.is_headquarters IS 'Je to centrála/sídlo firmy?';
COMMENT ON COLUMN facilities.is_warehouse IS 'Má funkciu skladu?';
COMMENT ON COLUMN facilities.is_production IS 'Výrobná prevádzka?';
COMMENT ON COLUMN facilities.is_store IS 'Predajňa/obchod?';

-- Trigger pre updated_at
CREATE TRIGGER update_facilities_updated_at
    BEFORE UPDATE ON facilities
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

## 3. MAPPING POLÍ

### Facilities (1:1 mapping)

| Btrieve Pole | Typ Btrieve | PostgreSQL Pole | Typ PostgreSQL | Transformácia | Poznámka |
|--------------|-------------|-----------------|----------------|---------------|----------|
| WriNum | INTEGER | facility_id | INTEGER | Priamo | PK |
| WriNam | STRING[30] | facility_name | VARCHAR(100) | Priamo | **ROZŠÍRENÉ z 30 na 100** |
| WriCod | STRING[20] | facility_code | VARCHAR(20) | Priamo | Voliteľný kód |
| WriAddr | STRING[30] | street | VARCHAR(100) | Priamo | **PREMENOVANÉ + ROZŠÍRENÉ** |
| WriCtn | STRING[3] | city | VARCHAR(100) | Priamo | **PREMENOVANÉ + ROZŠÍRENÉ** |
| WriZip | STRING[15] | zip_code | VARCHAR(20) | Priamo | **ROZŠÍRENÉ na 20** |
| WriCntry | CHAR[2] | country_code | VARCHAR(2) | Priamo | **Zmenené z CHAR na VARCHAR** |
| WriPhone | STRING[30] | phone | VARCHAR(30) | Priamo | |
| WriFax | STRING[30] | fax | VARCHAR(30) | Priamo | |
| WriEmail | STRING[100] | email | VARCHAR(100) | Priamo | |
| WriWeb | STRING[100] | web | VARCHAR(100) | Priamo | |
| WriIco | STRING[20] | company_id | VARCHAR(20) | Priamo | IČO |
| WriDic | STRING[20] | tax_id | VARCHAR(20) | Priamo | DIČ |
| WriIcDph | STRING[20] | vat_id | VARCHAR(20) | Priamo | IČ DPH |
| WriBankAcc | STRING[34] | bank_account | VARCHAR(34) | Priamo | IBAN |
| WriBankCod | STRING[11] | bank_code | VARCHAR(11) | Priamo | SWIFT |
| WriStatNum | STRING[20] | statistical_number | VARCHAR(20) | Priamo | |
| WriActv | BOOLEAN | is_active | BOOLEAN | Priamo | |
| WriHq | BOOLEAN | is_headquarters | BOOLEAN | Priamo | |
| WriWhs | BOOLEAN | is_warehouse | BOOLEAN | Priamo | |
| WriProd | BOOLEAN | is_production | BOOLEAN | Priamo | |
| WriStore | BOOLEAN | is_store | BOOLEAN | Priamo | |
| WriNote | MEMO | note | TEXT | Priamo | |
| WriCrDt | DATE | created_at | TIMESTAMP | Date+Time | Part of timestamp |
| WriCrTm | TIME | created_at | TIMESTAMP | Date+Time | Part of timestamp |
| WriCrUsr | STRING[30] | created_by | VARCHAR(50) | Priamo | **ROZŠÍRENÉ z 30 na 50** |
| WriUpDt | DATE | updated_at | TIMESTAMP | Date+Time | Part of timestamp |
| WriUpTm | TIME | updated_at | TIMESTAMP | Date+Time | Part of timestamp |
| WriUpUsr | STRING[30] | updated_by | VARCHAR(50) | Priamo | **ROZŠÍRENÉ z 30 na 50** |

**Zlúčené polia:**
- `WriCrDt` + `WriCrTm` → `created_at` (TIMESTAMP)
- `WriUpDt` + `WriUpTm` → `updated_at` (TIMESTAMP)

**Premenované polia:**
- `WriAddr` → `street` (unifikácia so štandardom)
- `WriCtn` → `city` (unifikácia so štandardom)

---

## 4. BIZNIS LOGIKA

### Použitie facilities

**1. Tlač dokumentov**
```sql
-- Získanie údajov prevádzky pre hlavičku faktúry
SELECT 
    facility_name,
    street,
    city,
    zip_code,
    company_id,
    tax_id,
    vat_id,
    phone,
    email
FROM facilities
WHERE facility_id = 1  -- Centrála
  AND is_active = true;
```

**2. Multi-facility operácie**
```sql
-- Zoznam všetkých aktívnych skladov
SELECT 
    facility_id,
    facility_name,
    city
FROM facilities
WHERE is_warehouse = true
  AND is_active = true
ORDER BY facility_name;
```

**3. Výrobné prevádzky**
```sql
-- Výrobné jednotky
SELECT 
    facility_id,
    facility_name,
    street,
    city
FROM facilities
WHERE is_production = true
  AND is_active = true;
```

### Pravidlá

1. **Jedinečnosť:**
   - facility_id musí byť jedinečné (PK)
   - facility_code (ak je vyplnený) by mal byť jedinečný

2. **Centrála:**
   - Práve jedna prevádzka má `is_headquarters = true`
   - Táto prevádzka sa používa ako primárna na dokumentoch

3. **Aktivácia/deaktivácia:**
   - Prevádzka sa môže deaktivovať (`is_active = false`)
   - Deaktivovaná prevádzka sa nezobrazuje v zoznamoch
   - História ostává zachovaná

4. **Viaceré funkcie:**
   - Prevádzka môže mať viacero funkcií súčasne
   - Napr. is_warehouse + is_store (sklad a predajňa)

---

## 5. VZŤAHY S INÝMI TABUĽKAMI

```sql
-- Facilities → Stocks (1:N)
-- Každá prevádzka môže mať viacero skladov
ALTER TABLE stocks
ADD CONSTRAINT fk_stocks_facility
FOREIGN KEY (facility_id) 
REFERENCES facilities(facility_id)
ON DELETE RESTRICT;  -- Nemožno zmazať prevádzku so skladmi

-- Facilities → Documents (1:N)
-- Faktúry, dodacie listy vystavené prevádzkou
-- Poznámka: FK sa nepridáva (archívne dokumenty)

-- Facilities → Production_orders (1:N)
-- Výrobné príkazy pre výrobnú prevádzku
-- Poznámka: Bude doplnené pri dokumentácii výroby
```

### Diagram vzťahov

```
facilities (1) ----< (N) stocks
     |
     | (použitie v dokumentoch - bez FK)
     |
     +----< invoices
     +----< delivery_notes
     +----< production_orders
```

---

## 6. VALIDAČNÉ PRAVIDLÁ

```sql
-- CHECK constraints pre facilities
ALTER TABLE facilities
ADD CONSTRAINT chk_facilities_name_not_empty
CHECK (LENGTH(TRIM(facility_name)) > 0);

ALTER TABLE facilities
ADD CONSTRAINT chk_facilities_country_code
CHECK (country_code ~ '^[A-Z]{2}$');  -- 2 veľké písmená

ALTER TABLE facilities
ADD CONSTRAINT chk_facilities_email_format
CHECK (email IS NULL OR email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

ALTER TABLE facilities
ADD CONSTRAINT chk_facilities_one_headquarters
CHECK (
    -- Toto je len ukážka, reálna validácia cez trigger
    is_headquarters = false OR
    (SELECT COUNT(*) FROM facilities WHERE is_headquarters = true) <= 1
);
```

### Trigger pre jedinečnú centrálu

```sql
CREATE OR REPLACE FUNCTION check_single_headquarters()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_headquarters = true THEN
        -- Skontroluj či už existuje iná centrála
        IF EXISTS (
            SELECT 1 FROM facilities 
            WHERE is_headquarters = true 
              AND facility_id != NEW.facility_id
        ) THEN
            RAISE EXCEPTION 'Už existuje centrála (is_headquarters = true)';
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_facilities_single_headquarters
    BEFORE INSERT OR UPDATE ON facilities
    FOR EACH ROW
    EXECUTE FUNCTION check_single_headquarters();
```

---

## 7. QUERY PATTERNS

### Základné queries

```sql
-- 1. Detail prevádzky
SELECT * FROM facilities WHERE facility_id = 1;

-- 2. Zoznam aktívnych prevádzok
SELECT 
    facility_id,
    facility_name,
    city,
    is_warehouse,
    is_production,
    is_store
FROM facilities
WHERE is_active = true
ORDER BY facility_name;

-- 3. Centrála pre tlač dokumentov
SELECT 
    facility_name,
    street,
    city,
    zip_code,
    country_code,
    company_id,
    tax_id,
    vat_id,
    phone,
    email,
    bank_account
FROM facilities
WHERE is_headquarters = true;

-- 4. Sklady (prevádzky so skladom)
SELECT 
    f.facility_id,
    f.facility_name,
    COUNT(s.stock_id) as stock_count
FROM facilities f
LEFT JOIN stocks s ON f.facility_id = s.facility_id
WHERE f.is_warehouse = true
  AND f.is_active = true
GROUP BY f.facility_id, f.facility_name
ORDER BY f.facility_name;

-- 5. Výrobné prevádzky
SELECT 
    facility_id,
    facility_name,
    street,
    city,
    phone
FROM facilities
WHERE is_production = true
  AND is_active = true
ORDER BY facility_name;
```

### Pokročilé queries

```sql
-- 6. Prevádzky s viacerými funkciami
SELECT 
    facility_name,
    CASE 
        WHEN is_warehouse THEN 'Sklad ' 
        ELSE '' 
    END ||
    CASE 
        WHEN is_production THEN 'Výroba ' 
        ELSE '' 
    END ||
    CASE 
        WHEN is_store THEN 'Predajňa' 
        ELSE '' 
    END as functions
FROM facilities
WHERE is_active = true
  AND (is_warehouse OR is_production OR is_store)
ORDER BY facility_name;

-- 7. Audit - posledné zmeny
SELECT 
    facility_id,
    facility_name,
    updated_at,
    updated_by
FROM facilities
WHERE updated_at > CURRENT_TIMESTAMP - INTERVAL '7 days'
ORDER BY updated_at DESC;
```

---

## 8. PRÍKLAD DÁT

```sql
-- Centrála (Komárno)
INSERT INTO facilities (
    facility_id, facility_name, facility_code,
    street, city, zip_code, country_code,
    phone, email, web,
    company_id, tax_id, vat_id,
    bank_account, bank_code,
    is_active, is_headquarters, is_warehouse
) VALUES (
    1, 'ICC Komárno s.r.o. - Centrála', 'HQ',
    'Továrenská 2', 'Komárno', '94501', 'SK',
    '+421 35 123 4567', 'info@icc.sk', 'www.icc.sk',
    '12345678', '1234567890', 'SK1234567890',
    'SK89 7500 0000 0040 0123 4567', 'GIBASKBX',
    true, true, true
);

-- Pobočka Bratislava (sklad + predajňa)
INSERT INTO facilities (
    facility_id, facility_name, facility_code,
    street, city, zip_code, country_code,
    phone, email,
    company_id, tax_id, vat_id,
    is_active, is_headquarters, is_warehouse, is_store
) VALUES (
    2, 'ICC Bratislava - Pobočka', 'BA',
    'Priemyselná 15', 'Bratislava', '82109', 'SK',
    '+421 2 123 4567', 'bratislava@icc.sk',
    '12345678', '1234567890', 'SK1234567890',
    true, false, true, true
);

-- Výrobňa Nitra
INSERT INTO facilities (
    facility_id, facility_name, facility_code,
    street, city, zip_code, country_code,
    phone,
    company_id, tax_id, vat_id,
    is_active, is_headquarters, is_production
) VALUES (
    3, 'ICC Výroba Nitra', 'NR-PROD',
    'Výrobná 8', 'Nitra', '94901', 'SK',
    '+421 37 123 4567',
    '12345678', '1234567890', 'SK1234567890',
    true, false, true
);
```

---

## 9. POZNÁMKY PRE MIGRÁCIU

### Python príklad načítania z Btrieve

```python
from btrieve import Btrieve
import psycopg2
from datetime import datetime

def migrate_facilities():
    # Otvoriť Btrieve súbor
    btr = Btrieve()
    btr.open('WRILST.BTR', 'r')
    
    # Pripojiť sa na PostgreSQL
    conn = psycopg2.connect(
        host="localhost",
        database="nex_automat",
        user="postgres",
        password="password"
    )
    cur = conn.cursor()
    
    # Prechádzať záznamy
    for record in btr:
        # Zlúčenie dátumu a času
        created_at = None
        if record['WriCrDt'] and record['WriCrTm']:
            created_at = datetime.combine(
                record['WriCrDt'], 
                record['WriCrTm']
            )
        
        updated_at = None
        if record['WriUpDt'] and record['WriUpTm']:
            updated_at = datetime.combine(
                record['WriUpDt'], 
                record['WriUpTm']
            )
        
        # INSERT do PostgreSQL
        cur.execute("""
            INSERT INTO facilities (
                facility_id, facility_name, facility_code,
                street, city, zip_code, country_code,
                phone, fax, email, web,
                company_id, tax_id, vat_id,
                bank_account, bank_code, statistical_number,
                is_active, is_headquarters, is_warehouse,
                is_production, is_store,
                note,
                created_at, created_by,
                updated_at, updated_by
            ) VALUES (
                %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s,
                %s,
                %s, %s,
                %s, %s
            )
        """, (
            record['WriNum'], record['WriNam'], record['WriCod'],
            record['WriAddr'], record['WriCtn'], 
            record['WriZip'], record['WriCntry'] or 'SK',
            record['WriPhone'], record['WriFax'], 
            record['WriEmail'], record['WriWeb'],
            record['WriIco'], record['WriDic'], record['WriIcDph'],
            record['WriBankAcc'], record['WriBankCod'], 
            record['WriStatNum'],
            record['WriActv'], record['WriHq'], record['WriWhs'],
            record['WriProd'], record['WriStore'],
            record['WriNote'],
            created_at, record['WriCrUsr'],
            updated_at, record['WriUpUsr']
        ))
    
    conn.commit()
    cur.close()
    conn.close()
    btr.close()
    
    print("Migrácia facilities dokončená!")

if __name__ == '__main__':
    migrate_facilities()
```

### Dôležité upozornenia

1. **Rozšírené polia:**
   - `facility_name`: z VARCHAR(30) na VARCHAR(100)
   - `street`: z VARCHAR(30) na VARCHAR(100)
   - `city`: z VARCHAR(3) na VARCHAR(100)
   - `zip_code`: z VARCHAR(15) na VARCHAR(20)
   - `created_by/updated_by`: z VARCHAR(30) na VARCHAR(50)

2. **Premenované polia:**
   - `WriAddr` → `street` (unifikácia)
   - `WriCtn` → `city` (unifikácia)

3. **Zmeny typov:**
   - `country_code`: z CHAR(2) na VARCHAR(2)

4. **Zlúčené polia:**
   - `WriCrDt` + `WriCrTm` → `created_at`
   - `WriUpDt` + `WriUpTm` → `updated_at`

5. **Defaultné hodnoty:**
   - `country_code`: DEFAULT 'SK'
   - `is_active`: DEFAULT true
   - Ostatné boolean: DEFAULT false

6. **Validácie:**
   - Email vo formáte xxx@yyy.zzz
   - country_code presne 2 veľké písmená
   - facility_name nesmie byť prázdny
   - Len jedna centrála (is_headquarters = true)

---

## 10. VERZIA A ZMENY

| Verzia | Dátum | Autor | Zmeny |
|--------|-------|-------|-------|
| 1.0 | 2025-12-11 | Zoltán + Claude | Prvá verzia dokumentácie |
| 1.1 | 2025-12-11 | Zoltán + Claude | **OPRAVA: Zjednotené so štandardom**<br>- Adresy: street, city, zip_code (rozšírené)<br>- country_code: VARCHAR(2) DEFAULT 'SK'<br>- facility_name: VARCHAR(100)<br>- Audit polia: VARCHAR(50) |

**Status:** ✅ Kompletný a zjednotený so štandardom  
**Session:** 5 (oprava nekonzistencií)  
**Súbor:** `docs/architecture/database/stock/cards/tables/WRILST-facilities.md`