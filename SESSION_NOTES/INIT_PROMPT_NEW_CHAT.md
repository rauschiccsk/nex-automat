# INIT PROMPT - NEX Automat: Database Table Docs Migration (Batch 6 Continue)

**Projekt:** nex-automat  
**Úloha:** Database table docs migration (batch 6 continuation - Products section)  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** https://claude.ai/chat/[CURRENT_CHAT_URI]  
**Status:** 8/28 dokumentov dokončených, **20 zostáva**

---

## ⚠️ KRITICKÉ: COLLABORATION RULES

**MUSÍŠ dodržiavať 22 pravidiel z memory_user_edits!**

Kľúčové pravidlá pre túto session:
- **Rule #7:** CRITICAL artifacts pre všetky dokumenty/kód
- **Rule #8:** Step-by-step, confirmation pred pokračovaním
- **Rule #20:** "novy chat" = **3 artifacts** (ARCHIVE, INIT, commit) - **SESSION_NOTES.md ZRUŠENÝ!**
- **Rule #5:** Slovak language, presná terminológia projektov
- **Rule #22:** Na začiatku každého chatu skontrolovať všetky pravidlá

---

## ✅ ČO SME DOKONČILI V PREVIOUS SESSION

### Partners Section - COMPLETE! (8 dokumentov)

1. **PAGLST-partner_categories.md** (14.9 KB → 7.0 KB, 53%)
2. **PAYLST-payment_methods.md** (8.3 KB → 4.2 KB, 49%)
3. **TRPLST-transport_methods.md** (8.6 KB → 4.3 KB, 50%)
4. **PANOTI-partner_catalog_texts.md** (15.4 KB → 6.5 KB, 58%)
5. **PASUBC-partner_catalog_facilities.md** (18.0 KB → 7.5 KB, 58%)

