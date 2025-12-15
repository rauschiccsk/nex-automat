# Database Relationships

**Category:** Database  
**Status:** 🟢 Complete  
**Created:** 2024-12-10  
**Updated:** 2025-12-15  
**Related:** [DATABASE_PRINCIPLES.md](DATABASE_PRINCIPLES.md)

---

## Overview

Cross-system database relationships, foreign key constraints, cascading rules, and business logic.

---

## PREHĽAD KATEGÓRIÍ

| Kategória | Folder | Počet tabuliek | Popis |
|-----------|--------|----------------|-------|
| 📁 System | `system/` | ~5 | Konfigurácia, užívatelia, práva |
| 📊 Catalogs | `catalogs/` | ~12 | Číselníky (produkty, partneri, skupiny) |
| 📦 Stock | `stock/` | ~8 | Skladové hospodárstvo, pohyby, doklady |
| 💰 Accounting | `accounting/` | ~15 | Účtovníctvo, účty, doklady |

---

## 1. CATALOGS - Interné vzťahy

### 1.1 Products → Číselníky

**Hlavné entity:**
```
product_catalog (hlavná tabuľka)
├── product_catalog_extensions (1:1)
├── product_catalog_identifiers (1:N)
├── product_catalog_categories (1:N) → product_categories
├── product_catalog_texts (1:N)
└── vat_groups (N:1)
```

**SQL Relationships:**
```sql
-- product_catalog → product_catalog_extensions (1:1)
ALTER TABLE product_catalog_extensions 
    ADD FOREIGN KEY (product_id) REFERENCES product_catalog(product_id) ON DELETE CASCADE;

-- product_catalog → product_catalog_identifiers (1:N)
ALTER TABLE product_catalog_identifiers 
    ADD FOREIGN KEY (product_id) REFERENCES product_catalog(product_id) ON DELETE CASCADE;

-- product_catalog → product_catalog_categories (1:N)
ALTER TABLE product_catalog_categories 
    ADD FOREIGN KEY (product_id) REFERENCES product_catalog(product_id) ON DELETE CASCADE;
ALTER TABLE product_catalog_categories
    ADD FOREIGN KEY (category_id) REFERENCES product_categories(category_id) ON DELETE RESTRICT;

-- product_catalog → product_catalog_texts (1:N)
ALTER TABLE product_catalog_texts 
    ADD FOREIGN KEY (product_id) REFERENCES product_catalog(product_id) ON DELETE CASCADE;

-- product_catalog → vat_groups (N:1)
ALTER TABLE product_catalog 
    ADD FOREIGN KEY (vat_group_id) REFERENCES vat_groups(vat_group_id) ON DELETE RESTRICT;
```

**Cascading Rules:**
- ✅ `ON DELETE CASCADE` - ak zmažem produkt, zmažú sa extensions, identifiers, categories, texts
- ✅ `ON DELETE RESTRICT` - ak zmažem VAT group, NESMIE sa zmazať ak existujú produkty s ňou

---

### 1.2 Product Categories - Univerzálny číselník skupín

**Vzťah:**
```
product_catalog_categories.category_id → product_categories.category_id
```

**Číselník obsahuje 3 typy kategórií:**
- `category_type = 'product'` - Tovarové skupiny (MGLST.BTR)
- `category_type = 'financial'` - Finančné skupiny (FGLST.BTR)
- `category_type = 'specific'` - Špecifické skupiny (SGLST.BTR)

**SQL:**
```sql
CREATE TABLE product_categories (
    category_id SERIAL PRIMARY KEY,
    category_type VARCHAR(20) NOT NULL CHECK (category_type IN ('product', 'financial', 'specific')),
    category_code VARCHAR(20) UNIQUE NOT NULL,
    category_name VARCHAR(100) NOT NULL,
    parent_category_id INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (parent_category_id) REFERENCES product_categories(category_id)
);

CREATE TABLE product_catalog_categories (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    category_type VARCHAR(20) NOT NULL,
    category_id INTEGER NOT NULL,
    
    FOREIGN KEY (product_id) REFERENCES product_catalog(product_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES product_categories(category_id) ON DELETE RESTRICT,
    UNIQUE(product_id, category_type)
);
```

