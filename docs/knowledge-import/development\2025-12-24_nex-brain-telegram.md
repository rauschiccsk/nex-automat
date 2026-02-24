# INIT PROMPT - NEX Brain Telegram Vylepšenia

**Projekt:** nex-automat / NEX Brain  
**Úloha:** Telegram Bot vylepšenia  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Odhad:** 1-2 dni

⚠️ **KRITICKÉ:** Dodržiavať pravidlá z memory_user_edits!

---

## 🎯 Cieľ

Vylepšiť NEX Brain Telegram Bot o lepšie formátovanie, históriu konverzácie a interaktívne prvky.

---

## ✅ Aktuálny stav

| Položka | Status |
|---------|--------|
| Telegram Bot základný | ✅ Funkčný |
| /start, /help, /tenant príkazy | ✅ Implementované |
| RAG integrácia | ✅ Funguje |
| Multi-tenant | ✅ Podporované |
| @NexBrainTest_bot | ✅ Development |

**Štruktúra:**
```
apps/nex-brain/telegram/
├── bot.py              # Hlavný bot
├── config.py           # Konfigurácia
└── requirements.txt    # Dependencies
```

**API Endpoint:**
- URL: `http://localhost:8001/api/v1/chat`
- Method: POST
- Body: `{"question": "...", "tenant": "icc"}`

---

## 📋 Úlohy na implementáciu

### 1. 🟡 Formátovanie odpovede (Medium)

**Cieľ:** Lepšia čitateľnosť odpovedí

**Implementácia:**
- [ ] Markdown formátovanie (bold, italic, code)
- [ ] Emoji pre lepšiu vizuálnu navigáciu
- [ ] Oddelenie sekcií v dlhších odpovediach
- [ ] Formátovanie zdrojov (sources) na konci

**Príklad:**
```
📋 **Odpoveď:**
Text odpovede s *dôležitými* časťami zvýraznenými.

📚 **Zdroje:**
• dokument1.md
• dokument2.md
```

### 2. 🟡 História konverzácie (Medium)

**Cieľ:** Pamätanie kontextu v rámci session

**Implementácia:**
- [ ] In-memory storage pre chat history (per user)
- [ ] Posielanie posledných N správ ako kontext
- [ ] /clear príkaz na reset histórie
- [ ] Timeout na automatický reset (napr. 30 min)

**Štruktúra:**
```python
conversation_history = {
    user_id: {
        "messages": [...],
        "last_activity": datetime,
        "tenant": "icc"
    }
}
```

### 3. 🟢 Inline tlačidlá (Low)

**Cieľ:** Rýchle akcie a follow-up otázky

**Implementácia:**
- [ ] InlineKeyboardMarkup pre akcie
- [ ] "Viac detailov" tlačidlo
- [ ] "Súvisiace témy" tlačidlá
- [ ] Feedback tlačidlá (👍/👎)

**Príklad:**
```python
keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("👍", callback_data="feedback_good"),
     InlineKeyboardButton("👎", callback_data="feedback_bad")],
    [InlineKeyboardButton("📖 Viac detailov", callback_data="more_details")]
])
```

### 4. 🟢 Logging a Analytics (Low)

**Cieľ:** Sledovanie používania pre zlepšenie

**Implementácia:**
- [ ] Ukladanie dotazov do PostgreSQL
- [ ] Timestamp, user_id, tenant, question, answer
- [ ] Feedback score ak poskytnutý
- [ ] Jednoduchý dashboard/report

**Tabuľka:**
```sql
CREATE TABLE telegram_logs (
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    tenant VARCHAR(50),
    question TEXT,
    answer TEXT,
    feedback VARCHAR(10),
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔧 Technické detaily

### Dependencies (aktuálne)
```
python-telegram-bot>=20.0
httpx>=0.25.0
```

### Spustenie
```powershell
$env:TELEGRAM_BOT_TOKEN='your-token'
$env:NEX_BRAIN_API_URL='http://localhost:8001'
python apps/nex-brain/telegram/bot.py
```

### Konfigurácia
```python
# config.py
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
NEX_BRAIN_API_URL = os.getenv("NEX_BRAIN_API_URL", "http://localhost:8001")
DEFAULT_TENANT = "icc"
HISTORY_MAX_MESSAGES = 10
HISTORY_TIMEOUT_MINUTES = 30
```

---

## 📊 Plánované boty

| Bot | Firma | Status |
|-----|-------|--------|
| @NexBrainTest_bot | Development | ✅ Funkčný |
| @NexBrainICC_bot | ICC s.r.o. | 🔵 Planned |
| @NexBrainAndros_bot | ANDROS s.r.o. | 🔵 Planned |

---

## ✅ Success Criteria

| Kritérium | Cieľ |
|-----------|------|
| Markdown formátovanie | Implementované |
| História konverzácie | 10 správ, 30 min timeout |
| Inline tlačidlá | Feedback + akcie |
| Logging | PostgreSQL tabuľka |

---

## 🔗 RAG Queries

```
https://rag-api.icc.sk/search?query=NEX+Brain+Telegram+bot+implementation&limit=5
https://rag-api.icc.sk/search?query=python-telegram-bot+inline+keyboard&limit=3
```

---

## 📝 Session Priority

1. **Formátovanie odpovede** - najviditeľnejší efekt
2. **História konverzácie** - zlepšenie UX
3. **Inline tlačidlá** - interaktivita
4. **Logging** - analytics

---

**Odhadovaný čas:**
- Formátovanie: 2-3 hodiny
- História: 3-4 hodiny
- Inline tlačidlá: 2-3 hodiny
- Logging: 2-3 hodiny
- **Celkom: 1-2 dni**