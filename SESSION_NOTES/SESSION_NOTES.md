# NEX Automat - Session Notes

**Last Updated:** 2025-12-15  
**Current Task:** Database table docs migration (batch 6)  
**Status:** ⏸️ IN PROGRESS (4/28 dokumentov)

---

## CURRENT STATUS

### Active Task: .md-old Migration - Batch 6

**Cieľ:** Migrácia 28 database table dokumentov (Btrieve → PostgreSQL mapping)

**Progress:** 4/28 dokumentov (14.3%)

**Completed in this session:**
1. ✅ BANKLST-bank_catalog.md (script 32)
2. ✅ PAB-partner_catalog.md (script 33)
3. ✅ PABACC-partner_catalog_bank_accounts.md (script 34)
4. ✅ PACNCT-partner_catalog_contacts.md (script 35)

**Zostáva:** 24 dokumentov

---

## NEXT STEPS

### Immediate Actions

**1. Git Commit (PRVÉ!)**
```powershell
git add docs/ scripts/
git commit -m "docs: Database table docs migration batch 6 - partners (4 docs)"
git push origin develop
```

**2. Pokračovať batch 6 - Partners (5 dokumentov)**

Prioritné dokumenty:
- PAGLST-partner_categories.md-old (14.9 KB)
- PAYLST-payment_methods.md-old (8.3 KB)
- TRPLST-transport_methods.md-old (8.6 KB)
- PANOTI-partner_catalog_texts.md-old (15.4 KB)
- PASUBC-partner_catalog_facilities.md-old (18.0 KB)

**3. Products sekcia (5 dokumentov)**

**4. Stock Management (7 dokumentov)**

**5. Accounting + Sales (4 dokumenty)**

---

## OVERALL PROGRESS

### .md-old Migration Status

**Total:** 60 súborov  
**Completed:** 35 súborov (58.3%)  
**Remaining:** 25 súborov (41.7%)

**By Category:**
- ✅ Deployment: 11/11 (100%) - **COMPLETE**
- ✅ Database General: 4/4 (100%) - **COMPLETE**
- ✅ Database Indexes: 7/7 (100%) - **COMPLETE**
- ⏳ Database Tables: 4/28 (14.3%) - **IN PROGRESS**
- ⏳ Strategic: 0/2 (0%)
- ⏳ Development: 0/1 (0%)
- ⏳ Other: 0/4 (0%)

### Scripts Created

**Total:** 35 scripts (numbered 01-35)

**Batches completed:**
- Batch 1: Deployment docs (scripts 01-11)
- Batch 2: Database general (scripts 12-15)
- Batch 3: Database docs batch 1 (scripts 16-21)
- Batch 4: Database docs batch 2 (scripts 22-24)
- Batch 5: Database indexes (scripts 25-31)
- Batch 6: Database tables (scripts 32-35) - **PARTIAL**

---

## CRITICAL NOTES

### Database Table Docs Pattern

**Všetky súbory v adresári:** `C:\NEX\YEARACT\DIALS\`

**Formát úprav:**
1. Pridať popis Btrieve súboru (location)
2. Odstrániť SQL scripts (CREATE, INDEX, TRIGGER, FUNCTION)
3. Odstrániť query patterns
4. Odstrániť Python migration code
5. Zachovať mapping, biznis logiku, validačné pravidlá

**Priemerná redukcia:** 50-60% veľkosti

### Kritické zistenia

**1. bank_code NIE je FK!**
- V partner_catalog_bank_accounts
- Textová hodnota, nie referencia na bank_catalog

**2. FirstName/LastName SWAP!**
- V PACNCT.BTR je to opačne
- Pri migrácii MUSÍME swapovať

**3. GDPR Compliance**
- PACNCT.BTR: NEPRENÁŠAŤ citlivé údaje
- Adresa trvalého pobytu, doklady, dátum narodenia, občianstvo

---

## WORKFLOW

### Overený proces

1. Načítaj dokument (web_fetch)
2. Opýtaj sa na Btrieve location
3. Vytvor upravený dokument (artifact)
4. Vytvor script (artifact)
5. User skopíruje + spustí script
6. Pokračuj ďalším

### Best Practices

- Stručné odpovede
- Artifacts FIRST
- Čakanie po každom artifacte
- Progress tracking

---

## ESTIMATED TIME

**Zostávajúca práca:**
- Partners (5 docs): 90-120 min
- Products (5 docs): 90-120 min
- Stock (7 docs): 2-3 hours
- Accounting + Sales (4 docs): 60-90 min
- Strategic + Other (7 docs): ~2 hours

**Total remaining:** ~6-8 hours (4-5 sessions)

---

## COLLABORATION RULES

**22 pravidiel aktívnych** (memory_user_edits)

**Kľúčové pre túto úlohu:**
- Rule #7: CRITICAL artifacts pre všetky dokumenty
- Rule #8: Step-by-step, confirmation pred pokračovaním
- Rule #5: Slovak language
- Rule #20: "novy chat" = 4 artifacts
- Rule #22: Check all rules at start

---

## PROJECT CONTEXT

**Project:** nex-automat  
**Developer:** Zoltán (40 rokov skúseností)  
**Language:** Slovenčina  
**Current Version:** v2.4  

**Main Goal:** Migrácia NEX Genesis (Btrieve) → NEX Automat (PostgreSQL)

**Documentation Strategy:** Systematic cleanup of .md-old files with proper archival/relocation

---

**Status:** ⏸️ READY FOR NEXT SESSION  
**Next Task:** Partners sekcia (5 dokumentov)  
**Priority:** Git commit FIRST!

---

**KONIEC SESSION NOTES**