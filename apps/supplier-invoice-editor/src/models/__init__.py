# src/models/__init__.py
"""
Invoice Editor - Data Models
Python dataclasses pre NEX Genesis tabuľky
"""

from .barcode import BarcodeRecord
from .gscat import GSCATRecord
from .pab import PABRecord
from .mglst import MGLSTRecord

__all__ = [
    'BarcodeRecord',
    'GSCATRecord',
    'PABRecord',
    'MGLSTRecord',
]

__version__ = '1.0.0'
