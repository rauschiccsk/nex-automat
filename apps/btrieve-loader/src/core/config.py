"""
Configuration for Btrieve-Loader REST API.

Uses Pydantic Settings for environment-based configuration.
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # API Settings
    api_title: str = Field(default="Btrieve-Loader API", description="API title")
    api_version: str = Field(default="1.0.0", description="API version")
    api_prefix: str = Field(default="/api/v1", description="API prefix")
    api_key: str = Field(default="", description="API key for authentication")
    port: int = Field(default=8001, description="API server port")
    host: str = Field(default="0.0.0.0", description="API server host")
    debug: bool = Field(default=False, description="Debug mode")

    # Btrieve Settings
    btrieve_path: Path = Field(
        default=Path(r"C:\NEX\YEARACT\STORES"),
        description="Path to Btrieve database files",
    )
    btrieve_dials_path: Path = Field(
        default=Path(r"C:\NEX\YEARACT\DIALS"),
        description="Path to Btrieve DIALS files (PAB, etc.)",
    )
    btrieve_encoding: str = Field(
        default="cp852",
        description="Character encoding for Btrieve data",
    )
    btrieve_owner: str = Field(
        default="",
        description="Btrieve file owner password (if secured)",
    )

    # Database config path (for BtrieveClient)
    database_config_path: Path | None = Field(
        default=None,
        description="Path to database.yaml config file",
    )

    # Pagination defaults
    default_page_size: int = Field(default=50, description="Default page size")
    max_page_size: int = Field(default=1000, description="Maximum page size")

    @property
    def btrieve_config(self) -> dict:
        """Generate config dict for BtrieveClient."""
        return {
            "database_path": str(self.btrieve_path),
            "nex_genesis": {
                "tables": {
                    "gscat": str(self.btrieve_path / "GSCAT.BTR"),
                    "barcode": str(self.btrieve_path / "BARCODE.BTR"),
                    "mglst": str(self.btrieve_path / "MGLST.BTR"),
                    "tsh": str(self.btrieve_path / "TSHA-{book_id}.BTR"),
                    "tsi": str(self.btrieve_path / "TSIA-{book_id}.BTR"),
                    "pab": str(self.btrieve_dials_path / "PAB00000.BTR"),
                }
            },
        }


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
