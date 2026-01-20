# INIT PROMPT - ICC Windows Deployment

**Projekt:** nex-automat v3.0
**Úloha:** Dokončiť ICC deployment na Windows VM
**Developer:** Zoltán Rausch
**Dátum:** 2026-01-20

---

## 🎯 CIEĽ SESSION

Dokončiť ICC invoice processing systém na Windows VM (192.168.122.75).

---

## ✅ DOKONČENÉ (predchádzajúca session)

### Ubuntu Docker Stacks
- [x] ANDROS: PostgreSQL 5432, Temporal 7233, UI 8080
- [x] ICC: PostgreSQL 5433, Temporal 7234, UI 8082

### Windows VM - ANDROS
- [x] Git clone C:\ANDROS\nex-automat\
- [x] venv (64-bit) + venv32 (32-bit)
- [x] .env konfigurácia (worker + loader)
- [x] Windows Services (3x) - všetky Running
- [x] API health check OK (port 8001)

### Git Opravy
- [x] DB=postgres → DB=postgres12 (Temporal)
- [x] OAuth2 → Standard IMAP (email_activities.py)
- [x] Config template syntax errors
- [x] NEX_GENESIS_ENABLED pridané

---

## ⏳ ZOSTÁVA DOKONČIŤ

### Fáza 1: ICC Windows VM Setup
- [ ] Git clone C:\ICC\nex-automat\ (develop branch)
- [ ] Spustiť setup-icc-venv.ps1
- [ ] Skopírovať NSSM: `copy C:\Tools\nssm-2.24\win64\nssm.exe C:\ICC\nex-automat\tools\nssm\win64\`

### Fáza 2: ICC Konfigurácia
- [ ] Vytvoriť apps\supplier-invoice-worker\.env
- [ ] Vytvoriť apps\supplier-invoice-loader\.env
- [ ] Doinštalovať packages do venv32:
  ```powershell
  .\venv32\Scripts\Activate.ps1
  pip install rapidfuzz unidecode
  pip install -e packages\nexdata
  pip install -e packages\nex-staging
  ```
- [ ] Doinštalovať packages do venv:
  ```powershell
  .\venv\Scripts\Activate.ps1
  pip install pydantic-settings
  ```

### Fáza 3: ICC Windows Services
- [ ] Spustiť install-services-icc.ps1 (ako Admin)
- [ ] Vymazať __pycache__ pred štartom
- [ ] Start-Service NEX-*-ICC
- [ ] Overiť curl http://localhost:8002/health

### Fáza 4: Testovanie
- [ ] ANDROS: Poslať faktúru na andros.invoices@icc.sk
- [ ] ICC: Poslať faktúru na icc.invoices@icc.sk
- [ ] Skontrolovať Temporal UI (8080, 8082)

---

## 📋 ICC KONFIGURÁCIA

### apps\supplier-invoice-worker\.env
```
TEMPORAL_HOST=192.168.122.1
TEMPORAL_PORT=7234
TEMPORAL_NAMESPACE=default
TEMPORAL_TASK_QUEUE=icc-invoice-queue
IMAP_HOST=mail.webglobe.sk
IMAP_PORT=993
IMAP_USER=icc.invoices@icc.sk
IMAP_PASSWORD=Nex-Icc2026-Inv
IMAP_FOLDER=INBOX
IMAP_USE_SSL=true
FASTAPI_URL=http://localhost:8002
LS_API_KEY=ls-dev-key-change-in-production-2025
SMTP_HOST=mail.webglobe.sk
SMTP_PORT=465
SMTP_USER=icc.invoices@icc.sk
SMTP_PASSWORD=Nex-Icc2026-Inv
NOTIFY_EMAIL=rausch@icc.sk
LOG_LEVEL=INFO
```

### apps\supplier-invoice-loader\.env
```
DATABASE_URL=postgresql://nex_admin:Nex1968@192.168.122.1:5433/nex_automat
LS_API_KEY=ls-dev-key-change-in-production-2025
NEX_BASE_PATH=C:\ICC\NEX
NEX_IMPORT_PATH=C:\ICC\NEX\IMPORT
NEX_STAGING_PATH=C:\ICC\NEX\IMPORT\SUPPLIER-STAGING
NEX_ARCHIVE_PATH=C:\ICC\NEX\YEARACT\ARCHIV\SUPPLIER-INVOICES
BTRIEVE_DLL_PATH=C:\ICC\NEX\w3btrv7.dll
```

---

## 🖥️ PRÍSTUPY

### Windows VM
```
RDP: 100.107.134.104 (Tailscale)
User: Administrator
```

### Ubuntu Host
```bash
ssh andros@192.168.100.23
# Password: Andros-2026
```

---

## 📊 PORT MAPPING

| Service | ANDROS | ICC |
|---------|--------|-----|
| PostgreSQL | 5432 | 5433 |
| Temporal | 7233 | 7234 |
| Temporal UI | 8080 | 8082 |
| FastAPI Loader | 8001 | 8002 |

---

## 🚀 ZAČAŤ S

### Windows VM - PowerShell (Admin)

```powershell
# 1. Git clone ICC
cd C:\ICC
git clone -b develop https://github.com/rauschiccsk/nex-automat.git

# 2. Setup venv
cd C:\ICC\nex-automat
.\deployment\scripts\setup-icc-venv.ps1
```

---

## ⚠️ ZNÁME PROBLÉMY

1. **Python cache** - Vždy vymazať __pycache__ po git pull
2. **NSSM** - Treba skopírovať do tools\nssm\win64\
3. **Packages** - nexdata a nex-staging treba nainštalovať ako editable
4. **Port 8081** - Obsadený cadvisor, ICC UI používa 8082