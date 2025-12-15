# INIT PROMPT - NEX Automat: Systematic Documentation Continue

**Projekt:** nex-automat  
**Úloha:** Pokračovanie návrhu supplier-invoice-staging aplikácie  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** https://claude.ai/chat/b64ae513-c5a0-414a-8a0c-4f3b0fd5d09c  
**Status:** 🔄 Pokračujeme po token limit issue

---

## ⚠️ KRITICKÉ: COLLABORATION RULES

**MUSÍŠ dodržiavať 21 pravidiel z memory_user_edits!**

Kľúčové pravidlá pre túto session:
- **Rule #7:** CRITICAL artifacts pre všetky dokumenty/kód
- **Rule #8:** Step-by-step, confirmation pred pokračovaním
- **Rule #20:** "novy chat" = 4 artifacts (ARCHIVE, NOTES, INIT, commit)
- **Rule #5:** Slovak language, presná terminológia projektov

---

## 📋 ČO SME DOKONČILI V PREVIOUS SESSION

### ✅ Definície Aplikácie
- **Názov:** `supplier-invoice-staging` ✅
- **Framework:** PySide6 (migration z PyQt5) ✅
- **Umiestnenie:** `apps/supplier-invoice-staging/` ✅
- **Dokumentácia:** `apps/supplier-invoice-staging/docs/SUPPLIER_INVOICE_STAGING.md` ✅

### ✅ Databázová Schéma (Hotová)

**Tabuľka:** `supplier_invoice_items`

**Kategórie polí:**
1. **xml_*** (11 polí) - Originálne XML dáta - IMMUTABLE
2. **nex_*** (6 polí) - NEX Genesis enrichment - AUTO
3. **user_*** (3 polia) - Manuálne editované - EDITABLE
4. **Statusové** (2 polia) - match_status, validation_status

**Farebná schéma:**
- 🟢 Zelená = Spárované (ean_matched | name_matched | manual_matched)
- 🔴 Červená = Nespárované (unmatched - treba vytvoriť v NEX)

**SQL schéma kompletná** - viď PROJECT_ARCHIVE_SESSION.md sekcia 5

### ✅ Workflow (9 krokov definovaných)
1. Zobrazenie pending faktúr
2. Výber faktúry
3. Zobrazenie položiek (farebne)
4. Identifikácia produktov
5. Vytvorenie nových produktov v NEX
6. Úprava cien (priame / margin %)
7. Validácia
8. Archivovanie
9. Import do NEX Genesis

---

## 🔄 ČO TREBA DOKONČIŤ TERAZ

### Priority 1: SUPPLIER_INVOICE_STAGING.md
**Čo máme:**
- ✅ Sekcia 1: Overview & Purpose (hotové v artifacts)
- ✅ Sekcia 2: Databázová štruktúra (hotové v artifacts)
- ❌ Sekcia 3: GUI Štruktúra (CHÝBA)
- ❌ Sekcia 4: Workflows (CHÝBA)
- ❌ Sekcia 5: NEX Genesis Integration (CHÝBA)
- ❌ Sekcia 6: Configuration (CHÝBA)
- ❌ Sekcia 7: Development & Deployment (CHÝBA)

**Akcia:** Dokončiť SUPPLIER_INVOICE_STAGING.md (sekcie 3-7)

### Priority 2: PySide6 Migration Plan
**Čo treba:**
- BaseWindow trieda (PySide6)
- BaseGrid trieda (PySide6)
- Quick search (PySide6)
- Grid persistence (PySide6)

**Akcia:** Vytvoriť PYSIDE6_MIGRATION_PLAN.md

### Priority 3: Implementation Plan
**Následne:**
- Python kód aplikácie
- Config súbory
- Database migrations
- Testing suite

---

## 🎯 SUGGESTED NEXT STEPS

### Krok 1: Dokončiť Dokumentáciu
```
1. Otvor artifact "supplier_invoice_staging_doc"
2. Dopíš sekcie 3-7:
   - GUI Štruktúra (windows, widgets, layouts)
   - Workflows (detailný popis 9 krokov)
   - NEX Genesis Integration (API calls, data sync)
   - Configuration (config.yaml štruktúra)
   - Development & Deployment (setup, dependencies)
3. Ulož do apps/supplier-invoice-staging/docs/SUPPLIER_INVOICE_STAGING.md
```

### Krok 2: PySide6 Migration
```
1. Analyzuj existujúce BaseWindow (PyQt5)
2. Analyzuj existujúce BaseGrid (PyQt5)
3. Vytvor PYSIDE6_MIGRATION_PLAN.md
4. Vytvor migračné scripty
```

### Krok 3: Implementácia
```
1. Vytvor kostru projektu supplier-invoice-staging
2. Implementuj BaseWindow (PySide6)
3. Implementuj BaseGrid (PySide6)
4. Implementuj hlavné okno aplikácie
```

