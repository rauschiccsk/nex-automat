# Session Archive: Database Table Docs Batch 6 - Stock Management Complete

**Dátum:** 2025-12-15  
**Trvanie:** ~45 minút  
**Status:** ✅ Complete - Stock Management section finished  
**Tokens použité:** ~82,000 / 190,000 (43%)

---

## Prehľad Session

Pokračovanie batch 6 migrácie database table dokumentácie - dokončenie Stock Management sekcie (2 dokumenty).

---

## Dokončené Úlohy

### 1. STM-stock_card_movements.md (35.6 KB → 15.3 KB)

**Súbor:**
- Originál: `docs/architecture/database/stock/cards/tables/STM-stock_card_movements.md-old`
- Vyčistený: `docs/architecture/database/stock/cards/tables/STM-stock_card_movements.md`

**Btrieve umiestnenie:**
- Adresár: `C:\NEX\YEARACT\STORES\`
- Súbory: `STMnnnnn.BTR` (multi-file, per sklad)

**Kľúčové vlastnosti:**
- Denník skladových pohybov
- Multi-file architektúra (STM00001.BTR, STM00002.BTR, ...)
- PostgreSQL: jedna tabuľka + stock_id
- Každý príjem = 1 STM + 1 FIFO karta
- Výdaj môže byť cez viacero STM záznamov (FIFO logika)

**Redukcia:** 57%

**Zachované:**
- Mapping polí (Btrieve → PostgreSQL)
- Biznis logika (typy pohybov, príjem, výdaj, prevody, FIFO)
- Vzťahy s tabuľkami
- Validačné pravidlá
- Príklady dát

**Odstránené:**
- CREATE TABLE statements
- CREATE INDEX statements
- CREATE TRIGGER statements
- Query patterns (veľké SQL bloky)
- Python migration code

### 2. STK-stock_cards.md (38.5 KB → 16.5 KB)

**Súbor:**
- Originál: `docs/architecture/database/stock/cards/tables/STK-stock_cards.md-old`
- Vyčistený: `docs/architecture/database/stock/cards/tables/STK-stock_cards.md`

**Btrieve umiestnenie:**
- Adresár: `C:\NEX\YEARACT\STORES\`
- Súbory: `STKnnnnn.BTR` (multi-file, per sklad)

**Kľúčové vlastnosti:**
- Skladové karty zásob (master data)
- Multi-file architektúra (STK00001.BTR, STK00002.BTR, ...)
- PostgreSQL: jedna tabuľka + stock_id
- Composite PK: (stock_id, product_id)
- Oceňovanie: AVCO, FIFO, Last Price
- Normatívy: min/max/opt
- Rezervácie a objednávky

**Redukcia:** 57%

**Zachované:**
- Mapping polí (40+ polí)
- Biznis logika (oceňovanie, voľné množstvo, normatívy)
- Vzťahy s tabuľkami
- Validačné pravidlá
- Príklady dát

**Odstránené:**
- CREATE TABLE statements (komplexná schéma)
- CREATE INDEX statements (10+ indexov)
- CREATE TRIGGER statements (3 triggery)
- Query patterns (10+ queries)
- Python migration code
- Materializované views

---

## Progress Summary

### Celkový Progress

**Dokončené:** 20/28 dokumentov (71.4%)

**By Category:**
- ✅ **Partners:** 8/8 (100%) - COMPLETE
- ✅ **Products:** 5/5 (100%) - COMPLETE
- ✅ **Stock Management:** 7/7 (100%) - COMPLETE ⭐
- ⏳ **Accounting:** 0/3 (0%)
- ⏳ **Sales:** 0/1 (0%)

### Stock Management Complete (7/7)

1. ✅ WRILST-facilities.md (17.9 KB → 7.7 KB)
2. ✅ STKLST-stocks.md (20.4 KB → 8.7 KB)
3. ✅ TSH-supplier_delivery_heads.md (25.4 KB → 11.2 KB)
4. ✅ FIF-stock_card_fifos.md (28.5 KB → 11.8 KB)
5. ✅ TSI-supplier_delivery_items.md (29.7 KB → 12.5 KB)
6. ✅ **STM-stock_card_movements.md** (35.6 KB → 15.3 KB) ⭐ NEW
7. ✅ **STK-stock_cards.md** (38.5 KB → 16.5 KB) ⭐ NEW

**Priemerná redukcia:** 57.4%

### Zostáva (8 dokumentov)

**Accounting (3 sÃºbory):**
- ISH-supplier_invoice_heads.md-old (34.8 KB)
- ISI-supplier_invoice_items.md-old (29.6 KB)
- PAYJRN-payment_journal.md-old (25.8 KB)

**Sales (1 sÃºbor):**
- PLSnnnnn-price_list_items.md-old (20.5 KB)

**Poznámka:** 4 ďalšie dokumenty (4 súbory, iné kategórie)

---

## Technické Detaily

### Btrieve Locations Zistené

**DIALS adresár:**
- BANKLST.BTR, PAB.BTR, PABACC.BTR, PACNCT.BTR
- PAGLST.BTR, PAYLST.BTR, TRPLST.BTR
- PANOTI.BTR, PASUBC.BTR

**STORES adresár:**
- BARCODE.BTR, FGLST.BTR, GSCAT.BTR, MGLST.BTR, SGLST.BTR
- WRILST.BTR, STKLST.BTR
- TSH[YY][NNN].BTR, TSI[YY][NNN].BTR
- FIF[NNNNN].BTR
- **STM[NNNNN].BTR** ⭐ (verified)
- **STK[NNNNN].BTR** ⭐ (verified)

### Multi-file Architektúra

**Stock Management súbory s multi-file architektúrou:**

1. **TSH/TSI** (Supplier Delivery Documents):
   - Btrieve: TSH25001.BTR, TSH25002.BTR (kniha+rok)
   - PostgreSQL: supplier_delivery_heads (jedna tabuľka)

2. **FIF** (FIFO Cards):
   - Btrieve: FIF00001.BTR, FIF00002.BTR (per sklad)
   - PostgreSQL: stock_card_fifos (jedna tabuľka + stock_id)

3. **STM** (Stock Movements):
   - Btrieve: STM00001.BTR, STM00002.BTR (per sklad)
   - PostgreSQL: stock_card_movements (jedna tabuľka + stock_id)

4. **STK** (Stock Cards):
   - Btrieve: STK00001.BTR, STK00002.BTR (per sklad)
   - PostgreSQL: stock_cards (jedna tabuľka + stock_id)
   - Composite PK: (stock_id, product_id)

### Konzistentný Formát

**Všetky dokumenty obsahujú:**
- Prehľad a účel
- Btrieve súbor info (názov, umiestnenie, štruktúra)
- PostgreSQL architektúra
- Mapping polí (Btrieve → PostgreSQL)
- Polia ktoré SA NEPRENÁŠAJÚ
- Biznis logika
- Vzťahy s inými tabuľkami
- Validačné pravidlá
- Príklady dát
- Poznámky pre migráciu
- Verzia a zmeny

**Metadata:**
- Status: ✅ Pripravené na migráciu
- Batch: Batch 6 (Stock Management)
- Dátum: 2025-12-15

---

## Workflow Použitý

1. **web_fetch** - načítať .md-old z GitHubu
2. **Opýtať sa na Btrieve location** - STORES (verified)
3. **Vytvoriť artifact** - vyčistený dokument
4. **User skopíruje + zmaže starý** - manuálne
5. **Pokračovať ďalším dokumentom**

---

## Kľúčové Poznatky

### 1. FIFO Logika v Stock Management

**Výdaj cez viacero FIFO kariet:**
- Jeden doklad môže vytvoriť viacero STM záznamov
- Každý záznam s iným fifo_id
- Rovnaký document_number a document_line_number
- Postupné spotrebovanie FIFO kariet

**Príklad:**
- Dostupné FIFO: 50 ks + 200 ks
- Výdaj: 120 ks
- Výsledok: 2 STM záznamy (50 ks + 70 ks)

### 2. Oceňovanie Zásob

**Tri metódy:**
1. **AVCO** (Average Cost): average_price = value_total / quantity_on_hand
2. **FIFO**: current_fifo_price (z najstaršej aktívnej FIFO karty)
3. **Last**: last_purchase_price (posledná nákupná cena)

### 3. Voľné Množstvo

**Automatický prepočet (trigger):**
```
free_quantity = quantity_on_hand 
              - reserved_customer_orders 
              - reserved_other 
              - sold_quantity
