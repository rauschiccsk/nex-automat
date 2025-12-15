#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update Documentation Structure - NEX Automat
Location: C:/Development/nex-automat/scripts/02-update-documentation-structure.py

Aktualizuje dokumentačnú štruktúru - pridáva nové adresáre a súbory,
zachováva existujúce dokumenty.
"""

from pathlib import Path
from datetime import datetime

# Konfigurácia
MONOREPO_ROOT = Path("C:/Development/nex-automat")
DOCS_ROOT = MONOREPO_ROOT / "docs"

# Definitívna dokumentačná štruktúra
DOCUMENTATION_STRUCTURE = {
    "strategic": [
        "00_STRATEGIC_INDEX.md",
        "PROJECT_ROADMAP.md",
        "TECHNOLOGY_DECISIONS.md"
    ],
    "system": [
        "00_SYSTEM_INDEX.md",
        "ARCHITECTURE.md",
        "MONOREPO_STRUCTURE.md",
        "GUI_FRAMEWORK.md",
        "CONFIGURATION.md",
        "CODING_STANDARDS.md"
    ],
    "database": {
        "__files__": ["00_DATABASE_INDEX.md"],
        "catalogs": [],
        "documents": [],
        "migrations": []
    },
    "documents": [
        "00_DOCUMENTS_INDEX.md",
        "DOCUMENT_TYPES.md",
        "NUMBERING.md",
        "WORKFLOWS.md"
    ],
    "applications": {
        "__files__": ["00_APPLICATIONS_INDEX.md"],
        "supplier-invoice-loader": [
            "00_LOADER_INDEX.md",
            "API_SPECIFICATION.md",
            "WORKFLOWS.md",
            "CONFIGURATION.md"
        ],
        "supplier-invoice-staging": [
            "00_STAGING_INDEX.md",
            "DATABASE_SCHEMA.md",
            "GUI_STRUCTURE.md",
            "WORKFLOWS.md",
            "NEX_INTEGRATION.md",
            "CONFIGURATION.md"
        ]
    },
    "packages": {
        "__files__": ["00_PACKAGES_INDEX.md"],
        "nex-shared": [
            "00_NEX_SHARED_INDEX.md",
            "BASE_WINDOW.md",
            "BASE_GRID.md",
            "UTILITIES.md"
        ],
        "nexdata": [
            "00_NEXDATA_INDEX.md",
            "BTRIEVE_ACCESS.md",
            "DATA_MODELS.md"
        ]
    },
    "development": [
        "00_DEVELOPMENT_INDEX.md",
        "SETUP_GUIDE.md",
        "TESTING_STRATEGY.md",
        "DEPLOYMENT.md"
    ],
    "migration": [
        "00_MIGRATION_INDEX.md",
        "PYSIDE6_MIGRATION.md",
        "DATABASE_MIGRATION.md"
    ],
    "reference": [
        "00_REFERENCE_INDEX.md",
        "GLOSSARY.md",
        "API_REFERENCE.md"
    ],
    "archive": {
        "__files__": ["00_ARCHIVE_INDEX.md"],
        "sessions": []
    }
}


def create_markdown_header(title: str, category: str = "", description: str = "") -> str:
    """Vytvorí štandardnú hlavičku pre markdown súbor"""

    # Determínuj status
    if title.startswith("00_") or title.endswith("INDEX"):
        status = "🟢 Complete"
    else:
        status = "🔴 Draft"

    header = f"""# {title.replace('_', ' ').replace('.md', '')}

**Kategória:** {category if category else 'TODO'}  
**Status:** {status}  
**Vytvorené:** {datetime.now().strftime('%Y-%m-%d')}  
**Aktualizované:** {datetime.now().strftime('%Y-%m-%d')}

---

## Obsah

TODO: Doplniť obsah dokumentu

---

