# PAB.BTR + PACNCT.BTR → partner_catalog_contacts

**Súbor:** PACNCT-partner_catalog_contacts.md  
**Verzia:** 1.0  
**Autor:** Zoltán & Claude  
**Dátum:** 2025-12-11  
**Status:** ✅ Production Ready

---

## 1. PREHĽAD

**Btrieve súbory:**
- PAB00000.BTR (Partner Address Book) - kontakty pre adresy
- PACNCT.BTR (Partner Contacts) - kontaktné osoby partnerov

**PostgreSQL tabuľka:** `partner_catalog_contacts`  
**Účel:** Univerzálna tabuľka pre všetky kontaktné údaje partnerov s podporou 2 typov:
- `address` - kontakty viazané na adresu (telefón, email pre sídlo/pobočku)
- `person` - kontaktné osoby partnera (zamestnanci, obchodníci, VIP osoby)

---

## 2. KOMPLEXNÁ SQL SCHÉMA

```sql
CREATE TABLE partner_catalog_contacts (
    -- Primárny kľúč
    contact_id SERIAL PRIMARY KEY,
    
    -- Typ kontaktu
    contact_type VARCHAR(20) NOT NULL,  -- 'address', 'person'
    
    -- FK na adresu (pre contact_type='address')
    address_id INTEGER REFERENCES partner_catalog_addresses(address_id) ON DELETE CASCADE,
    
    -- FK na partnera (pre contact_type='person')
    partner_id INTEGER REFERENCES partner_catalog(partner_id) ON DELETE CASCADE,
    
    -- === POLIA PRE contact_type='address' (z PAB.BTR) ===
    
    -- Kontaktné údaje adresy
    phone VARCHAR(50),
    mobile VARCHAR(50),
    fax VARCHAR(50),
    email VARCHAR(100),
    website VARCHAR(200),
    
    -- Kontaktná osoba (len meno)
    contact_person VARCHAR(100),
    contact_position VARCHAR(100),
    
    -- === POLIA PRE contact_type='person' (z PACNCT.BTR) ===
    
    -- Tituly a meno
    title_before VARCHAR(10),        -- TitulBef
    first_name VARCHAR(15),          -- Meno (z Btrieve LastName!)
    last_name VARCHAR(15),           -- Priezvisko (z Btrieve FirstName!)
    full_name VARCHAR(30),           -- FullName
    title_after VARCHAR(10),         -- TitulAft
    
    -- Funkcia a údaje
    function VARCHAR(30),            -- Function
    sex_mark VARCHAR(1),             -- SexMark (M-muž, W-žena)
    accost VARCHAR(30),              -- Accost (oslovenie)
    
    -- Pracovné kontakty
    work_tel VARCHAR(20),            -- WorkTel
    work_extension VARCHAR(5),       -- WorkSec (klapka)
    work_email VARCHAR(30),          -- WorkEml
    
    -- Mobilné a súkromné kontakty
    mobile_tel VARCHAR(20),          -- MobTel
    private_tel VARCHAR(20),         -- PrivTel
    private_email VARCHAR(30),       -- PrivEml
    
    -- Poznámka
    notice VARCHAR(30),              -- Notice
    
    -- Audit polia
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(50),
    
    -- Business constraints
    CONSTRAINT check_contact_type CHECK (contact_type IN ('address', 'person')),
    CONSTRAINT check_address_fk CHECK (
        (contact_type = 'address' AND address_id IS NOT NULL AND partner_id IS NULL) OR
        (contact_type = 'person' AND partner_id IS NOT NULL AND address_id IS NULL)
    ),
    CONSTRAINT check_sex_mark CHECK (sex_mark IS NULL OR sex_mark IN ('M', 'W')),
    CONSTRAINT check_email_format CHECK (
        email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$' OR email IS NULL
    ),
    CONSTRAINT check_work_email_format CHECK (
        work_email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$' OR work_email IS NULL
    ),
    CONSTRAINT check_private_email_format CHECK (
        private_email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$' OR private_email IS NULL
    )
);

-- Indexy pre vyhľadávanie
CREATE INDEX idx_partner_contacts_type ON partner_catalog_contacts(contact_type);
CREATE INDEX idx_partner_contacts_address ON partner_catalog_contacts(address_id) WHERE contact_type = 'address';
CREATE INDEX idx_partner_contacts_partner ON partner_catalog_contacts(partner_id) WHERE contact_type = 'person';
CREATE INDEX idx_partner_contacts_full_name ON partner_catalog_contacts(full_name) WHERE contact_type = 'person';
CREATE INDEX idx_partner_contacts_work_tel ON partner_catalog_contacts(work_tel) WHERE contact_type = 'person';
CREATE INDEX idx_partner_contacts_mobile_tel ON partner_catalog_contacts(mobile_tel) WHERE contact_type = 'person';
CREATE INDEX idx_partner_contacts_email ON partner_catalog_contacts(email) WHERE contact_type = 'address';
CREATE INDEX idx_partner_contacts_work_email ON partner_catalog_contacts(work_email) WHERE contact_type = 'person';

-- Trigger pre updated_at
CREATE TRIGGER update_partner_contacts_updated_at
    BEFORE UPDATE ON partner_catalog_contacts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

## 3. MAPPING POLÍ

### 3.1 Mapovanie z PAB.BTR (contact_type='address')

| Btrieve pole | PostgreSQL pole | Poznámka |
|--------------|-----------------|----------|
| PABPhone | phone | Telefón |
| PABMobile | mobile | Mobilný telefón |
| PABFax | fax | Fax |
| PABEmail | email | Email |
| PABWww | website | Web stránka |
| PABContact | contact_person | Meno kontaktu |
| PABPosition | contact_position | Funkcia |
| - | contact_type | Fixed: 'address' |
| - | address_id | FK z PAB adresy |

### 3.2 Mapovanie z PACNCT.BTR (contact_type='person')

| Btrieve pole | PostgreSQL pole | Poznámka |
|--------------|-----------------|----------|
| **Identifikátor** |
| PaCode | partner_id | FK na partner_catalog |
| - | contact_type | Fixed: 'person' |
| **Meno a tituly** |
| TitulBef | title_before | Titul pred menom |
| FirstName | last_name | Priezvisko (SWAP!) |
| LastName | first_name | Meno (SWAP!) |
| FullName | full_name | Plné meno |
| TitulAft | title_after | Titul za menom |
| **Funkcia a údaje** |
| Function | function | Funkcia |
| SexMark | sex_mark | M/W |
| Accost | accost | Oslovenie |
| **Pracovné kontakty** |
| WorkTel | work_tel | Pracovný telefón |
| WorkSec | work_extension | Klapka |
| WorkEml | work_email | Pracovný email |
| **Mobilné a súkromné** |
| MobTel | mobile_tel | Mobilný telefón |
| PrivTel | private_tel | Súkromný telefón |
| PrivEml | private_email | Súkromný email |
| **Poznámka** |
| Notice | notice | Poznámka |
| **Audit** |
| CrtUser | created_by | Vytvoril |
| CrtDate + CrtTime | created_at | Dátum a čas vytvorenia |
| ModUser | updated_by | Zmenil |
| ModDate + ModTime | updated_at | Dátum a čas zmeny |

### 3.3 Polia ktoré SA NEPRENÁŠAJÚ

| Btrieve pole | Dôvod neprenášania |
|--------------|--------------------|
| PaName, _PaName | Názov partnera - máme cez FK partner_id |
| _FullName | Vyhľadávacie pole - PostgreSQL má ILIKE |
| RsdAddr, RsdCtc, RsdCtn, RsdZip | Adresa trvalého pobytu - už nepoužívame |
| RsdStc, RsdStn | Štát trvalého pobytu - už nepoužívame |
| WorkFax, PrivFax | Fax - zastaralý údaj |
| IdnType, IdnCard | Doklad totožnosti - GDPR citlivé údaje |
| BrtDate, BrtPlac | Dátum a miesto narodenia - GDPR citlivé |
| Citizen | Občianstvo - GDPR citlivé |
| MidName | Druhé krstné meno - nepoužívané |
| VisNum, VisType | Číselník hostí pre HRS - nepoužívané |
| ModNum | Číslo modifikácie - nie je potrebné |

---

## 4. BIZNIS LOGIKA

### 4.1 Typy kontaktov

**contact_type='address'**
- Kontakty viazané na ADRESU partnera
- Telefón, email, web pre sídlo/korešpondenčnú/fakturačnú adresu
- Jednoduchá kontaktná osoba (len meno a funkcia)
- **FK:** address_id NOT NULL, partner_id NULL

**contact_type='person'**
- Konkrétne OSOBY pracujúce pre partnera
- Zamestnanci, obchodníci, konateľia, VIP osoby
- Detailné údaje (tituly, funkcia, oslovenie, pracovné aj súkromné kontakty)
- **FK:** partner_id NOT NULL, address_id NULL

### 4.2 FirstName vs LastName - SWAP pri migrácii!

**V NEX Genesis PACNCT.BTR je to OPAČNE:**
- `FirstName` = priezvisko (Nový)
- `LastName` = meno (Ján)
- `FullName` = "Ing. Ján Nový, PhD."

**V NEX Automat PostgreSQL je to SPRÁVNE:**
- `first_name` = meno (Ján)
- `last_name` = priezvisko (Nový)
- `full_name` = kompletné meno s titulmi

**Pri migrácii SWAPUJEME:**
- Btrieve FirstName → PostgreSQL `last_name`
- Btrieve LastName → PostgreSQL `first_name`

### 4.3 CHECK Constraints - FK validácia

```sql
CONSTRAINT check_address_fk CHECK (
    (contact_type = 'address' AND address_id IS NOT NULL AND partner_id IS NULL) OR
    (contact_type = 'person' AND partner_id IS NOT NULL AND address_id IS NULL)
)
```

**Zabezpečuje:**
- 'address' → address_id povinné, partner_id NULL
- 'person' → partner_id povinné, address_id NULL

---

## 5. VZŤAHY S INÝMI TABUĽKAMI

### 5.1 Incoming (z iných tabuliek)

```
partner_catalog_addresses (FK: address_id pre contact_type='address')
    ↓