```

**Poznámka:** Môže byť záporné (viac rezervácií ako zásob).

### 4. Normatívy

**Min/Max/Opt:**
- min_quantity: dolná hranica (objednať ak pod)
- max_quantity: horná hranica (prebytok ak nad)
- optimal_quantity: optimálne množstvo
- Validácia: min ≤ opt ≤ max

### 5. Prevody medzi Skladmi

**2 pohyby:**
- Prevod OUT zo Skladu 1 (movement_type_code = 6)
- Prevod IN do Skladu 2 (movement_type_code = 5)
- Prepojené cez contra_stock_id
- Rovnaký document_number

---

## Štatistiky

### Dokončené v Tejto Session

- **Dokumenty:** 2
- **Originálne KB:** 74.1 KB
- **Vyčistené KB:** 31.8 KB
- **Redukcia:** 57.1%
- **Čas:** ~45 minút
- **Tokens:** ~82,000

### Celkové (Batch 6)

- **Dokumenty dokončené:** 20/28 (71.4%)
- **Celková redukcia:** 57.4%
- **Stock Management:** 7/7 (100%) ✅

---

## Next Steps

### Accounting Section (3 dokumenty)

**Odporúčané poradie:**

1. **ISH-supplier_invoice_heads.md-old** (34.8 KB)
   - Hlavičky dodávateľských faktúr
   - Prepojenie s TSH (dodacie listy)
   - Multi-file? (ISH[YY][NNN].BTR? - overiť)

2. **ISI-supplier_invoice_items.md-old** (29.6 KB)
   - Položky dodávateľských faktúr
   - Prepojenie s TSI (položky dodacích listov)
   - Multi-file? (ISI[YY][NNN].BTR? - overiť)

3. **PAYJRN-payment_journal.md-old** (25.8 KB)
   - Platobný denník
   - Prepojenie s ISH (úhrady faktúr)
   - Pravdepodobne: C:\NEX\YEARACT\ACCOUNTS\

### Sales Section (1 dokument)

4. **PLSnnnnn-price_list_items.md-old** (20.5 KB)
   - Položky cenníka
   - Multi-file: PLS[NNNNN].BTR (per cenník)
   - Pravdepodobne: C:\NEX\YEARACT\STORES\

**Estimated time:** 90-120 minút (veľké dokumenty)

---

## Git Commit

```bash
git add docs/architecture/database/stock/cards/tables/
git commit -m "docs: Database table docs batch 6 - stock management complete (2 docs)"
git push origin develop
```

---

**Session Complete:** ✅  
**Stock Management:** ✅ 100%  
**Overall Progress:** 20/28 (71.4%)  
**Archived:** 2025-12-15