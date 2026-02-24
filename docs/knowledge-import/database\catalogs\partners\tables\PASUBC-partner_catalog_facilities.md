# PASUBC.BTR → partner_catalog_facilities

**Súbor:** PASUBC-partner_catalog_facilities.md  
**Verzia:** 1.1  
**Autor:** Zoltán & Claude  
**Dátum:** 2025-12-15  
**Status:** ✅ Production Ready

---

## 1. PREHĽAD

**PostgreSQL tabuľka:** `partner_catalog_facilities`  
**Účel:** Prevádzkové jednotky obchodných partnerov (pobočky, sklady, výdajné miesta).

### Btrieve súbor

- **Názov:** PASUBC.BTR
- **Umiestnenie:** `C:\NEX\YEARACT\DIALS\PASUBC.BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\DIALS\`
- **Účel:** Partner Subunits Catalog - prevádzkové jednotky partnerov

**Poznámka:** Každý partner môže mať viacero prevádzkových jednotiek s vlastnými adresami, kontaktmi a spôsobom dopravy.

---

## 2. MAPPING POLÍ

### 2.1 Polia ktoré SA PRENÁŠAJÚ

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
| **Nové polia** |
| - | facility_id | New | SERIAL PRIMARY KEY |
| - | is_active | New | Default: TRUE |

### 2.2 Polia ktoré SA NEPRENÁŠAJÚ

| Btrieve pole | Dôvod neprenášania |
|--------------|--------------------|
| WpaFax | Zastaralý údaj - fax sa už nepoužíva |
| WpaCty | Kód obce - nepotrebný, máme názov mesta (WpaCtn) |
| TrsName | Názov dopravy - je v číselníku transport_methods |
| ModNum | Poradové číslo modifikácie - nie je potrebné |

---

## 3. BIZNIS LOGIKA

### 3.1 Prevádzkové jednotky

**Účel:**
- Pobočky firmy (viaceré predajne, sklady)
- Výdajné miesta
- Rôzne adresy dodania/prevzatia tovaru

**Príklady:**
- Dodávateľ má centrálny sklad + regionálne sklady
- Odberateľ má hlavnú pobočku + pobočky v iných mestách
- Partner má sídlo firmy + výrobné závody

### 3.2 Spôsob dopravy

Každá prevádzkové jednotka môže mať vlastný preferovaný spôsob dopravy:
- Centrála → kuriér (rýchla doprava)
- Sklad → nákladná doprava
- Pobočka → osobný odber

**FK na transport_methods:** Zabezpečuje konzistentný číselník.

### 3.3 Počítadlo v partner_catalog

Automatická aktualizácia cez trigger:
```
Pri INSERT do partner_catalog_facilities → facility_count + 1
Pri DELETE z partner_catalog_facilities → facility_count - 1
```

---

## 4. VZŤAHY S INÝMI TABUĽKAMI

### 4.1 Incoming (z iných tabuliek)

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

### 4.2 Outgoing (do iných tabuliek)

```
partner_catalog_facilities
    ↓
invoices, sales_orders, stock_movements... (⚠️ BEZ FK constraints - denormalizované!)
```

**KRITICKÉ:** Archívne dokumenty (faktúry, príjemky, výdajky) nemajú FK constraint na partner_catalog_facilities! Údaje sú snapshot v dokumente (právny požiadavok).

---

## 5. VALIDAČNÉ PRAVIDLÁ

### 5.1 Constraints

**UNIQUE constraint:**
- `UNIQUE (partner_id, facility_code)` - každý partner môže mať facility_code len raz

**CHECK constraints:**
- `LENGTH(country_code) = 2` - validácia krajiny (2-znakový kód)
- `email` validácia formátu (ak je zadaný)

**Povinné polia:**
- `partner_id` NOT NULL
- `facility_code` NOT NULL
- `facility_name` NOT NULL

**Default hodnoty:**
- `country_code` = 'SK'
- `is_active` = TRUE
- `created_at` = CURRENT_TIMESTAMP
- `updated_at` = CURRENT_TIMESTAMP

### 5.2 Triggery

**update_partner_facilities_updated_at:**
- Pri každom UPDATE nastaví updated_at na CURRENT_TIMESTAMP

**update_partner_facility_count:**
- Pri INSERT/DELETE aktualizuje počítadlo v partner_catalog

---

## 6. PRÍKLAD DÁT

```sql
-- ABC Veľkoobchod - centrálny sklad
(1, 1, 'Centrálny sklad Bratislava', 'Skladová 10', 'Bratislava', '82101', 'SK')
(1, 2, 'Regionálny sklad Košice', 'Priemyselná 25', 'Košice', '04011', 'SK')
(1, 3, 'Výdajňa Žilina', 'Obchodná 8', 'Žilina', '01001', 'SK')

