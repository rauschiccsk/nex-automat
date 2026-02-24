# PLSnnnnn.BTR → price_list_items

**Kategória:** Sales - Predajné cenníky  
**NEX Genesis:** PLSnnnnn.BTR (kde nnnnn = číslo cenníka)  
**NEX Automat:** `price_list_items`  
**Vytvorené:** 2025-12-15  
**Aktualizované:** 2025-12-15  
**Status:** ✅ Pripravené na migráciu  
**Batch:** Batch 6 (Sales - dokument 1/1 - FINAL)

---

## PREHĽAD

### Btrieve súbor

- **Názov:** PLS[nnnnn].BTR (kde nnnnn = 5-miestne číslo cenníka)
- **Umiestnenie:** `C:\NEX\YEARACT\STORES\PLS[nnnnn].BTR`
  - Premenná časť: `C:\NEX\` (root path)
  - Fixná časť: `\YEARACT\STORES\`
- **Účel:** Položky predajných cenníkov (každý cenník = samostatný súbor)
- **Príklady:** PLS00001.BTR, PLS00002.BTR, PLS00003.BTR

### Historický vývoj cenníkov

**NEX Genesis (Btrieve obmedzenia):**
- Každý cenník = samostatná tabuľka PLSnnnnn.BTR
- Príklady: PLS00001.BTR (maloobchod), PLS00002.BTR (veľkoobchod), PLS00003.BTR (akcie)
- Obsahuje duplikované údaje z GSCAT (kvôli chýbajúcemu JOIN)

**NEX Automat (PostgreSQL):**
- JEDNA tabuľka `price_list_items` pre všetky cenníky
- Rozlíšenie cez `price_list_id`
- Bez duplikácie údajov (použijeme JOIN s product_catalog)

### Účel tabuľky

Položky cenníkov definujú predajné ceny produktov v jednotlivých cenníkoch. Jeden produkt môže mať rôzne ceny v rôznych cenníkoch (maloobchod, veľkoobchod, akcie) a dokonca rôzne ceny na rôznych skladoch.

---

## POSTGRESQL TABUĽKA

**Tabuľka:** `price_list_items`  
**Popis:** Predajné ceny produktov v jednotlivých cenníkoch

**Primárny kľúč:** `id` (SERIAL)  
**Unique constraint:** `(price_list_id, product_id, stock_list_id)`  
**Foreign keys:**
- `product_id` → `product_catalog(product_id)`
- `stock_list_id` → `stock_lists(stock_list_id)`

**Indexy:**
- `idx_price_list_items_list` na `price_list_id`
- `idx_price_list_items_product` na `product_id`
- `idx_price_list_items_stock` na `stock_list_id`
- `idx_price_list_items_promotional` na `is_promotional WHERE TRUE`
- `idx_price_list_items_disabled` na `is_disabled`
- `idx_price_list_items_label` na `requires_label_print WHERE TRUE`

---

## MAPPING POLÍ

### Polia ktoré SA PRENÁŠAJÚ

| NEX Genesis | Typ | NEX Automat | Typ | Popis |
|-------------|-----|-------------|-----|-------|
| nnnnn (názov súboru) | - | price_list_id | INTEGER | Číslo cenníka z PLSnnnnn.BTR |
| GsCode | longint | product_id | INTEGER | Tovarové číslo (PLU) |
| StkNum | word | stock_list_id | INTEGER | Číslo skladu (0 → NULL) |
| Profit | double | profit_margin | DECIMAL(5,2) | Percentuálna sadzba zisku |
| - | - | purchase_price | DECIMAL(12,2) | **NOVÉ!** Nákupná cena (dopočíta sa) |
| APrice | double | price_excl_vat | DECIMAL(12,2) | Predajná cena bez DPH |
| BPrice | double | price_incl_vat | DECIMAL(12,2) | Predajná cena s DPH |
| MinQnt | double | min_quantity | DECIMAL(12,4) | Minimálne predajné množstvo |
| OpenGs | byte | allow_price_override | BOOLEAN | Otvorené PLU (1=možno meniť cenu) |
| Action | Str1 | is_promotional | BOOLEAN | Príznak akcie (A=akciový tovar) |
| ChgItm | Str1 | requires_label_print | BOOLEAN | Príznak zmeny (P=tlačiť etiketu) |
| DisFlag | byte | is_disabled | BOOLEAN | Vyradený (1=vyradený) |
| ModUser | Str8 | created_by, updated_by | VARCHAR(30) | Audit údaje |
| ModDate | DateType | created_at, updated_at | TIMESTAMP | Audit údaje |
| ModTime | TimeType | created_at, updated_at | TIMESTAMP | Audit údaje |

### Polia ktoré SA NEPRENÁŠAJÚ - Duplikácia z GSCAT

Tieto polia sa neprenášajú, pretože ich získame cez JOIN z `product_catalog`:

| NEX Genesis | Dôvod neprenášania |
|-------------|--------------------|
| GsName, _GsName | Z product_catalog.product_name |
| MgCode, FgCode | Z product_catalog_categories |
| BarCode, StkCode, OsdCode | Z product_catalog_identifiers |
| MsName | Z product_catalog.unit_name |
| PackGs | Z product_catalog.package_product_id |
| VatPrc | Z product_catalog.vat_group_id |
| GsType | Z product_catalog.product_type |
| DrbMust, PdnMust | Z product_catalog_extensions |
| GrcMth | Z product_catalog.warranty_months |
| GaName, _GaName | Z product_catalog_texts |

### Polia ktoré SA NEPRENÁŠAJÚ - Zastarané/Nepoužité

| NEX Genesis | Dôvod neprenášania |
|-------------|--------------------|
| UPrice, OvsUser, OvsDate | História cien - riešime cez price_history tabuľku |
| DscPrc1-3, PrfPrc1-3 | Alternatívne ceny D1-D3 - nepoužívame |
| APrice1-3, BPrice1-3 | Alternatívne ceny D1-D3 - nepoužívame |
| OrdPrn | Číslo oddelenia reštaurácie - špecifické |
| CpcSrc | Zdroj nákupnej ceny - nepotrebujeme |
| Sended | Sync flag - zastarané |
| ModNum | Verzia záznamu - PostgreSQL trigger |

---

## BIZNIS LOGIKA

### 1. Číslo cenníka (price_list_id)

**Extrakcia z názvu súboru:**
- Príklad: PLS00001.BTR → price_list_id = 1
- Formát: PLS[5-ciferné číslo].BTR

**Použitie:**
- price_list_id = 1 → "Cenník pre koncových zákazníkov"
- price_list_id = 2 → "Cenník pre veľkoodberateľov"
- price_list_id = 3 → "Akciový cenník"

**Poznámka:** Názvy cenníkov sú v samostatnom číselníku `price_lists` (vytvorí sa neskôr).

### 2. Výpočet cien

**Vzorce:**
```
Nákupná cena → Predajná cena bez DPH:
price_excl_vat = purchase_price * (1 + profit_margin / 100)

