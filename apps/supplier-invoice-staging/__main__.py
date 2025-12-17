"""Entry point: python -m supplier_invoice_staging"""
import sys
from pathlib import Path

app_root = Path(__file__).parent
if str(app_root) not in sys.path:
    sys.path.insert(0, str(app_root))

from app import main

if __name__ == "__main__":
    sys.exit(main())
