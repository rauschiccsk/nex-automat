# BARCODE.BTR + GSCAT.BTR → product_catalog_identifiers

**Kategória:** Catalogs - Identifikačné kódy  
**NEX Genesis:** BARCODE.BTR + GSCAT.BTR (polia: BarCode, StkCode, SpcCode, OsdCode)  
**NEX Automat:** `product_catalog_identifiers`  
**Vytvorené:** 2025-12-10  
**Aktualizované:** 2025-12-15  
**Status:** ✅ Pripravené na migráciu

---

## PREHĽAD

### Btrieve súbory

**BARCODE.BTR:**
- **Názov:** BARCODE.BTR
- **Umiestnenie:** `C:\NEX\YEARACT\STORES\BARCODE.BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\STORES\`
- **Účel:** Sekundárne čiarové kódy produktov (viacnásobné EAN kódy)

**GSCAT.BTR (relevantné polia):**
- **Názov:** GSCAT.BTR
- **Umiestnenie:** `C:\NEX\YEARACT\STORES\GSCAT.BTR`
- **Účel:** Primárne identifikátory produktov (BarCode, StkCode, SpcCode, OsdCode)

### Historický vývoj identifikačných kódov

**Fáza 1 - Začiatok:**
- Jeden čiarový kód priamo v GSCAT.BTR (pole `BarCode`)

**Fáza 2 - Viacnásobné čiarové kódy:**
- Nová tabuľka BARCODE.BTR pre ďalšie čiarové kódy
- Prvý zostal v GSCAT.BTR
- Dôvod: Ten istý tovar môže mať rôzne EAN kódy podľa výrobcu/krajiny

**Fáza 3 - "Zneužitie" BARCODE.BTR:**
- Zákazníci začali do BARCODE.BTR dávať aj iné druhy kódov (nie len čiarové)
- Chceli ich vidieť v samostatných stĺpcoch v gride
- Dôvod: Umožnilo to rýchle vyhľadávanie produktu

**Fáza 4 - Riešenie bez JOIN (Btrieve obmedzenia):**
- Do GSCAT.BTR pridané špecializované polia:
  - `StkCode` - skladový kód (interný)
  - `SpcCode` - špecifikačný kód
  - `OsdCode` - kód dodávateľa
- Dôvod: Btrieve nemal JOIN operáciu

**Fáza 5 - Migrácia do NEX Automat (PostgreSQL):**
- ✅ Všetko zlúčiť do `product_catalog_identifiers`
- ✅ Použiť `identifier_type` pre rozlíšenie
- ✅ Podpora neobmedzeného počtu identifikátorov
- ✅ Využiť PostgreSQL indexy pre rýchle vyhľadávanie

---

## MAPPING GSCAT.BTR → product_catalog_identifiers

### Zdroj: GSCAT.BTR - Primárne identifikátory

| NEX Genesis | Typ | NEX Automat | Typ | Identifier Type | is_primary |
|-------------|-----|-------------|-----|-----------------|------------|
| GsCode | longint | product_id | INTEGER | - | - |
| BarCode | Str15 | identifier_code | VARCHAR(50) | 'barcode' | TRUE |
| StkCode | Str15 | identifier_code | VARCHAR(50) | 'stock' | TRUE |
| SpcCode | Str30 | identifier_code | VARCHAR(50) | 'spec' | TRUE |
| OsdCode | Str15 | identifier_code | VARCHAR(50) | 'supplier' | TRUE |
| CrtUser | Str8 | created_by | VARCHAR(30) | - | - |
| CrtDate | DateType | created_at | TIMESTAMP | - | - |
| CrtTime | TimeType | created_at | TIMESTAMP | - | - |
| ModUser | Str8 | updated_by | VARCHAR(30) | - | - |
| ModDate | DateType | updated_at | TIMESTAMP | - | - |
| ModTime | TimeType | updated_at | TIMESTAMP | - | - |

**Poznámky k mappingu:**
- Všetky identifikátory z GSCAT.BTR majú `is_primary = TRUE`
- Ak pole je prázdne (NULL), záznam sa nevkladá
- `CrtUser/CrtDate/CrtTime` = kedy bol produkt vytvorený
- `ModUser/ModDate/ModTime` = kedy bol produkt naposledy modifikovaný
- Ak ModUser neexistuje, použije sa CrtUser

---

## MAPPING BARCODE.BTR → product_catalog_identifiers

### Zdroj: BARCODE.BTR - Sekundárne čiarové kódy

| NEX Genesis | Typ | NEX Automat | Typ | Identifier Type | is_primary |
|-------------|-----|-------------|-----|-----------------|------------|
| GsCode | longint | product_id | INTEGER | - | - |
| BarCode | Str15 | identifier_code | VARCHAR(50) | 'barcode' | FALSE |
| ModUser | Str8 | created_by, updated_by | VARCHAR(30) | - | - |
| ModDate | DateType | created_at, updated_at | TIMESTAMP | - | - |
| ModTime | TimeType | created_at, updated_at | TIMESTAMP | - | - |

**Poznámky k mappingu:**
- Všetky záznamy z BARCODE.BTR majú `identifier_type = 'barcode'` a `is_primary = FALSE`
- ModDate + ModTime sa kombinujú do jedného TIMESTAMP
- Duplicity (product_id + identifier_type + identifier_code) sa ignorujú

---

## BIZNIS LOGIKA

### Typy identifikátorov - Použitie

**barcode (čiarový kód):**
- EAN-13, EAN-8, UPC-A, Code128, QR kód
- Použitie: pokladnice, čítačky čiarových kódov, e-shopy
- Primárny: z GSCAT.BTR (najčastejšie používaný)
- Sekundárne: z BARCODE.BTR (alternatívne kódy)

**stock (skladový kód):**
- Interný identifikátor pre sklady
- Použitie: skladové operácie, inventúra, etikety
- Často kratší než EAN (napr. "SK-12345")

**spec (špecifikačný kód):**
- Technický/katalógový kód
- Použitie: technická dokumentácia, katalógy
- Môže obsahovať verziu/variant (napr. "MT-100-V2")

**supplier (kód dodávateľa):**
- Kód produktu u dodávateľa
- Použitie: objednávky, príjemky
- Každý dodávateľ môže mať vlastný kód pre ten istý produkt

### Primárny vs sekundárny identifikátor

**is_primary = TRUE:**
- Preferovaný identifikátor daného typu
- Zobrazuje sa v gridoch ako hlavný
- Vždy z GSCAT.BTR

**is_primary = FALSE:**
- Alternatívne identifikátory
- Používajú sa pri vyhľadávaní
- Vždy z BARCODE.BTR

**Pravidlo:** Produkt môže mať **max. 1 primárny** identifikátor každého typu, ale **neobmedzený počet sekundárnych**.

### Viacnásobnosť

| Typ | Primárny (GSCAT) | Sekundárne (BARCODE) | Celkom |
|-----|------------------|----------------------|--------|
| barcode | 0-1 | 0-N | 0-N |
| stock | 0-1 | 0 | 0-1 |
| spec | 0-1 | 0 | 0-1 |
| supplier | 0-1 | 0 | 0-1 |

**Vysvetlenie:**
- Len `barcode` môže mať viacero hodnôt (BARCODE.BTR)
- `stock`, `spec`, `supplier` majú max. 1 hodnotu (len z GSCAT.BTR)

---

## VALIDAČNÉ PRAVIDLÁ

### UNIQUE Constraint

**Pravidlo:** Ten istý kód nemôže byť priradený k tomu istému produktu a typu viackrát.

**Constraint:**
```
UNIQUE(product_id, identifier_type, identifier_code)
```

### CHECK Constraint

**Pravidlo:** Len povolené typy identifikátorov.

**Hodnoty identifier_type:**
- `'barcode'` - čiarový kód
- `'stock'` - skladový kód
- `'spec'` - špecifikačný kód
- `'supplier'` - kód dodávateľa

### Foreign Key Constraint

**Pravidlo:** Identifikátor musí patriť existujúcemu produktu.

**Vzťah:** `product_id` → `product_catalog(product_id)`

**Cascading:** Ak zmažem produkt → automaticky sa zmažú všetky jeho identifikátory

### Aplikačné pravidlá

**Audit polia (štandard pre všetky tabuľky):**
- `created_by`, `created_at` - kto a kedy vytvoril záznam (nemenné)
- `updated_by`, `updated_at` - kto a kedy naposledy modifikoval (aktualizuje sa pri každej zmene)

**Pri migrácii z NEX Genesis:**
- `CrtUser/CrtDate/CrtTime` → `created_by/created_at`
- `ModUser/ModDate/ModTime` → `updated_by/updated_at`
- Ak ModUser neexistuje → použiť CrtUser
- Ak nie sú dostupné audit polia → použiť 'MIGRATION' a CURRENT_TIMESTAMP

**Max. 1 primárny identifikátor daného typu:**
- Aplikačná logika alebo database trigger kontroluje túto podmienku

**Prázdne kódy:**
- Nepovoliť prázdne stringy: `TRIM(identifier_code) != ''`

---

## VZŤAHY S INÝMI TABUĽKAMI

### product_catalog → product_catalog_identifiers

**Vzťah:** 1:N (One-to-Many)
- Jeden produkt môže mať viacero identifikátorov
- Identifikátor patrí práve jednému produktu

**Foreign Key:** `product_id` → `product_catalog(product_id)` ON DELETE CASCADE

---

## PRÍKLADY DÁT

### Príklad 1 - Produkt s jedným čiarovým kódom

**GSCAT.BTR:**
```
GsCode: 1001
BarCode: '8588006123456'
StkCode: 'SK-1001'
SpcCode: 'MT-100-V1'
OsdCode: 'SUP-A123'
```

**Výsledok v product_catalog_identifiers:**
```
product_id=1001, type='barcode',  code='8588006123456', is_primary=TRUE
product_id=1001, type='stock',    code='SK-1001',       is_primary=TRUE
product_id=1001, type='spec',     code='MT-100-V1',     is_primary=TRUE
product_id=1001, type='supplier', code='SUP-A123',      is_primary=TRUE
```

### Príklad 2 - Produkt s viacerými čiarovými kódmi

**GSCAT.BTR:**
```
GsCode: 2002
BarCode: '8588006789012'  -- Primárny
StkCode: 'SK-2002'
```

**BARCODE.BTR:**
```
GsCode: 2002, BarCode: '4006381333627'  -- Nemecký EAN
GsCode: 2002, BarCode: '5901234123457'  -- Poľský EAN
```

**Výsledok v product_catalog_identifiers:**
```
product_id=2002, type='barcode', code='8588006789012', is_primary=TRUE   -- GSCAT
product_id=2002, type='barcode', code='4006381333627', is_primary=FALSE  -- BARCODE
product_id=2002, type='barcode', code='5901234123457', is_primary=FALSE  -- BARCODE
product_id=2002, type='stock',   code='SK-2002',       is_primary=TRUE
```

### Príklad 3 - Produkt bez čiarového kódu

**GSCAT.BTR:**
```
GsCode: 3003
BarCode: NULL  -- Žiadny čiarový kód
StkCode: 'SK-3003'
```

**Výsledok v product_catalog_identifiers:**
```
product_id=3003, type='stock', code='SK-3003', is_primary=TRUE
-- Žiadny barcode záznam!
```

---

## MIGRAČNÉ POZNÁMKY

### Poradie migrácie

**Správne poradie:**
1. Najprv GSCAT.BTR (primárne identifikátory)
2. Potom BARCODE.BTR (sekundárne čiarové kódy)
3. Dôvod: UNIQUE constraint zabezpečí že primárne ostanú is_primary=TRUE

### Duplicitné identifikátory

**Problém:** V GSCAT alebo BARCODE môže byť ten istý kód pre rôzne produkty.

**Detekcia:** Pred migráciou skontrolovať duplicitné čiarové kódy a manuálne vyriešiť.

**Riešenie:**
- Preferované: Manuálna kontrola a oprava pred migráciou
- Alternatíva: Povoliť duplicity (odstrániť UNIQUE na identifier_code)
- Alternatíva: Pridať product_id do vyhľadávania (vrátiť všetky matches)

### Whitespace a veľké/malé písmená

**Problém:** Kódy môžu obsahovať medzery alebo mať rôznu veľkosť písmen.

**Riešenie:** Normalizácia pri migrácii - `UPPER(TRIM(code))`

### Testovanie po migrácii

**Kontrola počtu záznamov:**
- Porovnať počet identifikátorov v GSCAT/BARCODE vs NEX Automat
- Overiť že žiadny produkt nemá viacero primárnych identifikátorov rovnakého typu

**Test vyhľadávania:**
- Náhodne vybrať produkty z GSCAT a otestovať vyhľadávanie v NEX Automat
- Overiť že sekundárne čiarové kódy z BARCODE.BTR sú správne priradené

---

**Vytvoril:** Claude & Zoltán  
**Dátum:** 2025-12-10  
**Aktualizované:** 2025-12-15  
**Verzia:** 1.1  
**Status:** ✅ Pripravené na migráciu