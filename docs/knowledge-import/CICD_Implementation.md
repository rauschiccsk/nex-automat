# CI/CD Implementácia pre NEX Automat

**Dokument:** Knowledge pre RAG
**Dátum:** 2026-01-29
**Status:** Fázy 1-3 dokončené, Fáza 4-5 v príprave

---

## Prehľad

CI/CD pipeline pre NEX Automat používa GitHub Actions so self-hosted runnerom na ANDROS serveri. Pipeline automatizuje testovanie, linting, security scanning a Docker build.

## Architektúra

**Repozitár:** github.com/rauschiccsk/nex-automat
**Branch stratégia:** develop (staging) → main (production)
**Runner:** Self-hosted na ANDROS Ubuntu (Dell PowerEdge R740XD)

## Dokončené fázy

### Fáza 1: CI infraštruktúra

Vytvorené súbory:
- `.github/workflows/ci.yml` - hlavný CI workflow
- `docker-compose.runner.yml` - GitHub Actions runner container
- `pyproject.toml` - rozšírený o ruff, mypy, pytest konfiguráciu

Commity:
- `4e734dc` - základná CI infraštruktúra
- `63e24e1` - oprava: pip install namiesto uv sync

### Fáza 2: Rozšírenie testov

- 52 testov celkovo
- 15% code coverage
- Commit: `8b556c9`

Riešené problémy:
- Ruff našiel 1352 lint chýb, 1033 automaticky opravených cez `ruff check --fix`
- Pridané ignore pravidlá do pyproject.toml pre zvyšné chyby

### Fáza 3: Docker build

Matrix build pre 2 Docker images:
- `nex-brain` (Dockerfile.nex-brain)
- `nex-telegram` (Dockerfile.telegram)

Commit: `092077a`

## CI Pipeline štruktúra

```
.github/workflows/ci.yml:
  lint (8s) → test (36s) → build (3min)
  security (parallel)
```

Celkový čas: ~4 minúty
Status: 3x zelený za sebou

## Fáza 4-5: Deployment automation (plánované)

### Požiadavky

1. Deployment proces = plne automatizovaný
2. Deployment spustenie = manuálne schválenie per zákazník (workflow_dispatch)
3. One-click deploy pre každého zákazníka

### Plánovaný deploy.yml

- **workflow_dispatch** trigger (manuálne spustenie)
- Input: výber zákazníka (ANDROS, MAGER, ...)
- **Environment protection** - manuálne schválenie v GitHub
- **Dynamický runner** podľa zákazníka (`runs-on: ${{ inputs.customer }}-runner`)

### Zákazníci

| Zákazník | Server | Poznámka |
|----------|--------|----------|
| ANDROS | ANDROS Ubuntu | Dell PowerEdge R740XD |
| MAGER | MAGER | Mágerstav |

## GitHub Secrets

```
POSTGRES_PASSWORD        # Databázové heslo
TELEGRAM_BOT_TOKEN       # Pre notifikácie
TELEGRAM_CHAT_ID         # Chat ID pre notifikácie
RUNNER_TOKEN             # GitHub runner registration token
```

## Workflow pravidlá

- **Dev→Git→Deploy** - nikdy priamo na deployment
- **Chat** = plánovanie, review
- **Claude Code** = implementácia, testy, Git operácie

## CC Fleet pre deployment

| CC | Účel |
|----|------|
| DEVELOPMENT | Dev PC, implementácia |
| ANDROS Ubuntu | Server deployment |
| ANDROS Windows | Windows VM |
| MAGER | Mágerstav deployment |

## Technické nástroje

- **Ruff** - linting a formatting
- **Pytest** - testovanie
- **Mypy** - type checking (konfigurácia v pyproject.toml)
- **Bandit** - security scanning

## Súvisiace dokumenty

- Deployment postupy pre ANDROS
- Docker compose konfigurácie
- NEX Automat architektúra