partner_catalog_contacts

partner_catalog (FK: partner_id pre contact_type='person')
    ↓
partner_catalog_contacts
```

**ON DELETE CASCADE:**
- Pri vymazaní adresy sa vymažú jej kontakty
- Pri vymazaní partnera sa vymažú jeho kontaktné osoby

### 5.2 Outgoing (do iných tabuliek)

**Žiadne** - toto je dátová tabuľka.

---

## 6. VALIDAČNÉ PRAVIDLÁ

### 6.1 CHECK Constraints

```sql
-- Povolené typy kontaktov
CONSTRAINT check_contact_type CHECK (contact_type IN ('address', 'person'))

-- Validácia FK podľa typu
CONSTRAINT check_address_fk CHECK (
    (contact_type = 'address' AND address_id IS NOT NULL AND partner_id IS NULL) OR
    (contact_type = 'person' AND partner_id IS NOT NULL AND address_id IS NULL)
)

-- Pohlavie (ak je zadané)
CONSTRAINT check_sex_mark CHECK (sex_mark IS NULL OR sex_mark IN ('M', 'W'))

-- Email formáty
CONSTRAINT check_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$' OR email IS NULL)
CONSTRAINT check_work_email_format CHECK (work_email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$' OR work_email IS NULL)
CONSTRAINT check_private_email_format CHECK (private_email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$' OR private_email IS NULL)
```

### 6.2 Povinné polia

```sql
contact_type NOT NULL
address_id OR partner_id NOT NULL (podľa contact_type)
```

---

## 7. QUERY PATTERNS

### 7.1 Kontakty pre adresu (contact_type='address')

```sql
-- Kontakty pre sídlo partnera
SELECT 
    pc.phone,
    pc.email,
    pc.contact_person,
    pc.contact_position
FROM partner_catalog_addresses pa
LEFT JOIN partner_catalog_contacts pc 
    ON pa.address_id = pc.address_id 
    AND pc.contact_type = 'address'
WHERE pa.partner_id = 123
  AND pa.address_type = 'registered';
```

### 7.2 Kontaktné osoby partnera (contact_type='person')

```sql
-- Všetky kontaktné osoby partnera
SELECT 
    full_name,
    function,
    work_tel,
    work_email,
    mobile_tel
FROM partner_catalog_contacts
WHERE partner_id = 123
  AND contact_type = 'person'
ORDER BY full_name;
```

### 7.3 Vyhľadávanie kontaktnej osoby

```sql
-- Vyhľadanie osoby podľa mena
SELECT 
    p.partner_name,
    pc.full_name,
    pc.function,
    pc.work_tel,
    pc.work_email
FROM partner_catalog_contacts pc
JOIN partner_catalog p ON pc.partner_id = p.partner_id
WHERE pc.contact_type = 'person'
  AND pc.full_name ILIKE '%Nový%'
ORDER BY p.partner_name, pc.full_name;
```

### 7.4 Vyhľadávanie podľa telefónu

```sql
-- Nájsť kontaktnú osobu podľa telefónu
SELECT 
    p.partner_name,
    pc.full_name,
    pc.function,
    pc.work_tel,
    pc.mobile_tel
FROM partner_catalog_contacts pc
JOIN partner_catalog p ON pc.partner_id = p.partner_id
WHERE pc.contact_type = 'person'
  AND (pc.work_tel = '+421905123456' 
       OR pc.mobile_tel = '+421905123456')
LIMIT 1;
```

### 7.5 Komplexný SELECT pre partnera

```sql
-- Partner s adresami a kontaktmi
SELECT 
    p.partner_number,
    p.partner_name,
    
    -- Adresa
    pa.address_type,
    pa.street,
    pa.city,
    
    -- Kontakt pre adresu
    pc_addr.phone AS address_phone,
    pc_addr.email AS address_email,
    
    -- Kontaktné osoby
    pc_pers.full_name AS contact_person,
    pc_pers.function AS person_function,
    pc_pers.work_tel AS person_work_tel,
    pc_pers.work_email AS person_work_email

FROM partner_catalog p
LEFT JOIN partner_catalog_addresses pa ON p.partner_id = pa.partner_id
LEFT JOIN partner_catalog_contacts pc_addr 
    ON pa.address_id = pc_addr.address_id 
    AND pc_addr.contact_type = 'address'
LEFT JOIN partner_catalog_contacts pc_pers 
    ON p.partner_id = pc_pers.partner_id 
    AND pc_pers.contact_type = 'person'

WHERE p.partner_number = '12345'
ORDER BY pa.address_type, pc_pers.full_name;
```

---

## 8. PRÍKLAD DÁT

### 8.1 Kontakty pre adresy (contact_type='address')

```sql
-- Kontakty pre sídlo partnera ABC Veľkoobchod
INSERT INTO partner_catalog_contacts (
    contact_type, address_id,
    phone, mobile, fax, email, website,
    contact_person, contact_position,
    created_by
) VALUES
    ('address', 1,  -- sídlo
     '+421 2 1234 5678', '+421 905 123 456', '+421 2 1234 5679', 
     'info@abc-vo.sk', 'www.abc-vo.sk',
     'Ján Nový', 'Obchodný riaditeľ',
     'migration'),
     
    ('address', 2,  -- korešpondenčná adresa
     '+421 2 9876 5432', NULL, NULL,
     'office@abc-vo.sk', NULL,
     'Mária Nováková', 'Asistentka',
     'migration');
```

### 8.2 Kontaktné osoby (contact_type='person')

```sql
-- Kontaktné osoby partnera ABC Veľkoobchod
INSERT INTO partner_catalog_contacts (
    contact_type, partner_id,
    title_before, first_name, last_name, full_name, title_after,
    function, sex_mark, accost,
    work_tel, work_extension, work_email,
    mobile_tel, private_tel, private_email,
    notice,
    created_by
) VALUES
    ('person', 1,
     'Ing.', 'Nový', 'Ján', 'Ing. Ján Nový', NULL,
     'Konateľ spoločnosti', 'M', 'pán Nový',
     '+421 2 1234 5678', '101', 'jan.novy@abc-vo.sk',
     '+421 905 123 456', NULL, 'jan.novy@gmail.com',
     'VIP - priamy kontakt na konateľa',
     'migration'),
     
    ('person', 1,
     'Mgr.', 'Nováková', 'Mária', 'Mgr. Mária Nováková', NULL,
     'Obchodná manažérka', 'W', 'pani Nováková',
     '+421 2 1234 5679', '102', 'maria.novakova@abc-vo.sk',
     '+421 905 234 567', NULL, NULL,
     'Zodpovedná za zákazníkov v BA regióne',
     'migration'),
     
    ('person', 1,
     NULL, 'Horný', 'Peter', 'Peter Horný', NULL,
     'Vedúci skladu', 'M', 'pán Horný',
     '+421 2 1234 5680', '201', 'peter.horny@abc-vo.sk',
     '+421 905 345 678', NULL, NULL,
     'Kontakt pre dodávky a výdaj tovaru',
     'migration');
```

---

## 9. POZNÁMKY PRE MIGRÁCIU

### 9.1 Poradie migrácie

```
KRITICKÉ: Migrovať v tomto poradí!

1. partner_catalog (Btrieve: PAB00000.BTR)           -- Hlavná tabuľka
2. partner_catalog_addresses (Btrieve: PAB00000.BTR) -- Adresy
3. partner_catalog_contacts                          -- TÁTO TABUĽKA
   a) contact_type='address' z PAB00000.BTR
   b) contact_type='person' z PACNCT.BTR
