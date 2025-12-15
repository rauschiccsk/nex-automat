#!/usr/bin/env python3
"""
Script 22: Split COMMON_DOCUMENT_PRINCIPLES.md-old

Splits into 3 documents:
1. docs/documents/DOCUMENT_TYPES.md (Section 0)
2. docs/documents/NUMBERING.md (Sections 1, 3, 4, 5)
3. docs/database/DATABASE_PRINCIPLES.md (Sections 2, 6, 7, 8, 9, 10)
"""

from pathlib import Path

# Paths
REPO_ROOT = Path(r"C:\Development\nex-automat")
SOURCE = REPO_ROOT / "docs/architecture/database/COMMON_DOCUMENT_PRINCIPLES.md-old"

# Target files
DOC_TYPES = REPO_ROOT / "docs/documents/DOCUMENT_TYPES.md"
DOC_NUMBERING = REPO_ROOT / "docs/documents/NUMBERING.md"
DB_PRINCIPLES = REPO_ROOT / "docs/database/DATABASE_PRINCIPLES.md"


def read_source():
    """Read source file"""
    with open(SOURCE, 'r', encoding='utf-8') as f:
        return f.read()


def extract_section(content, section_num):
    """Extract section by number"""
    # Find section start
    section_marker = f"## {section_num}."
    start_idx = content.find(section_marker)
    if start_idx == -1:
        return ""

    # Find next section or end
    next_section = section_num + 1
    next_marker = f"## {next_section}."
    end_idx = content.find(next_marker, start_idx + 1)

    if end_idx == -1:
        # Last section - find "---" before final notes
        end_idx = content.find("\n## 11. ZÁVER", start_idx + 1)
        if end_idx == -1:
            end_idx = len(content)

    return content[start_idx:end_idx].strip()


def create_document_types(content):
    """Create DOCUMENT_TYPES.md"""
    header = """# Document Types

**Category:** Documents  
**Status:** 🟢 Complete  
**Created:** 2024-12-12  
**Updated:** 2025-12-15  
**Source:** COMMON_DOCUMENT_PRINCIPLES.md

---

## Overview

NEX Automat supports **22 document types**, each with unique two-letter code and English name.

---

"""

    section_0 = extract_section(content, 0)

    footer = """

---

**See Also:**
- [NUMBERING.md](NUMBERING.md) - Document numbering system
- [WORKFLOWS.md](WORKFLOWS.md) - Document workflows
"""

    return header + section_0 + footer


def create_numbering(content):
    """Create NUMBERING.md"""
    header = """# Document Numbering

**Category:** Documents  
**Status:** 🟢 Complete  
**Created:** 2024-12-12  
**Updated:** 2025-12-15  
**Source:** COMMON_DOCUMENT_PRINCIPLES.md

---

## Overview

Document numbering system with three number types:
- System number (document_number)
- Global sequence (global_sequence)  
- Book sequence (book_sequence)

---

"""

    section_1 = extract_section(content, 1)
    section_3 = extract_section(content, 3)
    section_4 = extract_section(content, 4)
    section_5 = extract_section(content, 5)

    footer = """

---

**See Also:**
- [DOCUMENT_TYPES.md](DOCUMENT_TYPES.md) - Document types
- [../database/DATABASE_PRINCIPLES.md](../database/DATABASE_PRINCIPLES.md) - Database design
"""

    return header + section_1 + "\n\n---\n\n" + section_3 + "\n\n---\n\n" + section_4 + "\n\n---\n\n" + section_5 + footer


def create_database_principles(content):
    """Create DATABASE_PRINCIPLES.md"""
    header = """# Database Design Principles

**Category:** Database  
**Status:** 🟢 Complete  
**Created:** 2024-12-12  
**Updated:** 2025-12-15  
**Source:** COMMON_DOCUMENT_PRINCIPLES.md

---

## Overview

Common database design principles for NEX Automat:
- Versioning system for catalogs
- Universal document texts table
- Audit fields and triggers
- Naming conventions
- Migration rules
- Validation rules

---

"""

    section_2 = extract_section(content, 2)
    section_6 = extract_section(content, 6)
    section_7 = extract_section(content, 7)
    section_8 = extract_section(content, 8)
    section_9 = extract_section(content, 9)
    section_10 = extract_section(content, 10)

    footer = """

---

**See Also:**
- [00_DATABASE_INDEX.md](00_DATABASE_INDEX.md) - Database documentation index
- [../documents/NUMBERING.md](../documents/NUMBERING.md) - Document numbering
"""

    sections = [section_2, section_6, section_7, section_8, section_9, section_10]
    body = "\n\n---\n\n".join(s for s in sections if s)

    return header + body + footer


def main():
    print("=" * 80)
    print("Script 22: Split COMMON_DOCUMENT_PRINCIPLES.md-old")
    print("=" * 80)

    if not SOURCE.exists():
        print(f"\n❌ ERROR: Source not found: {SOURCE}")
        return False

    print(f"\n✅ Source: {SOURCE.name} ({SOURCE.stat().st_size:,} bytes)")

    # Read source
    print("\n" + "=" * 80)
    print("Step 1: Reading source file")
    print("=" * 80)

    content = read_source()
    print(f"✅ Loaded {len(content):,} characters")

    # Create target documents
    print("\n" + "=" * 80)
    print("Step 2: Creating split documents")
    print("=" * 80)

    # 1. DOCUMENT_TYPES.md
    doc_types_content = create_document_types(content)
    DOC_TYPES.parent.mkdir(parents=True, exist_ok=True)
    with open(DOC_TYPES, 'w', encoding='utf-8') as f:
        f.write(doc_types_content)
    print(f"✅ Created: {DOC_TYPES.relative_to(REPO_ROOT)}")
    print(f"   Section 0: Document Types (22 types)")
    print(f"   Size: {len(doc_types_content):,} chars")

    # 2. NUMBERING.md
    numbering_content = create_numbering(content)
    DOC_NUMBERING.parent.mkdir(parents=True, exist_ok=True)
    with open(DOC_NUMBERING, 'w', encoding='utf-8') as f:
        f.write(numbering_content)
    print(f"\n✅ Created: {DOC_NUMBERING.relative_to(REPO_ROOT)}")
    print(f"   Sections 1, 3, 4, 5: Numbering, Books, Lifecycle, AC/FC")
    print(f"   Size: {len(numbering_content):,} chars")

    # 3. DATABASE_PRINCIPLES.md
    db_principles_content = create_database_principles(content)
    DB_PRINCIPLES.parent.mkdir(parents=True, exist_ok=True)
    with open(DB_PRINCIPLES, 'w', encoding='utf-8') as f:
        f.write(db_principles_content)
    print(f"\n✅ Created: {DB_PRINCIPLES.relative_to(REPO_ROOT)}")
    print(f"   Sections 2, 6, 7, 8, 9, 10: Versioning, Texts, Audit, Naming, Migration, Validation")
    print(f"   Size: {len(db_principles_content):,} chars")

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

    print("\n✅ Split into 3 documents:")
    print(f"   1. docs/documents/DOCUMENT_TYPES.md")
    print(f"   2. docs/documents/NUMBERING.md")
    print(f"   3. docs/database/DATABASE_PRINCIPLES.md")

    print(f"\n✅ Deleted: docs/architecture/database/COMMON_DOCUMENT_PRINCIPLES.md-old")

    print("\n📋 Update indexes:")
    print("   - docs/documents/00_DOCUMENTS_INDEX.md")
    print("   - docs/database/00_DATABASE_INDEX.md")

    print("\n✅ Script completed")
    print("=" * 80)

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)