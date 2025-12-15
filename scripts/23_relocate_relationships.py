#!/usr/bin/env python3
"""
Script 23: Relocate DATABASE_RELATIONSHIPS.md-old

Relocates from docs/architecture/database/ to docs/database/
Renames to RELATIONSHIPS.md
Updates header with new metadata
"""

import shutil
from pathlib import Path
import re

# Paths
REPO_ROOT = Path(r"C:\Development\nex-automat")
SOURCE = REPO_ROOT / "docs/architecture/database/DATABASE_RELATIONSHIPS.md-old"
TARGET = REPO_ROOT / "docs/database/RELATIONSHIPS.md"


def update_header(content):
    """Update document header"""

    # New header
    new_header = """# Database Relationships

**Category:** Database  
**Status:** 🟢 Complete  
**Created:** 2024-12-10  
**Updated:** 2025-12-15  
**Related:** [DATABASE_PRINCIPLES.md](DATABASE_PRINCIPLES.md)

---

## Overview

Cross-system database relationships, foreign key constraints, cascading rules, and business logic.

---

"""

    # Find where main content starts (after first ---)
    # Skip old header up to first "## PREHĽAD KATEGÓRIÍ" or similar
    sections_start = content.find("## PREHĽAD KATEGÓRIÍ")
    if sections_start == -1:
        sections_start = content.find("## 1.")

    if sections_start == -1:
        # Fallback - just prepend new header
        return new_header + content

    # Keep content from first section onwards
    main_content = content[sections_start:]

    return new_header + main_content


def main():
    print("=" * 80)
    print("Script 23: Relocate DATABASE_RELATIONSHIPS.md-old")
    print("=" * 80)

    if not SOURCE.exists():
        print(f"\n❌ ERROR: Source not found: {SOURCE}")
        return False

    print(f"\n✅ Source: {SOURCE.name} ({SOURCE.stat().st_size:,} bytes)")

    # Read source
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
    print(f"   New name: RELATIONSHIPS.md")

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

    print("\n✅ Relocated: DATABASE_RELATIONSHIPS.md-old")
    print(f"   From: docs/architecture/database/")
    print(f"   To:   docs/database/RELATIONSHIPS.md")

    print("\n📋 Document covers:")
    print("   - Catalog relationships (Products, Partners)")
    print("   - Cross-system relationships (Catalogs ↔ Stock ↔ Accounting)")
    print("   - Foreign key constraints and cascading rules")
    print("   - Archive document patterns (no FK constraints)")
    print("   - Performance indexes")
    print("   - Business rules")

    print("\n📋 Update index:")
    print("   - docs/database/00_DATABASE_INDEX.md")

    print("\n✅ Script completed")
    print("=" * 80)

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)