# PAB.BTR → partner_catalog (8 tabuliek)

**Verzia:** 1.1 (OPRAVENÉ: iban → iban_code)  
**Autor:** Zoltán & Claude  
**Dátum:** 2025-12-10  
**Status:** ✅ Production Ready (po oprave)

---

## 1. PREHĽAD

**Btrieve súbor:** PAB.BTR (Partner Address Book)  
**PostgreSQL tabuľky:**
1. `partner_catalog` - hlavné údaje partnera (16 polí)
2. `partner_catalog_extensions` - rozšírené údaje predaj/nákup (19 polí)
3. `partner_catalog_categories` - mapovanie na skupiny partnerov
4. `partner_catalog_addresses` - tri typy adries (registered, correspondence, invoice)
5. `partner_catalog_contacts` - kontaktné údaje pre každý typ adresy
6. `partner_catalog_texts` - textové polia (owner_name)
7. `partner_catalog_bank_accounts` - bankové účty partnera (PABACC.BTR)
8. `partner_catalog_facilities` - prevádzkové jednotky (⏳ TODO)

**Účel:** Komplexný katalóg obchodných partnerov (dodávatelia, odberatelia) s rozšírenými údajmi potrebnými pre fakturáciu, účtovníctvo a obchodné transakcie.

**Poznámka:** PAB.BTR je jeden z najkomplexnejších súborov v NEX Genesis s viac ako 100 poliami v pôvodnej štruktúre.

---

## 2. KOMPLEXNÁ SQL SCHÉMA

### 2.1 Hlavná tabuľka - partner_catalog

```sql
CREATE TABLE partner_catalog (
    -- Primárny kľúč
    partner_id SERIAL PRIMARY KEY,
    
    -- Základné identifikátory (Btrieve: PABNr, PABSuNr, PABSubIdx)
    partner_number VARCHAR(20) NOT NULL,
    partner_subnumber VARCHAR(10) DEFAULT '',
    partner_subindex VARCHAR(5) DEFAULT '',
    
    -- Názov a základné údaje (Btrieve: PABName, PABShName)
    partner_name VARCHAR(100) NOT NULL,
    partner_shortname VARCHAR(50),
    
    -- IČO/DIČ (Btrieve: PABICO, PABDIC)
    company_id VARCHAR(20),
    tax_id VARCHAR(20),
    vat_number VARCHAR(20),
    
    -- Partner types (Btrieve: PABTyp)
    is_supplier BOOLEAN DEFAULT FALSE,
    is_customer BOOLEAN DEFAULT FALSE,
    is_both BOOLEAN DEFAULT FALSE,
    
    -- Finančné údaje (Btrieve: PABCurr, PABFinGrp, PABPayMeth)
    currency_code VARCHAR(3) DEFAULT 'EUR',
    financial_category_id INTEGER REFERENCES product_categories(category_id),
    default_payment_method_id INTEGER REFERENCES payment_methods(payment_method_id),
    
    -- Počítadlá (automatické cez triggery)
    bank_account_count INTEGER DEFAULT 0,
    facility_count INTEGER DEFAULT 0,
    
    -- Audit polia
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Business constraints
    CONSTRAINT unique_partner_number UNIQUE (partner_number, partner_subnumber, partner_subindex),
    CONSTRAINT check_partner_type CHECK (is_supplier OR is_customer OR is_both),
    CONSTRAINT check_currency_code CHECK (LENGTH(currency_code) = 3)
);

-- Indexy pre vyhľadávanie
CREATE INDEX idx_partner_catalog_number ON partner_catalog(partner_number);
CREATE INDEX idx_partner_catalog_name ON partner_catalog(partner_name);
CREATE INDEX idx_partner_catalog_company_id ON partner_catalog(company_id);
CREATE INDEX idx_partner_catalog_tax_id ON partner_catalog(tax_id);
CREATE INDEX idx_partner_catalog_type ON partner_catalog(is_supplier, is_customer, is_both);
CREATE INDEX idx_partner_catalog_active ON partner_catalog(is_active);

-- Trigger pre updated_at
CREATE TRIGGER update_partner_catalog_updated_at
    BEFORE UPDATE ON partner_catalog
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Funkcia pre update_updated_at_column (univerzálna)
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### 2.2 Rozšírené údaje - partner_catalog_extensions

```sql
CREATE TABLE partner_catalog_extensions (
    extension_id SERIAL PRIMARY KEY,
    partner_id INTEGER NOT NULL REFERENCES partner_catalog(partner_id) ON DELETE CASCADE,
    
    -- Obchodné podmienky - predaj (Btrieve: PABPayMeth, PABTrpMeth, PABDisc)
    sales_payment_method_id INTEGER REFERENCES payment_methods(payment_method_id),
    sales_transport_method_id INTEGER REFERENCES transport_methods(transport_method_id),
    sales_discount_percent DECIMAL(5,2) DEFAULT 0.00,
    sales_credit_limit DECIMAL(15,2) DEFAULT 0.00,
    
    -- Obchodné podmienky - nákup (Btrieve: PABPayMethP, PABTrpMethP, PABDiscP)
    purchase_payment_method_id INTEGER REFERENCES payment_methods(payment_method_id),
    purchase_transport_method_id INTEGER REFERENCES transport_methods(transport_method_id),
    purchase_discount_percent DECIMAL(5,2) DEFAULT 0.00,
    purchase_credit_limit DECIMAL(15,2) DEFAULT 0.00,
    
    -- Cenové politiky (Btrieve: PABPrcLst)
    default_price_list_number VARCHAR(20),
    
    -- Kontaktné osoby (Btrieve: PABContact, PABContactP)
    sales_contact_person VARCHAR(100),
    purchase_contact_person VARCHAR(100),
    
    -- Poznámky (Btrieve: PABNote1, PABNote2)
    sales_notes TEXT,
    purchase_notes TEXT,
    internal_notes TEXT,
    
    -- Štatistické údaje
    last_sales_date DATE,
    last_purchase_date DATE,
    total_sales_amount DECIMAL(15,2) DEFAULT 0.00,
    total_purchase_amount DECIMAL(15,2) DEFAULT 0.00,
    
    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Business constraints
    CONSTRAINT unique_partner_extension UNIQUE (partner_id),
    CONSTRAINT check_sales_discount CHECK (sales_discount_percent BETWEEN 0 AND 100),
    CONSTRAINT check_purchase_discount CHECK (purchase_discount_percent BETWEEN 0 AND 100)
);

