# INIT PROMPT - NEX Automat: Database Table Docs Migration (Batch 6 Continue)

**Projekt:** nex-automat  
**Úloha:** Database table docs migration (batch 6 continuation)  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** https://claude.ai/chat/[CURRENT_CHAT_URI]  
**Status:** 4/28 dokumentov dokončených, **24 zostáva**

---

## ⚠️ KRITICKÉ: COLLABORATION RULES

**MUSÍŠ dodržiavať 22 pravidiel z memory_user_edits!**

Kľúčové pravidlá pre túto session:
- **Rule #7:** CRITICAL artifacts pre všetky dokumenty/kód
- **Rule #8:** Step-by-step, confirmation pred pokračovaním
- **Rule #20:** "novy chat" = 4 artifacts (ARCHIVE, NOTES, INIT, commit)
- **Rule #5:** Slovak language, presná terminológia projektov
- **Rule #22:** Na začiatku každého chatu skontrolovať všetky pravidlá

---

## 📋 ČO SME DOKONČILI V PREVIOUS SESSION

### ✅ Migrované Dokumenty (4/28)

**Catalogs - Partners (4 dokumenty):**

1. **BANKLST-bank_catalog.md** (10.7 KB → 6 KB)
   - Location: DIALS
   - Script: 32_update_BANKLST_doc.py
   - Redukcia: 44%

2. **PAB-partner_catalog.md** (39.9 KB → 18 KB) ⚠️ VEĽKÝ
   - Location: DIALS
   - 8 tabuliek partner systému
   - Script: 33_update_PAB_doc.py
   - Redukcia: 55%

3. **PABACC-partner_catalog_bank_accounts.md** (12.6 KB → 7 KB)
   - Location: DIALS
   - Script: 34_update_PABACC_doc.py
   - **KRITICKÉ:** bank_code je textová hodnota, NIE FK!
   - Redukcia: 45%

4. **PACNCT-partner_catalog_contacts.md** (22.8 KB → 10 KB)
   - Location: DIALS
   - Script: 35_update_PACNCT_doc.py
   - **KRITICKÉ:** FirstName/LastName SWAP pri migrácii!
   - Redukcia: 56%

### 📊 Progress

**Dokončené:** 35/60 súborov (58.3%)  
**Batch 6:** 4/28 dokumentov (14.3%)  
**Zostáva:** 24 database table dokumentov

**By Category:**
- ✅ Deployment: 11/11 (100%) - **COMPLETE**
- ✅ Database General: 4/4 (100%) - **COMPLETE**
- ✅ Database Indexes: 7/7 (100%) - **COMPLETE**
- ⏳ Database Tables: 4/28 (14.3%) - **IN PROGRESS**
- ⏳ Strategic: 0/2 (0%)
- ⏳ Development: 0/1 (0%)
- ⏳ Other: 0/4 (0%)

---

## 🎯 ČO TREBA UROBIŤ TERAZ

### Priority 1: Git Commit (PRVÉ!)

```powershell
# Commit batch 6 partial progress
git add docs/ scripts/
git commit -m "docs: Database table docs migration batch 6 - partners (4 docs)"
git push origin develop
```

### Priority 2: Pokračovať Batch 6 - Partners Sekcia

**Zostávajúce Partners dokumenty (5):**

1. **PAGLST-partner_categories.md-old** (14.9 KB)
2. **PAYLST-payment_methods.md-old** (8.3 KB)
3. **TRPLST-transport_methods.md-old** (8.6 KB)
4. **PANOTI-partner_catalog_texts.md-old** (15.4 KB)
5. **PASUBC-partner_catalog_facilities.md-old** (18.0 KB)

**Všetky pravdepodobne v adresári DIALS** (overiť pri každom).

---

## 📂 ZOSTÁVAJÚCE DOKUMENTY (24 total)

### Catalogs - Partners (5 súborov)

- PAGLST-partner_categories.md-old (14.9 KB)
- PAYLST-payment_methods.md-old (8.3 KB)
- TRPLST-transport_methods.md-old (8.6 KB)
- PANOTI-partner_catalog_texts.md-old (15.4 KB)
- PASUBC-partner_catalog_facilities.md-old (18.0 KB)

### Catalogs - Products (5 súborov)

