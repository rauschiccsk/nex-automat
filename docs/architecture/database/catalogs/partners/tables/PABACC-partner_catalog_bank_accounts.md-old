# PABACC.BTR → partner_catalog_bank_accounts

**Kategória:** Catalogs - Katalóg partnerov  
**NEX Genesis:** PABACC.BTR  
**NEX Automat:** `partner_catalog_bank_accounts`  
**Vytvorené:** 2025-12-10  
**Status:** ✅ Pripravené na review

---

## PREHĽAD

### Historický vývoj

**NEX Genesis (Btrieve):**
- PABACC.BTR = bankové účty obchodných partnerov
- Samostatný súbor (nie súčasť PAB00000.BTR)
- Obsahuje zastaralé pole ContoNum (číslo účtu)

**NEX Automat (PostgreSQL):**
- **partner_catalog_bank_accounts** - bankové účty partnerov
- Odstránené zastaralé pole ContoNum
- IBAN ako primárny identifikátor účtu
- Pridané pole bank_seat (adresa banky)

**Účel:**
- Správa bankových účtov partnerov
- Podpora pre viacero účtov na partnera
- Označenie hlavného účtu (is_primary)

---

## KOMPLEXNÁ SQL SCHÉMA

### partner_catalog_bank_accounts

**Tabuľka:** `partner_catalog_bank_accounts`  
**Popis:** Bankové účty partnerov

```sql
CREATE TABLE partner_catalog_bank_accounts (
    id SERIAL PRIMARY KEY,
    partner_id INTEGER NOT NULL,
    
    -- Bankové údaje
    bank_code VARCHAR(10),
    bank_name VARCHAR(100),
    bank_seat VARCHAR(100),
    iban_code VARCHAR(50) NOT NULL,
    swift_bic VARCHAR(20),
    
    -- Príznaky
    is_primary BOOLEAN DEFAULT FALSE,
    
    -- Audit
    created_by VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(30),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (partner_id) REFERENCES partner_catalog(partner_id) ON DELETE CASCADE,
    UNIQUE (partner_id, iban_code)
);

CREATE INDEX idx_partner_bank_accounts_partner ON partner_catalog_bank_accounts(partner_id);
CREATE INDEX idx_partner_bank_accounts_iban_code ON partner_catalog_bank_accounts(iban_code);
CREATE INDEX idx_partner_bank_accounts_primary ON partner_catalog_bank_accounts(is_primary) WHERE is_primary = TRUE;
CREATE INDEX idx_partner_bank_accounts_bank_code ON partner_catalog_bank_accounts(bank_code);

-- Trigger pre automatickú aktualizáciu updated_at
CREATE TRIGGER update_partner_bank_accounts_updated_at
    BEFORE UPDATE ON partner_catalog_bank_accounts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger pre aktualizáciu počítadla
CREATE OR REPLACE FUNCTION update_partner_bank_account_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE partner_catalog 
        SET bank_account_count = bank_account_count + 1
        WHERE partner_id = NEW.partner_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE partner_catalog 
        SET bank_account_count = bank_account_count - 1
        WHERE partner_id = OLD.partner_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_bank_account_count_insert
    AFTER INSERT ON partner_catalog_bank_accounts
    FOR EACH ROW
    EXECUTE FUNCTION update_partner_bank_account_count();

CREATE TRIGGER trg_update_bank_account_count_delete
    AFTER DELETE ON partner_catalog_bank_accounts
    FOR EACH ROW
    EXECUTE FUNCTION update_partner_bank_account_count();

-- Trigger pre aktualizáciu is_primary
CREATE OR REPLACE FUNCTION ensure_single_primary_bank_account()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_primary = TRUE THEN
        -- Zruš is_primary pre ostatné účty daného partnera
        UPDATE partner_catalog_bank_accounts
        SET is_primary = FALSE
        WHERE partner_id = NEW.partner_id
          AND id != COALESCE(NEW.id, 0);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_ensure_single_primary_bank_account
    BEFORE INSERT OR UPDATE ON partner_catalog_bank_accounts
    FOR EACH ROW
    WHEN (NEW.is_primary = TRUE)
    EXECUTE FUNCTION ensure_single_primary_bank_account();
```

---

## MAPPING POLÍ

### Polia ktoré SA PRENÁŠAJÚ

