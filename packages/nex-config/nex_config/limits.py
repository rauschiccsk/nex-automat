"""Limity — page sizes, batch sizes, retries, buffer sizes."""

MAX_RETRIES = 3
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 1000
PAB_BATCH_SIZE = 100
RAG_BATCH_SIZE = 32
EMBEDDING_MAX_CHARS = 8000

# MuFis API page size — used by eshop/router.py getOrder & getProduct handlers.
# Centralized here so both call sites read from one source.
MUFIS_PAGE_SIZE = 50