```

### 9.2 Python príklad transformácie

```python
from btrieve import Btrieve
import psycopg2
from datetime import datetime

def migrate_address_contacts():
    """
    Migrácia kontaktov pre adresy z PAB00000.BTR
    """
    pab = Btrieve('C:/NEX/DATA/PAB00000.BTR')
    conn = psycopg2.connect("host=localhost dbname=nex_automat user=postgres")
    cur = conn.cursor()
    
    print("Migrácia PAB.BTR → partner_catalog_contacts (address)")
    
    for record in pab.records():
        # Lookup partner_id
        partner_number = str(record.get('PABNr', 0))
        
        cur.execute("""
            SELECT partner_id FROM partner_catalog
            WHERE partner_number = %s
        """, (partner_number,))
        
        result = cur.fetchone()
        if not result:
            continue
        
        partner_id = result[0]
        
        # Získať address_id pre registered adresu
        cur.execute("""
            SELECT address_id FROM partner_catalog_addresses
            WHERE partner_id = %s AND address_type = 'registered'
        """, (partner_id,))
        
        addr_result = cur.fetchone()
        if not addr_result:
            continue
        
        address_id = addr_result[0]
        
        # INSERT kontaktu pre adresu
        cur.execute("""
            INSERT INTO partner_catalog_contacts (
                contact_type, address_id,
                phone, fax, email, website,
                contact_person,
                created_by, updated_by
            ) VALUES (
                'address', %s, %s, %s, %s, %s, %s, 'migration', 'migration'
            )
            ON CONFLICT DO NOTHING
        """, (
            address_id,
            record.get('PABPhone', '').strip() or None,
            record.get('PABFax', '').strip() or None,
            record.get('PABEmail', '').strip() or None,
            record.get('PABWww', '').strip() or None,
            record.get('PABContact', '').strip() or None
        ))
        
        print(f"Partner {partner_number}: address contact migrated")
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Migrácia address contacts dokončená")

