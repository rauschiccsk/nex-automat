# INIT PROMPT - UAE Legal RAG System Continuation

**Projekt:** nex-automat  
**Session:** Cabinet Decision 10/2019 Indexing + Telegram Bot Setup  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina s anglickou technickou terminológiou  
**Dátum:** 2026-01-09  

⚠️ **KRITICKÉ:** Dodržiavať pravidlá z memory_user_edits!

---

## 🎯 CURRENT FOCUS

**Dokončiť UAE Legal Tenant Integration:**
1. ✅ Cabinet Decision 10/2019 - zaindexovaný (Document ID: 1137, 35 chunks)
2. 🔄 **Pridať UAE Telegram bota** do multi-tenant systému
3. 🔄 **Otestovať RAG retrieval** cez Telegram bot
4. 📋 Pripraviť analýzu Federal Decree-Law 20/2018 (next TIER 1 document)

---

## 📊 ČO JE HOTOVÉ

### Cabinet Decision 10/2019 Analysis ✅
| Komponenta | Status | Detail |
|------------|--------|--------|
| PDF Extraction | ✅ | 41 pages, 62 articles |
| Comprehensive Analysis | ✅ | 30,000 words, defense-focused |
| Markdown Document | ✅ | `Cabinet_Decision_10_2019_Executive_Regulation_Analysis.md` |
| RAG Indexing | ✅ | Doc ID 1137, 35 chunks, 34K tokens |
| Article-by-Article Breakdown | ✅ | All 62 articles analyzed |
| Defense Checklists | ✅ | Appendix A + B created |
| Comparison Framework | ✅ | CD 10/2019 vs 134/2025 |

### RAG System Status ✅
- **Database:** nex_automat_rag (PostgreSQL)
- **Documents:** 86 (increased from 85)
- **Chunks:** 311 (increased from 276)
- **Embedding Model:** sentence-transformers/all-MiniLM-L6-v2 (384 dims)
- **Multi-tenant:** Funguje (ICC, ANDROS tenants verified)

### NEX Brain API ✅
- **Port:** 8003 (8001 obsadený)
- **Status:** Running (Uvicorn)
- **Endpoints:** `/api/v1/chat`, `/api/v1/tenants`

---

## 🚨 AKTUÁLNY PROBLÉM

### **UAE Telegram Bot - Chýba Konfigurácia**

**Situácia:**
- Multi-bot runner má len: Admin, ICC, ANDROS
- **UAE tenant nie je nakonfigurovaný**
- Bot beží, ale nemá UAE instanciu

**Čo treba urobiť:**

#### KROK 1: Pridať UAE Bot do `multi_bot.py`
```python
# File: apps/nex-brain/telegram/multi_bot.py
# Pridať do BOTS list:

BotConfig(
    token=os.getenv("TELEGRAM_BOT_TOKEN_UAE"),
    tenant="uae",
    requires_approval=True,
    name="UAE"
),
```

#### KROK 2: Vytvoriť Token v BotFather (ak neexistuje)
```
1. Telegram: @BotFather
2. /newbot
3. Name: NEX Brain UAE
4. Username: @NexBrainUAE_bot (alebo podobné)
5. Copy token
```

#### KROK 3: Pridať Token do `.env`
```bash
# File: .env (root directory)
TELEGRAM_BOT_TOKEN_UAE=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz...
```

#### KROK 4: Reštartovať Bot
```bash
cd C:\Development
ex-automatpps
ex-brain	elegram
# Ctrl+C (stop current)
python multi_bot.py
# Verify logs: "Inicializujem NEX Brain UAE..."
```

---

## 🔍 VEDĽAJŠÍ PROBLÉM (Lower Priority)

### CLI Search Tool Bug
```bash
python -m tools.rag "query"
# Error: 'SearchResult' object is not subscriptable
```

**Impact:** CLI nefunguje, ale Telegram bot používa iný code path (cez API), takže by mal fungovať.

**Root Cause:** `tools/rag/__main__.py` pristupuje k SearchResult ako dictionary (`r['score']`), ale SearchResult je objekt.

**Fix (ak potrebné):**
```python
# V __main__.py, zmeniť:
score = r['score']  # ❌
# Na:
score = r.score     # ✅
```

---

## 📋 NEXT STEPS (Priority Order)

