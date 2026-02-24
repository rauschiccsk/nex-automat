# PABACC.BTR → partner_catalog_bank_accounts

**Kategória:** Catalogs - Katalóg partnerov  
**NEX Genesis:** PABACC.BTR  
**NEX Automat:** `partner_catalog_bank_accounts`  
**Vytvorené:** 2025-12-10  
**Aktualizované:** 2025-12-15  
**Status:** ✅ Pripravené na implementáciu

---

## PREHĽAD

### Btrieve súbor
- **Názov:** PABACC.BTR
- **Umiestnenie:** `C:\NEX\YEARACT\DIALS\PABACC.BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\DIALS\`
- **Účel:** Bankové účty obchodných partnerov

### Historický vývoj

**NEX Genesis (Btrieve):**
- PABACC.BTR = bankové účty obchodných partnerov
- Samostatný súbor (nie súčasť PAB.BTR)
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

## ŠTRUKTÚRA TABUĽKY

### partner_catalog_bank_accounts

**Popis:** Bankové účty partnerov

**Kľúčové polia:**
- `id` - SERIAL PRIMARY KEY
- `partner_id` - INTEGER NOT NULL FK (partner_catalog)
- `bank_code` - VARCHAR(10) (textová hodnota, NIE FK!)
- `bank_name` - VARCHAR(100)
- `bank_seat` - VARCHAR(100) (adresa banky)
- `iban_code` - VARCHAR(50) NOT NULL (primárny identifikátor)
- `swift_bic` - VARCHAR(20)
- `is_primary` - BOOLEAN DEFAULT FALSE (hlavný účet)
- Audit polia: created_by, created_at, updated_by, updated_at

**Constraints:**
- FK na partner_catalog(partner_id) ON DELETE CASCADE
- UNIQUE (partner_id, iban_code)

**Indexy:**
- PRIMARY KEY na id
- INDEX na partner_id
- INDEX na iban_code
- Partial INDEX na is_primary WHERE is_primary = TRUE
- INDEX na bank_code

**Triggery:**
- update_updated_at_column - automatická aktualizácia updated_at
- update_partner_bank_account_count - aktualizácia počítadla v partner_catalog
- ensure_single_primary_bank_account - len jeden is_primary = TRUE na partnera

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
- `bank_code` je textová hodnota, NIE FK na bank_catalog!

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
- (partner_id, iban_code) - každý IBAN musí byť unikátny pre partnera

**Znamená:**
- Partner môže mať viacero účtov
- Ale každý IBAN musí byť unikátny pre partnera
- Zahraničné IBANy (CZ, AT, HU...) podporované

### 3. is_primary flag

**Trigger zabezpečuje:**
- Vždy len **JEDEN** účet s `is_primary = TRUE` na partnera
- Pri nastavení is_primary = TRUE sa automaticky zruší pre ostatné účty

**Transformácia z Btrieve:**
```
Default = '*' → is_primary = TRUE
Default = ''  → is_primary = FALSE
```

### 4. Počítadlo účtov

**Automatická aktualizácia cez trigger:**
- `partner_catalog.bank_account_count`
- Pri INSERT → +1
- Pri DELETE → -1

---

## VZŤAHY S INÝMI TABUĽKAMI

### partner_catalog_bank_accounts → partner_catalog

**Relácia:** MANY-TO-ONE
- Mnoho bankových účtov môže patriť jednému partnerovi
- FK constraint s ON DELETE CASCADE (pri zmazaní partnera sa zmažú všetky účty)

**Use cases:**
- Získať všetky bankové účty partnera
- Nájsť primárny bankový účet partnera
- Štatistika počtu účtov na partnera
- Vyhľadanie partnera podľa IBAN

### bank_catalog (pomocný číselník)

**NIE JE FK relácia!**
- bank_code je len textová hodnota
- Používa sa pre predvyplnenie údajov
- Užívateľ môže zmeniť hodnoty

---

## VALIDAČNÉ PRAVIDLÁ

### 1. IBAN povinný
- `iban_code VARCHAR(50) NOT NULL`

### 2. Unikátny IBAN pre partnera
- `UNIQUE (partner_id, iban_code)`

### 3. Len jeden primárny účet
- Zabezpečené triggerom `ensure_single_primary_bank_account`
- Automaticky zruší is_primary pre ostatné účty pri nastavení nového primárneho

### 4. Validácia IBAN formátu (budúce rozšírenie)
- `CHECK (iban_code ~ '^[A-Z]{2}[0-9]{2}[A-Z0-9]+$')`
- Formát: 2 písmená (krajina) + 2 číslice (kontrola) + alfanumerický reťazec

---

## POZNÁMKY PRE MIGRÁCIU

### 1. Transformácia is_primary

**Z Btrieve:**
```
Default = '*' → is_primary = TRUE
Default = ''  → is_primary = FALSE
```

**Ak partner má viac účtov:**
- Prvý účet s Default = '*' → is_primary = TRUE
- Ostatné → is_primary = FALSE
- Ak žiadny účet nemá Default = '*' → prvý účet → is_primary = TRUE

### 2. Handling prázdnych polí

**Bank údaje môžu byť prázdne (zahraničné účty):**
- bank_code → NULL ak prázdne
- bank_name → NULL ak prázdne
- bank_seat → NULL ak prázdne
- swift_bic → NULL ak prázdne

**IBAN je vždy povinný:**
- Ak chýba IBAN → SKIP záznam (loguj chybu)

### 3. Poradie migrácie

**KRITICKÉ:**
1. ✅ Najprv migrovať **PAB.BTR** → partner_catalog
2. ✅ Potom migrovať **PABACC.BTR** → partner_catalog_bank_accounts
   - FK na partner_catalog(partner_id) musí existovať!

### 4. Validácia po migrácii

**Kontrola počtu účtov:**
- Overiť, že partner_catalog.bank_account_count sa zhoduje s actual_count
- Trigger mal aktualizovať počítadlo automaticky

**Kontrola primárnych účtov:**
- Každý partner by mal mať MAX 1 účet s is_primary = TRUE
- Ak má partner aspoň jeden účet, mal by mať jeden primárny

**Kontrola IBAN uniqueness:**
- Žiadny IBAN sa nesmie opakovať pre jedného partnera

### 5. Mapovanie partner_id

**Z Btrieve PaCode → PostgreSQL partner_id:**
- PaCode je Btrieve internal record number
- Treba vytvoriť mapping dictionary: PaCode → partner_id
- Lookup cez partner_number (PABNr)

**Príklad:**
```
1. Načítaj PAB.BTR → vytvor mapping: PaCode → partner_id
2. Pri migrácii PABACC.BTR použij mapping na lookup partner_id
```

---

## PRÍKLAD DÁT

### Partner s 2 bankovými účtami

```sql
-- Primárny účet (Tatra Banka)
INSERT INTO partner_catalog_bank_accounts (
    partner_id, bank_code, bank_name, bank_seat, 
    iban_code, swift_bic, is_primary, created_by
) VALUES (
    1, '1100', 'TATRA BANKA a.s.', 'Hodžovo námestie 3, Bratislava',
    'SK1234567890123456789012', 'TATRSKBX', TRUE, 'admin'
);

