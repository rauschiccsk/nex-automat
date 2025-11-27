"""
Update __init__.py files in nex-shared package
"""

from pathlib import Path

# Paths
REPOSITORIES_INIT = Path("packages/nex-shared/repositories/__init__.py")
MAIN_INIT = Path("packages/nex-shared/__init__.py")

# Content for repositories/__init__.py
REPOSITORIES_INIT_CONTENT = '''"""
NEX Shared - Repositories
"""

from .base_repository import BaseRepository
from .tsh_repository import TSHRepository
from .tsi_repository import TSIRepository
from .gscat_repository import GSCATRepository
from .barcode_repository import BARCODERepository
from .pab_repository import PABRepository
from .mglst_repository import MGLSTRepository

__all__ = [
    "BaseRepository",
    "TSHRepository",
    "TSIRepository",
    "GSCATRepository",
    "BARCODERepository",
    "PABRepository",
    "MGLSTRepository",
]
'''

# Content for main __init__.py
MAIN_INIT_CONTENT = '''"""
NEX Shared Package
Common models, repositories and utilities for NEX Genesis integration
"""

# Btrieve
from .btrieve.btrieve_client import BtrieveClient

# Models
from .models.tsh import TSHRecord
from .models.tsi import TSIRecord
from .models.gscat import GSCATRecord
from .models.barcode import BARCODERecord
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
    "BARCODERecord",
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


def update_init_files():
    print("=" * 60)
    print("UPDATE: __init__.py Files")
    print("=" * 60)

    files_updated = 0

    # Update repositories/__init__.py
    print(f"\n📄 {REPOSITORIES_INIT}")
    print("-" * 60)

    try:
        with open(REPOSITORIES_INIT, "w", encoding="utf-8") as f:
            f.write(REPOSITORIES_INIT_CONTENT)

        size = REPOSITORIES_INIT.stat().st_size
        print(f"✅ Updated ({size:,} bytes)")
        print("   Exports: 7 repositories")
        files_updated += 1

    except Exception as e:
        print(f"❌ Error: {e}")

    # Update main __init__.py
    print(f"\n📄 {MAIN_INIT}")
    print("-" * 60)

    try:
        with open(MAIN_INIT, "w", encoding="utf-8") as f:
            f.write(MAIN_INIT_CONTENT)

        size = MAIN_INIT.stat().st_size
        print(f"✅ Updated ({size:,} bytes)")
        print("   Exports:")
        print("     - 1 Btrieve client")
        print("     - 6 Models")
        print("     - 7 Repositories")
        files_updated += 1

    except Exception as e:
        print(f"❌ Error: {e}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"  ✅ Updated: {files_updated}/2")
    print("=" * 60)

    if files_updated == 2:
        print("\n📋 Package structure:")
        print("   from nex_shared import BtrieveClient")
        print("   from nex_shared import TSHRecord, TSIRecord")
        print("   from nex_shared import TSHRepository, TSIRepository")
        print("   from nex_shared import GSCATRepository, BARCODERepository")
        print("   from nex_shared import PABRepository, MGLSTRepository")

        print("\n📝 Next step:")
        print("   Test import: python -c \"from nex_shared import *\"")

    return files_updated == 2


if __name__ == "__main__":
    success = update_init_files()
    exit(0 if success else 1)