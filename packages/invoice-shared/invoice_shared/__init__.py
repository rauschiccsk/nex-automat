"""
Invoice Shared Package
Zdieľané utility pre invoice processing projekty
"""

__version__ = "0.1.0"

# Export hlavných modulov
from invoice_shared.database.postgres_staging import PostgresStagingClient
from invoice_shared.utils.text_utils import clean_string

__all__ = [
    "PostgresStagingClient",
    "clean_string",
]
