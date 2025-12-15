# INIT PROMPT - NEX Automat: Database Table Docs Migration (Batch 6 - Accounting Start)

**Projekt:** nex-automat  
**Úloha:** Database table docs migration (batch 6 - Accounting section)  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** https://claude.ai/chat/[LINK_TO_CURRENT_SESSION]  
**Status:** 20/28 dokumentov dokončených, **8 zostáva**

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

### Stock Management Section - COMPLETE! (7 dokumentov) ⭐

1. **WRILST-facilities.md** (17.9 KB → 7.7 KB, 57%) ✅
2. **STKLST-stocks.md** (20.4 KB → 8.7 KB, 57%) ✅
3. **TSH-supplier_delivery_heads.md** (25.4 KB → 11.2 KB, 56%) ✅
4. **FIF-stock_card_fifos.md** (28.5 KB → 11.8 KB, 59%) ✅
5. **TSI-supplier_delivery_items.md** (29.7 KB → 12.5 KB, 58%) ✅
6. **STM-stock_card_movements.md** (35.6 KB → 15.3 KB, 57%) ✅
7. **STK-stock_cards.md** (38.5 KB → 16.5 KB, 57%) ✅

---

## 📊 PROGRESS

**Dokončené:** 20/28 dokumentov (71.4%)  
**Zostáva:** 8 database table dokumentov

**By Category:**
- ✅ **Partners:** 8/8 (100%) - **COMPLETE**
- ✅ **Products:** 5/5 (100%) - **COMPLETE**
- ✅ **Stock Management:** 7/7 (100%) - **COMPLETE**
- ⏳ **Accounting:** 0/3 (0%) ← **START HERE**
- ⏳ **Sales:** 0/1 (0%)

**Priemerná redukcia:** 57.4% veľkosti

---

## 🎯 ČO TREBA UROBIŤ TERAZ

### Priority 1: Accounting Section - Začať (3 dokumenty)

**Odporúčané poradie:**

1. **ISH-supplier_invoice_heads.md-old** (34.8 KB) ⚠️ VEĽKÉ ← **ZAČNI TÝMTO**
   - Hlavičky dodávateľských faktúr
   - Prepojenie s TSH (dodacie listy)
   - Multi-file architektúra? (ISH[YY][NNN].BTR? - overiť pri načítaní)

2. **ISI-supplier_invoice_items.md-old** (29.6 KB) ⚠️ VEĽKÉ
   - Položky dodávateľských faktúr
   - Prepojenie s TSI (položky dodacích listov)
   - Multi-file architektúra? (ISI[YY][NNN].BTR? - overiť pri načítaní)

3. **PAYJRN-payment_journal.md-old** (25.8 KB)
   - Platobný denník
   - Prepojenie s ISH (úhrady faktúr)
   - Pravdepodobne: C:\NEX\YEARACT\ACCOUNTS\

**Pravdepodobné Btrieve adresáre:**
- ACCOUNTS (faktúry, platby)
- STORES (ak súvisí s TSH/TSI)

---

## 📂 ZOSTÁVAJÚCE DOKUMENTY (8 total)

### Accounting (3 súbory - START HERE)

- **ISH-supplier_invoice_heads.md-old** (34.8 KB) ⚠️ VEĽKÉ
- **ISI-supplier_invoice_items.md-old** (29.6 KB) ⚠️ VEĽKÉ
- **PAYJRN-payment_journal.md-old** (25.8 KB)

### Sales (1 súbor)

- PLSnnnnn-price_list_items.md-old (20.5 KB)

### Ostatné (4 súbory - TBD)

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
- TSH[YY][NNN].BTR, TSI[YY][NNN].BTR
- FIF[NNNNN].BTR, STM[NNNNN].BTR, STK[NNNNN].BTR
- **Možno aj:** ISH[YY][NNN].BTR, ISI[YY][NNN].BTR (overiť!)

**ACCOUNTS adresár (pravdepodobne):**
- PAYJRN.BTR (platobný denník)
- **Možno aj:** ISH[YY][NNN].BTR, ISI[YY][NNN].BTR (overiť!)

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
- Batch info: "Batch 6 (Accounting - dokument X/Y)"

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

**57.4% veľkosti** (overené na 20 dokumentoch)
- Partners: 49-58%
- Products: 49-58%
- Stock Management: 56-59%
- Expected pre Accounting: podobné

---

## 💡 KRITICKÉ POZNÁMKY PRE MIGRÁCIU

### 1. Multi-file Btrieve Architektúra

**Špeciálne prípady v Stock Management (reference):**

**TSH/TSI** (Supplier Delivery Documents):
- Btrieve: TSH25001.BTR, TSH25002.BTR (kniha+rok)
- PostgreSQL: supplier_delivery_heads (jedna tabuľka)
- Extrahovať book_num z názvu súboru

**FIF/STM/STK** (FIFO/Movements/Cards):
- Btrieve: FIF00001.BTR, STM00001.BTR, STK00001.BTR (per sklad)
- PostgreSQL: jedna tabuľka + stock_id
- Extrahovať stock_id z názvu súboru

**ISH/ISI** (Supplier Invoices - TBD):
- Pravdepodobne: ISH[YY][NNN].BTR, ISI[YY][NNN].BTR (kniha+rok?)
- Alebo: ISH.BTR, ISI.BTR (single file?)
- **Overiť pri načítaní dokumentu!**

### 2. Prepojenia Accounting s Stock Management