def migrate_person_contacts():
    """
    Migrácia kontaktných osôb z PACNCT.BTR
    """
    pacnct = Btrieve('C:/NEX/DATA/PACNCT.BTR')
    conn = psycopg2.connect("host=localhost dbname=nex_automat user=postgres")
    cur = conn.cursor()
    
    print("Migrácia PACNCT.BTR → partner_catalog_contacts (person)")
    
    for record in pacnct.records():
        # Lookup partner_id
        pa_code = record.get('PaCode', 0)
        partner_number = str(pa_code)
        
        cur.execute("""
            SELECT partner_id FROM partner_catalog
            WHERE partner_number = %s
        """, (partner_number,))
        
        result = cur.fetchone()
        if not result:
            print(f"Partner {partner_number} neexistuje, preskakujem.")
            continue
        
        partner_id = result[0]
        
        # Audit údaje
        crt_user = record.get('CrtUser', '').strip() or 'migration'
        crt_date = record.get('CrtDate')
        crt_time = record.get('CrtTime')
        
        if crt_date and crt_time:
            created_at = datetime.combine(crt_date, crt_time)
        else:
            created_at = None
        
        mod_user = record.get('ModUser', '').strip() or 'migration'
        mod_date = record.get('ModDate')
        mod_time = record.get('ModTime')
        
        if mod_date and mod_time:
            updated_at = datetime.combine(mod_date, mod_time)
        else:
            updated_at = None
        
        # INSERT kontaktnej osoby
        cur.execute("""
            INSERT INTO partner_catalog_contacts (
                contact_type, partner_id,
                title_before, first_name, last_name, full_name, title_after,
                function, sex_mark, accost,
                work_tel, work_extension, work_email,
                mobile_tel, private_tel, private_email,
                notice,
                created_at, created_by,
                updated_at, updated_by
            ) VALUES (
                'person', %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
        """, (
            partner_id,
            record.get('TitulBef', '').strip() or None,
            record.get('LastName', '').strip() or None,   # ← SWAP: LastName = meno
            record.get('FirstName', '').strip() or None,  # ← SWAP: FirstName = priezvisko
            record.get('FullName', '').strip() or None,
            record.get('TitulAft', '').strip() or None,
            record.get('Function', '').strip() or None,
            record.get('SexMark', '').strip() or None,
            record.get('Accost', '').strip() or None,
            record.get('WorkTel', '').strip() or None,
            record.get('WorkSec', '').strip() or None,
            record.get('WorkEml', '').strip() or None,
            record.get('MobTel', '').strip() or None,
            record.get('PrivTel', '').strip() or None,
            record.get('PrivEml', '').strip() or None,
            record.get('Notice', '').strip() or None,
            created_at or datetime.now(),
            crt_user,
            updated_at or datetime.now(),
            mod_user
        ))
        
        full_name = record.get('FullName', '').strip()
        print(f"Partner {partner_number}: person contact {full_name} migrated")
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Migrácia person contacts dokončená")

