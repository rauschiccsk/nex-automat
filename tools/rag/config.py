"""
RAG Configuration Module
Loads and validates configuration from config/rag_config.yaml
"""

import os
from pathlib import Path

import yaml
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings


class DatabaseConfig(BaseModel):
    """PostgreSQL database configuration"""

    host: str = "localhost"
    port: int = 5432
    database: str = "nex_automat_rag"
    user: str = "postgres"
    password: str
    pool_min_size: int = Field(default=2, ge=1)
    pool_max_size: int = Field(default=10, ge=1)

    @field_validator("pool_max_size")
    @classmethod
    def validate_pool_size(cls, v: int, info) -> int:
        if "pool_min_size" in info.data and v < info.data["pool_min_size"]:
            raise ValueError("pool_max_size must be >= pool_min_size")
        return v


class EmbeddingConfig(BaseModel):
    """Embedding model configuration"""

    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    dimension: int = Field(default=384, ge=1)
    batch_size: int = Field(default=32, ge=1)
    max_seq_length: int = Field(default=512, ge=1)
    device: str | None = None  # auto-detect if None
    cache_dir: Path | None = None


class VectorIndexConfig(BaseModel):
    """Vector index configuration (HNSW)"""

    index_type: str = "hnsw"
    m: int = Field(default=16, ge=4, le=64)
    ef_construction: int = Field(default=64, ge=8, le=512)
    ef_search: int = Field(default=40, ge=8, le=512)


class ChunkingConfig(BaseModel):
    """Document chunking configuration"""

    chunk_size: int = Field(default=1000, ge=100)
    chunk_overlap: int = Field(default=200, ge=0)
    min_chunk_size: int = Field(default=100, ge=50)

    @field_validator("chunk_overlap")
    @classmethod
    def validate_overlap(cls, v: int, info) -> int:
        if "chunk_size" in info.data and v >= info.data["chunk_size"]:
            raise ValueError("chunk_overlap must be < chunk_size")
        return v


class SearchConfig(BaseModel):
    """Search configuration"""

    default_limit: int = Field(default=10, ge=1, le=100)
    similarity_threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    hybrid_alpha: float = Field(default=0.5, ge=0.0, le=1.0)  # vector vs keyword weight


class RAGConfig(BaseSettings):
    """Main RAG configuration"""

    database: DatabaseConfig
    embedding: EmbeddingConfig
    vector_index: VectorIndexConfig
    chunking: ChunkingConfig
    search: SearchConfig

    model_config = {"arbitrary_types_allowed": True, "extra": "ignore"}


def load_config(config_path: Path | None = None) -> RAGConfig:
    """
    Load RAG configuration from YAML file

    Args:
        config_path: Path to config file, defaults to config/rag_config.yaml

    Returns:
        RAGConfig instance

    Raises:
        FileNotFoundError: If config file not found
        ValueError: If config validation fails
    """
    if config_path is None:
        # Default to project root / config / rag_config.yaml
        project_root = Path(__file__).parent.parent.parent
        config_path = project_root / "config" / "rag_config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    # Load YAML
    with open(config_path, encoding="utf-8") as f:
        config_data = yaml.safe_load(f)

    # Get password from environment if not in config
    if "database" in config_data:
        if "password" not in config_data["database"]:
            password = os.getenv("POSTGRES_PASSWORD")
            if password:
                config_data["database"]["password"] = password

    # Create and validate config
    try:
        config = RAGConfig(**config_data)
        return config
    except Exception as e:
        raise ValueError(f"Config validation failed: {e}")


# Global config instance (lazy loaded)
_config: RAGConfig | None = None


def get_config(reload: bool = False) -> RAGConfig:
    """
    Get global RAG configuration (singleton pattern)

    Args:
        reload: Force reload from file

    Returns:
        RAGConfig instance
    """
    global _config

    if _config is None or reload:
        _config = load_config()

    return _config


if __name__ == "__main__":
    # Test config loading
    print("Testing RAG config loading...")
    try:
        config = load_config()
        print("✓ Config loaded successfully")
        print(
            f"  Database: {config.database.host}:{config.database.port}/{config.database.database}"
        )
        print(
            f"  Embedding: {config.embedding.model_name} (dim={config.embedding.dimension})"
        )
        print(
            f"  Chunking: {config.chunking.chunk_size} chars, overlap={config.chunking.chunk_overlap}"
        )
    except Exception as e:
        print(f"✗ Error: {e}")