**Biznis pravidlo:** 
- Hierarchická štruktúra - kategória môže mať nadradenú kategóriu (parent_category_id)
- Produkt môže mať max. 1 kategóriu každého typu
- Pri zmazaní produktu sa zmažú mapovanie (CASCADE)
- Pri zmazaní kategórie sa nesmie zmazať ak existujú produkty (RESTRICT)

---

### 1.3 Product Categories → Partners (výrobcovia, dodávatelia)

**Mapovanie pre výrobcov a dodávateľov:**

| category_type | category_id → | Tabuľka | Popis |
|---------------|---------------|---------|-------|
| 'manufacturer' | partner_id | partner_catalog | Výrobca produktu |
| 'supplier' | partner_id | partner_catalog | Dodávateľ produktu |

**Poznámka:** Výrobcovia a dodávatelia NIE SÚ v product_categories, ale v partner_catalog.

**SQL:**
```sql
-- Samostatná mapovacia tabuľka pre partnerov
CREATE TABLE product_catalog_partners (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    partner_type VARCHAR(20) NOT NULL CHECK (partner_type IN ('manufacturer', 'supplier')),
    partner_id INTEGER NOT NULL,
    
    FOREIGN KEY (product_id) REFERENCES product_catalog(product_id) ON DELETE CASCADE,
    FOREIGN KEY (partner_id) REFERENCES partner_catalog(partner_id) ON DELETE RESTRICT,
    UNIQUE(product_id, partner_type)
);
```

**Biznis pravidlo:** Produkt môže mať max. 1 výrobcu a max. 1 dodávateľa.

---

### 1.4 Products → Self-reference (Obaly)

**Vzťah:**
```
product_catalog.package_product_id → product_catalog.product_id
```

**SQL:**
```sql
ALTER TABLE product_catalog 
    ADD FOREIGN KEY (package_product_id) REFERENCES product_catalog(product_id) ON DELETE SET NULL;
```

**Biznis pravidlo:** Ak produkt má pripojený obal, `package_product_id` odkazuje na iný produkt kde `product_type = 'O'`

---

## 2. CATALOGS ↔ STOCK - Cross-system vzťahy

### 2.1 Products → Stock Cards

**Vzťah:**
```
stock_cards.product_id → product_catalog.product_id
```

**SQL:**
```sql
CREATE TABLE stock_cards (
    card_id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    warehouse_id INTEGER NOT NULL,
    quantity_on_hand DECIMAL(12,4) DEFAULT 0,
    quantity_reserved DECIMAL(12,4) DEFAULT 0,
    last_movement_date DATE,
    
    FOREIGN KEY (product_id) REFERENCES product_catalog(product_id) ON DELETE RESTRICT,
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id) ON DELETE RESTRICT,
    UNIQUE(product_id, warehouse_id)
);
```

**Cascading:** `ON DELETE RESTRICT` - nesmie sa zmazať produkt ak existuje skladová karta

---

### 2.2 Product Extensions → Stock Info

**Spätný vzťah (denormalizácia):**
```
product_catalog_extensions.last_receipt_date
product_catalog_extensions.last_receipt_stock → warehouses.warehouse_id
product_catalog_extensions.last_supplier_id → partner_catalog.partner_id
```

**Poznámka:** Tieto polia sú **denormalizované** pre rýchly prístup. Majú byť syncované s `stock_movements`.

---

### 2.3 Partners → Stock Documents

**Vzťah:**
```
receipt_documents.supplier_id → partner_catalog.partner_id
issue_documents.customer_id → partner_catalog.partner_id
```

**SQL:**
```sql
CREATE TABLE receipt_documents (
    document_id SERIAL PRIMARY KEY,
    document_number VARCHAR(50) NOT NULL,
    document_date DATE NOT NULL,
    supplier_id INTEGER NOT NULL,
    warehouse_id INTEGER NOT NULL,
    
    -- Denormalizované dáta dodávateľa (snapshot)
    supplier_name VARCHAR(200) NOT NULL,
    supplier_address TEXT,
    supplier_ico VARCHAR(20),
    
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id) ON DELETE RESTRICT
    -- supplier_id BEZ FK CONSTRAINT! (archívny dokument)
);

CREATE TABLE issue_documents (
    document_id SERIAL PRIMARY KEY,
    document_number VARCHAR(50) NOT NULL,
    document_date DATE NOT NULL,
    customer_id INTEGER NOT NULL,
    warehouse_id INTEGER NOT NULL,
    
    -- Denormalizované dáta zákazníka (snapshot)
    customer_name VARCHAR(200) NOT NULL,
    customer_address TEXT,
    customer_ico VARCHAR(20),
    
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id) ON DELETE RESTRICT
    -- customer_id BEZ FK CONSTRAINT! (archívny dokument)
);
```

