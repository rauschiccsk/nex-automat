"""
NEX Data Package
Common models, repositories and utilities for NEX Genesis integration
"""

# Btrieve
from .btrieve.btrieve_client import BtrieveClient
from .models.barcode import BarcodeRecord
from .models.gscat import GSCATRecord
from .models.mglst import MGLSTRecord
from .models.pab import PABRecord

# Models
from .models.tsh import TSHRecord
from .models.tsi import TSIRecord

# Repositories
from .repositories import (
    BARCODERepository,
    BaseRepository,
    GSCATRepository,
    MGLSTRepository,
    PABRepository,
    TSHRepository,
    TSIRepository,
)

__version__ = "0.1.0"

__all__ = [
    # Btrieve
    "BtrieveClient",
    # Models
    "TSHRecord",
    "TSIRecord",
    "GSCATRecord",
    "BarcodeRecord",
    "PABRecord",
    "MGLSTRecord",
    # Repositories
    "BaseRepository",
    "TSHRepository",
    "TSIRepository",
    "GSCATRepository",
    "BARCODERepository",
    "PABRepository",
    "MGLSTRepository",
]
