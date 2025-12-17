# shared-pyside6

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