---

## 📂 AKTUÁLNA ŠTRUKTÚRA PROJEKTU

```
nex-automat/
├── apps/
│   ├── supplier-invoice-loader/       # FastAPI (port 8001) - HOTOVÉ ✅
│   ├── supplier-invoice-editor/       # Stará GUI (PyQt5) - DEPRECATED ❌
│   └── supplier-invoice-staging/      # Nová GUI (PySide6) - V NÁVRHU 🔄
│       ├── docs/
│       │   └── SUPPLIER_INVOICE_STAGING.md  (čiastočne hotové)
│       ├── src/                       (NEEXISTUJE)
│       ├── database/                  (NEEXISTUJE)
│       └── config/                    (NEEXISTUJE)
├── packages/
│   ├── nex-shared/
│   │   ├── gui/                       # BaseWindow, BaseGrid (PyQt5) ❌
│   │   ├── database/                  # DB utils ✅
│   │   └── models/                    # Data models ✅
│   └── nexdata/                       # NEX data access ✅
└── docs/
    ├── architecture/
    │   └── database/                  # Sessions 1-8 dokumentácia ✅
    └── COLLABORATION_RULES.md v1.2    ✅
```

---

## 🔑 KĽÚČOVÉ TECHNICKÉ INFO

### Database Connection
```python
# PostgreSQL invoice_staging
HOST = "localhost"
PORT = 5432
DATABASE = "invoice_staging"
USER = "postgres"
```

### NEX Genesis Connection
```python
# Btrieve NEX Genesis
NEX_DATA_PATH = "X:\\NEX\\DATA\\"  # Server path
GSCAT_FILE = "GSCAT.BTR"           # Product catalog
```

### Tech Stack
- **GUI:** PySide6 (Qt 6.x)
- **Database:** PostgreSQL 15
- **ORM:** SQLAlchemy (ak použijeme)
- **Config:** PyYAML
- **Data:** Pandas (pre bulk operations)

---

## 💡 ROZHODNUTIA Z PREVIOUS SESSION

### 1. PySide6 > PyQt5
**Dôvod:** LGPL licencia, oficiálny Qt for Python  
**Dopad:** Potreba migrácie BaseWindow/BaseGrid

### 2. Kategorizácia Polí (xml_*, nex_*, user_*)
**Dôvod:** Prehľadnosť, jasná separácia concerns  
**Benefit:** Jednoduchšia údržba, lepšia dokumentácia

### 3. Farebná Schéma (zelená/červená)
**Dôvod:** Intuitívna pre používateľa  
**Benefit:** Okamžitá vizuálna identifikácia problémov

### 4. Systematická Dokumentácia
**Pattern:** Každá app = vlastný docs/ adresár  
**Benefit:** Modularizácia, ľahké nájdenie info

---

## ⚠️ KNOWN ISSUES

### Token Limit Problem
**Problem:** Previous session sa zablokovala pri ~95k / 190k tokenov  
**Expected:** Malo byť priestoru na ~95k ešte  
**Actual:** Predčasné zablokovanie  
**Hypotéza:** Možný bug Claude.ai alebo skryté limity  

**Ako sa vyhnúť:**
- Kratšie artifacts
- Modulárna dokumentácia
- Častejšie checkpointy

---

## 📋 CHECKLIST PRE TÚTO SESSION

### Before You Start
- [ ] Prečítaj COLLABORATION_RULES.md pravidlá
- [ ] Prečítaj PROJECT_ARCHIVE_SESSION.md
- [ ] Understand databázová schéma (sekcia 5 v ARCHIVE)
- [ ] Understand workflow (9 krokov)

### During Session
- [ ] ALWAYS artifacts pre dokumenty/kód
- [ ] ONE step at a time, WAIT for confirmation
- [ ] Token usage na konci každej odpovede
- [ ] Follow Slovak language + English tech terms

### End of Session
- [ ] Update SESSION_NOTES.md
- [ ] Create INIT_PROMPT_NEW_CHAT.md (pre ďalšiu session)
- [ ] Create commit-message.txt (ak sú zmeny)
- [ ] Append to PROJECT_ARCHIVE.md

---

## 🎯 IMMEDIATE GOAL

**ČO UROBIŤ PRVÉ:**

Opýtaj sa:
> "Chceš pokračovať dokončením SUPPLIER_INVOICE_STAGING.md (sekcie 3-7)  
> alebo radšej začať PySide6 migration plan?"

**Potom postupuj step-by-step podľa výberu.**

---

**Token Budget:** 190,000  
**Estimated Completion:** 2-4 hodiny (závisí od zložitosti)  
**Ready to Continue:** ✅ ÁNO