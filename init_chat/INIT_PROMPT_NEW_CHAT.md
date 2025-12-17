# INIT PROMPT - NEX Automat Project

**Projekt:** nex-automat  
**Current Status:** RAG Cloudflare Integration - BLOCKED  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** RAG Cloudflare Tunnel Setup (2025-12-17)

---

## ⚠️ KRITICKÉ: COLLABORATION RULES

**MUSÍŠ dodržiavať 22 pravidiel z memory_user_edits!**

Kľúčové pravidlá:
- **Rule #7:** CRITICAL artifacts pre všetky dokumenty/kód
- **Rule #8:** Step-by-step, confirmation pred pokračovaním
- **Rule #5:** Slovak language, presná terminológia projektov
- **Rule #22:** Na začiatku každého chatu skontrolovať všetky pravidlá

---

## 🚨 HIGHEST PRIORITY - RAG EXTERNAL ACCESS

### STRATEGIC BLOCKER ❌

**Problém:** Cloudflare Managed Rules blokujú Claude's prístup k RAG serveru

**Evidence:**
```
URL: https://n8n.icc.sk/rag/health
Status: 403 Forbidden
Mitigation: Block by Managed rules
Source IP: 34.162.230.222 (Anthropic/Claude)
```

**Zoltán's Decision:**
> "Zastavím všetky projekty pokiaľ to nevyriešime. Som v 21. storočí, plánujeme futuristické riešenia - nedokážeme vyriešiť elementárnu úlohu?"

**Vízia:**
1. Claude má priamy prístup k RAG dokumentácii (no manual courier)
2. RAG system = budúci produkt pre veľké firmy
3. Centrálny AI-powered knowledge repository

---

## 🎯 IMMEDIATE NEXT STEPS

### Priority #1: Vyriešiť Cloudflare Blocking DEFINITÍVNE

**Čo funguje:**
- ✅ RAG Server: http://127.0.0.1:8765 (healthy, 107 docs)
- ✅ Cloudflare Tunnel: n8n-tunnel running
- ✅ Path routing: https://n8n.icc.sk/rag/* 
- ✅ Local access + browser access funguje
- ❌ Claude external access - 403

**Action Plan (postupne vyskúšať):**

### Option 1: Cloudflare Workers ⭐ (NAJVIAC SĽUBNÉ)
**Why:** Workers bežia na edge, môžu bypassovať managed rules

**Steps:**
1. Cloudflare Dashboard → Workers & Pages
2. Create Service: `rag-proxy`
3. Deploy worker code (proxy to localhost:8765)
4. Workers Routes: `n8n.icc.sk/rag/*`
5. Test: Claude pristúpi cez worker

**Expected time:** 10-15 minút

---

### Option 2: Subdoména `rag.icc.sk`
**Why:** Nová subdoména BEZ managed rules + security policies

**Steps:**
1. DNS: Add `rag.icc.sk` CNAME to Cloudflare Tunnel
2. Update Cloudflare Tunnel config
3. NO security rules na subdoméne
4. Test: `https://rag.icc.sk/health`

**Expected time:** 15-20 minút

---

### Option 3: API Token Authentication
**Why:** Autentifikovaný prístup môže bypassovať managed rules

**Steps:**
1. RAG server: Add API key middleware
2. Cloudflare: Allow requests with valid API key header
3. Claude: Send API key in X-API-Key header
4. Test: web_fetch with headers

**Expected time:** 25-30 minút

---

## ✅ COMPLETED - Previous Session

