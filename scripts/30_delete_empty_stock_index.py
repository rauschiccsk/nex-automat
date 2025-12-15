#!/usr/bin/env python3
"""
Script 30: Create STOCK_REFERENCE.md placeholder
Reason: Empty INDEX.md-old, but maintain reference doc structure
"""

from pathlib import Path


def create_stock_reference() -> str:
    """Generate placeholder content for stock reference."""

    return """# Stock Reference - Skladové hospodárstvo

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
"""


def main():
    """Create stock reference placeholder."""

    # Paths
    source = Path(r"C:\Development\nex-automat\docs\architecture\database\stock\INDEX.md-old")
    target = Path(r"C:\Development\nex-automat\docs\database\STOCK_REFERENCE.md")

    print("=" * 70)
    print("Script 30: Create Stock Reference Placeholder")
    print("=" * 70)

    # Check source
    if not source.exists():
        print(f"\n❌ Source not found: {source}")
        return False

    print(f"\n📄 Source:")
    print(f"   {source}")
    print(f"   Size: {source.stat().st_size:,} bytes (empty)")

    print(f"\n📄 Target:")
    print(f"   {target}")

    # Check if target exists
    if target.exists():
        print(f"\n⚠️  Target already exists!")
        return False

    # Ensure target directory exists
    target.parent.mkdir(parents=True, exist_ok=True)

    # Create placeholder content
    content = create_stock_reference()

    # Write to target
    try:
        target.write_text(content, encoding='utf-8')
        print(f"\n✅ Placeholder created: {target}")
        print(f"   Size: {len(content):,} bytes")
    except Exception as e:
        print(f"\n❌ Error writing target: {e}")
        return False

    # Delete empty source
    try:
        source.unlink()
        print(f"✅ Empty source deleted: {source}")
    except Exception as e:
        print(f"\n❌ Error deleting source: {e}")
        return False

    print(f"\n📊 Summary:")
    print(f"   - Created placeholder for future stock documentation")
    print(f"   - Maintains consistent reference doc structure")
    print(f"   - Ready for future table documentation")

    return True


if __name__ == "__main__":
    success = main()
    print("\n" + "=" * 70)
    if success:
        print("✅ Migration complete - Stock reference placeholder created")
        print("\nNext steps:")
        print("1. Update docs/database/00_DATABASE_INDEX.md")
        print("2. Update docs.json manifest")
        print("3. Continue with stock/cards/INDEX.md-old")
    else:
        print("❌ Migration failed")
    print("=" * 70)