-- Sekundárny účet (Slovenská sporiteľňa)
INSERT INTO partner_catalog_bank_accounts (
    partner_id, bank_code, bank_name, bank_seat, 
    iban_code, swift_bic, is_primary, created_by
) VALUES (
    1, '0900', 'Slovenská sporiteľňa a.s.', 'Tomášikova 48, Bratislava',
    'SK9876543210987654321098', 'GIBASKBX', FALSE, 'admin'
);
```

### Partner so zahraničným účtom

```sql
-- Zahraničný účet (bez bank_code)
INSERT INTO partner_catalog_bank_accounts (
    partner_id, bank_code, bank_name, bank_seat, 
    iban_code, swift_bic, is_primary, created_by
) VALUES (
    2, NULL, 'Česká spořitelna a.s.', 'Praha, Česká republika',
    'CZ1234567890123456789012', 'GIBACZPX', TRUE, 'admin'
);
```

---

## ROZŠÍRENIA V BUDÚCNOSTI

### Možné pridanie polí

**Rozšírené informácie:**
- `account_purpose` - účel účtu (predaj, nákup, oboje)
- `account_currency` - mena účtu (EUR, USD, CZK...)
- `account_status` - status účtu (active, closed, suspended)

**Variabilné symboly:**
- `variable_symbol_sales` - VS pre predaj
- `variable_symbol_purchase` - VS pre nákup

**Poznámky:**
- `account_notes` - poznámky k účtu

---

## SÚVISIACE DOKUMENTY

- **partner_catalog** → `PAB-partner_catalog.md`
- **bank_catalog** → `BANKLST-bank_catalog.md` (číselník pre pomôcku)

---

**Vytvoril:** Claude & Zoltán  
**Dátum:** 2025-12-10  
**Aktualizované:** 2025-12-15  
**Verzia:** 1.1  
**Status:** ✅ Pripravené na implementáciu