#!/usr/bin/env python
"""
Setup script for shared-pyside6 package.
Creates package structure with all necessary files.
"""
import os
from pathlib import Path

BASE_DIR = Path(r"C:\Development\nex-automat")
PACKAGE_DIR = BASE_DIR / "packages" / "shared-pyside6"


def create_file(path: Path, content: str) -> None:
    """Create file with content."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"✅ Created: {path.relative_to(BASE_DIR)}")


def main():
    print("=" * 60)
    print("Setting up shared-pyside6 package")
    print("=" * 60)

    # === pyproject.toml ===
    create_file(PACKAGE_DIR / "pyproject.toml", '''[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "shared-pyside6"
version = "1.0.0"
description = "Shared PySide6 components for NEX Automat"
readme = "README.md"
requires-python = ">=3.11"
license = {text = "Proprietary"}
authors = [
    {name = "ICC Komárno", email = "info@icc.sk"}
]

dependencies = [
    "PySide6>=6.5.0",
    "openpyxl>=3.1.0",
    "asyncpg>=0.28.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-qt>=4.2.0",
]

[tool.setuptools.packages.find]
where = ["."]
include = ["shared_pyside6*"]
''')

    # === README.md ===
    create_file(PACKAGE_DIR / "README.md", '''# shared-pyside6

Shared PySide6 components for NEX Automat system.

## Features

- **BaseWindow** - Window persistence (position, size, maximize state)
- **BaseGrid** - Grid persistence with advanced features:
  - Column widths, order, visibility
  - Custom headers
  - Row cursor memory
  - Export to Excel/CSV
  - Inline editing
- **QuickSearch** - NEX Genesis style incremental search

## Installation

```bash
cd packages/shared-pyside6
pip install -e .
```

## Usage

```python
from shared_pyside6.ui import BaseWindow, BaseGrid

class MyWindow(BaseWindow):
    def __init__(self):
        super().__init__(
            window_name="my_window",
            default_size=(1024, 768),
            user_id="user123"
        )
```

## Requirements

- Python 3.11+
- PySide6 6.5+
- PostgreSQL (for persistence)
''')

    # === Main package __init__.py ===
    create_file(PACKAGE_DIR / "shared_pyside6" / "__init__.py", '''"""
shared-pyside6: Shared PySide6 components for NEX Automat.

Modules:
    ui: GUI components (BaseWindow, BaseGrid, QuickSearch)
    database: Database utilities
    utils: Helper utilities
"""
__version__ = "1.0.0"

from shared_pyside6.ui import BaseWindow, BaseGrid
''')

    # === UI package __init__.py ===
    create_file(PACKAGE_DIR / "shared_pyside6" / "ui" / "__init__.py", '''"""
UI components for NEX Automat.

Classes:
    BaseWindow: Base class for all windows with persistence
    BaseGrid: Base class for all grids with advanced features
    QuickSearchEdit: Quick search input widget
    QuickSearchContainer: Container for quick search
    QuickSearchController: Controller for quick search logic
    GreenHeaderView: Custom header with green highlighting
    ColumnChooserDialog: Dialog for column settings
"""
from shared_pyside6.ui.base_window import BaseWindow
from shared_pyside6.ui.base_grid import BaseGrid, GreenHeaderView
from shared_pyside6.ui.quick_search import (
    QuickSearchEdit,
    QuickSearchContainer, 
    QuickSearchController
)

__all__ = [
    "BaseWindow",
    "BaseGrid",
    "GreenHeaderView",
    "QuickSearchEdit",
    "QuickSearchContainer",
    "QuickSearchController",
]
''')

    # === Database package __init__.py ===
    create_file(PACKAGE_DIR / "shared_pyside6" / "database" / "__init__.py", '''"""
Database utilities for NEX Automat.

Classes:
    SettingsRepository: Repository for user settings persistence
"""
from shared_pyside6.database.settings_repository import SettingsRepository

__all__ = ["SettingsRepository"]
''')

    # === Utils package __init__.py ===
    create_file(PACKAGE_DIR / "shared_pyside6" / "utils" / "__init__.py", '''"""
Utility functions for NEX Automat.
"""
''')

    # === Placeholder files (to be implemented) ===
    create_file(PACKAGE_DIR / "shared_pyside6" / "ui" / "base_window.py", '''"""
BaseWindow - Base class for all windows with persistence.
TODO: Implement in Phase 2
"""
from PySide6.QtWidgets import QMainWindow

class BaseWindow(QMainWindow):
    """Placeholder - to be implemented."""
    pass
''')

    create_file(PACKAGE_DIR / "shared_pyside6" / "ui" / "base_grid.py", '''"""
BaseGrid - Base class for all grids with advanced features.
TODO: Implement in Phase 3-4
"""
from PySide6.QtWidgets import QWidget, QHeaderView

class GreenHeaderView(QHeaderView):
    """Placeholder - to be implemented."""
    pass

class BaseGrid(QWidget):
    """Placeholder - to be implemented."""
    pass
''')

    create_file(PACKAGE_DIR / "shared_pyside6" / "ui" / "quick_search.py", '''"""
QuickSearch - NEX Genesis style incremental search.
TODO: Implement in Phase 5
"""
from PySide6.QtWidgets import QLineEdit, QWidget
from PySide6.QtCore import QObject

class QuickSearchEdit(QLineEdit):
    """Placeholder - to be implemented."""
    pass

class QuickSearchContainer(QWidget):
    """Placeholder - to be implemented."""
    pass

class QuickSearchController(QObject):
    """Placeholder - to be implemented."""
    pass
''')

    create_file(PACKAGE_DIR / "shared_pyside6" / "database" / "settings_repository.py", '''"""
SettingsRepository - Repository for user settings persistence.
TODO: Implement
"""

class SettingsRepository:
    """Placeholder - to be implemented."""
    pass
''')

    # === Tests directory ===
    create_file(PACKAGE_DIR / "tests" / "__init__.py", '''"""Tests for shared-pyside6 package."""
''')

    create_file(PACKAGE_DIR / "tests" / "test_imports.py", '''"""Test that all imports work correctly."""
import pytest


def test_pyside6_available():
    """Test that PySide6 is installed."""
    import PySide6
    assert PySide6 is not None


def test_package_import():
    """Test that package can be imported."""
    import shared_pyside6
    assert shared_pyside6.__version__ == "1.0.0"


def test_ui_imports():
    """Test UI component imports."""
    from shared_pyside6.ui import BaseWindow, BaseGrid
    assert BaseWindow is not None
    assert BaseGrid is not None
''')

    print()
    print("=" * 60)
    print("✅ Package structure created!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Run: cd packages/shared-pyside6")
    print("2. Run: pip install -e .")
    print("3. Run: pytest tests/ -v")
    print()


if __name__ == "__main__":
    main()