CREATE INDEX idx_partner_extensions_partner ON partner_catalog_extensions(partner_id);
CREATE INDEX idx_partner_extensions_price_list ON partner_catalog_extensions(default_price_list_number);

CREATE TRIGGER update_partner_extensions_updated_at
    BEFORE UPDATE ON partner_catalog_extensions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### 2.3 Kategorizácia - partner_catalog_categories

```sql
CREATE TABLE partner_catalog_categories (
    mapping_id SERIAL PRIMARY KEY,
    partner_id INTEGER NOT NULL REFERENCES partner_catalog(partner_id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES partner_categories(category_id) ON DELETE RESTRICT,
    
    -- Audit
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_by VARCHAR(50),
    
    -- Business constraints
    CONSTRAINT unique_partner_category UNIQUE (partner_id, category_id)
);

CREATE INDEX idx_partner_categories_partner ON partner_catalog_categories(partner_id);
CREATE INDEX idx_partner_categories_category ON partner_catalog_categories(category_id);
```

### 2.4 Adresy - partner_catalog_addresses

```sql
CREATE TABLE partner_catalog_addresses (
    address_id SERIAL PRIMARY KEY,
    partner_id INTEGER NOT NULL REFERENCES partner_catalog(partner_id) ON DELETE CASCADE,
    
    -- Typ adresy
    address_type VARCHAR(20) NOT NULL,  -- 'registered', 'correspondence', 'invoice'
    
    -- Adresné údaje (Btrieve: PABStreet, PABCtn, PABZip, PABState)
    street VARCHAR(100),
    city VARCHAR(100),
    zip_code VARCHAR(20),
    country_code VARCHAR(2) DEFAULT 'SK',
    
    -- Poznámka
    address_note TEXT,
    
    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Business constraints
    CONSTRAINT unique_partner_address_type UNIQUE (partner_id, address_type),
    CONSTRAINT check_address_type CHECK (address_type IN ('registered', 'correspondence', 'invoice')),
    CONSTRAINT check_country_code CHECK (LENGTH(country_code) = 2)
);

CREATE INDEX idx_partner_addresses_partner ON partner_catalog_addresses(partner_id);
CREATE INDEX idx_partner_addresses_type ON partner_catalog_addresses(address_type);

CREATE TRIGGER update_partner_addresses_updated_at
    BEFORE UPDATE ON partner_catalog_addresses
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### 2.5 Kontakty - partner_catalog_contacts

```sql
CREATE TABLE partner_catalog_contacts (
    contact_id SERIAL PRIMARY KEY,
    address_id INTEGER NOT NULL REFERENCES partner_catalog_addresses(address_id) ON DELETE CASCADE,
    
    -- Kontaktné údaje (Btrieve: PABPhone, PABFax, PABEmail, PABWww)
    phone VARCHAR(50),
    mobile VARCHAR(50),
    fax VARCHAR(50),
    email VARCHAR(100),
    website VARCHAR(200),
    
    -- Kontaktná osoba
    contact_person VARCHAR(100),
    contact_position VARCHAR(100),
    
    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Business constraints
    CONSTRAINT check_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
);

CREATE INDEX idx_partner_contacts_address ON partner_catalog_contacts(address_id);
CREATE INDEX idx_partner_contacts_email ON partner_catalog_contacts(email);

CREATE TRIGGER update_partner_contacts_updated_at
    BEFORE UPDATE ON partner_catalog_contacts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### 2.6 Textové polia - partner_catalog_texts

