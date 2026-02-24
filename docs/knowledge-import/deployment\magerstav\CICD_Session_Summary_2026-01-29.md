---
title: CI/CD Implementation Session - MAGER Server
category: session-summary
tags: [ci-cd, github-actions, mager, docker, windows, deployment]
created: 2026-01-29
---

# CI/CD Implementation Session - MAGER Server

## Prehľad

Session zameraná na implementáciu CI/CD pipeline pre MAGER server s hybridným deployment modelom.

## Dokončené úlohy

### 1. MAGER GitHub Actions Runner

| Parameter | Hodnota |
|-----------|---------|
| Názov | mager-runner |
| Labels | MAGER, self-hosted, Windows |
| Adresár | C:\github-runner |
| Služba | actions.runner.rauschiccsk-nex-automat.mager-runner |
| Status | ✅ Online |

### 2. Docker infraštruktúra na MAGER

- Docker Desktop 29.1.5
- Docker Compose 5.0.1
- WSL2 s Ubuntu
- Auto-start enabled

### 3. Hybridný deployment model

**Dôvod:** Btrieve (Pervasive PSQL Workgroup) je len 32-bit, Docker kontajnery sú 64-bit Linux.

| Komponenta | Prostredie | Port |
|------------|------------|------|
| PostgreSQL | Windows Service | 5432 |
| Temporal | Windows Service | 7233, 8233 |
| Invoice-Worker | Docker | - |
| Polling-Scheduler | Docker | - |
| Btrieve-Loader | Windows Service | 8001 |

Docker workers sa pripájajú na Windows služby cez `host.docker.internal`.

### 4. CI/CD Workflow

**Súbor:** `.github/workflows/deploy.yml`

MAGER deployment steps:
1. Git Pull (C:\opt\nex-automat-src)
2. Copy docker-compose.yml
3. Docker Compose Up
4. Restart NEX-BtrieveLoader
5. Health Check

**Shell:** PowerShell (nie pwsh, nie bash)

### 5. Premenovanie supplier-invoice-loader → btrieve-loader

| Komponent | Pred | Po |
|-----------|------|-----|
| Adresár (repo) | apps/supplier-invoice-loader | apps/btrieve-loader |
| Adresár (MAGER) | C:\Deployment\...\supplier-invoice-loader | C:\Deployment\...\btrieve-loader |
| Windows Service | NEX-SupplierInvoiceLoader | NEX-BtrieveLoader |

### 6. CI Pipeline opravy

- Špecifikované `runs-on: [self-hosted, ANDROS]` pre všetky CI joby
- Opravený shell syntax pre Security Scan (`shell: bash`)
- Obnovený ANDROS runner (nový token)

## Finálny stav

| Server | Runner | CI | Deploy | Čas |
|--------|--------|-----|--------|-----|
| ANDROS | ✅ nex-automat-runner | ✅ | ✅ | 22s |
| MAGER | ✅ mager-runner | N/A | ✅ | 13s |

## Adresárová štruktúra MAGER

```
C:\opt\
├── nex-automat\           # Deployment
│   ├── docker-compose.yml
│   └── .env
└── nex-automat-src\       # Git repository

C:\Deployment\nex-automat\
├── apps\
│   └── btrieve-loader\    # Windows Service
├── venv32\                # 32-bit Python pre Btrieve
└── venv64\                # 64-bit Python
```

## Troubleshooting riešené

| Problém | Riešenie |
|---------|----------|
| pwsh not found | Zmena na `shell: powershell` |
| PowerShell scripts disabled | `Set-ExecutionPolicy RemoteSigned` |
| Git dubious ownership | `git config --system --add safe.directory` |
| Port already allocated | Použiť existujúce Windows služby |
| ANDROS runner offline | Nový registration token |
| CI na Windows runner | Explicitný label `[self-hosted, ANDROS]` |

## Commity

| Hash | Popis |
|------|-------|
| cfb4f42 | feat(mager): add docker-compose for hybrid Btrieve deployment |
| 8f03e9b | feat(ci): add MAGER hybrid deployment to deploy.yml |
| abce75c | feat(worker): add Dockerfile for supplier-invoice-worker |
| 0a935f7 | fix(ci): use PowerShell instead of SSH for MAGER deployment |
| 32f1d02 | fix(ci): use powershell instead of pwsh for MAGER |
| ea70075 | fix(mager): correct Docker build context paths |
| 58875e2 | refactor(mager): use existing Windows services instead of Docker |
| adf189d | refactor: rename supplier-invoice-loader to btrieve-loader |
| 38d6662 | fix(ci): update service name to NEX-BtrieveLoader |
| b765e67 | fix(ci): specify ANDROS runner for CI pipeline |

## Nasledujúce kroky

1. **Btrieve-Loader** - kompletná implementácia REST API proxy
2. Gmail App Password - čaká na novú emailovú adresu
3. Monitoring (Prometheus/Grafana) - neskôr

## Súvisiace dokumenty

- docs/knowledge/deployment/magerstav/CICD_MAGER_DEPLOYMENT.md
- deploy/mager/docker-compose.yml
- .github/workflows/deploy.yml
- .github/workflows/ci.yml