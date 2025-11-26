# NEX Automat - Session Notes

**Date:** 2025-11-26  
**Project:** nex-automat  
**Location:** C:/Development/nex-automat  
**Session:** Strategic Planning & Terminology Definition

---

## 🎯 Session Summary

Strategické plánovanie projektu NEX Automat - refaktoring vývojových prác a vytvorenie kvalitnej projektovej dokumentácie.

---

## ✅ Completed This Session

### 1. Project Vision Definition
- **NEX Automat** = Kompletná automatizácia podnikových procesov
- **Stratégia:** Čiastočná → Úplná automatizácia
- **Problém:** Ľudský faktor = chyby, náklady
- **Hodnota:** Ušetrenie 1-3 FTE na zákazníka

### 2. Business Context
**Pilotní zákazníci (3):**
- Mágerstav s.r.o. - GO-LIVE 2025-11-27 (preview/demo)
- ANDROS s.r.o. - NEX Genesis zákazník
- ICC s.r.o. - interné testovanie

**Success kritériá:**
- Počet úspešne spracovaných faktúr
- Percento faktúr bez manuálneho zásahu
- Spokojnosť zákazníkov

### 3. Complete Terminology Dictionary
Vytvorený kompletný terminologický slovník NEX Genesis:
- **8 podsystémov**
- **31 modulov**
- SK → EN preklady s kódmi a popismi

**Podsystémy:**
| # | Code Prefix | SK | EN |
|---|-------------|----|----|
| 1 | MASTER- | Všeobecné číselníky | Master Data |
| 2 | STK- | Skladové hospodárstvo | Stock Management |
| 3 | PROD- | Výroba tovaru a polotovaru | Production Management |
| 4 | PROC- | Obstarávanie tovaru | Procurement |
| 5 | PRICE- | Tvorba predajných cien | Sales Price Management |
| 6 | SALES- | Predaj tovaru (odbyt) | Sales Management |
| 7 | FIN- | Finančné účtovníctvo | Financial Management |
| 8 | ACC- | Podvojné účtovníctvo | General Ledger Accounting |

### 4. Future NEX Automat Modules Identified
- ✅ Dodávateľské faktúry (PROC-INV) - 75% hotové
- 🟡 E-shop objednávky (SALES-ORD) - 80% v NEX Genesis
- ⚪ Bankové výpisy (FIN-BANK)
- ⚪ Podvojné účtovníctvo (ACC-*)
- ⚪ Uzávierka DPH
- ⚪ Ročná daňová uzávierka
- ⚪ Management reporty

---

## 📁 Artifacts Created

1. **TERMINOLOGY.md** - NEX Genesis Terminology Dictionary
   - 8 podsystémov, 31 modulov
   - SK → EN preklady
   - Kódy, popisy, usage guidelines
   - Uložiť do: `docs/strategy/TERMINOLOGY.md`

---

## 🔄 Current Status

### GO-LIVE 2025-11-27
**Typ:** Preview/Demo pre zákazníka Mágerstav  
**Scope:** Email → AI Extrakcia → GUI zobrazenie  
**Cieľ:** Ukázať zákazníkovi funkčnosť, validácia AI extrakcie

### supplier-invoice-editor (75% complete)
**Hotové:**
- PyQt5 GUI aplikácia
- PostgreSQL integration
- Zobrazenie faktúr a položiek
- Editácia marže → prepočet ceny
- NEX Genesis ČÍTANIE (Btrieve)
- XML import (ISDOC)

**Chýba (Phase 5):**
- Approval workflow
- NEX Genesis ZÁPIS (TSH/TSI)
- Price Change Requests

---

## 📋 Next Steps

### Immediate (Next Session)
1. **Bod 2 - AKTUÁLNY STAV (inventory)**
   - Čo máme hotové v NEX Automat
   - Čo funguje dobre
   - Kde sú limity/problémy

2. **Bod 3 - POŽIADAVKY & PRIORITY**
   - Must have / Should have / Nice to have

3. **Bod 4 - ARCHITEKTÚRA & DESIGN**
   - High-level dizajn
   - Technické rozhodnutia

4. **Bod 5 - ROADMAP & FÁZY**
   - Fázy implementácie
   - Časové odhady

### Documentation Structure Decision
Navrhnutá nová štruktúra:
```
docs/
└── strategy/           ← NOVÝ PRIEČINOK
    ├── TERMINOLOGY.md
    ├── VISION.md
    ├── ARCHITECTURE.md
    ├── ROADMAP.md
    └── REQUIREMENTS.md
```

---

## 📊 Planning Progress

| Bod | Názov | Status |
|-----|-------|--------|
| 1 | Definícia cieľov | ✅ COMPLETE |
| - | Terminológia | ✅ COMPLETE |
| 2 | Aktuálny stav (inventory) | ⏳ NEXT |
| 3 | Požiadavky & Priority | ⚪ TODO |
| 4 | Architektúra & Design | ⚪ TODO |
| 5 | Roadmap & Fázy | ⚪ TODO |
| 6 | Dokumentácia | ⚪ TODO |

---

## 🔗 Key Resources

**GitHub Repository:**
- https://github.com/rauschiccsk/nex-automat

**Project Location:**
- C:/Development/nex-automat

**Current Branch:**
- develop

**Key Files:**
- docs/apps/supplier-invoice-editor.json
- apps/supplier-invoice-editor/docs/SESSION_NOTES.md

---

## 💡 Key Decisions Made

1. **Terminology First** - Vytvorenie názvoslovia pred ďalším plánovaním
2. **Strategy Folder** - Strategická dokumentácia do `docs/strategy/`
3. **Pilotná fáza** - 3 zákazníci pred komerčným rolloutom
4. **Postupná automatizácia** - Od faktúr po kompletné účtovníctvo

---

**Last Updated:** 2025-11-26  
**Next Session:** Bod 2 - Aktuálny stav (inventory)  
**Status:** 🟡 Strategic Planning In Progress