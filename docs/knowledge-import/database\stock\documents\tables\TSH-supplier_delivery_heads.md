# TSH.BTR → supplier_delivery_heads

**Pre všeobecné zásady pozri:** [COMMON_DOCUMENT_PRINCIPLES.md](../../COMMON_DOCUMENT_PRINCIPLES.md)

Tento dokument popisuje **ŠPECIFICKÉ vlastnosti** dodávateľských dodacích listov (hlavičky).

---

## 1. PREHĽAD

### Účel

Hlavičky dodávateľských dodacích listov (Supplier Delivery Note Headers) obsahujú základné informácie o prijatých dodávkach od dodávateľov. Slúžia ako master záznamy pre detail položky, texty a platby.

### Btrieve súbory

**Starý systém (NEX Genesis):**
```
TSH25001.BTR  - Kniha č. 1, rok 2025
TSH25002.BTR  - Kniha č. 2, rok 2025
TSH24001.BTR  - Kniha č. 1, rok 2024
```

- **Umiestnenie:** `C:\NEX\YEARACT\STORES\TSH[YY][NNN].BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\STORES\`
  - [YY] = rok (25 = 2025)
  - [NNN] = číslo knihy (001, 002, ...)

**Nový systém (NEX Automat):**
```
supplier_delivery_heads - jedna tabuľka pre všetky knihy
```

### Vzťahy

```
supplier_delivery_heads (1 hlavička)
    ├──< supplier_delivery_items (N položiek)
    ├──< document_texts (N textov) - univerzálna tabuľka
    ├──< supplier_delivery_payments (N platieb)
    └──< supplier_delivery_vat_groups (N DPH skupín)
