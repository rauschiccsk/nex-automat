# INIT PROMPT - NEX Automat: Database Table Docs Migration (Batch 6 Continue)

**Projekt:** nex-automat  
**Úloha:** Database table docs migration (batch 6 continuation - dokončenie Stock Management + start Accounting)  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** https://claude.ai/chat/[LINK_TO_CURRENT_SESSION]  
**Status:** 18/28 dokumentov dokončených, **10 zostáva**

---

## ⚠️ KRITICKÉ: COLLABORATION RULES

**MUSÍŠ dodržiavať 22 pravidiel z memory_user_edits!**

Kľúčové pravidlá pre túto session:
- **Rule #7:** CRITICAL artifacts pre všetky dokumenty/kód
- **Rule #8:** Step-by-step, confirmation pred pokračovaním
- **Rule #20:** "novy chat" = **3 artifacts** (SESSION_ARCHIVE, INIT, commit)
- **Rule #5:** Slovak language, presná terminológia projektov
- **Rule #22:** Na začiatku každého chatu skontrolovať všetky pravidlá

---

## ✅ ČO SME DOKONČILI V PREVIOUS SESSIONS

### Partners Section - COMPLETE! (8 dokumentov)

1. BANKLST-bank_catalog.md
2. PAB-partner_catalog.md
3. PABACC-partner_catalog_bank_accounts.md
4. PACNCT-partner_catalog_contacts.md
5. PAGLST-partner_categories.md
6. PAYLST-payment_methods.md
7. TRPLST-transport_methods.md
8. PANOTI-partner_catalog_texts.md
9. PASUBC-partner_catalog_facilities.md

### Products Section - COMPLETE! (5 dokumentov)

1. BARCODE-product_catalog_identifiers.md (24.2 KB → 10.5 KB, 56.6%)
2. FGLST-product_categories.md (16.1 KB → 7.0 KB, 56.5%)
3. GSCAT-product_catalog.md (20.7 KB → 10.5 KB, 49.3%)
4. MGLST-product_categories.md (17.4 KB → 7.5 KB, 56.9%)
5. SGLST-product_categories.md (20.1 KB → 8.5 KB, 57.7%)

### Stock Management Section - PARTIAL! (5/7 dokumentov)

1. **WRILST-facilities.md** (17.9 KB → 7.7 KB, 57%) ✅
2. **STKLST-stocks.md** (20.4 KB → 8.7 KB, 57%) ✅
3. **TSH-supplier_delivery_heads.md** (25.4 KB → 11.2 KB, 56%) ✅
4. **FIF-stock_card_fifos.md** (28.5 KB → 11.8 KB, 59%) ✅
5. **TSI-supplier_delivery_items.md** (29.7 KB → 12.5 KB, 58%) ✅

---

## 📊 PROGRESS

**Dokončené:** 18/28 dokumentov (64.3%)  
**Zostáva:** 10 database table dokumentov

**By Category:**
- ✅ **Partners:** 8/8 (100%) - **COMPLETE**
- ✅ **Products:** 5/5 (100%) - **COMPLETE**
- ⏳ **Stock Management:** 5/7 (71.4%) - **PARTIAL**
- ⏳ **Accounting:** 0/3 (0%)
- ⏳ **Sales:** 0/1 (0%)

**Priemerná redukcia:** 57.4% veľkosti

---

## 🎯 ČO TREBA UROBIŤ TERAZ

### Priority 1: Stock Management - Dokončiť (2 dokumenty)

**Odporúčané poradie (veľké dokumenty!):**

1. **STM-stock_card_movements.md-old** (35.6 KB) ⚠️ VEĽKÉ ← **ZAČNI TÝMTO**
   - Skladové pohyby (príjmy/výdaje)
   - Prepojenie s FIFO kartami
   - Multi-file architektúra (STMnnnnn.BTR)

