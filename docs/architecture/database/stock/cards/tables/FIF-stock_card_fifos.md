# FIFnnnnn.BTR → stock_card_fifos

## 1. PREHĽAD

**Účel:** FIFO karty zásob - sledovanie jednotlivých príjmov a ich postupné vyskladnenie.

**Charakteristika:**
- Každý príjem tovaru vytvorí novú FIFO kartu
- Výdaj sa realizuje z najstaršej aktívnej karty (FIFO princíp)
- Sleduje bilanciu: Prijaté - Vydané = Zostatok
- Statusy: A (aktívna), W (čakajúca), X (spotrebovaná)
- Eviduje trvanlivosť (DrbDate), šarže (RbaCode)
- Prepojené so skladovými pohybmi (STM) cez FifNum

**Btrieve architektúra:**
- NEX Genesis: `FIF00001.BTR` (sklad 1), `FIF00002.BTR` (sklad 2), ...
- Samostatný súbor pre každý sklad

**PostgreSQL architektúra:**
- `stock_card_fifos` - jedna tabuľka pre všetky sklady
- Pridané pole: `stock_id` (číslo skladu)
- PK: `fifo_id` (z FifNum, musí byť unique naprieč skladmi)

**Vzťahy:**
- Parent: `stock_cards` (N:1), `partners` (N:1, dodávateľ)
- Child: `stock_card_movements` (1:N)
- Related: `stock_batches` (1:N, šarže)

### Btrieve súbor

- **Názov:** FIFnnnnn.BTR (n = číslo skladu)
- **Umiestnenie:** `C:\NEX\YEARACT\STORES\FIF[NNNNN].BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\STORES\`
  - [NNNNN] = číslo skladu (00001, 00002, ...)
- **Účel:** FIFO karty zásob - sledovanie príjmov a ich vyskladnenia
- **Primárny kľúč:** FifNum (LONGINT)
- **PostgreSQL PK:** fifo_id (BIGINT, unique naprieč skladmi)

---

## 2. MAPPING POLÍ

### Stock Card FIFOs

| Btrieve Pole | Typ Btrieve | PostgreSQL Pole | Typ PostgreSQL | Transformácia | Poznámka |
|--------------|-------------|-----------------|----------------|---------------|----------|
| **PRIDANÉ** | - | stock_id | INTEGER | - | Číslo skladu (z názvu súboru) |
| FifNum | LONGINT | fifo_id | BIGSERIAL | Priamo | PK (unique naprieč skladmi) |
| DocNum | STRING[12] | document_number | VARCHAR(12) | Priamo | Číslo príjmového dokladu |
| ItmNum | LONGINT | document_line_number | INTEGER | Priamo | Riadok dokladu |
| GsCode | LONGINT | product_id | INTEGER | Priamo | FK na products |
| DocDate | DATE | document_date | DATE | Priamo | Dátum dokladu |
| DrbDate | DATE | expiration_date | DATE | Priamo | Trvanlivosť |
| InPrice | DOUBLE | purchase_price | DECIMAL(15,2) | Priamo | Nákupná cena bez DPH |
| InQnt | DOUBLE | received_quantity | DECIMAL(15,3) | Priamo | Prijaté množstvo |
| OutQnt | DOUBLE | issued_quantity | DECIMAL(15,3) | Priamo | Vydané množstvo |
| ActQnt | DOUBLE | remaining_quantity | DECIMAL(15,3) | Vypočítané | InQnt - OutQnt (trigger) |
| Status | STRING[1] | status | VARCHAR(1) | Priamo | A/W/X |
| PaCode | LONGINT | supplier_id | INTEGER | Priamo | FK na partners |
| BegStat | STRING[1] | is_beginning_balance | BOOLEAN | 'B'→true | Počiatočný stav |
| RbaCode | STRING[30] | batch_code | VARCHAR(30) | Priamo | Výrobná šarža |
| RbaDate | DATE | batch_date | DATE | Priamo | Dátum výroby šarže |

### Polia ktoré SA NEPRENÁŠAJÚ

| Btrieve Pole | Dôvod neprenášania |
|--------------|-------------------|
| Sended | Technický príznak (NEX Genesis replikácia) |
| PdnQnt | Množstvo s výrobnými číslami (stock_serial_numbers tabuľka) |
| AcqStat | Príznak obstarania R/K (nepotrebné v NEX Automat) |

**Vypočítané polia:**
- `remaining_quantity` = `received_quantity` - `issued_quantity` (trigger)
- Status automaticky 'X' ak `remaining_quantity` = 0

---

## 3. BIZNIS LOGIKA

### 1. FIFO Princíp (First In, First Out)

**Základné pravidlo:**
- Výdaj sa realizuje vždy z **najstaršej aktívnej** FIFO karty
- Poradie: `document_date` ASC (najstarší dátum príjmu)

Najstaršia aktívna FIFO karta sa získa filtrom na stock_id, product_id, status='A', zoradené podľa document_date ASC, fifo_id ASC, LIMIT 1.

### 2. Stavy FIFO karty

**A (Active) - Aktívna:**
- Karta z ktorej sa aktuálne vydáva
- remaining_quantity > 0
- Najstaršia aktívna karta je na rade

**W (Waiting) - Čakajúca:**
- Karta čaká na svoj rad
- remaining_quantity > 0
- Staršie karty sú ešte aktívne

**X (eXhausted) - Spotrebovaná:**
- Všetko už bolo vydané
- remaining_quantity = 0
- Automatická zmena cez trigger

### 3. Proces výdaja

**Scenár 1: Výdaj z jednej FIFO karty**

Dostupné: FIFO #1 = 100 ks, Výdaj: 50 ks. Výsledok: UPDATE issued_quantity += 50, remaining_quantity -= 50. Status ostáva 'A', remaining = 50.

**Scenár 2: Výdaj spotrebuje celú FIFO kartu**

Dostupné: FIFO #1 = 100 ks, Výdaj: 100 ks. Výsledok: UPDATE issued_quantity += 100, remaining_quantity = 0, status = 'X' (automaticky cez trigger).

**Scenár 3: Výdaj cez viacero FIFO kariet** ⭐

Dostupné: FIFO #1 (2025-01-01) = 50 ks, FIFO #2 (2025-01-15) = 100 ks. Výdaj: 120 ks.
- Krok 1: Výdaj z FIFO #1 (najstaršia) - 50 ks, status→'X'. Vytvorí sa stock_card_movements: -50 ks, fifo_id=1.
- Krok 2: Výdaj z FIFO #2 (ďalšia) - 70 ks, remaining=30. Vytvorí sa stock_card_movements: -70 ks, fifo_id=2.
- Výsledok: 2 záznamy v stock_card_movements!

### 4. Výpočet aktuálnej FIFO ceny

**Aktuálna FIFO cena = cena najstaršej aktívnej karty**

Získanie aktuálnej FIFO ceny produktu: SELECT purchase_price z stock_card_fifos kde stock_id, product_id, status='A', ORDER BY document_date ASC, LIMIT 1. Táto cena sa aktualizuje v stock_cards.current_fifo_price.

### 5. Sledovanie trvanlivosti (FEFO - First Expired, First Out)

**Možná úprava FIFO → FEFO:**

Pri výdaji možno uprednostniť produkty s blížiacou sa expiráciou. ORDER BY najprv podľa expiration_date (NULL na koniec), potom document_date (FIFO).

### 6. Šarže (Batches)

Vyhľadanie FIFO kariet podľa batch_code umožňuje sledovať stav výrobných šarží. Agregácia SUM(remaining_quantity) a SUM(issued_quantity) podľa batch_code poskytuje celkový stav šarže.

---

## 4. VZŤAHY S INÝMI TABUĽKAMI

### Parent tabuľky

```
stocks (1) ----< (N) stock_card_fifos
    ON DELETE RESTRICT

