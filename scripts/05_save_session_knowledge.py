#!/usr/bin/env python
"""
Save session knowledge to RAG-indexed location.
"""

from datetime import datetime
from pathlib import Path

BASE_PATH = Path("C:/Development/nex-automat")
KNOWLEDGE_PATH = BASE_PATH / "docs" / "knowledge" / "development"
TODAY = datetime.now().strftime("%Y-%m-%d")

KNOWLEDGE_CONTENT = f"""# NEX Brain - Fáza 1 Foundation

**Dátum:** {TODAY}
**Kategória:** Development
**Status:** ✅ Complete

---

## Prehľad

NEX Brain je inteligentné rozhranie pre NEX ekosystém - "mozog" ktorý umožňuje používateľom pristupovať ku všetkým firemným informáciám pomocou prirodzeného jazyka.

## Architektúra

### Komponenty
- **FastAPI Backend** - REST API na porte 8100
- **RAG Service** - integrácia s rag-api.icc.sk
- **LLM Service** - Ollama s llama3.1:8b
- **CLI** - interaktívne testovanie

### Multi-tenant
- Jeden server obsluhuje viacero zákazníkov
- Konfigurácia: `MODE=multi-tenant`, `TENANTS=icc,andros`
- Tenant-specific system prompts
- RAG filtering podľa tenanta

## Štruktúra súborov

```
apps/nex-brain/
├── api/
│   ├── main.py              # FastAPI app
│   ├── routes/chat.py       # POST /api/v1/chat
│   └── services/
│       ├── rag_service.py   # RAG integrácia
│       └── llm_service.py   # Ollama integrácia
├── cli/chat_cli.py          # CLI testing
├── config/settings.py       # Multi-tenant config
├── requirements.txt
└── README.md
```

## Konfigurácia

### .env súbor
```env
# Multi-tenant (dev server)
MODE=multi-tenant
TENANTS=icc,andros

# Single-tenant (u zákazníka)
MODE=single-tenant
TENANT=andros

# Services
RAG_API_URL=https://rag-api.icc.sk
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

## API Endpoints

| Endpoint | Method | Popis |
|----------|--------|-------|
| `/` | GET | Info o službe |
| `/health` | GET | Health check |
| `/api/v1/tenants` | GET | Zoznam tenantov |
| `/api/v1/chat` | POST | Chat s RAG + LLM |

### Chat Request
```json
{{
    "tenant": "icc",
    "question": "Čo je NEX Brain?",
    "context_limit": 5,
    "include_sources": true
}}
```

## Ollama Model

### Odporúčaný: llama3.1:8b
- 8B parametrov
- 5-8 GB VRAM
- 128K context window
- Dobrá slovenčina
- Apache 2.0 licencia

### Inštalácia
```powershell
ollama pull llama3.1:8b
```

### Kontrola
```powershell
& "$env:LOCALAPPDATA\\Programs\\Ollama\\ollama.exe" ps
```

## Spustenie

### CLI
```powershell
cd apps/nex-brain
python cli/chat_cli.py
```

### API Server
```powershell
cd apps/nex-brain
uvicorn api.main:app --host 0.0.0.0 --port 8100 --reload
```

## Migrácia modelu

Zmena modelu je triviálna - jeden parameter:
```python
# settings.py alebo .env
OLLAMA_MODEL=llama3.1:70b  # upgrade na väčší model
```

Žiadne zmeny v kóde nie sú potrebné.

## Pilot zákazníci

| Zákazník | Typ | Časový rámec |
|----------|-----|--------------|
| ICC s.r.o. | Dev/Test | Január 2026 |
| ANDROS s.r.o. | Production pilot | Február 2026 |

---

## Súvisiace dokumenty

- [NEX_BRAIN_PRODUCT.md](../strategic/NEX_BRAIN_PRODUCT.md) - Strategický dokument
- [RAG_IMPLEMENTATION.md](../../strategic/RAG_IMPLEMENTATION.md) - RAG systém

---

**Vytvorené:** {TODAY}
**Autori:** Zoltán Rausch, Claude
"""


def main():
    KNOWLEDGE_PATH.mkdir(parents=True, exist_ok=True)

    filepath = KNOWLEDGE_PATH / f"{TODAY}_nex-brain-foundation.md"
    filepath.write_text(KNOWLEDGE_CONTENT, encoding="utf-8")
    print(f"✅ Created: {filepath}")

    print("\nNext: python tools/rag/rag_update.py --new")


if __name__ == "__main__":
    main()