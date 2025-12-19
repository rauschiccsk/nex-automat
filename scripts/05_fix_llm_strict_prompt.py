#!/usr/bin/env python
"""
Fix llm_service.py - Even stricter prompt to prevent hallucinations.
"""

from pathlib import Path

FILE_PATH = Path("C:/Development/nex-automat/apps/nex-brain/api/services/llm_service.py")

CONTENT = '''"""
LLM Service - Integration with Ollama.
"""

import httpx
from typing import Tuple, List, Dict, Any, Optional
from config.settings import settings
from api.services.rag_service import RAGService


SYSTEM_PROMPT = """Si NEX Brain asistent. Odpovedaj STRUCNE po slovensky.

DOLEZITE PRAVIDLA:
1. Pouzivaj IBA informacie z KONTEXTU nizsie
2. Ak nieco nie je v kontexte, povedz "Nemam tuto informaciu"
3. NIKDY si nevymyslaj fakty
4. Max 2-3 vety
5. Ziadne ** ani ## formatovanie"""


class LLMService:
    """Service for LLM (Ollama) interactions."""

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
                            "temperature": 0.0,
                            "num_predict": 150,
                            "top_p": 0.1,
                            "repeat_penalty": 1.2,
                            "stop": ["Otazka:", "KONTEXT:", "\\n\\n\\n"],
                        }
                    }
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
'''


def main():
    FILE_PATH.write_text(CONTENT, encoding="utf-8")
    print("✅ Fixed: llm_service.py")
    print("   - temperature=0.0 (deterministic)")
    print("   - top_p=0.1 (very focused)")
    print("   - repeat_penalty=1.2")
    print("   - Simpler, stricter prompt")


if __name__ == "__main__":
    main()