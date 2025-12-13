# BANKLST.BTR → bank_catalog

**Kategória:** Catalogs - Číselníky  
**NEX Genesis:** BANKLST.BTR  
**NEX Automat:** `bank_catalog`  
**Vytvorené:** 2025-12-10  
**Status:** ✅ Pripravené na review

---

## PREHĽAD

### Historický vývoj

**NEX Genesis (Btrieve):**
- BANKLST.BTR = číselník bankových ústavov
- Identifikácia len cez textový kód (BankCode: "1100", "0200"...)
- Slovenský smerovací kód banky

**NEX Automat (PostgreSQL):**
- **bank_catalog** - číselník bánk
- Pridané numerické ID (bank_id) pre konzistenciu
- Zachovaný BankCode pre kompatibilitu

**Účel:**
- Číselník slovenských a zahraničných bánk
- Referencované z partner_catalog_bank_accounts
- Použité pri platobných transakciách

---

## KOMPLEXNÁ SQL SCHÉMA

### bank_catalog

**Tabuľka:** `bank_catalog`  
**Popis:** Číselník bankových ústavov

```sql
CREATE TABLE bank_catalog (
    bank_id SERIAL PRIMARY KEY,
    
    -- Základné údaje
    bank_code VARCHAR(20) UNIQUE NOT NULL,
    bank_name VARCHAR(100) NOT NULL,
    
    -- Adresa banky (komplexná)
    bank_seat VARCHAR(100),
    
    -- Registračné údaje
    bank_tax_id VARCHAR(20),
    
    -- Príznaky
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Audit záznamu
    created_by VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(30),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_bank_catalog_code ON bank_catalog(bank_code);
CREATE INDEX idx_bank_catalog_name ON bank_catalog(bank_name);
CREATE INDEX idx_bank_catalog_active ON bank_catalog(is_active) WHERE is_active = TRUE;

-- Trigger pre automatickú aktualizáciu updated_at
CREATE TRIGGER update_bank_catalog_updated_at
    BEFORE UPDATE ON bank_catalog
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

## MAPPING POLÍ

### Polia ktoré SA PRENÁŠAJÚ

| Btrieve Field | Typ | → | PostgreSQL Column | Typ | Popis |
|---------------|-----|---|-------------------|-----|-------|
| - | - | → | bank_id | SERIAL | **NOVÉ!** Numerické ID (1, 2, 3...) |
| BankCode | Str15 | → | bank_code | VARCHAR(20) | Smerovací kód banky |
| BankName | Str30 | → | bank_name | VARCHAR(100) | Názov banky |
| BankAddr + BankCtn + BankZip | Str30+Str30+Str15 | → | bank_seat | VARCHAR(100) | Komplexná adresa banky |
| BankIno | Str15 | → | bank_tax_id | VARCHAR(20) | IČO banky |
| CrtUser | Str8 | → | created_by | VARCHAR(30) | Vytvoril užívateľ |
| CrtDate, CrtTime | Date+Time | → | created_at | TIMESTAMP | Dátum vytvorenia |
| ModUser | Str8 | → | updated_by | VARCHAR(30) | Upravil užívateľ |
| ModDate, ModTime | Date+Time | → | updated_at | TIMESTAMP | Dátum úpravy |

### Polia ktoré SA NEPRENÁŠAJÚ

| Btrieve Field | Typ | Dôvod neprenášania |
|---------------|-----|--------------------|
| _BankName | Str15 | Vyhľadávacie pole - PostgreSQL full-text search |
| IbanCode | Str34 | IBAN banky - nevyužíva sa |
| SwftCode | Str20 | SWIFT banky - nevyužíva sa |
| ModNum | word | Verzia záznamu - PostgreSQL má to automaticky |

---

## BIZNIS LOGIKA

### 1. Numerické ID vs textový kód

**NOVÉ v NEX Automat:**
```sql
bank_id SERIAL PRIMARY KEY  -- 1, 2, 3, 4...
```

**Prečo:**
- Konzistentný spôsob referencovania (FK)
- Rýchlejšie JOIN operácie (INTEGER vs VARCHAR)
- Možnosť zmeny kódu bez ovplyvnenia FK

**BankCode zostáva:**
- Pre ľudskú čitateľnosť
- Pre import/export
- Pre kompatibilitu so slovenským bankovým systémom

### 2. Slovenské bankové kódy

**Formát:** 4-miestny kód

| Kód | Názov banky |
|-----|-------------|
| 1100 | TATRA BANKA a.s. |
| 0200 | Všeobecná úverová banka a.s. |
| 5600 | Prima banka Slovensko a.s. |
| 0900 | Slovenská sporiteľňa a.s. |
| 3100 | Poštová banka a.s. |
| 6500 | ČSOB a.s. |
| 7500 | Československá obchodná banka a.s. |

### 3. Použitie v partner_catalog_bank_accounts

```sql
-- Bankový účet partnera
-- Poznámka: bank_catalog je VOLITEĽNÝ - FK môže byť NULL
partner_catalog_bank_accounts.bank_id → bank_catalog.bank_id (nullable)
```

**Prečo nullable:**
- Partner môže mať zahraniční bankový účet (IBAN)
- Banka nemusí byť v našom číselníku
- IBAN je unikátny identifikátor účtu

---

## VZŤAHY S INÝMI TABUĽKAMI

### bank_catalog ← partner_catalog_bank_accounts

```sql
-- Partneri s účtom v Tatra banke
SELECT 
    pc.partner_name,
    pba.iban,
    bc.bank_name,
    bc.bank_code