2. **STK-stock_cards.md-old** (38.5 KB) ⚠️ NAJVÄČŠÍ
   - Skladové karty (master data)
   - Bilancie, FIFO ceny
   - Multi-file architektúra (STKnnnnn.BTR)

**Všetky pravdepodobne v adresári STORES** (overiť pri každom).

---

## 📂 ZOSTÁVAJÚCE DOKUMENTY (10 total)

### Stock Management (2 súbory - dokončiť)

- **STM-stock_card_movements.md-old** (35.6 KB) ⚠️ VEĽKÉ
- **STK-stock_cards.md-old** (38.5 KB) ⚠️ NAJVÄČŠÍ

### Accounting (3 súbory - nové)

- ISH-supplier_invoice_heads.md-old (34.8 KB)
- ISI-supplier_invoice_items.md-old (29.6 KB)
- PAYJRN-payment_journal.md-old (25.8 KB)

### Sales (1 súbor - nový)

- PLSnnnnn-price_list_items.md-old (20.5 KB)

---

## 🔧 KRITICKÉ TECHNICKÉ INFO

### Overený Workflow

1. **web_fetch** - načítať .md-old z GitHubu
2. **Opýtať sa na Btrieve location** (user poskytne adresár)
3. **Vytvoriť 1 artifact** - vyčistený dokument
4. **User skopíruje obsah + zmaže starý súbor** - manuálne
5. **Pokračuj ďalším dokumentom**

### Zistené Btrieve Locations

**DIALS adresár:**
- BANKLST.BTR, PAB.BTR, PABACC.BTR, PACNCT.BTR
- PAGLST.BTR, PAYLST.BTR, TRPLST.BTR
- PANOTI.BTR, PASUBC.BTR

**STORES adresár:**
- BARCODE.BTR, FGLST.BTR, GSCAT.BTR, MGLST.BTR, SGLST.BTR
- WRILST.BTR, STKLST.BTR
- TSH[YY][NNN].BTR (TSH25001.BTR, TSH25002.BTR, ...)
- TSI[YY][NNN].BTR (TSI25001.BTR, TSI25002.BTR, ...)
- FIF[NNNNN].BTR (FIF00001.BTR, FIF00002.BTR, ...)
- **Pravdepodobne aj:** STM[NNNNN].BTR, STK[NNNNN].BTR (overiť!)

### Formát Úprav (konzistentný)

**PRIDÁVAME:**
- Btrieve súbor info:
  ```markdown
  ### Btrieve súbor
  - **Názov:** [FILE].BTR
  - **Umiestnenie:** `C:\NEX\YEARACT\[DIR]\[FILE].BTR`
    - Premenná časť: `C:\NEX\` (root path)
    - Fixná časť: `\YEARACT\[DIR]\`
  - **Účel:** [popis]
  ```
- Aktualizované metadáta (dátum: 2025-12-15)
- Status: ✅ Pripravené na migráciu
- Batch info: "Batch 6 (Stock Management - dokumenty X/Y)"

**ODSTRAŇUJEME:**
- CREATE TABLE statements
- CREATE INDEX statements
- CREATE TRIGGER statements
- CREATE FUNCTION statements
- Query patterns (veľké SQL bloky)
- Python migration code (komplexné funkcie)
- Veľké INSERT príklady

**ZACHOVÁVAME:**
- Mapping polí (Btrieve → PostgreSQL)
- Biznis logika (koncepčný popis)
- Vzťahy s inými tabuľkami (popis)
- Validačné pravidlá (koncepčný popis)
- Poznámky pre migráciu (koncepčné, BEZ kódu)
- Malé príklady dát (ukážkové INSERT)

### Priemerná Redukcia

**57.4% veľkosti** (overené na 18 dokumentoch)
- Partners: 49-58%
- Products: 49-58%
- Stock Management (5 docs): 56-59%
- Expected pre STM/STK: podobné

---

## 💡 KRITICKÉ POZNÁMKY PRE MIGRÁCIU