Predajná cena bez DPH → Predajná cena s DPH:
price_incl_vat = price_excl_vat * (1 + vat_rate / 100)

Spätný výpočet nákupnej ceny (pri migrácii):
purchase_price = price_excl_vat / (1 + profit_margin / 100)
```

**Príklad:**
- purchase_price = 10.00 €
- profit_margin = 25%
- vat_rate = 20%
- Výsledok: price_excl_vat = 12.50 €, price_incl_vat = 15.00 €

### 3. Minimálne predajné množstvo (min_quantity)

**Použitie:**
- `1.0` → Produkt sa predáva po kusoch
- `6.0` → Minimálny nákup 6 kusov (napr. pivo po sixpackoch)
- `0.5` → Možno kúpiť aj polovicu (napr. meter látky)

**Validácia:** Pri predaji sa kontroluje, či predané množstvo spĺňa minimum.

### 4. Otvorené PLU (allow_price_override)

**Použitie:**
- `TRUE` → Pokladníčka môže zmeniť cenu na pokladni
- `FALSE` → Cena je fixná

**Príklady:**
- Zelenina/ovocie na váhu → TRUE
- Balené potraviny → FALSE
- Služby → TRUE

### 5. Akciový tovar (is_promotional)

**Použitie:**
- Označenie akčných cien
- Filter pre akciový letáK
- Špeciálne zobrazenie v e-shope

### 6. Tlač etikiet (requires_label_print)

**Workflow:**
1. Po zmene ceny sa nastaví `requires_label_print = TRUE`
2. Systém vytlačí nové cenovky
3. Po vytlačení sa nastaví späť na FALSE

### 7. Sklad (stock_list_id)

**Použitie:**
- Produkt môže mať rôzne ceny na rôznych skladoch
- `NULL` → Univerzálna cena pre všetky sklady
- Konkrétne číslo → Cena špecifická pre daný sklad

**Príklad:**
- Produkt 1001 má univerzálnu cenu 15.00 € (stock_list_id = NULL)
- Na sklade 2 má špeciálnu cenu 14.00 € (stock_list_id = 2)

---

## VZŤAHY S INÝMI TABUĽKAMI

### price_list_items → product_catalog

Získanie ceny produktu s jeho základnými údajmi. JOIN cez `product_id` poskytuje názov produktu, merné jednotky, kategórie a ďalšie údaje bez duplikácie dát.

### price_list_items → stock_lists

Spojenie s číselníkom skladov umožňuje definovať rôzne ceny produktu na rôznych skladoch. Ak `stock_list_id IS NULL`, cena platí univerzálne.

### price_list_items → vat_groups (cez product_catalog)

DPH sadzba sa získava cez `product_catalog.vat_group_id`, nie priamo. Pri migrácii sa `VatPrc` z PLS súboru používa len na validáciu.

### price_list_items → price_lists

Prepojenie s číselníkom cenníkov (tabuľka `price_lists` sa vytvorí neskôr) poskytuje názov a popis cenníka.

---

## VALIDAČNÉ PRAVIDLÁ

### 1. Ceny musia byť konzistentné

- Cena s DPH musí byť vyššia alebo rovná cene bez DPH
- Marža musí byť v rozumnom rozsahu (0-1000%)
- Minimálne množstvo musí byť kladné

### 2. Produkt musí existovať

Foreign key constraint na `product_catalog(product_id)` s `ON DELETE RESTRICT` zabezpečuje, že nemožno vymazať produkt, ktorý má ceny v cenníkoch.

### 3. Sklad musí existovať (ak je zadaný)

Foreign key constraint na `stock_lists(stock_list_id)` s `ON DELETE RESTRICT` zabezpečuje integritu skladových dát.

### 4. Unikátnosť

Unique constraint `(price_list_id, product_id, stock_list_id)` zabezpečuje, že v jednom cenníku môže byť produkt len raz pre daný sklad, ale môže mať rôzne ceny na rôznych skladoch.

---

## PRÍKLAD DÁT

```sql
-- Cenník 1: Maloobchod
INSERT INTO price_list_items (price_list_id, product_id, stock_list_id, purchase_price, profit_margin, price_excl_vat, price_incl_vat, min_quantity) VALUES
(1, 1001, NULL, 10.00, 25.00, 12.50, 15.00, 1.0),
(1, 1002, NULL, 5.00, 30.00, 6.50, 7.80, 1.0),
(1, 1003, NULL, 8.00, 40.00, 11.20, 13.44, 6.0);

