# Stock Cards - Skladové karty zásob

**Účel:** Komplexný systém pre správu skladových kariet, FIFO oceňovanie a skladové pohyby.

**Rozsah:** Aktuálne stavy zásob, FIFO karty, denník skladových pohybov.

**Status:** ✅ Kompletný (Session 5)

---

## 📋 OBSAH

1. [Prehľad systému](#prehľad-systému)
2. [Tabuľky](#tabuľky)
3. [FIFO logika](#fifo-logika)
4. [Query patterns](#query-patterns)
5. [Dokumenty](#dokumenty)

---

## PREHĽAD SYSTÉMU

### Architektúra skladových kariet

```
┌─────────────────────────────────────────────────────────┐
│                    STOCK CARDS SYSTEM                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌────────────────────────────────────────────────┐   │
│  │           stock_cards (Aktuálny stav)          │   │
│  ├────────────────────────────────────────────────┤   │
│  │ PK: (stock_id, product_id)                     │   │
│  │                                                 │   │
│  │ • Množstvá:                                    │   │
│  │   - quantity_on_hand (aktuálna zásoba)         │   │
│  │   - reserved_customer_orders                   │   │
│  │   - free_quantity (dostupné)                   │   │
│  │   - ordered_quantity (objednané)               │   │
│  │                                                 │   │
│  │ • Hodnoty:                                     │   │
│  │   - value_total (celková hodnota)              │   │
│  │   - average_price (AVCO)                       │   │
│  │   - current_fifo_price (FIFO)                  │   │
│  │   - last_purchase_price (posledná)             │   │
│  │                                                 │   │
│  │ • Normatívy:                                   │   │
│  │   - min_quantity, max_quantity                 │   │
│  │   - optimal_quantity                           │   │
│  │                                                 │   │
│  │ • Štatistiky:                                  │   │
│  │   - current_year_sold_quantity                 │   │
│  │   - previous_year_sold_quantity                │   │
│  │                                                 │   │
│  │ 🔄 Aktualizované: Triggery z movements        │   │
│  └────────────────────────────────────────────────┘   │
│                       │                                 │
│                       │ 1:N                             │
│                       ▼                                 │
│  ┌────────────────────────────────────────────────┐   │
│  │      stock_card_fifos (FIFO karty)             │   │
│  ├────────────────────────────────────────────────┤   │
│  │ PK: fifo_id (BIGSERIAL)                        │   │
│  │                                                 │   │
│  │ • Každý príjem = nová FIFO karta              │   │
│  │ • Status: A/W/X                                │   │
│  │   - A = Active (aktívna)                       │   │
│  │   - W = Waiting (čakajúca)                     │   │
│  │   - X = eXhausted (spotrebovaná)               │   │
│  │                                                 │   │
│  │ • Bilancia:                                    │   │
│  │   - received_quantity (prijaté)                │   │
│  │   - issued_quantity (vydané)                   │   │
│  │   - remaining_quantity (zostatok)              │   │
│  │     → received - issued = remaining            │   │
│  │                                                 │   │
│  │ • Šarže:                                       │   │
│  │   - batch_code, batch_date                     │   │
│  │   - expiration_date (trvanlivosť)              │   │
│  │                                                 │   │
│  │ 🔄 Aktualizované: Triggery z movements        │   │
│  └────────────────────────────────────────────────┘   │
│                       │                                 │
│                       │ 1:N                             │
│                       ▼                                 │
│  ┌────────────────────────────────────────────────┐   │
│  │  stock_card_movements (Skladové pohyby)        │   │
│  ├────────────────────────────────────────────────┤   │
│  │ PK: movement_id (BIGSERIAL)                    │   │
│  │                                                 │   │
│  │ • Typy pohybov:                                │   │
│  │   - Príjmy (+)                                 │   │
│  │   - Výdaje (-)                                 │   │
│  │   - Korekcie (± inventúra)                     │   │
│  │   - Prevody (IN/OUT)                           │   │
│  │                                                 │   │
│  │ • Prepojenie:                                  │   │
│  │   - fifo_id → stock_card_fifos                 │   │
│  │   - partner_id → partners                      │   │
│  │   - contra_stock_id → stocks (prevody)         │   │
│  │                                                 │   │
│  │ • Audit trail:                                 │   │
│  │   - document_number, document_date             │   │
│  │   - created_by, created_at                     │   │
│  │                                                 │   │
│  │ ⚡ Triggery: Aktualizujú cards a fifos         │   │
│  └────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## TABUĽKY

### 1. stock_cards - Skladové karty

**Účel:** Aktuálny stav produktov na skladoch.

**Dokumentácia:** [STK-stock_cards.md](tables/STK-stock_cards.md)

**Composite PK:** `(stock_id, product_id)`

**Kľúčové vlastnosti:**
- ✅ Jeden záznam = jeden produkt na jednom sklade
- ✅ Aktualizované automaticky cez triggery
- ✅ Denormalizované pre výkon (agregované hodnoty)
- ✅ Podporuje 3 metódy oceňovania (AVCO, FIFO, Last)

**Hlavné polia:**

| Kategória | Polia |
|-----------|-------|
| **Množstvá** | quantity_on_hand, reserved_*, free_quantity, ordered_quantity |
| **Hodnoty** | value_total, average_price, current_fifo_price, last_purchase_price |
| **Normatívy** | min_quantity, max_quantity, optimal_quantity |
| **Štatistiky** | current_year_*, previous_year_*, total_in_*, total_out_* |
| **Posledné pohyby** | last_receipt_date, last_issue_date, last_receipt_quantity |

**Počet záznamov:** Cca produkt_count × stock_count (napr. 10 000 produktov × 5 skladov = 50 000)

---

### 2. stock_card_fifos - FIFO karty

**Účel:** FIFO karty pre oceňovanie zásob podľa princípu First In, First Out.

**Dokumentácia:** [FIF-stock_card_fifos.md](tables/FIF-stock_card_fifos.md)

**PK:** `fifo_id` (BIGSERIAL, unique naprieč skladmi)

**Kľúčové vlastnosti:**
- ✅ Každý príjem tovaru vytvorí novú FIFO kartu
- ✅ Výdaj sa realizuje z najstaršej aktívnej karty
- ✅ Status automaticky mení trigger (A → X ak zostatok = 0)
- ✅ Sleduje šarže a trvanlivosť

**Stavy FIFO karty:**

| Status | Názov | Popis |
|--------|-------|-------|
| **A** | Active | Aktívna - možno z nej vydávať |
| **W** | Waiting | Čakajúca - staršie karty sú ešte aktívne |
| **X** | eXhausted | Spotrebovaná - všetko vydané |

**Hlavné polia:**

| Kategória | Polia |
|-----------|-------|
| **Identifikácia** | fifo_id, stock_id, product_id |
| **Doklad** | document_number, document_line_number, document_date |
| **Množstvá** | received_quantity, issued_quantity, remaining_quantity |
| **Oceňovanie** | purchase_price |
| **Šarže** | batch_code, batch_date, expiration_date |
| **Status** | status (A/W/X) |
| **Partner** | supplier_id |

**Počet záznamov:** Tisíce až desiatky tisíc aktívnych FIFO kariet

---

### 3. stock_card_movements - Skladové pohyby

**Účel:** Denník skladových pohybov - kompletný audit trail všetkých pohybov zásob.

**Dokumentácia:** [STM-stock_card_movements.md](tables/STM-stock_card_movements.md)

**PK:** `movement_id` (BIGSERIAL, unique naprieč skladmi)

**Kľúčové vlastnosti:**
- ✅ Všetky príjmy, výdaje, korekcie, prevody
- ✅ Jeden výdaj môže vytvoriť viacero záznamov (cez viacero FIFO)
- ✅ Triggery aktualizujú stock_cards a stock_card_fifos
- ✅ Kompletný audit trail (kto, kedy, čo)

**Typy pohybov (movement_type_code):**

| Kód | Typ | Quantity | Poznámka |
|-----|-----|----------|----------|
| 1 | Príjem z nákupu | + | Vytvorí FIFO kartu |
| 2 | Výdaj na predaj | - | Z FIFO karty |
| 5 | Prevod IN | + | Z iného skladu |
| 6 | Prevod OUT | - | Do iného skladu |
| 21 | Korekcia + | + | Inventúra (našli viac) |
| 22 | Korekcia - | - | Inventúra (našli menej) |
| 31 | Počiatočný stav | + | Začiatok roka |

**Hlavné polia:**

| Kategória | Polia |
|-----------|-------|
| **Identifikácia** | movement_id, stock_id, product_id |
| **Doklad** | document_number, document_line_number, document_date |
| **Typ pohybu** | movement_type_code |
| **Množstvo** | quantity (+ príjem, - výdaj), cost_value |
| **FIFO prepojenie** | fifo_id |
| **Partner** | partner_id, supplier_id |
| **Prevody** | contra_stock_id (protisklad) |
| **Audit** | created_by, created_at, updated_by, updated_at |

**Počet záznamov:** Státisíce až milióny záznamov

---

## FIFO LOGIKA

### 1. Príjem tovaru

**Proces:**
```
1. Príjmový doklad (PRI2025/0100)
   │
   ├──> Vytvor FIFO kartu (stock_card_fifos)
   │    - received_quantity = 100
   │    - issued_quantity = 0
   │    - remaining_quantity = 100
   │    - status = 'A'
   │
   └──> Vytvor movement záznam (stock_card_movements)
        - quantity = +100
        - fifo_id = [nová FIFO karta]
        │
        └──> Trigger aktualizuje stock_cards
             - quantity_on_hand += 100
             - value_total += cost_value
             - average_price = recalc
```

**Výsledok:** 1 príjem = 1 FIFO karta = 1 STM záznam

---

### 2. Výdaj - jednoduchý prípad

**Scenár:** Výdaj 30 ks, FIFO #1 má zostatok 100 ks

**Proces:**
```
1. Výdajový doklad (VYD2025/0050)
   │
   └──> Vytvor movement záznam (stock_card_movements)
        - quantity = -30
        - fifo_id = 100001 (najstaršia aktívna)
        │
        ├──> Trigger aktualizuje stock_card_fifos
        │    - issued_quantity += 30
        │    - remaining_quantity -= 30
        │    - status = 'A' (stále aktívna, zostatok 70)
        │
        └──> Trigger aktualizuje stock_cards
             - quantity_on_hand -= 30
             - value_total -= cost_value
```

**Výsledok:** 1 výdaj z 1 FIFO = 1 STM záznam

---

### 3. Výdaj - cez viacero FIFO ⭐

**Scenár:** Výdaj 120 ks, dostupné:
- FIFO #1 (2025-01-15): 50 ks zostatok
- FIFO #2 (2025-02-01): 200 ks zostatok

**Proces:**
```
1. Výdajový doklad (VYD2025/0060)
   │
   ├──> Vytvor movement #1 (stock_card_movements)
   │    - quantity = -50 (celý zostatok FIFO #1)
   │    - fifo_id = 100001
   │    │
   │    └──> Trigger aktualizuje stock_card_fifos
   │         - FIFO #1: remaining = 0, status = 'X'
   │
   └──> Vytvor movement #2 (stock_card_movements)
        - quantity = -70 (čiastočne z FIFO #2)
        - fifo_id = 100002
        │
        └──> Trigger aktualizuje stock_card_fifos
             - FIFO #2: remaining = 130, status = 'A'
```

**Výsledok:** 1 výdaj z 2 FIFO = 2 STM záznamy!

**Pravidlo:** Jeden doklad (document_number, document_line_number) môže mať viacero STM záznamov s rôznymi fifo_id.

---

### 4. Prevod medzi skladmi

**Scenár:** Prevod 20 ks z Skladu 1 → Sklad 2

**Proces:**
```
1. Doklad prevodu (PRV2025/0010)
   │
   ├──> Vytvor movement OUT (stock_card_movements)
   │    - stock_id = 1
   │    - quantity = -20
   │    - contra_stock_id = 2
   │    - fifo_id = 100001 (z najstaršej FIFO v Sklade 1)
   │
   └──> Vytvor movement IN (stock_card_movements)
        - stock_id = 2
        - quantity = +20
        - contra_stock_id = 1
        - fifo_id = 200050 (nová FIFO v Sklade 2)
```

**Výsledok:** 1 prevod = 2 STM záznamy (OUT + IN)

---

## QUERY PATTERNS

### Získanie najstaršej aktívnej FIFO karty

```sql
SELECT *
FROM stock_card_fifos
WHERE stock_id = 1
  AND product_id = 12345
  AND status = 'A'
ORDER BY document_date ASC, fifo_id ASC
LIMIT 1;
```

### Aktuálna FIFO cena produktu

```sql
SELECT purchase_price as current_fifo_price
FROM stock_card_fifos
WHERE stock_id = 1
  AND product_id = 12345
  AND status = 'A'
ORDER BY document_date ASC
LIMIT 1;
```

### História pohybov produktu

```sql
SELECT 
    m.document_date,
    m.document_number,
    m.movement_type_code,
    m.quantity,
    m.cost_value,
    f.fifo_id,
    f.remaining_quantity as fifo_remaining,
    p.partner_name
FROM stock_card_movements m
LEFT JOIN stock_card_fifos f ON m.fifo_id = f.fifo_id
LEFT JOIN partners p ON m.partner_id = p.partner_id
WHERE m.stock_id = 1
  AND m.product_id = 12345
ORDER BY m.document_date DESC, m.movement_id DESC;
```

### Agregácia naprieč skladmi

```sql
SELECT 
    p.product_id,
    p.product_code,
    p.product_name,
    SUM(sc.quantity_on_hand) as total_quantity,
    SUM(sc.value_total) as total_value,
    AVG(sc.average_price) as avg_price
FROM products p
LEFT JOIN stock_cards sc ON p.product_id = sc.product_id
WHERE sc.quantity_on_hand > 0
GROUP BY p.product_id, p.product_code, p.product_name;
```

### Produkty pod minimom (objednať)

```sql
SELECT 
    sc.stock_id,
    sc.product_id,
    p.product_code,
    p.product_name,
    sc.quantity_on_hand,
    sc.min_quantity,
    (sc.optimal_quantity - sc.quantity_on_hand) as order_quantity
FROM stock_cards sc
JOIN products p ON sc.product_id = p.product_id
WHERE sc.quantity_on_hand < sc.min_quantity
  AND sc.is_discontinued = false
ORDER BY (sc.min_quantity - sc.quantity_on_hand) DESC;
```

### FIFO karty blízko expirácie

```sql
SELECT 
    f.stock_id,
    f.product_id,
    p.product_name,
    f.remaining_quantity,
    f.expiration_date,
    f.expiration_date - CURRENT_DATE as days_to_expiration
FROM stock_card_fifos f
JOIN products p ON f.product_id = p.product_id
WHERE f.status = 'A'
  AND f.expiration_date IS NOT NULL
  AND f.expiration_date <= CURRENT_DATE + INTERVAL '30 days'
ORDER BY f.expiration_date ASC;
```

---

## DOKUMENTY

### Tabuľky

| Dokument | Tabuľka | Btrieve | Status |
|----------|---------|---------|--------|
| [STK-stock_cards.md](tables/STK-stock_cards.md) | stock_cards | STKnnnnn.BTR | ✅ Kompletný |
| [FIF-stock_card_fifos.md](tables/FIF-stock_card_fifos.md) | stock_card_fifos | FIFnnnnn.BTR | ✅ Kompletný |
| [STM-stock_card_movements.md](tables/STM-stock_card_movements.md) | stock_card_movements | STMnnnnn.BTR | ✅ Kompletný |

### Súvisiace dokumenty

| Dokument | Účel | Status |
|----------|------|--------|
| [STKLST-stocks.md](tables/STKLST-stocks.md) | Číselník skladov | ✅ Kompletný |
| [WRILST-facilities.md](tables/WRILST-facilities.md) | Prevádzkové jednotky | ✅ Kompletný |

---

## ŠTATISTIKA

**Zdokumentované tabuľky:** 3  
**Btrieve súbory:** 3 typy × N skladov  
**PostgreSQL tabuľky:** 3 (+ stock_id)

**Session:** 5  
**Vytvorené:** 2025-12-11  
**Autor:** Zoltán + Claude

---

## KĽÚČOVÉ KONCEPTY

### Multi-sklad architektúra

**Výhody:**
- ✅ Jedna tabuľka namiesto N súborov
- ✅ Jednoduchšie queries naprieč skladmi
- ✅ Composite PK: (stock_id, product_id)
- ✅ ACID transakcie aj pri prevodoch

### Oceňovanie zásob

**3 metódy:**
1. **AVCO** (Average Cost) - `average_price`
   - Hlavná metóda
   - Automatický prepočet pri každom príjme/výdaji

2. **FIFO** (First In, First Out) - `current_fifo_price`
   - Cena najstaršej aktívnej FIFO karty
   - Aktualizuje sa pri výdaji

3. **Last Purchase** - `last_purchase_price`
   - Posledná nákupná cena
   - Aktualizuje sa pri príjme

### Triggery

**Automatické aktualizácie:**

1. **stock_card_movements → stock_cards**
   - quantity_on_hand, value_total
   - average_price (prepočet)
   - last_receipt_date, last_issue_date

2. **stock_card_movements → stock_card_fifos**
   - issued_quantity, remaining_quantity
   - status (A → X ak zostatok = 0)

3. **stock_card_fifos → stock_cards**
   - current_fifo_price (pri zmene statusu)

4. **stock_cards → free_quantity**
   - Automatický prepočet pri INSERT/UPDATE
   - free = on_hand - reserved - sold

---

## POZNÁMKY PRE IMPLEMENTÁCIU

### Príjem tovaru (receipt)

```python
# 1. Vytvor FIFO kartu
fifo = create_fifo_card(
    stock_id=1,
    product_id=12345,
    document_number='PRI2025/0100',
    received_quantity=100,
    purchase_price=50.00,
    supplier_id=5001
)

# 2. Vytvor movement
create_movement(
    stock_id=1,
    product_id=12345,
    document_number='PRI2025/0100',
    movement_type_code=1,  # Príjem
    fifo_id=fifo.fifo_id,
    quantity=100,
    cost_value=5000.00,
    partner_id=5001
)

# 3. Trigger automaticky aktualizuje stock_cards
```

### Výdaj tovaru (issue)

```python
# 1. Nájdi najstaršiu aktívnu FIFO kartu
fifos = get_active_fifos(stock_id=1, product_id=12345)
required_quantity = 120

# 2. Rozdeľ výdaj na viacero FIFO
for fifo in fifos:
    if required_quantity <= 0:
        break
    
    issue_quantity = min(required_quantity, fifo.remaining_quantity)
    
    # Vytvor movement pre túto FIFO
    create_movement(
        stock_id=1,
        product_id=12345,
        document_number='VYD2025/0060',
        movement_type_code=2,  # Výdaj
        fifo_id=fifo.fifo_id,
        quantity=-issue_quantity,
        cost_value=-(issue_quantity * fifo.purchase_price),
        partner_id=2001
    )
    
    required_quantity -= issue_quantity

# 3. Trigger automaticky aktualizuje stock_cards a fifos
```

---

**Verzia:** 1.0  
**Posledná aktualizácia:** 2025-12-11  
**Status:** ✅ Aktuálny  
**Session:** 5