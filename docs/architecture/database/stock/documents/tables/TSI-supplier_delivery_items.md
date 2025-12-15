# TSI.BTR → supplier_delivery_items

**Pre všeobecné zásady pozri:** [COMMON_DOCUMENT_PRINCIPLES.md](../../COMMON_DOCUMENT_PRINCIPLES.md)

Tento dokument popisuje **ŠPECIFICKÉ vlastnosti** položiek dodávateľských dodacích listov.

---

## 1. PREHĽAD

### Účel

Položky dodávateľských dodacích listov (Supplier Delivery Note Items) obsahujú detailné informácie o prijatých produktoch. Každá položka reprezentuje jeden riadok dodávky s množstvom, cenami a stavmi spracovania.

### Btrieve súbory

**Starý systém (NEX Genesis):**
```
TSI25001.BTR  - Položky knihy č. 1, rok 2025
TSI25002.BTR  - Položky knihy č. 2, rok 2025
TSI24001.BTR  - Položky knihy č. 1, rok 2024
```

- **Umiestnenie:** `C:\NEX\YEARACT\STORES\TSI[YY][NNN].BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\STORES\`
  - [YY] = rok (25 = 2025)
  - [NNN] = číslo knihy (001, 002, ...)

**Nový systém (NEX Automat):**
```
supplier_delivery_items - jedna tabuľka pre všetky knihy
```

### Vzťahy

```
supplier_delivery_heads (1 hlavička)
    └──< supplier_delivery_items (N položiek)
            ├──< supplier_delivery_invoices (N faktúr - M:N)
            └──< supplier_delivery_orders (N objednávok - M:N)
```

### Kľúčové entity

- **Hlavička:** delivery_head_id (FK na supplier_delivery_heads)
- **Produkt:** product_id + product_modify_id (versioning systém)
- **Dodávateľ:** supplier_id (z hlavičky, pre index)
- **Sklad:** stock_id (kam sa prijíma)
- **Faktúry:** M:N párovanie cez supplier_delivery_invoices
- **Objednávky:** M:N párovanie cez supplier_delivery_orders

---

## 2. MAPPING POLÍ

### Prepojenie

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| DocNum | Str12 | delivery_head_id | BIGINT | FK na supplier_delivery_heads |
| ItmNum | word | item_number | INTEGER | Poradové číslo |

### Produkt (Versioning)

**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 2

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| GsCode | longint | product_id | INTEGER | ID produktu |
| - | - | product_modify_id | INTEGER | Verzia (NOVÉ) |
| MgCode, GsName, BarCode... | - | - | - | V product_catalog_history |

### Sklad a množstvo

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| StkNum | word | stock_id | INTEGER |
| GsQnt | double | quantity | DECIMAL(15,3) |

### DPH a zľavy

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| VatPrc | double | vat_rate | DECIMAL(5,2) |
| DscPrc | double | discount_percent | DECIMAL(5,2) |

### NSO (Aliquotne rozdelené)

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| AcZValue | double | customs_cost_ac | DECIMAL(15,2) | Colné náklady |
| AcTValue | double | transport_cost_ac | DECIMAL(15,2) | Doprava |
| AcOValue | double | other_cost_ac | DECIMAL(15,2) | Ostatné |

### Ceny v účtovnej mene (AC)

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| AcSPrice | double | unit_price_ac | DECIMAL(15,2) | NC/MJ s NSO |
| AcDValue | double | list_value_ac | DECIMAL(15,2) | Pred zľavou |
| AcDscVal | double | discount_value_ac | DECIMAL(15,2) | Zľava |
| AcRndVal | double | rounding_value_ac | DECIMAL(15,2) | Zaokrúhlenie |
| AcCValue | double | purchase_base_value_ac | DECIMAL(15,2) | NC bez DPH, bez NSO |
| AcEValue | double | purchase_total_value_ac | DECIMAL(15,2) | NC s DPH, s NSO |
| AcSValue | double | acquisition_value_ac | DECIMAL(15,2) | OC s NSO |
| AcAValue | double | sales_base_value_ac | DECIMAL(15,2) | PC bez DPH |
| AcBValue | double | sales_total_value_ac | DECIMAL(15,2) | PC s DPH |

### Ceny vo vyúčtovacej mene (FC)

| Btrieve | Typ | PostgreSQL | Typ |
|---------|-----|------------|-----|
| FgDPrice | double | unit_list_price_fc | DECIMAL(15,2) |
| FgCPrice | double | unit_base_price_fc | DECIMAL(15,2) |
| FgEPrice | double | unit_total_price_fc | DECIMAL(15,2) |
| FgDValue | double | list_value_fc | DECIMAL(15,2) |
| FgDscVal | double | discount_value_fc | DECIMAL(15,2) |
| FgRndVal | double | rounding_value_fc | DECIMAL(15,2) |
| FgCValue | double | purchase_base_value_fc | DECIMAL(15,2) |
| FgEValue | double | purchase_total_value_fc | DECIMAL(15,2) |

### Trvanlivosť a šarža

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| DrbDate | DateType | expiry_date | DATE | NULL ak nevyžaduje |
| RbaCode | Str30 | batch_code | VARCHAR(30) | NULL ak nevyžaduje |
| RbaDate | DateType | batch_date | DATE | NULL ak nevyžaduje |

### Stavy položky

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| StkStat | Str1 | stock_status | VARCHAR(20) | N→recorded, S→stocked |
| FinStat | Str1 | financial_status | VARCHAR(20) | ''→unpaired, F→invoiced, C→cash_register |

### Dodávateľ

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| PaCode | longint | supplier_id | INTEGER | Z hlavičky (pre index) |

### Audit

**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 7

| Btrieve | Typ | PostgreSQL | Typ | Poznámka |
|---------|-----|------------|-----|----------|
| CrtUser | Str8 | created_by | VARCHAR(8) | - |
| CrtDate + CrtTime | Date + Time | created_at | TIMESTAMP | Zlúčené |
| ModUser | Str8 | updated_by | VARCHAR(8) | - |
| ModDate + ModTime | Date + Time | updated_at | TIMESTAMP | Zlúčené |

### Párovanie s faktúrou (M:N tabuľka)

| Btrieve | PostgreSQL |
|---------|------------|
| IsdNum, IsdItm, IsdDate | supplier_delivery_invoices |

### Párovanie s objednávkou (M:N tabuľka)

| Btrieve | PostgreSQL |
|---------|------------|
| OsdNum, OsdItm | supplier_delivery_orders |

### NEPRENESENÉ POLIA

**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 9.3

Pracovné polia, staré odkazy, zastarané funkcie.

---

## 3. BIZNIS LOGIKA (ŠPECIFICKÉ PRE TSI)

### Aliquotné rozdelenie NSO

**KĽÚČOVÁ FUNKCIA:** NSO náklady sa zadávajú v **hlavičke**, automaticky sa rozdeľujú na **položky**.

**Pri zmene NSO v hlavičke → prepočítať všetky položky:**

Vzorec pre každú položku:
```
ratio = položka.NC / celková_NC_všetkých_položiek

