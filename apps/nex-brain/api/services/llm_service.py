"""
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
ICC je softvérová firma vyvíjajúca NEX Genesis ERP systém a NEX Automat.""",

    "andros": """Si NEX Brain - inteligentný asistent pre ANDROS s.r.o.
Pomáhaj zamestnancom s procesmi, dokumentáciou a ERP systémom.""",

    "default": """Si NEX Brain - inteligentný asistent pre NEX systém."""
}

# Common instructions for all tenants
COMMON_INSTRUCTIONS = """
PRAVIDLÁ:
- Odpovedaj VŽDY v slovenčine
- Odpovedaj stručne a presne na položenú otázku
- Odpovedz LEN na túto jednu otázku, NEPRIDÁVAJ ďalšie otázky ani odpovede
- Ak informácia nie je v kontexte, povedz "Túto informáciu nemám v knowledge base."
- Nepoužívaj markdown formátovanie (žiadne ** alebo ##)
"""


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
                            "temperature": 0.3,  # Lower = more focused
                            "num_predict": 512,  # Limit response length
                            "stop": ["OTÁZKA:", "Otázka:", "?\n\n"],  # Stop sequences
                        }
                    }
                )
                response.raise_for_status()
                data = response.json()

                answer = data.get("response", "").strip()
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
        tenant_intro = TENANT_PROMPTS.get(tenant, TENANT_PROMPTS["default"])
        system = tenant_intro + COMMON_INSTRUCTIONS

        if context:
            context_text = self.rag_service.format_context(context)
            return f"""{system}

KONTEXT Z KNOWLEDGE BASE:
{context_text}

OTÁZKA POUŽÍVATEĽA: {question}

TVOJA ODPOVEĎ (len na túto otázku):"""
        else:
            return f"""{system}

OTÁZKA POUŽÍVATEĽA: {question}

TVOJA ODPOVEĎ (len na túto otázku):"""

    async def health_check(self) -> bool:
        """Check if Ollama is running."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except:
            return False