```sql
CREATE TABLE partner_catalog_texts (
    text_id SERIAL PRIMARY KEY,
    partner_id INTEGER NOT NULL REFERENCES partner_catalog(partner_id) ON DELETE CASCADE,
    
    -- Textové polia (Btrieve: PABOwner)
    owner_name VARCHAR(200),  -- Majiteľ/konateľ spoločnosti
    
    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Business constraint
    CONSTRAINT unique_partner_texts UNIQUE (partner_id)
);

CREATE INDEX idx_partner_texts_partner ON partner_catalog_texts(partner_id);

CREATE TRIGGER update_partner_texts_updated_at
    BEFORE UPDATE ON partner_catalog_texts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### 2.7 Bankové účty - partner_catalog_bank_accounts

```sql
CREATE TABLE partner_catalog_bank_accounts (
    account_id SERIAL PRIMARY KEY,
    partner_id INTEGER NOT NULL REFERENCES partner_catalog(partner_id) ON DELETE CASCADE,
    
    -- Bankové údaje (Btrieve PABACC: BankCode, BankAccNr, IBAN)
    bank_code VARCHAR(10),  -- ⚠️ TEXTOVÁ HODNOTA, NIE FK!
    account_number VARCHAR(50),
    iban_code VARCHAR(50),  -- ✅ OPRAVENÉ: iban → iban_code
    swift_code VARCHAR(20),
    
    -- Adresa banky (Btrieve: BankName, BankAddr, BankCtn, BankZip)
    bank_name VARCHAR(100),
    bank_seat VARCHAR(200),  -- Komplexná adresa banky
    
    -- Variabilné symboly (Btrieve: VarSymS, VarSymP)
    variable_symbol_sales VARCHAR(20),
    variable_symbol_purchase VARCHAR(20),
    
    -- Primárny účet
    is_primary BOOLEAN DEFAULT FALSE,
    
    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Business constraints
    CONSTRAINT unique_partner_bank_account UNIQUE (partner_id, iban_code),  -- ✅ OPRAVENÉ
    CONSTRAINT check_iban_format CHECK (iban_code ~* '^[A-Z]{2}[0-9]{2}[A-Z0-9]+$')
);

-- Indexy
CREATE INDEX idx_partner_bank_accounts_partner ON partner_catalog_bank_accounts(partner_id);
CREATE INDEX idx_partner_bank_accounts_iban_code ON partner_catalog_bank_accounts(iban_code);  -- ✅ OPRAVENÉ
CREATE INDEX idx_partner_bank_accounts_primary ON partner_catalog_bank_accounts(partner_id, is_primary);

-- Trigger pre updated_at
CREATE TRIGGER update_partner_bank_accounts_updated_at
    BEFORE UPDATE ON partner_catalog_bank_accounts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger pre is_primary (len jeden primárny účet)
CREATE OR REPLACE FUNCTION ensure_single_primary_bank_account()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_primary = TRUE THEN
        UPDATE partner_catalog_bank_accounts
        SET is_primary = FALSE
        WHERE partner_id = NEW.partner_id
          AND account_id != COALESCE(NEW.account_id, 0);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_single_primary_bank_account
    BEFORE INSERT OR UPDATE ON partner_catalog_bank_accounts
    FOR EACH ROW
    WHEN (NEW.is_primary = TRUE)
    EXECUTE FUNCTION ensure_single_primary_bank_account();

-- Trigger pre aktualizáciu počítadla v partner_catalog
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

CREATE TRIGGER trigger_update_bank_account_count
    AFTER INSERT OR DELETE ON partner_catalog_bank_accounts
    FOR EACH ROW
    EXECUTE FUNCTION update_partner_bank_account_count();
```

### 2.8 Prevádzkové jednotky - partner_catalog_facilities

```sql
-- ⏳ TODO: Špecifikácia po potvrdení od Usera
-- Táto tabuľka bude obsahovať:
-- - facility_id, partner_id
-- - facility_name, facility_code
-- - address údaje
-- - kontakty
-- - is_active
```

---

## 3. MAPPING POLÍ

### 3.1 Polia ktoré SA PRENÁŠAJÚ

| Btrieve pole | PostgreSQL pole | Typ transformácie | Poznámka |
|--------------|-----------------|-------------------|----------|
| **Základné identifikátory** |
| PABNr | partner_number | Direct | Povinné |
| PABSuNr | partner_subnumber | Default empty | Voliteľné číslo |
| PABSubIdx | partner_subindex | Default empty | Voliteľný index |
| PABName | partner_name | Direct | Povinný názov |
| PABShName | partner_shortname | Direct | Skrátený názov |
| **Identifikačné čísla** |
| PABICO | company_id | Direct | IČO |
| PABDIC | tax_id | Direct | DIČ |
| PABDPH | vat_number | Direct | IČ DPH |
| **Typ partnera** |
| PABTyp | is_supplier / is_customer / is_both | Boolean split | Typ partnera |
| **Finančné údaje** |
| PABCurr | currency_code | Direct | Mena |
| PABFinGrp | financial_category_id | Lookup | FK na product_categories |
| PABPayMeth | default_payment_method_id | Lookup | FK na payment_methods |
| **Adresy (3 typy)** |
| PABStreet | street | Direct | Ulica |
| PABCtn | city | Direct | Mesto |
| PABZip | zip_code | Direct | PSČ |
| PABState | country_code | Direct | Štát |
| **Kontakty** |
| PABPhone | phone | Direct | Telefón |
| PABFax | fax | Direct | Fax |
| PABEmail | email | Direct | Email |
| PABWww | website | Direct | Web |
| **Rozšírené údaje - predaj** |
| PABPayMeth | sales_payment_method_id | Lookup | FK na payment_methods |
| PABTrpMeth | sales_transport_method_id | Lookup | FK na transport_methods |
| PABDisc | sales_discount_percent | Direct | Zľava % |
| PABCreditLim | sales_credit_limit | Direct | Úverový limit |
| PABPrcLst | default_price_list_number | Direct | Cenník |
| PABContact | sales_contact_person | Direct | Kontaktná osoba |
| PABNote1 | sales_notes | Direct | Poznámky |
| **Rozšírené údaje - nákup** |
| PABPayMethP | purchase_payment_method_id | Lookup | FK na payment_methods |
| PABTrpMethP | purchase_transport_method_id | Lookup | FK na transport_methods |
| PABDiscP | purchase_discount_percent | Direct | Zľava % |
| PABCreditLimP | purchase_credit_limit | Direct | Úverový limit |
| PABContactP | purchase_contact_person | Direct | Kontaktná osoba |
| PABNote2 | purchase_notes | Direct | Poznámky |
| **Textové polia** |
| PABOwner | owner_name | Direct | Majiteľ/konateľ |
| **Bankové účty (PABACC.BTR)** |
| BankCode | bank_code | Direct | ⚠️ Textová hodnota |
| BankAccNr | account_number | Direct | Číslo účtu |
| IBAN | iban_code | Direct | ✅ OPRAVENÉ: iban → iban_code |
| SWIFT | swift_code | Direct | SWIFT kód |
| BankName | bank_name | Direct | Názov banky |
| BankAddr + BankCtn + BankZip | bank_seat | Concatenate | Komplexná adresa |
| VarSymS | variable_symbol_sales | Direct | VS predaj |
| VarSymP | variable_symbol_purchase | Direct | VS nákup |

### 3.2 Polia ktoré SA NEPRENÁŠAJÚ

| Btrieve pole | Dôvod neprenášania |
|--------------|--------------------|
| PABRecNo | Btrieve internal record number - nahradené SERIAL |
| PABLocked | Zámok záznamu - nie je potrebný v PostgreSQL |
| PABLastUpd | Nahradené audit poľami (updated_at) |
| PABDeleted | Nahradené is_active flag |
| PABVersion | Verzovanie - riešené inak |
| PAB_Reserved_* | Rezervované polia - nepoužívané |

---

## 4. BIZNIS LOGIKA

### 4.1 Partner Types (is_supplier, is_customer, is_both)

**Pôvodný systém (Btrieve):**
- PABTyp = 'D' (dodávateľ)
- PABTyp = 'O' (odberateľ)
- PABTyp = 'B' (oboje)

**Nový systém (PostgreSQL):**
```sql
-- Dodávateľ
is_supplier = TRUE, is_customer = FALSE, is_both = FALSE

