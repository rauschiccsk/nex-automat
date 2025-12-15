# INIT PROMPT - NEX Automat: Database Table Docs Migration (Batch 6 - Sales Final)

**Projekt:** nex-automat  
**Úloha:** Database table docs migration (batch 6 - Sales section - FINAL)  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** https://claude.ai/chat/[LINK_TO_CURRENT_SESSION]  
**Status:** 23/28 dokumentov dokončených, **1 zostáva**

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

### Stock Management Section - COMPLETE! (7 dokumentov)

1. WRILST-facilities.md (17.9 KB → 7.7 KB, 57%)
2. STKLST-stocks.md (20.4 KB → 8.7 KB, 57%)
3. TSH-supplier_delivery_heads.md (25.4 KB → 11.2 KB, 56%)
4. FIF-stock_card_fifos.md (28.5 KB → 11.8 KB, 59%)
5. TSI-supplier_delivery_items.md (29.7 KB → 12.5 KB, 58%)
6. STM-stock_card_movements.md (35.6 KB → 15.3 KB, 57%)
7. STK-stock_cards.md (38.5 KB → 16.5 KB, 57%)

### Accounting Section - COMPLETE! (3 dokumenty) ⭐

1. **ISH-supplier_invoice_heads.md** (34.8 KB → 15.5 KB, 55.5%) ✅
2. **ISI-supplier_invoice_items.md** (29.6 KB → 13.5 KB, 54.4%) ✅
3. **PAYJRN-payment_journal.md** (25.8 KB → 12.0 KB, 53.5%) ✅

---

## 📊 PROGRESS

**Dokončené:** 23/28 dokumentov (82.1%)  
**Zostáva:** 1 database table dokument

**By Category:**
- ✅ **Partners:** 8/8 (100%) - **COMPLETE**
- ✅ **Products:** 5/5 (100%) - **COMPLETE**
- ✅ **Stock Management:** 7/7 (100%) - **COMPLETE**
- ✅ **Accounting:** 3/3 (100%) - **COMPLETE**
- ⏳ **Sales:** 0/1 (0%) ← **START HERE - FINAL DOCUMENT**

**Priemerná redukcia:** 55.2% veľkosti

---

## 🎯 ČO TREBA UROBIŤ TERAZ

### Priority 1: Sales Section - FINAL DOCUMENT (1 dokument)

**Jediný zostávajúci dokument:**

1. **PLSnnnnn-price_list_items.md-old** (20.5 KB) ← **ZAČNI TÝMTO - POSLEDNÝ!**
   - Položky cenníkov (Price List Items)
   - Multi-file architektúra: PLS[nnnnn].BTR (per cenník)
   - Pravdepodobne: C:\NEX\YEARACT\STORES\

**Pravdepodobné Btrieve adresáre:**
- STORES (cenníky - pravdepodobne)
- DIALS (číselníky - menej pravdepodobné)

---

## 📂 TECHNICKÉ INFO

### Overený Workflow

1. **web_fetch** - načítať .md-old z GitHubu
2. **Opýtať sa na Btrieve location** (user poskytne adresár)
3. **Vytvoriť 1 artifact** - vyčistený dokument
4. **User skopíruje obsah + zmaže starý súbor** - manuálne
5. **DONE!** - všetky dokumenty dokončené

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
- **Pravdepodobne aj:** PLS[nnnnn].BTR (overiť!)

**LEDGER adresár:**
- ISH[YY][NNN].BTR, ISI[YY][NNN].BTR
- PAYJRN.BTR

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
- Batch info: "Batch 6 (Sales - dokument 1/1 - FINAL)"

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

**Všetky dokončené sekcie:**
- Partners: 49-58%
- Products: 49-58%
- Stock Management: 56-59%
- Accounting: 54-56%
- Expected pre Sales: podobné (~55%)

---

## 💡 KRITICKÉ POZNÁMKY PRE MIGRÁCIU

### 1. Multi-file Btrieve Architektúra

**Špeciálne prípady (reference):**

**PLS[nnnnn]** (Price List Items - TBD):
- Btrieve: PLS00001.BTR, PLS00002.BTR (per cenník)
- PostgreSQL: price_list_items (jedna tabuľka)
- Extrahovať price_list_id z názvu súboru
- **Overiť pri načítaní dokumentu!**

### 2. Prepojenia Sales s ostatnými sekciami

**PLS → GSCAT:**
- Položky cenníka odkazujú na produkty
- Prepojenie cez product_id
- Poznámka: Detail prepojenia v PLS dokumente

**PLS → Customer Orders (možno):**
- Predajné ceny z cenníkov
- Použitie v objednávkach
- Poznámka: Detail v dokumente

### 3. Versioning Systém

