# PASUBC.BTR → partner_catalog_facilities

**Súbor:** PASUBC-partner_catalog_facilities.md  
**Verzia:** 1.0  
**Autor:** Zoltán & Claude  
**Dátum:** 2025-12-11  
**Status:** ✅ Production Ready

---

## 1. PREHĽAD

**Btrieve súbor:** PASUBC.BTR (Partner Subunits Catalog)  
**PostgreSQL tabuľka:** `partner_catalog_facilities`  
**Účel:** Prevádzkové jednotky obchodných partnerov (pobočky, sklady, výdajné miesta).

**Poznámka:** Každý partner môže mať viacero prevádzkových jednotiek s vlastnými adresami, kontaktmi a spôsobom dopravy.

---

## 2. KOMPLEXNÁ SQL SCHÉMA

```sql
CREATE TABLE partner_catalog_facilities (
    -- Primárny kľúč
    facility_id SERIAL PRIMARY KEY,
    
    -- FK na partnera (Btrieve: PaCode)
    partner_id INTEGER NOT NULL REFERENCES partner_catalog(partner_id) ON DELETE CASCADE,
    
    -- Kód prevádzkové jednotky (Btrieve: WpaCode)
    facility_code INTEGER NOT NULL,
    
    -- Názov prevádzkové jednotky (Btrieve: WpaName)
    facility_name VARCHAR(60) NOT NULL,
    
    -- Adresné údaje (Btrieve: WpaAddr, WpaCtn, WpaZip, WpaSta)
    street VARCHAR(30),
    city VARCHAR(30),
    zip_code VARCHAR(15),
    country_code VARCHAR(2) DEFAULT 'SK',
    
    -- Kontaktné údaje (Btrieve: WpaTel, WpaEml)
    phone VARCHAR(20),
    email VARCHAR(30),
    
    -- Spôsob dopravy (Btrieve: TrsCode → FK)
    transport_method_id INTEGER REFERENCES transport_methods(transport_method_id),
    
    -- Aktivita
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Audit polia (Btrieve: CrtUser, CrtDate, CrtTime, ModUser, ModDate, ModTime)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(50),
    
    -- Business constraints
    CONSTRAINT unique_partner_facility UNIQUE (partner_id, facility_code),
    CONSTRAINT check_country_code CHECK (LENGTH(country_code) = 2),
    CONSTRAINT check_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$' OR email IS NULL)
);

-- Indexy pre vyhľadávanie
CREATE INDEX idx_partner_facilities_partner ON partner_catalog_facilities(partner_id);
CREATE INDEX idx_partner_facilities_code ON partner_catalog_facilities(facility_code);
CREATE INDEX idx_partner_facilities_transport ON partner_catalog_facilities(transport_method_id);
CREATE INDEX idx_partner_facilities_active ON partner_catalog_facilities(is_active);

-- Trigger pre updated_at
CREATE TRIGGER update_partner_facilities_updated_at
    BEFORE UPDATE ON partner_catalog_facilities
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger pre aktualizáciu facility_count v partner_catalog
CREATE OR REPLACE FUNCTION update_partner_facility_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE partner_catalog
        SET facility_count = facility_count + 1
        WHERE partner_id = NEW.partner_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE partner_catalog
        SET facility_count = facility_count - 1
        WHERE partner_id = OLD.partner_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_facility_count
    AFTER INSERT OR DELETE ON partner_catalog_facilities
    FOR EACH ROW
    EXECUTE FUNCTION update_partner_facility_count();
```

---

## 3. MAPPING POLÍ

### 3.1 Polia ktoré SA PRENÁŠAJÚ

