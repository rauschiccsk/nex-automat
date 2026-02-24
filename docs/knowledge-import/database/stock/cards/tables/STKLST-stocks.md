# STKLST.BTR → stocks

## 1. PREHĽAD

**Účel:** Číselník skladov v systéme.

**Charakteristika:**
- Master data tabuľka pre všetky sklady
- Každý sklad má typ (tovarový, materiálový, výrobný)
- Priradenie k prevádzkovej jednotke (facility)
- Môže mať priradený default cenník
- Základ pre skladové karty a skladové dokumenty

**PostgreSQL tabuľky:**
- `stocks` - jedna tabuľka (1:1 mapping s Btrieve)

**Vzťahy:**
- Nadradené: `facilities`, `price_lists`
- Podradené: `stock_cards`, `stock_movements`, `stock_documents`

### Btrieve súbor

- **Názov:** STKLST.BTR
- **Umiestnenie:** `C:\NEX\YEARACT\STORES\STKLST.BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\STORES\`
- **Účel:** Číselník skladov (stocks catalog)
- **Primárny kľúč:** StkNum (INTEGER)
- **Indexy:** StkNum (unique), stock_code (unique)

---

## 2. MAPPING POLÍ

### Prenášané polia

| Btrieve pole | Typ | PostgreSQL pole | Typ | Poznámka |
|---|---|---|---|---|
| `StkNum` | word | `stock_id` | INTEGER | Primárny kľúč |
| - | - | `stock_code` | VARCHAR(10) | **NOVÉ**: Generované z stock_id (napr. "SK01") |
| `StkName` | Str30 | `stock_name` | VARCHAR(30) | Názov skladu |
| `StkType` | Str1 | `stock_type` | CHAR(1) | T/M/V |
| `WriNum` | word | `facility_id` | INTEGER | FK: Prevádzková jednotka |
| `PlsNum` | word | `price_list_id` | INTEGER | FK: Cenník (NULL allowed) |
| `ModUser` | Str8 | `updated_by` | VARCHAR(50) | Používateľ |
| `ModDate` + `ModTime` | DateType + TimeType | `updated_at` | TIMESTAMP | **ZLÚČENÉ**: Dátum + čas do TIMESTAMP |

### Neprenášané polia (s dôvodom)

| Btrieve pole | Typ | Dôvod neprenášania |
|---|---|---|
| `Shared` | byte | FTP synchronizácia - Btrieve technický príznak |
| `ModNum` | word | Poradové číslo modifikácie - internal counter |
| `_StkName` | Str15 | Denormalizované vyhľadávacie pole pre Btrieve index |
| `IvDate` | DateType | Dátum inventúry - historická informácia, možno vlastná tabuľka inventory |

### Nové polia v PostgreSQL

| Pole | Typ | Účel |
|---|---|---|
| `stock_code` | VARCHAR(10) | Human-readable kód (napr. "SK01", "SK02") |
| `created_at` | TIMESTAMP | Dátum vytvorenia záznamu |
| `created_by` | VARCHAR(50) | Používateľ ktorý vytvoril záznam |

---

## 3. BIZNIS LOGIKA

### Typ skladu (stock_type)

| Kód | Význam | Účel |
|---|---|---|
| `T` | Tovarový | Sklad tovaru (trade goods) |
| `M` | Materiálový | Sklad materiálu (raw materials) |
| `V` | Výrobný | Výrobný sklad (production warehouse) |

### Väzby

**1. Prevádzková jednotka (facility_id)**
- Každý sklad je priradený k prevádzkovej jednotke
- ON DELETE RESTRICT - nemožno zmazať facility ak má sklady
- Umožňuje organizačnú štruktúru (pobočky, závody)

**2. Default cenník (price_list_id)**
- Môže byť NULL (nie je povinný)
- Ak je nastavený, používa sa ako default pre dokument/faktúru zo skladu
- ON DELETE SET NULL - pri zmazaní cenníka sa iba nullne, sklad zostáva

### Validácie

1. **Typ skladu:** Musí byť 'T', 'M' alebo 'V'
2. **Názov:** Nesmie byť prázdny (TRIM(stock_name) <> '')
3. **Kód:** Nesmie byť prázdny a musí byť unique
4. **Pred DELETE:** Kontroluje sa existencia stock_cards a stock_movements, ak existujú → DELETE sa zamietne

### Automatizácia

**updated_at trigger:**
Pri každom UPDATE automaticky aktualizuje `updated_at = CURRENT_TIMESTAMP`, zabezpečuje audit trail.

**before_delete trigger:**
Kontroluje či neexistujú skladové karty alebo pohyby. Ak áno, vyvolá sa výjimka a DELETE sa zamietne.

---

## 4. VZŤAHY S INÝMI TABUĽKAMI

### Parent tabuľky (Master data)

```
facilities (facility_id)
    ↓ ON DELETE RESTRICT
stocks (facility_id)

price_lists (price_list_id)
    ↓ ON DELETE SET NULL
stocks (price_list_id)
```

### Child tabuľky (Dependent data)

```
stocks (stock_id)
    ↓ ON DELETE RESTRICT (via trigger)
stock_cards (stock_id)

stocks (stock_id)
    ↓ ON DELETE RESTRICT (via trigger)
stock_movements (stock_id)

stocks (stock_id)
    ↓ ON DELETE RESTRICT