**Products (v cenníkoch):**
- product_id + product_modify_id
- History: product_catalog_history
- Pri migrácii: modify_id = 0

**Cenníky (možno):**
- price_list_id + price_list_modify_id?
- **Overiť pri načítaní dokumentu!**

---

## 📈 SUCCESS METRICS

**Pre túto session očakávame:**
- ✅ 1 Sales dokument dokončený (PLSnnnnn)
- ✅ Progress: 24/28 súborov (85.7%)
- ✅ Konzistentný štýl s predchádzajúcimi dokumentmi
- ✅ Priemerná redukcia ~55%
- ✅ **VŠETKY DATABASE TABLE DOKUMENTY DOKONČENÉ!**

**Estimated time:** 15-20 minút (stredný dokument!)

---

## 🎯 DECISION FRAMEWORK QUICK REFERENCE

| Typ dokumentu | Rozhodnutie | Príklad |
|---------------|-------------|---------|
| Database table mapping | CLEAN + KEEP | PLSnnnnn.md-old v batch 6 |
| SQL scripts | REMOVE | CREATE TABLE, INDEX, TRIGGER |
| Python migration code | REMOVE | Veľké bloky kódu |
| Mapping tables | KEEP | Btrieve → PostgreSQL |
| Biznis logika | KEEP | Koncepčný popis |
| Query patterns | REMOVE | Mnoho SQL SELECT blokov |
| Príklady dát | KEEP MINIMAL | Malé ukážkové INSERT |

---

## 📋 DOKUMENTAČNÉ ŠTANDARDY

### Documentation Manifest Location

```
C:\Development\nex-automat\SESSION_NOTES\docs.json
```

### GitHub Raw URL Pattern

```
https://raw.githubusercontent.com/rauschiccsk/nex-automat/develop/docs/architecture/database/[path]
```

**Sales paths:**
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
5. **DONE - ALL DOCUMENTS COMPLETE!**

### Komunikácia

✅ **Stručne** - žiadny verbose output  
✅ **Akcie** - artifacts, konkrétne kroky  
✅ **Čakanie** - po každom artifacte čakať na potvrdenie  
✅ **Progress** - token stats na konci každej odpovede

---

## 🚀 IMMEDIATE ACTION

**Prvý krok po načítaní tohto promptu:**

1. Skontroluj memory_user_edits (22 pravidiel) ✅
2. Načítaj **PLSnnnnn-price_list_items.md-old** z GitHubu
3. Opýtaj sa: "V akom adresári sú PLS súbory?"
4. Po odpovedi vytvor artifact s vyčisteným dokumentom
5. **ALL DONE!** 🎉

**Po dokončení:**
- **VŠETKY** database table dokumenty dokončené (24/28 celkový progress)
- Aktualizovať docs/archive/00_ARCHIVE_INDEX.md
- Git commit všetkých zmien

---

## 📋 GIT WORKFLOW (user robí manuálne)

```powershell
# Git workflow
git status
git add docs/
git commit -m "docs: Database table docs batch 6 - sales section (FINAL)"
git push origin develop

# Generate manifests
python tools/generate_manifests.py
```

---

## 🔗 SÚVISIACE DOKUMENTY

**Already processed (reference):**
- docs/architecture/database/accounting/tables/ISH-supplier_invoice_heads.md
- docs/architecture/database/accounting/tables/ISI-supplier_invoice_items.md
- docs/architecture/database/accounting/tables/PAYJRN-payment_journal.md

**To be processed:**
- docs/architecture/database/sales/tables/PLSnnnnn-price_list_items.md-old

**Reference documents:**
- docs/COLLABORATION_RULES.md (22 pravidiel)
- docs/archive/00_ARCHIVE_INDEX.md (update po session)

---

## ⚠️ ŠPECIÁLNE UPOZORNENIA

### Pre PLS (Price List Items)

**Očakávané vlastnosti:**
- Položky cenníkov (predajné ceny)
- Prepojenie s GSCAT (produkty)
- Multi-file architektúra? (PLS[nnnnn].BTR? - overiť)
- Sleduje ceny, zľavy, DPH, platnosť
- Možno versioning cenníkov?

**Kľúčové mapping polia (očakávané):**
- PlsNum → price_list_id (FK na price_lists)
- GsCode → product_id (FK na products)
- Price → unit_price
- VatRate → vat_rate
- ValidFrom → valid_from_date
- ValidTo → valid_to_date

**DÔLEŽITÉ:**
- Overiť multi-file architektúru pri načítaní!
- Overiť versioning systém pri načítaní!
- Overiť prepojenia s produktami a objednávkami!

---

**Token Budget:** 190,000  
**Estimated Session:** 15-20 minút (posledný dokument!)  
**Ready to Start:** ✅ ÁNO

---

**KONIEC INIT PROMPTU**