#!/usr/bin/env python3
"""
New Chat Template - NEX Automat
===============================
TEMPLATE: Tento súbor je template. Claude doplní len premenné v sekcii CONFIG.

Použitie:
1. Claude skopíruje tento template
2. Doplní SESSION_DATE, SESSION_NAME, KNOWLEDGE_CONTENT, INIT_PROMPT
3. User uloží ako scripts/new_chat.py a spustí

Tento template NEMENÍME - je otestovaný a funkčný.
"""
import sys
import subprocess
from pathlib import Path

# =============================================================================
# CONFIG - CLAUDE DOPLNÍ TIETO PREMENNÉ
# =============================================================================

SESSION_DATE = "2025-12-24"  # YYYY-MM-DD
SESSION_NAME = "nex-brain-telegram-multibot"  # krátky názov bez medzier

KNOWLEDGE_CONTENT = """\
# NEX Brain Telegram Multi-Bot System

**Dátum:** 2025-12-24
**Status:** ✅ DONE
**Projekt:** nex-automat / NEX Brain

---

## Prehľad

NEX Brain Telegram integrácia s multi-bot architektúrou, schvaľovaním používateľov a centrálnym admin rozhraním.

## Telegram Boty

| Bot | Username | Token | Účel |
|-----|----------|-------|------|
| Admin | @ai_dev_automatin_bot | 8585064403:AAFHf_xXeA43QBWUcObjt6pYA3xOFPjVpjg | Admin rozhranie, testovanie, /tenant prepínanie |
| ICC | @NexBrainIcc_bot | 8487965429:AAFmbe18rJo9NMLV7Ams-_HkHCrcIeXHAYM | Pre ICC používateľov, vyžaduje schválenie |
| ANDROS | @NexBrainAndros_bot | 8178049225:AAGjwzT2-VcaSWJQADQcMHkvTiY8eMvgj9A | Pre ANDROS používateľov, vyžaduje schválenie |

## Štruktúra súborov

```
apps/nex-brain/telegram/
├── .env                    # Tokeny a konfigurácia
├── config.py               # Multi-bot settings s python-dotenv
├── db.py                   # PostgreSQL logging modul
├── multi_bot.py            # Hlavný multi-bot systém
├── user_manager.py         # Správa používateľov a schvaľovanie
├── requirements.txt        # Dependencies
├── create_table.sql        # telegram_logs tabuľka
└── create_users_table.sql  # telegram_users + telegram_admins tabuľky
```

## Databázové tabuľky

### telegram_logs
- Logging všetkých dotazov a odpovedí
- Feedback (good/bad) z inline tlačidiel
- Response time tracking

### telegram_users
- user_id, username, first_name
- tenant (icc/andros)
- status (pending/approved/rejected)
- requested_at, approved_at, approved_by

### telegram_admins
- Zoznam admin používateľov

## Admin príkazy (@ai_dev_automatin_bot)

| Príkaz | Popis |
|--------|-------|
| /pending | Zoznam čakajúcich používateľov |
| /approve {user_id} {tenant} | Schválenie používateľa |
| /reject {user_id} {tenant} | Zamietnutie používateľa |
| /users | Zoznam schválených používateľov |
| /tenant {icc/andros} | Zmena tenant pre testovanie |

## Funkcie botov

- ✅ Markdown formátovanie odpovedí + emoji
- ✅ Zobrazenie zdrojov z RAG
- ✅ História konverzácie (10 správ, 30 min timeout)
- ✅ Inline feedback tlačidlá (👍/👎)
- ✅ PostgreSQL logging
- ✅ Multi-tenant (ICC, ANDROS)
- ✅ Schvaľovanie nových používateľov
- ✅ Admin notifikácie o nových žiadostiach

## Flow schvaľovania

1. Nový používateľ napíše /start na @NexBrainIcc_bot
2. Bot vytvorí záznam so status=pending
3. Admin dostane notifikáciu na @ai_dev_automatin_bot
4. Admin schváli: /approve {user_id} icc
5. Používateľ dostane správu "Boli ste schválení"
6. Používateľ môže používať bota

## Spustenie

```powershell
cd apps/nex-brain/telegram
python multi_bot.py
```

Spustí všetky 3 boty v jednom procese.

## Konfigurácia (.env)

```env
# Tokeny
TELEGRAM_ADMIN_BOT_TOKEN=8585064403:AAFHf_xXeA43QBWUcObjt6pYA3xOFPjVpjg
TELEGRAM_ICC_BOT_TOKEN=8487965429:AAFmbe18rJo9NMLV7Ams-_HkHCrcIeXHAYM
TELEGRAM_ANDROS_BOT_TOKEN=8178049225:AAGjwzT2-VcaSWJQADQcMHkvTiY8eMvgj9A

# API
NEX_BRAIN_API_URL=http://localhost:8001

# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=nex_automat_rag
POSTGRES_USER=postgres
```

## Dependencies

```
python-telegram-bot>=20.0
httpx>=0.25.0
pg8000>=1.30.0
python-dotenv>=1.0.0
```

## Admin User ID

Zoltán: 7204918893 (hardcoded v multi_bot.py pre notifikácie)
"""

