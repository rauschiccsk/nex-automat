#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create Documentation Structure - NEX Automat
Location: C:/Development/nex-automat/scripts/01-create-documentation-structure.py

Vytvorí systematickú hierarchickú štruktúru dokumentácie a premenuje existujúce .md súbory.
"""

from pathlib import Path
from datetime import datetime

# Konfigurácia
MONOREPO_ROOT = Path("C:/Development/nex-automat")
DOCS_ROOT = MONOREPO_ROOT / "docs"
SESSION_NOTES = MONOREPO_ROOT / "SESSION_NOTES"

# Súbory ktoré sa NEPREMENÚVAJÚ na .md-old
EXCLUDED_FILES = {
    "INIT_PROMPT_NEW_CHAT.md",
    "SESSION_NOTES.md"
}

# Dokumentačná štruktúra
DOCUMENTATION_STRUCTURE = {
    "strategic": [
        "PROJECT_ROADMAP.md",
        "TECHNOLOGY_DECISIONS.md"
    ],
    "system": [
        "GUI_FRAMEWORK.md",
        "CONFIGURATION.md",
        "CODING_STANDARDS.md"
    ],
    "database": {
        "__files__": ["DATABASE_INDEX.md"],
        "catalogs": [],
        "documents": [],
        "migrations": []
    },
    "documents": [
        "DOCUMENT_TYPES.md",
        "NUMBERING.md",
        "WORKFLOWS.md"
    ],
    "applications": [
        "APPLICATIONS_INDEX.md"
    ],
    "archive": {
        "__files__": ["ARCHIVE_INDEX.md"],
        "sessions": []
    }
}


def create_markdown_header(title: str, description: str = "") -> str:
    """Vytvorí základnú hlavičku pre markdown súbor"""
    header = f"""# {title}

**Vytvorené:** {datetime.now().strftime('%Y-%m-%d')}  
**Status:** 🚧 V príprave  
**Verzia:** 1.0

---

"""
    if description:
        header += f"{description}\n\n---\n\n"

    header += "## Obsah\n\n"
    header += "TODO: Doplniť obsah\n"

    return header


def create_directory_structure(base_path: Path, structure: dict | list, parent_name: str = ""):
    """Rekurzívne vytvorí adresárovú štruktúru a súbory"""

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
                            create_markdown_header(title),
                            encoding='utf-8'
                        )
                        print(f"   ✅ Vytvorený: {file_path.relative_to(MONOREPO_ROOT)}")
            else:
                # Vytvor podadresár
                dir_path = base_path / dir_name
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"   📁 Adresár: {dir_path.relative_to(MONOREPO_ROOT)}")

                # Rekurzia do podadresára
                create_directory_structure(dir_path, content, dir_name)

    elif isinstance(structure, list):
        # List = súbory v aktuálnom adresári
        for filename in structure:
            file_path = base_path / filename
            if not file_path.exists():
                title = filename.replace(".md", "").replace("_", " ")
                file_path.write_text(
                    create_markdown_header(title),
                    encoding='utf-8'
                )
                print(f"   ✅ Vytvorený: {file_path.relative_to(MONOREPO_ROOT)}")


def rename_existing_md_files():
    """Premenuje všetky existujúce .md súbory na .md-old (okrem vylúčených)"""
    print("\n2️⃣ Premenovanie existujúcich .md súborov...")
    print("=" * 70)

    renamed_count = 0
    skipped_count = 0

    # Prejdi celý projekt
    for md_file in MONOREPO_ROOT.rglob("*.md"):
        # Preskočiť vylúčené súbory
        if md_file.name in EXCLUDED_FILES:
            print(f"   ⏭️  Preskočené: {md_file.relative_to(MONOREPO_ROOT)}")
            skipped_count += 1
            continue

        # Preskočiť ak už existuje .md-old
        old_file = md_file.with_suffix('.md-old')
        if old_file.exists():
            print(f"   ⚠️  Už existuje: {old_file.relative_to(MONOREPO_ROOT)}")
            continue

        # Preskočiť novovytvorené súbory v docs/
        if md_file.is_relative_to(DOCS_ROOT):
            created_recently = (datetime.now() - datetime.fromtimestamp(md_file.stat().st_mtime)).seconds < 60
            if created_recently:
                print(f"   ⏭️  Nový súbor: {md_file.relative_to(MONOREPO_ROOT)}")
                skipped_count += 1
                continue

        # Premenuj
        md_file.rename(old_file)
        print(f"   ✅ Premenované: {md_file.relative_to(MONOREPO_ROOT)} → {old_file.name}")
        renamed_count += 1

    print()
    print(f"   Premenovaných: {renamed_count}")
    print(f"   Preskočených: {skipped_count}")


def create_main_index():
    """Vytvorí hlavný DOCUMENTATION_INDEX.md"""
    index_path = DOCS_ROOT / "DOCUMENTATION_INDEX.md"

    content = """# Dokumentácia NEX Automat - Hlavný Index