### 1. Multi-file Btrieve Architektúra

**Špeciálne prípady:**

**TSH/TSI** (Supplier Delivery Documents):
- Btrieve: TSH25001.BTR, TSH25002.BTR (kniha+rok)
- PostgreSQL: supplier_delivery_heads (jedna tabuľka)
- Extrahovať book_num z názvu súboru

**FIF** (FIFO Cards):
- Btrieve: FIF00001.BTR, FIF00002.BTR (per sklad)
- PostgreSQL: stock_card_fifos (jedna tabuľka + stock_id)
- Extrahovať stock_id z názvu súboru

**STM/STK** (Stock Movements/Cards):
- Btrieve: STMnnnnn.BTR, STKnnnnn.BTR (per sklad)
- PostgreSQL: stock_card_movements, stock_cards (jedna tabuľka + stock_id)
- Extrahovať stock_id z názvu súboru

### 2. Versioning Systém

**Partners (v documents):**
- supplier_id + supplier_modify_id
- History: partner_catalog_history
- Pri migrácii: modify_id = 0

**Products (v documents):**
- product_id + product_modify_id
- History: product_catalog_history
- Pri migrácii: modify_id = 0

### 3. FIFO Logika (pre STM/STK)

**FIFO Princíp:**
- Výdaj vždy z najstaršej aktívnej karty
- ORDER BY document_date ASC, fifo_id ASC
- Ak výdaj > zostatok → rozdeliť na viacero movements

**Stavy:**
- A (Active) - aktívna karta
- W (Waiting) - čaká na rad
- X (eXhausted) - spotrebovaná

### 4. NSO (Náklady súvisiace s obstaraním)

**Koncept:**
- NSO sa zadávajú v hlavičke (TSH)
- Automaticky sa rozdeľujú na položky (TSI) aliquotne
- OC = NC + NSO
- Detail rozdelenia už je v TSI dokumentácii

---

## 📈 SUCCESS METRICS

**Pre túto session očakávame:**
- ✅ 2 Stock Management dokumenty dokončené (STM, STK)
- ✅ Progress: 20/28 súborov (71.4%)
- ✅ Konzistentný štýl s predchádzajúcimi dokumentmi
- ✅ Priemerná redukcia ~57%

**Estimated time:** 90-120 minút (veľké dokumenty!)

---

## 🎯 DECISION FRAMEWORK QUICK REFERENCE

| Typ dokumentu | Rozhodnutie | Príklad |
|---------------|-------------|---------|
| Database table mapping | CLEAN + KEEP | Všetky .md-old v batch 6 |
| SQL scripts | REMOVE | CREATE TABLE, INDEX, TRIGGER |
| Python migration code | REMOVE | Veľké bloky kódu |
| Mapping tables | KEEP | Btrieve → PostgreSQL |
| Biznis logika | KEEP | Koncepčný popis |
| Query patterns | REMOVE | Mnoho SQL SELECT blokov |
| Príklady dát | KEEP MINIMAL | Malé ukážkové INSERT |

---

## 📝 DOKUMENTAČNÉ ŠTANDARDY

### Documentation Manifest Location

```
C:\Development\nex-automat\SESSION_NOTES\docs.json
```

### GitHub Raw URL Pattern

```
https://raw.githubusercontent.com/rauschiccsk/nex-automat/develop/docs/architecture/database/[path]
```

**Stock Management paths:**
```
docs/architecture/database/stock/cards/tables/
docs/architecture/database/stock/documents/tables/
```

**Accounting paths (pre budúce dokumenty):**
```
docs/architecture/database/accounting/tables/
```

**Sales paths (pre budúce dokumenty):**
```
docs/architecture/database/sales/tables/
```

---

## ⚡ WORKFLOW BEST PRACTICES

### Overený Proces (funguje dobre)

