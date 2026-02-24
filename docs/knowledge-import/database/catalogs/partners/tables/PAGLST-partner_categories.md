# PAGLST.BTR → partner_categories

**Súbor:** PAGLST-partner_categories.md  
**Verzia:** 1.1  
**Autor:** Zoltán & Claude  
**Dátum:** 2025-12-15  
**Status:** ✅ Production Ready

---

## 1. PREHĽAD

**PostgreSQL tabuľka:** `partner_categories`  
**Účel:** Skupiny partnerov (primárne dodávatelia, rozšírené o odberateľov)

### Btrieve súbor

- **Názov:** PAGLST.BTR
- **Umiestnenie:** `C:\NEX\YEARACT\DIALS\PAGLST.BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\DIALS\`
- **Účel:** Skupiny partnerov (číselník dodávateľských skupín)

### Historický vývoj

**NEX Genesis (Btrieve):**
- ✅ PAGLST.BTR - číselník skupín dodávateľov
- ✅ PAB.BTR pole `PagCode` - odkaz na PAGLST.BTR
- ❌ PGCLST.BTR - **neexistuje** číselník pre odberateľov!
- ⚠️ PAB.BTR pole `PgcCode` - kód bez číselníka (len textová hodnota)

**NEX Automat (PostgreSQL):**
- ✅ Unifikovaný číselník `partner_categories`
- ✅ Podporuje 2 typy: `supplier` (dodávatelia), `customer` (odberatelia)
- ✅ Migrácia z PAGLST.BTR pre `category_type = 'supplier'`
- ✅ Manuálne naplnenie pre `category_type = 'customer'`

---

## 2. MAPPING POLÍ

### 2.1 Polia ktoré SA PRENÁŠAJÚ

| Btrieve pole | PostgreSQL pole | Typ transformácie | Poznámka |
|--------------|-----------------|-------------------|----------|
| **Identifikátory** |
| PagCode | category_code | Direct | Číslo skupiny (konvertované na VARCHAR) |
| PagName | category_name | Direct | Názov skupiny |
| **Audit údaje** |
| ModUser | updated_by | Direct | Užívateľ ktorý uložil |
| ModDate + ModTime | updated_at | Combine | Dátum a čas zmeny |
| **Nové polia** |
| - | category_type | New | Fixed: 'supplier' pre PAGLST.BTR |
| - | category_description | New | NULL (možno doplniť manuálne) |
| - | is_active | New | Default: TRUE |
| - | created_by | New | Same as updated_by |
| - | created_at | New | Same as updated_at |

### 2.2 Polia ktoré SA NEPRENÁŠAJÚ

| Btrieve pole | Dôvod neprenášania |
|--------------|--------------------|
| _PagName | Vyhľadávacie pole - nie je potrebné (PostgreSQL má ILIKE) |

---

## 3. BIZNIS LOGIKA

### 3.1 Typy kategórií

**Supplier (Dodávateľ):**
- Migrované z PAGLST.BTR
- Skupiny dodávateľov podľa typu tovaru
- Napríklad: "Potraviny", "Elektronika", "Textil"

**Customer (Odberateľ):**
- **Nie sú v NEX Genesis** (číselník neexistoval)
- Manuálne naplnenie v NEX Automat
- Skupiny zákazníkov podľa typu obchodu
- Napríklad: "Maloobchod", "Veľkoobchod", "HoReCa"

### 3.2 Unique constraint

Kombinácia `(category_type, category_code)` je unique - umožňuje rovnaký kód pre supplier/customer:
- `category_type = 'supplier'`, `category_code = '001'` (Skupina dodávateľov)
- `category_type = 'customer'`, `category_code = '001'` (Skupina zákazníkov)

### 3.3 Použitie v PAB.BTR

**NEX Genesis:**
```
PAB.BTR → PagCode (WORD) → PAGLST.BTR → PagCode, PagName
PAB.BTR → PgcCode (WORD) → ❌ Bez číselníka!
```

**NEX Automat:**
```
partner_catalog → partner_catalog_categories → partner_categories
```

---

## 4. VZŤAHY S INÝMI TABUĽKAMI

### 4.1 Incoming (z iných tabuliek)

**Žiadne** - toto je číselník (master data).

### 4.2 Outgoing (do iných tabuliek)

```
partner_categories
    ↓
