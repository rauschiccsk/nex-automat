# Partners - Obchodní partneri

**Kategória:** Catalogs  
**Verzia:** 1.0  
**Dátum:** 2025-12-11  
**Status:** ✅ Kompletná dokumentácia

---

## PREHĽAD

Katalóg obchodných partnerov (dodávatelia, odberatelia) s kompletnými údajmi pre fakturáciu, účtovníctvo a obchodné transakcie.

**Zdokumentované:** 7 dokumentov (9 tabuliek)  
**Status:** ✅ Kompletné

---

## ŠTRUKTÚRA DOKUMENTÁCIE

```
partners/
├── INDEX.md                                    ✅ (v1.0)
└── tables/
    ├── PAB-partner_catalog.md                  ✅ Hlavný katalóg (8 tabuliek)
    ├── PABACC-partner_catalog_bank_accounts.md ✅ Bankové účty
    ├── PASUBC-partner_catalog_facilities.md    ✅ Prevádzkové jednotky
    ├── PACNCT-partner_catalog_contacts.md      ✅ Kontakty (univerzálna tabuľka)
    ├── PANOTI-partner_catalog_texts.md         ✅ Textové polia (univerzálna tabuľka)
    ├── PAGLST-partner_categories.md            ✅ Skupiny partnerov
    ├── PAYLST-payment_methods.md               ✅ Formy úhrady
    ├── TRPLST-transport_methods.md             ✅ Spôsoby dopravy
    └── BANKLST-bank_catalog.md                 ✅ Číselník bánk
```

---

## HLAVNÝ KATALÓG PARTNEROV

### PAB-partner_catalog.md (8 tabuliek)

**Btrieve súbory:** PAB00000.BTR, PABACC.BTR, PASUBC.BTR

**PostgreSQL tabuľky:**
1. `partner_catalog` - hlavné údaje partnera (16 polí)
2. `partner_catalog_extensions` - rozšírené údaje predaj/nákup (19 polí)
3. `partner_catalog_categories` - mapovanie skupín partnerov
4. `partner_catalog_addresses` - tri typy adries (registered, correspondence, invoice)
5. `partner_catalog_contacts` - kontaktné údaje (univerzálna tabuľka)
6. `partner_catalog_texts` - textové polia (univerzálna tabuľka)
7. `partner_catalog_bank_accounts` - bankové účty partnera
8. `partner_catalog_facilities` - prevádzkové jednotky

**Účel:** Komplexný katalóg obchodných partnerov s rozšírenými údajmi.

---

## DETAILNÁ DOKUMENTÁCIA

### 1. Bankové účty - PABACC-partner_catalog_bank_accounts.md

**Btrieve:** PABACC.BTR  
**Tabuľka:** `partner_catalog_bank_accounts`

**Kľúčové vlastnosti:**
- IBAN, SWIFT, číslo účtu
- Variabilné symboly pre predaj/nákup
- is_primary trigger (len jeden primárny účet)
- bank_seat - komplexná adresa banky

### 2. Prevádzkové jednotky - PASUBC-partner_catalog_facilities.md

**Btrieve:** PASUBC.BTR  
**Tabuľka:** `partner_catalog_facilities`

**Kľúčové vlastnosti:**
- Pobočky, sklady, výdajne partnera
- Adresy a kontakty jednotlivých jednotiek
- Spôsob dopravy pre jednotku
- facility_count trigger

### 3. Kontakty - PACNCT-partner_catalog_contacts.md

**Btrieve:** PAB00000.BTR, PACNCT.BTR  
**Tabuľka:** `partner_catalog_contacts` (univerzálna)

**Typy kontaktov:**
- `contact_type='address'` - kontakty pre adresu (FK address_id)
- `contact_type='person'` - kontaktné osoby (FK partner_id)

**Kľúčové vlastnosti:**
- Tituly, meno, priezvisko, funkcia
- Pracovné, mobilné, súkromné kontakty
- ⚠️ FirstName ↔ LastName SWAP pri migrácii!

### 4. Textové polia - PANOTI-partner_catalog_texts.md

**Btrieve:** PAB00000.BTR, PANOTI.BTR  
**Tabuľka:** `partner_catalog_texts` (univerzálna)

**Typy textov:**
- `text_type='owner_name'` - majiteľ/konateľ (1 riadok)
- `text_type='description'` - popis partnera (1 riadok)
- `text_type='notice'` - poznámky (N riadkov, line_number)

**Kľúčové vlastnosti:**
- Viacjazyčnosť (language: sk, en, cz...)
- Viacriadkové texty (line_number)
- UNIQUE(partner_id, text_type, line_number, language)

