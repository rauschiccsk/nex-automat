"""
NEX Brain Configuration - Multi-tenant support with local RAG.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with multi-tenant support."""

    # Deployment mode
    MODE: str = "multi-tenant"  # "multi-tenant" or "single-tenant"
    TENANT: str = ""  # For single-tenant mode
    TENANTS: str = "icc,andros,dev"  # Comma-separated list for multi-tenant

    # Qdrant (vector database)
    QDRANT_URL: str = "http://localhost:6333"

    # Ollama (LLM + embeddings)
    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1:8b"
    EMBEDDING_MODEL: str = "nomic-embed-text"
    EMBEDDING_DIMENSIONS: int = 768

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def is_multi_tenant(self) -> bool:
        return self.MODE == "multi-tenant"

    @property
    def tenant_list(self) -> list[str]:
        return [t.strip() for t in self.TENANTS.split(",") if t.strip()]

    def get_tenant(self, request_tenant: str | None = None) -> str:
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