stock_documents (stock_id)
```

### Ukážkové query patterns

**Zoznam skladov s facility:**
Načítanie všetkých skladov s informáciami o prevádzkovej jednotke, zoradené podľa kódu skladu.

**Sklady podľa typu:**
Filtrovanie skladov podľa typu (T/M/V), napríklad iba tovarové sklady.

**Kontrola existencie skladových kariet:**
Aggregate query ktorá pre každý sklad spočíta počet skladových kariet, celkové množstvo a hodnotu.

---

## 5. VALIDAČNÉ PRAVIDLÁ

### CHECK constraints

1. **stock_type:** Musí byť 'T', 'M' alebo 'V'
2. **stock_name:** Nesmie byť prázdny (TRIM(stock_name) <> '')
3. **stock_code:** Nesmie byť prázdny (TRIM(stock_code) <> '')

### UNIQUE constraints

- **stock_code:** Musí byť unique v celej tabuľke

### Trigger validations

**Pred DELETE:**
- Kontrola stock_cards - ak existujú záznamy, DELETE sa zamietne
- Kontrola stock_movements - ak existujú pohyby, DELETE sa zamietne
- Výnimka: "Cannot delete stock [code]: [count] stock cards/movements exist"

---

## 6. PRÍKLAD DÁT

```sql
INSERT INTO stocks (
    stock_id,
    stock_code,
    stock_name,
    stock_type,
    facility_id,
    price_list_id,
    created_by,
    updated_by
) VALUES
    (1, 'SK01', 'Hlavný sklad Bratislava', 'T', 1, 1, 'SYSTEM', 'SYSTEM'),
    (2, 'SK02', 'Pobočka Košice', 'T', 2, 1, 'SYSTEM', 'SYSTEM'),
    (3, 'SK03', 'Materiálový sklad', 'M', 1, NULL, 'SYSTEM', 'SYSTEM'),
    (4, 'SK04', 'Výrobný sklad Žilina', 'V', 3, NULL, 'SYSTEM', 'SYSTEM'),
    (5, 'SK05', 'Konsignačný sklad', 'T', 1, 2, 'SYSTEM', 'SYSTEM');
```

**Výsledok SELECT:**

```
stock_id | stock_code | stock_name                  | stock_type | facility_id | price_list_id
---------|------------|----------------------------|------------|-------------|---------------
1        | SK01       | Hlavný sklad Bratislava    | T          | 1           | 1
2        | SK02       | Pobočka Košice             | T          | 2           | 1
3        | SK03       | Materiálový sklad          | M          | 1           | NULL
4        | SK04       | Výrobný sklad Žilina       | V          | 3           | NULL
5        | SK05       | Konsignačný sklad          | T          | 1           | 2
```

---

## 7. POZNÁMKY PRE MIGRÁCIU

### Transformácie

**1. Generovanie stock_code**

Stock_code sa generuje z Btrieve StkNum podľa vzoru "SK" + dvojciferné číslo (napr. StkNum=1 → "SK01", StkNum=15 → "SK15").

**2. Zlúčenie ModDate + ModTime**

Btrieve polia ModDate a ModTime sa zlúčia do jediného PostgreSQL TIMESTAMP poľa updated_at pomocou datetime.combine().

**3. Validácia stock_type**

Typ skladu sa validuje - musí byť jeden z platných typov ('T', 'M', 'V'). Ak nie, vyvolá sa výjimka.

**4. NULL hodnoty**

- facility_id môže byť NULL ak WriNum = 0
- price_list_id môže byť NULL ak PlsNum = 0

**5. created_at/created_by**

Pri migrácii sa created_at nastaví rovnako ako updated_at a created_by rovnako ako updated_by.

### Poradie migrácie

**KRITICKÉ:** Stocks je master tabuľka - poradie:

```
1. ✅ facilities (prevádzky) - musí existovať PRED stocks
2. ✅ price_lists (cenníky) - musí existovať PRED stocks
3. → stocks (táto tabuľka)
4. → stock_cards (skladové karty) - závisia od stocks
5. → stock_movements (pohyby) - závisia od stocks
6. → stock_documents (doklady) - závisia od stocks
```

### Špeciálne prípady

**Duplicitné stock_code:**
Pred INSERT kontrolovať duplicitu stock_code. Ak existuje duplicita, pridať suffix "_DUP" alebo upraviť generovanie kódu.

**Kontrola pred zmazaním:**
Query pre zistenie či je možné zmazať sklad - spočíta stock_cards a stock_movements a vráti status "Možno zmazať" alebo dôvod prečo nie.

---

## 8. VERZIA A ZMENY

| Verzia | Dátum | Autor | Zmeny |
|--------|-------|-------|-------|
| 1.0 | 2025-12-11 | Zoltán + Claude | Počiatočná verzia - kompletná dokumentácia |
| 2.0 | 2025-12-15 | Zoltán + Claude | **Batch 6 migration**: Vyčistenie dokumentácie od SQL/Python kódu |

**Status:** ✅ Pripravené na migráciu  
**Batch:** 6 (Stock Management - dokumenty 2/7)  
**Súbor:** `docs/architecture/database/stock/cards/tables/STKLST-stocks.md`

---

**Migračné dependencies:**
```
facilities → stocks
price_lists → stocks
stocks → stock_cards
stocks → stock_movements
```