| Btrieve pole | PostgreSQL pole | Typ transformácie | Poznámka |
|--------------|-----------------|-------------------|----------|
| **Identifikátory** |
| PaCode | partner_id | Lookup | FK na partner_catalog |
| WpaCode | facility_code | Direct | Číslo prevádzkové jednotky |
| WpaName | facility_name | Direct | Názov prevádzkové jednotky |
| **Adresné údaje** |
| WpaAddr | street | Direct | Ulica |
| WpaCtn | city | Direct | Názov mesta |
| WpaZip | zip_code | Direct | PSČ |
| WpaSta | country_code | Direct | Kód štátu (SK, CZ...) |
| **Kontaktné údaje** |
| WpaTel | phone | Direct | Telefónne číslo |
| WpaEml | email | Direct | Email |
| **Spôsob dopravy** |
| TrsCode | transport_method_id | Lookup | FK na transport_methods |
| **Audit údaje** |
| CrtUser | created_by | Direct | Vytvoril užívateľ |
| CrtDate + CrtTime | created_at | Combine | Dátum a čas vytvorenia |
| ModUser | updated_by | Direct | Zmenil užívateľ |
| ModDate + ModTime | updated_at | Combine | Dátum a čas zmeny |

### 3.2 Polia ktoré SA NEPRENÁŠAJÚ

| Btrieve pole | Dôvod neprenášania |
|--------------|--------------------|
| WpaFax | Zastaralý údaj - fax sa už nepoužíva |
| WpaCty | Kód obce - nepotrebný, máme názov mesta (WpaCtn) |
| TrsName | Názov dopravy - je v číselníku transport_methods |
| ModNum | Poradové číslo modifikácie - nie je potrebné |

---

## 4. BIZNIS LOGIKA

### 4.1 Prevádzkové jednotky

**Účel:**
- Pobočky firmy (viaceré predajne, sklady)
- Výdajné miesta
- Rôzne adresy dodania/prevzatia tovaru

**Príklady:**
- Dodávateľ má centrálny sklad + regionálne sklady
- Odberateľ má hlavnú pobočku + pobočky v iných mestách
- Partner má sídlo firmy + výrobné závody

### 4.2 Spôsob dopravy

Každá prevádzkové jednotka môže mať vlastný preferovaný spôsob dopravy:
- Centrála → kuriér (rýchla doprava)
- Sklad → nákladná doprava
- Pobočka → osobný odber

**FK na transport_methods:** Zabezpečuje konzistentný číselník.

### 4.3 Počítadlo v partner_catalog

Automatická aktualizácia cez trigger:
```sql
-- Pri INSERT do partner_catalog_facilities
facility_count = facility_count + 1

-- Pri DELETE z partner_catalog_facilities
facility_count = facility_count - 1
```

---

## 5. VZŤAHY S INÝMI TABUĽKAMI

### 5.1 Incoming (z iných tabuliek)

```
partner_catalog (FK: partner_id)
    ↓
partner_catalog_facilities

transport_methods (FK: transport_method_id)
    ↓
partner_catalog_facilities
```

**ON DELETE CASCADE:** Pri vymazaní partnera sa vymažú všetky jeho prevádzkové jednotky.

**ON DELETE RESTRICT:** Pri vymazaní spôsobu dopravy sa nedovolí, ak sa používa v prevádkových jednotkách.

### 5.2 Outgoing (do iných tabuliek)

```
partner_catalog_facilities
    ↓
invoices, sales_orders, stock_movements... (⚠️ BEZ FK constraints - denormalizované!)
```

**KRITICKÉ:** Archívne dokumenty (faktúry, príjemky, výdajky) nemajú FK constraint na partner_catalog_facilities! Údaje sú snapshot v dokumente (právny požiadavok).

---

## 6. VALIDAČNÉ PRAVIDLÁ

### 6.1 CHECK Constraints

```sql
-- Unique kombinace partner + facility_code
CONSTRAINT unique_partner_facility UNIQUE (partner_id, facility_code)

-- Validácia krajiny (2-znakový kód)
CONSTRAINT check_country_code CHECK (LENGTH(country_code) = 2)

-- Validácia email formátu (ak je zadaný)
CONSTRAINT check_email_format CHECK (
    email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$' 
    OR email IS NULL
)
```

