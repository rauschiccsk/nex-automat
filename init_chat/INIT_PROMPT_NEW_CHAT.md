# INIT PROMPT - NEX Automat Project

**Projekt:** nex-automat  
**Current Status:** RAG External Access COMPLETE ✅  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** RAG External Access Complete (2025-12-17)

---

## ⚠️ KRITICKÉ: COLLABORATION RULES

**MUSÍŠ dodržiavať 23 pravidiel z memory_user_edits!**

Kľúčové pravidlá:
- **Rule #7:** CRITICAL artifacts pre všetky dokumenty/kód
- **Rule #8:** Step-by-step, confirmation pred pokračovaním
- **Rule #5:** Slovak language, presná terminológia projektov
- **Rule #20:** "novy chat" = 3 artifacts + archive + RAG reindex
- **Rule #23:** RAG maintenance po pridaní nových docs

---

## ✅ RAG EXTERNAL ACCESS - FUNGUJE

### Claude má prístup k RAG API:
```
https://rag-api.icc.sk/health
https://rag-api.icc.sk/search?query=...&limit=N
https://rag-api.icc.sk/stats
```

### Pred použitím RAG:
1. Zoltán musí mať spustený RAG Server + Cloudflare Tunnel
2. Zoltán poskytne URL do chatu (permission requirement)

### RAG obsahuje:
- 261 dokumentov (107 docs + 154 code docs)
- 614 chunks, 475k tokens
- Docs: `docs/**/*.md`
- Code: `docs/code/*.md` (vygenerované z Python)

---

## 🎯 IMMEDIATE NEXT STEPS

### Priority #1: NEX Genesis Product Enrichment (v2.4 Phase 4)

**Cieľ:** Implementácia product enrichment functionality

**Potrebné:**
- EAN barcode matching
- Btrieve database integration
- GUI pre product enrichment

### Priority #2: Btrieve → PostgreSQL Migration

**Stav:** Dokumentácia complete, implementácia pending

---

## 🚀 RAG MAINTENANCE

### Po pridaní nových docs:
```powershell
cd C:\Development\nex-automat
.\venv\Scripts\Activate.ps1
python tools/rag/rag_reindex.py --new
```

### Po zmene Python kódu:
```powershell
python tools/rag/generate_code_docs.py
python tools/rag/rag_reindex.py --dir docs/code/
```

### Kontrola stavu:
```powershell
python tools/rag/rag_reindex.py --stats
```

---

## 🔧 SPUSTENIE SLUŽIEB (po reštarte PC)

### Terminal 1 - RAG Server:
```powershell
cd C:\Development\nex-automat
.\venv\Scripts\Activate.ps1
python -m tools.rag.server start
```

### Terminal 2 - Cloudflare Tunnel:
```powershell
cloudflared tunnel --config C:\Users\ZelenePC\.cloudflared\config.yml run n8n-tunnel
```

### Overenie:
```
https://rag-api.icc.sk/health
```

---

## 📂 PROJECT STRUCTURE

```
nex-automat/
├── apps/
│   ├── supplier-invoice-editor/    # PyQt5 GUI
│   ├── supplier-invoice-loader/    # FastAPI backend
│   └── supplier-invoice-staging/   # Staging app
├── packages/
│   ├── nex-shared/                 # Shared GUI components
│   └── nexdata/                    # Btrieve access layer
├── tools/
│   └── rag/                        # ✅ RAG system (COMPLETE)
│       ├── server.py               # Server manager
│       ├── rag_reindex.py          # Reindex tool
│       └── generate_code_docs.py   # Code docs generator
├── docs/
│   ├── infrastructure/             # RAG_EXTERNAL_ACCESS.md
│   └── code/                       # Generated Python docs (154 files)
├── scripts/
│   └── infrastructure/             # start-rag-services.bat
└── venv/                           # Python 3.12 64-bit
```

---

## 📚 KEY DOCUMENTS

**Infrastructure:**
- `docs/infrastructure/RAG_EXTERNAL_ACCESS.md` - RAG setup guide

**Strategic:**
- `docs/strategic/RAG_IMPLEMENTATION.md` - RAG plán
- `docs/strategic/PROJECT_ROADMAP.md` - Roadmap

**Database:**
- `docs/database/MIGRATION_MAPPING.md` - Btrieve→PostgreSQL
- `docs/database/DATABASE_PRINCIPLES.md` - Konvencie

---

## 🔍 SESSION WORKFLOW

1. Načítaj tento INIT_PROMPT
2. Skontroluj memory_user_edits (23 pravidiel)
3. Ak potrebuješ info z RAG, požiadaj o URL
4. Pracuj step-by-step s confirmations
5. Na konci: "novy chat" → 3 artifacts + archive + RAG reindex

---

**Token Budget:** 190,000  
**Location:** C:\Development\nex-automat  
**Status:** 🟢 READY - RAG Access Working

---

**KONIEC INIT PROMPTU**