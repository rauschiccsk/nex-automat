"""
UI components for NEX Automat.

Classes:
    BaseWindow: Base class for all windows with persistence
    BaseGrid: Base class for all grids with advanced features
    GreenHeaderView: Custom header with green highlighting
    QuickSearchEdit: Quick search input widget
    QuickSearchContainer: Container for quick search
    QuickSearchController: Controller for quick search logic
"""

from shared_pyside6.ui.base_grid import BaseGrid, GreenHeaderView
from shared_pyside6.ui.base_window import BaseWindow
from shared_pyside6.ui.quick_search import (
    QuickSearchContainer,
    QuickSearchController,
    QuickSearchEdit,
)

__all__ = [
    "BaseWindow",
    "BaseGrid",
    "GreenHeaderView",
    "QuickSearchEdit",
    "QuickSearchContainer",
    "QuickSearchController",
]
