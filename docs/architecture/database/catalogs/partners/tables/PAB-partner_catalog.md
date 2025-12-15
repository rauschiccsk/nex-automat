# PAB.BTR → partner_catalog (8 tabuliek)

**Kategória:** Catalogs - Číselníky  
**NEX Genesis:** PAB.BTR (Partner Address Book)  
**NEX Automat:** `partner_catalog` + 7 súvisiacich tabuliek  
**Vytvorené:** 2025-12-10  
**Aktualizované:** 2025-12-15  
**Status:** ✅ Pripravené na implementáciu

---

## PREHĽAD

### Btrieve súbor
- **Názov:** PAB.BTR
- **Umiestnenie:** `C:\NEX\YEARACT\DIALS\PAB.BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\DIALS\`
- **Účel:** Komplexný katalóg obchodných partnerov (Partner Address Book)

**Poznámka:** PAB.BTR je jeden z najkomplexnejších súborov v NEX Genesis s viac ako 100 poliami v pôvodnej štruktúre.

### PostgreSQL tabuľky

**8 tabuliek:**
1. `partner_catalog` - hlavné údaje partnera (16 polí)
2. `partner_catalog_extensions` - rozšírené údaje predaj/nákup (19 polí)
3. `partner_catalog_categories` - mapovanie na skupiny partnerov
4. `partner_catalog_addresses` - tri typy adries (registered, correspondence, invoice)
5. `partner_catalog_contacts` - kontaktné údaje pre každý typ adresy
6. `partner_catalog_texts` - textové polia (owner_name)
7. `partner_catalog_bank_accounts` - bankové účty partnera (PABACC.BTR)
8. `partner_catalog_facilities` - prevádzkové jednotky (⏳ TODO)

**Účel:** Komplexný katalóg obchodných partnerov (dodávatelia, odberatelia) s rozšírenými údajmi potrebnými pre fakturáciu, účtovníctvo a obchodné transakcie.

---

## ŠTRUKTÚRA TABULIEK

### partner_catalog (hlavná tabuľka)

**Kľúčové polia:**
- `partner_id` - SERIAL PRIMARY KEY
- `partner_number` - VARCHAR(20) NOT NULL (hlavné číslo)
- `partner_subnumber` - VARCHAR(10) (podcíslo)
- `partner_subindex` - VARCHAR(5) (index)
- `partner_name` - VARCHAR(100) NOT NULL
- `partner_shortname` - VARCHAR(50)
- `company_id` - VARCHAR(20) (IČO)
- `tax_id` - VARCHAR(20) (DIČ)
- `vat_number` - VARCHAR(20) (IČ DPH)
- `is_supplier`, `is_customer`, `is_both` - BOOLEAN (typ partnera)
- `currency_code` - VARCHAR(3) DEFAULT 'EUR'
- `financial_category_id` - FK na product_categories
- `default_payment_method_id` - FK na payment_methods
- `bank_account_count`, `facility_count` - INTEGER (počítadlá)
- Audit polia: is_active, created_at, updated_at

**Unique constraint:** (partner_number, partner_subnumber, partner_subindex)

### partner_catalog_extensions

**Kľúčové polia:**
- `extension_id` - SERIAL PRIMARY KEY
- `partner_id` - FK NOT NULL
- Predaj: sales_payment_method_id, sales_transport_method_id, sales_discount_percent, sales_credit_limit
- Nákup: purchase_payment_method_id, purchase_transport_method_id, purchase_discount_percent, purchase_credit_limit
- `default_price_list_number` - VARCHAR(20)
- `sales_contact_person`, `purchase_contact_person` - VARCHAR(100)
- `sales_notes`, `purchase_notes`, `internal_notes` - TEXT
- Štatistika: last_sales_date, last_purchase_date, total_sales_amount, total_purchase_amount

**Unique constraint:** (partner_id) - ONE-TO-ONE vzťah

### partner_catalog_categories

**Kľúčové polia:**
- `mapping_id` - SERIAL PRIMARY KEY
- `partner_id` - FK NOT NULL
- `category_id` - FK NOT NULL (partner_categories)
- `assigned_at`, `assigned_by` - audit

**Unique constraint:** (partner_id, category_id) - MANY-TO-MANY

### partner_catalog_addresses

**Kľúčové polia:**
- `address_id` - SERIAL PRIMARY KEY
- `partner_id` - FK NOT NULL
- `address_type` - VARCHAR(20) NOT NULL ('registered', 'correspondence', 'invoice')
- `street`, `city`, `zip_code`, `country_code` - adresné údaje
- `address_note` - TEXT

**Unique constraint:** (partner_id, address_type) - každý typ len raz

### partner_catalog_contacts

**Kľúčové polia:**
- `contact_id` - SERIAL PRIMARY KEY
- `address_id` - FK NOT NULL
- `phone`, `mobile`, `fax`, `email`, `website` - kontakty
- `contact_person`, `contact_position` - kontaktná osoba

**Validácia:** email format check

### partner_catalog_texts

**Kľúčové polia:**
- `text_id` - SERIAL PRIMARY KEY
- `partner_id` - FK NOT NULL
- `owner_name` - VARCHAR(200) (majiteľ/konateľ spoločnosti)

**Unique constraint:** (partner_id) - ONE-TO-ONE vzťah

### partner_catalog_bank_accounts

**Kľúčové polia:**
- `account_id` - SERIAL PRIMARY KEY
- `partner_id` - FK NOT NULL
- `bank_code` - VARCHAR(10) ⚠️ TEXTOVÁ HODNOTA, NIE FK!
- `account_number`, `iban_code`, `swift_code` - bankové údaje
- `bank_name`, `bank_seat` - údaje banky
- `variable_symbol_sales`, `variable_symbol_purchase` - VS
- `is_primary` - BOOLEAN (len jeden účet môže byť primárny)

**Unique constraint:** (partner_id, iban_code)
**Validácia:** IBAN format check
**Trigger:** ensure_single_primary_bank_account (len jeden is_primary = TRUE)

### partner_catalog_facilities

⏳ **TODO:** Špecifikácia po potvrdení od používateľa

---

## MAPPING POLÍ

### Polia ktoré SA PRENÁŠAJÚ

#### Základné identifikátory

| Btrieve Field | Typ | → | PostgreSQL Column | Typ | Poznámka |
|---------------|-----|---|-------------------|-----|----------|
| PABNr | Str20 | → | partner_number | VARCHAR(20) | Povinné číslo partnera |
| PABSuNr | Str10 | → | partner_subnumber | VARCHAR(10) | Voliteľné podcíslo |
| PABSubIdx | Str5 | → | partner_subindex | VARCHAR(5) | Voliteľný index |
| PABName | Str100 | → | partner_name | VARCHAR(100) | Povinný názov |
| PABShName | Str50 | → | partner_shortname | VARCHAR(50) | Skrátený názov |

#### Identifikačné čísla

| Btrieve Field | Typ | → | PostgreSQL Column | Typ | Poznámka |
|---------------|-----|---|-------------------|-----|----------|
| PABICO | Str20 | → | company_id | VARCHAR(20) | IČO |
| PABDIC | Str20 | → | tax_id | VARCHAR(20) | DIČ |
| PABDPH | Str20 | → | vat_number | VARCHAR(20) | IČ DPH |

#### Typ partnera

| Btrieve Field | Typ | → | PostgreSQL Column | Typ | Transformácia |
|---------------|-----|---|-------------------|-----|---------------|
| PABTyp | Char1 | → | is_supplier / is_customer / is_both | BOOLEAN | 'D' → is_supplier=TRUE<br>'O' → is_customer=TRUE<br>'B' → is_both=TRUE |

#### Finančné údaje

| Btrieve Field | Typ | → | PostgreSQL Column | Typ | Poznámka |
|---------------|-----|---|-------------------|-----|----------|
| PABCurr | Str3 | → | currency_code | VARCHAR(3) | Mena (EUR, USD...) |
| PABFinGrp | Str10 | → | financial_category_id | INTEGER FK | Lookup na product_categories |
| PABPayMeth | Str10 | → | default_payment_method_id | INTEGER FK | Lookup na payment_methods |

#### Adresy (3 typy: registered, correspondence, invoice)

| Btrieve Field | Typ | → | PostgreSQL Column | Typ | Poznámka |
|---------------|-----|---|-------------------|-----|----------|
| PABStreet | Str100 | → | street | VARCHAR(100) | Ulica |
| PABCtn | Str100 | → | city | VARCHAR(100) | Mesto |
| PABZip | Str20 | → | zip_code | VARCHAR(20) | PSČ |
| PABState | Str2 | → | country_code | VARCHAR(2) | Štát (SK) |

#### Kontakty

| Btrieve Field | Typ | → | PostgreSQL Column | Typ | Poznámka |
|---------------|-----|---|-------------------|-----|----------|
| PABPhone | Str50 | → | phone | VARCHAR(50) | Telefón |
| PABFax | Str50 | → | fax | VARCHAR(50) | Fax |
| PABEmail | Str100 | → | email | VARCHAR(100) | Email |
| PABWww | Str200 | → | website | VARCHAR(200) | Web |

#### Rozšírené údaje - predaj

| Btrieve Field | Typ | → | PostgreSQL Column | Typ | Poznámka |
|---------------|-----|---|-------------------|-----|----------|
| PABPayMeth | Str10 | → | sales_payment_method_id | INTEGER FK | Spôsob platby |
| PABTrpMeth | Str10 | → | sales_transport_method_id | INTEGER FK | Spôsob dopravy |
| PABDisc | Decimal | → | sales_discount_percent | DECIMAL(5,2) | Zľava % |
| PABCreditLim | Decimal | → | sales_credit_limit | DECIMAL(15,2) | Úverový limit |
| PABPrcLst | Str20 | → | default_price_list_number | VARCHAR(20) | Cenník |
| PABContact | Str100 | → | sales_contact_person | VARCHAR(100) | Kontaktná osoba |
| PABNote1 | Text | → | sales_notes | TEXT | Poznámky predaj |

#### Rozšírené údaje - nákup

| Btrieve Field | Typ | → | PostgreSQL Column | Typ | Poznámka |
|---------------|-----|---|-------------------|-----|----------|
| PABPayMethP | Str10 | → | purchase_payment_method_id | INTEGER FK | Spôsob platby |
| PABTrpMethP | Str10 | → | purchase_transport_method_id | INTEGER FK | Spôsob dopravy |
| PABDiscP | Decimal | → | purchase_discount_percent | DECIMAL(5,2) | Zľava % |
| PABCreditLimP | Decimal | → | purchase_credit_limit | DECIMAL(15,2) | Úverový limit |
| PABContactP | Str100 | → | purchase_contact_person | VARCHAR(100) | Kontaktná osoba |
| PABNote2 | Text | → | purchase_notes | TEXT | Poznámky nákup |

#### Textové polia

| Btrieve Field | Typ | → | PostgreSQL Column | Typ | Poznámka |
|---------------|-----|---|-------------------|-----|----------|
| PABOwner | Str200 | → | owner_name | VARCHAR(200) | Majiteľ/konateľ |

#### Bankové účty (PABACC.BTR)

| Btrieve Field | Typ | → | PostgreSQL Column | Typ | Poznámka |
|---------------|-----|---|-------------------|-----|----------|
| BankCode | Str10 | → | bank_code | VARCHAR(10) | ⚠️ Textová hodnota |
| BankAccNr | Str50 | → | account_number | VARCHAR(50) | Číslo účtu |
| IBAN | Str50 | → | iban_code | VARCHAR(50) | IBAN |
| SWIFT | Str20 | → | swift_code | VARCHAR(20) | SWIFT kód |
| BankName | Str100 | → | bank_name | VARCHAR(100) | Názov banky |
| BankAddr + BankCtn + BankZip | Str | → | bank_seat | VARCHAR(200) | Komplexná adresa |
| VarSymS | Str20 | → | variable_symbol_sales | VARCHAR(20) | VS predaj |
| VarSymP | Str20 | → | variable_symbol_purchase | VARCHAR(20) | VS nákup |

### Polia ktoré SA NEPRENÁŠAJÚ

| Btrieve Field | Dôvod neprenášania |
|--------------|--------------------|
| PABRecNo | Btrieve internal record number - nahradené SERIAL |
| PABLocked | Zámok záznamu - PostgreSQL MVCC |
| PABLastUpd | Nahradené audit poľami (updated_at) |
| PABDeleted | Nahradené is_active flag |
| PABVersion | Verzovanie - riešené inak |
| PAB_Reserved_* | Rezervované polia - nepoužívané |

---

## BIZNIS LOGIKA

### 1. Partner Types (is_supplier, is_customer, is_both)

**Pôvodný systém (Btrieve):**
- PABTyp = 'D' (dodávateľ)
- PABTyp = 'O' (odberateľ)
- PABTyp = 'B' (oboje)

**Nový systém (PostgreSQL):**
- Dodávateľ: is_supplier = TRUE, is_customer = FALSE, is_both = FALSE
- Odberateľ: is_supplier = FALSE, is_customer = TRUE, is_both = FALSE
- Oboje: is_supplier = FALSE, is_customer = FALSE, is_both = TRUE

**Business rule:** Aspoň jeden flag musí byť TRUE (CHECK constraint).

### 2. Adresy a kontakty

**Tri typy adries:**
1. **registered** - sídlo spoločnosti (povinné)
2. **correspondence** - korešpondenčná adresa (voliteľné)
3. **invoice** - fakturačná adresa (voliteľné)

**Kontakty:** Každá adresa môže mať vlastné kontaktné údaje (telefón, email, atď.)

**Vzťah:** partner_catalog → partner_catalog_addresses → partner_catalog_contacts

### 3. Bankové účty

**Business rules:**
1. Partner môže mať viacero bankových účtov
2. Len jeden účet môže byť primárny (is_primary = TRUE)
3. IBAN musí byť unique pre partnera
4. **bank_code je TEXTOVÁ hodnota, NIE FK na bank_catalog!**

**Workflow pri pridávaní účtu:**
1. User vyberie banku z číselníka (bank_catalog)
2. Systém predvyplní polia: bank_code, bank_name, bank_seat
3. User môže všetko zmeniť (nie je to záväzné)
4. Uloží sa textová hodnota (nie referencia)

**Trigger:** ensure_single_primary_bank_account
- Pri nastavení is_primary = TRUE automaticky zruší primárny flag pre ostatné účty partnera

### 4. Počítadlá (bank_account_count, facility_count)

**Automatická aktualizácia cez triggery:**
- Pri INSERT do partner_catalog_bank_accounts → bank_account_count + 1
- Pri DELETE z partner_catalog_bank_accounts → bank_account_count - 1
- Analogicky pre facility_count

### 5. Rozšírené údaje (extensions)

**ONE-TO-ONE vzťah:** Každý partner má maximálne jeden záznam v partner_catalog_extensions

**Obsahuje:**
- Obchodné podmienky pre predaj (platba, doprava, zľava, úver)
- Obchodné podmienky pre nákup (platba, doprava, zľava, úver)
- Cenové politiky (default_price_list_number)
- Kontaktné osoby (sales/purchase)
- Poznámky (sales/purchase/internal)
- Štatistické údaje (last_sales_date, total_sales_amount...)

---

## VZŤAHY S INÝMI TABUĽKAMI

### Incoming (z iných tabuliek)

**FK do partner_catalog:**
- product_categories (financial_category_id)
- payment_methods (default_payment_method_id)

**FK do partner_catalog_extensions:**
- payment_methods (sales_payment_method_id, purchase_payment_method_id)
- transport_methods (sales_transport_method_id, purchase_transport_method_id)

**FK do partner_catalog_categories:**
- partner_categories (category_id)

### Štruktúra referencií

```
product_categories ─┐
payment_methods ────┼──→ partner_catalog
                    │         │
                    │         ├──→ partner_catalog_extensions ←── payment_methods
                    │         │                                   transport_methods
                    │         ├──→ partner_catalog_categories ←── partner_categories
                    │         │
                    │         ├──→ partner_catalog_addresses
                    │         │         │
                    │         │         └──→ partner_catalog_contacts
                    │         │
                    │         ├──→ partner_catalog_texts
                    │         │
                    │         ├──→ partner_catalog_bank_accounts
                    │         │
                    │         └──→ partner_catalog_facilities