- BARCODE-product_catalog_identifiers.md-old (24.2 KB)
- FGLST-product_categories.md-old (16.1 KB)
- GSCAT-product_catalog.md-old (20.7 KB)
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
- BANKLST.BTR
- PAB.BTR
- PABACC.BTR
- PACNCT.BTR

**Očakávané:** Väčšina súborov pravdepodobne v DIALS, ale vždy sa opýtať!

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

**50-60% veľkosti** (overené na 4 dokumentoch)

---

## 💡 KRITICKÉ POZNÁMKY PRE MIGRÁCIU

### 1. bank_code NIE je FK!

**V partner_catalog_bank_accounts:**
- `bank_code` je textová hodnota
- NIE FK constraint na bank_catalog
- User vyberie z číselníka → systém predvyplní → user môže zmeniť
- Dôvod: denormalizácia, flexibility

### 2. FirstName/LastName SWAP!

**V PACNCT.BTR (partner_catalog_contacts):**
- Btrieve FirstName = priezvisko
- Btrieve LastName = meno
- Pri migrácii MUSÍME swapovať!
- PostgreSQL first_name = meno, last_name = priezvisko

### 3. GDPR Compliance

**PACNCT.BTR - NEPRENÁŠAME:**
- Adresa trvalého pobytu
- Doklady totožnosti (IdnType, IdnCard)
- Dátum a miesto narodenia (BrtDate, BrtPlac)
- Občianstvo (Citizen)

### 4. Manuálny Krok Pre Veľké Dokumenty

**Pre dokumenty >15 KB:**
- Artifact content → user copy to file
- Script len zmaže .md-old
- Dôvod: token/content size limits

---

## 📝 DOKUMENTAČNÉ ŠTANDARDY

### Documentation Manifest Location

```
C:\Development\nex-automat\SESSION_NOTES\docs.json
```

### GitHub Raw URL Pattern

```
https://raw.githubusercontent.com/rauschiccsk/nex-automat/develop/[path]
```

### Script Naming

```
[NUMBER]_update_[TABLE]_doc.py
```

**Aktuálny number:** 36 (ďalší script)

---

## ⚠️ WORKFLOW BEST PRACTICES

### Overený Proces

1. **Načítaj dokument** (web_fetch)
2. **Opýtaj sa na Btrieve location** (user poskytne adresár)
3. **Vytvor upravený dokument** (artifact)
4. **Vytvor script** (artifact)
5. **User skopíruje obsah + spustí script**
6. **Pokračuj ďalším dokumentom**

### Komunikácia

✅ **StruÄne** - žiadny verbose output  
✅ **Akcie** - artifacts, scripts, konkrétne kroky  
✅ **Čakanie** - po každom artifacte čakať na potvrdenie  
✅ **Progress** - token stats na konci každej odpovede

---

## 🚀 IMMEDIATE ACTION

**Prvý krok po načítaní tohto promptu:**

1. Skontroluj memory_user_edits (22 pravidiel) ✅
2. Opýtaj sa: "Spustil si už git commit pre batch 6 partial?"
3. Ak ÁNO → "Pokračujem s ďalším dokumentom? (PAGLST-partner_categories.md-old)"
4. Ak NIE → "Mám ti pomôcť s git commit?"

**Odporúčaný workflow:**
1. **Git commit FIRST** (ak ešte nie)
2. **Načítaj PAGLST-partner_categories.md-old**
3. **Opýtaj sa na adresár**
4. **Vytvor 2 artifacts** (cleaned doc + script)
5. **User skopíruje + spustí**
6. **Pokračuj ďalším**

---

## 📈 SUCCESS METRICS

**Pre túto session očakávame:**
- ✅ Git commit batch 6 partial (ak ešte nie)
- ✅ 5 Partners dokumentov dokončených
- ✅ Progress: 39/60 súborov (65%)
- ✅ Scripts 36-40 vytvorené

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
git add docs/ scripts/
git commit -m "docs: Database table docs batch 6 - partners (N docs)"
git push origin develop

# Generate manifests
python tools/generate_manifests.py

# Run script
python scripts/[NUMBER]_update_[TABLE]_doc.py
```

---

**Token Budget:** 190,000  
**Estimated Session:** 90-120 minút  
**Ready to Continue:** ✅ ÁNO

---

**KONIEC INIT PROMPTU**