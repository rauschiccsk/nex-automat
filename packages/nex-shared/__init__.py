"""
NEX Shared Package
Zdieľané komponenty pre NEX Automat systém.
"""

from .database import WindowSettingsDB
from .ui import BaseWindow, WindowPersistenceManager

__version__ = "2.0.0"

__all__ = [
    "BaseWindow",
    "WindowPersistenceManager",
    "WindowSettingsDB",
]
