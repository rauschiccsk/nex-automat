# STKnnnnn.BTR → stock_cards

## 1. PREHĽAD

**Účel:** Skladové karty zásob - evidencia aktuálneho stavu produktov na skladoch.

**Charakteristika:**
- Hlavná tabuľka pre sledovanie zásob po skladoch
- Každý produkt má samostatnú kartu na každom sklade
- Obsahuje aktuálne množstvá, hodnoty, rezervácie, objednávky
- Sleduje príjmy, výdaje, predaj od začiatku roka
- Eviduje normatívy (min/max/opt), ceny (avg/last/act)
- Podporuje AVCO (Average Cost) aj FIFO oceňovanie

**Vzťahy:**
- Parent: `stocks` (1:N) + `products` (1:N)
- Child: `stock_card_movements` (1:N), `stock_card_fifos` (1:N), `stock_reservations` (1:N)

### Btrieve súbor

- **Názov:** STKnnnnn.BTR (kde nnnnn = číslo skladu, napr. STK00001.BTR)
- **Umiestnenie:** `C:\NEX\YEARACT\STORES\STKnnnnn.BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\STORES\`
- **Účel:** Multi-file architektúra - samostatný súbor pre každý sklad
- **Primárny kľúč:** GsCode (product_id) v rámci jedného skladu

### PostgreSQL architektúra

- **Tabuľka:** `stock_cards`
- **Štruktúra:** Jedna tabuľka pre všetky sklady
- **Pridané pole:** `stock_id` (číslo skladu, extrahované z názvu súboru)
- **Primárny kľúč:** Composite `(stock_id, product_id)`

---

## 2. MAPPING POLÍ

### Stock Cards (hlavná tabuľka)

| Btrieve Pole | Typ Btrieve | PostgreSQL Pole | Typ PostgreSQL | Transformácia | Poznámka |
|--------------|-------------|-----------------|----------------|---------------|----------|
| **PRIDANÉ** | - | stock_id | INTEGER | Z názvu súboru | **PK part 1** (STK00001 → 1) |
| GsCode | LONGINT | product_id | INTEGER | Priamo | **PK part 2** |
| BegQnt | DOUBLE | beginning_quantity | DECIMAL(15,3) | Priamo | Začiatočný stav |
| InQnt | DOUBLE | total_in_quantity | DECIMAL(15,3) | Priamo | Príjem od začiatku roka |
| OutQnt | DOUBLE | total_out_quantity | DECIMAL(15,3) | Priamo | Výdaj od začiatku roka |
| ActQnt | DOUBLE | quantity_on_hand | DECIMAL(15,3) | Priamo | Aktuálna zásoba |
| SalQnt | DOUBLE | sold_quantity | DECIMAL(15,3) | Priamo | Predané (neodpočítané) |
| NrsQnt | DOUBLE | unavailable_quantity | DECIMAL(15,3) | Priamo | Nemožné rezervovať |
| OcdQnt | DOUBLE | reserved_customer_orders | DECIMAL(15,3) | Priamo | Rezervácie objednávky |
| FreQnt | DOUBLE | free_quantity | DECIMAL(15,3) | Vypočítané | Voľné množstvo (trigger) |
| OsdQnt | DOUBLE | ordered_quantity | DECIMAL(15,3) | Priamo | Objednané od dodávateľa |
| BegVal | DOUBLE | beginning_value | DECIMAL(15,2) | Priamo | Začiatočná hodnota |
| InVal | DOUBLE | total_in_value | DECIMAL(15,2) | Priamo | Hodnota príjmu |
| OutVal | DOUBLE | total_out_value | DECIMAL(15,2) | Priamo | Hodnota výdaja |
| ActVal | DOUBLE | value_total | DECIMAL(15,2) | Priamo | Aktuálna hodnota |
| AvgPrice | DOUBLE | average_price | DECIMAL(15,2) | Priamo | Priemerná cena (AVCO) |
| LastPrice | DOUBLE | last_purchase_price | DECIMAL(15,2) | Priamo | Posledná nákupná |
| ActPrice | DOUBLE | current_fifo_price | DECIMAL(15,2) | Priamo | Aktuálna FIFO cena |
| MaxQnt | DOUBLE | max_quantity | DECIMAL(15,3) | Priamo | Maximum normatív |
| MinQnt | DOUBLE | min_quantity | DECIMAL(15,3) | Priamo | Minimum normatív |
| OptQnt | DOUBLE | optimal_quantity | DECIMAL(15,3) | Priamo | Optimum normatív |
| LastIDate | DATE | last_receipt_date | DATE | Priamo | Dátum posledného príjmu |
| LastODate | DATE | last_issue_date | DATE | Priamo | Dátum posledného výdaja |
| LastIQnt | DOUBLE | last_receipt_quantity | DECIMAL(15,3) | Priamo | Posledné množstvo príjmu |
| LastOQnt | DOUBLE | last_issue_quantity | DECIMAL(15,3) | Priamo | Posledné množstvo výdaja |
| ActSnQnt | LONGINT | unreleased_serial_count | INTEGER | Priamo | Počet nevydaných výr. čísiel |
| DisFlag | BYTE | is_discontinued | BOOLEAN | 1→true | Vyradenie |
| ModUser | STRING[8] | updated_by | VARCHAR(50) | Priamo | Audit |
| ModDate | DATE | updated_at | TIMESTAMP | Date+Time | Part of |
| ModTime | TIME | updated_at | TIMESTAMP | Date+Time | Part of |
| LinPac | LONGINT | last_supplier_id | INTEGER | Priamo | FK na partners |
| NsuQnt | DOUBLE | unsettled_quantity | DECIMAL(15,3) | Priamo | Nevysporiadané |
| OsrQnt | DOUBLE | reserved_other | DECIMAL(15,3) | Priamo | Iné rezervácie |
| FroQnt | DOUBLE | free_order_quantity | DECIMAL(15,3) | Priamo | Voľné z objednávky |
| ASaQnt | DOUBLE | current_year_sold_quantity | DECIMAL(15,3) | Priamo | Predaj aktuálny rok |
| AOuQnt | DOUBLE | current_year_issued_quantity | DECIMAL(15,3) | Priamo | Výdaj aktuálny rok |
| PSaQnt | DOUBLE | previous_year_sold_quantity | DECIMAL(15,3) | Priamo | Predaj predošlý rok |
| POuQnt | DOUBLE | previous_year_issued_quantity | DECIMAL(15,3) | Priamo | Výdaj predošlý rok |
| ImrQnt | DOUBLE | incoming_reserved_quantity | DECIMAL(15,3) | Priamo | Tovar na ceste |
| PosQnt | DOUBLE | location_quantity | DECIMAL(15,3) | Priamo | Na pozičných miestach |
| InvDate | DATE | last_inventory_date | DATE | Priamo | Posledná inventúra |
| OfrQnt | DOUBLE | available_supplier_quantity | DECIMAL(15,3) | Priamo | Dostupné od dodávateľov |

### Polia ktoré SA NEPRENÁŠAJÚ (sú v products tabuľke)

| Btrieve Pole | Dôvod neprenášania |
|--------------|-------------------|
| MgCode | FK na product_categories (v products) |
| FgCode | FK na product_categories (v products) |
| GsName | product_name (v products) |
| _GsName | Vyhľadávacie pole (nepotrebné v PostgreSQL) |
| BarCode | product_catalog_identifiers tabuľka |
| StkCode | product_code (v products) |
| MsName | unit (v products) |
| VatPrc | vat_rate (v products) |
| GsType | product_type (v products) |
| DrbMust | track_expiration (v products) |
| PdnMust | track_serial_numbers (v products) |
| GrcMth | warranty_months (v products) |
| MinMax | Vypočítané (query na základe min/max) |
| Profit | Obchodná marža (vypočítaná) |
| BPrice | sale_price_with_vat (v products) |
| Action | Cenová akcia (samostatná tabuľka?) |
| DefPos | Hlavné pozičné miesto (samostatná tabuľka?) |
| GaName | additional_name (v products) |
| _GaName | Vyhľadávacie pole (nepotrebné) |
| OsdCode | supplier_product_code (v products) |
| Sended | Technický príznak (NEX Genesis replikácia) |

**Zlúčené polia:**
- `ModDate` + `ModTime` → `updated_at` (TIMESTAMP)

**Vypočítané polia:**
- `free_quantity` = `quantity_on_hand` - `reserved_customer_orders` - `reserved_other` - `sold_quantity` (automatický trigger)

---

## 3. BIZNIS LOGIKA

### 1. Oceňovanie zásob

**NEX Genesis používa 3 metódy:**

**AVCO (Average Cost) - hlavná metóda:**
- Priemerná cena = Celková hodnota / Celkové množstvo
- `average_price = value_total / quantity_on_hand`
- Automaticky prepočítaná po každom pohybe

**FIFO (First In, First Out):**
- Aktuálna cena podľa najstaršej FIFO karty
- `current_fifo_price` - z stock_card_fifos tabuľky
- Vyžaduje vedenie FIFO kariet

**Last Purchase Price:**
- Posledná nákupná cena pri príjme
- `last_purchase_price`
- Aktualizovaná pri každom príjme

### 2. Voľné množstvo (Free Quantity)

**Automatický prepočet cez trigger:**

```
free_quantity = quantity_on_hand 
              - reserved_customer_orders 
              - reserved_other 
              - sold_quantity