### 6.2 Triggery

**update_partner_facilities_updated_at:**
- Pri každom UPDATE nastaví updated_at na CURRENT_TIMESTAMP

**update_partner_facility_count:**
- Pri INSERT/DELETE aktualizuje počítadlo v partner_catalog

---

## 7. QUERY PATTERNS

### 7.1 Všetky prevádzkové jednotky partnera

```sql
-- Základný SELECT
SELECT 
    f.facility_code,
    f.facility_name,
    f.street,
    f.city,
    f.zip_code,
    f.phone,
    f.email
FROM partner_catalog_facilities f
WHERE f.partner_id = 123
  AND f.is_active = TRUE
ORDER BY f.facility_code;
```

### 7.2 Prevádzkové jednotka s detailom partnera

```sql
-- Facility s názvom partnera
SELECT 
    p.partner_number,
    p.partner_name,
    f.facility_code,
    f.facility_name,
    f.street,
    f.city,
    f.zip_code,
    f.phone
FROM partner_catalog p
JOIN partner_catalog_facilities f ON p.partner_id = f.partner_id
WHERE p.partner_number = '12345'
  AND f.facility_code = 1
  AND f.is_active = TRUE;
```

### 7.3 Prevádzkové jednotky so spôsobom dopravy

```sql
-- Facility s detailom dopravy
SELECT 
    p.partner_name,
    f.facility_code,
    f.facility_name,
    f.city,
    tm.transport_method_code,
    tm.transport_method_name
FROM partner_catalog p
JOIN partner_catalog_facilities f ON p.partner_id = f.partner_id
LEFT JOIN transport_methods tm ON f.transport_method_id = tm.transport_method_id
WHERE p.partner_id = 123
  AND f.is_active = TRUE
ORDER BY f.facility_code;
```

### 7.4 Vyhľadávanie podľa mesta

```sql
-- Všetky facilities v danom meste
SELECT 
    p.partner_name,
    f.facility_name,
    f.street,
    f.zip_code,
    f.phone
FROM partner_catalog_facilities f
JOIN partner_catalog p ON f.partner_id = p.partner_id
WHERE f.city = 'Bratislava'
  AND f.is_active = TRUE
ORDER BY p.partner_name, f.facility_code;
```

### 7.5 Počet prevádzkových jednotiek partnera

```sql
-- Priamy SELECT z počítadla
SELECT 
    partner_number,
    partner_name,
    facility_count
FROM partner_catalog
WHERE partner_number = '12345';

-- Alebo dynamický COUNT
SELECT 
    p.partner_number,
    p.partner_name,
    COUNT(f.facility_id) AS facility_count
FROM partner_catalog p
LEFT JOIN partner_catalog_facilities f ON p.partner_id = f.partner_id
WHERE p.partner_number = '12345'
GROUP BY p.partner_id, p.partner_number, p.partner_name;
```

### 7.6 Kompletný SELECT pre NEX Automat

```sql
-- Kompletné dáta facility pre spracovanie objednávky/faktúry
SELECT 
    -- Partner
    p.partner_id,
    p.partner_number,
    p.partner_name,
    
    -- Facility
    f.facility_id,
    f.facility_code,
    f.facility_name,
    f.street,
    f.city,
    f.zip_code,
    f.country_code,
    f.phone,
    f.email,
    
    -- Spôsob dopravy
    tm.transport_method_code,
    tm.transport_method_name,
    tm.default_transport_price,
    
    -- Audit
    f.created_at,
    f.created_by,
    f.updated_at,
    f.updated_by

FROM partner_catalog p
JOIN partner_catalog_facilities f ON p.partner_id = f.partner_id
LEFT JOIN transport_methods tm ON f.transport_method_id = tm.transport_method_id

WHERE p.partner_number = '12345'
  AND f.facility_code = 1
  AND f.is_active = TRUE;
```

---

## 8. PRÍKLAD DÁT

