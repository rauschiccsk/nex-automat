# STMnnnnn.BTR → stock_card_movements

## 1. PREHĽAD

**Účel:** Denník skladových pohybov - kompletný záznam všetkých príjmov, výdajov a korekcií zásob.

**Charakteristika:**
- Všetky pohyby zásob (príjem/výdaj/korekcia/prevod)
- Každý príjem = 1 STM záznam = 1 FIFO karta
- Každý výdaj = 1 alebo viacero STM záznamov (podľa FIFO logiky)
- Prepojenie na FIFO karty (FifNum)
- Sleduje typ pohybu (SmCode), partnera, hodnotu
- Umožňuje audit trail a históriu zmien

**Vzťahy:**
- Parent: `stock_cards` (N:1), `stock_card_fifos` (N:1), `partners` (N:1)
- Trigger: Aktualizuje `stock_cards` a `stock_card_fifos`

### Btrieve súbor

- **Názov:** STMnnnnn.BTR (kde nnnnn = číslo skladu, napr. STM00001.BTR)
- **Umiestnenie:** `C:\NEX\YEARACT\STORES\STMnnnnn.BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\STORES\`
- **Účel:** Multi-file architektúra - samostatný súbor pre každý sklad
- **Primárny kľúč:** StmNum (LONGINT)

### PostgreSQL architektúra

- **Tabuľka:** `stock_card_movements`
- **Štruktúra:** Jedna tabuľka pre všetky sklady
- **Pridané pole:** `stock_id` (číslo skladu, extrahované z názvu súboru)
- **Primárny kľúč:** `movement_id` (BIGSERIAL, unique naprieč skladmi)

---

## 2. MAPPING POLÍ

### Stock Card Movements

| Btrieve Pole | Typ Btrieve | PostgreSQL Pole | Typ PostgreSQL | Transformácia | Poznámka |
|--------------|-------------|-----------------|----------------|---------------|----------|
| **PRIDANÉ** | - | stock_id | INTEGER | Z názvu súboru | Číslo skladu (STM00001 → 1) |
| StmNum | LONGINT | movement_id | BIGSERIAL | Priamo | PK (unique naprieč skladmi) |
| DocNum | STRING[12] | document_number | VARCHAR(12) | Priamo | Číslo dokladu |
| ItmNum | LONGINT | document_line_number | INTEGER | Priamo | Riadok dokladu |
| DocDate | DATE | document_date | DATE | Priamo | Dátum dokladu |
| SmCode | WORD | movement_type_code | INTEGER | Priamo | Typ pohybu |
| GsCode | LONGINT | product_id | INTEGER | Priamo | FK na products |
| FifNum | LONGINT | fifo_id | BIGINT | Priamo | FK na stock_card_fifos |
| GsQnt | DOUBLE | quantity | DECIMAL(15,3) | Priamo | + príjem, - výdaj |
| CValue | DOUBLE | cost_value | DECIMAL(15,2) | Priamo | Nákupná hodnota bez DPH |
| PaCode | LONGINT | partner_id | INTEGER | Priamo | FK na partners (hlavný) |
| SpaCode | LONGINT | supplier_id | INTEGER | Priamo | FK na partners (dodávateľ) |
| ConStk | WORD | contra_stock_id | INTEGER | Priamo | FK na stocks (protisklad) |
| BegStat | STRING[1] | is_beginning_balance | BOOLEAN | 'B'→true | Počiatočný stav |
| ModUser | STRING[8] | updated_by | VARCHAR(50) | Priamo | Audit |
| ModDate | DATE | updated_at | TIMESTAMP | Date+Time | Part of |
| ModTime | TIME | updated_at | TIMESTAMP | Date+Time | Part of |

### Polia ktoré SA NEPRENÁŠAJÚ

| Btrieve Pole | Dôvod neprenášania |
|--------------|-------------------|
| MgCode | Tovarová skupina (v products) |
| GsName | Názov tovaru (v products) |
| BValue | Hodnota v PC s DPH (vypočítaná z cost_value + DPH) |
| Sended | Technický príznak (NEX Genesis replikácia) |
| OcdNum, OcdItm | Objednávka (môže byť samostatná tabuľka customer_orders) |
| Bprice | Predajná cena s DPH (v products alebo price_lists) |
| AcqStat | Príznak obstarania R/K (nepotrebné) |

**Zlúčené polia:**
- `ModDate` + `ModTime` → `updated_at` (TIMESTAMP)

---

## 3. BIZNIS LOGIKA

### 1. Typy skladových pohybov (movement_type_code)

**Príklady kódov SmCode:**

**Príjmy (quantity > 0):**
- 1 = Príjem z nákupu
- 5 = Prevod IN (z iného skladu)
- 11 = Príjem z výroby
- 21 = Korekcia + (inventúra)
- 31 = Počiatočný stav

**Výdaje (quantity < 0):**
- 2 = Výdaj na predaj
- 6 = Prevod OUT (do iného skladu)
- 12 = Výdaj do výroby
- 22 = Korekcia - (inventúra)
- 32 = Reklamácia

**Poznámka:** Konkrétne kódy závisia od NEX Genesis konfigurácie.

### 2. Logika príjmu

**Príjem vytvorí:**
- 1 záznam v `stock_card_movements` (quantity > 0)
- 1 záznam v `stock_card_fifos` (nová FIFO karta)

**Proces:**
1. Vytvor FIFO kartu s received_quantity
2. Vytvor movement záznam s fifo_id
3. Trigger automaticky aktualizuje stock_cards

### 3. Logika výdaja (jednoduchý prípad)

**Výdaj z jednej FIFO karty:**
- Vytvor movement záznam (quantity < 0, fifo_id)
- Trigger automaticky:
  - Aktualizuje stock_card_fifos (issued_quantity += abs(quantity), remaining -= abs(quantity))
  - Aktualizuje stock_cards (quantity_on_hand -= abs(quantity), value -= abs(cost_value))
  - Nastaví FIFO status na 'X' ak remaining = 0

### 4. Logika výdaja (cez viacero FIFO kariet) ⭐

**Výdaj väčší ako zostatok najstaršej FIFO:**

Proces:
1. Nájdi najstaršiu aktívnu FIFO kartu (ORDER BY document_date ASC)
2. Ak výdaj <= zostatok FIFO:
   - Vytvor 1 movement záznam
3. Ak výdaj > zostatok FIFO:
   - Vytvor movement záznam pre celý zostatok prvej FIFO
   - Vytvor ďalší movement záznam pre zostatok z druhej FIFO
   - Rovnaký document_number a document_line_number pre všetky záznamy

**Výsledok:**
- Viacero STM záznamov pre jeden doklad
- Každý s iným fifo_id
- FIFO karty postupne spotrebované (status 'X')

### 5. Prevody medzi skladmi

**Prevod = 2 pohyby:**

1. **Výdaj zo Skladu 1:**
   - movement_type_code = 6 (Prevod OUT)
   - quantity < 0
   - contra_stock_id = 2 (cieľový sklad)
   - fifo_id (z ktorej FIFO sa berie)

2. **Príjem do Skladu 2:**
   - movement_type_code = 5 (Prevod IN)
   - quantity > 0
   - contra_stock_id = 1 (zdrojový sklad)
   - fifo_id (nová FIFO karta v Sklade 2)

**Vlastnosti:**
- Rovnaký document_number pre oba záznamy
- Vytvorí sa nová FIFO karta v cieľovom sklade
- Prepojenie cez contra_stock_id

### 6. Korekcie (inventúra)

**Korekcia + (našli sme viac):**
- movement_type_code = 21
- quantity > 0
- cost_value = quantity × priemerná cena
- Vytvorí novú FIFO kartu

**Korekcia - (našli sme menej):**
- movement_type_code = 22
- quantity < 0
- fifo_id (môže byť z konkrétnej FIFO)
- Odpíše zo stock_cards

### 7. Počiatočný stav

**Vlastnosti:**
- is_beginning_balance = true
- Špeciálny doklad "BEGIN2025"
- movement_type_code = 31
- Vytvorí FIFO kartu s počiatočným stavom
- Typicky na začiatku roka

---

## 4. VZŤAHY S INÝMI TABUĽKAMI

### Diagram vzťahov

```
stocks (1) ----< (N) stock_card_movements (N) >---- (1) products
                         |
                         +---- (N) >---- (1) stock_card_fifos
                         |
                         +---- (N) >---- (1) stock_cards (composite FK)
                         |
                         +---- (N) >---- (1) partners (partner_id)
                         |
                         +---- (N) >---- (1) partners (supplier_id)
                         |
                         +---- (N) >---- (1) stocks (contra_stock_id)
