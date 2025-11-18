# src/btrieve/__init__.py
"""
Btrieve Client Module

Python wrapper pre Pervasive PSQL Btrieve API
"""

from .btrieve_client import BtrieveClient, open_btrieve_file

__all__ = [
    'BtrieveClient',
    'open_btrieve_file',
]

__version__ = '0.2.1'