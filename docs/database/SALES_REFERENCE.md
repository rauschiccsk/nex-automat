# Sales Reference - Odbytový systém

**Category:** Database / Sales  
**Status:** 🟡 In Progress (1/10 tables documented)  
**Created:** 2025-12-10  
**Updated:** 2025-12-15  
**Related:** [CATALOGS_REFERENCE.md](CATALOGS_REFERENCE.md), [PRODUCTS_REFERENCE.md](PRODUCTS_REFERENCE.md)

---


## ÚČEL SEKCIE

Táto sekcia dokumentuje **odbytový systém** NEX Automat - všetko čo súvisí s predajom tovaru, cenovým hospodárstvom a obchodnými podmienkami.

### Obsahuje:
- 📋 **Cenníky** - predajné ceny produktov
- 💰 **Cenové histórie** - zmeny cien v čase
- 🏷️ **Zľavové systémy** - akcie, kampane, množstevné zľavy
- 📊 **Obchodné podmienky** - pre zákazníkov a produkty

---

## HLAVNÉ KOMPONENTY

### 1. Price Lists (Cenníky)

**Účel:** Správa predajných cien produktov v rôznych cenníkoch

**Tabuľky:**
- `price_list_items` - položky cenníkov (ceny produktov)
- `price_lists` - číselník cenníkov (názvy, platnosť)
- `price_history` - história zmien cien

**Dokumentácia:**
- ✅ [PLSnnnnn-price_list_items.md](tables/PLSnnnnn-price_list_items.md)
- ⏳ price_lists.md (Todo)
- ⏳ price_history.md (Todo)

---

### 2. Discount System (Zľavy)

**Účel:** Správa zľavových systémov a akcií

**Tabuľky:**
- `discount_rules` - pravidlá zľavy
- `discount_campaigns` - akciové kampane
- `discount_vouchers` - zľavové kupóny

**Dokumentácia:**
- 📋 Todo

---

### 3. Customer Pricing (Zákaznícke ceny)

**Účel:** Špecifické ceny pre konkrétnych zákazníkov

**Tabuľky:**
- `customer_price_agreements` - cenové dohody
- `customer_discounts` - individuálne zľavy

**Dokumentácia:**
- 📋 Todo

---

## MIGRÁCIA Z NEX GENESIS

### Btrieve → PostgreSQL Mapping

| Btrieve | PostgreSQL | Status | Poznámka |
|---------|-----------|--------|----------|
| PLSnnnnn.BTR | price_list_items | ✅ Zdokumentované | Viacero súborov → 1 tabuľka |
| (v PAB.BTR) | customer_price_agreements | 📋 Todo | Cenové dohody v partnerovi |
| (kód v Pascale) | discount_rules | 📋 Todo | Pravidlá boli hardcoded |

### Kľúčové zmeny:
- ✅ **Konsolidácia cenníkov** - z PLSnnnnn.BTR → jedna tabuľka price_list_items
- ✅ **Eliminácia duplikácie** - údaje z GSCAT sa už nekopírujú do cenníkov
- ✅ **História cien** - nová funkcionalita (v Genesis neexistovala)
- ⏳ **Zľavový systém** - prechod z hardcoded logiky do databázy

---

## BIZNIS LOGIKA

### 1. Cenová hierarchia

**Priorita pri určení ceny:**
1. Zákaznícka cenová dohoda (customer_price_agreements)
2. Špecifická cena pre sklad (price_list_items.stock_list_id)
3. Univerzálna cena (price_list_items.stock_list_id IS NULL)
4. Základná cena z product_catalog

### 2. Výpočet finálnej ceny

```sql
-- Finálna cena po zľavách
final_price = base_price * (1 - discount_percentage / 100)

-- S množstevnou zľavou
IF quantity >= min_quantity_for_discount THEN
    final_price = base_price * (1 - volume_discount / 100)
END IF
```

### 3. Akciové ceny

**Princíp:**
- Produkt má `is_promotional = TRUE` v price_list_items
- Akcia má časovú platnosť (from_date, to_date)
- Po skončení akcie sa vráti pôvodná cena

---

## VZŤAHY S INÝMI SEKCIAMI

### Catalogs
- `price_list_items.product_id` → `product_catalog.product_id`
- `customer_price_agreements.partner_id` → `partner_catalog.partner_id`

### Warehouses
- `price_list_items.stock_list_id` → `warehouses.warehouse_id`

### Accounting
- Predajné ceny sa používaju pri fakturácii
- Zľavy ovplyvňujú účtovné zápisy

---

## TABUĽKOVÁ DOKUMENTÁCIA

### Hotové dokumenty

| Dokument | Tabuľka | Status | Poznámka |
|----------|---------|--------|----------|
| [PLSnnnnn-price_list_items.md](tables/PLSnnnnn-price_list_items.md) | price_list_items | ✅ Kompletné | Cenníkové položky |

### Čakajú na spracovanie