```

### Popis vzťahov

**stock_card_movements → stocks (N:1)**
- Každý pohyb patrí do jedného skladu
- FK: stock_id → stocks.stock_id
- ON DELETE RESTRICT

**stock_card_movements → products (N:1)**
- Každý pohyb sa týka jedného produktu
- FK: product_id → products.product_id
- ON DELETE RESTRICT

**stock_card_movements → stock_card_fifos (N:1, optional)**
- Príjem: vytvorí novú FIFO kartu (fifo_id)
- Výdaj: spotrebuje z existujúcej FIFO karty
- FK: fifo_id → stock_card_fifos.fifo_id
- ON DELETE SET NULL

**stock_card_movements → stock_cards (N:1)**
- Každý pohyb aktualizuje skladovú kartu
- Composite FK: (stock_id, product_id) → stock_cards(stock_id, product_id)
- ON DELETE RESTRICT

**stock_card_movements → partners (N:1, optional)**
- Hlavný partner (dodávateľ pri príjme, odberateľ pri výdaji)
- FK: partner_id → partners.partner_id
- ON DELETE SET NULL

**stock_card_movements → partners (N:1, optional)**
- Originálny dodávateľ (pri prebalení, prevodoch)
- FK: supplier_id → partners.partner_id
- ON DELETE SET NULL

**stock_card_movements → stocks (N:1, optional)**
- Protisklad pri prevodoch medzi skladmi
- FK: contra_stock_id → stocks.stock_id
- ON DELETE SET NULL

---

## 5. VALIDAČNÉ PRAVIDLÁ

### Základné validácie

**1. Množstvo nesmie byť 0**
- CHECK (quantity != 0)
- Pohyb musí mať nenulové množstvo

**2. Príjem musí mať FIFO kartu**
- Ak quantity > 0, potom fifo_id IS NOT NULL
- Každý príjem vytvára FIFO kartu

**3. Logika contra_stock_id**
- contra_stock_id je NULL alebo movement_type_code IN (5, 6)
- Len pri prevodoch medzi skladmi

**4. Validácia FIFO zostátku (trigger)**
- Pri výdaji skontroluj či FIFO má dostatok
- remaining_quantity >= abs(new.quantity)
- Vyhodi chybu ak nie je dostatok

### Automatické aktualizácie (triggers)

**Pri INSERT do stock_card_movements:**

1. **Aktualizuj stock_cards:**
   - Príjem (quantity > 0):
     - quantity_on_hand += quantity
     - value_total += cost_value
     - total_in_quantity += quantity
     - total_in_value += cost_value
     - last_receipt_date = document_date
   - Výdaj (quantity < 0):
     - quantity_on_hand -= abs(quantity)
     - value_total -= abs(cost_value)
     - total_out_quantity += abs(quantity)
     - total_out_value += abs(cost_value)
     - last_issue_date = document_date

2. **Aktualizuj stock_card_fifos (ak je fifo_id):**
   - Výdaj:
     - issued_quantity += abs(quantity)
     - remaining_quantity -= abs(quantity)
     - Ak remaining = 0, nastav status = 'X'

3. **Prepočítaj average_price:**
   - average_price = value_total / quantity_on_hand
   - Ak quantity_on_hand = 0, potom 0

---

## 6. PRÍKLAD DÁT

```sql
-- Príklad 1: Príjem z nákupu
INSERT INTO stock_card_movements (
    movement_id, stock_id, product_id,
    document_number, document_line_number, document_date,
    movement_type_code, fifo_id,
    quantity, cost_value, partner_id
) VALUES (
    200001, 1, 12345,
    'PRI2025/0100', 1, '2025-12-11',
    1, 100001,
    100.000, 5000.00, 5001
);