```

### Outgoing (do iných tabuliek)

**KRITICKÉ:** Archívne dokumenty (faktúry, príjemky) nemajú FK constraint na partner_catalog!

**Dôvod:** Všetky údaje sú snapshot v dokumente (právny požiadavok SK účtovných predpisov).

**Použitie:**
- invoices (supplier_invoice_heads, customer_invoice_heads)
- purchase_orders
- sales_orders
- delivery_notes
- ...

**Implementácia:** Denormalizované údaje - partner_id sa ukladá, ale BEZ FK constraint.

---

## VALIDAČNÉ PRAVIDLÁ

### CHECK Constraints

**partner_catalog:**
- Partner type: `CHECK (is_supplier OR is_customer OR is_both)`
- Currency code: `CHECK (LENGTH(currency_code) = 3)`
- Unique number: `UNIQUE (partner_number, partner_subnumber, partner_subindex)`

**partner_catalog_extensions:**
- Sales discount: `CHECK (sales_discount_percent BETWEEN 0 AND 100)`
- Purchase discount: `CHECK (purchase_discount_percent BETWEEN 0 AND 100)`
- Unique partner: `UNIQUE (partner_id)`

**partner_catalog_addresses:**
- Address type: `CHECK (address_type IN ('registered', 'correspondence', 'invoice'))`
- Country code: `CHECK (LENGTH(country_code) = 2)`
- Unique type: `UNIQUE (partner_id, address_type)`

**partner_catalog_contacts:**
- Email format: `CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')`