### 1. **UAE Telegram Bot Setup** (URGENT)
- [ ] Vytvoriť UAE bot v BotFather (ak neexistuje)
- [ ] Pridať token do `.env`
- [ ] Pridať BotConfig do `multi_bot.py`
- [ ] Reštartovať bot
- [ ] Verify: "Inicializujem NEX Brain UAE..." v logs

### 2. **Test UAE RAG Retrieval**
Test queries cez Telegram:
```
1. "What is reasonable grounds to suspect in Cabinet Decision 10/2019?"
   Expected: Explanation of Article 17 standard

2. "CDD threshold AED 55000"
   Expected: Article 6 - occasional transactions threshold

3. "FIU administrative freeze 7 days"
   Expected: Article 46 - Governor's freezing power

4. "Article 47 contest freezing order"
   Expected: Right to contest, 14-day decision deadline

5. "beneficial owner 25 percent"
   Expected: Article 9 - beneficial owner identification threshold
```

### 3. **Verify Tenant Isolation**
- Test ICC bot → should NOT see UAE documents
- Test ANDROS bot → should NOT see UAE documents
- Test UAE bot → should ONLY see UAE documents

### 4. **Fix CLI Search Bug** (Optional)
- Locate bug in `__main__.py` or `api.py`
- Change dictionary access to object attribute access
- Test: `python -m tools.rag "test query"`

### 5. **Prepare Next TIER 1 Document**
- **Federal Decree-Law 20/2018** (parent law)
  - Cabinet Decision 10/2019 is executive regulation FOR this law
  - Essential for understanding legal framework
  - Similar analysis approach as CD 10/2019

---

## 🔗 IMPORTANT FILES & PATHS

### UAE Documents
```
docs/knowledge/tenants/uae/
├── cabinet_decisions/
│   └── Cabinet_Decision_10_2019_Executive_Regulation_Analysis.md ✅
├── federal_laws/
│   ├── Federal_Decree_Law_10_2025_AML.md ✅
│   └── Federal_Decree_Law_38_2022_Criminal_Procedure.md ✅
```

### Telegram Bot Config
```
apps/nex-brain/telegram/
├── multi_bot.py         ← ADD UAE BOT HERE
├── config.py            ← Port 8003 (verified)
└── .env (root)          ← ADD TELEGRAM_BOT_TOKEN_UAE
```

### RAG Tools
```
tools/rag/
├── rag_reindex.py      # Manual indexing
├── __main__.py         # CLI search (broken)
├── api.py              # RAG API (working)
└── indexer.py          # Indexing logic
```

---

## 🎓 SYSTEMATIC APPROACH REMINDERS

### Pravidlá z userMemories:
1. ✅ **Krok-za-krokom riešenie** (nie veľa info naraz)
2. ✅ **Token info na konci každej odpovede**
3. ✅ **Systematický troubleshooting** (jeden príkaz → output → analýza)
4. ✅ **Slovak + English technical terms**
5. ✅ **40 rokov skúseností = preferencia tested solutions**

### Token Budget Tracking:
- **Session start:** 190,000 tokens
- **Always report at end:**
  - Used: X / 190,000 (Y%)
  - Remaining: Z (W%)

---

## 📊 RAG QUERY FOR CONTEXT

Ak potrebuješ dodatočný kontext z predošlých sessions:

```
https://rag-api.icc.sk/search?query=telegram+bot+configuration+multi+tenant+uae&limit=5
https://rag-api.icc.sk/search?query=cabinet+decision+indexing+rag&limit=5
https://rag-api.icc.sk/search?query=nex+brain+api+port+8003&limit=5
```

---

## ✅ SUCCESS CRITERIA

**Session is complete when:**
1. ✅ UAE Telegram bot beží a odpovedá
2. ✅ Test queries z UAE legal documents fungujú
3. ✅ Tenant isolation verified (ICC/ANDROS nevidia UAE docs)
4. ✅ (Optional) CLI search bug opravený
5. 📋 Next document (FD-L 20/2018) pripravený na analýzu

---

## 🚀 START COMMAND

```bash
# 1. Otvor multi_bot.py
notepad apps
ex-brain	elegram\multi_bot.py

# 2. Pridaj UAE BotConfig (see KROK 1 above)

# 3. Pridaj token do .env
notepad .env
# TELEGRAM_BOT_TOKEN_UAE=...

# 4. Reštartuj bot
cd apps
ex-brain	elegram
python multi_bot.py

# 5. Test v Telegram
# Send: "What is reasonable grounds to suspect?"
```

---

**Ready to continue!** 🎯