```sql
-- Pridanie prevádzkových jednotiek pre partnerov

-- ABC Veľkoobchod - centrálny sklad
INSERT INTO partner_catalog_facilities (
    partner_id, facility_code, facility_name,
    street, city, zip_code, country_code,
    phone, email,
    transport_method_id,
    created_by
) VALUES
    (1, 1, 'Centrálny sklad Bratislava',
     'Skladová 10', 'Bratislava', '82101', 'SK',
     '+421 2 5555 1111', 'sklad.ba@abc-vo.sk',
     1,  -- transport_method_id
     'admin'),
     
    (1, 2, 'Regionálny sklad Košice',
     'Priemyselná 25', 'Košice', '04011', 'SK',
     '+421 55 6666 2222', 'sklad.ke@abc-vo.sk',
     2,
     'admin'),
     
    (1, 3, 'Výdajňa Žilina',
     'Obchodná 8', 'Žilina', '01001', 'SK',
     '+421 41 7777 3333', 'vydajna.za@abc-vo.sk',
     3,
     'admin');

-- XYZ Retail - pobočky v mestách
INSERT INTO partner_catalog_facilities (
    partner_id, facility_code, facility_name,
    street, city, zip_code, country_code,
    phone, email,
    transport_method_id,
    created_by
) VALUES
    (2, 1, 'Pobočka Bratislava',
     'Obchodná 15', 'Bratislava', '81101', 'SK',
     '+421 2 8888 4444', 'ba@xyz-retail.sk',
     1,
     'admin'),
     
    (2, 2, 'Pobočka Nitra',
     'Hlavná 30', 'Nitra', '94901', 'SK',
     '+421 37 9999 5555', 'nr@xyz-retail.sk',
     2,
     'admin');

-- Global Trading - hlavný sklad + Czech Republic
INSERT INTO partner_catalog_facilities (
    partner_id, facility_code, facility_name,
    street, city, zip_code, country_code,
    phone, email,
    transport_method_id,
    created_by
) VALUES
    (3, 1, 'Hlavný sklad Žilina',
     'Skladová 100', 'Žilina', '01008', 'SK',
     '+421 41 1111 6666', 'sklad@global-trading.sk',
     1,
     'admin'),
     
    (3, 2, 'Pobočka Praha',
     'Průmyslová 50', 'Praha', '14000', 'CZ',
     '+420 2 2222 7777', 'praha@global-trading.cz',
     2,
     'admin');
```

---

## 9. POZNÁMKY PRE MIGRÁCIU

### 9.1 Poradie migrácie

```
KRITICKÉ: Migrovať v tomto poradí!

1. transport_methods (Btrieve: TRPLST.BTR)    -- FK pre partner_catalog_facilities
2. partner_catalog (Btrieve: PAB00000.BTR)    -- FK pre partner_catalog_facilities
3. partner_catalog_facilities (Btrieve: PASUBC.BTR)  -- TÁTO TABUĽKA
```

### 9.2 Python príklad transformácie