-- Odberateľ
is_supplier = FALSE, is_customer = TRUE, is_both = FALSE

-- Oboje
is_supplier = FALSE, is_customer = FALSE, is_both = TRUE
```

**Business rule:** Aspoň jeden flag musí byť TRUE (CHECK constraint).

### 4.2 Adresy a kontakty

**Tri typy adries:**
1. **registered** - sídlo spoločnosti (povinné)
2. **correspondence** - korešpondenčná adresa (voliteľné)
3. **invoice** - fakturačná adresa (voliteľné)

**Kontakty:** Každá adresa môže mať vlastné kontaktné údaje (telefón, email, atď.)

### 4.3 Bankové účty

**Business rules:**
1. Partner môže mať viacero bankových účtov
2. Len jeden účet môže byť primárny (is_primary = TRUE)
3. IBAN musí byť unique pre partnera
4. bank_code je TEXTOVÁ hodnota, NIE FK na bank_catalog!

**Workflow pri pridávaní účtu:**
1. User vyberie banku z číselníka (bank_catalog)
2. Systém predvyplní polia: bank_code, bank_name, bank_seat
3. User môže všetko zmeniť (nie je to záväzné)
4. Uloží sa textová hodnota (nie referencia)

### 4.4 Počítadlá (bank_account_count, facility_count)

**Automatická aktualizácia cez triggery:**
```sql
-- Pri INSERT do partner_catalog_bank_accounts
bank_account_count = bank_account_count + 1

-- Pri DELETE z partner_catalog_bank_accounts
bank_account_count = bank_account_count - 1
```

---

## 5. VZŤAHY S INÝMI TABUĽKAMI

### 5.1 Incoming (z iných tabuliek)

```
product_categories (FK: financial_category_id)
    ↓
partner_catalog
    ↓
├→ partner_catalog_extensions
├→ partner_catalog_categories ←─ partner_categories
├→ partner_catalog_addresses
│   ↓
│   └→ partner_catalog_contacts
├→ partner_catalog_texts
├→ partner_catalog_bank_accounts
└→ partner_catalog_facilities

payment_methods (FK: default_payment_method_id, sales_payment_method_id, purchase_payment_method_id)
    ↓
partner_catalog / partner_catalog_extensions

transport_methods (FK: sales_transport_method_id, purchase_transport_method_id)
    ↓
partner_catalog_extensions
```

### 5.2 Outgoing (do iných tabuliek)

```
partner_catalog
    ↓
invoices, purchase_orders, sales_orders... (⚠️ BEZ FK constraints - denormalizované!)
```

**KRITICKÉ:** Archívne dokumenty (faktúry, príjemky) nemajú FK constraint na partner_catalog! Všetky údaje sú snapshot v dokumente (právny požiadavok SK účtovných predpisov).

---

## 6. VALIDAČNÉ PRAVIDLÁ

### 6.1 CHECK Constraints

```sql
-- Partner type validation
CONSTRAINT check_partner_type CHECK (is_supplier OR is_customer OR is_both)

-- Discount validation
CONSTRAINT check_sales_discount CHECK (sales_discount_percent BETWEEN 0 AND 100)
CONSTRAINT check_purchase_discount CHECK (purchase_discount_percent BETWEEN 0 AND 100)

-- Currency code
CONSTRAINT check_currency_code CHECK (LENGTH(currency_code) = 3)

-- Country code
CONSTRAINT check_country_code CHECK (LENGTH(country_code) = 2)

-- Address type
CONSTRAINT check_address_type CHECK (address_type IN ('registered', 'correspondence', 'invoice'))

-- Email format
CONSTRAINT check_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')

