---
title: MAGER CI/CD Deployment
category: infrastructure
tags: [ci-cd, github-actions, mager, docker, windows]
created: 2026-01-29
---

# MAGER CI/CD Deployment

## Architektúra

MAGER používa hybridný model - Docker workers + Windows services pre Btrieve závislosť.

### Komponenty

| Komponenta | Prostredie | Port | Účel |
|------------|------------|------|------|
| PostgreSQL | Windows Service | 5432 | Databáza |
| Temporal | Windows Service | 7233, 8233 | Workflow orchestrácia |
| Invoice-Worker | Docker | - | Temporal worker |
| Polling-Scheduler | Docker | - | Cron scheduler (5 min) |
| Btrieve-Loader | Windows Service | 8001 | REST API proxy pre NEX Genesis |

### Prečo hybridný model

Btrieve (Pervasive PSQL Workgroup) je len 32-bit. Docker kontajnery sú 64-bit Linux. Btrieve-Loader ostáva Windows Service kým neprebehne migrácia NEX Genesis → PostgreSQL.

## GitHub Actions

### Workflow

Súbor: `.github/workflows/deploy.yml`

Trigger: `workflow_dispatch` s inputom `customer: [ANDROS, MAGER]`

### MAGER Job

```yaml
deploy-mager:
  runs-on: [self-hosted, MAGER]
  environment: production-MAGER
  steps:
    - Git Pull (C:\opt\nex-automat-src)
    - Copy docker-compose.yml
    - Docker Compose Up
    - Restart Btrieve-Loader
    - Health Check
```

### Runner

| Parameter | Hodnota |
|-----------|---------|
| Názov | mager-runner |
| Labels | MAGER, self-hosted, Windows |
| Adresár | C:\github-runner |
| Služba | actions.runner.rauschiccsk-nex-automat.mager-runner |

## Adresárová štruktúra

```
C:\opt\
├── nex-automat\           # Deployment (docker-compose.yml, .env)
└── nex-automat-src\       # Git repository clone
```

## Docker Compose

Súbor: `deploy/mager/docker-compose.yml`

Workers sa pripájajú na Windows služby cez `host.docker.internal`:

| Premenná | Hodnota |
|----------|---------|
| TEMPORAL_HOST | host.docker.internal |
| TEMPORAL_PORT | 7233 |
| POSTGRES_HOST | host.docker.internal |
| POSTGRES_PORT | 5432 |
| FASTAPI_URL | http://host.docker.internal:8001 |

## Konfigurácia

### .env súbor

Umiestnenie: `C:\opt\nex-automat\.env`

Povinné premenné:
- POSTGRES_PASSWORD
- IMAP_USER, IMAP_PASSWORD (Gmail App Password)
- LS_API_KEY
- MARSO_API_KEY (voliteľné)

### Git safe.directory

Pre SYSTEM account (GitHub runner):

```powershell
git config --system --add safe.directory C:/opt/nex-automat-src
```

### PowerShell ExecutionPolicy

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
```

## Manuálny deployment

```powershell
cd C:\opt\nex-automat
docker compose pull
docker compose up -d
Restart-Service NEX-BtrieveLoader
docker compose ps
```

## Troubleshooting

### Port konflikt

Ak Docker hlási "port already allocated", skontroluj či Windows služby nepoužívajú rovnaké porty:

```powershell
netstat -ano | findstr :5432
netstat -ano | findstr :7233
```

### Git dubious ownership

```powershell
git config --system --add safe.directory C:/opt/nex-automat-src
```

### PowerShell scripts disabled

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
```

### Docker Desktop nefunguje

1. Over že Docker Desktop beží
2. Over WSL2: `wsl --status`
3. Reštartuj Docker Desktop

## Porovnanie ANDROS vs MAGER

| Aspekt | ANDROS | MAGER |
|--------|--------|-------|
| OS | Ubuntu Linux | Windows 11 |
| Runner | nex-automat-runner | mager-runner |
| Deployment | Full Docker | Hybrid (Docker + Windows) |
| Btrieve | N/A | Windows Service (32-bit) |
| Shell | bash | powershell |
| PostgreSQL | Docker | Windows Service |
| Temporal | Docker | Windows Service |

## Súvisiace dokumenty

- [CI/CD Overview](../ci-cd-overview.md)
- [ANDROS Deployment](../andros/ci-cd-andros-deployment.md)
- [Docker Infrastructure](../docker-infrastructure.md)