```

**Príklad:**
- quantity_on_hand = 100 ks
- reserved_customer_orders = 20 ks (objednávky zákazníkov)
- reserved_other = 10 ks (iné rezervácie)
- sold_quantity = 5 ks (predané, ešte neodpočítané)
- **→ free_quantity = 100 - 20 - 10 - 5 = 65 ks**

**Poznámka:** free_quantity môže byť záporné (viac rezervácií ako zásob).

### 3. Normatívy (Min/Max/Opt)

**Kontrola normatívov:**
- **UNDER_MIN:** quantity_on_hand < min_quantity → treba objednať
- **OVER_MAX:** quantity_on_hand > max_quantity → prebytok
- **OPTIMAL:** quantity_on_hand = optimal_quantity → ideálny stav
- **NORMAL:** ostatné prípady

**Objednávacie množstvo:**
- order_quantity = optimal_quantity - quantity_on_hand
- Ak je pod minimom, objednať na optimum

### 4. Objednávanie

**Logika automatického objednávania:**
1. Kontrola: quantity_on_hand < min_quantity
2. Výpočet: order_quantity = optimal_quantity - quantity_on_hand - ordered_quantity
3. Zváženie: available_supplier_quantity (dostupné od dodávateľov)
4. Vytvorenie objednávky pre dodávateľa

### 5. Rezervácie

**Dva typy rezervácií:**

**reserved_customer_orders (OcdQnt):**
- Rezervácie pre zákaznícke objednávky
- Automaticky vytvorené pri objednávke zákazníka
- Zrušené po expedícii

**reserved_other (OsrQnt):**
- Iné typy rezervácií (výroba, interné potreby)
- Manuálne vytvorené
- Zrušené po výdaji

**Kontrola možnosti rezervácie:**
- Dostupné množstvo = free_quantity
- Rezervácia možná ak: free_quantity >= požadované_množstvo

### 6. Agregácia naprieč skladmi

**Celkový stav produktu na všetkých skladoch:**
- Suma quantity_on_hand zo všetkých skladov
- Suma value_total zo všetkých skladov
- Priemer average_price
- Suma free_quantity (celkovo dostupné)
- Suma reserved_customer_orders (celkovo rezervované)

### 7. Aktualizácia z pohybov

**Automatická aktualizácia triggermi z stock_card_movements:**

**Pri príjme (quantity > 0):**
- quantity_on_hand += quantity
- value_total += cost_value
- total_in_quantity += quantity
- total_in_value += cost_value
- last_receipt_date = document_date
- last_receipt_quantity = quantity
- average_price = value_total / quantity_on_hand

**Pri výdaji (quantity < 0):**
- quantity_on_hand -= abs(quantity)
- value_total -= abs(cost_value)
- total_out_quantity += abs(quantity)
- total_out_value += abs(cost_value)
- last_issue_date = document_date
- last_issue_quantity = abs(quantity)
- average_price = value_total / quantity_on_hand

---

## 4. VZŤAHY S INÝMI TABUĽKAMI

### Diagram vzťahov

```
stocks (1) ----< (N) stock_cards (N) >---- (1) products
                         |
                         | (optional)
                         +---- (N) >---- (1) partners (last_supplier)
                         |
                         +----< (1:N) stock_card_movements
                         +----< (1:N) stock_card_fifos
                         +----< (1:N) stock_reservations