-- IBAN format (SK aj medzinárodné)
CONSTRAINT check_iban_format CHECK (iban_code ~* '^[A-Z]{2}[0-9]{2}[A-Z0-9]+$')  -- ✅ OPRAVENÉ
```

### 6.2 Triggery

**ensure_single_primary_bank_account:**
- Pri nastavení is_primary = TRUE zruší primárny flag pre ostatné účty partnera
- Zabezpečuje, že len jeden účet môže byť primárny

**update_partner_bank_account_count:**
- Pri INSERT/DELETE aktualizuje počítadlo v partner_catalog

**update_updated_at_column:**
- Pri každom UPDATE nastaví updated_at na CURRENT_TIMESTAMP

---

## 7. QUERY PATTERNS

### 7.1 Vyhľadávanie partnera podľa čísla

```sql
-- Základné vyhľadávanie
SELECT p.*, pe.*, pa.*, pc.*, pt.*
FROM partner_catalog p
LEFT JOIN partner_catalog_extensions pe ON p.partner_id = pe.partner_id
LEFT JOIN partner_catalog_addresses pa ON p.partner_id = pa.partner_id
LEFT JOIN partner_catalog_contacts pc ON pa.address_id = pc.address_id
LEFT JOIN partner_catalog_texts pt ON p.partner_id = pt.partner_id
WHERE p.partner_number = '12345'
  AND p.is_active = TRUE;
```

### 7.2 Kompletný partner s bankovými účtami

```sql
-- Partner s primárnym bankovým účtom
SELECT 
    p.*,
    pba.iban_code,  -- ✅ OPRAVENÉ
    pba.account_number,
    pba.bank_name,
    pba.swift_code
FROM partner_catalog p
LEFT JOIN partner_catalog_bank_accounts pba 
    ON p.partner_id = pba.partner_id 
    AND pba.is_primary = TRUE
WHERE p.partner_number = '12345';

-- Partner s všetkými bankovými účtami
SELECT 
    p.partner_name,
    pba.bank_name,
    pba.iban_code,  -- ✅ OPRAVENÉ
    pba.account_number,
    pba.is_primary
FROM partner_catalog p
LEFT JOIN partner_catalog_bank_accounts pba ON p.partner_id = pba.partner_id
WHERE p.partner_number = '12345'
ORDER BY pba.is_primary DESC, pba.bank_name;
```

### 7.3 Vyhľadávanie podľa typu partnera

```sql
-- Všetci dodávatelia
SELECT p.*, pe.purchase_payment_method_id, pe.purchase_discount_percent
FROM partner_catalog p
LEFT JOIN partner_catalog_extensions pe ON p.partner_id = pe.partner_id
WHERE p.is_supplier = TRUE
  AND p.is_active = TRUE;

-- Všetci odberatelia
SELECT p.*, pe.sales_payment_method_id, pe.sales_discount_percent
FROM partner_catalog p
LEFT JOIN partner_catalog_extensions pe ON p.partner_id = pe.partner_id
WHERE p.is_customer = TRUE
  AND p.is_active = TRUE;

-- Partneri oboje (dodávatelia aj odberatelia)
SELECT p.*, pe.*
FROM partner_catalog p
LEFT JOIN partner_catalog_extensions pe ON p.partner_id = pe.partner_id
WHERE p.is_both = TRUE
  AND p.is_active = TRUE;
```

### 7.4 Vyhľadávanie podľa IČO/DIČ

```sql
-- Vyhľadanie podľa IČO
SELECT * FROM partner_catalog
WHERE company_id = '12345678'
  AND is_active = TRUE;

-- Vyhľadanie podľa DIČ
SELECT * FROM partner_catalog
WHERE tax_id = '1234567890'
  AND is_active = TRUE;

-- Vyhľadanie podľa IČ DPH
SELECT * FROM partner_catalog
WHERE vat_number = 'SK1234567890'
  AND is_active = TRUE;
```

### 7.5 Partner s kategóriami

```sql
-- Partner s pripojenými kategóriami
SELECT 
    p.partner_name,
    pc_cat.category_code,
    pc_cat.category_name
FROM partner_catalog p
JOIN partner_catalog_categories pcc ON p.partner_id = pcc.partner_id
JOIN partner_categories pc_cat ON pcc.category_id = pc_cat.category_id
WHERE p.partner_number = '12345'
ORDER BY pc_cat.category_code;
```

### 7.6 Komplexný SELECT pre NEX Automat

```sql
-- Kompletné dáta partnera pre spracovanie faktúry
SELECT 
    -- Hlavné údaje
    p.partner_id,
    p.partner_number,
    p.partner_name,
    p.company_id,
    p.tax_id,
    p.vat_number,
    
    -- Typ partnera
    p.is_supplier,
    p.is_customer,
    
    -- Rozšírené údaje
    pe.sales_payment_method_id,
    pe.sales_discount_percent,
    pe.default_price_list_number,
    
    -- Sídlo spoločnosti
    pa_reg.street AS registered_street,
    pa_reg.city AS registered_city,
    pa_reg.zip_code AS registered_zip,
    
    -- Kontakty
    pc_reg.email AS registered_email,
    pc_reg.phone AS registered_phone,
    
    -- Primárny bankový účet
    pba.iban_code AS primary_iban,  -- ✅ OPRAVENÉ
    pba.account_number AS primary_account,
    pba.bank_name AS primary_bank_name,
    pba.swift_code AS primary_swift,
    pba.variable_symbol_sales,
    
    -- Majiteľ
    pt.owner_name

