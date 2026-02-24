# TRPLST.BTR → transport_methods

**Súbor:** TRPLST-transport_methods.md  
**Verzia:** 1.1  
**Autor:** Zoltán & Claude  
**Dátum:** 2025-12-15  
**Status:** ✅ Production Ready

---

## 1. PREHĽAD

**PostgreSQL tabuľka:** `transport_methods`  
**Účel:** Spôsoby dopravy tovaru (kuriér, osobný odber, pošta...)

### Btrieve súbor

- **Názov:** TRPLST.BTR
- **Umiestnenie:** `C:\NEX\YEARACT\DIALS\TRPLST.BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\DIALS\`
- **Účel:** Číselník spôsobov dopravy

### Historický vývoj

**NEX Genesis (Btrieve):**
- TRPLST.BTR = číselník spôsobov dopravy
- Identifikácia len cez textový kód (TrsCode: "KUR", "OSO", "POS"...)
- Duplikácia názvov v PAB.BTR (IcTrsName, IsTrsName)

**NEX Automat (PostgreSQL):**
- **transport_methods** - číselník dopravných metód
- Pridané numerické ID (transport_method_id) pre konzistenciu
- Eliminácia duplikácie - názvy len v číselníku

---

## 2. MAPPING POLÍ

### 2.1 Polia ktoré SA PRENÁŠAJÚ

| Btrieve pole | PostgreSQL pole | Typ transformácie | Poznámka |
|--------------|-----------------|-------------------|----------|
| **Identifikátory** |
| - | transport_method_id | New | **NOVÉ!** Numerické ID (SERIAL) |
| TrsCode | transport_method_code | Direct | Kód metódy ("KUR", "OSO"...) |
| TrsName | transport_method_name | Direct | Názov metódy |
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
| _TrsName | Vyhľadávacie pole - PostgreSQL full-text search |
| Sended | Sync flag - zastaralé |

---

## 3. BIZNIS LOGIKA

### 3.1 Numerické ID vs textový kód

**NOVÉ v NEX Automat:**
```
transport_method_id SERIAL PRIMARY KEY  -- 1, 2, 3, 4...
```

**Prečo:**
- Konzistentný spôsob referencovania (FK)
- Rýchlejšie JOIN operácie (INTEGER vs VARCHAR)
- Možnosť zmeny kódu bez ovplyvnenia FK

**TrsCode zostáva:**
- Pre ľudskú čitateľnosť
- Pre import/export
- Pre API integrácie

### 3.2 Typické dopravné metódy

| Kód | Názov | Použitie |
|-----|-------|----------|
| KUR | Kuriér | Kuriérska služba (GLS, DPD...) |
| OSO | Osobný odber | Vyzdvihnutie na sklade |
| POS | Poštou | Slovenská pošta |
| DOP | Vlastná doprava | Dovoz vlastným autom |
| ZAS | Zásielkovňa | Packeta, Zásielkovňa.sk |
| EXP | Expresná zásielka | Expresné doručenie do 24h |

### 3.3 Použitie v partner_catalog_extensions

Referencované ako FK pre zákaznícke a dodávateľské dopravné metódy:
- `customer_transport_method_id` → transport_methods(transport_method_id)
- `supplier_transport_method_id` → transport_methods(transport_method_id)

---

## 4. VZŤAHY S INÝMI TABUĽKAMI

### 4.1 Incoming (z iných tabuliek)

**Žiadne** - toto je číselník (master data).

### 4.2 Outgoing (do iných tabuliek)

```
transport_methods
    ↓
partner_catalog_extensions
    - customer_transport_method_id FK
    - supplier_transport_method_id FK
```

**Poznámka:** Príjemky/výdajky môžu mať transport_method_id (archívny odkaz, BEZ FK constraint).

---

## 5. VALIDAČNÉ PRAVIDLÁ

### 5.1 Constraints

**UNIQUE constraint:**
- `transport_method_code` UNIQUE NOT NULL - každý kód len raz

**Povinné polia:**
- `transport_method_code` NOT NULL
- `transport_method_name` NOT NULL

**Default hodnoty:**
- `is_active` = TRUE
- `created_at` = CURRENT_TIMESTAMP
- `updated_at` = CURRENT_TIMESTAMP

---

## 6. PRÍKLAD DÁT

```sql
-- Základné dopravné metódy
('KUR', 'Kuriér')
('OSO', 'Osobný odber')
('POS', 'Poštou')
('DOP', 'Vlastná doprava')
('ZAS', 'Zásielkovňa')
('EXP', 'Expresná zásielka')
('PAL', 'Paletová preprava')
```

---

## 7. POZNÁMKY PRE MIGRÁCIU

### 7.1 Poradie migrácie

**KRITICKÉ:**
1. ✅ Najprv migrovať **TRPLST.BTR** → transport_methods
2. ✅ Vytvoriť mapping dictionary (TrsCode → transport_method_id)
3. ✅ Potom migrovať **PAB.BTR** → partner_catalog_extensions (použiť mapping)

### 7.2 Transformačné pravidlá

**Generovanie transport_method_id:**
- transport_method_id sa automaticky generuje (SERIAL)
- Pri INSERT nie je potrebné špecifikovať ID
- PostgreSQL pridelí ID automaticky (1, 2, 3...)

**Vytvorenie mapping dictionary:**
Po migrácii TRPLST → transport_methods je potrebné vytvoriť mapu:
```
TrsCode → transport_method_id
"KUR" → 1
"OSO" → 2
"POS" → 3
```

**Použitie mapping pri migrácii PAB.BTR:**
- IcTrsCode (Btrieve) → customer_transport_method_id (PostgreSQL)
- IsTrsCode (Btrieve) → supplier_transport_method_id (PostgreSQL)
- Vyhľadať transport_method_id podľa kódu z dictionary

**_TrsName (vyhľadávacie pole):**
- V Btrieve používané pre case-insensitive vyhľadávanie
- V PostgreSQL nahradené: `WHERE transport_method_name ILIKE '%xyz%'`
- Netreba migrovať

**Sended (sync flag):**
- Zastaralé pole pre synchronizáciu
- Netreba migrovať

**Eliminácia duplikácie:**
- V PAB.BTR sú IcTrsName, IsTrsName (duplikované názvy)
- V PostgreSQL názvy len v transport_methods
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
- Redukcia: 8.6 KB → 4.3 KB (50%)

### v1.0 (2025-12-10)
- Prvotná verzia dokumentu
- Mapping TRPLST.BTR → transport_methods
- Popis číselníka dopravných metód

---

**Koniec dokumentu TRPLST-transport_methods.md**