"""

    if description:
        header += f"{description}\n\n---\n\n"

    return header


def create_directory_structure(base_path: Path, structure: dict | list, category: str = ""):
    """Rekurzívne vytvorí adresárovú štruktúru a súbory"""

    created_files = []
    created_dirs = []
    skipped_files = []

    if isinstance(structure, dict):
        # Dictionary = adresár s podadresármi/súbormi
        for dir_name, content in structure.items():
            if dir_name == "__files__":
                # Špeciálny kľúč pre súbory v aktuálnom adresári
                for filename in content:
                    file_path = base_path / filename
                    if not file_path.exists():
                        title = filename.replace(".md", "").replace("_", " ")
                        file_path.write_text(
                            create_markdown_header(title, category),
                            encoding='utf-8'
                        )
                        created_files.append(file_path)
                    else:
                        skipped_files.append(file_path)
            else:
                # Vytvor podadresár
                dir_path = base_path / dir_name
                if not dir_path.exists():
                    dir_path.mkdir(parents=True, exist_ok=True)
                    created_dirs.append(dir_path)

                # Rekurzia do podadresára
                sub_created_files, sub_created_dirs, sub_skipped = create_directory_structure(
                    dir_path, content, category or dir_name
                )
                created_files.extend(sub_created_files)
                created_dirs.extend(sub_created_dirs)
                skipped_files.extend(sub_skipped)

    elif isinstance(structure, list):
        # List = súbory v aktuálnom adresári
        for filename in structure:
            file_path = base_path / filename
            if not file_path.exists():
                title = filename.replace(".md", "").replace("_", " ")
                file_path.write_text(
                    create_markdown_header(title, category),
                    encoding='utf-8'
                )
                created_files.append(file_path)
            else:
                skipped_files.append(file_path)

    return created_files, created_dirs, skipped_files


def create_main_index():
    """Vytvorí/aktualizuje hlavný 00_DOCUMENTATION_INDEX.md"""
    index_path = DOCS_ROOT / "00_DOCUMENTATION_INDEX.md"

    content = f"""# Dokumentácia NEX Automat - Hlavný Index

**Vytvorené:** {datetime.now().strftime('%Y-%m-%d')}  
**Status:** 🟢 Complete  
**Verzia:** 2.0 FINAL

---

## 🎯 Účel Tejto Dokumentácie

Tento dokument slúži ako hlavný vstupný bod do komplexnej dokumentácie projektu NEX Automat. 
Dokumentácia je organizovaná hierarchicky pre jednoduchú navigáciu, efektívne využitie tokenov 
a prípravu na RAG (Retrieval-Augmented Generation) systém.

---

## 📁 Štruktúra Dokumentácie

### 🎯 1. Strategické Plánovanie
**Umiestnenie:** [`strategic/`](strategic/00_STRATEGIC_INDEX.md)

Dlhodobé plány, strategické rozhodnutia, roadmap projektu.

- [Strategic Index](strategic/00_STRATEGIC_INDEX.md)
- [Project Roadmap](strategic/PROJECT_ROADMAP.md)
- [Technology Decisions](strategic/TECHNOLOGY_DECISIONS.md)

---

### ⚙️ 2. Systémová Dokumentácia
**Umiestnenie:** [`system/`](system/00_SYSTEM_INDEX.md)

High-level architektúra, monorepo štruktúra, všeobecné systémové nastavenia.

- [System Index](system/00_SYSTEM_INDEX.md)
- [Architecture](system/ARCHITECTURE.md)
- [Monorepo Structure](system/MONOREPO_STRUCTURE.md)
- [GUI Framework](system/GUI_FRAMEWORK.md)
- [Configuration](system/CONFIGURATION.md)
- [Coding Standards](system/CODING_STANDARDS.md)

---

### 🗄️ 3. Databázová Dokumentácia
**Umiestnenie:** [`database/`](database/00_DATABASE_INDEX.md)

Databázové schémy, mappingy NEX Genesis → NEX Automat, migrations.

- [Database Index](database/00_DATABASE_INDEX.md)
- **Katalógy:** [`catalogs/`](database/catalogs/) - GSCAT, PAB, BARCODE
- **Doklady:** [`documents/`](database/documents/) - DDLIST, INVOICE, STOCK
- **Migrácie:** [`migrations/`](database/migrations/) - Migration dokumenty

---

### 📄 4. Dokumentácia Dokladov
**Umiestnenie:** [`documents/`](documents/00_DOCUMENTS_INDEX.md)