**Vytvorené:** {date}  
**Status:** 🚧 V príprave  
**Verzia:** 1.0

---

## Účel Tejto Dokumentácie

Tento dokument slúži ako hlavný vstupný bod do komplexnej dokumentácie projektu NEX Automat. 
Dokumentácia je organizovaná hierarchicky pre jednoduchú navigáciu a efektívne využitie tokenov.

---

## Štruktúra Dokumentácie

### 📋 1. Strategické Plánovanie
**Umiestnenie:** `docs/strategic/`

- [PROJECT_ROADMAP.md](strategic/PROJECT_ROADMAP.md) - Plány a milestones projektu
- [TECHNOLOGY_DECISIONS.md](strategic/TECHNOLOGY_DECISIONS.md) - Technologické rozhodnutia a ich odôvodnenie

**Účel:** Dlhodobé plány, strategické rozhodnutia, roadmap

---

### ⚙️ 2. Systémová Dokumentácia
**Umiestnenie:** `docs/system/`

- [GUI_FRAMEWORK.md](system/GUI_FRAMEWORK.md) - PySide6 štandardy a guidelines
- [CONFIGURATION.md](system/CONFIGURATION.md) - Konfiguračný systém
- [CODING_STANDARDS.md](system/CODING_STANDARDS.md) - Code style a best practices

**Účel:** Všeobecné systémové nastavenia, štandardy, frameworks

---

### 🗄️ 3. Databázová Dokumentácia
**Umiestnenie:** `docs/database/`

- [DATABASE_INDEX.md](database/DATABASE_INDEX.md) - Index všetkých DB dokumentov
- **Katalógy:** `database/catalogs/` - GSCAT, PAB, BARCODE, atď.
- **Doklady:** `database/documents/` - DDLIST, INVOICE, STOCK, atď.
- **Migrácie:** `database/migrations/` - Migration dokumenty

**Účel:** Databázové schémy, mappingy NEX Genesis → NEX Automat

---

### 📄 4. Dokumentácia Dokladov
**Umiestnenie:** `docs/documents/`

- [DOCUMENT_TYPES.md](documents/DOCUMENT_TYPES.md) - Typy dokladov v NEX Genesis
- [NUMBERING.md](documents/NUMBERING.md) - Systém číslovania dokladov
- [WORKFLOWS.md](documents/WORKFLOWS.md) - Business workflows

**Účel:** Všeobecné informácie o dokladoch, číslovaní, procesoch

---

### 💻 5. Aplikácie (Programové Moduly)
**Umiestnenie:** `docs/applications/`

- [APPLICATIONS_INDEX.md](applications/APPLICATIONS_INDEX.md) - Index všetkých modulov
- **Jednotlivé moduly:** `applications/{{module-name}}/`
  - supplier-invoice-loader
  - supplier-invoice-staging
  - supplier-invoice-editor (deprecated)

**Účel:** Detailná dokumentácia jednotlivých aplikácií

---

### 📦 6. Archív Session
**Umiestnenie:** `docs/archive/`

- [ARCHIVE_INDEX.md](archive/ARCHIVE_INDEX.md) - Zoznam všetkých sessions
- **Sessions:** `archive/sessions/` - Detailné záznamy jednotlivých sessions

**Účel:** História vývoja projektu, dokumentácia sessions

---

### 📝 7. Session Notes
**Umiestnenie:** `SESSION_NOTES/`

- `SESSION_NOTES.md` - Aktuálne poznámky k session
- `INIT_PROMPT_NEW_CHAT.md` - Init prompt pre nový chat