-- Príklad 2: Výdaj na predaj (z jednej FIFO)
INSERT INTO stock_card_movements (
    movement_id, stock_id, product_id,
    document_number, document_line_number, document_date,
    movement_type_code, fifo_id,
    quantity, cost_value, partner_id
) VALUES (
    200002, 1, 12345,
    'VYD2025/0050', 1, '2025-12-11',
    2, 100001,
    -30.000, -1500.00, 2001
);

-- Príklad 3a: Výdaj (z viacerých FIFO) - prvá časť
INSERT INTO stock_card_movements (
    movement_id, stock_id, product_id,
    document_number, document_line_number, document_date,
    movement_type_code, fifo_id,
    quantity, cost_value, partner_id
) VALUES (
    200003, 1, 12345,
    'VYD2025/0060', 1, '2025-12-11',
    2, 100001,
    -70.000, -3500.00, 2002
);

-- Príklad 3b: Výdaj (z viacerých FIFO) - druhá časť (ten istý doklad!)
INSERT INTO stock_card_movements (
    movement_id, stock_id, product_id,
    document_number, document_line_number, document_date,
    movement_type_code, fifo_id,
    quantity, cost_value, partner_id
) VALUES (
    200004, 1, 12345,
    'VYD2025/0060', 1, '2025-12-11',
    2, 100002,
    -50.000, -2600.00, 2002
);