-- Cenník 2: Veľkoobchod
INSERT INTO price_list_items (price_list_id, product_id, stock_list_id, purchase_price, profit_margin, price_excl_vat, price_incl_vat, min_quantity) VALUES
(2, 1001, NULL, 10.00, 15.00, 11.50, 13.80, 10.0),
(2, 1002, NULL, 5.00, 20.00, 6.00, 7.20, 20.0);

-- Akciový tovar
INSERT INTO price_list_items (price_list_id, product_id, stock_list_id, purchase_price, profit_margin, price_excl_vat, price_incl_vat, is_promotional, min_quantity) VALUES
(1, 1004, NULL, 12.00, 10.00, 13.20, 15.84, TRUE, 1.0);

-- Produkt s rôznou cenou na rôznych skladoch
INSERT INTO price_list_items (price_list_id, product_id, stock_list_id, purchase_price, profit_margin, price_excl_vat, price_incl_vat, min_quantity) VALUES
(1, 1005, NULL, 20.00, 25.00, 25.00, 30.00, 1.0),  -- univerzálna cena
(1, 1005, 2, 20.00, 20.00, 24.00, 28.80, 1.0);     -- špeciálna cena na sklade 2
```

---

## MIGRAČNÉ POZNÁMKY

### 1. Multi-file architektúra

Každý cenník je v samostatnom Btrieve súbore:
- PLS00001.BTR → price_list_id = 1
- PLS00002.BTR → price_list_id = 2
- PLS00003.BTR → price_list_id = 3

Pri migrácii sa extrahuje číslo cenníka z názvu súboru a všetky dáta sa uložia do jednej tabuľky `price_list_items` s rozlíšením cez `price_list_id`.

### 2. Dopočítanie purchase_price

Pole `purchase_price` je nové v PostgreSQL verzii. Pri migrácii sa dopočíta spätne zo zisku:
```
purchase_price = price_excl_vat / (1 + profit_margin / 100)
```

Ak `profit_margin = 0` alebo `price_excl_vat = 0`, `purchase_price` ostane `NULL`.

### 3. VatPrc vs vat_group_id

Pri migrácii:
- `VatPrc` z PLSnnnnn.BTR slúži len na validáciu
- Skutočný `vat_group_id` sa berie z `product_catalog`
- Ak sa líši → warning, ale použije sa z `product_catalog`

### 4. Konverzia príznakov

- `OpenGs`: 1 → TRUE, 0 → FALSE
- `Action`: 'A' → TRUE, inak FALSE
- `ChgItm`: 'P' → TRUE, inak FALSE
- `DisFlag`: 1 → TRUE, 0 → FALSE

### 5. Minimálne množstvo

- `MinQnt = 0` sa konvertuje na `1.0`
- `MinQnt > 0` sa prenáša bez zmeny

### 6. Sklad

- `StkNum = 0` sa konvertuje na `NULL` (univerzálna cena)
- `StkNum > 0` sa prenáša ako `stock_list_id`

---

## POZNÁMKY PRE MIGRÁCIU

### Poradie migrácie

1. **Najprv:** `product_catalog`, `stock_lists`, `vat_groups`
2. **Potom:** `price_lists` (číselník cenníkov)
3. **Nakoniec:** `price_list_items` (položky cenníkov)

### Validácia po migrácii

Po migrácii overiť:
1. Počet záznamov vo všetkých PLS súboroch vs. price_list_items
2. Konzistencia DPH sadzieb (VatPrc vs. product_catalog.vat_group_id)
3. Správnosť prepočítaných nákupných cien
4. Neexistujúce produkty (GsCode not in product_catalog)

### Závislosti

- Vyžaduje existujúcu tabuľku `product_catalog`
- Vyžaduje existujúcu tabuľku `stock_lists`
- Vyžaduje vytvorenú tabuľku `price_lists` (číselník cenníkov)

---

## SÚVISIACE DOKUMENTY

- **product_catalog** → `docs/architecture/database/catalogs/products/tables/GSCAT-product_catalog.md`
- **product_catalog_identifiers** → `docs/architecture/database/catalogs/products/tables/BARCODE-product_catalog_identifiers.md`
- **stock_lists** → `docs/architecture/database/stock/cards/tables/STKLST-stocks.md`
- **price_lists** → ⏳ Todo (číselník cenníkov)
- **price_history** → ⏳ Todo (história zmien cien)

---

**Vytvoril:** Claude & Zoltán  
**Dátum:** 2025-12-15  
**Verzia:** 1.1  
**Status:** ✅ Pripravené na migráciu