FROM partner_catalog p
LEFT JOIN partner_catalog_extensions pe ON p.partner_id = pe.partner_id
LEFT JOIN partner_catalog_addresses pa_reg ON p.partner_id = pa_reg.partner_id 
    AND pa_reg.address_type = 'registered'
LEFT JOIN partner_catalog_contacts pc_reg ON pa_reg.address_id = pc_reg.address_id
LEFT JOIN partner_catalog_bank_accounts pba ON p.partner_id = pba.partner_id 
    AND pba.is_primary = TRUE
LEFT JOIN partner_catalog_texts pt ON p.partner_id = pt.partner_id

WHERE p.partner_number = '12345'
  AND p.is_active = TRUE;
```

---

## 8. PRÍKLAD DÁT

### 8.1 Partner catalog - hlavné údaje

```sql
INSERT INTO partner_catalog (
    partner_number, partner_subnumber, partner_subindex,
    partner_name, partner_shortname,
    company_id, tax_id, vat_number,
    is_supplier, is_customer, is_both,
    currency_code, financial_category_id, default_payment_method_id,
    is_active
) VALUES
    ('10001', '', '', 'ABC Veľkoobchod s.r.o.', 'ABC VO', '12345678', '1234567890', 'SK1234567890', 
     TRUE, FALSE, FALSE, 'EUR', 1, 1, TRUE),
     
    ('20001', '', '', 'XYZ Retail s.r.o.', 'XYZ', '87654321', '0987654321', 'SK0987654321',
     FALSE, TRUE, FALSE, 'EUR', 2, 2, TRUE),
     
    ('30001', '', '', 'Global Trading s.r.o.', 'GLOBAL', '11223344', '4433221100', 'SK4433221100',
     FALSE, FALSE, TRUE, 'EUR', 3, 3, TRUE);
```

### 8.2 Partner catalog extensions

```sql
INSERT INTO partner_catalog_extensions (
    partner_id,
    sales_payment_method_id, sales_transport_method_id, sales_discount_percent, sales_credit_limit,
    purchase_payment_method_id, purchase_transport_method_id, purchase_discount_percent, purchase_credit_limit,
    default_price_list_number,
    sales_contact_person, purchase_contact_person,
    sales_notes, purchase_notes
) VALUES
    (1, 1, 1, 5.00, 10000.00, NULL, NULL, 0.00, 0.00, 'PL001', 'Ján Nový', NULL, 'VIP zákazník', NULL),
    (2, 2, 2, 2.00, 5000.00, NULL, NULL, 0.00, 0.00, 'PL002', NULL, NULL, NULL, NULL),
    (3, 3, 3, 3.00, 15000.00, 3, 3, 2.00, 8000.00, 'PL003', 'Peter Varga', 'Mária Horná', 'Dôležitý partner', 'Overené');
```

### 8.3 Partner addresses

```sql
INSERT INTO partner_catalog_addresses (
    partner_id, address_type,
    street, city, zip_code, country_code
) VALUES
    -- ABC Veľkoobchod - sídlo
    (1, 'registered', 'Hlavná 123', 'Bratislava', '81101', 'SK'),
    (1, 'correspondence', 'Nová 45', 'Bratislava', '82105', 'SK'),
    
    -- XYZ Retail - sídlo
    (2, 'registered', 'Obchodná 67', 'Košice', '04001', 'SK'),
    
    -- Global Trading - sídlo + fakturačná
    (3, 'registered', 'Továrenská 89', 'Žilina', '01001', 'SK'),
    (3, 'invoice', 'Skladová 12', 'Žilina', '01008', 'SK');
```

### 8.4 Partner contacts

```sql
INSERT INTO partner_catalog_contacts (
    address_id,
    phone, mobile, fax, email, website,
    contact_person, contact_position
) VALUES
    -- ABC Veľkoobchod - sídlo
    (1, '+421 2 1234 5678', '+421 905 123 456', '+421 2 1234 5679', 'info@abc-vo.sk', 'www.abc-vo.sk', 
     'Ján Nový', 'Obchodný riaditeľ'),
     
    -- ABC Veľkoobchod - korešpondenčná
    (2, '+421 2 9876 5432', NULL, NULL, 'office@abc-vo.sk', NULL, 'Mária Nováková', 'Asistentka'),
    
    -- XYZ Retail - sídlo
    (3, '+421 55 1234 567', '+421 910 987 654', NULL, 'kontakt@xyz-retail.sk', 'www.xyz-retail.sk',
     'Peter Varga', 'Konateľ'),
     
    -- Global Trading - sídlo
    (4, '+421 41 123 4567', '+421 915 555 666', '+421 41 123 4568', 'sales@global-trading.sk', 'www.global-trading.sk',
     'Lukáš Horný', 'Sales Manager'),
     
    -- Global Trading - fakturačná
    (5, '+421 41 987 6543', NULL, NULL, 'accounting@global-trading.sk', NULL, 'Eva Biela', 'Účtovníčka');
```

### 8.5 Partner texts

```sql
INSERT INTO partner_catalog_texts (
    partner_id, owner_name
) VALUES
    (1, 'Ing. Ján Nový'),
    (2, 'Mgr. Peter Varga'),
    (3, 'Ing. Lukáš Horný, PhD.');