```

### Popis vzťahov

**stock_cards → stocks (N:1)**
- Každá karta patrí jednému skladu
- FK: stock_id → stocks.stock_id
- ON DELETE RESTRICT (nemožno zmazať sklad s kartami)

**stock_cards → products (N:1)**
- Každá karta sa týka jedného produktu
- FK: product_id → products.product_id
- ON DELETE RESTRICT (nemožno zmazať produkt so skladovou kartou)

**stock_cards → partners (N:1, optional)**
- Posledný dodávateľ produktu
- FK: last_supplier_id → partners.partner_id
- ON DELETE SET NULL (ak zmazať partnera, ponechať NULL)

**stock_cards ← stock_card_movements (1:N)**
- Pohyby aktualizujú stock_cards cez triggery
- Každý príjem/výdaj aktualizuje quantity_on_hand, value_total, atď.

**stock_cards ← stock_card_fifos (1:N)**
- FIFO karty pre oceňovanie
- Potrebné pre current_fifo_price

**stock_cards ← stock_reservations (1:N)**
- Detailné rezervácie
- Agregované do reserved_customer_orders, reserved_other

---

## 5. VALIDAČNÉ PRAVIDLÁ

### Základné validácie

**1. Množstvá musia byť nezáporné**
- CHECK (quantity_on_hand >= 0)
- CHECK (beginning_quantity >= 0)
- CHECK (total_in_quantity >= 0)
- CHECK (total_out_quantity >= 0)

**Poznámka:** free_quantity MÔŽE byť záporné (viac rezervácií ako zásob).

**2. Normatívy musia byť logické**
- CHECK (min_quantity IS NULL OR min_quantity >= 0)
- CHECK (max_quantity IS NULL OR max_quantity >= 0)
- CHECK (optimal_quantity IS NULL OR optimal_quantity >= 0)
- CHECK (min_quantity IS NULL OR max_quantity IS NULL OR min_quantity <= max_quantity)

**3. Ceny musia byť nezáporné**
- CHECK (average_price >= 0)
- CHECK (last_purchase_price >= 0)
- CHECK (current_fifo_price >= 0)

**4. Hodnoty musia byť nezáporné**
- CHECK (value_total >= 0)
- CHECK (beginning_value >= 0)
- CHECK (total_in_value >= 0)
- CHECK (total_out_value >= 0)

**5. Jedinečnosť (stock_id, product_id)**
- Automaticky zabezpečené PRIMARY KEY constraint

### Automatické aktualizácie (triggers)

**Trigger pre free_quantity:**
- BEFORE INSERT OR UPDATE
- Automatický prepočet voľného množstva
- free_quantity = quantity_on_hand - reserved_customer_orders - reserved_other - sold_quantity

**Trigger pre kontrolu normatívov:**
- AFTER INSERT OR UPDATE
- RAISE NOTICE ak pod minimom
- RAISE NOTICE ak nad maximom

**Trigger pre updated_at:**
- BEFORE UPDATE
- Automatické nastavenie updated_at = CURRENT_TIMESTAMP

---

## 6. PRÍKLAD DÁT

```sql
-- Príklad 1: Bežný produkt s dostatočnou zásobou
INSERT INTO stock_cards (
    stock_id, product_id,
    beginning_quantity, beginning_value,
    total_in_quantity, total_in_value,
    total_out_quantity, total_out_value,
    quantity_on_hand, value_total,
    average_price, last_purchase_price, current_fifo_price,
    min_quantity, max_quantity, optimal_quantity,
    last_receipt_date, last_issue_date
) VALUES (
    1, 12345,
    100.000, 5000.00,
    500.000, 26000.00,
    380.000, 19570.00,
    220.000, 11430.00,
    51.95, 52.00, 51.90,
    50.000, 300.000, 200.000,
    '2025-12-01', '2025-12-10'
);