**KRITICKÉ:** Dokumenty (príjemky, výdajky) sú **archívne** - všetky údaje sú uložené priamo v dokumente (denormalizácia). Nemajú FK constraints na partners, pretože partner môže byť zmazaný, ale dokument musí ostať nemenný!

---

## 3. CATALOGS ↔ ACCOUNTING - Cross-system vzťahy

### 3.1 VAT Groups → Chart of Accounts

**Vzťah:**
```
vat_groups.vat_rate → používa sa v účtovníctve
product_catalog.vat_group_id → určuje DPH pri predaji/nákupe
```

**SQL:**
```sql
CREATE TABLE chart_of_accounts (
    account_id SERIAL PRIMARY KEY,
    account_number VARCHAR(10) UNIQUE NOT NULL,
    account_name VARCHAR(200) NOT NULL,
    account_type VARCHAR(20) NOT NULL,  -- 'asset', 'liability', 'income', 'expense'
    vat_applicable BOOLEAN DEFAULT FALSE
);
```

---

### 3.2 Financial Groups → Chart of Accounts

**Vzťah:**
```
product_categories (WHERE category_type='financial') → chart_of_accounts
```

**Biznis pravidlo:** Finančná skupina produktu určuje na ktorý účet sa zaúčtuje predaj/nákup

---

### 3.3 Partners → Accounting (ARCHÍVNE DOKUMENTY!)

**KRITICKÉ: Faktúry sú archívne dokumenty bez FK constraints!**

**Vzťah:**
```
invoices.partner_id → partner_catalog.partner_id (BEZ FK CONSTRAINT!)
invoice_items.product_id → product_catalog.product_id (BEZ FK CONSTRAINT!)
```

**SQL:**
```sql
CREATE TABLE invoices (
    invoice_id SERIAL PRIMARY KEY,
    invoice_number VARCHAR(50) NOT NULL,
    invoice_date DATE NOT NULL,
    invoice_type VARCHAR(20) NOT NULL,  -- 'issued', 'received'
    
    -- Referencia (môže byť NULL ak partner bol zmazaný)
    partner_id INTEGER,  -- BEZ FK CONSTRAINT!
    
    -- Denormalizované dáta partnera (snapshot v čase vystavenia)
    partner_code VARCHAR(20) NOT NULL,
    partner_name VARCHAR(200) NOT NULL,
    partner_address TEXT,
    partner_ico VARCHAR(20),
    partner_dic VARCHAR(20),
    partner_ic_dph VARCHAR(20),
    
    total_amount DECIMAL(12,2),
    vat_amount DECIMAL(12,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE invoice_items (
    item_id SERIAL PRIMARY KEY,
    invoice_id INTEGER NOT NULL,
    
    -- Referencia (môže byť NULL ak produkt bol zmazaný)
    product_id INTEGER,  -- BEZ FK CONSTRAINT!
    
    -- Denormalizované dáta produktu (snapshot v čase vystavenia)
    product_code VARCHAR(20) NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    quantity DECIMAL(12,4) NOT NULL,
    unit_name VARCHAR(20) NOT NULL,
    unit_price DECIMAL(12,2) NOT NULL,
    vat_rate DECIMAL(5,2) NOT NULL,
    line_total DECIMAL(12,2) NOT NULL,
    
    FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id) ON DELETE RESTRICT
);
```

**Dôvod:**
- ✅ **Nemennosť** - faktúra zostane rovnaká aj po rokoch
- ✅ **Právna istota** - splnenie účtovných predpisov SR
- ✅ **Audit trail** - vidíš presne čo tam bolo v čase vystavenia
- ✅ **Flexibilita** - môžeš zmazať produkt/partnera bez obavy
- ✅ **Performance** - žiadne JOINy pri tlači faktúry

**Zákon:** Podľa slovenských účtovných predpisov nemožno meniť údaje na účtovných dokladoch spätne!

---

## 4. STOCK - Interné vzťahy

### 4.1 Stock Cards → Stock Movements

**Vzťah:**
```
stock_movements.card_id → stock_cards.card_id
```

