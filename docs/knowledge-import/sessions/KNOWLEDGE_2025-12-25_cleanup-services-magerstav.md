# Session: Cleanup & Services Mágerstav

**Dátum:** 2025-12-25
**Status:** ✅ DONE

---

## Dokončené úlohy

- cleanup_databases.py script vytvorený (SQLite + PostgreSQL)
- PostgreSQL staging vyčistený (8 faktúr, 7 položiek)
- Staré adresáre odstránené (cloudflared-magerstav, invoice-loader)
- NSSM obnovený do C:\Deployment\nex-automat\tools\nssm\
- Worker settings fix - pridané extra='ignore' pre Pydantic v2
- Všetky NEX služby spustené (NEXAutomat, NEX-Invoice-Worker, NEX-Polling-Scheduler, NEX-Temporal-Server)
- CloudflaredMagerstav služba odstránená (nepoužívaná)
- Git synchronizácia Development → Deployment

## Vytvorené súbory

- scripts/cleanup_databases.py - vymaže SQLite + PostgreSQL dáta
- scripts/01_fix_worker_settings.py - fix pre Pydantic v2 extra fields

## Dôležité príkazy

```powershell
# Cleanup databáz
python scripts/cleanup_databases.py

# Windows Services
Get-Service NEX*
Start-Service NEX*
Stop-Service NEX* -Force

# Služby continue z Paused stavu
Get-Service NEX* | ForEach-Object { & sc.exe continue $_.Name }
```

## Lessons Learned

1. Pydantic v2 defaultne zakazuje extra fieldy - potrebné `extra = 'ignore'` v Config
2. NSSM služby v Paused stave vyžadujú `sc.exe continue` pred reštartom
3. Port konflikt (10048) - vždy skontrolovať `netstat -ano | findstr :PORT`