**Plus predchádzajúce:**
- BANKLST-bank_catalog.md (script #32)
- PAB-partner_catalog.md (script #33)
- PABACC-partner_catalog_bank_accounts.md (script #34)
- PACNCT-partner_catalog_contacts.md (script #35)

### Products Section - Started

**BARCODE-product_catalog_identifiers.md-old:**
- Size: 24.2 KB
- Location: STORES (BARCODE.BTR + GSCAT.BTR)
- Status: Načítaný, ready for cleanup

---

## 📊 PROGRESS

**Dokončené:** 8/28 dokumentov (28.6%)  
**Zostáva:** 20 database table dokumentov

**By Category:**
- ✅ **Partners:** 8/8 (100%) - **COMPLETE**
- ⏳ **Products:** 0/5 (0%) - BARCODE loaded
- ⏳ **Stock Management:** 0/7 (0%)
- ⏳ **Accounting:** 0/3 (0%)
- ⏳ **Sales:** 0/1 (0%)

---

## 🎯 ČO TREBA UROBIŤ TERAZ

### Priority 1: Cleanup BARCODE (PRVÉ!)

**BARCODE-product_catalog_identifiers.md-old** (24.2 KB):
- Location: STORES (BARCODE.BTR + GSCAT.BTR)
- Očakávaná redukcia: ~58% (cca 10 KB)
- **User má už dokument načítaný z predchádzajúcej session**

### Priority 2: Pokračovať Products Section

**Zostávajúce Products dokumenty (4):**

1. **FGLST-product_categories.md-old** (16.1 KB)
2. **GSCAT-product_catalog.md-old** (20.7 KB) ⚠️ VEĽKÝ
3. **MGLST-product_categories.md-old** (17.4 KB)
4. **SGLST-product_categories.md-old** (20.1 KB)

**Všetky pravdepodobne v adresári STORES** (overiť pri každom).

---

## 📂 ZOSTÁVAJÚCE DOKUMENTY (20 total)

### Catalogs - Products (5 súborov)

- BARCODE-product_catalog_identifiers.md-old (24.2 KB) ← **TERAZ**
- FGLST-product_categories.md-old (16.1 KB)
- GSCAT-product_catalog.md-old (20.7 KB) ⚠️ VEĽKÝ
- MGLST-product_categories.md-old (17.4 KB)
- SGLST-product_categories.md-old (20.1 KB)

### Stock Management (7 súborov)

- FIF-stock_card_fifos.md-old (28.5 KB)
- STK-stock_cards.md-old (38.5 KB) ⚠️ VEĽKÝ
- STKLST-stocks.md-old (20.4 KB)
- STM-stock_card_movements.md-old (35.6 KB) ⚠️ VEĽKÝ
- WRILST-facilities.md-old (17.9 KB)
- TSH-supplier_delivery_heads.md-old (25.4 KB)
- TSI-supplier_delivery_items.md-old (29.7 KB)

### Accounting (3 súbory)

- ISH-supplier_invoice_heads.md-old (34.8 KB)
- ISI-supplier_invoice_items.md-old (29.6 KB)
- PAYJRN-payment_journal.md-old (25.8 KB)

### Sales (1 súbor)

- PLSnnnnn-price_list_items.md-old (20.5 KB)

---

## 🔧 KRITICKÉ TECHNICKÉ INFO

### Btrieve Locations (zistené)

**DIALS adresár:**
- BANKLST.BTR, PAB.BTR, PABACC.BTR, PACNCT.BTR
- PAGLST.BTR, PAYLST.BTR, TRPLST.BTR
- PANOTI.BTR, PASUBC.BTR

**STORES adresár:**
- BARCODE.BTR
- GSCAT.BTR

**Očakávané:** Väčšina Products súborov pravdepodobne v STORES, ale vždy sa opýtať!

### Formát Úprav

**Pridávame:**
- Popis Btrieve súboru:
  ```markdown
  ### Btrieve súbor
  - **Názov:** [FILE].BTR
  - **Umiestnenie:** `C:\NEX\YEARACT\[DIR]\[FILE].BTR`
    - Premenná časť: `C:\NEX\` (root path)
    - Fixná časť: `\YEARACT\[DIR]\`
  - **Účel:** [popis]
  ```
- Aktualizované metadáta (dátum: 2025-12-15)

**Odstraňujeme:**
- CREATE TABLE statements
- CREATE INDEX statements
- CREATE TRIGGER statements
- CREATE FUNCTION statements
- Query patterns (SQL bloky)
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

**49-58% veľkosti** (overené na 8 dokumentoch)

---

## 💡 KRITICKÉ POZNÁMKY PRE MIGRÁCIU

### 1. bank_code NIE je FK!

**V partner_catalog_bank_accounts:**
- `bank_code` je textová hodnota
- NIE FK constraint na bank_catalog
- Dôvod: denormalizácia, flexibility

### 2. FirstName/LastName SWAP!

**V PACNCT.BTR (partner_catalog_contacts):**
- Btrieve FirstName = priezvisko
- Btrieve LastName = meno
- Pri migrácii MUSÍME swapovať!

### 3. GDPR Compliance

**PACNCT.BTR - NEPRENÁŠAME:**
- Adresa trvalého pobytu
- Doklady totožnosti
- Dátum a miesto narodenia
- Občianstvo

### 4. Mapping Dictionary Pattern

**Pre číselníky (PAGLST, PAYLST, TRPLST):**
- Najprv migrovať číselník
- Vytvoriť mapping dictionary (Code → ID)
- Použiť pri migrácii PAB.BTR

---

## 📝 WORKFLOW CHANGES

### Simplified Workflow (Adopted in Previous Session)

1. **Claude vytvorí 1 artifact** - vyčistený .md obsah
2. **User skopíruje obsah** do súboru
3. **User zmaže starý .md-old** manuálne
4. **Žiadne scripty** (boli zbytočné)

### "novy chat" Workflow Change

**STARÝ workflow (zrušený):**
- 4 artifacts: SESSION_YYYY-MM-DD, SESSION_NOTES, INIT, commit

**NOVÝ workflow (platný od teraz):**
- **3 artifacts:** SESSION_YYYY-MM-DD, INIT, commit
- **SESSION_NOTES.md ZRUŠENÝ** - duplicitný, máme podrobné session archívy

---

## 📍 DOKUMENTAČNÉ ŠTANDARDY

### Documentation Manifest Location

```
C:\Development\nex-automat\SESSION_NOTES\docs.json
```

### GitHub Raw URL Pattern

```
https://raw.githubusercontent.com/rauschiccsk/nex-automat/develop/[path]
```

### Script Naming (Historical)

```
[NUMBER]_update_[TABLE]_doc.py
```

**Note:** Scripts sú teraz deprecated, ale numbering pattern zostáva pre históriu.

---

## ⚡ WORKFLOW BEST PRACTICES

### Overený Proces

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
2. Opýtaj sa: "Skopíroval si už BARCODE dokument do súboru a zmazal .md-old?"
3. Ak ÁNO → "Pokračujem s ďalším dokumentom? (FGLST-product_categories.md-old)"
4. Ak NIE → "Vytvorím artifact pre BARCODE cleanup"

**Odporúčaný workflow:**
1. **Dokončiť BARCODE** (ak ešte nie)
2. **Načítať FGLST-product_categories.md-old**
3. **Opýtať sa na adresár**
4. **Vytvoriť 1 artifact** (cleaned doc)
5. **User skopíruje + zmaže**
6. **Pokračovať ďalším**

---

## 📈 SUCCESS METRICS

**Pre túto session očakávame:**
- ✅ BARCODE cleanup dokončený (ak ešte nie)
- ✅ 4-5 Products dokumentov dokončených
- ✅ Progress: 12-13/28 súborov (43-46%)

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

## 🔧 QUICK COMMANDS FOR REFERENCE

```powershell
# Git workflow
git status
git add docs/
git commit -m "docs: Database table docs batch 6 - products (N docs)"
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