```

**POZNÁMKA:** Párovanie s faktúrami (`supplier_delivery_invoices`) je na úrovni **POLOŽIEK** (TSI), nie hlavičiek!

### Kľúčové entity

- **Dodávateľ:** Partner (supplier_id + supplier_modify_id) - versioning systém
- **Prevádzka dodávateľa:** Facility (supplier_facility_id + supplier_facility_modify_id) - versioning systém
- **Sklad:** Stock (stock_id)
- **Kniha dokladov:** book_num
- **Platobný spôsob:** payment_method_id
- **Dopravný spôsob:** transport_method_id

---

## 2. MAPPING POLÍ

### Číslovanie dokladov

**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 1

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| Year | Str2 | year | SMALLINT | 25 → 2025 |
| SerNum | longint | global_sequence | INTEGER | Globálne poradie |
| DocNum | Str12 | document_number | VARCHAR(13) | DD2500000123 |
| ExtNum | Str12 | external_number | VARCHAR(12) | Číslo dodávateľa |
| - | - | book_num | INTEGER | Z TSH25001 → 1 |
| - | - | book_sequence | INTEGER | Auto-trigger |
| - | - | old_document_number | VARCHAR(13) | Migrácia |

### Základné údaje

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| DocDate | DateType | document_date | DATE |
| StkNum | word | stock_id | INTEGER |

### Dodávateľ (Versioning)

**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 2

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| PaCode | longint | supplier_id | INTEGER | ID partnera |
| - | - | supplier_modify_id | INTEGER | Verzia (NOVÉ) |
| PaName, RegName, RegIno... | - | - | - | V partner_catalog_history |
| WpaCode | word | supplier_facility_id | INTEGER | ID prevádzky |
| - | - | supplier_facility_modify_id | INTEGER | Verzia (NOVÉ) |
| WpaName, WpaAddr... | - | - | - | V partner_facilities_history |

### Platba a doprava

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| PayCode | Str3 | payment_method_id | INTEGER |
| PayName | Str20 | payment_method_name | VARCHAR(20) |
| TrsCode | Str3 | transport_method_id | INTEGER |
| TrsName | Str20 | transport_method_name | VARCHAR(20) |

### Cenník a zľavy

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| PlsNum | word | price_list_id | INTEGER |
| DscPrc | double | discount_percent | DECIMAL(5,2) |
| PrfPrc | double | margin_percent | DECIMAL(5,2) |

### NSO (Náklady súvisiace s obstaraním)

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| AcZValue | double | customs_cost_ac | DECIMAL(15,2) | Colné náklady |
| AcTValue | double | transport_cost_ac | DECIMAL(15,2) | Doprava |
| AcOValue | double | other_cost_ac | DECIMAL(15,2) | Ostatné |
| AcSValue | double | acquisition_value_ac | DECIMAL(15,2) | OC s NSO |

### Hodnoty v účtovnej mene (AC)

**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 5

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| AcDvzName | Str3 | accounting_currency | VARCHAR(3) |
| AcDValue | double | list_value_ac | DECIMAL(15,2) |
| AcDscVal | double | discount_value_ac | DECIMAL(15,2) |
| AcRndVal | double | rounding_value_ac | DECIMAL(15,2) |
| AcAValue | double | sales_base_value_ac | DECIMAL(15,2) |
| AcBValue | double | sales_total_value_ac | DECIMAL(15,2) |
| AcCValue | double | purchase_base_value_ac | DECIMAL(15,2) |
| AcVatVal | double | purchase_vat_value_ac | DECIMAL(15,2) |
| AcEValue | double | purchase_total_value_ac | DECIMAL(15,2) |
| AcPrfVal | double | margin_value_ac | DECIMAL(15,2) |

### Hodnoty vo vyúčtovacej mene (FC)

**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 5

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| FgDvzName | Str3 | foreign_currency | VARCHAR(3) |
| FgCourse | double | foreign_currency_rate | DECIMAL(15,6) |
| FgDValue | double | list_value_fc | DECIMAL(15,2) |
| FgDscVal | double | discount_value_fc | DECIMAL(15,2) |
| FgRndVal | double | rounding_value_fc | DECIMAL(15,2) |
| FgCValue | double | purchase_base_value_fc | DECIMAL(15,2) |
| FgVatVal | double | purchase_vat_value_fc | DECIMAL(15,2) |
| FgEValue | double | purchase_total_value_fc | DECIMAL(15,2) |

### DPH skupiny (Multi-row → EAV)

| Btrieve | PostgreSQL Tabuľka | Amount Type |
|---------|-------------------|-------------|
| VatPrc1-5 | supplier_delivery_vat_groups | vat_rate |
| AcCValue1-5 | supplier_delivery_vat_amounts | base_ac |
| AcEValue1-5 | supplier_delivery_vat_amounts | total_ac |
| FgCValue1-5 | supplier_delivery_vat_amounts | base_fc |
| FgEValue1-5 | supplier_delivery_vat_amounts | total_fc |
| FgCsdVal1-5 | supplier_delivery_vat_amounts | cash_register_base_fc |

### Stavy dokladu

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| DstStk | Str1 | status | VARCHAR(20) | N→draft, S→received/posted |
| DstAcc | Str1 | status | VARCHAR(20) | ''→draft/received, A→posted |
| DstPair | Str1 | paired_status | VARCHAR(1) | N/P/Q/H/C |
| VatDoc | byte | is_vat_document | BOOLEAN | Daňový doklad |

### Štatistika

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| ItmQnt | word | item_count | INTEGER |
| PrnCnt | byte | print_count | INTEGER |
| SmCode | word | stock_movement_id | INTEGER |

### Audit

**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 7

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| CrtUser | Str8 | created_by | VARCHAR(8) | - |
| CrtDate + CrtTime | Date + Time | created_at | TIMESTAMP | Zlúčené |
| ModUser | Str8 | updated_by | VARCHAR(8) | - |
| ModDate + ModTime | Date + Time | updated_at | TIMESTAMP | Zlúčené |

### NEPRENESENÉ POLIA

**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 9.3

Pracovné polia, staré odkazy, zastarané funkcie - kompletný zoznam v COMMON.

---

## 3. BIZNIS LOGIKA (ŠPECIFICKÉ PRE DD)

### Lifecycle dokladu

```
┌─────────┐   Prijať    ┌──────────┐   Zaúčtovať   ┌────────┐
│  DRAFT  │  na sklad   │ RECEIVED │   do účt.     │ POSTED │
│ (N, '') │ ─────────> │ (S, '')  │ ──────────>  │ (S, A) │
└─────────┘             └──────────┘               └────────┘