FROM partner_catalog pc
INNER JOIN partner_catalog_bank_accounts pba ON pc.partner_id = pba.partner_id
LEFT JOIN bank_catalog bc ON pba.bank_id = bc.bank_id
WHERE bc.bank_code = '1100';
```

### Účty bez bankového číselníka

```sql
-- Partneri so zahraničným účtom (bez bank_id)
SELECT 
    pc.partner_name,
    pba.iban,
    pba.bank_name AS custom_bank_name
FROM partner_catalog pc
INNER JOIN partner_catalog_bank_accounts pba ON pc.partner_id = pba.partner_id
WHERE pba.bank_id IS NULL;
```

---

## VALIDAČNÉ PRAVIDLÁ

### 1. Unikátny kód

```sql
bank_code VARCHAR(20) UNIQUE NOT NULL
```

### 2. Povinné polia

```sql
bank_code NOT NULL
bank_name NOT NULL
```

---

## QUERY PATTERNS

### Zoznam aktívnych bánk

```sql
SELECT 
    bank_id,
    bank_code,
    bank_name,
    bank_seat
FROM bank_catalog
WHERE is_active = TRUE
ORDER BY bank_name;
```

### Získať bank_id z kódu

```sql
-- Pri migrácii: BankCode → bank_id
SELECT bank_id 
FROM bank_catalog 
WHERE bank_code = '1100';
```

### Štatistika použitia bánk

```sql
SELECT 
    bc.bank_name,
    bc.bank_code,
    COUNT(pba.id) AS account_count,
    COUNT(DISTINCT pba.partner_id) AS partner_count
FROM bank_catalog bc
LEFT JOIN partner_catalog_bank_accounts pba ON bc.bank_id = pba.bank_id
GROUP BY bc.bank_name, bc.bank_code
ORDER BY account_count DESC;
```

### Vyhľadanie banky podľa názvu

```sql
SELECT 
    bank_id,
    bank_code,
    bank_name
FROM bank_catalog
WHERE bank_name ILIKE '%tatra%'
  AND is_active = TRUE;
```

---

## PRÍKLAD DÁT

```sql
INSERT INTO bank_catalog (bank_code, bank_name, bank_seat, bank_tax_id, created_by) VALUES
('1100', 'TATRA BANKA a.s.', 'Hodžovo námestie 3, Bratislava, 81106', '00686930', 'admin'),
('0200', 'Všeobecná úverová banka a.s.', 'Mlynské Nivy 1, Bratislava, 82990', '31320155', 'admin'),
('5600', 'Prima banka Slovensko a.s.', 'Hodžova 11, Žilina, 01001', '31575951', 'admin'),
('0900', 'Slovenská sporiteľňa a.s.', 'Tomášikova 48, Bratislava, 83206', '00151653', 'admin'),
('3100', 'Poštová banka a.s.', 'Dvořákovo nábrežie 4, Bratislava, 81102', '31340890', 'admin'),
('6500', 'ČSOB a.s.', 'Michalská 18, Bratislava, 81585', '36854', 'admin'),
('7500', 'Československá obchodná banka a.s.', 'Michalská 18, Bratislava, 81585', '36854', 'admin'),
('8330', 'UniCredit Bank Czech Republic and Slovakia a.s.', 'Šancová 1/A, Bratislava, 81325', '49240901', 'admin'),
('1200', 'Privat banka a.s.', 'Einsteinova 24, Bratislava, 85101', '00483559', 'admin'),
('5200', 'OTP Banka Slovensko a.s.', 'Štúrova 5, Bratislava, 81302', '31318916', 'admin');
```

---

## POZNÁMKY PRE MIGRÁCIU

### 1. Generovanie bank_id

```python
# BANKLST.BTR → bank_catalog
# bank_id sa automaticky generuje (SERIAL)

