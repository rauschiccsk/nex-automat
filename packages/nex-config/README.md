# nex-config

Centrálna konfigurácia pre NEX Automat ekosystém.

## Inštalácia

```bash
pip install -e packages/nex-config/
```

## Použitie

```python
from nex_config.database import DB_HOST, DB_PORT
from nex_config.timeouts import HTTP_DEFAULT_TIMEOUT_SECONDS
from nex_config.services import QDRANT_URL

# Security modul vyžaduje JWT_SECRET_KEY env var
from nex_config.security import JWT_SECRET_KEY
```

## Princípy

- Každá hodnota definovaná na JEDNOM mieste
- Citlivé hodnoty (hesla, secrets) → `os.getenv()` BEZ fallbacku
- Prevádzkové hodnoty → `os.getenv()` S rozumným default
- Konštanty → priamo v module
- Jednotky v názvoch: `_SECONDS`, `_MINUTES`, `_MS`, `_MB`