-- Príklad 4: Prevod OUT (do iného skladu)
INSERT INTO stock_card_movements (
    movement_id, stock_id, product_id,
    document_number, document_line_number, document_date,
    movement_type_code, fifo_id,
    quantity, cost_value, contra_stock_id
) VALUES (
    200005, 1, 12345,
    'PRV2025/0010', 1, '2025-12-11',
    6, 100002,
    -20.000, -1040.00, 2
);

-- Príklad 5: Prevod IN (z iného skladu)
INSERT INTO stock_card_movements (
    movement_id, stock_id, product_id,
    document_number, document_line_number, document_date,
    movement_type_code, fifo_id,
    quantity, cost_value, contra_stock_id
) VALUES (
    200006, 2, 12345,
    'PRV2025/0010', 1, '2025-12-11',
    5, 100050,
    20.000, 1040.00, 1
);

-- Príklad 6: Korekcia + (inventúra)
INSERT INTO stock_card_movements (
    movement_id, stock_id, product_id,
    document_number, document_line_number, document_date,
    movement_type_code,
    quantity, cost_value
) VALUES (
    200007, 1, 12345,
    'INV2025/0001', 1, '2025-12-11',
    21,
    5.000, 250.00
);

-- Príklad 7: Počiatočný stav
INSERT INTO stock_card_movements (
    movement_id, stock_id, product_id,
    document_number, document_line_number, document_date,
    movement_type_code, fifo_id,
    quantity, cost_value, is_beginning_balance
) VALUES (
    100000, 1, 67890,
    'BEGIN2025', 1, '2025-01-01',
    31, 90000,
    150.000, 6750.00, true
);
```

---

## 7. POZNÁMKY PRE MIGRÁCIU

### Multi-file Btrieve architektúra

**Štruktúra súborov:**
- Btrieve: STM00001.BTR (sklad 1), STM00002.BTR (sklad 2), ...
- PostgreSQL: stock_card_movements (jedna tabuľka + stock_id)

**Migračný proces:**
1. Nájdi všetky STMnnnnn.BTR súbory v STORES adresári
2. Extrahuj stock_id z názvu súboru (STM00001 → 1)
3. Pre každý súbor:
   - Otvor Btrieve súbor
   - Načítaj všetky záznamy
   - INSERT do PostgreSQL s pridaným stock_id
4. PK movement_id musí byť unique naprieč skladmi

### Dôležité upozornenia

**1. Primárny kľúč:**
- StmNum je unique len v rámci jedného skladu
- V PostgreSQL musí byť movement_id unique naprieč skladmi
- Riešenie: použiť BIGSERIAL a generovať nové ID

**2. Výdaj cez viacero FIFO:**
- Jeden doklad môže mať viacero STM záznamov
- Každý s iným fifo_id
- Rovnaký document_number a document_line_number

**3. Triggery:**
- Automaticky aktualizujú stock_cards
- Automaticky aktualizujú stock_card_fifos
- Prepočítavajú average_price

**4. Prevody medzi skladmi:**
- Vytvoria 2 movements (OUT + IN)
- Prepojené cez contra_stock_id
- Rovnaký document_number

**5. Počiatočný stav:**
- is_beginning_balance = true
- Typicky na začiatku roka
- Vytvorí FIFO kartu

### Extrakcia stock_id z názvu súboru

```python
import glob

# Nájsť všetky STM súbory
stm_files = glob.glob('C:/NEX/YEARACT/STORES/STM?????.BTR')

for stm_file in sorted(stm_files):
    # Extrahovať číslo skladu z názvu súboru
    # STM00001.BTR → stock_id = 1
    filename = os.path.basename(stm_file)
    stock_id = int(filename[3:8])  # "STM00001.BTR" → "00001" → 1
    
    print(f"Processing {filename} (stock_id={stock_id})")
```

---

## 8. VERZIA A ZMENY

| Verzia | Dátum | Autor | Zmeny |
|--------|-------|-------|-------|
| 1.0 | 2025-12-11 | Zoltán + Claude | Prvá verzia dokumentácie |
| 1.1 | 2025-12-15 | Zoltán + Claude | Vyčistenie - batch 6 migration |

**Status:** ✅ Pripravené na migráciu  
**Batch:** Batch 6 (Stock Management - dokument 6/7)  
**Súbor:** `docs/architecture/database/stock/cards/tables/STM-stock_card_movements.md`