**SQL:**
```sql
CREATE TABLE stock_movements (
    movement_id SERIAL PRIMARY KEY,
    card_id INTEGER NOT NULL,
    movement_date DATE NOT NULL,
    movement_type VARCHAR(20) NOT NULL,  -- 'receipt', 'issue', 'transfer', 'adjustment'
    quantity DECIMAL(12,4) NOT NULL,
    document_id INTEGER,
    document_type VARCHAR(20),
    
    FOREIGN KEY (card_id) REFERENCES stock_cards(card_id) ON DELETE RESTRICT
);
```

---

### 4.2 Stock Movements → Documents

**Polymorfný vzťah:**
```
stock_movements.document_id + document_type → receipt_documents | issue_documents | transfer_documents
```

**Poznámka:** Polymorfný vzťah - `document_type` určuje do ktorej tabuľky odkazuje `document_id`

---

## 5. INDEXY PRE PERFORMANCE

### Catalogs - Products
```sql
-- Product Catalog
CREATE INDEX idx_product_catalog_name ON product_catalog(product_name);
CREATE INDEX idx_product_catalog_business_type ON product_catalog(business_type);
CREATE INDEX idx_product_catalog_product_type ON product_catalog(product_type);
CREATE INDEX idx_product_catalog_vat_group ON product_catalog(vat_group_id);
CREATE INDEX idx_product_catalog_disabled ON product_catalog(is_disabled);

-- Product Identifiers (vyhľadávanie podľa EAN)
CREATE INDEX idx_identifiers_code ON product_catalog_identifiers(identifier_code);
CREATE INDEX idx_identifiers_type_code ON product_catalog_identifiers(identifier_type, identifier_code);

-- Product Categories
CREATE INDEX idx_product_categories_type_category ON product_catalog_categories(category_type, category_id);
CREATE INDEX idx_product_categories_product ON product_catalog_categories(product_id);

-- Categories Master
CREATE INDEX idx_categories_type ON product_categories(category_type);
CREATE INDEX idx_categories_code ON product_categories(category_code);
```

### Stock
```sql
-- Stock Cards
CREATE INDEX idx_stock_cards_product ON stock_cards(product_id);
CREATE INDEX idx_stock_cards_warehouse ON stock_cards(warehouse_id);
CREATE INDEX idx_stock_cards_quantity ON stock_cards(quantity_on_hand) WHERE quantity_on_hand > 0;

-- Stock Movements
CREATE INDEX idx_movements_card_date ON stock_movements(card_id, movement_date);
CREATE INDEX idx_movements_document ON stock_movements(document_type, document_id);
```

### Accounting
```sql
-- Invoices
CREATE INDEX idx_invoices_partner ON invoices(partner_id) WHERE partner_id IS NOT NULL;
CREATE INDEX idx_invoices_date ON invoices(invoice_date);
CREATE INDEX idx_invoices_number ON invoices(invoice_number);

-- Invoice Items
CREATE INDEX idx_invoice_items_product ON invoice_items(product_id) WHERE product_id IS NOT NULL;
CREATE INDEX idx_invoice_items_invoice ON invoice_items(invoice_id);
```

---

## 6. BIZNIS PRAVIDLÁ

### 6.1 Referenčná integrita

**Prísne pravidlá (ON DELETE RESTRICT) - Master Data:**
- ✅ Nesmie sa zmazať produkt ak existuje **stock card** (aktívna zásoba)
- ✅ Nesmie sa zmazať VAT group ak existujú produkty s ňou
- ✅ Nesmie sa zmazať category ak existujú produkty v nej
- ✅ Nesmie sa zmazať warehouse ak existujú stock cards
- ✅ Nesmie sa zmazať invoice ak existujú invoice items

**Kaskádové mazanie (ON DELETE CASCADE) - Závislé dáta:**
- ✅ Ak zmažem produkt → zmažú sa extensions, identifiers, categories, texts
- ✅ Ak zmažem invoice → zmažú sa invoice items
- ✅ Ak zmažem document → zmažú sa document items

**Nullovanie (ON DELETE SET NULL) - Voliteľné väzby:**
- ✅ Ak zmažem obal (package_product_id) → nastaví sa NULL

**BEZ FK CONSTRAINT - Archívne dokumenty:**
- ✅ `invoices.partner_id` - môže byť NULL, partner môže byť zmazaný
- ✅ `invoice_items.product_id` - môže byť NULL, produkt môže byť zmazaný
- ✅ `receipt_documents.supplier_id` - môže byť NULL
- ✅ `issue_documents.customer_id` - môže byť NULL