položka.colné = hlavička.colné × ratio
položka.doprava = hlavička.doprava × ratio
položka.ostatné = hlavička.ostatné × ratio

položka.OC = položka.NC + položka.colné + položka.doprava + položka.ostatné
```

**Koncept:** NSO náklady z hlavičky sa proporcionálne rozdeľujú na položky podľa pomeru ich nákupnej ceny k celkovej nákupnej cene všetkých položiek. Obstarávacia cena položky = NC + aliquotné NSO.

---

### Výpočet hodnôt položky

**Základný výpočtový reťazec:**

1. Základná hodnota pred zľavou = unit_list_price_ac × quantity
2. Zľava = list_value_ac × (discount_percent / 100)
3. Hodnota bez DPH (bez NSO) = list_value_ac - discount_value_ac
4. DPH = purchase_base_value_ac × (vat_rate / 100)
5. Hodnota s DPH (s NSO) = purchase_base_value_ac + DPH + NSO náklady
6. Obstarávacia cena s NSO = purchase_base_value_ac + NSO náklady
7. Jednotková cena s NSO = acquisition_value_ac / quantity

---

### Stavy položky - Lifecycle

```
┌──────────┐   Naskladniť   ┌─────────┐
│ RECORDED │  ───────────>  │ STOCKED │
│  (N)     │                │  (S)    │
└──────────┘                └─────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
            ┌──────────────┐         ┌───────────────┐
            │   INVOICED   │         │ CASH_REGISTER │
            │     (F)      │         │      (C)      │
            └──────────────┘         └───────────────┘

