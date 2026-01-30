"""Core module for Btrieve-Loader REST API."""

from .btrieve import get_btrieve_client
from .config import settings

__all__ = ["get_btrieve_client", "settings"]