Všeobecné informácie o dokladoch, číslovanie, business workflows.

- [Documents Index](documents/00_DOCUMENTS_INDEX.md)
- [Document Types](documents/DOCUMENT_TYPES.md)
- [Numbering](documents/NUMBERING.md)
- [Workflows](documents/WORKFLOWS.md)

---

### 💻 5. Aplikácie
**Umiestnenie:** [`applications/`](applications/00_APPLICATIONS_INDEX.md)

Detailná dokumentácia jednotlivých programových modulov.

- [Applications Index](applications/00_APPLICATIONS_INDEX.md)
- **supplier-invoice-loader** - FastAPI backend (port 8001)
  - [Loader Index](applications/supplier-invoice-loader/00_LOADER_INDEX.md)
  - [API Specification](applications/supplier-invoice-loader/API_SPECIFICATION.md)
  - [Workflows](applications/supplier-invoice-loader/WORKFLOWS.md)
  - [Configuration](applications/supplier-invoice-loader/CONFIGURATION.md)
- **supplier-invoice-staging** - PySide6 GUI frontend
  - [Staging Index](applications/supplier-invoice-staging/00_STAGING_INDEX.md)
  - [Database Schema](applications/supplier-invoice-staging/DATABASE_SCHEMA.md)
  - [GUI Structure](applications/supplier-invoice-staging/GUI_STRUCTURE.md)
  - [Workflows](applications/supplier-invoice-staging/WORKFLOWS.md)
  - [NEX Integration](applications/supplier-invoice-staging/NEX_INTEGRATION.md)
  - [Configuration](applications/supplier-invoice-staging/CONFIGURATION.md)

---

### 📦 6. Shared Packages
**Umiestnenie:** [`packages/`](packages/00_PACKAGES_INDEX.md)

Dokumentácia zdieľaných Python balíkov (nex-shared, nexdata).

- [Packages Index](packages/00_PACKAGES_INDEX.md)
- **nex-shared** - GUI komponenty, utilities
  - [nex-shared Index](packages/nex-shared/00_NEX_SHARED_INDEX.md)
  - [Base Window](packages/nex-shared/BASE_WINDOW.md)
  - [Base Grid](packages/nex-shared/BASE_GRID.md)
  - [Utilities](packages/nex-shared/UTILITIES.md)
- **nexdata** - NEX Genesis data access
  - [nexdata Index](packages/nexdata/00_NEXDATA_INDEX.md)
  - [Btrieve Access](packages/nexdata/BTRIEVE_ACCESS.md)
  - [Data Models](packages/nexdata/DATA_MODELS.md)

---

### 🛠️ 7. Development
**Umiestnenie:** [`development/`](development/00_DEVELOPMENT_INDEX.md)

Setup guides, testing stratégie, deployment procesy.

- [Development Index](development/00_DEVELOPMENT_INDEX.md)
- [Setup Guide](development/SETUP_GUIDE.md)
- [Testing Strategy](development/TESTING_STRATEGY.md)
- [Deployment](development/DEPLOYMENT.md)

---

### 🔄 8. Migration
**Umiestnenie:** [`migration/`](migration/00_MIGRATION_INDEX.md)

Migration plány a dokumentácia (PyQt5→PySide6, Btrieve→PostgreSQL).

- [Migration Index](migration/00_MIGRATION_INDEX.md)
- [PySide6 Migration](migration/PYSIDE6_MIGRATION.md)
- [Database Migration](migration/DATABASE_MIGRATION.md)

---

### 📚 9. Reference
**Umiestnenie:** [`reference/`](reference/00_REFERENCE_INDEX.md)

Glossary, API reference, collaboration rules.

- [Reference Index](reference/00_REFERENCE_INDEX.md)
- [Glossary](reference/GLOSSARY.md)
- [API Reference](reference/API_REFERENCE.md)
- [Collaboration Rules](reference/COLLABORATION_RULES.md)

---

### 📦 10. Archív
**Umiestnenie:** [`archive/`](archive/00_ARCHIVE_INDEX.md)

História vývoja projektu, dokumentácia sessions.

- [Archive Index](archive/00_ARCHIVE_INDEX.md)
- **Sessions:** [`sessions/`](archive/sessions/) - Session history

