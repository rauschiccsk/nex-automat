# Knowledge: ANDROS/ICC Multi-Tenant Deployment

**Dátum:** 2026-01-20
**Session:** andros-icc-deployment
**Status:** ANDROS ✅ Complete, ICC ⏳ Pending

---

## Dokončené úlohy

### 1. Deployment Infrastructure (Git)

Vytvorené súbory v `deployment/`:

```
deployment/
├── docker/
│   ├── docker-compose.andros.yml    # PostgreSQL, Temporal, UI
│   ├── docker-compose.icc.yml       # PostgreSQL, Temporal, UI
│   ├── .env.andros.example
│   ├── .env.icc.example
│   ├── .env.worker.andros.example
│   ├── .env.worker.icc.example
│   ├── .env.loader.andros.example
│   └── .env.loader.icc.example
└── scripts/
    ├── setup-andros-venv.ps1
    ├── setup-icc-venv.ps1
    ├── install-services-andros.ps1
    └── install-services-icc.ps1
```

### 2. Ubuntu Docker Stacks

**ANDROS Stack:**
- nex-postgres-andros: 5432 ✅
- nex-temporal-andros: 7233 ✅
- nex-temporal-ui-andros: 8080 ✅

**ICC Stack:**
- nex-postgres-icc: 5433 ✅
- nex-temporal-icc: 7234 ✅
- nex-temporal-ui-icc: 8082 ✅ (zmenené z 8081 kvôli cadvisor)

### 3. Windows VM - ANDROS Services

| Service | Status | Python | Port |
|---------|--------|--------|------|
| NEX-Invoice-Worker-ANDROS | ✅ Running | venv (64-bit) | - |
| NEX-Polling-Scheduler-ANDROS | ✅ Running | venv (64-bit) | - |
| NEX-Automat-Loader-ANDROS | ✅ Running | venv32 (32-bit) | 8001 |

---

## Opravy počas deployment

### 1. Temporal DB driver
- **Problém:** `DB=postgres` nefunguje
- **Riešenie:** Zmeniť na `DB=postgres12`
- **Commit:** af1336f

### 2. OAuth2 → Standard IMAP
- **Problém:** Kód používal Gmail OAuth2
- **Riešenie:** Upravený `email_activities.py` pre štandardný IMAP
- **Commit:** 41b563b

### 3. Config template syntax error
- **Problém:** Dokumentácia bez `#` komentárov
- **Riešenie:** Pridané `#` pred dokumentáciu
- **Commit:** 19a0d3e

### 4. Chýbajúca NEX_GENESIS_ENABLED
- **Problém:** `AttributeError: 'NEX_GENESIS_ENABLED'`
- **Riešenie:** Pridané do config_template.py
- **Commit:** (posledný)

### 5. Chýbajúce Python packages (venv32)
Manuálne doinštalované:
- rapidfuzz
- unidecode
- nexdata (editable)
- nex-staging (editable)

---

## Port Mapping

| Service | ANDROS | ICC |
|---------|--------|-----|
| PostgreSQL | 5432 | 5433 |
| Temporal | 7233 | 7234 |
| Temporal UI | 8080 | 8082 |
| FastAPI Loader | 8001 | 8002 |

---

## Dôležité cesty

### Ubuntu Host (192.168.100.23)
- `/opt/nex-automat/` - Docker compose súbory
- `/opt/nex-automat-src/` - Git repozitár
- `/data/docker-volumes/andros/` - ANDROS volumes
- `/data/docker-volumes/icc/` - ICC volumes

### Windows VM (192.168.122.75)
- `C:\ANDROS\nex-automat\` - ANDROS deployment
- `C:\ICC\nex-automat\` - ICC deployment (pending)
- `C:\Tools\nssm-2.24\` - NSSM binaries

---

## Konfigurácia

### ANDROS .env (worker)
```
TEMPORAL_HOST=192.168.122.1
TEMPORAL_PORT=7233
IMAP_HOST=mail.webglobe.sk
IMAP_USER=andros.invoices@icc.sk
IMAP_PASSWORD=Nex-Andros2026-Inv
```

### ANDROS .env (loader)
```
DATABASE_URL=postgresql://nex_admin:Nex1968@192.168.122.1:5432/nex_automat
LS_API_KEY=ls-dev-key-change-in-production-2025
```

---

## Príkazy

### Ubuntu - Docker
```bash
# ANDROS stack
docker compose -f docker-compose.andros.yml --env-file .env.andros up -d

# ICC stack
docker compose -f docker-compose.icc.yml --env-file .env.icc up -d

# Logy
docker logs nex-temporal-andros -f --tail 50
docker logs nex-temporal-icc -f --tail 50
```

### Windows - Services
```powershell
# Status
Get-Service NEX-*-ANDROS

# Reštart
Get-Service NEX-*-ANDROS | Restart-Service

# Logy
type C:\ANDROS\nex-automat\logs\services\*.log | Select-Object -Last 50
```

---

## Zostáva dokončiť

1. **ICC Windows deployment:**
   - Git clone C:\ICC\nex-automat
   - setup-icc-venv.ps1
   - .env konfigurácia
   - install-services-icc.ps1
   - Doinštalovať packages (nexdata, nex-staging)

2. **Testovanie:**
   - ANDROS: Poslať faktúru na andros.invoices@icc.sk
   - ICC: Poslať faktúru na icc.invoices@icc.sk

3. **Dokumentácia:**
   - Aktualizovať DEPLOYMENT_ANDROS_ICC.md
   - RAG reindex