INIT_PROMPT = """\
# INIT PROMPT - NEX Brain Telegram

**Projekt:** nex-automat / NEX Brain
**Modul:** Telegram Multi-Bot System
**Status:** ✅ Kompletný
**Developer:** Zoltán (40 rokov skúseností)
**Jazyk:** Slovenčina

⚠️ KRITICKÉ: Dodržiavať pravidlá z memory_user_edits!

---

## ✅ Dokončené

| Funkcia | Status |
|---------|--------|
| Multi-bot architektúra | ✅ |
| Admin bot (@ai_dev_automatin_bot) | ✅ |
| ICC bot (@NexBrainIcc_bot) | ✅ |
| ANDROS bot (@NexBrainAndros_bot) | ✅ |
| Schvaľovanie používateľov | ✅ |
| Admin notifikácie | ✅ |
| PostgreSQL logging | ✅ |
| Feedback tlačidlá | ✅ |
| História konverzácie | ✅ |

## 🔧 Technické detaily

**Spustenie:**
```powershell
cd apps/nex-brain/telegram
python multi_bot.py
```

**Admin príkazy:**
- /pending - čakajúci
- /approve {user_id} {tenant}
- /reject {user_id} {tenant}
- /users - schválení
- /tenant - zmena tenant

## 📋 RAG Query

```
https://rag-api.icc.sk/search?query=NEX+Brain+Telegram+bot+multibot&limit=5
```
"""


# =============================================================================
# TEMPLATE CODE - NEMENÍME
# =============================================================================

def get_base_dir() -> Path:
    """Získa base directory projektu."""
    # Ak sme v nex-automat adresári
    cwd = Path.cwd()
    if cwd.name == "nex-automat":
        return cwd
    # Ak sme v scripts/
    if cwd.name == "scripts" and cwd.parent.name == "nex-automat":
        return cwd.parent
    # Ak sme niekde inde, skús nájsť nex-automat
    for parent in cwd.parents:
        if parent.name == "nex-automat":
            return parent
    # Fallback na cwd
    return cwd


def main():
    print("=" * 60)
    print("NEW CHAT SCRIPT")
    print("=" * 60)

    BASE_DIR = get_base_dir()
    print(f"📁 Base directory: {BASE_DIR}")

    # Verify we're in correct directory
    if not (BASE_DIR / "apps").exists():
        print(f"❌ ERROR: Not in nex-automat directory!")
        print(f"   Current: {Path.cwd()}")
        print(f"   Expected: C:\\Development\\nex-automat")
        sys.exit(1)

    DOCS_DIR = BASE_DIR / "docs"
    KNOWLEDGE_DIR = DOCS_DIR / "knowledge" / "sessions"
    SESSION_DIR = DOCS_DIR / "sessions"

    # Ensure directories exist
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
    SESSION_DIR.mkdir(parents=True, exist_ok=True)

    session_filename = f"SESSION_{SESSION_DATE}_{SESSION_NAME}.md"
    knowledge_filename = f"KNOWLEDGE_{SESSION_DATE}_{SESSION_NAME}.md"

    # 1. Save SESSION file
    session_file = SESSION_DIR / session_filename
    session_file.write_text(KNOWLEDGE_CONTENT, encoding="utf-8")
    print(f"✅ SESSION saved: {session_file}")

    # 2. Save KNOWLEDGE file
    knowledge_file = KNOWLEDGE_DIR / knowledge_filename
    knowledge_file.write_text(KNOWLEDGE_CONTENT, encoding="utf-8")
    print(f"✅ KNOWLEDGE saved: {knowledge_file}")

    # 3. Save INIT_PROMPT
    init_file = BASE_DIR / "INIT_PROMPT.md"
    init_file.write_text(INIT_PROMPT, encoding="utf-8")
    print(f"✅ INIT_PROMPT saved: {init_file}")

    # 4. Run RAG update
    print()
    print("=" * 60)
    print("Running RAG update...")
    print("=" * 60)

    rag_script = BASE_DIR / "tools" / "rag" / "rag_update.py"
    if not rag_script.exists():
        print(f"⚠️ RAG script not found: {rag_script}")
    else:
        # Use main venv Python, not worker venv
        main_venv_python = BASE_DIR / "venv" / "Scripts" / "python.exe"
        if not main_venv_python.exists():
            print(f"⚠️ Main venv not found: {main_venv_python}")
            print("   Skipping RAG update. Run manually:")
            print(f"   cd {BASE_DIR}")
            print(f"   .\\venv\\Scripts\\Activate.ps1")
            print(f"   python tools/rag/rag_update.py --new")
        else:
            try:
                # Set UTF-8 encoding for subprocess
                env = {**subprocess.os.environ, "PYTHONIOENCODING": "utf-8"}
                result = subprocess.run(
                    [str(main_venv_python), str(rag_script), "--new"],
                    cwd=str(BASE_DIR),
                    check=True,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    env=env
                )
                print(result.stdout)
                print("✅ RAG updated")
            except subprocess.CalledProcessError as e:
                print(f"⚠️ RAG update failed: {e}")
                if e.stdout:
                    print(f"STDOUT: {e.stdout}")
                if e.stderr:
                    print(f"STDERR: {e.stderr}")
                print()
                print("Run manually:")
                print(f"   .\\venv\\Scripts\\Activate.ps1")
                print(f"   python tools/rag/rag_update.py --new")

    print()
    print("=" * 60)
    print("✅ DONE!")
    print()
    print("Next steps:")
    print(f"  1. Git commit: git add -A && git commit -m 'Session {SESSION_DATE}'")
    print(f"  2. Start new chat with INIT_PROMPT.md")
    print("=" * 60)


if __name__ == "__main__":
    main()