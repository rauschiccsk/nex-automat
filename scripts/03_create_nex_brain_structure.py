#!/usr/bin/env python
"""
Create NEX Brain application structure.
Phase 1: Foundation - Directory structure and base files.
"""

from pathlib import Path

BASE_PATH = Path("C:/Development/nex-automat/apps/nex-brain")

# File contents
FILES = {
    "api/__init__.py": '''"""NEX Brain API package."""
''',

    "api/main.py": '''"""
NEX Brain API - FastAPI Application
Inteligentné rozhranie pre NEX ekosystém.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import chat

app = FastAPI(
    title="NEX Brain API",
    description="Inteligentné rozhranie pre NEX ekosystém",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])


@app.get("/")
async def root():
    return {"service": "NEX Brain", "status": "running", "version": "0.1.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
''',

    "api/routes/__init__.py": '''"""API routes package."""
''',

    "api/routes/chat.py": '''"""
Chat endpoint for NEX Brain - Multi-tenant support.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from api.services.rag_service import RAGService
from api.services.llm_service import LLMService
from config.settings import settings

router = APIRouter()

rag_service = RAGService()
llm_service = LLMService()


class ChatRequest(BaseModel):
    question: str
    tenant: Optional[str] = None  # Required in multi-tenant mode
    context_limit: int = 5
    include_sources: bool = True


class ChatResponse(BaseModel):
    answer: str
    tenant: str
    sources: Optional[list] = None
    model: str
    tokens_used: Optional[int] = None


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a question using RAG + LLM.

    Multi-tenant: requires 'tenant' in request
    Single-tenant: uses tenant from config

    1. Resolve tenant
    2. Search RAG for relevant context (filtered by tenant)
    3. Send context + question to Ollama
    4. Return answer with sources
    """
    try:
        # 1. Resolve tenant
        try:
            tenant = settings.get_tenant(request.tenant)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        # 2. Get context from RAG (with tenant filter)
        rag_results = await rag_service.search(
            query=request.question, 
            limit=request.context_limit,
            tenant=tenant
        )

        # 3. Generate answer with LLM
        answer, tokens = await llm_service.generate(
            question=request.question,
            context=rag_results,
            tenant=tenant
        )

        # 4. Build response
        sources = None
        if request.include_sources and rag_results:
            sources = [
                {"filename": r["filename"], "score": r["score"]} 
                for r in rag_results
            ]

        return ChatResponse(
            answer=answer,
            tenant=tenant,
            sources=sources,
            model=llm_service.model_name,
            tokens_used=tokens
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tenants")
async def list_tenants():
    """List available tenants (only in multi-tenant mode)."""
    if settings.is_multi_tenant:
        return {"tenants": settings.tenant_list}
    else:
        return {"tenant": settings.TENANT, "mode": "single-tenant"}
''',

    "api/services/__init__.py": '''"""Services package."""
''',

    "api/services/rag_service.py": '''"""
RAG Service - Integration with existing RAG API.
Multi-tenant support with tenant-based filtering.
"""

import httpx
from typing import List, Dict, Any, Optional
from config.settings import settings


class RAGService:
    """Service for RAG (Retrieval-Augmented Generation) queries."""

    def __init__(self):
        self.base_url = settings.RAG_API_URL

    async def search(
        self, 
        query: str, 
        limit: int = 5,
        tenant: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search RAG knowledge base.

        Args:
            query: Search query
            limit: Max results to return
            tenant: Tenant identifier for filtering

        Returns:
            List of relevant documents with scores
        """
        try:
            # Build query with tenant prefix if provided
            # RAG can filter by path: tenant/docs/...
            search_query = query

            async with httpx.AsyncClient(timeout=30.0) as client:
                params = {"query": search_query, "limit": limit}

                response = await client.get(
                    f"{self.base_url}/search",
                    params=params
                )
                response.raise_for_status()
                data = response.json()
                results = data.get("results", [])

                # Filter by tenant if needed (client-side filtering)
                # TODO: Add server-side tenant filtering to RAG API
                if tenant:
                    results = self._filter_by_tenant(results, tenant)

                return results

        except httpx.RequestError as e:
            print(f"RAG API error: {e}")
            return []

    def _filter_by_tenant(
        self, 
        results: List[Dict[str, Any]], 
        tenant: str
    ) -> List[Dict[str, Any]]:
        """
        Filter results by tenant.

        Convention: Files in tenant folder or shared folder.
        - tenant/... = tenant-specific
        - shared/... = available to all tenants
        """
        filtered = []
        for r in results:
            filename = r.get("filename", "").lower()
            # Include if: tenant-specific OR shared OR no tenant prefix
            if (
                f"{tenant}/" in filename or
                "shared/" in filename or
                "/" not in filename  # Root level = shared
            ):
                filtered.append(r)
        return filtered

    def format_context(self, results: List[Dict[str, Any]]) -> str:
        """Format RAG results as context for LLM."""
        if not results:
            return ""

        context_parts = []
        for i, r in enumerate(results, 1):
            context_parts.append(
                f"[Zdroj {i}: {r.get('filename', 'unknown')}]\\n"
                f"{r.get('content', '')}"
            )

        return "\\n\\n---\\n\\n".join(context_parts)
''',

    "api/services/llm_service.py": '''"""
LLM Service - Integration with Ollama.
Multi-tenant support with tenant-aware prompts.
"""

import httpx
from typing import Tuple, List, Dict, Any, Optional
from config.settings import settings
from api.services.rag_service import RAGService


# Tenant-specific system prompts
TENANT_PROMPTS = {
    "icc": """Si NEX Brain - inteligentný asistent pre ICC s.r.o.
Odpovedaj v slovenčine, stručne a presne.
Ak informácia nie je v kontexte, povedz to priamo.
ICC je softvérová firma vyvíjajúca NEX Genesis ERP systém.""",

    "andros": """Si NEX Brain - inteligentný asistent pre ANDROS s.r.o.
Odpovedaj v slovenčine, stručne a presne.
Ak informácia nie je v kontexte, povedz to priamo.
Pomáhaj zamestnancom s procesmi, dokumentáciou a ERP systémom.""",

    "default": """Si NEX Brain - inteligentný asistent pre NEX systém.
Odpovedaj v slovenčine, stručne a presne.
Ak informácia nie je v kontexte, povedz to priamo."""
}


class LLMService:
    """Service for LLM (Ollama) interactions with multi-tenant support."""

    def __init__(self):
        self.base_url = settings.OLLAMA_URL
        self.model_name = settings.OLLAMA_MODEL
        self.rag_service = RAGService()

    async def generate(
        self, 
        question: str, 
        context: Optional[List[Dict[str, Any]]] = None,
        tenant: str = "default"
    ) -> Tuple[str, int]:
        """
        Generate answer using Ollama.

        Args:
            question: User question
            context: RAG context (optional)
            tenant: Tenant identifier

        Returns:
            Tuple of (answer, tokens_used)
        """
        # Build prompt with tenant-specific system prompt
        prompt = self._build_prompt(question, context, tenant)

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model_name,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "num_predict": 1024,
                        }
                    }
                )
                response.raise_for_status()
                data = response.json()

                answer = data.get("response", "")
                tokens = data.get("eval_count", 0)

                return answer, tokens

        except httpx.RequestError as e:
            return f"Chyba pri komunikácii s LLM: {e}", 0

    def _build_prompt(
        self, 
        question: str, 
        context: Optional[List[Dict[str, Any]]] = None,
        tenant: str = "default"
    ) -> str:
        """Build prompt with tenant-specific system prompt and context."""

        # Get tenant-specific or default system prompt
        system = TENANT_PROMPTS.get(tenant, TENANT_PROMPTS["default"])

        if context:
            context_text = self.rag_service.format_context(context)
            return f"""{system}

KONTEXT Z KNOWLEDGE BASE:
{context_text}

OTÁZKA: {question}

ODPOVEĎ:"""
        else:
            return f"""{system}

OTÁZKA: {question}

ODPOVEĎ:"""

    async def health_check(self) -> bool:
        """Check if Ollama is running."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except:
            return False
''',

    "cli/__init__.py": '''"""CLI package."""
''',

    "cli/chat_cli.py": '''#!/usr/bin/env python
"""
NEX Brain CLI - Command line interface for testing.
Multi-tenant support.
"""

import asyncio
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.services.rag_service import RAGService
from api.services.llm_service import LLMService
from config.settings import settings


async def main():
    """Interactive CLI for NEX Brain."""
    print("=" * 60)
    print("  NEX Brain CLI - Interaktívne rozhranie")
    print("=" * 60)

    # Show mode
    if settings.is_multi_tenant:
        print(f"Mode: Multi-tenant ({', '.join(settings.tenant_list)})")
    else:
        print(f"Mode: Single-tenant ({settings.TENANT})")

    print("-" * 60)
    print("Príkazy:")
    print("  'quit' alebo 'q'    - ukončenie")
    print("  'rag <query>'       - priame RAG vyhľadávanie")
    print("  'tenant <name>'     - zmena tenanta (multi-tenant mode)")
    print("-" * 60)

    rag = RAGService()
    llm = LLMService()

    # Current tenant
    if settings.is_multi_tenant:
        current_tenant = settings.tenant_list[0]  # Default to first
        print(f"Aktuálny tenant: {current_tenant}")
    else:
        current_tenant = settings.TENANT or "default"

    # Check Ollama
    if await llm.health_check():
        print(f"✅ Ollama: {llm.model_name}")
    else:
        print("⚠️  Ollama nie je dostupná - odpovede budú len z RAG")

    print()

    while True:
        try:
            prompt = f"[{current_tenant}] Otázka: " if settings.is_multi_tenant else "Otázka: "
            question = input(prompt).strip()

            if not question:
                continue

            if question.lower() in ('quit', 'q', 'exit'):
                print("Dovidenia!")
                break

            # Change tenant
            if question.lower().startswith('tenant '):
                new_tenant = question[7:].strip()
                if new_tenant in settings.tenant_list:
                    current_tenant = new_tenant
                    print(f"✅ Tenant zmenený na: {current_tenant}")
                else:
                    print(f"❌ Neznámy tenant. Dostupné: {', '.join(settings.tenant_list)}")
                print()
                continue

            # Direct RAG search
            if question.lower().startswith('rag '):
                query = question[4:].strip()
                print(f"\\nVyhľadávam v RAG: '{query}' (tenant: {current_tenant})...")
                results = await rag.search(query, limit=5, tenant=current_tenant)

                if results:
                    for i, r in enumerate(results, 1):
                        print(f"\\n[{i}] {r.get('filename')} (score: {r.get('score', 0):.3f})")
                        content = r.get('content', '')[:200]
                        print(f"    {content}...")
                else:
                    print("Žiadne výsledky.")
                print()
                continue

            # Full RAG + LLM query
            print("\\nHľadám kontext...")
            context = await rag.search(question, limit=5, tenant=current_tenant)

            if context:
                print(f"Našiel som {len(context)} relevantných dokumentov.")

            print("Generujem odpoveď...\\n")
            answer, tokens = await llm.generate(question, context, tenant=current_tenant)

            print("-" * 40)
            print(answer)
            print("-" * 40)

            if tokens:
                print(f"[tenant: {current_tenant}, tokens: {tokens}]")
            print()

        except KeyboardInterrupt:
            print("\\nUkončené.")
            break
        except Exception as e:
            print(f"Chyba: {e}")


if __name__ == "__main__":
    asyncio.run(main())
''',

    "config/__init__.py": '''"""Config package."""
''',

    "config/settings.py": '''"""
NEX Brain Configuration - Multi-tenant support.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional, List


class Settings(BaseSettings):
    """Application settings with multi-tenant support."""

    # Deployment mode
    MODE: str = "multi-tenant"  # "multi-tenant" or "single-tenant"
    TENANT: str = ""  # For single-tenant mode
    TENANTS: str = "icc,andros"  # Comma-separated list for multi-tenant

    # RAG API
    RAG_API_URL: str = "https://rag-api.icc.sk"

    # Ollama
    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1:8b"

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8100

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def is_multi_tenant(self) -> bool:
        return self.MODE == "multi-tenant"

    @property
    def tenant_list(self) -> List[str]:
        return [t.strip() for t in self.TENANTS.split(",") if t.strip()]

    def get_tenant(self, request_tenant: Optional[str] = None) -> str:
        """Get tenant - from request (multi) or config (single)."""
        if self.is_multi_tenant:
            if not request_tenant:
                raise ValueError("Tenant required in multi-tenant mode")
            if request_tenant not in self.tenant_list:
                raise ValueError(f"Unknown tenant: {request_tenant}")
            return request_tenant
        else:
            return self.TENANT or "default"


settings = Settings()
''',

    "tests/__init__.py": '''"""Tests package."""
''',

    "requirements.txt": '''# NEX Brain dependencies
fastapi>=0.104.0
uvicorn>=0.24.0
httpx>=0.25.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
python-dotenv>=1.0.0
''',

    "README.md": '''# NEX Brain

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
curl -X POST http://localhost:8100/api/v1/chat \\
  -H "Content-Type: application/json" \\
  -d \'{"tenant": "icc", "question": "Ako spracujem reklamáciu?"}\'
```

### Príklad použitia (single-tenant)

```bash
curl -X POST http://localhost:8100/api/v1/chat \\
  -H "Content-Type: application/json" \\
  -d \'{"question": "Ako spracujem reklamáciu?"}\'
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
''',
}


def main():
    print("=" * 60)
    print("  Creating NEX Brain Application Structure")
    print("=" * 60)

    # Create directories
    dirs = [
        "api/routes",
        "api/services",
        "cli",
        "config",
        "tests",
    ]

    for d in dirs:
        dir_path = BASE_PATH / d
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"📁 {d}/")

    # Create files
    print()
    for filepath, content in FILES.items():
        file_path = BASE_PATH / filepath
        file_path.write_text(content, encoding="utf-8")
        print(f"✅ {filepath}")

    print()
    print("=" * 60)
    print("✅ NEX Brain structure created!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. cd apps/nex-brain")
    print("2. pip install -r requirements.txt")
    print("3. Install Ollama: https://ollama.com")
    print("4. ollama pull llama3.1:8b")
    print("5. python cli/chat_cli.py")


if __name__ == "__main__":
    main()