# Stock Reference - Skladové hospodárstvo

**Category:** Database / Stock  
**Status:** 🔴 Placeholder (0% documented)  
**Created:** 2025-12-15  
**Updated:** 2025-12-15  
**Related:** [CATALOGS_REFERENCE.md](CATALOGS_REFERENCE.md), [SALES_REFERENCE.md](SALES_REFERENCE.md)

---

## ÚČEL SEKCIE

Táto sekcia dokumentuje **skladové hospodárstvo** NEX Automat - všetko čo súvisí so skladovými kartami, pohybmi, príjemkami a výdajkami.

### Bude obsahovať:
- 📦 **Stock Cards** - skladové karty produktov
- 📊 **Movements** - pohyby na skladoch
- 📥 **Receipts** - príjemky tovaru
- 📤 **Issues** - výdajky tovaru
- 🏭 **Warehouses** - sklady a prevádzky
- 📈 **FIFO** - oceňovanie zásob

---

## HLAVNÉ KOMPONENTY

### 1. Stock Cards (Skladové karty)

**Účel:** Evidence zásob produktov na skladoch

**Tabuľky:**
- ⏳ `stock_cards` - skladové karty (STK.BTR)
- ⏳ `stock_movements` - pohyby (STM.BTR)
- ⏳ `stock_fifos` - FIFO oceňovanie (FIF.BTR)

**Dokumentácia:**
- 📋 Todo: STK-stock_cards.md
- 📋 Todo: STM-stock_card_movements.md
- 📋 Todo: FIF-stock_card_fifos.md

---

### 2. Warehouses (Sklady)

**Účel:** Číselník skladov a prevádzkových jednotiek

**Tabuľky:**
- ⏳ `warehouses` - sklady (WRILST.BTR)
- ⏳ `stocks` - sklady alternatívne (STKLST.BTR)

**Dokumentácia:**
- 📋 Todo: WRILST-facilities.md
- 📋 Todo: STKLST-stocks.md

---

### 3. Documents (Príjemky, Výdajky)

**Účel:** Skladové doklady

**Tabuľky:**
- ⏳ `supplier_delivery_heads` - hlavičky príjemok (TSH.BTR)
- ⏳ `supplier_delivery_items` - položky príjemok (TSI.BTR)

**Dokumentácia:**
- 📋 Todo: TSH-supplier_delivery_heads.md
- 📋 Todo: TSI-supplier_delivery_items.md

---

## MIGRÁCIA Z NEX GENESIS

### Btrieve → PostgreSQL Mapping

| Btrieve | PostgreSQL | Status | Poznámka |
|---------|-----------|--------|----------|
| STK.BTR | stock_cards | 📋 Todo | Skladové karty |
| STM.BTR | stock_movements | 📋 Todo | Pohyby na skladoch |
| FIF.BTR | stock_fifos | 📋 Todo | FIFO oceňovanie |
| WRILST.BTR | warehouses | 📋 Todo | Sklady |
| STKLST.BTR | stocks | 📋 Todo | Sklady alternatívne |
| TSH.BTR | supplier_delivery_heads | 📋 Todo | Príjemky hlavičky |
| TSI.BTR | supplier_delivery_items | 📋 Todo | Príjemky položky |

---

## VZŤAHY S INÝMI SEKCIAMI

### Catalogs
- `stock_cards.product_id` → `product_catalog.product_id`
- `stock_cards.warehouse_id` → `warehouses.warehouse_id`

### Accounting
- Skladové pohyby generujú účtovné zápisy
- FIFO oceňovanie pre výpočet nákladov

### Sales
- Stock levels pre dostupnosť produktov
- Rezervácie pre objednávky

---

## POZNÁMKY

**Tento dokument je placeholder** pre budúcu dokumentáciu skladového hospodárstva.

Detailná dokumentácia bude vytvorená v ďalších fázach migrácie .md-old súborov.

---

**Progress:** 0/7 tabuliek (0%)  
**Status:** 🔴 Placeholder  
**Ďalej:** Postupná dokumentácia stock tabuliek

---

**Vytvoril:** Claude & Zoltán  
**Dátum:** 2025-12-15  
**Verzia:** 0.1 (Placeholder)