stock_status: recorded → stocked
financial_status: unpaired → invoiced/cash_register
```

**Pravidlá:**
1. **Nová položka:** stock_status='recorded', financial_status='unpaired'
2. **Naskladnenie:** stock_status='stocked' (vytvorí STM záznamy)
3. **Faktúra:** financial_status='invoiced' (vytvorí supplier_delivery_invoices)
4. **Pokladnica:** financial_status='cash_register'

---

### Trvanlivosť a šarža (Podmienené!)

**Kľúčový koncept:** Sleduje sa **LEN** pre produkty s `product_catalog.track_expiry = true`

**Pravidlá:**
- `track_expiry = true` → polia môžu byť vyplnené
- `track_expiry = false` → polia MUSIA byť NULL
- Ak je `batch_code` vyplnený → `batch_date` musí byť tiež vyplnený

**Validácia pri uložení:** Kontrola, či produkt vyžaduje sledovanie expirácie. Ak nie, polia expiry_date, batch_code, batch_date musia byť NULL.

---

### Párovanie s faktúrou (M:N na úrovni POLOŽIEK!)

**KRITICKÉ:** Párovanie je na úrovni **POLOŽIEK**, nie hlavičiek!

**Pri vytvorení faktúry:**

1. Vytvor záznam v supplier_delivery_invoices s delivery_item_id a invoice_item_id
2. Aktualizuj financial_status položky na 'invoiced'
3. Aktualizuj paired_status hlavičky podľa stavu všetkých položiek:
   - Všetky položky unpaired → 'N' (Not paired)
   - Všetky položky invoiced → 'Q' (Queued/Paired)
   - Časť položiek invoiced → 'P' (Partially paired)

**Agregácia stavu hlavičky:**

Paired_status hlavičky sa vypočíta zo stavov všetkých položiek. Ak je časť položiek vyfakturovaná, hlavička má status 'P' (partially). Ak sú všetky vyfakturované, má status 'Q' (queued). Ak žiadna, má status 'N' (not paired).

---

### Párovanie s objednávkou

**Pri vytvorení dodacieho listu z objednávky:**

Pre každú položku objednávky sa vytvorí položka dodacieho listu a následne sa vytvorí záznam v supplier_delivery_orders spájajúci delivery_item_id s order_item_id.

---

## 4. VZŤAHY S INÝMI TABUĽKAMI

### Master-Detail vzťah

```
supplier_delivery_heads (1) ──< (N) supplier_delivery_items
    ON DELETE CASCADE
```

### M:N vzťahy (SPRÁVNE NA ÚROVNI POLOŽIEK!)

```
supplier_delivery_items (M) ──< supplier_delivery_invoices >── (N) supplier_invoice_items

supplier_delivery_items (M) ──< supplier_delivery_orders >── (N) supplier_order_items
```

### Reference na katalógy (Versioning)

**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 2

```
product_id + product_modify_id → product_catalog_history

stock_id → stocks (RESTRICT)
supplier_id → partners (z hlavičky, pre index)
```

### Reference na skladové systémy

```
item_id → stock_card_movements.source_item_id (pri naskladnení)
item_id → stock_card_fifos.source_item_id (pri naskladnení)
```

---

## 5. PRÍKLAD DÁT

### Vytvorenie položky

```sql
INSERT INTO supplier_delivery_items (
    delivery_head_id, item_number,
    product_id, product_modify_id,
    stock_id, quantity,
    vat_rate, discount_percent,
    customs_cost_ac, transport_cost_ac, other_cost_ac,
    unit_price_ac,
    purchase_base_value_ac, purchase_total_value_ac,
    acquisition_value_ac,
    stock_status, financial_status,
    supplier_id,
    created_by, created_at
) VALUES (
    1, 1,
    789, 0,
    1, 10.000,
    20.00, 5.00,
    6.00, 3.00, 1.80,
    10.88,
    95.00, 124.80,
    108.80,
    'recorded', 'unpaired',
    456,
    'zoltan', '2025-01-15 10:35:00'
);
```

### Položka s trvanlivosťou a šaržou

```sql
INSERT INTO supplier_delivery_items (
    delivery_head_id, item_number,
    product_id, product_modify_id,
    stock_id, quantity, vat_rate,
    purchase_base_value_ac, purchase_total_value_ac,
    expiry_date, batch_code, batch_date,
    stock_status, financial_status,
    supplier_id, created_by, created_at
) VALUES (
    1, 2,
    890, 0,
    1, 50.000, 10.00,
    200.00, 220.00,
    '2026-06-30', 'BATCH-2025-001', '2025-01-10',
    'recorded', 'unpaired',
    456, 'zoltan', '2025-01-15 10:40:00'
);
```

### Párovanie s faktúrou

```sql
-- Vytvor párovanie
INSERT INTO supplier_delivery_invoices (
    delivery_item_id, invoice_item_id, paired_by
) VALUES (1, 555, 'zoltan');