-- XYZ Retail - pobočky v mestách
(2, 1, 'Pobočka Bratislava', 'Obchodná 15', 'Bratislava', '81101', 'SK')
(2, 2, 'Pobočka Nitra', 'Hlavná 30', 'Nitra', '94901', 'SK')

-- Global Trading - hlavný sklad + Czech Republic
(3, 1, 'Hlavný sklad Žilina', 'Skladová 100', 'Žilina', '01008', 'SK')
(3, 2, 'Pobočka Praha', 'Průmyslová 50', 'Praha', '14000', 'CZ')
```

---

## 7. POZNÁMKY PRE MIGRÁCIU

### 7.1 Poradie migrácie

```
KRITICKÉ: Migrovať v tomto poradí!

1. transport_methods (Btrieve: TRPLST.BTR)    -- FK pre partner_catalog_facilities
2. partner_catalog (Btrieve: PAB00000.BTR)    -- FK pre partner_catalog_facilities
3. partner_catalog_facilities (Btrieve: PASUBC.BTR)  -- TÁTO TABUĽKA
```

### 7.2 Transformačné pravidlá

**PaCode mapping:**
- Zistiť presný formát PaCode (longint)
- Overiť ako sa mapuje na partner_number (VARCHAR)
- Možno potrebné rozšírené mapovanie cez pomocnú tabuľku

**TrsCode → transport_method_id:**
- LOOKUP cez transport_methods
- Ak TrsCode neexistuje v číselníku → NULL
- Validovať všetky kódy pred migráciou

**Audit polia:**
- Kombinovať CrtDate + CrtTime do TIMESTAMP
- Kombinovať ModDate + ModTime do TIMESTAMP
- Ak nie sú vyplnené → použiť CURRENT_TIMESTAMP

**Trigger automaticky aktualizuje:**
- `partner_catalog.facility_count` sa aktualizuje cez trigger
- Niet potreby počítať manuálne

**WpaFax NEPRENÁŠAME:**
- Zastaralý údaj
- Fax sa už nepoužíva v moderných obchodných systémoch

**WpaCty NEPRENÁŠAME:**
- Kód obce nie je potrebný
- Máme názov mesta (WpaCtn)

**TrsName NEPRENÁŠAME:**
- Názov dopravy je v číselníku transport_methods
- Eliminácia duplikácie

---

## 8. SÚVISIACE DOKUMENTY

- **partner_catalog** → `PAB-partner_catalog.md`
- **transport_methods** → `TRPLST-transport_methods.md`
- **partner_catalog_texts** → `PANOTI-partner_catalog_texts.md`

---

## 9. VERZIA A ZMENY

### v1.1 (2025-12-15)
- Cleanup: odstránené SQL CREATE statements
- Cleanup: odstránené Query patterns
- Cleanup: odstránený Python migration code
- Pridané: Btrieve súbor lokácia (DIALS)
- Zachované: Mapping, biznis logika, validačné pravidlá (koncepčne)
- Redukcia: 18.0 KB → 7.5 KB (58%)

### v1.0 (2025-12-11)
- Prvotná verzia dokumentu
- Komplexná SQL schéma s triggermi
- Mapping polí Btrieve → PostgreSQL

---

**Koniec dokumentu PASUBC-partner_catalog_facilities.md**