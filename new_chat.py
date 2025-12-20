"""
New Chat Script - NEX Automat Project
Creates: SESSION_*.md, KNOWLEDGE_*.md, INIT_PROMPT, runs rag_update.py
"""
import subprocess
import sys
from datetime import datetime
from pathlib import Path

TODAY = datetime.now().strftime("%Y-%m-%d")
SESSION_NAME = "temporal-migration-implementation"

# Paths
DOCS_ARCHIVE = Path("docs/archive/sessions")
DOCS_KNOWLEDGE = Path("docs/knowledge")
INIT_PROMPT_PATH = Path("init_chat/INIT_PROMPT_NEW_CHAT.md")

# ============================================================
# SESSION ARCHIVE
# ============================================================
SESSION_CONTENT = f"""# Session: NEX Brain Telegram Bot + Temporal Migration Docs

**Dátum:** {TODAY}
**Projekt:** nex-automat
**Fokus:** NEX Brain UI + Temporal Migration Documentation

---

## DOKONČENÉ V TEJTO SESSION

### 1. NEX Brain UI Rozhodnutie
- ✅ Analýza 6 alternatív (Web, Desktop, Panel, Electron, CLI, Telegram)
- ✅ Finálne rozhodnutie:
  - Fáza 4a: Telegram Bot (MVP) - 2-3 dni
  - Fáza 4b: PySide6 Panel (Finálne) - 2 týždne
- ✅ Aktualizovaný NEX_BRAIN_PRODUCT.md

### 2. Telegram Bot Implementácia
- ✅ `apps/nex-brain/telegram/bot.py` - hlavný bot
- ✅ `apps/nex-brain/telegram/config.py` - konfigurácia
- ✅ Multi-tenant podpora (/tenant príkaz)
- ✅ RAG integrácia funguje
- ✅ Testované - všetky odpovede správne

### 3. Temporal Migration Documentation
- ✅ Analýza n8n workflow (JSON)
- ✅ Extrakcia IMAP konfigurácie
- ✅ Kompletný migračný dokument s Python kódom
- ✅ `docs/knowledge/strategic/N8N_TO_TEMPORAL_MIGRATION.md`
- ✅ Zaindexované v RAG

---

## KĽÚČOVÉ SÚBORY VYTVORENÉ

```
apps/nex-brain/telegram/
├── __init__.py
├── bot.py              # Telegram bot
├── config.py           # Settings
└── requirements.txt

docs/knowledge/strategic/
├── NEX_BRAIN_PRODUCT.md           # UI rozhodnutie
└── N8N_TO_TEMPORAL_MIGRATION.md   # Kompletný migračný plán
```

---

## KĽÚČOVÉ ROZHODNUTIA

1. **NEX Brain UI:** Telegram Bot (MVP) → PySide6 Panel (Finálne)
2. **Temporal:** Natívne Windows (BEZ DOCKERU)
3. **Produkčné boty:** Samostatný bot pre každú firmu (ICC, ANDROS)

---

## NEXT STEPS (pre nasledujúcu session)

### Priority #1: Temporal Migration - Phase 1 Setup
- [ ] Inštalácia Temporal Server na Windows
- [ ] Konfigurácia PostgreSQL pre Temporal
- [ ] Vytvorenie `apps/temporal-invoice-worker/` štruktúry

### Priority #2: Temporal Migration - Phase 2 Activities
- [ ] Implementácia email_activities.py
- [ ] Implementácia invoice_activities.py
- [ ] Implementácia notification_activities.py

---

## TECHNICKÉ POZNÁMKY

### Telegram Bot
- Token: Nastavený v environment
- API URL: http://localhost:8001/api/v1/chat
- Default tenant: ICC

### Temporal Migration
- Bez Dockeru (Windows Server 2012 kompatibilita)
- FastAPI na localhost (žiadny Cloudflare Tunnel)
- IMAP: Gmail App Password (nie OAuth2)

---

**Koniec session**
"""

# ============================================================
# KNOWLEDGE DOCUMENT
# ============================================================
KNOWLEDGE_CONTENT = f"""# Knowledge: NEX Brain Telegram + Temporal Docs

**Dátum:** {TODAY}
**Session:** nex-brain-telegram-temporal-docs

---

## Telegram Bot Pre NEX Brain

### Štruktúra
```
apps/nex-brain/telegram/
├── bot.py          # Hlavný bot s /start, /help, /tenant
├── config.py       # TELEGRAM_BOT_TOKEN, NEX_BRAIN_API_URL
└── requirements.txt # python-telegram-bot, httpx
```

### Spustenie
```powershell
$env:TELEGRAM_BOT_TOKEN='xxx'
$env:NEX_BRAIN_API_URL='http://localhost:8001'
python apps/nex-brain/telegram/bot.py
```

### API Endpoint
- URL: `http://localhost:8001/api/v1/chat`
- Method: POST
- Body: `{{"question": "...", "tenant": "icc"}}`
- Response: `{{"answer": "...", "tenant": "icc", "sources": [...]}}`

---

## UI Rozhodnutie

| Fáza | Typ | Trvanie | Status |
|------|-----|---------|--------|
| 4a | Telegram Bot (MVP) | 2-3 dni | ✅ Done |
| 4b | PySide6 Panel | 2 týždne | 🔵 Planned |

---

## Temporal Migration

### Kľúčové dokumenty
- `docs/knowledge/strategic/N8N_TO_TEMPORAL_MIGRATION.md` - Kompletný plán

### Architektúra (BEZ DOCKERU)
```
Gmail IMAP → Temporal Worker → FastAPI (localhost) → PostgreSQL
```

### Implementation Roadmap
1. Phase 1: Setup (1 týždeň)
2. Phase 2: Core Activities (1-2 týždne)
3. Phase 3: Workflow (1 týždeň)
4. Phase 4: Testing (1 týždeň)
5. Phase 5: Deployment (1 týždeň)
6. Phase 6: Migration (1 týždeň)

Celková doba: 6-8 týždňov

---

**Koniec knowledge dokumentu**
"""

