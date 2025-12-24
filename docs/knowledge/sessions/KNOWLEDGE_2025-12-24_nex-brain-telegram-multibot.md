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
