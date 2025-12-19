# NEX Brain

**Inteligentné rozhranie pre NEX ekosystém**

> "Opýtajte sa svojho ERP systému ľudským jazykom"

## Popis

NEX Brain kombinuje RAG (Retrieval-Augmented Generation) s lokálnym LLM (Ollama) 
pre poskytovanie odpovedí na otázky o firemných procesoch, dokumentácii a ERP dátach.

**Multi-tenant podpora** - jeden server môže obsluhovať viacero zákazníkov.

## Quick Start

### 1. Inštalácia závislostí

```bash
cd apps/nex-brain
pip install -r requirements.txt
```

### 2. Inštalácia Ollama

```bash
# Windows - stiahnuť z https://ollama.com
# Po inštalácii:
ollama pull llama3.1:8b
```

### 3. Konfigurácia

Vytvor `.env` súbor:

```env
# Multi-tenant mode (dev server)
MODE=multi-tenant
TENANTS=icc,andros

# Single-tenant mode (u zákazníka)
# MODE=single-tenant
# TENANT=andros

# Services
RAG_API_URL=https://rag-api.icc.sk
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

### 4. Spustenie CLI

```bash
python cli/chat_cli.py
```

### 5. Spustenie API

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8100 --reload
```

## API Endpoints

- `GET /` - Info o službe
- `GET /health` - Health check
- `GET /api/v1/tenants` - Zoznam tenantov
- `POST /api/v1/chat` - Chat endpoint

### Príklad použitia (multi-tenant)

```bash
curl -X POST http://localhost:8100/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"tenant": "icc", "question": "Ako spracujem reklamáciu?"}'
```

### Príklad použitia (single-tenant)

```bash
curl -X POST http://localhost:8100/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Ako spracujem reklamáciu?"}'
```

## Štruktúra

```
nex-brain/
├── api/              # FastAPI aplikácia
│   ├── routes/       # API endpointy
│   └── services/     # RAG a LLM služby
├── cli/              # Command line interface
├── config/           # Konfigurácia
└── tests/            # Testy
```

## Multi-tenant vs Single-tenant

| Režim | Použitie | Konfigurácia |
|-------|----------|--------------|
| **Multi-tenant** | Dev server, viacero zákazníkov | `MODE=multi-tenant` |
| **Single-tenant** | Produkcia u zákazníka | `MODE=single-tenant` |

**Presun k zákazníkovi:** Len zmena `.env` súboru, žiadne zmeny v kóde.

## Technológie

- **FastAPI** - REST API
- **Ollama** - Lokálny LLM (llama3.1:8b)
- **RAG API** - Knowledge base vyhľadávanie
- **httpx** - Async HTTP klient

---

**Verzia:** 0.1.0  
**Status:** 📋 Development