| Btrieve Field | Typ | → | PostgreSQL Column | Typ | Popis |
|---------------|-----|---|-------------------|-----|-------|
| PaCode | longint | → | partner_id | INTEGER | FK → partner_catalog |
| BankCode | Str4 | → | bank_code | VARCHAR(10) | Kód banky (pomôcka) |
| BankName | Str30 | → | bank_name | VARCHAR(100) | Názov banky |
| BankSeat | Str30 | → | bank_seat | VARCHAR(100) | Adresa banky |
| IbanCode | Str34 | → | iban_code | VARCHAR(50) | IBAN |
| SwftCode | Str20 | → | swift_bic | VARCHAR(20) | SWIFT/BIC |
| Default | Str1 | → | is_primary | BOOLEAN | '*' = hlavný účet |
| CrtUser | Str8 | → | created_by | VARCHAR(30) | Vytvoril užívateľ |
| CrtDate, CrtTime | Date+Time | → | created_at | TIMESTAMP | Dátum vytvorenia |
| ModUser | Str8 | → | updated_by | VARCHAR(30) | Upravil užívateľ |
| ModDate, ModTime | Date+Time | → | updated_at | TIMESTAMP | Dátum úpravy |

### Polia ktoré SA NEPRENÁŠAJÚ

| Btrieve Field | Typ | Dôvod neprenášania |
|---------------|-----|--------------------|
| ContoNum | Str30 | Zastaralé číslo účtu - nahradené IBAN |
| ModNum | word | Verzia záznamu - PostgreSQL má to automaticky |

---

## BIZNIS LOGIKA

### 1. BankCode je pomôcka, NIE FK!

**KRITICKÉ:**
```sql
bank_code VARCHAR(10)  -- Textová hodnota, NIE FK!
```

**Prečo:**
- V editore vyberieme banku z číselníka `bank_catalog`
- Systém **predvyplní** polia: bank_code, bank_name, bank_seat
- Užívateľ **môže všetko zmeniť** (nie je FK constraint!)
- Ukladá sa aktuálna textová hodnota (nie referencia)

**Workflow:**
1. Užívateľ v editore vyberie "TATRA BANKA a.s." z číselníka
2. Systém predvyplní:
   - bank_code = "1100"
   - bank_name = "TATRA BANKA a.s."
   - bank_seat = "Hodžovo námestie 3, Bratislava"
3. Užívateľ môže zmeniť napríklad bank_name na "Tatra Banka"
4. Uloží sa zmenená hodnota (nie referencia na číselník)

### 2. IBAN ako primárny identifikátor

**UNIQUE constraint:**
```sql
UNIQUE (partner_id, iban_code)
```

**Znamená:**
- Partner môže mať viacero účtov
- Ale každý IBAN musí byť unikátny pre partnera
- Zahraničné IBANy (CZ, AT, HU...) podporované

### 3. is_primary flag

**Trigger zabezpečuje:**
- Vždy len **JEDEN** účet s `is_primary = TRUE` na partnera
- Pri nastavení is_primary = TRUE sa automaticky zruší pre ostatné účty

**Transformácia:**
```python
is_primary = (record['Default'] == '*')
```

### 4. Počítadlo účtov

**Trigger automaticky aktualizuje:**
```sql
partner_catalog.bank_account_count
```

Pri INSERT → +1, pri DELETE → -1

---

## VZŤAHY S INÝMI TABUĽKAMI

### partner_catalog_bank_accounts → partner_catalog

```sql
-- Bankové účty partnera
SELECT 
    pc.partner_name,
    pba.bank_name,
    pba.iban_code,
    pba.is_primary
FROM partner_catalog pc
INNER JOIN partner_catalog_bank_accounts pba ON pc.partner_id = pba.partner_id
WHERE pc.partner_id = :partner_id
ORDER BY pba.is_primary DESC, pba.id;
```

### Hlavný bankový účet partnera

```sql
-- Získať primárny účet
SELECT 
    bank_name,
    iban_code,
    swift_bic
FROM partner_catalog_bank_accounts
WHERE partner_id = :partner_id
  AND is_primary = TRUE;
```

### Štatistika bánk (cez bank_code)

```sql
-- Koľko partnerov používa jednotlivé banky
SELECT 
    pba.bank_code,
    pba.bank_name,
    COUNT(DISTINCT pba.partner_id) AS partner_count,
    COUNT(pba.id) AS account_count
FROM partner_catalog_bank_accounts pba
GROUP BY pba.bank_code, pba.bank_name
ORDER BY partner_count DESC;
```

---

## VALIDAČNÉ PRAVIDLÁ

### 1. IBAN povinný

```sql
iban_code VARCHAR(50) NOT NULL
```

### 2. Unikátny IBAN pre partnera

```sql
UNIQUE (partner_id, iban_code)
```

### 3. Len jeden primárny účet

Zabezpečené triggerom `trg_ensure_single_primary_bank_account`.

### 4. Validácia IBAN formátu

```sql
-- Budúce rozšírenie: CHECK constraint pre IBAN formát
CHECK (iban_code ~ '^[A-Z]{2}[0-9]{2}[A-Z0-9]+$')
```

---

## QUERY PATTERNS

### Všetky účty partnera

```sql
SELECT 
    id,
    bank_name,
    iban_code,
    is_primary
FROM partner_catalog_bank_accounts
WHERE partner_id = :partner_id
ORDER BY is_primary DESC, created_at;
```