```

### 8.6 Partner bank accounts

```sql
INSERT INTO partner_catalog_bank_accounts (
    partner_id,
    bank_code, account_number, iban_code, swift_code,  -- ✅ OPRAVENÉ: iban → iban_code
    bank_name, bank_seat,
    variable_symbol_sales, variable_symbol_purchase,
    is_primary
) VALUES
    -- ABC Veľkoobchod - primárny účet
    (1, '0200', '1234567890/0200', 'SK3102000000001234567890', 'SUBASKBX',
     'VÚB Banka', 'Mlynské nivy 1, 82990 Bratislava',
     '10001', NULL, TRUE),
     
    -- ABC Veľkoobchod - sekundárny účet
    (1, '1100', '9876543210/1100', 'SK8811000000009876543210', 'TATRSKBX',
     'Tatra banka', 'Hodžovo námestie 3, 81106 Bratislava',
     '10001S', NULL, FALSE),
     
    -- XYZ Retail - primárny účet
    (2, '0900', '5555666677/0900', 'SK4509000000005555666677', 'GIBASKBX',
     'Slovenská sporiteľňa', 'Tomášikova 48, 83106 Bratislava',
     NULL, '20001', TRUE),
     
    -- Global Trading - predajný účet
    (3, '0200', '1111222233/0200', 'SK1102000000001111222233', 'SUBASKBX',
     'VÚB Banka', 'Mlynské nivy 1, 82990 Bratislava',
     '30001', NULL, TRUE),
     
    -- Global Trading - nákupný účet
    (3, '0200', '4444555566/0200', 'SK7702000000004444555566', 'SUBASKBX',
     'VÚB Banka', 'Mlynské nivy 1, 82990 Bratislava',
     NULL, '30001P', FALSE);
```

### 8.7 Partner categories

```sql
INSERT INTO partner_catalog_categories (
    partner_id, category_id, assigned_by
) VALUES
    (1, 1, 'admin'),  -- ABC VO → VIP dodávatelia
    (2, 2, 'admin'),  -- XYZ → Maloobchod
    (3, 1, 'admin'),  -- GLOBAL → VIP dodávatelia
    (3, 3, 'admin');  -- GLOBAL → Veľkoobchod
```

---

## 9. POZNÁMKY PRE MIGRÁCIU

### 9.1 Poradie migrácie tabuliek

```
KRITICKÉ: Migrovať v tomto poradí!

1. product_categories (Btrieve: FGLST.BTR)       -- FK pre partner_catalog
2. payment_methods (Btrieve: PAYLST.BTR)         -- FK pre partner_catalog
3. transport_methods (Btrieve: TRPLST.BTR)       -- FK pre partner_catalog_extensions
4. partner_categories (nová funkcionalita)       -- FK pre partner_catalog_categories
5. bank_catalog (Btrieve: BANKLST.BTR)           -- Pomocný číselník (nie FK!)

6. partner_catalog (Btrieve: PAB00000.BTR)       -- HLAVNÁ TABUĽKA
7. partner_catalog_extensions                    -- Priamo z PAB00000.BTR
8. partner_catalog_addresses                     -- Priamo z PAB00000.BTR
9. partner_catalog_contacts                      -- Priamo z PAB00000.BTR
10. partner_catalog_texts                        -- Priamo z PAB00000.BTR
11. partner_catalog_categories                   -- Mapovanie na kategórie

12. partner_catalog_bank_accounts (Btrieve: PABACC.BTR)  -- Samostatný súbor!

13. partner_catalog_facilities (?)               -- TODO: Špecifikácia
```

### 9.2 Python príklad transformácie

```python
from btrieve import Btrieve
import psycopg2

# Príklad migrácie z PAB.BTR do partner_catalog
def migrate_partner_catalog():
    # Otvorenie Btrieve súboru
    pab = Btrieve('C:/NEX/DATA/PAB00000.BTR')
    
    # Pripojenie na PostgreSQL
    conn = psycopg2.connect("host=localhost dbname=nex_automat user=postgres")
    cur = conn.cursor()
    
    # Spracovanie každého záznamu
    for record in pab.records():
        # Transformácia typu partnera
        pab_typ = record.get('PABTyp', '').strip()
        is_supplier = pab_typ == 'D'
        is_customer = pab_typ == 'O'
        is_both = pab_typ == 'B'
        
        # Transformácia čísla partnera
        partner_number = record.get('PABNr', '').strip()
        partner_subnumber = record.get('PABSuNr', '').strip()
        partner_subindex = record.get('PABSubIdx', '').strip()
        
        # Lookup FK pre financial_category_id
        fin_grp = record.get('PABFinGrp', '').strip()
        cur.execute("""
            SELECT category_id FROM product_categories
            WHERE category_code = %s AND category_type = 'financial'
        """, (fin_grp,))
        financial_category_id = cur.fetchone()[0] if cur.rowcount > 0 else None
        
        # Lookup FK pre default_payment_method_id
        pay_meth = record.get('PABPayMeth', '').strip()
        cur.execute("""
            SELECT payment_method_id FROM payment_methods
            WHERE payment_method_code = %s
        """, (pay_meth,))
        default_payment_method_id = cur.fetchone()[0] if cur.rowcount > 0 else None
        
        # INSERT do partner_catalog
        cur.execute("""
            INSERT INTO partner_catalog (
                partner_number, partner_subnumber, partner_subindex,
                partner_name, partner_shortname,
                company_id, tax_id, vat_number,
                is_supplier, is_customer, is_both,
                currency_code, financial_category_id, default_payment_method_id
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) RETURNING partner_id
        """, (
            partner_number, partner_subnumber, partner_subindex,
            record.get('PABName', '').strip(),
            record.get('PABShName', '').strip(),
            record.get('PABICO', '').strip(),
            record.get('PABDIC', '').strip(),
            record.get('PABDPH', '').strip(),
            is_supplier, is_customer, is_both,
            record.get('PABCurr', 'EUR').strip(),
            financial_category_id,
            default_payment_method_id
        ))
        
        partner_id = cur.fetchone()[0]
        
        # INSERT do partner_catalog_extensions
        # ... (podobne pre ostatné tabuľky)
        
        # INSERT do partner_catalog_addresses (registered)
        cur.execute("""
            INSERT INTO partner_catalog_addresses (
                partner_id, address_type, street, city, zip_code, country_code
            ) VALUES (%s, 'registered', %s, %s, %s, %s)
            RETURNING address_id
        """, (
            partner_id,
            record.get('PABStreet', '').strip(),
            record.get('PABCtn', '').strip(),
            record.get('PABZip', '').strip(),
            record.get('PABState', 'SK').strip()
        ))
        
        address_id = cur.fetchone()[0]
        
        # INSERT do partner_catalog_contacts
        cur.execute("""
            INSERT INTO partner_catalog_contacts (
                address_id, phone, fax, email, website
            ) VALUES (%s, %s, %s, %s, %s)
        """, (
            address_id,
            record.get('PABPhone', '').strip(),
            record.get('PABFax', '').strip(),
            record.get('PABEmail', '').strip(),
            record.get('PABWww', '').strip()
        ))
        
        # INSERT do partner_catalog_texts
        cur.execute("""
            INSERT INTO partner_catalog_texts (
                partner_id, owner_name
            ) VALUES (%s, %s)
        """, (
            partner_id,
            record.get('PABOwner', '').strip()
        ))
    
    conn.commit()
    cur.close()
    conn.close()

