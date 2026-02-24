# WRILST.BTR → facilities

## 1. PREHĽAD

**Účel:** Číselník prevádzkových jednotiek (facilities) vlastnej firmy.

**Charakteristika:**
- Master data tabuľka pre naše vlastné prevádzky/pobočky
- Každá prevádzkáreň má jedinečné číslo (WriNum)
- Obsahuje úplné kontaktné údaje a nastavenia
- Prepojenie na výrobné prevádzky, sklady, predajne
- Používa sa pri tlači dokumentov (hlavičky faktúr, dodacích listov)

**PostgreSQL tabuľky:**
- `facilities` - jedna tabuľka (1:1 mapping s Btrieve)

**Vzťahy:**
- Súvisí s `stocks` (každý sklad môže patriť prevádzke)
- Používa sa v dokumentoch (faktúry, dodacie listy)
- Kľúčové pre multi-facility operácie

### Btrieve súbor

- **Názov:** WRILST.BTR
- **Umiestnenie:** `C:\NEX\YEARACT\STORES\WRILST.BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\STORES\`
- **Účel:** Číselník prevádzkových jednotiek vlastnej firmy (pobočky, sklady, výrobne)
- **Primárny kľúč:** WriNum (INTEGER)
- **Indexy:** WriNum (unique)

---

## 2. MAPPING POLÍ

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

## 3. BIZNIS LOGIKA

### Použitie facilities

**1. Tlač dokumentov**

Získanie údajov prevádzky pre hlavičku faktúry - načítajú sa údaje aktívnej centrály (is_headquarters = true), vrátane názvu, adresy, identifikačných čísiel a kontaktov.

**2. Multi-facility operácie**

Zoznam všetkých aktívnych skladov - filtruje sa podľa is_warehouse = true a is_active = true, zoradené podľa názvu.

**3. Výrobné prevádzky**

Výrobné jednotky - filtruje sa podľa is_production = true a is_active = true.

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
   - História ostáva zachovaná

4. **Viaceré funkcie:**
   - Prevádzka môže mať viacero funkcií súčasne
   - Napr. is_warehouse + is_store (sklad a predajňa)

---

## 4. VZŤAHY S INÝMI TABUĽKAMI

### Facilities → Stocks (1:N)

Každá prevádzka môže mať viacero skladov. Pri pokuse o zmazanie prevádzky so skladmi sa operácia zamietne (ON DELETE RESTRICT).

### Facilities → Documents (1:N)

Faktúry a dodacie listy vystavené prevádzkou. FK sa nepridáva kvôli archívnym dokumentom.

### Facilities → Production_orders (1:N)

Výrobné príkazy pre výrobnú prevádzku. Bude doplnené pri dokumentácii výroby.

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

## 5. VALIDAČNÉ PRAVIDLÁ

### Základné validácie

1. **facility_name**: nesmie byť prázdny (LENGTH(TRIM(facility_name)) > 0)
2. **country_code**: presne 2 veľké písmená (regex: ^[A-Z]{2}$)
3. **email**: validný formát email adresy (regex: ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$)

### Jedinečná centrála

Len jedna prevádzka môže mať is_headquarters = true. Pri pokuse o nastavenie druhej centrály sa operácia zamietne s chybovou hláškou "Už existuje centrála (is_headquarters = true)".

---

## 6. PRÍKLAD DÁT

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
```

---

## 7. POZNÁMKY PRE MIGRÁCIU

### Dôležité transformácie

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

### Migration workflow

Pri migrácii z Btrieve do PostgreSQL:

1. Načítať záznamy z WRILST.BTR v adresári STORES
2. Pre každý záznam:
   - Zlúčiť dátumové a časové polia do TIMESTAMP
   - Transformovať premenované polia (WriAddr → street, WriCtn → city)
   - Nastaviť defaultné hodnoty pre prázdne polia
   - Validovať formát email a country_code
3. Overiť, že existuje práve jedna centrála (is_headquarters = true)
4. Importovať do tabuľky facilities
5. Overiť integrity constraints a indexy

---

## 8. VERZIA A ZMENY

| Verzia | Dátum | Autor | Zmeny |
|--------|-------|-------|-------|
| 1.0 | 2025-12-11 | Zoltán + Claude | Prvá verzia dokumentácie |
| 1.1 | 2025-12-11 | Zoltán + Claude | Zjednotené so štandardom (adresy, audit polia) |
| 2.0 | 2025-12-15 | Zoltán + Claude | **Batch 6 migration**: Vyčistenie dokumentácie od SQL/Python kódu |

**Status:** ✅ Pripravené na migráciu  
**Batch:** 6 (Stock Management - dokumenty 1/7)  
**Súbor:** `docs/architecture/database/stock/cards/tables/WRILST-facilities.md`