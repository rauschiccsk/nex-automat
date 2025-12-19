"""
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