**Účel:** Live dokumentácia aktuálnej práce

---

## Zásady Používania Dokumentácie

### Token Efektivita
- Vždy načítať len relevantné dokumenty
- Použiť indexy na rýchle vyhľadanie
- Neloadovať celé sekcie zbytočne

### Aktualizácia Dokumentácie
- Pri každej zmene aktualizovať príslušný dokument
- Udržiavať odkazy aktuálne
- Dokumentovať rozhodnutia v TECHNOLOGY_DECISIONS.md

### Referencovanie
- Vždy odkazovať na existujúce dokumenty
- Neduplicovať informácie
- Používať relatívne cesty

---

## Rýchle Odkazy

### Pre Development
- [GUI Framework](system/GUI_FRAMEWORK.md) - PySide6
- [Coding Standards](system/CODING_STANDARDS.md)
- [Database Index](database/DATABASE_INDEX.md)

### Pre Planning
- [Project Roadmap](strategic/PROJECT_ROADMAP.md)
- [Applications Index](applications/APPLICATIONS_INDEX.md)

### Pre Session Work
- [Session Notes](../SESSION_NOTES/SESSION_NOTES.md)
- [Archive Index](archive/ARCHIVE_INDEX.md)

---

**Verzia:** 1.0  
**Vytvoril:** Zoltán & Claude  
**Dátum:** {date}
""".format(date=datetime.now().strftime('%Y-%m-%d'))

    index_path.write_text(content, encoding='utf-8')
    print(f"   ✅ Vytvorený: {index_path.relative_to(MONOREPO_ROOT)}")


def main():
    """Hlavná funkcia scriptu"""
    print("=" * 70)
    print("📋 VYTVORENIE DOKUMENTAČNEJ ŠTRUKTÚRY - NEX AUTOMAT")
    print("=" * 70)
    print()
    print(f"Monorepo: {MONOREPO_ROOT}")
    print(f"Docs:     {DOCS_ROOT}")
    print()

    # 1. Vytvor adresárovú štruktúru
    print("1️⃣ Vytváranie adresárovej štruktúry a súborov...")
    print("=" * 70)

    # Vytvor docs root
    DOCS_ROOT.mkdir(parents=True, exist_ok=True)
    print(f"   📁 Hlavný adresár: {DOCS_ROOT.relative_to(MONOREPO_ROOT)}")
    print()

    # Vytvor hierarchickú štruktúru
    create_directory_structure(DOCS_ROOT, DOCUMENTATION_STRUCTURE)
    print()

    # Vytvor hlavný index
    create_main_index()
    print()

    # 2. Premenuj existujúce .md súbory
    rename_existing_md_files()
    print()

    # 3. Sumár
    print("=" * 70)
    print("✅ DOKUMENTAČNÁ ŠTRUKTÚRA VYTVORENÁ!")
    print("=" * 70)
    print()
    print("📊 Vytvoreň štruktúra:")
    print()
    print("docs/")
    print("├── DOCUMENTATION_INDEX.md          # Hlavný index")
    print("├── strategic/                      # Strategické plánovanie")
    print("│   ├── PROJECT_ROADMAP.md")
    print("│   └── TECHNOLOGY_DECISIONS.md")
    print("├── system/                         # Systémová dokumentácia")
    print("│   ├── GUI_FRAMEWORK.md")
    print("│   ├── CONFIGURATION.md")
    print("│   └── CODING_STANDARDS.md")
    print("├── database/                       # Databázová dokumentácia")
    print("│   ├── DATABASE_INDEX.md")
    print("│   ├── catalogs/")
    print("│   ├── documents/")
    print("│   └── migrations/")
    print("├── documents/                      # Dokumentácia dokladov")
    print("│   ├── DOCUMENT_TYPES.md")
    print("│   ├── NUMBERING.md")
    print("│   └── WORKFLOWS.md")
    print("├── applications/                   # Aplikácie")
    print("│   └── APPLICATIONS_INDEX.md")
    print("└── archive/                        # Archív")
    print("    ├── ARCHIVE_INDEX.md")
    print("    └── sessions/")
    print()
    print("🔄 Ďalší krok:")
    print("   Postupne migrovať existujúcu dokumentáciu z .md-old súborov")
    print("   do novovytvorenej štruktúry.")
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()