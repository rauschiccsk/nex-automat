"""
NEX Data Package
Common models, repositories and utilities for NEX Genesis integration
"""

# Btrieve
from .btrieve.btrieve_client import BtrieveClient

# Models
from .models.tsh import TSHRecord
from .models.tsi import TSIRecord
from .models.gscat import GSCATRecord
from .models.barcode import BarcodeRecord
from .models.pab import PABRecord
from .models.mglst import MGLSTRecord

# Repositories
from .repositories import (
    BaseRepository,
    TSHRepository,
    TSIRepository,
    GSCATRepository,
    BARCODERepository,
    PABRepository,
    MGLSTRepository,
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