**partner_catalog_bank_accounts:**
- IBAN format: `CHECK (iban_code ~* '^[A-Z]{2}[0-9]{2}[A-Z0-9]+$')`
- Unique IBAN: `UNIQUE (partner_id, iban_code)`

### Triggery

**ensure_single_primary_bank_account:**
- Pri nastavení is_primary = TRUE zruší primárny flag pre ostatné účty partnera
- Zabezpečuje, že len jeden účet môže byť primárny

**update_partner_bank_account_count:**
- Pri INSERT/DELETE aktualizuje počítadlo v partner_catalog

**update_updated_at_column:**
- Pri každom UPDATE nastaví updated_at na CURRENT_TIMESTAMP

---

## POZNÁMKY PRE MIGRÁCIU

### 1. Poradie migrácie tabuliek

**KRITICKÉ:** Migrovať v tomto poradí!

```
1. product_categories (Btrieve: FGLST.BTR)       -- FK pre partner_catalog
2. payment_methods (Btrieve: PAYLST.BTR)         -- FK pre partner_catalog
3. transport_methods (Btrieve: TRPLST.BTR)       -- FK pre extensions
4. partner_categories (nová funkcionalita)       -- FK pre categories
5. bank_catalog (Btrieve: BANKLST.BTR)           -- Pomocný číselník

6. partner_catalog (Btrieve: PAB.BTR)            -- HLAVNÁ TABUĽKA
7. partner_catalog_extensions                    -- Priamo z PAB.BTR
8. partner_catalog_addresses                     -- Priamo z PAB.BTR
9. partner_catalog_contacts                      -- Priamo z PAB.BTR
10. partner_catalog_texts                        -- Priamo z PAB.BTR
11. partner_catalog_categories                   -- Mapovanie na kategórie

12. partner_catalog_bank_accounts (Btrieve: PABACC.BTR)  -- Samostatný súbor!

13. partner_catalog_facilities                   -- TODO: Špecifikácia
```

