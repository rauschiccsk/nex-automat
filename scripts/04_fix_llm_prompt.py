#!/usr/bin/env python
"""
Fix llm_service.py - Better prompt and stop sequences.
"""

from pathlib import Path

FILE_PATH = Path("C:/Development/nex-automat/apps/nex-brain/api/services/llm_service.py")

CONTENT = '''"""
LLM Service - Integration with Ollama.
Multi-tenant support with tenant-aware prompts.
"""

import httpx
from typing import Tuple, List, Dict, Any, Optional
from config.settings import settings
from api.services.rag_service import RAGService


# Tenant-specific system prompts
TENANT_PROMPTS = {
    "icc": """Si NEX Brain - inteligentny asistent pre ICC s.r.o.
ICC je softverova firma vyvijajuca NEX Genesis ERP system a NEX Automat.
NEX Brain je inteligentne rozhranie pre NEX ekosystem - umoznuje pristup k firemnym informaciam pomocou prirodzeneho jazyka.""",

    "andros": """Si NEX Brain - inteligentny asistent pre ANDROS s.r.o.
Pomahaj zamestnancom s procesmi, dokumentaciou a ERP systemom.""",

    "default": """Si NEX Brain - inteligentny asistent pre NEX system.
NEX Brain je inteligentne rozhranie pre NEX ekosystem."""
}

# Common instructions for all tenants
COMMON_INSTRUCTIONS = """

ZASADY:
1. Odpovedaj VZDY po slovensky
2. Odpovedaj STRUCNE - max 2-3 vety
3. Pouzivaj LEN informacie z KONTEXTU nizsie
4. Ak informacia nie je v kontexte, povedz: "Tuto informaciu nemam."
5. NIKDY nevymyslaj informacie
6. NIKDY nepridavaj dalsie otazky
7. NIKDY nepouzivaj markdown (** ## atd)
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
        """Generate answer using Ollama."""
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
                            "temperature": 0.1,
                            "num_predict": 256,
                            "stop": [
                                "OTAZKA:",
                                "Otazka:",
                                "KONTEXT:",
                                "Kontext:",
                                "ZASADY:",
                                "\\n\\n\\n",
                            ],
                        }
                    }
                )
                response.raise_for_status()
                data = response.json()

                answer = data.get("response", "").strip()
                # Clean up any prompt leakage
                answer = self._clean_answer(answer)
                tokens = data.get("eval_count", 0)

                return answer, tokens

        except httpx.RequestError as e:
            return f"Chyba pri komunikacii s LLM: {e}", 0

    def _clean_answer(self, answer: str) -> str:
        """Remove any prompt leakage from answer."""
        # Remove common prompt patterns that might leak
        patterns_to_remove = [
            "OTAZKA POUZIVATELA:",
            "TVOJA ODPOVED:",
            "KONTEXT Z KNOWLEDGE BASE:",
        ]
        for pattern in patterns_to_remove:
            if pattern in answer:
                answer = answer.split(pattern)[0].strip()
        return answer

    def _build_prompt(
        self, 
        question: str, 
        context: Optional[List[Dict[str, Any]]] = None,
        tenant: str = "default"
    ) -> str:
        """Build prompt with tenant-specific system prompt and context."""
        tenant_intro = TENANT_PROMPTS.get(tenant, TENANT_PROMPTS["default"])
        system = tenant_intro + COMMON_INSTRUCTIONS

        if context:
            context_text = self.rag_service.format_context(context)
            return f"""{system}

KONTEXT:
{context_text}

OTAZKA: {question}

ODPOVED:"""
        else:
            return f"""{system}

OTAZKA: {question}

ODPOVED:"""

    async def health_check(self) -> bool:
        """Check if Ollama is running."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except:
            return False
'''

def main():
    FILE_PATH.write_text(CONTENT, encoding="utf-8")
    print(f"✅ Fixed: {FILE_PATH.name}")
    print("   - Better system prompt (explains what NEX Brain is)")
    print("   - Lower temperature (0.1)")
    print("   - Shorter max tokens (256)")
    print("   - More stop sequences")
    print("   - Answer cleanup function")

if __name__ == "__main__":
    main()