---

## 🎯 Zásady Používania Dokumentácie

### Token Efektivita
1. **Vždy načítaj index** príslušnej kategórie najprv
2. **Načítaj len relevantné** dokumenty podľa potreby
3. **Neloaduj celé sekcie** zbytočne
4. **Používaj cross-links** na navigáciu medzi dokumentmi

### Aktualizácia Dokumentácie
1. Pri každej zmene **aktualizuj príslušný dokument**
2. **Udržiavaj odkazy** aktuálne
3. **Dokumentuj rozhodnutia** v TECHNOLOGY_DECISIONS.md
4. **Update indexy** pri pridaní/odstránení dokumentov

### Referencovanie
- **Vždy používaj relatívne cesty**
- **Neduplikuj informácie** - link na existujúce
- **Cross-link** súvisiace dokumenty

### RAG Príprava
- Každý dokument = samostatná jednotka pre indexing
- Max 15k tokens per dokument
- Štruktúrovaný obsah s heading hierarchy
- Jasné sekcie a subsekcie

---

## 🚀 Quick Start Links

### Pre Development
- [System Architecture](system/ARCHITECTURE.md)
- [GUI Framework (PySide6)](system/GUI_FRAMEWORK.md)
- [Coding Standards](system/CODING_STANDARDS.md)
- [Setup Guide](development/SETUP_GUIDE.md)

### Pre Database Work
- [Database Index](database/00_DATABASE_INDEX.md)
- [Catalog Structure](database/catalogs/)
- [Document Types](documents/DOCUMENT_TYPES.md)

### Pre Applications
- [Applications Index](applications/00_APPLICATIONS_INDEX.md)
- [Loader (FastAPI)](applications/supplier-invoice-loader/00_LOADER_INDEX.md)
- [Staging (GUI)](applications/supplier-invoice-staging/00_STAGING_INDEX.md)

### Pre Session Work
- [Session Notes](../SESSION_NOTES/SESSION_NOTES.md)
- [Archive Index](archive/00_ARCHIVE_INDEX.md)

---

## 📊 Dokumentačná Štatistika

**Kategórií:** 10  
**Indexov:** 11  
**Tech Dokumentov:** ~32  
**Total Dokumentov:** ~45  
**Estimated Tokens:** ~450k (rozpočítané)

---