-- Príklad 2: Produkt pod minimom (treba objednať)
INSERT INTO stock_cards (
    stock_id, product_id,
    beginning_quantity, beginning_value,
    quantity_on_hand, value_total,
    average_price, last_purchase_price,
    min_quantity, max_quantity, optimal_quantity,
    reserved_customer_orders,
    last_issue_date
) VALUES (
    1, 67890,
    200.000, 10000.00,
    35.000, 1750.00,  -- ⚠️ POD MINIMOM (min=50)
    50.00, 50.00,
    50.000, 300.000, 200.000,
    10.000,
    '2025-12-08'
);

-- Príklad 3: Produkt s vysokými rezerváciami
INSERT INTO stock_cards (
    stock_id, product_id,
    quantity_on_hand, value_total,
    average_price,
    reserved_customer_orders,
    reserved_other,
    sold_quantity
) VALUES (
    2, 11111,
    100.000, 8000.00,
    80.00,
    60.000,  -- Rezervované objednávky
    15.000,  -- Iné rezervácie
    5.000    -- Predané (neodpočítané)
    -- free_quantity = 100-60-15-5 = 20 (trigger vypočíta)
);

-- Príklad 4: Vyradený produkt
INSERT INTO stock_cards (
    stock_id, product_id,
    quantity_on_hand, value_total,
    average_price,
    is_discontinued
) VALUES (
    1, 99999,
    0.000, 0.00,
    25.00,
    true  -- ❌ VYRADENÉ
);
```

---

## 7. POZNÁMKY PRE MIGRÁCIU

### Multi-file Btrieve architektúra

**Štruktúra súborov:**
- Btrieve: STK00001.BTR (sklad 1), STK00002.BTR (sklad 2), ...
- PostgreSQL: stock_cards (jedna tabuľka + stock_id)

**Migračný proces:**
1. Nájdi všetky STKnnnnn.BTR súbory v STORES adresári
2. Extrahuj stock_id z názvu súboru (STK00001 → 1)
3. Pre každý súbor:
   - Otvor Btrieve súbor
   - Načítaj všetky záznamy
   - INSERT do PostgreSQL s pridaným stock_id
4. PK je composite (stock_id, product_id)

### Dôležité upozornenia

**1. Primárny kľúč:**
- Btrieve: GsCode (unique len v rámci jedného skladu)
- PostgreSQL: Composite PK (stock_id, product_id)
- Musí byť unique naprieč skladmi

**2. Denormalizované polia SA NEPRENÁŠAJÚ:**
- Všetky údaje z products (názov, jednotka, DPH, typ...)
- Získame cez JOIN na products tabuľku
- Znižuje redundanciu a zlepšuje konzistenciu

**3. Vypočítané polia:**
- free_quantity - automatický trigger
- MinMax príznak - nahradené query
- Profit - vypočítané (sale_price - average_price)

**4. Metódy oceňovania:**
- **AVCO:** average_price (hlavná metóda, automatický prepočet)
- **FIFO:** current_fifo_price (vyžaduje stock_card_fifos tabuľku)
- **Last:** last_purchase_price (posledná nákupná cena)

**5. Negatívne stavy:**
- CHECK constraint: quantity_on_hand >= 0
- Ale free_quantity MÔŽE byť záporné (viac rezervácií ako zásob)
- To je validný stav - upozornenie, nie chyba

**6. Trigger aktualizácie:**
- stock_card_movements INSERT → aktualizuje stock_cards
- Automatický prepočet quantity_on_hand, value_total, average_price
- Trigger sa vykonáva po každom pohybe

**7. Indexy:**
- Composite PK: (stock_id, product_id)
- Jednotlivé: stock_id, product_id
- Výkonové: quantity, value, prices, dates, discontinued

**8. Historické dáta:**
- current_year_sold_quantity - predaj za aktuálny rok
- previous_year_sold_quantity - predaj za predošlý rok
- Na konci roka: previous ← current, current ← 0
- Umožňuje year-over-year porovnanie

### Extrakcia stock_id z názvu súboru

```python
import os
import glob