**Dôvod archívnej denormalizácie:**  
Podľa slovenských účtovných predpisov **nemožno meniť údaje na účtovných dokladoch spätne**. Všetky údaje (názvy, ceny, adresy) sú uložené priamo v dokumente ako snapshot v čase vystavenia. Ak zmeníme názov produktu dnes, stará faktúra spred roka musí zostať nezmenená!

---

### 6.2 Konzistencia dát

**Denormalizované polia (treba syncovať):**
```
product_catalog_extensions.last_receipt_date ← stock_movements.movement_date
product_catalog_extensions.last_receipt_stock ← stock_movements.warehouse_id
product_catalog_extensions.last_supplier_id ← receipt_documents.supplier_id
```

**Riešenie:** Database triggers alebo application logic

**Archívne dokumenty (IMMUTABLE - nemenné):**
```
invoices.partner_name, partner_address, partner_ico... (snapshot)
invoice_items.product_name, unit_price, vat_rate... (snapshot)
receipt_documents.supplier_name, supplier_address... (snapshot)
issue_documents.customer_name, customer_address... (snapshot)
```

**Riešenie:** Kópia dát pri vytvorení dokumentu, potom sa NIKDY nemenia!

---

### 6.3 Validačné pravidlá

**Products:**
- `business_type` IN ('M', 'T', 'S')
- `product_type` IN ('T', 'W', 'O')
- `package_product_id` → musí byť produkt kde `product_type = 'O'`

**Product Categories:**
- Ak `category_type = 'product'` → must exist in `product_categories` WHERE `category_type = 'product'`
- Ak `category_type = 'financial'` → must exist in `product_categories` WHERE `category_type = 'financial'`
- Ak `category_type = 'specific'` → must exist in `product_categories` WHERE `category_type = 'specific'`
- Produkt môže mať max. 1 kategóriu každého typu (UNIQUE constraint)

**Product Partners:**
- Ak `partner_type = 'manufacturer'` → must exist in `partner_catalog` WHERE `partner_type = 'manufacturer'`
- Ak `partner_type = 'supplier'` → must exist in `partner_catalog` WHERE `partner_type = 'supplier'`

**Stock Cards:**
- `quantity_on_hand` >= `quantity_reserved`
- `quantity_on_hand` >= 0 (nemôže byť záporný stav)

**Archívne dokumenty:**
- Po vytvorení sa NESMÚ meniť žiadne údaje
- Všetky denormalizované polia musia byť vyplnené pri vytvorení

---

## 7. QUERY PATTERNS

### 7.1 Získať produkt s všetkými údajmi
```sql
SELECT 
    p.*,
    vg.vat_rate,
    pe.*
FROM product_catalog p
LEFT JOIN vat_groups vg ON p.vat_group_id = vg.vat_group_id
LEFT JOIN product_catalog_extensions pe ON p.product_id = pe.product_id
WHERE p.product_id = ?;
```

---

### 7.2 Vyhľadať produkt podľa EAN
```sql
SELECT p.*
FROM product_catalog p
INNER JOIN product_catalog_identifiers pi ON p.product_id = pi.product_id
WHERE pi.identifier_type = 'barcode'
  AND pi.identifier_code = ?;
```

---

### 7.3 Získať skladový stav produktu
```sql
SELECT 
    p.product_name,
    w.warehouse_name,
    sc.quantity_on_hand,
    sc.quantity_reserved,
    sc.quantity_on_hand - sc.quantity_reserved AS available_quantity
FROM stock_cards sc
INNER JOIN product_catalog p ON sc.product_id = p.product_id
INNER JOIN warehouses w ON sc.warehouse_id = w.warehouse_id
WHERE sc.product_id = ?;
```

---

### 7.4 Získať všetky kategórie produktu
```sql
SELECT 
    pc.category_type,
    c.category_code,
    c.category_name
FROM product_catalog_categories pc
INNER JOIN product_categories c ON pc.category_id = c.category_id
WHERE pc.product_id = ?
ORDER BY pc.category_type;
```

---

### 7.5 Získať výrobcu a dodávateľa produktu
```sql
SELECT 
    pp.partner_type,
    p.partner_code,
    p.partner_name
FROM product_catalog_partners pp
INNER JOIN partner_catalog p ON pp.partner_id = p.partner_id
WHERE pp.product_id = ?;
```