1. **Načítaj dokument** (web_fetch)
2. **Opýtaj sa na Btrieve location** (user poskytne adresár)
3. **Vytvor upravený dokument** (artifact)
4. **User skopíruje obsah + zmaže starý súbor**
5. **Pokračuj ďalším dokumentom**

### Komunikácia

✅ **Stručne** - žiadny verbose output  
✅ **Akcie** - artifacts, konkrétne kroky  
✅ **Čakanie** - po každom artifacte čakať na potvrdenie  
✅ **Progress** - token stats na konci každej odpovede

---

## 🚀 IMMEDIATE ACTION

**Prvý krok po načítaní tohto promptu:**

1. Skontroluj memory_user_edits (22 pravidiel) ✅
2. Načítaj **STM-stock_card_movements.md-old** z GitHubu
3. Opýtaj sa: "V akom adresári sú STM súbory?"
4. Po odpovedi vytvor artifact s vyčisteným dokumentom
5. Čakaj na potvrdenie a pokračuj STK

**Odporúčaný workflow pre session:**
1. **STM-stock_card_movements.md-old** (35.6 KB) - veľký, zložitý
2. **STK-stock_cards.md-old** (38.5 KB) - najväčší, master data
3. Ak zostane čas: začni Accounting sekciu (ISH)

---

## 📋 GIT WORKFLOW (user robí manuálne)

```powershell
# Git workflow
git status
git add docs/
git commit -m "docs: Database table docs batch 6 - stock management complete + start accounting (N docs)"
git push origin develop

# Generate manifests
python tools/generate_manifests.py
```

---

## 🔗 SÚVISIACE DOKUMENTY

**Already processed (reference):**
- docs/architecture/database/stock/cards/tables/WRILST-facilities.md
- docs/architecture/database/stock/cards/tables/STKLST-stocks.md
- docs/architecture/database/stock/documents/tables/TSH-supplier_delivery_heads.md
- docs/architecture/database/stock/cards/tables/FIF-stock_card_fifos.md
- docs/architecture/database/stock/documents/tables/TSI-supplier_delivery_items.md

**To be processed:**
- docs/architecture/database/stock/cards/tables/STM-stock_card_movements.md-old
- docs/architecture/database/stock/cards/tables/STK-stock_cards.md-old

**Reference documents:**
- docs/COLLABORATION_RULES.md (22 pravidiel)
- docs/architecture/database/COMMON_DOCUMENT_PRINCIPLES.md (všeobecné zásady)
- docs/archive/00_ARCHIVE_INDEX.md (update po session)

---

## ⚠️ ŠPECIÁLNE UPOZORNENIA

### Pre STM (Stock Card Movements)

**Očakávané vlastnosti:**
- Multi-file architektúra (STMnnnnn.BTR per sklad)
- Veľký počet záznamov (všetky pohyby)
- Prepojenie s FIFO kartami (fifo_id)
- Typy pohybov (príjem/výdaj/transfer)
- Dokumentové odkazy (source_document_type, source_item_id)

**Kľúčové mapping polia:**
- MovNum → movement_id
- GsCode → product_id
- StkNum → stock_id (z názvu súboru)
- MovQnt → quantity (+/- podľa typu)
- FifNum → fifo_id (pre výdaje)

### Pre STK (Stock Cards)

**Očakávané vlastnosti:**
- Multi-file architektúra (STKnnnnn.BTR per sklad)
- Master data pre produkt na sklade
- Bilancie (quantity_on_hand, value_total)
- FIFO ceny (current_fifo_price)
- Rezervácie (quantity_reserved)

**Kľúčové mapping polia:**
- GsCode → product_id
- StkNum → stock_id (z názvu súboru)
- ActQnt → quantity_on_hand
- ActVal → value_total
- FifPrice → current_fifo_price

---

**Token Budget:** 190,000  
**Estimated Session:** 90-120 minút (veľké dokumenty!)  
**Ready to Continue:** ✅ ÁNO

---

**KONIEC INIT PROMPTU**