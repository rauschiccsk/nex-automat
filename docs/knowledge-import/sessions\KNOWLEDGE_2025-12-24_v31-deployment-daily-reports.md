# Session: NEX Automat v3.1 Deployment & Daily Reports

**Dátum:** 2025-12-24
**Status:** ✅ DONE

---

## Dokončené úlohy

### Telegram Security Fix
- Revoked 3 bot tokens (Admin, ICC, ANDROS)
- Aktualizovaný CREDENTIALS.md s novými tokenmi
- RAG reindexed

### Mágerstav v3.1 Deployment
- Git pull na Mágerstav server
- Service restart
- SMTP password fix (App Password)
- Daily Reports modul nasadený

### Daily Summary Reports
- Windows Task Scheduler: 18:00 Po-Pi
- Recipients: iccforai@gmail.com, mate.bognar.22@gmail.com
- Fix run_daily_report.py - použitie .env hodnôt

### Git Cleanup
- Odstránený docs/knowledge/ z Git (RAG-only)
- Customer-specific deployment system vytvorený

### Deploy System
- deploy/config/base.yaml
- deploy/config/magerstav.yaml  
- deploy/config/andros.yaml
- deploy/deploy.py

## Dôležité príkazy

```powershell
# Deploy analysis
python deploy/deploy.py --customer magerstav --dry-run
python deploy/deploy.py --customer andros --dry-run

# RAG update
python tools/rag/rag_update.py --new

# Daily report test
.\venv32\Scripts\python.exe apps\supplier-invoice-loader\scripts\run_daily_report.py
```

## Next Steps

1. ANDROS server hardware upgrade planning
2. ANDROS deployment
