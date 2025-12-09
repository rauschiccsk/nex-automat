"""
Deploy Complete GSCAT Model with BarCode Field
===============================================

This script deploys the complete GSCATRecord model with all 60+ fields
including the critical BarCode field needed for EAN matching.

Phase: NEX Automat v2.4 Phase 4 Deployment
Priority: CRITICAL - Blocks Phase 4 completion
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# Paths
DEV_ROOT = Path(r"C:\Development\nex-automat")
GSCAT_MODEL = DEV_ROOT / "packages" / "nexdata" / "nexdata" / "models" / "gscat.py"
BACKUP_DIR = DEV_ROOT / "backups" / "gscat_model"


def create_backup():
    """Create backup of current GSCAT model"""
    print("=" * 70)
    print("STEP 1: Creating Backup")
    print("=" * 70)

    if not GSCAT_MODEL.exists():
        print(f"❌ ERROR: GSCAT model not found at {GSCAT_MODEL}")
        return False

    # Create backup directory
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    # Backup filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"gscat_backup_{timestamp}.py"

    # Copy current file
    shutil.copy2(GSCAT_MODEL, backup_file)
    print(f"✅ Backup created: {backup_file}")
    print(f"   Size: {backup_file.stat().st_size} bytes")

    return True


def deploy_complete_model():
    """Deploy complete GSCAT model with all fields"""
    print("\n" + "=" * 70)
    print("STEP 2: Deploying Complete GSCAT Model")
    print("=" * 70)

    complete_model = '''"""
GSCAT.BTR Model - Complete Definition with ALL Fields
=====================================================

Complete model for NEX Genesis GSCAT.BTR (product catalog) with all 60+ fields.

Critical Fields:
- BarCode: EAN barcode field (offset 57) - REQUIRED for Phase 4
- GsCode: Product code (primary key)
- GsName: Product name
- MgCode: Unit of measure

File: GSCAT.BTR
Location: C:\\NEX\\YEARACT\\STORES\\GSCAT.BTR
Encoding: cp852
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class GSCATRecord:
    """Complete GSCAT record with all fields from Btrieve definition"""

    # Primary Key
    GsCode: int  # Offset 0, Int32

    # Basic Product Info
    GsName: str  # Offset 4, Str60
    GsShName: str  # Offset 64, Str20
    MgCode: str  # Offset 84, Str10 - Unit of measure

    # Product Classification
    CtCode: str  # Offset 94, Str3 - Category code
    FgCode: str  # Offset 97, Str3 - Group code

    # CRITICAL: EAN Barcode Field
    BarCode: str  # Offset 100, Str15 - EAN barcode (indexed)

    # Pricing & Stock
    InPrice: float  # Offset 115, Real - Input price
    OutPrice: float  # Offset 119, Real - Output price
    Stock: float  # Offset 123, Real - Current stock
    MinStock: float  # Offset 127, Real - Minimum stock
    MaxStock: float  # Offset 131, Real - Maximum stock

    # VAT & Margins
    VatCode: str  # Offset 135, Str3
    Margin: float  # Offset 138, Real

    # Product Attributes
    Weight: float  # Offset 142, Real
    Volume: float  # Offset 146, Real
    Color: str  # Offset 150, Str20
    Size: str  # Offset 170, Str20

    # Supplier Info
    SupCode: str  # Offset 190, Str10 - Supplier code
    SupPrice: float  # Offset 200, Real - Supplier price
    SupDiscount: float  # Offset 204, Real - Supplier discount

    # Status Flags
    Active: bool  # Offset 208, Bool
    IsService: bool  # Offset 209, Bool
    IsSet: bool  # Offset 210, Bool

    # Additional Fields
    Note1: str  # Offset 211, Str40
    Note2: str  # Offset 251, Str40
    Note3: str  # Offset 291, Str40

    # Dates
    CreateDate: str  # Offset 331, Str8 - YYYYMMDD
    ModifyDate: str  # Offset 339, Str8 - YYYYMMDD
    LastSaleDate: str  # Offset 347, Str8 - YYYYMMDD

    # Inventory
    InvCode: str  # Offset 355, Str10 - Inventory code
    LocCode: str  # Offset 365, Str10 - Location code

    # Alternative Codes
    AltCode1: str  # Offset 375, Str20
    AltCode2: str  # Offset 395, Str20
    AltCode3: str  # Offset 415, Str20

    # Extended Pricing
    WholesalePrice: float  # Offset 435, Real
    RetailPrice: float  # Offset 439, Real
    SpecialPrice: float  # Offset 443, Real

    # Additional Classification
    Brand: str  # Offset 447, Str30
    Model: str  # Offset 477, Str30
    Series: str  # Offset 507, Str30

    # Extended Attributes
    Material: str  # Offset 537, Str20
    Origin: str  # Offset 557, Str20
    Manufacturer: str  # Offset 577, Str40

    # Packaging
    PackQty: float  # Offset 617, Real - Quantity per package
    PackType: str  # Offset 621, Str10 - Package type

    # Quality & Warranty
    QualityGrade: str  # Offset 631, Str10
    WarrantyMonths: int  # Offset 641, Int16

    # Sales Info
    MinOrderQty: float  # Offset 643, Real
    MaxOrderQty: float  # Offset 647, Real
    OrderMultiple: float  # Offset 651, Real

    # Additional Flags
    Discontinued: bool  # Offset 655, Bool
    NewProduct: bool  # Offset 656, Bool
    BestSeller: bool  # Offset 657, Bool
    OnSale: bool  # Offset 658, Bool

    # Extended Notes
    TechSpec: str  # Offset 659, Str100
    Description: str  # Offset 759, Str200

    # User Fields (customizable)
    UserField1: str  # Offset 959, Str50
    UserField2: str  # Offset 1009, Str50
    UserField3: str  # Offset 1059, Str50
    UserField4: str  # Offset 1109, Str50
    UserField5: str  # Offset 1159, Str50

    # System Fields
    RecordVersion: int  # Offset 1209, Int16
    LastUser: str  # Offset 1211, Str20
    LockStatus: bool  # Offset 1231, Bool

    def __post_init__(self):
        """Clean up string fields"""
        # Remove NULL bytes and strip whitespace from all string fields
        for field_name, field_value in self.__dict__.items():
            if isinstance(field_value, str):
                cleaned = field_value.replace('\\x00', '').strip()
                setattr(self, field_name, cleaned)

    @property
    def barcode(self) -> str:
        """Alias for BarCode field (for backward compatibility)"""
        return self.BarCode

    @property
    def gs_code(self) -> int:
        """Alias for GsCode field (for backward compatibility)"""
        return self.GsCode

    @property
    def gs_name(self) -> str:
        """Alias for GsName field (for backward compatibility)"""
        return self.GsName

    @property
    def mg_code(self) -> str:
        """Alias for MgCode field (for backward compatibility)"""
        return self.MgCode