### 2. Transformácia typu partnera

**Btrieve PABTyp → PostgreSQL boolean fields:**

```
'D' → is_supplier=TRUE, is_customer=FALSE, is_both=FALSE
'O' → is_supplier=FALSE, is_customer=TRUE, is_both=FALSE
'B' → is_supplier=FALSE, is_customer=FALSE, is_both=TRUE
```

### 3. Lookup FK polí

**financial_category_id:**
- Lookup na product_categories WHERE category_code = PABFinGrp AND category_type = 'financial'

**default_payment_method_id:**
- Lookup na payment_methods WHERE payment_method_code = PABPayMeth

**sales_transport_method_id:**
- Lookup na transport_methods WHERE transport_method_code = PABTrpMeth

### 4. Spracovanie adries

**Tri typy adries z jedného Btrieve záznamu:**
- registered: PABStreet, PABCtn, PABZip, PABState
- correspondence: (ak existujú odlišné polia v Btrieve)
- invoice: (ak existujú odlišné polia v Btrieve)

**Kontakty:** Priradené k address_id typu 'registered'

### 5. Bankové účty (PABACC.BTR)

**KRITICKÉ:** PABACC.BTR je samostatný súbor!
- Obsahuje bankové účty pre všetkých partnerov
- Mapuje sa cez PABNr (partner_number)
- Migruje sa AŽ PO partner_catalog!

