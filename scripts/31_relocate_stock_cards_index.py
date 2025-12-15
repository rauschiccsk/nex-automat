#!/usr/bin/env python3
"""
Script 31: Relocate stock/cards/INDEX.md-old → STOCK_CARDS_REFERENCE.md
Reason: Active comprehensive stock cards FIFO system documentation
"""

from pathlib import Path


def update_header(content: str) -> str:
    """Update document header for new location."""

    new_header = """# Stock Cards Reference - Skladové karty a FIFO

**Category:** Database / Stock  
**Status:** 🟢 Complete (3 tables documented)  
**Created:** 2025-12-11  
**Updated:** 2025-12-15  
**Related:** [STOCK_REFERENCE.md](STOCK_REFERENCE.md), [CATALOGS_REFERENCE.md](CATALOGS_REFERENCE.md)

---

"""

    # Find end of original header and replace
    parts = content.split('\n---\n', 1)
    if len(parts) == 2:
        return new_header + parts[1]
    return new_header + content


def main():
    """Relocate stock cards index to database docs."""

    # Paths
    source = Path(r"C:\Development\nex-automat\docs\architecture\database\stock\cards\INDEX.md-old")
    target = Path(r"C:\Development\nex-automat\docs\database\STOCK_CARDS_REFERENCE.md")

    print("=" * 70)
    print("Script 31: Relocate Stock Cards Index")
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
    print(f"   - 3 tables: stock_cards, stock_card_fifos, movements")
    print(f"   - Complete FIFO logic & query patterns")
    print(f"   - Implementation examples")

    return True


if __name__ == "__main__":
    success = main()
    print("\n" + "=" * 70)
    if success:
        print("✅ Migration complete - Stock cards index relocated")
        print("\nNext steps:")
        print("1. Update docs/database/00_DATABASE_INDEX.md")
        print("2. Update STOCK_REFERENCE.md with link")
        print("3. Continue with database table docs")
    else:
        print("❌ Migration failed")
    print("=" * 70)