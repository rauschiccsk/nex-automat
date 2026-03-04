"""Systémové cesty — Windows NEX Genesis a Linux knowledge."""
import os

# NEX Genesis (Windows)
NEX_ROOT_PATH = os.getenv("NEX_ROOT", "C:/NEX")
NEX_YEARACT_PATH = os.getenv("NEX_YEARACT", f"{NEX_ROOT_PATH}/YEARACT")
NEX_STORES_PATH = os.getenv("NEX_STORES", f"{NEX_YEARACT_PATH}/STORES")
NEX_SQLITE_PATH = os.getenv("NEX_SQLITE", f"{NEX_YEARACT_PATH}/SYSTEM/SQLITE")
ARCHIVE_PATH = os.getenv("ARCHIVE_PATH", f"{NEX_YEARACT_PATH}/ARCHIV")

# Linux knowledge
KNOWLEDGE_DIR = os.getenv("KNOWLEDGE_DIR", "/opt/nex-automat-src/docs/knowledge-import")
MANIFEST_PATH = os.getenv("MANIFEST_PATH", "/opt/nex-automat-src/docs/manifest.json")
