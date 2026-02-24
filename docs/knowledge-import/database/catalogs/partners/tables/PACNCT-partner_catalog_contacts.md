# PAB.BTR + PACNCT.BTR → partner_catalog_contacts

**Kategória:** Catalogs - Katalóg partnerov  
**NEX Genesis:** PAB.BTR + PACNCT.BTR  
**NEX Automat:** `partner_catalog_contacts`  
**Vytvorené:** 2025-12-11  
**Aktualizované:** 2025-12-15  
**Status:** ✅ Pripravené na implementáciu

---

## PREHĽAD

### Btrieve súbory

**PAB.BTR:**
- **Názov:** PAB.BTR
- **Umiestnenie:** `C:\NEX\YEARACT\DIALS\PAB.BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\DIALS\`
- **Účel:** Partner Address Book - kontakty pre adresy

**PACNCT.BTR:**
- **Názov:** PACNCT.BTR
- **Umiestnenie:** `C:\NEX\YEARACT\DIALS\PACNCT.BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\DIALS\`
- **Účel:** Partner Contacts - kontaktné osoby partnerov

### PostgreSQL tabuľka

**Tabuľka:** `partner_catalog_contacts`  
**Účel:** Univerzálna tabuľka pre všetky kontaktné údaje partnerov s podporou 2 typov:
- `address` - kontakty viazané na adresu (telefón, email pre sídlo/pobočku)
- `person` - kontaktné osoby partnera (zamestnanci, obchodníci, VIP osoby)

---

## ŠTRUKTÚRA TABUĽKY

### partner_catalog_contacts

**Popis:** Univerzálna tabuľka pre kontaktné údaje

**Kľúčové polia:**
- `contact_id` - SERIAL PRIMARY KEY
- `contact_type` - VARCHAR(20) NOT NULL ('address', 'person')
- `address_id` - INTEGER FK (pre contact_type='address')
- `partner_id` - INTEGER FK (pre contact_type='person')

**Polia pre contact_type='address' (z PAB.BTR):**
- `phone`, `mobile`, `fax`, `email`, `website` - kontaktné údaje adresy
- `contact_person`, `contact_position` - kontaktná osoba (len meno)

**Polia pre contact_type='person' (z PACNCT.BTR):**
- `title_before`, `first_name`, `last_name`, `full_name`, `title_after` - tituly a meno
- `function`, `sex_mark`, `accost` - funkcia a údaje
- `work_tel`, `work_extension`, `work_email` - pracovné kontakty
- `mobile_tel`, `private_tel`, `private_email` - mobilné a súkromné kontakty
- `notice` - poznámka

**Audit polia:** created_at, created_by, updated_at, updated_by

**Constraints:**
- CHECK contact_type IN ('address', 'person')
- CHECK pre validáciu FK (address_id alebo partner_id podľa typu)
- CHECK sex_mark IN ('M', 'W')
- CHECK email formát (3 polia)
- ON DELETE CASCADE na oba FK

**Indexy:**
- PRIMARY KEY na contact_id
- INDEX na contact_type
- Partial INDEX na address_id WHERE contact_type = 'address'
- Partial INDEX na partner_id WHERE contact_type = 'person'
- INDEX na full_name, work_tel, mobile_tel, email, work_email

**Trigger:**
- update_updated_at_column - automatická aktualizácia updated_at

---

## MAPPING POLÍ

### Mapovanie z PAB.BTR (contact_type='address')

| Btrieve Field | Typ | → | PostgreSQL Column | Typ | Poznámka |
|---------------|-----|---|-------------------|-----|----------|
| PABPhone | Str50 | → | phone | VARCHAR(50) | Telefón |
| PABMobile | Str50 | → | mobile | VARCHAR(50) | Mobilný telefón |
| PABFax | Str50 | → | fax | VARCHAR(50) | Fax |
| PABEmail | Str100 | → | email | VARCHAR(100) | Email |
| PABWww | Str200 | → | website | VARCHAR(200) | Web stránka |
| PABContact | Str100 | → | contact_person | VARCHAR(100) | Meno kontaktu |
| PABPosition | Str100 | → | contact_position | VARCHAR(100) | Funkcia |
| - | - | → | contact_type | VARCHAR(20) | Fixed: 'address' |
| - | - | → | address_id | INTEGER FK | FK z PAB adresy |

### Mapovanie z PACNCT.BTR (contact_type='person')

| Btrieve Field | Typ | → | PostgreSQL Column | Typ | Poznámka |
|---------------|-----|---|-------------------|-----|----------|
| **Identifikátor** | | | | | |
| PaCode | longint | → | partner_id | INTEGER FK | FK na partner_catalog |
| - | - | → | contact_type | VARCHAR(20) | Fixed: 'person' |
| **Meno a tituly** | | | | | |
| TitulBef | Str10 | → | title_before | VARCHAR(10) | Titul pred menom |
| FirstName | Str15 | → | last_name | VARCHAR(15) | **SWAP!** Priezvisko |
| LastName | Str15 | → | first_name | VARCHAR(15) | **SWAP!** Meno |
| FullName | Str30 | → | full_name | VARCHAR(30) | Plné meno |
| TitulAft | Str10 | → | title_after | VARCHAR(10) | Titul za menom |
| **Funkcia a údaje** | | | | | |
| Function | Str30 | → | function | VARCHAR(30) | Funkcia |
| SexMark | Str1 | → | sex_mark | VARCHAR(1) | M/W |
| Accost | Str30 | → | accost | VARCHAR(30) | Oslovenie |
| **Pracovné kontakty** | | | | | |
| WorkTel | Str20 | → | work_tel | VARCHAR(20) | Pracovný telefón |
| WorkSec | Str5 | → | work_extension | VARCHAR(5) | Klapka |
| WorkEml | Str30 | → | work_email | VARCHAR(30) | Pracovný email |
| **Mobilné a súkromné** | | | | | |
| MobTel | Str20 | → | mobile_tel | VARCHAR(20) | Mobilný telefón |
| PrivTel | Str20 | → | private_tel | VARCHAR(20) | Súkromný telefón |
| PrivEml | Str30 | → | private_email | VARCHAR(30) | Súkromný email |
| **Poznámka** | | | | | |
| Notice | Str30 | → | notice | VARCHAR(30) | Poznámka |
| **Audit** | | | | | |
| CrtUser | Str8 | → | created_by | VARCHAR(50) | Vytvoril |
| CrtDate, CrtTime | Date+Time | → | created_at | TIMESTAMP | Dátum vytvorenia |
| ModUser | Str8 | → | updated_by | VARCHAR(50) | Zmenil |
| ModDate, ModTime | Date+Time | → | updated_at | TIMESTAMP | Dátum zmeny |

### Polia ktoré SA NEPRENÁŠAJÚ

| Btrieve Field | Dôvod neprenášania |
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

## BIZNIS LOGIKA

### 1. Typy kontaktov

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

### 2. FirstName vs LastName - SWAP pri migrácii!

**KRITICKÉ! V NEX Genesis PACNCT.BTR je to OPAČNE:**
- Btrieve `FirstName` = priezvisko (Nový)
- Btrieve `LastName` = meno (Ján)
- Btrieve `FullName` = "Ing. Ján Nový, PhD."

**V NEX Automat PostgreSQL je to SPRÁVNE:**
- PostgreSQL `first_name` = meno (Ján)
- PostgreSQL `last_name` = priezvisko (Nový)
- PostgreSQL `full_name` = kompletné meno s titulmi

**Pri migrácii MUSÍME SWAPOVAŤ:**
- Btrieve FirstName → PostgreSQL `last_name`
- Btrieve LastName → PostgreSQL `first_name`
- Btrieve FullName → PostgreSQL `full_name` (BEZ zmeny)

### 3. CHECK Constraints - FK validácia

**Zabezpečuje správnu kombináciu FK:**
- 'address' → address_id povinné, partner_id NULL
- 'person' → partner_id povinné, address_id NULL

**Implementácia:**
```
CHECK (
    (contact_type = 'address' AND address_id IS NOT NULL AND partner_id IS NULL) OR
    (contact_type = 'person' AND partner_id IS NOT NULL AND address_id IS NULL)
)
```

### 4. GDPR citlivé údaje

**NEPRENÁŠAME:**
- Adresa trvalého pobytu (RsdAddr, RsdCtc, RsdCtn, RsdZip)
- Doklady totožnosti (IdnType, IdnCard)
- Dátum narodenia (BrtDate)
- Miesto narodenia (BrtPlac)
- Občianstvo (Citizen)

**Dôvod:** GDPR compliance - citlivé osobné údaje

---

## VZŤAHY S INÝMI TABUĽKAMI

### Incoming (z iných tabuliek)

**partner_catalog_addresses → partner_catalog_contacts**
- FK: address_id (pre contact_type='address')
- ON DELETE CASCADE - pri vymazaní adresy sa vymažú jej kontakty
- Use case: telefón, email pre sídlo/pobočku partnera

**partner_catalog → partner_catalog_contacts**
- FK: partner_id (pre contact_type='person')
- ON DELETE CASCADE - pri vymazaní partnera sa vymažú jeho kontaktné osoby
- Use case: zamestnanci, obchodníci, VIP osoby partnera

### Štruktúra referencií

```
partner_catalog_addresses
    ↓ (address_id)