**ISH/ISI ↔ TSH/TSI:**
- Faktúra môže byť vytvorená z dodacieho listu
- Prepojenie cez document_number alebo delivery_id
- Poznámka: Detail prepojenia v ISH/ISI dokumentoch

**PAYJRN ↔ ISH:**
- Úhrady faktúr v platobnom denníku
- Prepojenie cez invoice_id alebo document_number
- Poznámka: Detail prepojenia v PAYJRN dokumente

### 3. Versioning Systém

**Partners (v documents):**
- supplier_id + supplier_modify_id
- History: partner_catalog_history
- Pri migrácii: modify_id = 0

**Products (v documents):**
- product_id + product_modify_id
- History: product_catalog_history
- Pri migrácii: modify_id = 0

**Accounting documents (TBD):**
- Pravdepodobne: invoice_id + invoice_modify_id?
- **Overiť pri načítaní dokumentu!**

---

## 📈 SUCCESS METRICS

**Pre túto session očakávame:**
- ✅ 3 Accounting dokumenty dokončené (ISH, ISI, PAYJRN)
- ✅ Progress: 23/28 súborov (82.1%)
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

**Accounting paths:**
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
2. Načítaj **ISH-supplier_invoice_heads.md-old** z GitHubu
3. Opýtaj sa: "V akom adresári sú ISH súbory?"
4. Po odpovedi vytvor artifact s vyčisteným dokumentom
5. Čakaj na potvrdenie a pokračuj ISI

**Odporúčaný workflow pre session:**
1. **ISH-supplier_invoice_heads.md-old** (34.8 KB) - veľký, hlavičky
2. **ISI-supplier_invoice_items.md-old** (29.6 KB) - veľký, položky
3. **PAYJRN-payment_journal.md-old** (25.8 KB) - platby
4. Ak zostane čas: začni Sales sekciu (PLSnnnnn)

---

## 📋 GIT WORKFLOW (user robí manuálne)

```powershell
# Git workflow
git status
git add docs/
git commit -m "docs: Database table docs batch 6 - accounting section (N docs)"
git push origin develop

# Generate manifests
python tools/generate_manifests.py
```

---

## 🔗 SÚVISIACE DOKUMENTY

**Already processed (reference):**
- docs/architecture/database/stock/cards/tables/STM-stock_card_movements.md
- docs/architecture/database/stock/cards/tables/STK-stock_cards.md
- docs/architecture/database/stock/documents/tables/TSH-supplier_delivery_heads.md
- docs/architecture/database/stock/documents/tables/TSI-supplier_delivery_items.md

**To be processed:**
- docs/architecture/database/accounting/tables/ISH-supplier_invoice_heads.md-old
- docs/architecture/database/accounting/tables/ISI-supplier_invoice_items.md-old
- docs/architecture/database/accounting/tables/PAYJRN-payment_journal.md-old

**Reference documents:**
- docs/COLLABORATION_RULES.md (22 pravidiel)
- docs/archive/00_ARCHIVE_INDEX.md (update po session)

---

## ⚠️ ŠPECIÁLNE UPOZORNENIA

### Pre ISH (Supplier Invoice Heads)

**Očakávané vlastnosti:**
- Hlavičky faktúr od dodávateľov
- Prepojenie s TSH (dodacie listy)
- Prepojenie s PAB (dodávatelia)
- Prepojenie s PAYLST/TRPLST (platba/doprava)
- Multi-file architektúra? (ISH[YY][NNN].BTR? - overiť)
- Sleduje DPH, úhrady, stav faktúry

**Kľúčové mapping polia (očakávané):**
- InvNum → invoice_id
- PaCode → supplier_id (FK na partners)
- DocNum → document_number
- InvDate → invoice_date
- DueDate → due_date
- TotalVal → total_value
- VatVal → vat_value
- PaidVal → paid_value
- InvStat → invoice_status

### Pre ISI (Supplier Invoice Items)

**Očakávané vlastnosti:**
- Položky faktúr od dodávateľov
- Prepojenie s ISH (hlavička faktúry)
- Prepojenie s TSI (položky dodacích listov)
- Prepojenie s GSCAT (produkty)
- Multi-file architektúra? (ISI[YY][NNN].BTR? - overiť)
- Sleduje množstvo, cenu, DPH, zľavu

**Kľúčové mapping polia (očakávané):**
- InvNum → invoice_id
- ItmNum → item_line_number
- GsCode → product_id (FK na products)
- Quantity → quantity
- UnitPrice → unit_price
- VatRate → vat_rate
- NetVal → net_value
- VatVal → vat_value

### Pre PAYJRN (Payment Journal)

**Očakávané vlastnosti:**
- Platobný denník (všetky úhrady)
- Prepojenie s ISH (úhrady faktúr)
- Prepojenie s PAB (dodávatelia/odberatelia)
- Pravdepodobne single file: PAYJRN.BTR
- Sleduje typ platby, dátum, hodnotu, stav

**Kľúčové mapping polia (očakávané):**
- PayNum → payment_id
- PayDate → payment_date
- PaCode → partner_id (FK na partners)
- InvNum → invoice_id (FK na ISH)
- PayVal → payment_value
- PayType → payment_type_code
- PayStat → payment_status

---

**Token Budget:** 190,000  
**Estimated Session:** 90-120 minút (veľké dokumenty!)  
**Ready to Start:** ✅ ÁNO

---

**KONIEC INIT PROMPTU**