-- Aktualizuj stav
UPDATE supplier_delivery_items
SET financial_status = 'invoiced',
    updated_by = 'zoltan',
    updated_at = '2025-01-16 09:00:00'
WHERE item_id = 1;
```

---

## 6. MIGRÁCIA

### Versioning pri migrácii

**Detaily pozri:** COMMON_DOCUMENT_PRINCIPLES.md sekcia 9.2

**Pred migráciou dokladov:**
1. Migruj produkty do `product_catalog_history` s `modify_id = 0`

**Pri migrácii položky:**

Nastavenie product_id z Btrieve GsCode, product_modify_id = 0 (prvá verzia).

### Párovanie s faktúrou

Pri migrácii kontrolovať polia IsdNum a IsdItm. Ak sú vyplnené, nájsť zodpovedajúcu položku faktúry a vytvoriť záznam v supplier_delivery_invoices. Aktualizovať financial_status na 'invoiced'.

### Stavy položky

Transformácia stavov:
- StkStat = 'S' → stock_status = 'stocked'
- StkStat = 'N' → stock_status = 'recorded'
- FinStat = 'F' → financial_status = 'invoiced'
- FinStat = 'C' → financial_status = 'cash_register'
- FinStat = '' → financial_status = 'unpaired'

### Validácia po migrácii

**Kontroly:**

1. **Počet položiek:** Porovnať item_count v hlavičke vs. skutočný počet položiek
2. **NSO rozdelenie:** Suma NSO nákladov v položkách musí sedieť s hlavičkou (rozdiel < 0.01)
3. **Trvanlivosť:** Položky s vyplnenou expiry_date musia mať produkt s track_expiry = true
4. **Párovanie:** Všetky záznamy s IsdNum musia mať záznam v supplier_delivery_invoices

---

## 7. VERZIA A ZMENY

| Verzia | Dátum | Autor | Zmeny |
|--------|-------|-------|-------|
| 2.0 | 2025-12-13 | Zoltán + Claude | Optimalizácia dokumentácie |
| 2.1 | 2025-12-15 | Zoltán + Claude | **Batch 6 migration**: Vyčistenie od SQL/Python kódu |

**Status:** ✅ Pripravené na migráciu  
**Batch:** 6 (Stock Management - dokumenty 5/7)  
**Súbor:** `docs/architecture/database/stock/documents/tables/TSI-supplier_delivery_items.md`

---

### Závislosti

**Tento dokument vyžaduje:**
- `COMMON_DOCUMENT_PRINCIPLES.md` - všeobecné zásady
- `supplier_delivery_heads` - hlavičky
- `product_catalog` + `product_catalog_history` - versioning
- `stocks`, `partners` - číselníky

**Súvisiace dokumenty:**
- `TSH-supplier_delivery_heads.md` - hlavičky
- `document_texts` - texty (univerzálna tabuľka)
- `TSP-supplier_delivery_payments.md` - platby
- `supplier_invoice_items.md` - párovanie s faktúrami
- `supplier_order_items.md` - párovanie s objednávkami

### Kľúčové inovácie

1. **Versioning systém produktov** - `product_modify_id` namiesto kopírovania
2. **M:N párovanie** - `supplier_delivery_invoices` a `supplier_delivery_orders` **NA ÚROVNI POLOŽIEK**
3. **Aliquotné rozdelenie NSO** - náklady v hlavičke → automaticky na položky
4. **Podmienená trvanlivosť** - len pre `product_catalog.track_expiry = true`
5. **Dva nezávislé stavy** - `stock_status` + `financial_status`

### Poznámky

- **supplier_delivery_invoices je SPRÁVNE v TSI** (M:N medzi položkami!)
- **paired_status hlavičky** je agregovaný z položiek
- **NSO náklady** sa zadávajú v hlavičke, prepočítavajú na položky
- **Trvanlivosť a šarža** sú podmienené podľa produktu

---

**Koniec dokumentu TSI-supplier_delivery_items.md**