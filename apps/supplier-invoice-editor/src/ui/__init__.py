"""UI package"""
import sys
from pathlib import Path

# Add nex-shared to path BEFORE any imports
nex_shared_path = Path(__file__).parent.parent.parent.parent / "packages" / "nex-shared"
if str(nex_shared_path) not in sys.path:
    sys.path.insert(0, str(nex_shared_path))

from .main_window import MainWindow

__all__ = ['MainWindow']
