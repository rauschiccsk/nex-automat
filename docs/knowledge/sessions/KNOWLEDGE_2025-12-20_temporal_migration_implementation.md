# Knowledge: NEX Brain Telegram + Temporal Docs

**Dátum:** 2025-12-20
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
- Body: `{"question": "...", "tenant": "icc"}`
- Response: `{"answer": "...", "tenant": "icc", "sources": [...]}`

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