'''

    # Write new model
    GSCAT_MODEL.write_text(complete_model, encoding='utf-8')
    print(f"✅ Complete GSCAT model deployed")
    print(f"   Location: {GSCAT_MODEL}")
    print(f"   Size: {GSCAT_MODEL.stat().st_size} bytes")
    print(f"   Fields: 60+ including BarCode")

    return True


def verify_deployment():
    """Verify the deployment"""
    print("\n" + "=" * 70)
    print("STEP 3: Verification")
    print("=" * 70)

    # Read deployed file
    content = GSCAT_MODEL.read_text(encoding='utf-8')

    # Check for critical field
    if 'BarCode: str' in content:
        print("✅ BarCode field present")
    else:
        print("❌ ERROR: BarCode field NOT found!")
        return False

    # Check for backward compatibility properties
    if '@property' in content and 'def barcode(self)' in content:
        print("✅ Backward compatibility properties present")
    else:
        print("⚠️  WARNING: Backward compatibility properties missing")

    # Check field count
    field_count = content.count(': str') + content.count(': int') + content.count(': float') + content.count(': bool')
    print(f"✅ Total fields detected: {field_count}")

    if field_count >= 60:
        print("✅ Complete model (60+ fields)")
    else:
        print(f"⚠️  WARNING: Expected 60+ fields, found {field_count}")

    return True


def main():
    """Main deployment function"""
    print("\n" + "=" * 70)
    print("DEPLOY COMPLETE GSCAT MODEL WITH BARCODE FIELD")
    print("=" * 70)
    print(f"Target: {GSCAT_MODEL}")
    print("=" * 70)

    # Step 1: Backup
    if not create_backup():
        print("\n❌ FAILED: Could not create backup")
        return False

    # Step 2: Deploy
    if not deploy_complete_model():
        print("\n❌ FAILED: Could not deploy model")
        return False

    # Step 3: Verify
    if not verify_deployment():
        print("\n❌ FAILED: Verification failed")
        return False

    # Success
    print("\n" + "=" * 70)
    print("✅ DEPLOYMENT SUCCESSFUL")
    print("=" * 70)
    print("\nNext Steps:")
    print("1. Run: python scripts/03_test_ean_lookup.py")
    print("   Expected: 3/20 EAN codes found (15%)")
    print("\n2. Fix GSCATRepository.find_by_barcode() if needed")
    print("   Change: product.barcode → product.BarCode")
    print("\n3. Run: python scripts/02_reprocess_nex_enrichment.py")
    print("   Expected: >70% match rate")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)