# INIT PROMPT - NEX Automat: Database Table Docs Migration (Batch 6 Continue)

**Projekt:** nex-automat  
**Úloha:** Database table docs migration (batch 6 continuation - Stock Management section)  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** https://claude.ai/chat/[PREVIOUS_CHAT_URI]  
**Status:** 13/28 dokumentov dokončených, **15 zostáva**

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

1. **BANKLST-bank_catalog.md** (script #32)
2. **PAB-partner_catalog.md** (script #33)
3. **PABACC-partner_catalog_bank_accounts.md** (script #34)
4. **PACNCT-partner_catalog_contacts.md** (script #35)
5. **PAGLST-partner_categories.md** (14.9 KB → 7.0 KB, 53%)
6. **PAYLST-payment_methods.md** (8.3 KB → 4.2 KB, 49%)
7. **TRPLST-transport_methods.md** (8.6 KB → 4.3 KB, 50%)
8. **PANOTI-partner_catalog_texts.md** (15.4 KB → 6.5 KB, 58%)
9. **PASUBC-partner_catalog_facilities.md** (18.0 KB → 7.5 KB, 58%)

### Products Section - COMPLETE! (5 dokumentov)

1. **BARCODE-product_catalog_identifiers.md** (24.2 KB → 10.5 KB, 56.6%)
2. **FGLST-product_categories.md** (16.1 KB → 7.0 KB, 56.5%)
3. **GSCAT-product_catalog.md** (20.7 KB → 10.5 KB, 49.3%)
4. **MGLST-product_categories.md** (17.4 KB → 7.5 KB, 56.9%)
5. **SGLST-product_categories.md** (20.1 KB → 8.5 KB, 57.7%)

---

## 📊 PROGRESS

**Dokončené:** 13/28 dokumentov (46.4%)  
**Zostáva:** 15 database table dokumentov

**By Category:**
- ✅ **Partners:** 8/8 (100%) - **COMPLETE**
- ✅ **Products:** 5/5 (100%) - **COMPLETE**
- ⏳ **Stock Management:** 0/7 (0%)
- ⏳ **Accounting:** 0/3 (0%)
- ⏳ **Sales:** 0/1 (0%)

---

## 🎯 ČO TREBA UROBIŤ TERAZ

### Priority 1: Stock Management Section (START HERE!)

**Odporúčané poradie (menšie → väčšie):**

1. **WRILST-facilities.md-old** (17.9 KB) ← **ZAČNI TÝMTO**
2. **STKLST-stocks.md-old** (20.4 KB)
3. **TSH-supplier_delivery_heads.md-old** (25.4 KB)
4. **FIF-stock_card_fifos.md-old** (28.5 KB)
5. **TSI-supplier_delivery_items.md-old** (29.7 KB)
6. **STM-stock_card_movements.md-old** (35.6 KB) ⚠️ VEĽKÝ
7. **STK-stock_cards.md-old** (38.5 KB) ⚠️ VEĽKÝ

**Všetky pravdepodobne v adresári STORES** (overiť pri každom).

---

## 📂 ZOSTÁVAJÚCE DOKUMENTY (15 total)

### Stock Management (7 súborov)

- WRILST-facilities.md-old (17.9 KB)
- STKLST-stocks.md-old (20.4 KB)
- TSH-supplier_delivery_heads.md-old (25.4 KB)
- FIF-stock_card_fifos.md-old (28.5 KB)
- TSI-supplier_delivery_items.md-old (29.7 KB)
- STM-stock_card_movements.md-old (35.6 KB) ⚠️ VEĽKÝ
- STK-stock_cards.md-old (38.5 KB) ⚠️ VEĽKÝ

### Accounting (3 súbory)

- ISH-supplier_invoice_heads.md-old (34.8 KB)
- ISI-supplier_invoice_items.md-old (29.6 KB)
- PAYJRN-payment_journal.md-old (25.8 KB)

### Sales (1 súbor)

- PLSnnnnn-price_list_items.md-old (20.5 KB)

---

## 🔧 KRITICKÉ TECHNICKÉ INFO

### Overený Workflow

1. **web_fetch** - načítať .md-old z GitHubu
2. **Opýtať sa na Btrieve location** (user poskytne adresár)
3. **Vytvoriť 1 artifact** - vyčistený dokument
4. **User skopíruje obsah + zmaže starý súbor** - manuálne
5. **Pokračuj ďalším dokumentom**

### Btrieve Locations (zistené doteraz)

**DIALS adresár:**
- BANKLST.BTR, PAB.BTR, PABACC.BTR, PACNCT.BTR
- PAGLST.BTR, PAYLST.BTR, TRPLST.BTR
- PANOTI.BTR, PASUBC.BTR

**STORES adresár:**
- BARCODE.BTR, FGLST.BTR, GSCAT.BTR, MGLST.BTR, SGLST.BTR
- Pravdepodobne aj všetky Stock Management súbory (overiť!)

### Formát Úprav (konzistentný)

**Pridávame:**
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

**Odstraňujeme:**
- CREATE TABLE statements
- CREATE INDEX statements
- CREATE TRIGGER statements
- CREATE FUNCTION statements
- Query patterns (veľké SQL bloky)
- Python migration code
- Veľké INSERT príklady

**Zachovávame:**
- Mapping polí (Btrieve → PostgreSQL)
- Biznis logika (koncepčný popis)
- Vzťahy s inými tabuľkami (popis)
- Validačné pravidlá (koncepčný popis)
- Poznámky pre migráciu (koncepčné, BEZ kódu)
- Malé príklady dát (ukážkové)

### Priemerná Redukcia

**53.6% veľkosti** (overené na 13 dokumentoch)
- Partners: 49-58%
- Products: 49-58%
- Expected pre Stock Management: podobné

---

## 💡 KRITICKÉ POZNÁMKY PRE MIGRÁCIU

### 1. Audit Polia Pattern (štandard všade)

**created_by/created_at:**
- Kto a kedy vytvoril záznam (nemenné)
- Pri migrácii: CrtUser/CrtDate/CrtTime
- Ak neexistuje: 'MIGRATION' + CURRENT_TIMESTAMP

**updated_by/updated_at:**
- Kto a kedy naposledy modifikoval (aktualizuje sa pri zmene)
- Pri migrácii: ModUser/ModDate/ModTime
- Ak neexistuje: použiť CrtUser alebo 'MIGRATION'

### 2. Mapping Dictionary Pattern (pre číselníky)

Pri migrácii závislých tabuliek:
1. Najprv migrovať číselník
2. Vytvoriť mapping dictionary (Code → ID)
3. Použiť pri migrácii hlavnej tabuľky

### 3. Stock Management Specific Notes

**FIFO záznamy (FIF):**
- Sledovanie prijatých šarží produktov
- Väzba na stock cards (STK)

**Stock Movements (STM):**
- Veľký počet záznamov (všetky pohyby)
- Potrebné indexy pre performance

**Facilities (WRILST):**
- Číselník skladov/oddelení
- Base table pre STKLST

---

## 📁 DOKUMENTAČNÉ ŠTANDARDY

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
2. Načítaj **WRILST-facilities.md-old** z GitHubu
3. Opýtaj sa: "V akom adresári je WRILST.BTR?"
4. Po odpovedi vytvor artifact s vyčisteným dokumentom
5. Čakaj na potvrdenie a pokračuj STKLST

**Odporúčaný workflow pre session:**
1. **WRILST-facilities.md-old** (17.9 KB) - menší, dobrý na rozbeh
2. **STKLST-stocks.md-old** (20.4 KB)
3. **TSH-supplier_delivery_heads.md-old** (25.4 KB)
4. Podľa času a tokenov pokračovať ďalšími

---

## 📈 SUCCESS METRICS

**Pre túto session očakávame:**
- ✅ 3-5 Stock Management dokumentov dokončených
- ✅ Progress: 16-18/28 súborov (57-64%)
- ✅ Konzistentný štýl s predchádzajúcimi dokumentmi

**Estimated time:** 90-120 minút

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

## 📝 GIT WORKFLOW (user robí manuálne)

```powershell
# Git workflow
git status
git add docs/
git commit -m "docs: Database table docs batch 6 - stock management (N docs)"
git push origin develop

# Generate manifests
python tools/generate_manifests.py
```

---

**Token Budget:** 190,000  
**Estimated Session:** 90-120 minút  
**Ready to Continue:** ✅ ÁNO

---

**KONIEC INIT PROMPTU**