# Nájsť všetky STK súbory
stk_files = glob.glob('C:/NEX/YEARACT/STORES/STK?????.BTR')

for stk_file in sorted(stk_files):
    # Extrahovať číslo skladu z názvu súboru
    # STK00001.BTR → stock_id = 1
    filename = os.path.basename(stk_file)
    stock_id = int(filename[3:8])  # "STK00001.BTR" → "00001" → 1
    
    print(f"Processing {filename} (stock_id={stock_id})")
    
    # ... migrácia záznamy s stock_id
```

### Kontrola konzistencie po migrácii

**1. Kontrola quantity_on_hand:**
- Skontrolovať či quantity_on_hand = beginning_quantity + total_in_quantity - total_out_quantity
- Ak nie, prepočítať z stock_card_movements

**2. Kontrola value_total:**
- Skontrolovať či value_total = beginning_value + total_in_value - total_out_value
- Ak nie, prepočítať z stock_card_movements

**3. Kontrola average_price:**
- Skontrolovať či average_price = value_total / quantity_on_hand
- Ak quantity_on_hand = 0, average_price by mal byť 0 alebo last_purchase_price

**4. Kontrola current_fifo_price:**
- Skontrolovať s najstaršou aktívnou FIFO kartou
- Ak žiadna aktívna FIFO, použiť last_purchase_price

**5. Kontrola free_quantity:**
- Trigger automaticky prepočíta
- Skontrolovať: free_quantity = quantity_on_hand - reserved_customer_orders - reserved_other - sold_quantity

---

## 8. VERZIA A ZMENY

| Verzia | Dátum | Autor | Zmeny |
|--------|-------|-------|-------|
| 1.0 | 2025-12-11 | Zoltán + Claude | Prvá verzia dokumentácie |
| 1.1 | 2025-12-15 | Zoltán + Claude | Vyčistenie - batch 6 migration |

**Status:** ✅ Pripravené na migráciu  
**Batch:** Batch 6 (Stock Management - dokument 7/7 - COMPLETE)  
**Súbor:** `docs/architecture/database/stock/cards/tables/STK-stock_cards.md`