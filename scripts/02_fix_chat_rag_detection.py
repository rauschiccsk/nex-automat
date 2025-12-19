#!/usr/bin/env python
"""
Fix chat.py - Add detection for simple greetings that don't need RAG.
"""

from pathlib import Path

FILE_PATH = Path("C:/Development/nex-automat/apps/nex-brain/api/routes/chat.py")

NEW_CONTENT = '''"""
Chat endpoint for NEX Brain - Multi-tenant support.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import re

from api.services.rag_service import RAGService
from api.services.llm_service import LLMService
from config.settings import settings

router = APIRouter()

rag_service = RAGService()
llm_service = LLMService()

# Simple greetings that don't need RAG
GREETING_PATTERNS = [
    r"^ahoj\b", r"^čau\b", r"^cau\b", r"^hi\b", r"^hello\b",
    r"^dobrý deň\b", r"^dobry den\b", r"^zdravím\b", r"^vitaj\b",
    r"^ako sa máš\b", r"^ako sa mas\b", r"^čo robíš\b",
]

def is_simple_greeting(text: str) -> bool:
    """Check if text is a simple greeting that doesn't need RAG."""
    text_lower = text.lower().strip()
    for pattern in GREETING_PATTERNS:
        if re.match(pattern, text_lower):
            return True
    return False


class ChatRequest(BaseModel):
    question: str
    tenant: Optional[str] = None
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
'''


def main():
    FILE_PATH.write_text(NEW_CONTENT, encoding="utf-8")
    print(f"✅ Fixed: {FILE_PATH.name}")
    print("   - Added greeting detection")
    print("   - RAG skipped for simple greetings")


if __name__ == "__main__":
    main()