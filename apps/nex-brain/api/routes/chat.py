"""
Chat endpoint for NEX Brain - Multi-tenant support.
"""

import re

from config.settings import settings
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.services.llm_service import LLMService
from api.services.rag_service import RAGService

router = APIRouter()

rag_service = RAGService()
llm_service = LLMService()

# Simple greetings that don't need RAG (ASCII only to avoid encoding issues)
GREETING_PATTERNS = [
    r"^ahoj",
    r"^cau",
    r"^hi$",
    r"^hello",
    r"^dobry den",
    r"^dobry",
    r"^vitaj",
    r"^ako sa mas",
    r"^co robis",
    r"^zdravim",
]


def is_simple_greeting(text: str) -> bool:
    """Check if text is a simple greeting that doesn't need RAG."""
    # Normalize: lowercase, strip, remove diacritics
    text_lower = text.lower().strip()
    # Simple diacritics removal for Slovak
    replacements = {
        "á": "a",
        "ä": "a",
        "č": "c",
        "ď": "d",
        "é": "e",
        "í": "i",
        "ĺ": "l",
        "ľ": "l",
        "ň": "n",
        "ó": "o",
        "ô": "o",
        "ŕ": "r",
        "š": "s",
        "ť": "t",
        "ú": "u",
        "ý": "y",
        "ž": "z",
    }
    for sk, ascii_char in replacements.items():
        text_lower = text_lower.replace(sk, ascii_char)

    for pattern in GREETING_PATTERNS:
        if re.match(pattern, text_lower):
            return True
    return False


class ChatRequest(BaseModel):
    question: str
    tenant: str | None = None
    context_limit: int = 5
    include_sources: bool = True


class ChatResponse(BaseModel):
    answer: str
    tenant: str
    sources: list | None = None
    model: str
    tokens_used: int | None = None


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a question using RAG + LLM.

    - Simple greetings: direct LLM response (no RAG)
    - Knowledge questions: RAG + LLM
    """
    try:
        # 1. Resolve tenant
        try:
            tenant = settings.get_tenant(request.tenant)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        # 2. Check if RAG is needed
        needs_rag = not is_simple_greeting(request.question)

        rag_results = None
        if needs_rag:
            # Get context from RAG (with tenant filter)
            rag_results = await rag_service.search(query=request.question, limit=request.context_limit, tenant=tenant)

        # 3. Generate answer with LLM
        answer, tokens = await llm_service.generate(question=request.question, context=rag_results, tenant=tenant)

        # 4. Build response
        sources = None
        if request.include_sources and rag_results:
            sources = [{"filename": r["filename"], "score": r["score"]} for r in rag_results]

        return ChatResponse(
            answer=answer, tenant=tenant, sources=sources, model=llm_service.model_name, tokens_used=tokens
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


class IngestRequest(BaseModel):
    content: str
    filename: str
    tenant: str
    metadata: dict | None = None


class IngestResponse(BaseModel):
    success: bool
    message: str
    tenant: str


@router.post("/ingest", response_model=IngestResponse)
async def ingest_document(request: IngestRequest):
    """
    Ingest a document into the RAG knowledge base.
    Creates the tenant collection if it doesn't exist.
    """
    try:
        success = await rag_service.add_document(
            content=request.content,
            filename=request.filename,
            tenant=request.tenant,
            metadata=request.metadata
        )

        if success:
            return IngestResponse(
                success=True,
                message=f"Document '{request.filename}' ingested successfully",
                tenant=request.tenant
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to ingest document")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/collections")
async def list_collections():
    """List all Qdrant collections (tenants with data)."""
    try:
        collections = rag_service.qdrant.get_collections()
        result = []
        for c in collections.collections:
            info = rag_service.qdrant.get_collection(c.name)
            result.append({
                "name": c.name,
                "indexed_vectors_count": info.indexed_vectors_count,
                "points_count": info.points_count
            })
        return {"collections": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