partner_catalog_categories (mapovacia tabuľka)
    ↓
partner_catalog
```

**ON DELETE RESTRICT:** Pri vymazaní kategórie sa nedovolí, ak je používaná v partner_catalog_categories.

---

## 5. VALIDAČNÉ PRAVIDLÁ

### 5.1 Constraints

**CHECK constraints:**
- `category_type IN ('supplier', 'customer')` - povolené typy kategórií
- `UNIQUE (category_type, category_code)` - unikátna kombinácia typ + kód

**Povinné polia:**
- `category_type` NOT NULL
- `category_code` NOT NULL
- `category_name` NOT NULL

**Default hodnoty:**
- `is_active` = TRUE
- `created_at` = CURRENT_TIMESTAMP
- `updated_at` = CURRENT_TIMESTAMP

---

## 6. PRÍKLAD DÁT

### 6.1 Skupiny dodávateľov (z PAGLST.BTR)

```sql
-- Migrované z NEX Genesis PAGLST.BTR
('supplier', '001', 'Potraviny a nápoje')
('supplier', '002', 'Elektronika a spotrebiče')
('supplier', '003', 'Textil a odevy')
```

### 6.2 Skupiny zákazníkov (nové v NEX Automat)

```sql
-- Nové kategórie pre odberateľov (neboli v NEX Genesis)
('customer', '001', 'Maloobchod')
('customer', '002', 'Veľkoobchod')
('customer', '003', 'HoReCa')
```

---

## 7. POZNÁMKY PRE MIGRÁCIU

### 7.1 Poradie migrácie

```
KRITICKÉ: Migrovať v tomto poradí!

1. partner_categories (Btrieve: PAGLST.BTR)        -- TÁTO TABUĽKA
2. partner_catalog (Btrieve: PAB00000.BTR)         -- Používa PagCode
3. partner_catalog_categories                       -- Mapovanie partnerov na kategórie
```

### 7.2 Transformačné pravidlá

**PAGLST.BTR → supplier only:**
- Všetky záznamy z PAGLST.BTR majú `category_type = 'supplier'`
- PagCode (WORD) sa transformuje na VARCHAR
- ModDate + ModTime sa kombinujú do updated_at

**PgcCode v PAB.BTR nemá číselník:**
- V NEX Genesis neexistuje PGCLST.BTR
- PgcCode je len textová hodnota bez metadát
- V NEX Automat sa migrácia PgcCode rieši:
  - Buď ignoruje (ak nie sú dôležité)
  - Alebo sa vytvoria kategórie customer manuálne

**ON CONFLICT stratégia:**
- Umožňuje re-run migrácie
- Aktualizuje existujúce záznamy
- Neruší doplnené dáta (napr. category_description)

**_PagName (vyhľadávacie pole):**
- V Btrieve používané pre case-insensitive vyhľadávanie
- V PostgreSQL nahradené: `WHERE category_name ILIKE '%xyz%'`
- Netreba migrovať

**Manuálne doplnenie customer categories:**
- Vytvoriť predvolené skupiny zákazníkov
- Užívateľ môže pridať vlastné podľa potreby
- Používať konzistentné kódy (001, 002...)

---

## 8. SÚVISIACE DOKUMENTY

- **partner_catalog** → `PAB-partner_catalog.md`
- **partner_catalog_categories** → `PAB-partner_catalog.md` (mapovacia tabuľka)

---

## 9. VERZIA A ZMENY

### v1.1 (2025-12-15)
- Cleanup: odstránené SQL CREATE statements
- Cleanup: odstránené Query patterns
- Cleanup: odstránený Python migration code
- Pridané: Btrieve súbor lokácia (DIALS)
- Zachované: Mapping, biznis logika, validačné pravidlá (koncepčne)
- Redukcia: 14.9 KB → 7.0 KB (53%)

### v1.0 (2025-12-11)
- Prvotná verzia dokumentu
- Mapping PAGLST.BTR → partner_categories (supplier)
- Poznámky o neexistencii PGCLST.BTR

---

**Koniec dokumentu PAGLST-partner_categories.md**
