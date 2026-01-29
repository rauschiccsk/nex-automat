# Inicializačný Prompt: CI/CD Fáza 1 - CI Infraštruktúra

## Kontext

**Projekt:** NEX Automat - automatizačná platforma (Python 3.11+, FastAPI, PostgreSQL, Temporal)
**Repozitár:** `github.com/rauschiccsk/nex-automat` (branch: develop)
**Cieľ:** Implementovať základnú CI infraštruktúru s GitHub Actions

## Aktuálny stav

- `.github/` priečinok neexistuje
- `pyproject.toml` obsahuje dev dependencies ale chýba konfigurácia nástrojov
- Existujú 2 unit testy v `tests/unit/`
- Monorepo štruktúra: `apps/*`, `packages/*`

## Úlohy Fázy 1

### 1. Rozšíriť pyproject.toml

Pridať konfiguráciu nástrojov na koniec súboru:

```toml
[tool.ruff]
target-version = "py311"
line-length = 120
select = ["E", "F", "W", "I", "UP", "B", "C4"]
ignore = ["E501"]
exclude = ["*.pyi", "__pycache__", ".git", "*.md"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_ignores = true
ignore_missing_imports = true
exclude = ["tests/", "docs/"]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = "-v --tb=short"

[tool.coverage.run]
source = ["packages", "apps"]
omit = ["*/tests/*", "*/__pycache__/*", "*/.venv/*"]

[tool.coverage.report]
fail_under = 50
show_missing = true
```

### 2. Vytvoriť .github/workflows/ci.yml

```yaml
name: CI Pipeline

on:
  push:
    branches: [develop, main]
  pull_request:
    branches: [develop, main]

env:
  PYTHON_VERSION: "3.11"

jobs:
  lint:
    name: Lint & Format
    runs-on: self-hosted
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install uv
        run: pip install uv

      - name: Install dependencies
        run: uv sync --dev

      - name: Ruff lint
        run: uv run ruff check .

      - name: Ruff format check
        run: uv run ruff format --check .

      - name: Type check (mypy)
        run: uv run mypy packages/ apps/ --ignore-missing-imports
        continue-on-error: true

  test:
    name: Unit Tests
    runs-on: self-hosted
    needs: lint
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install uv
        run: pip install uv

      - name: Install dependencies
        run: uv sync --dev

      - name: Run tests
        run: uv run pytest tests/unit/ -v --tb=short
        continue-on-error: true

  security:
    name: Security Scan
    runs-on: self-hosted
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install bandit
        run: pip install bandit

      - name: Bandit scan
        run: bandit -r packages/ apps/ -ll -x "*/tests/*" || true
```

### 3. Vytvoriť docker-compose.runner.yml (v root)

```yaml
# GitHub Actions Self-Hosted Runner
# Spustenie: docker compose -f docker-compose.runner.yml up -d
# Pred spustením nastaviť RUNNER_TOKEN v .env alebo environment

services:
  github-runner:
    image: myoung34/github-runner:latest
    restart: unless-stopped
    environment:
      REPO_URL: https://github.com/rauschiccsk/nex-automat
      RUNNER_NAME: nex-automat-runner
      RUNNER_TOKEN: ${RUNNER_TOKEN}
      LABELS: self-hosted,linux,x64,nex-automat
      RUNNER_WORKDIR: /tmp/runner
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - runner-work:/tmp/runner
    networks:
      - nex-network

volumes:
  runner-work:

networks:
  nex-network:
    external: true
```

### 4. Aktualizovať .gitignore

Pridať ak chýba:

```
# GitHub Actions
.github/workflows/*.local.yml

# Coverage
.coverage
htmlcov/
coverage.xml
```

## Štruktúra súborov po implementácii

```
nex-automat/
├── .github/
│   └── workflows/
│       └── ci.yml
├── docker-compose.runner.yml
├── pyproject.toml (rozšírený)
└── .gitignore (aktualizovaný)
```

## Validácia

Po implementácii overiť:

1. `ruff check .` - žiadne kritické chyby
2. `ruff format --check .` - formátovanie OK
3. `pytest tests/unit/ -v` - testy prechádzajú

## Git commit

```
feat(ci): implement CI/CD Phase 1 - GitHub Actions infrastructure

- Add tool configuration to pyproject.toml (ruff, mypy, pytest, coverage)
- Create .github/workflows/ci.yml with lint, test, security jobs
- Add docker-compose.runner.yml for self-hosted runner
- Update .gitignore for coverage files
```

## Poznámky

- `continue-on-error: true` na mypy a pytest - dočasne, kým sa neopraví coverage
- Self-hosted runner bude spustený na ANDROS serveri (samostatný krok)
- Coverage threshold nastavený na 50% (zvýšime po rozšírení testov)