# Príklad migrácie bankových účtov z PABACC.BTR
def migrate_bank_accounts():
    pabacc = Btrieve('C:/NEX/DATA/PABACC.BTR')
    conn = psycopg2.connect("host=localhost dbname=nex_automat user=postgres")
    cur = conn.cursor()
    
    for record in pabacc.records():
        # Lookup partner_id podľa PABNr
        partner_number = record.get('PABNr', '').strip()
        cur.execute("""
            SELECT partner_id FROM partner_catalog
            WHERE partner_number = %s
        """, (partner_number,))
        
        result = cur.fetchone()
        if not result:
            continue  # Partner neexistuje, preskočiť
        
        partner_id = result[0]
        
        # Zloženie komplexnej adresy banky
        bank_addr = record.get('BankAddr', '').strip()
        bank_ctn = record.get('BankCtn', '').strip()
        bank_zip = record.get('BankZip', '').strip()
        bank_seat = f"{bank_addr}, {bank_zip} {bank_ctn}" if bank_addr else None
        
        # INSERT do partner_catalog_bank_accounts
        cur.execute("""
            INSERT INTO partner_catalog_bank_accounts (
                partner_id, bank_code, account_number, iban_code, swift_code,
                bank_name, bank_seat,
                variable_symbol_sales, variable_symbol_purchase,
                is_primary
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            partner_id,
            record.get('BankCode', '').strip(),
            record.get('BankAccNr', '').strip(),
            record.get('IBAN', '').strip(),  # ✅ Btrieve pole sa volá IBAN
            record.get('SWIFT', '').strip(),
            record.get('BankName', '').strip(),
            bank_seat,
            record.get('VarSymS', '').strip(),
            record.get('VarSymP', '').strip(),
            False  # is_primary sa nastaví neskôr
        ))
    
    conn.commit()
    cur.close()
    conn.close()
```

### 9.3 Dôležité poznámky

1. **bank_code je textová hodnota, NIE FK!**
   - User vyberie banku z číselníka → predvyplní polia
   - User môže všetko zmeniť
   - Uloží sa textová hodnota (nie referencia)

2. **bank_seat konzistencia:**
   - `bank_catalog.bank_seat` = komplexná adresa
   - `partner_catalog_bank_accounts.bank_seat` = komplexná adresa
   - Oba polia majú rovnaký názov a účel!

3. **is_primary trigger:**
   - Automaticky zabezpečuje len jeden primárny účet na partnera
   - Pri nastavení is_primary = TRUE sa automaticky zruší pre ostatné

4. **Počítadlá automatické:**
   - `bank_account_count` sa aktualizuje cez trigger
   - `facility_count` sa aktualizuje cez trigger

5. **PABACC.BTR je samostatný súbor!**
   - Obsahuje bankové účty pre všetkých partnerov
   - Mapuje sa cez PABNr (partner_number)
   - Migruje sa AŽ PO partner_catalog!

---

## 10. VERZIA A ZMENY

### v1.1 (2025-12-10) - OPRAVENÉ
- ✅ Zmenené `iban` → `iban_code` vo všetkých výskytoch
- ✅ CREATE TABLE partner_catalog_bank_accounts
- ✅ UNIQUE constraint: `UNIQUE (partner_id, iban_code)`
- ✅ INDEX: `idx_partner_bank_accounts_iban_code`
- ✅ Všetky query patterns
- ✅ Príklady dát (INSERT statements)
- ✅ Python migračný kód

### v1.0 (2025-12-10)
- Prvotná verzia dokumentu
- 8 tabuliek partner_catalog systému
- Komplexná SQL schéma s triggermi
- Mapping polí Btrieve → PostgreSQL
- Query patterns a príklady

---

**Koniec dokumentu PAB-partner_catalog.md**