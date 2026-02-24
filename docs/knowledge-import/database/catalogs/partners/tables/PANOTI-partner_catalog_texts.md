# PAB.BTR + PANOTI.BTR → partner_catalog_texts

**Súbor:** PANOTI-partner_catalog_texts.md  
**Verzia:** 1.1  
**Autor:** Zoltán & Claude  
**Dátum:** 2025-12-15  
**Status:** ✅ Production Ready

---

## 1. PREHĽAD

**PostgreSQL tabuľka:** `partner_catalog_texts`  
**Účel:** Univerzálna tabuľka pre všetky textové polia partnerov s podporou viacjazyčnosti a viacerých riadkov.

### Btrieve súbory

**PAB00000.BTR:**
- **Názov:** PAB00000.BTR
- **Umiestnenie:** `C:\NEX\YEARACT\DIALS\PAB00000.BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\DIALS\`
- **Účel:** Hlavná tabuľka partnerov - pole PABOwner (majiteľ/konateľ)

**PANOTI.BTR:**
- **Názov:** PANOTI.BTR
- **Umiestnenie:** `C:\NEX\YEARACT\DIALS\PANOTI.BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\DIALS\`
- **Účel:** Poznámkové riadky evidenčnej karty partnera

### Typy textov

- `owner_name` - majiteľ/konateľ spoločnosti (1 riadok na partnera, z PAB.BTR)
- `description` - popis partnera (1 riadok na partnera, nové v NEX Automat)
- `notice` - poznámky k partnerovi (N riadkov na partnera, z PANOTI.BTR)

---

## 2. MAPPING POLÍ

### 2.1 Mapovanie z PAB.BTR (owner_name)

| Btrieve pole | PostgreSQL pole | Hodnota | Poznámka |
|--------------|-----------------|---------|----------|
| PaCode | partner_id | Lookup | FK na partner_catalog |
| PABOwner | text | Direct | Majiteľ/konateľ |
| - | text_type | Fixed | 'owner_name' |
| - | line_number | Fixed | 0 |
| - | language | Fixed | 'sk' |

### 2.2 Mapovanie z PANOTI.BTR (notice)

| Btrieve pole | PostgreSQL pole | Hodnota | Poznámka |
|--------------|-----------------|---------|----------|
| PaCode | partner_id | Lookup | FK na partner_catalog |
| LinNum | line_number | Direct | Poradové číslo riadku |
| Notice | text | Direct | Text poznámky (Str250 → TEXT) |
| - | text_type | Fixed | 'notice' |
| - | language | Fixed | 'sk' |

### 2.3 Polia ktoré SA NEPRENÁŠAJÚ

**Žiadne** - všetky polia z Btrieve sa prenášajú.

---

## 3. BIZNIS LOGIKA

### 3.1 Typy textov

**owner_name** (1 riadok na partnera)
- Majiteľ alebo konateľ spoločnosti
- `line_number = 0` (vždy)
- Príklad: "Ing. Ján Nový"

**description** (1 riadok na partnera)
- Popis partnera, oblasť činnosti
- `line_number = 0` (vždy)
- Príklad: "Veľkoobchod s potravinami"

**notice** (N riadkov na partnera)
- Poznámky, špeciálne požiadavky, história komunikácie
- `line_number = 1, 2, 3...`
- Príklady:
  - "VIP zákazník - prioritná doprava"
  - "Platí vždy načas"
  - "Kontakt: Ján Nový, +421 905 123 456"

### 3.2 Viacjazyčnosť

Každý text môže existovať vo viacerých jazykoch:

```
Slovenčina: partner_id=123, text_type='description', line_number=0, language='sk'
Angličtina: partner_id=123, text_type='description', line_number=0, language='en'
```

### 3.3 UNIQUE constraint

```
UNIQUE (partner_id, text_type, line_number, language)
```

**Znamená:**
- Partner môže mať len jeden 'owner_name' v slovenčine
- Partner môže mať 'owner_name' aj v angličtine
- Partner môže mať viacero 'notice' riadkov (line_number 1, 2, 3...)

---

## 4. VZŤAHY S INÝMI TABUĽKAMI

### 4.1 Incoming (z iných tabuliek)

```
partner_catalog (FK: partner_id)
    ↓
