"""
LLM Service - Integration with Ollama.
"""

from typing import Any

import httpx
from config.settings import settings

from api.services.rag_service import RAGService

SYSTEM_PROMPT = """Si NEX Brain asistent pre NEX ERP system. Odpovedaj po slovensky.

PRAVIDLA:
1. Pouzivaj informacie z KONTEXTU nizsie
2. Ak kontext obsahuje relevantne informacie, VZDY ich pouzij v odpovedi
3. Ak kontext neobsahuje ziadne relevantne info, povedz ze nemas dostatok informacii
4. Mozes odpovedat podrobnejsie (5-10 viet ak treba)
5. Formatuj odpoved citatelne"""


class LLMService:
    """Service for LLM (Ollama) interactions."""

    def __init__(self):
        self.base_url = settings.OLLAMA_URL
        self.model_name = settings.OLLAMA_MODEL
        self.rag_service = RAGService()

    async def generate(
        self,
        question: str,
        context: list[dict[str, Any]] | None = None,
        tenant: str = "default",
    ) -> tuple[str, int]:
        """Generate answer using Ollama."""

        if context:
            context_text = self.rag_service.format_context(context)
            prompt = f"""{SYSTEM_PROMPT}

KONTEXT (pouzij TIETO informacie):
{context_text}

Otazka: {question}
Odpoved:"""
        else:
            prompt = f"""{SYSTEM_PROMPT}

Otazka: {question}
Odpoved:"""

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model_name,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.3,
                            "num_predict": 500,
                            "top_p": 0.7,
                            "repeat_penalty": 1.1,
                            "stop": ["Otazka:", "KONTEXT:"],
                        },
                    },
                )
                response.raise_for_status()
                data = response.json()

                answer = data.get("response", "").strip()
                answer = self._clean_answer(answer)
                tokens = data.get("eval_count", 0)

                return answer, tokens

        except httpx.RequestError as e:
            return f"Chyba: {e}", 0

    def _clean_answer(self, answer: str) -> str:
        """Remove prompt leakage."""
        for pattern in ["KONTEXT", "Otazka:", "Odpoved:", "DOLEZITE"]:
            if pattern in answer:
                answer = answer.split(pattern)[0].strip()
        return answer

    async def health_check(self) -> bool:
        """Check if Ollama is running."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except:
            return False
