"""
Fix nexdata/__init__.py - correct import names
"""

from pathlib import Path

INIT_FILE = Path("packages/nexdata/nexdata/__init__.py")

# Correct __init__.py content
INIT_CONTENT = '''"""
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
'''


def fix_init():
    print("=" * 60)
    print("FIX: nexdata/__init__.py imports")
    print("=" * 60)

    if not INIT_FILE.exists():
        print(f"❌ File not found: {INIT_FILE}")
        return False

    print(f"\n📄 Updating: {INIT_FILE}")
    print("-" * 60)

    # Write corrected content
    with open(INIT_FILE, "w", encoding="utf-8") as f:
        f.write(INIT_CONTENT)

    size = INIT_FILE.stat().st_size
    print(f"✅ Updated ({size:,} bytes)")

    print("\n📋 Fixed imports:")
    print("   ❌ BARCODERecord → ✅ BarcodeRecord")

    print("\n📋 All model imports:")
    print("   - TSHRecord")
    print("   - TSIRecord")
    print("   - GSCATRecord")
    print("   - BarcodeRecord  ← FIXED")
    print("   - PABRecord")
    print("   - MGLSTRecord")

    print("\n📝 Next step:")
    print("   pip install -e packages/nexdata")
    print('   python -c "from nexdata import *"')

    return True


if __name__ == "__main__":
    success = fix_init()
    exit(0 if success else 1)