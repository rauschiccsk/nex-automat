# ANDROS/ICC Multi-Tenant Deployment Guide

**Created:** 2026-01-20
**Status:** READY FOR DEPLOYMENT

---

## Prehľad

Dva izolované invoice processing systémy na zdieľanom ANDROS serveri.

| Zákazník | PostgreSQL | Temporal | Temporal UI | FastAPI |
|----------|------------|----------|-------------|---------|
| ANDROS | 5432 | 7233 | 8080 | 8001 |
| ICC | 5433 | 7234 | 8081 | 8002 |

---

## Architektúra

### Ubuntu Host (192.168.100.23)
- Docker: ANDROS stack (docker-compose.andros.yml)
- Docker: ICC stack (docker-compose.icc.yml)
- Volumes: /data/docker-volumes/andros/, /data/docker-volumes/icc/

### Windows VM (192.168.122.75)
- C:\ANDROS\nex-automat\ - ANDROS deployment
- C:\ICC\nex-automat\ - ICC deployment
- 6 Windows Services (3 per customer)

---

## Deployment kroky

### 1. Ubuntu - Docker stacks
```bash
ssh andros@192.168.100.23
cd /opt/nex-automat
git pull
# ANDROS stack
cp deployment/docker/.env.andros.example deployment/docker/.env.andros
# Edit .env.andros - set POSTGRES_PASSWORD
docker compose -f deployment/docker/docker-compose.andros.yml --env-file deployment/docker/.env.andros up -d
# ICC stack
cp deployment/docker/.env.icc.example deployment/docker/.env.icc
docker compose -f deployment/docker/docker-compose.icc.yml --env-file deployment/docker/.env.icc up -d
```

### 2. Windows VM - ANDROS
```powershell
cd C:\ANDROS\nex-automat
git pull
.\deployment\scripts\setup-andros-venv.ps1
# Copy and edit .env files for worker and loader
# Run as Admin:
.\deployment\scripts\install-services-andros.ps1
Get-Service NEX-*-ANDROS | Start-Service
```

### 3. Windows VM - ICC
```powershell
cd C:\ICC\nex-automat
git pull
.\deployment\scripts\setup-icc-venv.ps1
# Copy and edit .env files
# Run as Admin:
.\deployment\scripts\install-services-icc.ps1
Get-Service NEX-*-ICC | Start-Service
```

---

## Konfiguračné súbory

| Template | Destination |
|----------|-------------|
| .env.andros.example | /opt/nex-automat/deployment/docker/.env.andros |
| .env.worker.andros.example | C:\ANDROS\nex-automat\apps\supplier-invoice-worker\.env |
| .env.loader.andros.example | C:\ANDROS\nex-automat\apps\btrieve-loader\.env |

(Rovnako pre ICC)

---

## Windows Services

| Service | Customer | Python | Port |
|---------|----------|--------|------|
| NEX-Invoice-Worker-ANDROS | ANDROS | 64-bit | - |
| NEX-Polling-Scheduler-ANDROS | ANDROS | 64-bit | - |
| NEX-Automat-Loader-ANDROS | ANDROS | 32-bit | 8001 |
| NEX-Invoice-Worker-ICC | ICC | 64-bit | - |
| NEX-Polling-Scheduler-ICC | ICC | 64-bit | - |
| NEX-Automat-Loader-ICC | ICC | 32-bit | 8002 |

---

## Testovanie

### Temporal UI
- ANDROS: http://192.168.100.23:8080
- ICC: http://192.168.100.23:8081

### PostgreSQL
```bash
# ANDROS
psql -h 192.168.100.23 -p 5432 -U nex_admin -d nex_automat
# ICC
psql -h 192.168.100.23 -p 5433 -U nex_admin -d nex_automat
```

### Windows Services
```powershell
Get-Service NEX-* | Format-Table Name, Status
```

---

## Email konfigurácia

| Customer | Email | Server |
|----------|-------|--------|
| ANDROS | andros.invoices@icc.sk | mail.webglobe.sk |
| ICC | icc.invoices@icc.sk | mail.webglobe.sk |

IMAP: 993 (SSL), SMTP: 465 (SSL)