**Transformácia bank_seat:**
- BankAddr + BankCtn + BankZip → "ulica, PSČ mesto"
- NULL hodnoty sa preskakujú

**is_primary nastavenie:**
- Prvý účet partnera → is_primary = TRUE
- Ostatné → is_primary = FALSE

### 6. bank_code je textová hodnota

**DÔLEŽITÉ:**
- bank_code nie je FK na bank_catalog!
- Je to textová kópia z číselníka
- User môže zmeniť hodnotu
- Ukladá sa bez referencie

### 7. Počítadlá

**bank_account_count, facility_count:**
- Automaticky aktualizované cez triggery
- Pri migrácii sa inicializujú na 0
- Naplnia sa po migrácii bank_accounts a facilities

---

## ROZŠÍRENIA V BUDÚCNOSTI

### Možné pridanie polí

**partner_catalog:**
- `partner_rating` - hodnotenie partnera (A, B, C)
- `tax_exemption` - oslobodenie od DPH
- `payment_terms_days` - splatnosť v dňoch

**partner_catalog_extensions:**
- `preferred_delivery_time` - preferovaný čas dodávky
- `minimum_order_amount` - minimálna hodnota objednávky
- `loyalty_program_member` - člen vernostného programu

**partner_catalog_facilities:**
- Kompletná špecifikácia prevádzkových jednotiek

---

## SÚVISIACE DOKUMENTY

- **bank_catalog** → `BANKLST-bank_catalog.md`
- **partner_catalog_bank_accounts** → `PABACC-partner_catalog_bank_accounts.md`
- **partner_categories** → `PAGLST-partner_categories.md`
- **payment_methods** → `PAYLST-payment_methods.md`
- **transport_methods** → `TRPLST-transport_methods.md`

---

**Vytvoril:** Claude & Zoltán  
**Dátum:** 2025-12-10  
**Aktualizované:** 2025-12-15  
**Verzia:** 1.1  
**Status:** ✅ Pripravené na implementáciu