---

## ČÍSELNÍKY

### 5. Skupiny partnerov - PAGLST-partner_categories.md

**Btrieve:** PAGLST.BTR  
**Tabuľka:** `partner_categories`

**Typy skupín:**
- `category_type='supplier'` - skupiny dodávateľov (z PAGLST.BTR)
- `category_type='customer'` - skupiny odberateľov (manuálne)

**Poznámka:** PgcCode v PAB.BTR nemá číselník v NEX Genesis!

### 6. Formy úhrady - PAYLST-payment_methods.md

**Btrieve:** PAYLST.BTR  
**Tabuľka:** `payment_methods`

**Kľúčové vlastnosti:**
- Numerické ID + textový kód
- Hotovosť, karta, prevodom, dobierka...
- FK pre partner_catalog, invoices

### 7. Spôsoby dopravy - TRPLST-transport_methods.md

**Btrieve:** TRPLST.BTR  
**Tabuľka:** `transport_methods`

**Kľúčové vlastnosti:**
- Numerické ID + textový kód
- Kuriér, pošta, osobný odber...
- FK pre partner_catalog_extensions, facilities

### 8. Číselník bánk - BANKLST-bank_catalog.md

**Btrieve:** BANKLST.BTR  
**Tabuľka:** `bank_catalog`

**Kľúčové vlastnosti:**
- Zoznam bánk na Slovensku
- SWIFT kódy, adresy sídiel
- **Pomocný číselník** (nie FK!)

---

## PRIORITA MIGRÁCIE

### Fáza 1: Číselníky (✅ Hotovo)

```
1. PAGLST.BTR → partner_categories                ✅
2. PAYLST.BTR → payment_methods                   ✅
3. TRPLST.BTR → transport_methods                 ✅
4. BANKLST.BTR → bank_catalog                     ✅
```

### Fáza 2: Hlavný katalóg (✅ Hotovo)

```
5. PAB00000.BTR → partner_catalog + extensions + addresses  ✅
```

### Fáza 3: Závislé tabuľky (✅ Hotovo)

```
6. PABACC.BTR → partner_catalog_bank_accounts     ✅
7. PASUBC.BTR → partner_catalog_facilities        ✅
8. PACNCT.BTR → partner_catalog_contacts (person) ✅
9. PANOTI.BTR → partner_catalog_texts (notice)    ✅
```

---

## KĽÚČOVÉ PRINCÍPY

### 1. Univerzálne tabuľky s typom

```sql
-- Kontakty
partner_catalog_contacts WHERE contact_type IN ('address', 'person')

-- Textové polia
partner_catalog_texts WHERE text_type IN ('owner_name', 'description', 'notice')

-- Skupiny partnerov
partner_categories WHERE category_type IN ('supplier', 'customer')
```

### 2. Numerické ID pre číselníky

```sql
payment_method_id SERIAL PRIMARY KEY  -- 1, 2, 3...
payment_method_code VARCHAR(10)        -- "HOT", "KAR"...
```

**Výhody:**
- Konzistentné referencovanie (FK)
- Rýchlejšie JOIN operácie
- Textový kód pre ľudskú čitateľnosť

### 3. Referenčná integrita

```sql
ON DELETE RESTRICT  → Master data (partneri, kategórie)
ON DELETE CASCADE   → Závislé dáta (extensions, addresses, contacts)
BEZ FK              → Archívne dokumenty (invoices)
```

### 4. Automatické triggery

```sql
-- Počítadlá
bank_account_count  -- aktualizuje sa pri INSERT/DELETE
facility_count      -- aktualizuje sa pri INSERT/DELETE

-- Primárny účet
is_primary          -- zabezpečuje len jeden primárny účet

-- Timestamp
updated_at          -- aktualizuje sa pri UPDATE
```

---

## KONZISTENCIA NÁZVOV POLÍ

```sql
*_id        INTEGER       -- FK primárny kľúč
*_code      VARCHAR       -- Textový kód
*_name      VARCHAR       -- Názov
*_seat      VARCHAR(200)  -- Komplexná adresa (sídlo banky)
iban_code   VARCHAR(50)   -- ⚠️ NIE "iban"!
```

---

## ŠTATISTIKA

**Dokumenty:** 7  
**Tabuľky:** 9  
**Btrieve súbory:** 7  
**Status:** ✅ 100% kompletné

---

## VERZIA A ZMENY

### v1.0 (2025-12-11)
- Prvotná verzia
- Kompletná dokumentácia partner katalógu
- 7 dokumentov, 9 tabuliek
- Nová štruktúra adresárov

---

**Koniec dokumentu partners/INDEX.md**