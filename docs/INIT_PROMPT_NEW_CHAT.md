# Init Prompt - Strategic Planning Phase 2

**Project:** NEX Automat  
**Last Session:** 2025-11-26 (Terminology & Vision)  
**This Session:** Strategic Planning - Bod 2 (Aktuálny stav)  

---

## Quick Context

NEX Automat je projekt pre kompletná automatizáciu podnikových procesov pre zákazníkov používajúcich NEX Genesis ERP.

**Aktuálny stav:**
- Version: 2.0.0 (tagged)
- GO-LIVE: 2025-11-27 (preview/demo pre Mágerstav)
- Strategic Planning: In Progress

---

## What Was Completed Last Session

### 1. Project Vision ✅
- NEX Automat = Kompletná automatizácia podniku
- Stratégia: Čiastočná → Úplná automatizácia
- Hodnota: Ušetrenie 1-3 FTE na zákazníka

### 2. Business Context ✅
- Pilotní zákazníci: Mágerstav, ANDROS, ICC
- Success kritériá definované

### 3. Terminology Dictionary ✅
- 8 podsystémov NEX Genesis
- 31 modulov s EN názvami a kódmi
- Dokument: TERMINOLOGY.md (artifact)

---

## Planning Progress

| Bod | Názov | Status |
|-----|-------|--------|
| 1 | Definícia cieľov | ✅ COMPLETE |
| - | Terminológia | ✅ COMPLETE |
| 2 | Aktuálny stav (inventory) | ⏳ **THIS SESSION** |
| 3 | Požiadavky & Priority | ⚪ TODO |
| 4 | Architektúra & Design | ⚪ TODO |
| 5 | Roadmap & Fázy | ⚪ TODO |
| 6 | Dokumentácia | ⚪ TODO |

---

## This Session Goals

### Bod 2 - AKTUÁLNY STAV (inventory)

Zmapovať:
1. **Čo máme hotové** - všetky komponenty NEX Automat
2. **Čo funguje dobre** - stabilné časti systému
3. **Kde sú limity** - známe problémy, technické obmedzenia

**Komponenty na review:**
- n8n workflow (email processing)
- AI extrakcia (PDF → XML)
- FastAPI transfer
- supplier-invoice-loader
- supplier-invoice-editor
- PostgreSQL staging
- Btrieve integration

---

## Key Artifacts from Last Session

### TERMINOLOGY.md
Kompletný terminologický slovník NEX Genesis:

**Podsystémy:**
| Code | SK | EN |
|------|----|----|
| MASTER- | Všeobecné číselníky | Master Data |
| STK- | Skladové hospodárstvo | Stock Management |
| PROD- | Výroba | Production Management |
| PROC- | Obstarávanie tovaru | Procurement |
| PRICE- | Tvorba predajných cien | Sales Price Management |
| SALES- | Predaj tovaru | Sales Management |
| FIN- | Finančné účtovníctvo | Financial Management |
| ACC- | Podvojné účtovníctvo | General Ledger Accounting |

**Relevantné moduly pre aktuálny projekt:**
- PROC-DN: Supplier Delivery Notes
- PROC-INV: Supplier Invoices
- PRICE-CHANGE: Price Change Requests
- PRODUCTS: Product and Service Catalog
- PARTNERS: Business Partner Catalog

---

## Documentation Structure Decision

Navrhnutá štruktúra (schváliť):
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

## Project Files Structure

```
C:\Development\nex-automat\
├── docs\
│   ├── SESSION_NOTES.md
│   ├── strategy\           ← NEW (to create)
│   │   └── TERMINOLOGY.md
│   └── apps\
│       └── supplier-invoice-editor.json
├── apps\
│   ├── supplier-invoice-loader\
│   └── supplier-invoice-editor\
└── packages\
    ├── invoice-shared\
    └── nex-shared\
```

---

## Key Information

### Current Project Status
- **supplier-invoice-loader:** Production ready (v2.0.0)
- **supplier-invoice-editor:** 75% complete (Phase 4 done)
- **n8n workflow:** Running on dev server
- **PostgreSQL:** invoice_staging database

### GO-LIVE 2025-11-27
- **Type:** Preview/Demo
- **Customer:** Mágerstav s.r.o.
- **Scope:** Email → GUI display (no NEX Genesis write)
- **Purpose:** Customer familiarization, AI validation

### Known TODOs
- Filename duplicity issue (PDF/XML storage)
- Phase 5: NEX Genesis write operations
- Approval workflow
- Price Change Requests creation

---

## How to Start This Session

1. Load SESSION_NOTES.md from GitHub
2. Confirm understanding of last session
3. Start Bod 2: Aktuálny stav (inventory)
   - Review each component systematically
   - Document what works, what doesn't
   - Identify gaps and limitations

---

## Important Notes

- **This is planning session** - no coding
- **Output:** Strategic documentation
- **Use terminology** from TERMINOLOGY.md
- **Step by step** - one topic at a time

---

**Last Updated:** 2025-11-26  
**Version:** 1.0  
**Status:** 🟡 Strategic Planning In Progress