### Primárny účet partnera

```sql
SELECT 
    bank_name,
    iban_code,
    swift_bic
FROM partner_catalog_bank_accounts
WHERE partner_id = :partner_id
  AND is_primary = TRUE;
```

### Partneri s viacerými účtami

```sql
SELECT 
    pc.partner_name,
    COUNT(pba.id) AS account_count
FROM partner_catalog pc
INNER JOIN partner_catalog_bank_accounts pba ON pc.partner_id = pba.partner_id
GROUP BY pc.partner_id, pc.partner_name
HAVING COUNT(pba.id) > 1
ORDER BY account_count DESC;
```

### Vyhľadanie účtu podľa IBAN

```sql
SELECT 
    pc.partner_name,
    pba.bank_name,
    pba.iban_code
FROM partner_catalog_bank_accounts pba
INNER JOIN partner_catalog pc ON pba.partner_id = pc.partner_id
WHERE pba.iban_code = :iban_code;
```

---

## PRÍKLAD DÁT

```sql
-- Partner má 2 bankové účty
INSERT INTO partner_catalog_bank_accounts (partner_id, bank_code, bank_name, bank_seat, iban_code, swift_bic, is_primary, created_by) VALUES
(1, '1100', 'TATRA BANKA a.s.', 'Hodžovo námestie 3, Bratislava', 'SK1234567890123456789012', 'TATRSKBX', TRUE, 'admin'),
(1, '0900', 'Slovenská sporiteľňa a.s.', 'Tomášikova 48, Bratislava', 'SK9876543210987654321098', 'GIBASKBX', FALSE, 'admin');

-- Partner so zahraničným účtom (bez bank_code)
INSERT INTO partner_catalog_bank_accounts (partner_id, bank_code, bank_name, bank_seat, iban_code, swift_bic, is_primary, created_by) VALUES
(2, NULL, 'Česká spořitelna a.s.', 'Praha, Česká republika', 'CZ1234567890123456789012', 'GIBACZPX', TRUE, 'admin');
```

---

## POZNÁMKY PRE MIGRÁCIU

### 1. Transformácia is_primary

```python
# Default = '*' → is_primary = TRUE
is_primary = (record['Default'] == '*')
```

### 2. Handling prázdnych polí

```python
# Bank údaje môžu byť prázdne (zahraničné účty)
bank_code = record['BankCode'] or None
bank_name = record['BankName'] or None
bank_seat = record['BankSeat'] or None
swift_bic = record['SwftCode'] or None
```

### 3. Migračný script

```python
# PABACC.BTR → partner_catalog_bank_accounts
pabacc_records = read_btrieve_file('PABACC.BTR')

for record in pabacc_records:
    cursor.execute("""
        INSERT INTO partner_catalog_bank_accounts (
            partner_id,
            bank_code,
            bank_name,
            bank_seat,
            iban_code,
            swift_bic,
            is_primary,
            created_by,
            created_at,
            updated_by,
            updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        record['PaCode'],
        record['BankCode'] or None,
        record['BankName'] or None,
        record['BankSeat'] or None,
        record['IbanCode'],
        record['SwftCode'] or None,
        record['Default'] == '*',
        record['CrtUser'] or 'MIGRATION',
        combine_datetime(record['CrtDate'], record['CrtTime']),
        record['ModUser'] or 'MIGRATION',
        combine_datetime(record['ModDate'], record['ModTime'])
    ))
```

### 4. Poradie migrácie

**KRITICKÉ:**
1. ✅ Najprv migrovať **PAB00000.BTR** → partner_catalog
2. ✅ Potom migrovať **PABACC.BTR** → partner_catalog_bank_accounts
   - FK na partner_catalog(partner_id) musí existovať!

### 5. Validácia po migrácii

```sql
-- Kontrola počtu účtov
SELECT 
    pc.partner_id,
    pc.partner_name,
    pc.bank_account_count,
    COUNT(pba.id) AS actual_count
FROM partner_catalog pc
LEFT JOIN partner_catalog_bank_accounts pba ON pc.partner_id = pba.partner_id
GROUP BY pc.partner_id, pc.partner_name, pc.bank_account_count
HAVING pc.bank_account_count != COUNT(pba.id);

-- Kontrola primárnych účtov (každý partner by mal mať max 1)
SELECT 
    partner_id,
    COUNT(*) AS primary_count
FROM partner_catalog_bank_accounts
WHERE is_primary = TRUE
GROUP BY partner_id
HAVING COUNT(*) > 1;
```

---

## SÚVISIACE DOKUMENTY

- **partner_catalog** → `PAB-partner_catalog.md`
- **bank_catalog** → `BANKLST-bank_catalog.md` (číselník pre pomôcku)

---

**Vytvoril:** Claude & Zoltán  
**Dátum:** 2025-12-10  
**Verzia:** 1.1  
**Status:** ✅ Pripravené na review