DstStk: N = Not received, S = Stocked
DstAcc: '' = Not posted, A = Accounted
```

**Pravidlá:**
1. **Draft → Received:** Vytvorenie STM záznamov, aktualizácia stock_cards
2. **Received → Posted:** Zaúčtovanie do podvojného účtovníctva
3. **Nie je možné zmeniť doklad v stave Posted**

---

### Paired status (Vypárovanie)

**Cesta A: Faktúry** (vypárovanie na úrovni POLOŽIEK!)
```
N (nič) → P (čiastočne) → Q (celé)
```

**Cesta B: Pokladnica**
```
N (nič) → H (čiastočne) → C (celé)
```

**Stavy:**
- **N** - Not paired: Nič nie je vypárované ani uhradené
- **P** - Partially paired: Časť položiek je na faktúre/ách
- **Q** - Queued/Paired: Celý doklad vypárovaný s faktúrou/ami
- **H** - Half paid: Časť hodnoty cez pokladnicu
- **C** - Cash register paid: Celá hodnota cez pokladnicu

**KRITICKÉ:** 
- Párovanie s faktúrami je na úrovni **POLOŽIEK** (TSI), nie hlavičiek!
- `paired_status` v hlavičke je agregovaný stav z položiek
- Nemôže byť zmiešané (buď faktúra alebo pokladnica)

---

### NSO (Náklady súvisiace s obstaraním)

**Koncept:**
```
Obstarávacia cena = Nákupná cena + NSO náklady

acquisition_value_ac = purchase_base_value_ac + 
                       customs_cost_ac + 
                       transport_cost_ac + 
                       other_cost_ac
```

**Rozdelenie NSO:**
- NSO náklady sa zadávajú na úrovni **hlavičky**
- Aliquotne sa rozdeľujú na **položky** (podľa pomeru NC položky)
- Detail rozdelenia je v TSI-supplier_delivery_items.md

---

### Výpočet marže

```
Marža = Predajná cena - Nákupná cena
margin_value_ac = sales_base_value_ac - purchase_base_value_ac

Marža % = (Marža / Nákupná cena) × 100
margin_percent = (margin_value_ac / purchase_base_value_ac) × 100
```

---

### DPH skupiny (EAV Pattern)

**Prečo EAV pattern?**
- V Btrieve: fixné polia VatPrc1-5, AcCValue1-5, FgCValue1-5...
- V PostgreSQL: dynamické riadky pre každú DPH sadzbu
- Flexibilita: ľahko pridať nové typy hodnôt

**Koncept:**

Vytvorenie dokladu → vytvorenie DPH skupín (vat_groups) → vytvorenie hodnôt pre každú skupinu (vat_amounts). Pri migrácii z Btrieve sa polia VatPrc1-5 transformujú na samostatné riadky v supplier_delivery_vat_groups, a hodnoty AcCValue1-5, AcEValue1-5 atď. sa transformujú na riadky v supplier_delivery_vat_amounts s príslušným amount_type.

---

## 4. VZŤAHY S INÝMI TABUĽKAMI

### Master-Detail vzťahy

```
supplier_delivery_heads (1) ──< (N) supplier_delivery_items
    ON DELETE CASCADE

supplier_delivery_heads (1) ──< (N) document_texts
    WHERE document_type = 'supplier_delivery'
    ON DELETE CASCADE

supplier_delivery_heads (1) ──< (N) supplier_delivery_payments
    ON DELETE CASCADE

supplier_delivery_heads (1) ──< (N) supplier_delivery_vat_groups
    ON DELETE CASCADE
```

### Reference na katalógy (Versioning)

**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 2

```
supplier_id + supplier_modify_id → partner_catalog_history

supplier_facility_id + supplier_facility_modify_id → partner_facilities_history