---

### 7.6 Vytlačiť faktúru (bez JOINs!)
```sql
-- Hlavička faktúry (všetko uložené)
SELECT 
    invoice_number,
    invoice_date,
    partner_name,     -- denormalizované
    partner_address,  -- denormalizované
    partner_ico,      -- denormalizované
    total_amount,
    vat_amount
FROM invoices
WHERE invoice_id = ?;

-- Položky faktúry (všetko uložené)
SELECT 
    product_code,     -- denormalizované
    product_name,     -- denormalizované
    quantity,
    unit_name,        -- denormalizované
    unit_price,       -- denormalizované
    vat_rate,         -- denormalizované
    line_total
FROM invoice_items
WHERE invoice_id = ?
ORDER BY item_id;
```

**Poznámka:** Žiadne JOINy! Všetko je uložené priamo v dokumente.

---

## 8. DIAGRAM VZŤAHOV (ER Diagram)

```
┌─────────────────┐
│   VAT_GROUPS    │
│  vat_group_id   │──┐
└─────────────────┘  │
                     │ N:1
┌──────────────────────────────────┐
│      PRODUCT_CATALOG             │
│      product_id (PK)             │
│   vat_group_id (FK)              │──┐
│   package_product_id (FK)        │──┘ self-reference
└──────────────────────────────────┘
    │         │         │         │
    │ 1:1     │ 1:N     │ 1:N     │ 1:N
    ↓         ↓         ↓         ↓
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│PRODUCT_ │ │PRODUCT_ │ │PRODUCT_ │ │PRODUCT_ │
│CATALOG_ │ │CATALOG_ │ │CATALOG_ │ │CATALOG_ │
│EXTENS.  │ │IDENTIF. │ │CATEGOR. │ │ TEXTS   │
└─────────┘ └─────────┘ └─────────┘ └─────────┘
                            │ N:1
                            ↓
                ┌────────────────────────┐
                │  PRODUCT_CATEGORIES    │
                │    category_id (PK)    │
                │    category_type       │
                │  parent_category_id    │
                └────────────────────────┘
                            │ self-reference
                            ↓

┌──────────────────────────────────┐
│      PARTNER_CATALOG             │
│      partner_id (PK)             │
└──────────────────────────────────┘
    ↑                           ↑
    │ N:1                       │ N:1
┌─────────────────┐     ┌──────────────────┐
│PRODUCT_CATALOG_ │     │    INVOICES      │
│    PARTNERS     │     │ partner_id (NULL)│ BEZ FK!
└─────────────────┘     └──────────────────┘
                                │ 1:N
                                ↓
                        ┌──────────────────┐
                        │  INVOICE_ITEMS   │
                        │ product_id (NULL)│ BEZ FK!
                        └──────────────────┘
```

**Legenda:**
- **Plné čiary** = FK constraints
- **BEZ FK!** = Archívne dokumenty bez constraints

---

## 9. POTREBNÉ ČÍSELNÍKY

**Aktuálne zdokumentované:**
- ✅ product_catalog (GSCAT-product_catalog.md)
- ✅ product_catalog_extensions (GSCAT-product_catalog.md)
- ✅ product_catalog_identifiers (GSCAT-product_catalog.md)
- ✅ product_catalog_categories (GSCAT-product_catalog.md)
- ✅ product_catalog_texts (GSCAT-product_catalog.md)
- ✅ vat_groups (GSCAT-product_catalog.md)

**Čakajú na dokumentáciu:**
- ⏳ product_categories (MGLST-product_categories.md, FGLST-product_categories.md, SGLST-product_categories.md)
- ⏳ partner_catalog (PAB-partner_catalog.md)
- ⏳ units (merné jednotky)
- ⏳ warehouses (sklady)
- ⏳ stock_cards (skladové karty)
- ⏳ chart_of_accounts (účtová osnova)
- ⏳ invoices (faktúry - archívne)
- ⏳ receipt_documents (príjemky - archívne)
- ⏳ issue_documents (výdajky - archívne)

---

**Vytvoril:** Claude & Zoltán  
**Dátum:** 2025-12-10  
**Verzia:** 1.0  
**Status:** 🔄 V práci - rozširuje sa s každou novou tabuľkou