# ============================================================
# INIT PROMPT
# ============================================================
INIT_PROMPT_CONTENT = f"""# INIT PROMPT - NEX Automat Project

**Projekt:** nex-automat  
**Current Status:** Temporal Migration - Phase 1 Setup
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** nex-brain-telegram-temporal-docs ({TODAY})

---

## ⚠️ KRITICKÉ: COLLABORATION RULES

**MUSÍŠ dodržiavať pravidlá z memory_user_edits!**

Kľúčové pravidlá:
- **Rule #7:** CRITICAL artifacts pre všetky dokumenty/kód
- **Rule #8:** Step-by-step, confirmation pred pokračovaním
- **Rule #5:** Slovak language, presná terminológia projektov
- **Rule #19:** "novy chat" = spustiť `python new_chat.py`
- **Rule #23:** RAG Workflow - Claude vypíše URL, user vloží, Claude fetchne

---

## 🔄 DOKONČENÉ MINULÚ SESSION

### NEX Brain Telegram Bot - COMPLETE
- ✅ Telegram bot funguje
- ✅ RAG integrácia
- ✅ Multi-tenant (/tenant)
- ✅ UI rozhodnutie zdokumentované

### Temporal Migration Docs - COMPLETE
- ✅ Kompletný migračný dokument
- ✅ Python kód pre všetky komponenty
- ✅ Windows Services setup
- ✅ Zaindexované v RAG

---

## 🎯 IMMEDIATE NEXT STEPS

### Priority #1: Temporal Setup (Phase 1)
1. Inštalácia Temporal Server na Windows (Go binary)
2. Konfigurácia PostgreSQL pre Temporal persistence
3. Vytvorenie `apps/temporal-invoice-worker/` štruktúry
4. Python dependencies

### Priority #2: Core Activities (Phase 2)
1. email_activities.py - IMAP polling
2. invoice_activities.py - FastAPI calls
3. notification_activities.py - SMTP

---

## 📂 KEY PATHS

```
apps/temporal-invoice-worker/          # NOVÝ - vytvoríme
├── activities/
├── workflows/
├── workers/
├── scheduler/
├── config/
└── tests/

docs/knowledge/strategic/
└── N8N_TO_TEMPORAL_MIGRATION.md      # Kompletný plán
```

---

## 🔍 RAG ACCESS

```
https://rag-api.icc.sk/search?query=temporal+migration+workflow&limit=10
```

---

**Token Budget:** 190,000  
**Location:** C:\\Development\\nex-automat

---

**KONIEC INIT PROMPTU**
"""


def main():
    print("=" * 70)
    print("NEW CHAT SCRIPT - NEX Automat")
    print("=" * 70)

    # 1. Create SESSION archive
    DOCS_ARCHIVE.mkdir(parents=True, exist_ok=True)
    session_file = DOCS_ARCHIVE / f"SESSION_{TODAY}_{SESSION_NAME.replace('-', '_')}.md"
    session_file.write_text(SESSION_CONTENT, encoding='utf-8')
    print(f"✅ SESSION: {session_file}")

    # 2. Create KNOWLEDGE document
    DOCS_KNOWLEDGE.mkdir(parents=True, exist_ok=True)
    knowledge_file = DOCS_KNOWLEDGE / f"KNOWLEDGE_{TODAY}_{SESSION_NAME.replace('-', '_')}.md"
    knowledge_file.write_text(KNOWLEDGE_CONTENT, encoding='utf-8')
    print(f"✅ KNOWLEDGE: {knowledge_file}")

    # 3. Create INIT_PROMPT
    INIT_PROMPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    INIT_PROMPT_PATH.write_text(INIT_PROMPT_CONTENT, encoding='utf-8')
    print(f"✅ INIT_PROMPT: {INIT_PROMPT_PATH}")

    # 4. Run RAG update
    print()
    print("=" * 70)
    print("RUNNING RAG UPDATE...")
    print("=" * 70)
    subprocess.run([sys.executable, "tools/rag/rag_update.py", "--new"])

    print()
    print("=" * 70)
    print("✅ NEW CHAT READY")
    print("=" * 70)
    print()
    print("Ďalšie kroky:")
    print("1. Git commit všetkých zmien")
    print("2. Otvoriť nový chat")
    print("3. Priložiť: init_chat/INIT_PROMPT_NEW_CHAT.md")
    print("=" * 70)


if __name__ == "__main__":
    main()