# Krok 1: Načítať všetky záznamy z BANKLST.BTR
banklst_records = read_btrieve_file('BANKLST.BTR')

# Krok 2: INSERT do PostgreSQL
for record in banklst_records:
    # Spojenie adresy do jedného poľa
    bank_seat_parts = []
    if record['BankAddr']:
        bank_seat_parts.append(record['BankAddr'])
    if record['BankCtn']:
        bank_seat_parts.append(record['BankCtn'])
    if record['BankZip']:
        bank_seat_parts.append(record['BankZip'])
    bank_seat = ', '.join(bank_seat_parts) if bank_seat_parts else None
    
    cursor.execute("""
        INSERT INTO bank_catalog (
            bank_code,
            bank_name,
            bank_seat,
            bank_tax_id,
            created_by,
            created_at,
            updated_by,
            updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        record['BankCode'],
        record['BankName'],
        bank_seat,
        record['BankIno'],
        record['CrtUser'] or 'MIGRATION',
        combine_datetime(record['CrtDate'], record['CrtTime']),
        record['ModUser'] or 'MIGRATION',
        combine_datetime(record['ModDate'], record['ModTime'])
    ))
```

### 2. Vytvorenie mapping dictionary

```python
# Po migrácii BANKLST → bank_catalog
# Vytvoríme dictionary pre rýchle mapovanie

bank_catalog_map = {}
cursor.execute("SELECT bank_id, bank_code FROM bank_catalog")
for row in cursor.fetchall():
    bank_catalog_map[row['bank_code']] = row['bank_id']

# Použitie pri migrácii PAB.BTR → partner_catalog_bank_accounts
bank_id = bank_catalog_map.get(record['BankCode'])  # Môže byť None!
```

### 3. Handling NULL bank_id

**KRITICKÉ:**
```python
# V partner_catalog_bank_accounts je bank_id NULLABLE
# Dôvod: zahraničné banky, ktoré nie sú v našom číselníku

if record['BankCode'] in bank_catalog_map:
    bank_id = bank_catalog_map[record['BankCode']]
else:
    bank_id = None  # Zahraničná banka alebo neznáma
```

### 4. Poradie migrácie

**KRITICKÉ:**
1. ✅ Najprv migrovať **BANKLST.BTR** → bank_catalog
2. ✅ Vytvoriť mapping dictionary (BankCode → bank_id)
3. ✅ Potom migrovať **PAB.BTR** → partner_catalog_bank_accounts
   - `bank_id` = lookup v dictionary (môže byť NULL!)
   - `bank_name` = vždy uložiť (denormalizácia pre prípad NULL bank_id)

---

## ROZŠÍRENIA V BUDÚCNOSTI

### Možné pridanie polí:

```sql
-- Medzinárodné kódy
swift_code VARCHAR(20),          -- SWIFT/BIC kód
bic_code VARCHAR(20),             -- BIC kód

-- Kontaktné údaje
bank_website VARCHAR(100),
bank_phone VARCHAR(30),
bank_email VARCHAR(100),

-- Kategorizácia
bank_country_code VARCHAR(5) DEFAULT 'SK',
bank_type VARCHAR(20),            -- 'commercial', 'savings', 'investment'
```

---

## SÚVISIACE DOKUMENTY

- **partner_catalog** → `PAB-partner_catalog.md`
- **partner_catalog_bank_accounts** → `PAB-partner_catalog.md`

---

**Vytvoril:** Claude & Zoltán  
**Dátum:** 2025-12-10  
**Verzia:** 1.0  
**Status:** ✅ Pripravené na review