```python
from btrieve import Btrieve
import psycopg2
from datetime import datetime

def migrate_partner_facilities():
    """
    Migrácia prevádzkových jednotiek partnerov z PASUBC.BTR
    """
    # Otvorenie Btrieve súboru
    pasubc = Btrieve('C:/NEX/DATA/PASUBC.BTR')
    
    # Pripojenie na PostgreSQL
    conn = psycopg2.connect("host=localhost dbname=nex_automat user=postgres")
    cur = conn.cursor()
    
    # Spracovanie každého záznamu
    for record in pasubc.records():
        # Lookup partner_id podľa PaCode
        pa_code = record.get('PaCode', 0)
        
        # Najprv nájdeme partner_id z partner_number
        # PaCode v PASUBC môže byť číslo, partner_number môže byť text
        # Treba zistiť presný mapping
        cur.execute("""
            SELECT partner_id FROM partner_catalog
            WHERE partner_number = %s
        """, (str(pa_code),))
        
        result = cur.fetchone()
        if not result:
            print(f"Partner s PaCode={pa_code} neexistuje, preskakujem facility.")
            continue
        
        partner_id = result[0]
        
        # Transformácia spôsobu dopravy (TrsCode → transport_method_id)
        trs_code = record.get('TrsCode', '').strip()
        transport_method_id = None
        
        if trs_code:
            cur.execute("""
                SELECT transport_method_id FROM transport_methods
                WHERE transport_method_code = %s
            """, (trs_code,))
            
            trs_result = cur.fetchone()
            if trs_result:
                transport_method_id = trs_result[0]
        
        # Transformácia audit polí
        crt_date = record.get('CrtDate')  # DateType
        crt_time = record.get('CrtTime')  # TimeType
        
        # Kombinovanie dátumu a času do TIMESTAMP
        if crt_date and crt_time:
            created_at = datetime.combine(crt_date, crt_time)
        else:
            created_at = None
        
        mod_date = record.get('ModDate')
        mod_time = record.get('ModTime')
        
        if mod_date and mod_time:
            updated_at = datetime.combine(mod_date, mod_time)
        else:
            updated_at = None
        
        # INSERT do partner_catalog_facilities
        cur.execute("""
            INSERT INTO partner_catalog_facilities (
                partner_id, facility_code, facility_name,
                street, city, zip_code, country_code,
                phone, email,
                transport_method_id,
                created_at, created_by,
                updated_at, updated_by,
                is_active
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """, (
            partner_id,
            record.get('WpaCode', 0),
            record.get('WpaName', '').strip(),
            record.get('WpaAddr', '').strip() or None,
            record.get('WpaCtn', '').strip() or None,
            record.get('WpaZip', '').strip() or None,
            record.get('WpaSta', 'SK').strip(),
            record.get('WpaTel', '').strip() or None,
            record.get('WpaEml', '').strip() or None,
            transport_method_id,
            created_at,
            record.get('CrtUser', '').strip() or None,
            updated_at,
            record.get('ModUser', '').strip() or None,
            True  # is_active
        ))
        
        print(f"Migrovaná facility: Partner={partner_id}, Code={record.get('WpaCode')}, Name={record.get('WpaName', '').strip()}")
    
    conn.commit()
    cur.close()
    conn.close()
    
    print("Migrácia partner_catalog_facilities dokončená.")

# Spustenie migrácie
if __name__ == '__main__':
    migrate_partner_facilities()
```

### 9.3 Dôležité poznámky

1. **PaCode mapping:**
   - Zistiť presný formát PaCode (longint)
   - Overiť ako sa mapuje na partner_number (VARCHAR)
   - Možno potrebné rozšírené mapovanie cez pomocnú tabuľku

2. **TrsCode → transport_method_id:**
   - LOOKUP cez transport_methods
   - Ak TrsCode neexistuje v číselníku → NULL
   - Validovať všetky kódy pred migráciou

3. **Audit polia:**
   - Kombinovať CrtDate + CrtTime do TIMESTAMP
   - Kombinovať ModDate + ModTime do TIMESTAMP
   - Ak nie sú vyplnené → použiť CURRENT_TIMESTAMP

4. **Trigger automaticky aktualizuje:**
   - `partner_catalog.facility_count` sa aktualizuje cez trigger
   - Niet potreby počítať manuálne

5. **WpaFax NEPRENÁŠAME:**
   - Zastaralý údaj
   - Fax sa už nepoužíva v moderných obchodných systémoch

6. **WpaCty NEPRENÁŠAME:**
   - Kód obce nie je potrebný
   - Máme názov mesta (WpaCtn)

---

## 10. VERZIA A ZMENY

### v1.0 (2025-12-11)
- Prvotná verzia dokumentu
- Komplexná SQL schéma s triggermi
- Mapping polí Btrieve → PostgreSQL
- Query patterns a príklady
- Python migračný script

---

**Koniec dokumentu partner_catalog_facilities.md**