# GSCAT.BTR → product_catalog

**Kategória:** Catalogs  
**NEX Genesis:** GSCAT.BTR (Goods Catalog)  
**NEX Automat:** `product_catalog`, `product_catalog_extensions`, `product_catalog_identifiers`, `product_catalog_categories`, `product_catalog_texts`, `vat_groups`  
**Vytvorené:** 2025-12-10  
**Aktualizované:** 2025-12-15  
**Status:** ✅ Pripravené na migráciu

---

## PREHĽAD

### Btrieve súbor

**GSCAT.BTR:**
- **Názov:** GSCAT.BTR
- **Umiestnenie:** `C:\NEX\YEARACT\STORES\GSCAT.BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\STORES\`
- **Účel:** Hlavný katalóg produktov (tovar, materiál, služba)

**Migrácia do 6 tabuliek:**
1. `product_catalog` - základné údaje
2. `product_catalog_extensions` - rozšírené údaje
3. `product_catalog_identifiers` - identifikačné kódy (+ BARCODE.BTR)
4. `product_catalog_categories` - kategorizácia (+ MGLST, FGLST, SGLST)
5. `vat_groups` - skupiny DPH
6. `product_catalog_texts` - textové informácie

---

## 1. PRODUCT_CATALOG - Základný katalóg

**Tabuľka:** `product_catalog`  
**Popis:** Základné údaje o produkte (tovar, materiál, služba)

| NEX Genesis | Typ | NEX Automat | Typ | Popis | Index |
|-------------|-----|-------------|-----|-------|-------|
| GsCode | longint | product_id | INTEGER | Numerický identifikátor produktu (PLU) | PK |
| GsName | Str30 | product_name | VARCHAR(100) | Názov produktu | ✓ |
| ProTyp | Str1 | business_type | VARCHAR(1) | M=materiál, T=tovar, S=služba | ✓ |
| GsType | Str1 | product_type | VARCHAR(1) | T=riadny, W=váhový, O=obal | ✓ |
| MsName | Str10 | unit_name | VARCHAR(20) | Názov mernej jednotky (ks, kg, l) | - |
| MsuName | Str5 | base_unit | VARCHAR(10) | Základná jednotka (kg, m, l, m2, m3) | - |
| MsuQnt | double | base_unit_quantity | DECIMAL(12,4) | Množstvo v základnej jednotke | - |
| PackGs | longint | package_product_id | INTEGER | Tovarové číslo pripojeného obalu | FK |
| GrcMth | word | warranty_months | SMALLINT | Záručná doba (počet mesiacov) | - |
| DivSet | byte | divisibility | SMALLINT | 0=deliteľný, 1=nedeliteľný, 2=1/2... | - |
| DisFlag | byte | is_disabled | BOOLEAN | Vyradený z evidencie (1=vyradený) | ✓ |
| CrtUser | Str8 | created_by | VARCHAR(30) | Užívateľ ktorý vytvoril záznam | - |
| CrtDate | DateType | created_at | TIMESTAMP | Dátum a čas vytvorenia | - |
| CrtTime | TimeType | created_at | TIMESTAMP | Zahrnuté v created_at | - |
| ModUser | Str8 | updated_by | VARCHAR(30) | Kto naposledy modifikoval | - |
| ModDate | DateType | updated_at | TIMESTAMP | Kedy naposledy modifikované | - |
| ModTime | TimeType | updated_at | TIMESTAMP | Zahrnuté v updated_at | - |

**Poznámky k mappingu:**
- MgCode (tovarová skupina) sa mapuje cez `product_catalog_categories`, nie priamo v product_catalog
- VatPrc sa mapuje cez `vat_groups` tabuľku
- package_product_id → self-referencing FK na product_catalog

**Foreign Keys:**
- `package_product_id` → `product_catalog(product_id)` ON DELETE SET NULL
- `vat_group_id` → `vat_groups(vat_group_id)` ON DELETE RESTRICT

---

## 2. PRODUCT_CATALOG_EXTENSIONS - Rozšírenie katalógu

**Tabuľka:** `product_catalog_extensions`  
**Popis:** Dodatočné údaje, ktoré nie každý zákazník používa (1:1 väzba)

| NEX Genesis | Typ | NEX Automat | Typ | Popis |
|-------------|-----|-------------|-----|-------|
| GsCode | longint | product_id | INTEGER | Väzba na products (PK, FK) |
| Volume | double | volume_m3 | DECIMAL(12,4) | Objem (množstvo MJ na 1 m3) |
| Weight | double | weight_kg | DECIMAL(12,4) | Váha jednej MJ |
| SpirGs | byte | is_alcoholic | BOOLEAN | Liehový výrobok (1=áno) |
| DrbMust | byte | track_expiry | BOOLEAN | Povinné zadávanie trvanlivosti |
| DrbDay | word | expiry_days | SMALLINT | Počet dní trvanlivosti |
| PdnMust | byte | track_serial | BOOLEAN | Sledovanie výrobných čísiel |
| RbaTrc | byte | track_batch | BOOLEAN | Sledovanie výrobnej šarže |
| SecNum | byte | scale_section | SMALLINT | Číslo váhovej sekcie |
| WgCode | word | scale_plu | SMALLINT | Váhové PLU číslo |
| ShpNum | byte | eshop_id | SMALLINT | Číslo e-shopu |
| SndShp | byte | synced_to_eshop | BOOLEAN | Uložené do e-shopu |
| LinPrice | double | last_purchase_price | DECIMAL(12,2) | Posledná nákupná cena |
| LinDate | DateType | last_receipt_date | DATE | Dátum posledného príjmu |
| LinStk | word | last_receipt_stock | SMALLINT | Číslo skladu príjmu |
| LinPac | longint | last_supplier_id | INTEGER | Kód posledného dodávateľa |
| GscKfc | word | carton_quantity | SMALLINT | Počet kusov v kartóne |
| GspKfc | word | pallet_cartons | SMALLINT | Počet kartónov v palete |
| QliKfc | double | carton_weight | DECIMAL(10,4) | Hmotnosť kartónu |

**Poznámky k mappingu:**
- Extensions tabuľka nemá audit polia (created_by, updated_by) - audit je na hlavnej tabuľke product_catalog
- 1:1 väzba s product_catalog

**Foreign Key:**
- `product_id` → `product_catalog(product_id)` ON DELETE CASCADE

---

## 3. PRODUCT_CATALOG_IDENTIFIERS - Identifikačné kódy

**Tabuľka:** `product_catalog_identifiers`  
**Popis:** Všetky identifikačné kódy produktu (EAN, skladový, špecifikačný, dodávateľský) + obsah BARCODE.BTR

| NEX Genesis | Typ | NEX Automat | Typ | Identifier Type |
|-------------|-----|-------------|-----|-----------------|
| BarCode | Str15 | identifier_code | VARCHAR(50) | 'barcode' |
| StkCode | Str15 | identifier_code | VARCHAR(50) | 'stock' |
| SpcCode | Str30 | identifier_code | VARCHAR(50) | 'spec' |
| OsdCode | Str15 | identifier_code | VARCHAR(50) | 'supplier' |

**Štruktúra:**
- `product_id` - numerický identifikátor produktu
- `identifier_type` - typ kódu ('barcode', 'stock', 'spec', 'supplier')
- `identifier_code` - samotný identifikačný kód
- `is_primary` - primárny identifikátor daného typu (TRUE pre GSCAT, FALSE pre BARCODE.BTR)
- `created_by`, `created_at`, `updated_by`, `updated_at` - audit polia

**Hodnoty identifier_type:**
- `barcode` = čiarový kód (EAN-13, EAN-8, UPC-A, Code128...)
- `stock` = skladový kód (interný identifikátor)
- `spec` = špecifikačný kód (technický/katalógový kód)
- `supplier` = kód dodávateľa (objednávací kód u dodávateľa)

**Foreign Key:**
- `product_id` → `product_catalog(product_id)` ON DELETE CASCADE

**UNIQUE Constraint:**
- (product_id, identifier_type, identifier_code)

**Poznámka:** Do tejto tabuľky bude presunutý aj obsah `BARCODE.BTR` - sekundárne čiarové kódy produktu. Viac info v `BARCODE-product_catalog_identifiers.md`.

---

## 4. PRODUCT_CATALOG_CATEGORIES - Kategorizácia

**Tabuľka:** Mapovacia tabuľka medzi produktmi a kategóriami

| NEX Genesis | NEX Automat | Category Type | Číselník |
|-------------|-------------|---------------|----------|
| MgCode | category_id | 'product' | product_categories |
| FgCode | category_id | 'financial' | product_categories |
| SgCode | category_id | 'specific' | product_categories |

**Štruktúra product_catalog_categories:**
- `product_id` - numerický identifikátor produktu
- `category_type` - typ kategórie ('product', 'financial', 'specific')
- `category_id` - numerický identifikátor skupiny (kategórie)

**Hodnoty category_type:**
- `product` = tovarová skupina (MgCode) → MGLST.BTR
- `financial` = finančná skupina (FgCode) → FGLST.BTR
- `specific` = špecifická skupina (SgCode) → SGLST.BTR

**Foreign Keys:**
- `product_id` → `product_catalog(product_id)` ON DELETE CASCADE
- `category_id` → `product_categories(category_id)` ON DELETE RESTRICT

**UNIQUE Constraint:**
- (product_id, category_type)

**Potrebné číselníky:**
- `product_categories` - univerzálny číselník všetkých typov kategórií

**Poznámka pre výrobcov a dodávateľov:**
- PrdPac (výrobca) a SupPac (dodávateľ) sa mapujú cez samostatnú tabuľku `product_catalog_partners` → `partner_catalog`

---

## 5. VAT_GROUPS - Skupiny DPH

**Tabuľka:** `vat_groups`  
**Popis:** Percentuálne sadzby DPH s históriou platnosti

| NEX Genesis | Typ | NEX Automat | Typ | Popis |
|-------------|-----|-------------|-----|-------|
| VatPrc | byte | vat_rate | DECIMAL(5,2) | Percentuálna sadzba DPH |
| - | - | vat_name | VARCHAR(50) | Názov sadzby |
| - | - | is_active | BOOLEAN | Aktívna/archivovaná sadzba |
| - | - | valid_from | DATE | Platnosť od |
| - | - | valid_to | DATE | Platnosť do |

**Príklad dát:**
```
vat_group_id=1, vat_rate=20.00, vat_name='Základná sadzba 20%', is_active=TRUE, valid_from='2023-01-01'
vat_group_id=2, vat_rate=10.00, vat_name='Znížená sadzba 10%', is_active=TRUE, valid_from='2023-01-01'
vat_group_id=3, vat_rate=0.00, vat_name='Oslobodené od DPH', is_active=TRUE, valid_from='2023-01-01'
vat_group_id=4, vat_rate=19.00, vat_name='Základná sadzba 19% (archív)', is_active=FALSE, valid_from='2020-01-01', valid_to='2022-12-31'
```

**UNIQUE Constraint:**
- (vat_rate, valid_from)

---

## 6. PRODUCT_CATALOG_TEXTS - Textové informácie

**Tabuľka:** `product_catalog_texts`  
**Popis:** Rôzne typy textových informácií (dlhé názvy, poznámky...)

| NEX Genesis | Typ | NEX Automat | Typ | Text Type |
|-------------|-----|-------------|-----|-----------|
| GaName | Str60 | text | TEXT | 'extended_name' |
| Notice | Str240 | text | TEXT | 'notes' |

**Štruktúra:**
- `product_id` - numerický identifikátor produktu
- `text_type` - typ textu ('extended_name', 'notes', 'description', ...)
- `text` - samotný text
- `language` - jazyk (pre budúcu lokalizáciu)
- `created_by`, `created_at`, `updated_by`, `updated_at` - audit polia

**Hodnoty text_type:**
- `extended_name` = doplnkový názov pre tlač (GaName)
- `notes` = poznámkový riadok (Notice)
- `description` = dlhý popis pre e-shop
- `short_description` = krátky popis
- `technical_specs` = technické parametre

**Foreign Key:**
- `product_id` → `product_catalog(product_id)` ON DELETE CASCADE

**UNIQUE Constraint:**
- (product_id, text_type, language)

---

## POLIA KTORÉ SA NEPRENÁŠAJÚ

| NEX Genesis | Typ | Dôvod neprenášania |
|-------------|-----|--------------------|
| _GsName | Str15 | Vyhľadávacie pole - PostgreSQL full-text search |
| _GaName | Str60 | Vyhľadávacie pole - PostgreSQL full-text search |
| MinOsq | double | Nepoužité |
| BasGsc | longint | Nepoužité (väzba na základný tovar) |
| CctCod | Str10 | Nepoužité (colný kód) |
| Reserve | Str4 | Rezervované pole |
| SbcCnt | word | Počet kódov - PostgreSQL COUNT() |
| Sended | byte | Zastarané (sync flag) |
| ModNum | word | PostgreSQL má verziu cez trigger |
| IsiSnt | Str3 | Účtovné prerozúčtovanie - zastarané |
| IsiAnl | Str6 | Účtovné prerozúčtovanie - zastarané |
| IciSnt | Str3 | Účtovné prerozúčtovanie - zastarané |
| IciAnl | Str6 | Účtovné prerozúčtovanie - zastarané |
| PlsNum1-5 | word | Cenníky - nové riešenie cez tabuľku |
| NewVatPrc | Str2 | Pripravená sadzba - vat_groups.valid_from |

---

## BIZNIS LOGIKA

### business_type (ProTyp) vs product_type (GsType)

**business_type** (M/T/S) = ČO to je z hľadiska účtovníctva a účelu:
- M = Materiál (vstupy do výroby)
- T = Tovar (nákup-predaj bez zmeny)
- S = Služba (nehmotný produkt)

**product_type** (T/W/O) = AKO sa to predáva/obsluhuje:
- T = Riadny tovar (kusový predaj)
- W = Váhový tovar (predaj na váhu)
- O = Obal (vratné obaly)

### Trvanlivosť

- **track_expiry (DrbMust)** = Sledovať trvanlivosť áno/nie
- **expiry_days (DrbDay)** = Počet dní do expirácie
- **warranty_months (GrcMth)** = Záručná doba v mesiacoch (garancie)

### Výrobné čísla vs šarže

- **track_serial (PdnMust)** = Výrobné/sériové číslo (unique per kus)
- **track_batch (RbaTrc)** = Výrobná šarža (batch, viac kusov)

### Váhové položky

- **scale_section (SecNum)** = Sekcia na elektronickej váhe
- **scale_plu (WgCode)** = PLU číslo na váhe (pre integráciu)

### Deliteľnosť (DivSet)

- 0 = Deliteľný (možno predať 0.5 ks)
- 1 = Nedeliteľný (len celé kusy)
- 2, 3, 4... = Deliteľný na 1/2, 1/3, 1/4... (pre ovocie, zeleninu)

---

## VALIDAČNÉ PRAVIDLÁ

### CHECK Constraints

**business_type:**
- Povolené hodnoty: 'M', 'T', 'S'

**product_type:**
- Povolené hodnoty: 'T', 'W', 'O'

### Foreign Keys

- `package_product_id` → `product_catalog(product_id)` ON DELETE SET NULL
- `vat_group_id` → `vat_groups(vat_group_id)` ON DELETE RESTRICT

### Audit polia (štandard pre všetky tabuľky)

- `created_by`, `created_at` - kto a kedy vytvoril záznam (nemenné)
- `updated_by`, `updated_at` - kto a kedy naposledy modifikoval (aktualizuje sa pri každej zmene)

**Pri migrácii z NEX Genesis:**
- `CrtUser/CrtDate/CrtTime` → `created_by/created_at`
- `ModUser/ModDate/ModTime` → `updated_by/updated_at`
- Ak ModUser neexistuje → použiť CrtUser
- Ak nie sú dostupné audit polia → použiť 'MIGRATION' a CURRENT_TIMESTAMP

---

## MIGRAČNÉ POZNÁMKY

### 1. Duplicitné identifikátory

V GSCAT môže byť jeden BarCode pre viac produktov. V `product_catalog_identifiers` je UNIQUE constraint. Pred migráciou skontrolovať duplicity a manuálne vyriešiť.

### 2. Merné jednotky

MsName a MsuName sú text - potrebujeme číselník `units` pre normalizáciu merných jednotiek.

### 3. Kategórie

Všetky skupiny (MgCode, FgCode, SgCode) potrebujú migráciu do `product_categories` pred migráciou produktov.

### 4. Poradie migrácie

1. Číselníky (vat_groups, product_categories, units)
2. Partneri (partner_catalog)
3. Produkty (product_catalog)
4. Rozšírenia (product_catalog_extensions)
5. Identifikátory (product_catalog_identifiers + BARCODE.BTR)
6. Kategorizácia (product_catalog_categories)
7. Texty (product_catalog_texts)

### 5. Testovanie po migrácii

- Overiť počet záznamov: GSCAT.BTR vs product_catalog
- Skontrolovať foreign keys (package_product_id, vat_group_id)
- Overiť že audit polia sú správne naplnené
- Testovať vyhľadávanie produktov podľa identifikátorov

---

## DOKUMENTY SÚVISIACICH TABULIEK

- **product_catalog_identifiers** → `BARCODE-product_catalog_identifiers.md` (detailný mapping BARCODE.BTR)
- **product_categories** - Všetky typy kategórií:
  - `MGLST-product_categories.md` (tovarové skupiny)
  - `FGLST-product_categories.md` (finančné skupiny)
  - `SGLST-product_categories.md` (špecifické skupiny)
- **partner_catalog** - Partneri/Dodávatelia/Výrobcovia → `PAB-partner_catalog.md`
- **DATABASE_RELATIONSHIPS** → `DATABASE_RELATIONSHIPS.md`

---

**Vytvoril:** Claude & Zoltán  
**Dátum:** 2025-12-10  
**Aktualizované:** 2025-12-15  
**Verzia:** 1.2  
**Status:** ✅ Pripravené na migráciu
**Status:** ✅ Pripravené na migráciu