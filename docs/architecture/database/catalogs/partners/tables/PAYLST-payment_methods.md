# PAYLST.BTR → payment_methods

**Súbor:** PAYLST-payment_methods.md  
**Verzia:** 1.1  
**Autor:** Zoltán & Claude  
**Dátum:** 2025-12-15  
**Status:** ✅ Production Ready

---

## 1. PREHĽAD

**PostgreSQL tabuľka:** `payment_methods`  
**Účel:** Formy úhrady faktúr (hotovosť, karta, faktúra, prevodom...)

### Btrieve súbor

- **Názov:** PAYLST.BTR
- **Umiestnenie:** `C:\NEX\YEARACT\DIALS\PAYLST.BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\DIALS\`
- **Účel:** Číselník foriem úhrady faktúr

### Historický vývoj

**NEX Genesis (Btrieve):**
- PAYLST.BTR = číselník foriem úhrady faktúr
- Identifikácia len cez textový kód (PayCode: "HOT", "KAR", "FAK"...)
- Duplikácia názvov v PAB.BTR (IcPayName, IsPayName)

**NEX Automat (PostgreSQL):**
- **payment_methods** - číselník platobných metód
- Pridané numerické ID (payment_method_id) pre konzistenciu
- Eliminácia duplikácie - názvy len v číselníku

---

## 2. MAPPING POLÍ

### 2.1 Polia ktoré SA PRENÁŠAJÚ

| Btrieve pole | PostgreSQL pole | Typ transformácie | Poznámka |
|--------------|-----------------|-------------------|----------|
| **Identifikátory** |
| - | payment_method_id | New | **NOVÉ!** Numerické ID (SERIAL) |
| PayCode | payment_method_code | Direct | Kód metódy ("HOT", "KAR"...) |
| PayName | payment_method_name | Direct | Názov metódy |
| **Audit údaje** |
| ModUser | updated_by | Direct | Užívateľ ktorý uložil |
| ModDate + ModTime | updated_at | Combine | Dátum a čas zmeny |
| **Nové polia** |
| - | is_active | New | Default: TRUE |
| - | created_by | New | Same as updated_by |
| - | created_at | New | Same as updated_at |

### 2.2 Polia ktoré SA NEPRENÁŠAJÚ

| Btrieve pole | Dôvod neprenášania |
|--------------|--------------------|
| _PayName | Vyhľadávacie pole - PostgreSQL full-text search |

---

## 3. BIZNIS LOGIKA

### 3.1 Numerické ID vs textový kód

**NOVÉ v NEX Automat:**
```
payment_method_id SERIAL PRIMARY KEY  -- 1, 2, 3, 4...
```

**Prečo:**
- Konzistentný spôsob referencovania (FK)
- Rýchlejšie JOIN operácie (INTEGER vs VARCHAR)
- Možnosť zmeny kódu bez ovplyvnenia FK

**PayCode zostáva:**
- Pre ľudskú čitateľnosť
- Pre import/export
- Pre API integrácie

### 3.2 Typické platobné metódy

| Kód | Názov | Použitie |
|-----|-------|----------|
| HOT | Hotovosť | Okamžitá platba v hotovosti |
| KAR | Platobná karta | Okamžitá platba kartou |
| FAK | Faktúra | Odložená platba (splatnosť) |
| PRE | Prevodom | Bankový prevod |
| ZAL | Zálohová faktúra | Platba vopred |
| DOB | Dobierka | Platba pri doručení |

### 3.3 Použitie v partner_catalog_extensions

Referencované ako FK pre zákaznícke a dodávateľské platobné metódy:
- `customer_payment_method_id` → payment_methods(payment_method_id)
- `supplier_payment_method_id` → payment_methods(payment_method_id)

---

## 4. VZŤAHY S INÝMI TABUĽKAMI

### 4.1 Incoming (z iných tabuliek)

**Žiadne** - toto je číselník (master data).

### 4.2 Outgoing (do iných tabuliek)

```
payment_methods
    ↓
partner_catalog_extensions
    - customer_payment_method_id FK
    - supplier_payment_method_id FK
```

**Poznámka:** Faktúry môžu mať payment_method_id (archívny odkaz, BEZ FK constraint).

---

## 5. VALIDAČNÉ PRAVIDLÁ

### 5.1 Constraints

**UNIQUE constraint:**
- `payment_method_code` UNIQUE NOT NULL - každý kód len raz

**Povinné polia:**
- `payment_method_code` NOT NULL
- `payment_method_name` NOT NULL

**Default hodnoty:**
- `is_active` = TRUE
- `created_at` = CURRENT_TIMESTAMP
- `updated_at` = CURRENT_TIMESTAMP

---

## 6. PRÍKLAD DÁT

```sql
-- Základné platobné metódy
('HOT', 'Hotovosť')
('KAR', 'Platobná karta')
('FAK', 'Faktúra')
('PRE', 'Prevodom')
('ZAL', 'Zálohová faktúra')
('DOB', 'Dobierka')
('CHE', 'Šekom')
('INK', 'Inkaso')
```

---

## 7. POZNÁMKY PRE MIGRÁCIU

### 7.1 Poradie migrácie

**KRITICKÉ:**
1. ✅ Najprv migrovať **PAYLST.BTR** → payment_methods
2. ✅ Vytvoriť mapping dictionary (PayCode → payment_method_id)
3. ✅ Potom migrovať **PAB.BTR** → partner_catalog_extensions (použiť mapping)

### 7.2 Transformačné pravidlá

**Generovanie payment_method_id:**
- payment_method_id sa automaticky generuje (SERIAL)
- Pri INSERT nie je potrebné špecifikovať ID
- PostgreSQL pridelí ID automaticky (1, 2, 3...)

**Vytvorenie mapping dictionary:**
Po migrácii PAYLST → payment_methods je potrebné vytvoriť mapu:
```
PayCode → payment_method_id
"HOT" → 1
"KAR" → 2
"FAK" → 3
```

**Použitie mapping pri migrácii PAB.BTR:**
- IcPayCode (Btrieve) → customer_payment_method_id (PostgreSQL)
- IsPayCode (Btrieve) → supplier_payment_method_id (PostgreSQL)
- Vyhľadať payment_method_id podľa kódu z dictionary

**_PayName (vyhľadávacie pole):**
- V Btrieve používané pre case-insensitive vyhľadávanie
- V PostgreSQL nahradené: `WHERE payment_method_name ILIKE '%xyz%'`
- Netreba migrovať

**Eliminácia duplikácie:**
- V PAB.BTR sú IcPayName, IsPayName (duplikované názvy)
- V PostgreSQL názvy len v payment_methods
- Pri migrácii PAB → len FK, nie názvy

---

## 8. SÚVISIACE DOKUMENTY

- **partner_catalog** → `PAB-partner_catalog.md`
- **partner_catalog_extensions** → `PAB-partner_catalog.md`

---

## 9. VERZIA A ZMENY

### v1.1 (2025-12-15)
- Cleanup: odstránené SQL CREATE statements
- Cleanup: odstránené Query patterns
- Cleanup: odstránený Python migration code
- Pridané: Btrieve súbor lokácia (DIALS)
- Zachované: Mapping, biznis logika, validačné pravidlá (koncepčne)
- Redukcia: 8.3 KB → 4.2 KB (49%)

### v1.0 (2025-12-10)
- Prvotná verzia dokumentu
- Mapping PAYLST.BTR → payment_methods
- Popis číselníka platobných metód

---

**Koniec dokumentu PAYLST-payment_methods.md**