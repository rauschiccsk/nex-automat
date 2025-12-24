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
