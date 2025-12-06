"""
NEX Shared Package
Zdieľané komponenty pre NEX Automat systém.
"""
from .ui import BaseWindow, WindowPersistenceManager
from .database import WindowSettingsDB

__version__ = '2.0.0'

__all__ = [
    'BaseWindow',
    'WindowPersistenceManager',
    'WindowSettingsDB',
]
