#!/usr/bin/env python3
"""
Script 29: Relocate sales/INDEX.md-old → SALES_REFERENCE.md
Reason: Active sales system documentation with business logic
"""

from pathlib import Path


def update_header(content: str) -> str:
    """Update document header for new location."""

    new_header = """# Sales Reference - Odbytový systém

**Category:** Database / Sales  
**Status:** 🟡 In Progress (1/10 tables documented)  
**Created:** 2025-12-10  
**Updated:** 2025-12-15  
**Related:** [CATALOGS_REFERENCE.md](CATALOGS_REFERENCE.md), [PRODUCTS_REFERENCE.md](PRODUCTS_REFERENCE.md)

---

"""

    # Find end of original header and replace
    parts = content.split('\n---\n', 1)
    if len(parts) == 2:
        return new_header + parts[1]
    return new_header + content


def main():
    """Relocate sales index to database docs."""

    # Paths
    source = Path(r"C:\Development\nex-automat\docs\architecture\database\sales\INDEX.md-old")
    target = Path(r"C:\Development\nex-automat\docs\database\SALES_REFERENCE.md")

    print("=" * 70)
    print("Script 29: Relocate Sales Index")
    print("=" * 70)

    # Check source
    if not source.exists():
        print(f"\n❌ Source not found: {source}")
        return False

    print(f"\n📄 Source:")
    print(f"   {source}")
    print(f"   Size: {source.stat().st_size:,} bytes")

    print(f"\n📄 Target:")
    print(f"   {target}")

    # Check if target exists
    if target.exists():
        print(f"\n⚠️  Target already exists!")
        print(f"   Size: {target.stat().st_size:,} bytes")
        print(f"\n❌ Aborting to prevent overwrite")
        return False

    # Ensure target directory exists
    target.parent.mkdir(parents=True, exist_ok=True)

    # Read source
    try:
        content = source.read_text(encoding='utf-8')
    except Exception as e:
        print(f"\n❌ Error reading source: {e}")
        return False

    # Update content
    updated_content = update_header(content)

    # Write to target
    try:
        target.write_text(updated_content, encoding='utf-8')
        print(f"\n✅ File created: {target}")
    except Exception as e:
        print(f"\n❌ Error writing target: {e}")
        return False

    # Delete source
    try:
        source.unlink()
        print(f"✅ Source deleted: {source}")
    except Exception as e:
        print(f"\n❌ Error deleting source: {e}")
        return False

    print(f"\n📊 Summary:")
    print(f"   - Price lists, discount system")
    print(f"   - Business logic & query examples")
    print(f"   - Progress: 1/10 tables (10%)")

    return True


if __name__ == "__main__":
    success = main()
    print("\n" + "=" * 70)
    if success:
        print("✅ Migration complete - Sales index relocated")
        print("\nNext steps:")
        print("1. Update docs/database/00_DATABASE_INDEX.md")
        print("2. Update docs.json manifest")
        print("3. Continue with stock/INDEX.md-old")
    else:
        print("❌ Migration failed")
    print("=" * 70)