| Priorita | Dokument | Tabuľka | Poznámka |
|----------|----------|---------|----------|
| 1 | price_lists.md | price_lists | Číselník cenníkov |
| 2 | price_history.md | price_history | História zmien cien |
| 3 | discount_rules.md | discount_rules | Pravidlá zľavy |

---

## KĽÚČOVÉ KONCEPTY

### 1. Multi-Price List System

NEX Automat podporuje **viacero cenníkov** súčasne:
- CL1 = Maloobchod
- CL2 = Veľkoobchod  
- CL3 = Akciový cenník
- CLn = Vlastné cenníky

### 2. Stock-Specific Pricing

Produkt môže mať **rôzne ceny na rôznych skladoch**:
```sql
-- Univerzálna cena
(price_list_id=1, product_id=1001, stock_list_id=NULL, price=15.00)

-- Špecifická cena pre sklad 2
(price_list_id=1, product_id=1001, stock_list_id=2, price=14.00)
```

### 3. Promotional Items

**Akciové produkty:**
- `is_promotional = TRUE`
- Zvýraznené v UI/e-shope
- Filter pre akciový leták
- Automatické označenie pri zľave > 10%

### 4. Price Override

**Otvorené PLU (allow_price_override):**
- Pokladníčka môže zmeniť cenu
- Typicky pre vážený tovar
- Auditný záznam zmeny

---

## PRÍKLADY QUERIES

### Získať cenu produktu

```sql
-- Aktuálna predajná cena
SELECT 
    p.product_name,
    pli.price_incl_vat,
    pli.min_quantity,
    pli.is_promotional
FROM price_list_items pli
INNER JOIN product_catalog p ON pli.product_id = p.product_id
WHERE pli.price_list_id = 1
  AND pli.product_id = 1001
  AND pli.is_disabled = FALSE
  AND (pli.stock_list_id IS NULL OR pli.stock_list_id = :warehouse_id)
ORDER BY pli.stock_list_id NULLS LAST
LIMIT 1;
```

### Porovnanie cien v cenníkoch

```sql
-- Rozdiel medzi maloobchodom a veľkoobchodom
SELECT 
    p.product_name,
    pli1.price_incl_vat AS retail_price,
    pli2.price_incl_vat AS wholesale_price,
    pli1.price_incl_vat - pli2.price_incl_vat AS difference,
    ROUND((pli1.price_incl_vat - pli2.price_incl_vat) / pli2.price_incl_vat * 100, 2) AS discount_pct
FROM product_catalog p
INNER JOIN price_list_items pli1 ON p.product_id = pli1.product_id AND pli1.price_list_id = 1
INNER JOIN price_list_items pli2 ON p.product_id = pli2.product_id AND pli2.price_list_id = 2
WHERE p.is_disabled = FALSE
ORDER BY discount_pct DESC;
```

### Akciové produkty

```sql
-- Produkty v akcii
SELECT 
    p.product_name,
    pli.price_incl_vat,
    pli.profit_margin
FROM price_list_items pli
INNER JOIN product_catalog p ON pli.product_id = p.product_id
WHERE pli.price_list_id = 1
  AND pli.is_promotional = TRUE
  AND pli.is_disabled = FALSE
ORDER BY p.product_name;
```

---

## MIGRAČNÝ PLÁN

### Fáza 1: Základné cenníky ✅
- [x] price_list_items - DONE
- [ ] price_lists - číselník cenníkov
- [ ] price_history - história zmien

### Fáza 2: Zľavy
- [ ] discount_rules - pravidlá zľavy
- [ ] discount_campaigns - kampane
- [ ] discount_vouchers - kupóny

### Fáza 3: Zákaznícke ceny
- [ ] customer_price_agreements - cenové dohody
- [ ] customer_discounts - individuálne zľavy

---

## POZNÁMKY PRE VÝVOJ

### 1. Denormalizácia v dokladoch

**KRITICKÉ:** Pri vytváraní faktúr/dokladov sa ceny **DENORMALIZUJÚ**:
- Archívne dokumenty obsahujú snapshot ceny
- BEZ FK constraints na price_list_items
- Dôvod: právny požiadavok (SK účtovné predpisy)

### 2. Cache stratégia

**Pre performance:**
- Ceny sa načítavajú pri štarte session
- Invalidácia cache pri zmene cien
- Redis/Memcached pre multi-user environment

### 3. Audit trail

**Sledovanie zmien:**
- Každá zmena ceny → záznam do price_history
- created_by/updated_by pre compliance
- Timestamp s presnosťou na sekundu

---

## SÚVISIACE SEKCIE

- [Catalogs](../catalogs/products/INDEX.md) - Produkty, partneri, kategórie
- [Warehouses](../warehouses/INDEX.md) - Sklady a zásoby
- [Invoices](../invoices/INDEX.md) - Fakturácia
- [Accounting](../accounting/INDEX.md) - Účtovníctvo

---

**Progress:** 1/10 tabuliek (10%)  
**Status:** 🔄 Aktívna dokumentácia  
**Ďalej:** price_lists.md, price_history.md

---

**Vytvoril:** Claude & Zoltán  
**Dátum:** 2025-12-10  
**Verzia:** 1.0