stock_id → stocks (RESTRICT)
payment_method_id → payment_methods (RESTRICT)
transport_method_id → transport_methods (RESTRICT)
```

### Reference na skladové systémy

```
stock_movement_id → stock_card_movements.movement_id
```

---

## 5. PRÍKLAD DÁT

### Doklad - Draft

```sql
INSERT INTO supplier_delivery_heads (
    document_number, year, global_sequence,
    book_num, external_number,
    document_date, stock_id,
    supplier_id, supplier_modify_id,
    accounting_currency,
    purchase_base_value_ac, purchase_vat_value_ac, purchase_total_value_ac,
    status, paired_status,
    created_by, created_at
) VALUES (
    'DD2500000123', 2025, 123,
    1, 'DL-2025-456',
    '2025-01-15', 1,
    456, 0,
    'EUR',
    1500.00, 315.00, 1815.00,
    'draft', 'N',
    'zoltan', '2025-01-15 10:30:00'
);
```

### DPH skupiny

```sql
-- DPH 20%
INSERT INTO supplier_delivery_vat_groups (delivery_head_id, vat_rate)
VALUES (1, 20.00);

INSERT INTO supplier_delivery_vat_amounts (vat_group_id, amount_type, amount)
VALUES 
    (1, 'base_ac', 1000.00),
    (1, 'total_ac', 1200.00);

-- DPH 10%
INSERT INTO supplier_delivery_vat_groups (delivery_head_id, vat_rate)
VALUES (1, 10.00);

INSERT INTO supplier_delivery_vat_amounts (vat_group_id, amount_type, amount)
VALUES 
    (2, 'base_ac', 500.00),
    (2, 'total_ac', 550.00);
```

---

## 6. MIGRÁCIA

### Versioning pri migrácii

**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 9.2

**Pred migráciou dokladov:**
1. Migruj partnerov do `partner_catalog_history` s `modify_id = 0`
2. Migruj prevádzky do `partner_facilities_history` s `modify_id = 0`

**Pri migrácii dokladu:**

Nastavenie supplier_id z Btrieve PaCode, supplier_modify_id = 0 (prvá verzia), supplier_facility_id z WpaCode, supplier_facility_modify_id = 0.

### DPH skupiny

Pre každé z piatich DPH polí (VatPrc1-5) v Btrieve zázname, ak je VatPrc > 0, vytvor záznam v supplier_delivery_vat_groups a následne záznamy v supplier_delivery_vat_amounts pre base_ac (z AcCValue), total_ac (z AcEValue), base_fc (z FgCValue), total_fc (z FgEValue).

### Stavy dokladu

Transformácia stavov:
- Ak DstAcc = 'A' → status = 'posted'
- Ak DstStk = 'S' a DstAcc != 'A' → status = 'received'
- Inak → status = 'draft'
- paired_status = DstPair (N/P/Q/H/C)

### Validácia po migrácii

Kontroly:
1. Počet záznamov podľa knihy a roku
2. Počet DPH skupín a hodnôt
3. Sumy v hlavičke vs. suma položiek
4. Verzie partnerov a prevádzok

---

## 7. VERZIA A ZMENY

| Verzia | Dátum | Autor | Zmeny |
|--------|-------|-------|-------|
| 2.0 | 2025-12-13 | Zoltán + Claude | Optimalizácia dokumentácie |
| 2.1 | 2025-12-15 | Zoltán + Claude | **Batch 6 migration**: Vyčistenie od SQL/Python kódu |

**Status:** ✅ Pripravené na migráciu  
**Batch:** 6 (Stock Management - dokumenty 3/7)  
**Súbor:** `docs/architecture/database/stock/documents/tables/TSH-supplier_delivery_heads.md`

---

### Závislosti

**Tento dokument vyžaduje:**
- `COMMON_DOCUMENT_PRINCIPLES.md` - všeobecné zásady
- `partner_catalog` + `partner_catalog_history` - versioning
- `partner_facilities` + `partner_facilities_history` - versioning
- `stocks`, `payment_methods`, `transport_methods` - číselníky

**Súvisiace dokumenty:**
- `TSI-supplier_delivery_items.md` - položky dodacích listov
- `document_texts` - texty (univerzálna tabuľka)
- `TSP-supplier_delivery_payments.md` - platby

### Poznámky

1. **supplier_delivery_invoices** je v TSI (M:N medzi položkami a faktúrami), NIE v TSH!
2. **document_texts** je univerzálna tabuľka pre všetky typy dokladov
3. **paired_status** v hlavičke je agregovaný z položiek
4. **NSO náklady** sa rozdeľujú aliquotne na položky (detail v TSI)

---

**Koniec dokumentu TSH-supplier_delivery_heads.md**