partner_catalog_texts
```

**ON DELETE CASCADE:** Pri vymazaní partnera sa vymažú všetky jeho textové polia.

### 4.2 Outgoing (do iných tabuliek)

**Žiadne** - toto je dátová tabuľka partnera.

---

## 5. VALIDAČNÉ PRAVIDLÁ

### 5.1 Constraints

**CHECK constraints:**
- `text_type IN ('owner_name', 'description', 'notice')` - povolené typy textov
- `line_number >= 0` - poradové číslo >= 0
- `language IN ('sk', 'en', 'cz', 'de', 'hu')` - povolené jazyky
- `UNIQUE (partner_id, text_type, line_number, language)` - unikátna kombinácia

**Povinné polia:**
- `partner_id` NOT NULL
- `text_type` NOT NULL

**Default hodnoty:**
- `line_number` = 0
- `language` = 'sk'
- `created_at` = CURRENT_TIMESTAMP
- `updated_at` = CURRENT_TIMESTAMP

---

## 6. PRÍKLAD DÁT

### 6.1 Owner name (z PAB.BTR)

```sql
-- Majiteľ/konateľ v slovenčine
(1, 'owner_name', 0, 'Ing. Ján Nový', 'sk')
(2, 'owner_name', 0, 'Mgr. Peter Varga', 'sk')
(3, 'owner_name', 0, 'Ing. Lukáš Horný, PhD.', 'sk')
```

### 6.2 Description (nové v NEX Automat)

```sql
-- Popis partnera v slovenčine a angličtine
(1, 'description', 0, 'Veľkoobchod s potravinami a nápojmi', 'sk')
(1, 'description', 0, 'Wholesale food and beverage supplier', 'en')

(2, 'description', 0, 'Maloobchodná sieť so spotrebnou elektronikou', 'sk')
(2, 'description', 0, 'Retail chain for consumer electronics', 'en')
```

### 6.3 Notices (z PANOTI.BTR)

```sql
-- Poznámky k partnerom (viacero riadkov)
-- Partner 1
(1, 'notice', 1, 'VIP zákazník - prioritná doprava', 'sk')
(1, 'notice', 2, 'Platí vždy načas, 14 dní splatnosť', 'sk')
(1, 'notice', 3, 'Kontakt: Ján Nový, +421 905 123 456', 'sk')

-- Partner 2
(2, 'notice', 1, 'Odber len na objednávku', 'sk')
(2, 'notice', 2, 'Osobný odber v Košiciach', 'sk')

-- Partner 3
(3, 'notice', 1, 'Medzinárodný partner - faktúry v EUR', 'sk')
(3, 'notice', 2, 'Export do ČR - potrebné CLO dokumenty', 'sk')
```

---

## 7. POZNÁMKY PRE MIGRÁCIU

### 7.1 Poradie migrácie

```
KRITICKÉ: Migrovať v tomto poradí!

1. partner_catalog (Btrieve: PAB00000.BTR)       -- Hlavná tabuľka
2. partner_catalog_texts                         -- TÁTO TABUĽKA
   a) owner_name z PAB00000.BTR
   b) notice z PANOTI.BTR
```

### 7.2 Transformačné pravidlá

**PaCode mapping:**
- Zistiť presný formát PaCode (longint)
- Overiť ako sa mapuje na partner_number (VARCHAR)
- Použiť rovnakú logiku ako pri partner_catalog_facilities

**line_number pre owner_name:**
- Vždy `line_number = 0`
- Jeden riadok na partnera

**line_number pre notice:**
- Z Btrieve pole LinNum
- Zachovať poradie (1, 2, 3...)

**Notice pole Str250:**
- V PANOTI.BTR je Notice Str250 (dlhší text)
- PostgreSQL TEXT pole nemá limit

**ON CONFLICT stratégia:**
- Umožňuje re-run migrácie
- Aktualizuje existujúce záznamy

**Audit polia:**
- Pri migrácii: `created_by = 'migration'`, `updated_by = 'migration'`
- Pri manuálnom pridaní: username používateľa

**Budúce rozšírenia:**
- Pridať ďalšie text_type podľa potreby: 'internal_note', 'delivery_instruction'...
- Rozšíriť jazyky podľa potreby

---

## 8. SÚVISIACE DOKUMENTY

- **partner_catalog** → `PAB-partner_catalog.md`
- **partner_catalog_facilities** → `PASUBC-partner_catalog_facilities.md`

---

## 9. VERZIA A ZMENY

### v1.1 (2025-12-15)
- Cleanup: odstránené SQL CREATE statements
- Cleanup: odstránené Query patterns
- Cleanup: odstránený Python migration code
- Pridané: Btrieve súbor lokácia (DIALS) pre PAB a PANOTI
- Zachované: Mapping, biznis logika, validačné pravidlá (koncepčne)
- Redukcia: 15.4 KB → 6.5 KB (58%)

### v1.0 (2025-12-11)
- Prvotná verzia dokumentu
- Komplexná SQL schéma s viacjazyčnosťou
- Mapping z PAB.BTR (owner_name) a PANOTI.BTR (notice)

---

**Koniec dokumentu PANOTI-partner_catalog_texts.md**