**Verzia:** 2.0 FINAL  
**Vytvoril:** Zoltán & Claude  
**Dátum:** {datetime.now().strftime('%Y-%m-%d')}  
**Status:** ✅ Ready for Use
"""

    index_path.write_text(content, encoding='utf-8')
    return index_path


def print_structure_tree():
    """Vypíše stromovú štruktúru dokumentácie"""
    print("📁 Definitívna Štruktúra:")
    print()
    print("docs/")
    print("├── 00_DOCUMENTATION_INDEX.md")
    print("├── strategic/")
    print("│   ├── 00_STRATEGIC_INDEX.md")
    print("│   ├── PROJECT_ROADMAP.md")
    print("│   └── TECHNOLOGY_DECISIONS.md")
    print("├── system/")
    print("│   ├── 00_SYSTEM_INDEX.md")
    print("│   ├── ARCHITECTURE.md")
    print("│   ├── MONOREPO_STRUCTURE.md")
    print("│   ├── GUI_FRAMEWORK.md")
    print("│   ├── CONFIGURATION.md")
    print("│   └── CODING_STANDARDS.md")
    print("├── database/")
    print("│   ├── 00_DATABASE_INDEX.md")
    print("│   ├── catalogs/")
    print("│   ├── documents/")
    print("│   └── migrations/")
    print("├── documents/")
    print("│   ├── 00_DOCUMENTS_INDEX.md")
    print("│   ├── DOCUMENT_TYPES.md")
    print("│   ├── NUMBERING.md")
    print("│   └── WORKFLOWS.md")
    print("├── applications/")
    print("│   ├── 00_APPLICATIONS_INDEX.md")
    print("│   ├── supplier-invoice-loader/")
    print("│   │   ├── 00_LOADER_INDEX.md")
    print("│   │   ├── API_SPECIFICATION.md")
    print("│   │   ├── WORKFLOWS.md")
    print("│   │   └── CONFIGURATION.md")
    print("│   └── supplier-invoice-staging/")
    print("│       ├── 00_STAGING_INDEX.md")
    print("│       ├── DATABASE_SCHEMA.md")
    print("│       ├── GUI_STRUCTURE.md")
    print("│       ├── WORKFLOWS.md")
    print("│       ├── NEX_INTEGRATION.md")
    print("│       └── CONFIGURATION.md")
    print("├── packages/")
    print("│   ├── 00_PACKAGES_INDEX.md")
    print("│   ├── nex-shared/")
    print("│   │   ├── 00_NEX_SHARED_INDEX.md")
    print("│   │   ├── BASE_WINDOW.md")
    print("│   │   ├── BASE_GRID.md")
    print("│   │   └── UTILITIES.md")
    print("│   └── nexdata/")
    print("│       ├── 00_NEXDATA_INDEX.md")
    print("│       ├── BTRIEVE_ACCESS.md")
    print("│       └── DATA_MODELS.md")
    print("├── development/")
    print("│   ├── 00_DEVELOPMENT_INDEX.md")
    print("│   ├── SETUP_GUIDE.md")
    print("│   ├── TESTING_STRATEGY.md")
    print("│   └── DEPLOYMENT.md")
    print("├── migration/")
    print("│   ├── 00_MIGRATION_INDEX.md")
    print("│   ├── PYSIDE6_MIGRATION.md")
    print("│   └── DATABASE_MIGRATION.md")
    print("├── reference/")
    print("│   ├── 00_REFERENCE_INDEX.md")
    print("│   ├── GLOSSARY.md")
    print("│   └── API_REFERENCE.md")
    print("└── archive/")
    print("    ├── 00_ARCHIVE_INDEX.md")
    print("    └── sessions/")


def main():
    """Hlavná funkcia scriptu"""
    print("=" * 80)
    print("📋 AKTUALIZÁCIA DOKUMENTAČNEJ ŠTRUKTÚRY - NEX AUTOMAT v2.0 FINAL")
    print("=" * 80)
    print()
    print(f"Monorepo: {MONOREPO_ROOT}")
    print(f"Docs:     {DOCS_ROOT}")
    print()

    # 1. Vytvor adresárovú štruktúru
    print("1️⃣ Vytváranie/aktualizácia adresárovej štruktúry...")
    print("=" * 80)

    DOCS_ROOT.mkdir(parents=True, exist_ok=True)

    all_created_files = []
    all_created_dirs = []
    all_skipped_files = []

    created_files, created_dirs, skipped_files = create_directory_structure(
        DOCS_ROOT, DOCUMENTATION_STRUCTURE
    )

    all_created_files.extend(created_files)
    all_created_dirs.extend(created_dirs)
    all_skipped_files.extend(skipped_files)

    print()
    print(f"   Vytvorených adresárov: {len(all_created_dirs)}")
    print(f"   Vytvorených súborov: {len(all_created_files)}")
    print(f"   Preskočených (existujú): {len(all_skipped_files)}")
    print()

    # 2. Vytvor/aktualizuj hlavný index
    print("2️⃣ Vytváranie hlavného indexu...")
    print("=" * 80)
    main_index = create_main_index()
    print(f"   ✅ Vytvorený: {main_index.relative_to(MONOREPO_ROOT)}")
    print()

    # 3. Sumár
    print("=" * 80)
    print("✅ DOKUMENTAČNÁ ŠTRUKTÚRA AKTUALIZOVANÁ!")
    print("=" * 80)
    print()

    print_structure_tree()

    print()
    print("📊 Štatistika:")
    print(f"   Nových adresárov: {len(all_created_dirs)}")
    print(f"   Nových súborov: {len(all_created_files)}")
    print(f"   Existujúcich súborov: {len(all_skipped_files)}")
    print()
    print("🔄 Ďalší krok:")
    print("   1. git add docs/")
    print('   2. git commit -m "docs: Create final documentation structure v2.0"')
    print("   3. Systematicky migrovať .md-old súbory do novej štruktúry")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()