partner_catalog_contacts (contact_type='address')
    - phone, email, website
    - contact_person

partner_catalog
    ↓ (partner_id)
partner_catalog_contacts (contact_type='person')
    - full_name, function
    - work_tel, work_email
    - mobile_tel, private_email
```

### Outgoing (do iných tabuliek)

**Žiadne** - toto je dátová tabuľka bez outgoing FK.

---

## VALIDAČNÉ PRAVIDLÁ

### 1. Typ kontaktu
- `CHECK (contact_type IN ('address', 'person'))`
- Povolené len 2 typy

### 2. Validácia FK podľa typu
- 'address' → address_id NOT NULL, partner_id NULL
- 'person' → partner_id NOT NULL, address_id NULL
- Zabezpečené CHECK constraint

### 3. Pohlavie (ak je zadané)
- `CHECK (sex_mark IS NULL OR sex_mark IN ('M', 'W'))`
- M = muž, W = žena

### 4. Email formáty
- Validácia pre 3 email polia: email, work_email, private_email
- Regex: `^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$`
- Povolené NULL hodnoty

### 5. Povinné polia
- `contact_type` - NOT NULL
- `address_id` alebo `partner_id` - podľa contact_type

---

## POZNÁMKY PRE MIGRÁCIU

### 1. Poradie migrácie

**KRITICKÉ - migrovať v tomto poradí:**
1. partner_catalog (Btrieve: PAB.BTR)
2. partner_catalog_addresses (Btrieve: PAB.BTR)
3. **partner_catalog_contacts** - TÁTO TABUĽKA
   - a) contact_type='address' z PAB.BTR
   - b) contact_type='person' z PACNCT.BTR

### 2. Migrácia contact_type='address' z PAB.BTR

**Zdroj:** PAB.BTR  
**Cieľ:** partner_catalog_contacts WHERE contact_type='address'

**Postup:**
1. Načítaj záznam z PAB.BTR
2. Lookup partner_id z partner_number
3. Lookup address_id pre registered adresu
4. INSERT kontakt s contact_type='address'
5. Mapuj polia: PABPhone → phone, PABEmail → email, atď.

**Handling NULL:**
- Prázdne polia → NULL v PostgreSQL

### 3. Migrácia contact_type='person' z PACNCT.BTR

**Zdroj:** PACNCT.BTR  
**Cieľ:** partner_catalog_contacts WHERE contact_type='person'

**Postup:**
1. Načítaj záznam z PACNCT.BTR
2. Lookup partner_id z PaCode (cez partner_number)
3. INSERT kontakt s contact_type='person'
4. **KRITICKÉ: SWAP FirstName ↔ LastName!**
   - Btrieve FirstName → PostgreSQL last_name
   - Btrieve LastName → PostgreSQL first_name
5. Mapuj ostatné polia normálne

**FirstName/LastName SWAP:**
```
first_name = record['LastName']   # Btrieve LastName = meno
last_name = record['FirstName']   # Btrieve FirstName = priezvisko
full_name = record['FullName']    # BEZ zmeny
```

### 4. Handling PaCode → partner_id

**PaCode je Btrieve internal record number:**
- Treba vytvoriť mapping dictionary: PaCode → partner_id
- Lookup cez partner_number (PABNr)

**Príklad:**
1. Pri migrácii PAB.BTR vytvor mapping: PaCode → partner_id
2. Pri migrácii PACNCT.BTR použij mapping na lookup partner_id

### 5. GDPR citlivé údaje

**KRITICKÉ - NEPRENÁŠAME:**
- Adresa trvalého pobytu
- Doklady totožnosti
- Dátum a miesto narodenia
- Občianstvo

**Dôvod:** GDPR compliance

### 6. Zastaralé údaje

**NEPRENÁŠAME:**
- Fax čísla (WorkFax, PrivFax)
- VisNum, VisType (HRS systém)
- Vyhľadávacie polia (_PaName, _FullName)

### 7. Validácia po migrácii

**Kontrola počtu záznamov:**
- Overiť počet kontaktov typu 'address' vs počet PAB.BTR záznamov
- Overiť počet kontaktov typu 'person' vs počet PACNCT.BTR záznamov

**Kontrola FK integrity:**
- Všetky address_id musia existovať v partner_catalog_addresses
- Všetky partner_id musia existovať v partner_catalog

**Kontrola FirstName/LastName SWAP:**
- Overiť, že first_name obsahuje mená (Ján, Peter, Mária)
- Overiť, že last_name obsahuje priezviská (Nový, Horný, Nováková)

---

## ROZŠÍRENIA V BUDÚCNOSTI

### Možné pridanie polí

**Pre contact_type='address':**
- `address_priority` - priorita kontaktu (primary, secondary)
- `address_purpose` - účel kontaktu (general, sales, support)

**Pre contact_type='person':**
- `person_role` - rola osoby (employee, contractor, vip)
- `person_department` - oddelenie
- `person_photo_url` - URL na fotografiu
- `linkedin_profile` - LinkedIn profil

**Spoločné:**
- `is_active` - aktívny/neaktívny kontakt
- `preferred_contact_method` - preferovaný spôsob kontaktu

---

## SÚVISIACE DOKUMENTY

- **partner_catalog** → `PAB-partner_catalog.md`
- **partner_catalog_addresses** → `PAB-partner_catalog.md`

---

**Vytvoril:** Claude & Zoltán  
**Dátum:** 2025-12-11  
**Aktualizované:** 2025-12-15  
**Verzia:** 1.1  
**Status:** ✅ Pripravené na implementáciu