### RAG FastAPI Server ✅
- HTTP server: http://127.0.0.1:8765
- Endpoints: /health, /stats, /search
- Database: 107 docs, 500 chunks, 415,891 tokens
- Cloudflare Tunnel integration: n8n.icc.sk/rag/*

### Server Modifications ✅
- Added `root_path="/rag"` to FastAPI app
- Script: `scripts/01_add_root_path.py`
- Config: `C:\Users\ZelenePC\.cloudflared\config.yml`

### Cloudflare Security Rules ✅ (deployed, ale nefunkčné)
- Rule 1: Allow Anthropic IPs (Order: 1, Skip, All managed rules)
- Rule 2: Allow RAG API path (Order: 2, Skip, All managed rules)

### Testing Results ✅
- LocalTunnel: Fungoval perfektne (proof of concept)
- Ngrok: Verification page blocking
- Cloudflare: Managed rules blocking external IPs

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
│   ├── rag/                        # ✅ RAG system (COMPLETE)
│   │   ├── api.py                  # Python search API
│   │   ├── server_app.py           # FastAPI (root_path="/rag")
│   │   ├── server.py               # Server manager
│   │   ├── hybrid_search.py        # Hybrid search
│   │   ├── database.py             # PostgreSQL operations
│   │   ├── embeddings.py           # Sentence transformers
│   │   ├── __main__.py             # CLI tool
│   │   └── init_prompt_helper.py   # Context generator
│   └── setup/
├── config/
│   └── rag_config.yaml             # RAG configuration
├── docs/                           # 107 indexed documents
│   └── archive/
│       └── sessions/
│           └── SESSION_2025-12-17_RAG_Cloudflare_Integration.md
├── scripts/
│   └── 01_add_root_path.py         # RAG server patch
└── venv/                           # Python 3.12 64-bit
```

---

## 🔧 ENVIRONMENT

**Servers:**
- Development: C:\Development\nex-automat
- Deployment: C:\Deployment\nex-automat

**Python:**
- venv: Python 3.12.10 64-bit
- Activate: `.\venv\Scripts\Activate.ps1`

**PostgreSQL:**
- Port: 5432
- RAG DB: nex_automat_rag (107 docs, 500 chunks)
- Main DB: nex_automat

**RAG Server:**
- Host: 127.0.0.1
- Port: 8765
- Start: `python -m tools.rag.server start`

**Cloudflare Tunnel:**
- Name: n8n-tunnel
- Config: `C:\Users\ZelenePC\.cloudflared\config.yml`
- URL: https://n8n.icc.sk/rag/*
- Start: `cloudflared tunnel --config <path> run n8n-tunnel`

---

## 📚 KEY DOCUMENTS

**Strategic:**
- docs/strategic/RAG_IMPLEMENTATION.md - RAG plán
- docs/strategic/PROJECT_ROADMAP.md - Roadmap

**Database:**
- docs/database/MIGRATION_MAPPING.md - Btrieve→PostgreSQL
- docs/database/DATABASE_PRINCIPLES.md - Konvencie

**Sessions:**
- docs/archive/sessions/SESSION_2025-12-17_RAG_Cloudflare_Integration.md - Posledná session

---

## 📝 SESSION WORKFLOW

1. Načítaj tento INIT_PROMPT
2. Skontroluj memory_user_edits (22 pravidiel)
3. **FOCUS: Vyriešiť Cloudflare blocking (Option 1 → 2 → 3)**
4. Pracuj step-by-step s confirmations
5. Na konci: "novy chat" → 3 artifacts + archive update

---

## 🎯 SUCCESS CRITERIA

**DONE WHEN:**
- ✅ Claude môže volať `https://n8n.icc.sk/rag/health` (200 OK)
- ✅ Claude môže volať `/search?query=...` (JSON response)
- ✅ Žiadne 403 errory
- ✅ Stable solution (nie dočasný hack)

**After RAG access working:**
- NEX Genesis Product Enrichment (v2.4 Phase 4)
- Btrieve → PostgreSQL migration pokračovanie
- n8n → Temporal migration

---

## 💡 TECHNICAL HINTS

### Cloudflare Workers Template
```javascript
export default {
  async fetch(request) {
    const url = new URL(request.url);
    
    if (url.pathname.startsWith('/rag')) {
      // Proxy to local RAG server
      const ragUrl = `http://localhost:8765${url.pathname.replace('/rag', '')}${url.search}`;
      return fetch(ragUrl, {
        method: request.method,
        headers: request.headers,
        body: request.body
      });
    }
    
    return new Response('Not Found', { status: 404 });
  }
};
```

### Anthropic IP Addresses
```
34.162.230.222
34.34.24.135
2a01:c846:cc3:7200:...
```

---

**Token Budget:** 190,000  
**Location:** C:\Development\nex-automat  
**Status:** 🔴 BLOCKED - Cloudflare access issue

---

**KONIEC INIT PROMPTU**