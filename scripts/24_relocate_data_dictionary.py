#!/usr/bin/env python3
"""
Script 24: Relocate DATA_DICTIONARY.md-old

Relocates from docs/architecture/database/ to docs/database/
Renames to MIGRATION_MAPPING.md
Updates header with new metadata
"""

import shutil
from pathlib import Path

# Paths
REPO_ROOT = Path(r"C:\Development\nex-automat")
SOURCE = REPO_ROOT / "docs/architecture/database/DATA_DICTIONARY.md-old"
TARGET = REPO_ROOT / "docs/database/MIGRATION_MAPPING.md"


def update_header(content):
    """Update document header"""

    new_header = """# Migration Mapping - Btrieve to PostgreSQL

**Category:** Database  
**Status:** 🟢 Complete  
**Created:** 2024-12-10  
**Updated:** 2025-12-15  
**Related:** [DATABASE_PRINCIPLES.md](DATABASE_PRINCIPLES.md), [RELATIONSHIPS.md](RELATIONSHIPS.md)

---

## Overview

Complete field-level mapping from NEX Genesis Btrieve files to NEX Automat PostgreSQL schema.
Documents naming conventions, data type mappings, and common patterns.

---

"""

    # Find where main content starts
    sections_start = content.find("## 📋 OBSAH")
    if sections_start == -1:
        sections_start = content.find("## NAMING CONVENTIONS")

    if sections_start == -1:
        return new_header + content

    main_content = content[sections_start:]
    return new_header + main_content


def main():
    print("=" * 80)
    print("Script 24: Relocate DATA_DICTIONARY.md-old")
    print("=" * 80)

    if not SOURCE.exists():
        print(f"\n❌ ERROR: Source not found: {SOURCE}")
        return False

    print(f"\n✅ Source: {SOURCE.name} ({SOURCE.stat().st_size:,} bytes)")

    # Read and update
    print("\n" + "=" * 80)
    print("Step 1: Reading and updating content")
    print("=" * 80)

    with open(SOURCE, 'r', encoding='utf-8') as f:
        content = f.read()

    updated_content = update_header(content)
    print(f"✅ Content updated ({len(updated_content):,} chars)")

    # Create target
    print("\n" + "=" * 80)
    print("Step 2: Creating target document")
    print("=" * 80)

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    with open(TARGET, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"✅ Created: {TARGET.relative_to(REPO_ROOT)}")
    print(f"   New location: docs/database/")
    print(f"   New name: MIGRATION_MAPPING.md")

    # Delete original
    print("\n" + "=" * 80)
    print("Step 3: Deleting original .md-old")
    print("=" * 80)

    SOURCE.unlink()
    print(f"✅ Deleted: {SOURCE.name}")

    # Summary
    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)

    print("\n✅ Relocated: DATA_DICTIONARY.md-old")
    print(f"   From: docs/architecture/database/")
    print(f"   To:   docs/database/MIGRATION_MAPPING.md")

    print("\n📋 Document covers:")
    print("   - Naming conventions (PK, FK, boolean, dates)")
    print("   - Data type mapping (Btrieve → PostgreSQL)")
    print("   - Common patterns (universal tables, triggers)")
    print("   - Field mappings:")
    print("     • Products (GSCAT → products)")
    print("     • Product categories (MGLST, FGLST, SGLST)")
    print("     • Product identifiers (BARCODE)")
    print("     • Partners (PAB → partners + 7 tables)")
    print("     • Stock management")

    print("\n📋 Update index:")
    print("   - docs/database/00_DATABASE_INDEX.md")

    print("\n✅ Script completed")
    print("=" * 80)

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)