products (1) ----< (N) stock_card_fifos
    ON DELETE RESTRICT

partners (1) ----< (N) stock_card_fifos (supplier)
    ON DELETE SET NULL

stock_cards (1) ----< (N) stock_card_fifos
    Composite FK: (stock_id, product_id)
    ON DELETE RESTRICT
```

### Child tabuľky

```
stock_card_fifos (1) ----< (N) stock_card_movements
    Každý výdaj z FIFO karty je zaznamenaný v movements
```

### Diagram vzťahov

```
stocks (1) ----< (N) stock_card_fifos (N) >---- (1) products
                         |
                         +---- (N) >---- (1) partners (supplier)
                         |
                         +---- (N) >---- (1) stock_cards (composite FK)
                         |
                         +----< (1:N) stock_card_movements
```

---

## 5. VALIDAČNÉ PRAVIDLÁ

### CHECK constraints

1. **Množstvá musia byť logické:**
   - received_quantity > 0
   - issued_quantity >= 0
   - remaining_quantity >= 0

2. **Bilancia musí sedieť:**
   - remaining_quantity = received_quantity - issued_quantity

3. **Cena musí byť nezáporná:**
   - purchase_price >= 0

4. **Status logika:**
   - Ak status = 'X' → remaining_quantity = 0
   - Ak status IN ('A', 'W') → remaining_quantity > 0

5. **Jedinečnosť dokladu:**
   - UNIQUE INDEX na (stock_id, document_number, document_line_number)

### Trigger validations

**Automatický prepočet remaining_quantity:**

Trigger pred INSERT/UPDATE automaticky vypočíta remaining_quantity = received_quantity - issued_quantity. Ak je remaining_quantity <= 0, automaticky nastaví status = 'X'.

**Kontrola expirácie:**

Trigger po INSERT/UPDATE vyvolá WARNING ak expiration_date < CURRENT_DATE (expirovaný produkt).

---

## 6. PRÍKLAD DÁT

### Aktívna FIFO karta

```sql
INSERT INTO stock_card_fifos (
    fifo_id, stock_id, product_id,
    document_number, document_line_number, document_date,
    supplier_id,
    received_quantity, issued_quantity, remaining_quantity,
    purchase_price,
    expiration_date,
    batch_code, batch_date,
    status,
    created_by, updated_by
) VALUES (
    100001, 1, 12345,
    'PRI2025/0001', 1, '2025-01-15',
    5001,
    100.000, 30.000, 70.000,
    50.00,
    '2025-12-31',
    'BATCH2025001', '2025-01-10',
    'A',
    'system', 'system'
);
```

### Spotrebovaná FIFO karta

```sql
INSERT INTO stock_card_fifos (
    fifo_id, stock_id, product_id,
    document_number, document_line_number, document_date,
    supplier_id,
    received_quantity, issued_quantity, remaining_quantity,
    purchase_price,
    status,
    created_by, updated_by
) VALUES (
    99999, 1, 12345,
    'PRI2025/0001', 1, '2025-01-01',
    5001,
    50.000, 50.000, 0.000,
    48.00,
    'X',
    'system', 'system'
);
```

### Počiatočný stav (začiatok roka)

```sql
INSERT INTO stock_card_fifos (
    fifo_id, stock_id, product_id,
    document_number, document_line_number, document_date,
    received_quantity, issued_quantity, remaining_quantity,
    purchase_price,
    is_beginning_balance,
    status,
    created_by, updated_by
) VALUES (
    90000, 1, 67890,
    'BEGIN2025', 1, '2025-01-01',
    150.000, 0.000, 150.000,
    45.00,
    true,
    'A',
    'system', 'system'
);
```

---

## 7. POZNÁMKY PRE MIGRÁCIU

### Multi-sklad architektúra

**Btrieve:** Viacero súborov (FIF00001.BTR, FIF00002.BTR, ...)  
**PostgreSQL:** Jedna tabuľka + stock_id pole

Pri migrácii:
1. Nájsť všetky FIF?????.BTR súbory
2. Extrahovať stock_id z názvu súboru (FIF00001.BTR → stock_id = 1)
3. Pre každý súbor načítať záznamy a vložiť do stock_card_fifos
4. fifo_id musí byť unique naprieč všetkými skladmi!

### Dôležité transformácie

1. **stock_id:** Extrahovať z názvu Btrieve súboru (FIF00001.BTR → 1)
2. **remaining_quantity:** Vypočítané cez trigger (received - issued)
3. **status:** Automaticky 'X' ak remaining = 0 (trigger)
4. **is_beginning_balance:** BegStat = 'B' → true

### Neprenášané polia

- `Sended` - technický príznak replikácie
- `PdnQnt` - výrobné čísla (stock_serial_numbers tabuľka)
- `AcqStat` - príznak obstarania (nepotrebné)

### Validácie po migrácii

1. **Bilancia:** Kontrola remaining = received - issued pre všetky záznamy
2. **Status logika:** 'X' ↔ remaining = 0
3. **Unique fifo_id:** Žiadne duplicity naprieč skladmi
4. **Celkové množstvá:** SUM(remaining_quantity) v fifos = quantity_on_hand v stock_cards

### FIFO logika

**Výdaj vždy z najstaršej aktívnej karty:**
- ORDER BY document_date ASC, fifo_id ASC
- Ak výdaj > zostatok → rozdeliť na viacero stock_card_movements záznamov

### Trvanlivosť a šarže

**expiration_date:** Možnosť FEFO (First Expired, First Out) - uprednostniť skoršie expirujúce produkty.

**batch_code, batch_date:** Sledovanie výrobných šarží, agregácia stavu podľa šarže.

### Počiatočný stav

**is_beginning_balance = true:** Počiatok roka, špeciálny doklad (napr. "BEGIN2025").

---

## 8. VERZIA A ZMENY

| Verzia | Dátum | Autor | Zmeny |
|--------|-------|-------|-------|
| 1.0 | 2025-12-11 | Zoltán + Claude | Prvá verzia dokumentácie |
| 2.0 | 2025-12-15 | Zoltán + Claude | **Batch 6 migration**: Vyčistenie dokumentácie od SQL/Python kódu |

**Status:** ✅ Pripravené na migráciu  
**Batch:** 6 (Stock Management - dokumenty 4/7)  
**Súbor:** `docs/architecture/database/stock/cards/tables/FIF-stock_card_fifos.md`