# Spustenie migrácie
if __name__ == '__main__':
    # Krok 1: Kontakty pre adresy z PAB.BTR
    migrate_address_contacts()
    
    # Krok 2: Kontaktné osoby z PACNCT.BTR
    migrate_person_contacts()
```

### 9.3 Dôležité poznámky

1. **contact_type validácia:**
   - CHECK constraint zabezpečuje správne FK
   - 'address' → address_id povinné
   - 'person' → partner_id povinné

2. **FirstName vs LastName - SWAP!:**
   - V Btrieve je to OPAČNE!
   - Btrieve FirstName = priezvisko → PostgreSQL `last_name`
   - Btrieve LastName = meno → PostgreSQL `first_name`
   - V Python scripte: `record.get('LastName')` → `first_name`
   - V Python scripte: `record.get('FirstName')` → `last_name`

3. **GDPR citlivé údaje NEPRENÁŠAME:**
   - Adresa trvalého pobytu
   - Doklady totožnosti
   - Dátum narodenia
   - Občianstvo

4. **Zastaralé údaje NEPRENÁŠAME:**
   - Fax čísla
   - VisNum, VisType (HRS systém)

5. **PaName NEPRENÁŠAME:**
   - Je to názov partnera
   - Máme cez FK partner_id

6. **Vyhľadávacie polia (_PaName, _FullName):**
   - V Btrieve pre case-insensitive search
   - PostgreSQL: `WHERE full_name ILIKE '%xyz%'`

---

## 10. SÚVISIACE DOKUMENTY

- **partner_catalog** → `PAB-partner_catalog.md`
- **partner_catalog_addresses** → `PAB-partner_catalog.md`

---

## 11. VERZIA A ZMENY

### v1.0 (2025-12-11)
- Prvotná verzia dokumentu
- Univerzálna tabuľka s contact_type ('address', 'person')
- Mapping z PAB.BTR a PACNCT.BTR
- Query patterns a príklady
- Python migračný script

---

**Koniec dokumentu PACNCT-partner_catalog_contacts.md**