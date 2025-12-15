#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update All Index Files - NEX Automat
Location: C:/Development/nex-automat/scripts/03-update-all-indexes.py

Aktualizuje všetky 00_*_INDEX.md súbory podľa manifestu.
"""

from pathlib import Path
from datetime import datetime

# Konfigurácia
MONOREPO_ROOT = Path("C:/Development/nex-automat")
DOCS_ROOT = MONOREPO_ROOT / "docs"

# Index obsahy
INDEXES = {
    "strategic/00_STRATEGIC_INDEX.md": """# Strategic Documentation Index

**Kategória:** Strategic  
**Status:** 🟢 Complete  
**Vytvorené:** 2025-12-15  
**Aktualizované:** 2025-12-15

---

## Účel

Strategická dokumentácia obsahuje dlhodobé plány, vízii projektu, technologické rozhodnutia a roadmap.

---

## Dokumenty v Strategic

### Kompletné Dokumenty

**[AI_ML_TECHNOLOGIES.md](AI_ML_TECHNOLOGIES.md)**
- Schválené AI/ML technológie (PaddleOCR, Camelot, Claude API, DuckDB)
- Implementačný plán, náklady, benefity
- Status: 🟢 Complete
- Veľkosť: ~24 KB

**[PROJECT_ROADMAP.md](PROJECT_ROADMAP.md)**
- Kompletný roadmap NEX Automat projektu
- Fázy, milestones, časový harmonogram
- Status: 🟢 Complete
- Veľkosť: ~15 KB, 476 riadkov

**[PROJECT_VISION.md](PROJECT_VISION.md)**
- Vízia a ciele projektu
- Long-term stratégia
- Status: 🟢 Complete
- Veľkosť: ~13 KB, 443 riadkov

### Draft Dokumenty

**[TECHNOLOGY_DECISIONS.md](TECHNOLOGY_DECISIONS.md)**
- História technologických rozhodnutí
- Status: 🔴 Draft
- Potrebuje: Doplniť obsah

---

## Quick Links

**Pre plánovanie:**
- [Project Roadmap](PROJECT_ROADMAP.md) - Časový plán projektu
- [Project Vision](PROJECT_VISION.md) - Dlhodobá vízia

**Pre technológie:**
- [AI/ML Technologies](AI_ML_TECHNOLOGIES.md) - Schválené AI/ML nástroje
- [Technology Decisions](TECHNOLOGY_DECISIONS.md) - História rozhodnutí

---

## Štatistika

- **Total dokumentov:** 4
- **Complete:** 3
- **Draft:** 1
- **Total veľkosť:** ~52 KB

---

**See Also:**
- [Documentation Index](../00_DOCUMENTATION_INDEX.md) - Hlavný index
- [System Architecture](../system/ARCHITECTURE.md) - Technická architektúra
""",

    "system/00_SYSTEM_INDEX.md": """# System Documentation Index

**Kategória:** System  
**Status:** 🟡 In Progress  
**Vytvorené:** 2025-12-15  
**Aktualizované:** 2025-12-15

---

## Účel

Systémová dokumentácia obsahuje high-level architektúru, monorepo štruktúru, všeobecné systémové nastavenia a štandardy.

---

## Dokumenty v System

### Kompletné Dokumenty

**[ARCHITECTURE.md](ARCHITECTURE.md)**
- High-level systémová architektúra NEX Automat
- Komponenty, integration patterns, deployment
- Status: 🟢 Complete
- Veľkosť: ~32 KB, 827 riadkov

**[TERMINOLOGY.md](TERMINOLOGY.md)**
- NEX Genesis a NEX Automat terminológia
- Slovník pojmov, skratky
- Status: 🟢 Complete
- Veľkosť: ~16 KB, 329 riadkov

### Draft Dokumenty

**[MONOREPO_STRUCTURE.md](MONOREPO_STRUCTURE.md)**
- Štruktúra monorepo (apps, packages, tools)
- Status: 🔴 Draft
- Potrebuje: Doplniť detailný popis štruktúry

**[GUI_FRAMEWORK.md](GUI_FRAMEWORK.md)**
- PySide6 štandardy a guidelines
- Status: 🔴 Draft
- Potrebuje: BaseWindow, BaseGrid špecifikácia

**[CONFIGURATION.md](CONFIGURATION.md)**
- Konfiguračný systém (YAML, environment variables)
- Status: 🔴 Draft
- Potrebuje: Config patterns, best practices

**[CODING_STANDARDS.md](CODING_STANDARDS.md)**
- Code style, naming conventions, best practices
- Status: 🔴 Draft
- Potrebuje: Python standards, type hints, testing

---

## Quick Links

**Pre vývoj:**
- [Architecture](ARCHITECTURE.md) - Systémová architektúra
- [Coding Standards](CODING_STANDARDS.md) - Code style guide
- [GUI Framework](GUI_FRAMEWORK.md) - PySide6 guidelines

**Pre štruktúru:**
- [Monorepo Structure](MONOREPO_STRUCTURE.md) - Organizácia projektu
- [Configuration](CONFIGURATION.md) - Config systém

**Pre terminológiu:**
- [Terminology](TERMINOLOGY.md) - Slovník pojmov

---

## Štatistika

- **Total dokumentov:** 6
- **Complete:** 2
- **Draft:** 4
- **Total veľkosť:** ~48 KB

---

**See Also:**
- [Documentation Index](../00_DOCUMENTATION_INDEX.md) - Hlavný index
- [Development Guide](../development/00_DEVELOPMENT_INDEX.md) - Setup a deployment
- [Packages Index](../packages/00_PACKAGES_INDEX.md) - Shared packages
""",

    "database/00_DATABASE_INDEX.md": """# Database Documentation Index

**Kategória:** Database  
**Status:** 🟡 In Progress  
**Vytvorené:** 2025-12-15  
**Aktualizované:** 2025-12-15

---

## Účel

Databázová dokumentácia obsahuje schémy, mappingy NEX Genesis → NEX Automat, migration dokumenty a detailné popisy tabuliek.

---

## Štruktúra

Databázová dokumentácia je rozdelená do kategórií:

### [catalogs/](catalogs/)
Katalógové tabuľky (master data)
- **Produkty:** GSCAT, BARCODE, FGLST, MGLST, SGLST
- **Partneri:** PAB, PABACC, PACNCT, PAGLST, PANOTI, PASUBC
- **Podporné:** BANKLST, PAYLST, TRPLST

**Status:** Obsahuje .md-old súbory na migráciu

### [documents/](documents/)
Dokladové tabuľky (transactional data)
- **Nákup:** TSH, TSI (supplier deliveries)
- **Predaj:** (budúce dokumenty)
- **Účtovníctvo:** ISH, ISI, PAYJRN

**Status:** Obsahuje .md-old súbory na migráciu

### [migrations/](migrations/)
Migration dokumenty
- Btrieve → PostgreSQL migration plány
- Data transformation rules
- Schema evolution

**Status:** Prázdne, pripravené na dokumenty

---

## Dostupné .md-old Súbory na Migráciu

### Katalógy - Produkty (5 súborov)
- `GSCAT-product_catalog.md-old` (20.7 KB)
- `BARCODE-product_catalog_identifiers.md-old` (24.2 KB)
- `FGLST-product_categories.md-old` (16.1 KB)
- `MGLST-product_categories.md-old` (17.4 KB)
- `SGLST-product_categories.md-old` (20.1 KB)

### Katalógy - Partneri (9 súborov)
- `PAB-partner_catalog.md-old` (39.9 KB)
- `PABACC-partner_catalog_bank_accounts.md-old` (12.6 KB)
- `PACNCT-partner_catalog_contacts.md-old` (22.8 KB)
- `PAGLST-partner_categories.md-old` (14.9 KB)
- `PANOTI-partner_catalog_texts.md-old` (15.4 KB)
- `PASUBC-partner_catalog_facilities.md-old` (18.0 KB)
- `BANKLST-bank_catalog.md-old` (10.7 KB)
- `PAYLST-payment_methods.md-old` (8.3 KB)
- `TRPLST-transport_methods.md-old` (8.6 KB)

### Doklady - Stock (7 súborov)
- `STK-stock_cards.md-old` (38.5 KB)
- `STM-stock_card_movements.md-old` (35.6 KB)
- `FIF-stock_card_fifos.md-old` (28.5 KB)
- `STKLST-stocks.md-old` (20.4 KB)
- `WRILST-facilities.md-old` (17.9 KB)
- `TSH-supplier_delivery_heads.md-old` (25.4 KB)
- `TSI-supplier_delivery_items.md-old` (29.7 KB)

### Doklady - Accounting (3 súbory)
- `ISH-supplier_invoice_heads.md-old` (34.8 KB)
- `ISI-supplier_invoice_items.md-old` (29.6 KB)
- `PAYJRN-payment_journal.md-old` (25.8 KB)

### Všeobecné (4 súbory)
- `COMMON_DOCUMENT_PRINCIPLES.md-old` (42.8 KB)
- `DATABASE_RELATIONSHIPS.md-old` (24.1 KB)
- `DATA_DICTIONARY.md-old` (22.7 KB)
- `INDEX.md-old` (6.0 KB)

---

## Migration Strategy

Databázová dokumentácia sa bude migrovať postupne:

1. **Fáza 1:** Všeobecné dokumenty (principles, relationships, dictionary)
2. **Fáza 2:** Katalógy produktov (GSCAT, BARCODE, kategórie)
3. **Fáza 3:** Katalógy partnerov (PAB a súvisiace)
4. **Fáza 4:** Stock dokumenty (STK, STM, doklady)
5. **Fáza 5:** Accounting dokumenty (faktúry, platby)

---

## Quick Links

**Katalógy:**
- [Catalogs Directory](catalogs/) - Master data tabuľky

**Doklady:**
- [Documents Directory](documents/) - Transactional data tabuľky

**Migrácie:**
- [Migrations Directory](migrations/) - Migration plány

---

## Štatistika

- **Kategórie:** 3 (catalogs, documents, migrations)
- **.md-old súborov:** 32
- **Total veľkosť .md-old:** ~540 KB
- **Status:** Pripravené na systematickú migráciu

---

**See Also:**
- [Documentation Index](../00_DOCUMENTATION_INDEX.md) - Hlavný index
- [System Architecture](../system/ARCHITECTURE.md) - Systémová architektúra
- [Migration Index](../migration/00_MIGRATION_INDEX.md) - Migration dokumenty
""",

    "documents/00_DOCUMENTS_INDEX.md": """# Documents Documentation Index

**Kategória:** Documents  
**Status:** 🔴 Draft  
**Vytvorené:** 2025-12-15  
**Aktualizované:** 2025-12-15

---

## Účel

Dokumentácia dokladov obsahuje všeobecné informácie o dokladoch v NEX Genesis, systéme číslovania a business workflows.

---

## Dokumenty v Documents

### Draft Dokumenty

**[DOCUMENT_TYPES.md](DOCUMENT_TYPES.md)**
- Typy dokladov v NEX Genesis (faktúry, dodacie listy, objednávky...)
- Status: 🔴 Draft
- Potrebuje: Kompletný zoznam typov, formáty, štruktúry

**[NUMBERING.md](NUMBERING.md)**
- Systém číslovania dokladov
- Série, prefixes, auto-increment logika
- Status: 🔴 Draft
- Potrebuje: Numbering schema, príklady

**[WORKFLOWS.md](WORKFLOWS.md)**
- Business workflows dokladov (životný cyklus)
- State transitions, approvals
- Status: 🔴 Draft
- Potrebuje: Workflow diagramy, state machines

---

## Súvislosť s Database Documents

Táto sekcia popisuje **všeobecné princípy dokladov**.  
Pre **konkrétne databázové schémy dokladov** pozri:
- [Database Documents](../database/documents/) - Detailné tabuľky dokladov

---

## Quick Links

**Dokumenty:**
- [Document Types](DOCUMENT_TYPES.md) - Typy dokladov
- [Numbering](NUMBERING.md) - Číslovanie dokladov
- [Workflows](WORKFLOWS.md) - Business workflows

**Related:**
- [Database Documents](../database/documents/) - Schémy dokladov
- [System Architecture](../system/ARCHITECTURE.md) - Architektúra

---

## Štatistika

- **Total dokumentov:** 3
- **Complete:** 0
- **Draft:** 3
- **Priority:** Stredná (dopĺňať postupne)

---

**See Also:**
- [Documentation Index](../00_DOCUMENTATION_INDEX.md) - Hlavný index
- [Database Index](../database/00_DATABASE_INDEX.md) - Databázové schémy
""",

    "applications/00_APPLICATIONS_INDEX.md": """# Applications Documentation Index

**Kategória:** Applications  
**Status:** 🟡 In Progress  
**Vytvorené:** 2025-12-15  
**Aktualizované:** 2025-12-15

---

## Účel

Detailná dokumentácia jednotlivých programových modulov (aplikácií) v NEX Automat monorepo.

---

## Aplikácie

### Production Apps

#### [supplier-invoice-loader/](supplier-invoice-loader/)
**FastAPI Backend (Port 8001)**

Dokumenty:
- [Loader Index](supplier-invoice-loader/00_LOADER_INDEX.md) - 🔴 Draft
- [API Specification](supplier-invoice-loader/API_SPECIFICATION.md) - 🔴 Draft
- [Workflows](supplier-invoice-loader/WORKFLOWS.md) - 🔴 Draft
- [Configuration](supplier-invoice-loader/CONFIGURATION.md) - 🔴 Draft

**Popis:** FastAPI service pre spracovanie supplier faktúr (XML parsing, validation, storage)

**Status:** Produkcia (Mágerstav deployment)

---

#### [supplier-invoice-staging/](supplier-invoice-staging/)
**PySide6 GUI Frontend**

Dokumenty:
- [Staging Index](supplier-invoice-staging/00_STAGING_INDEX.md) - 🔴 Draft
- [Database Schema](supplier-invoice-staging/DATABASE_SCHEMA.md) - 🔴 Draft
- [GUI Structure](supplier-invoice-staging/GUI_STRUCTURE.md) - 🔴 Draft
- [Workflows](supplier-invoice-staging/WORKFLOWS.md) - 🔴 Draft
- [NEX Integration](supplier-invoice-staging/NEX_INTEGRATION.md) - 🔴 Draft
- [Configuration](supplier-invoice-staging/CONFIGURATION.md) - 🔴 Draft

**Popis:** PySide6 GUI aplikácia pre manuálnu review a staging faktúr pred importom do NEX Genesis

**Status:** V návrhu (replacement pre supplier-invoice-editor)

---

### Deprecated Apps

**supplier-invoice-editor** (PyQt5) - DEPRECATED
- Nahradené supplier-invoice-staging (PySide6)
- Dokumentácia sa nemigruje

---

## Quick Links

**Loader (Backend):**
- [Loader Index](supplier-invoice-loader/00_LOADER_INDEX.md)
- [API Spec](supplier-invoice-loader/API_SPECIFICATION.md)

**Staging (Frontend):**
- [Staging Index](supplier-invoice-staging/00_STAGING_INDEX.md)
- [GUI Structure](supplier-invoice-staging/GUI_STRUCTURE.md)

---

## Štatistika

- **Production apps:** 2 (loader, staging)
- **Deprecated apps:** 1 (editor)
- **Total dokumentov:** 10 (všetky draft)
- **Priority:** Vysoká (dokumentovať aktívne apps)

---

## Development Priority

1. **supplier-invoice-loader** (VYSOKÁ) - v produkcii, potrebuje docs
2. **supplier-invoice-staging** (VYSOKÁ) - aktívny development
3. supplier-invoice-editor (NÍZKA) - deprecated

---

**See Also:**
- [Documentation Index](../00_DOCUMENTATION_INDEX.md) - Hlavný index
- [Packages Index](../packages/00_PACKAGES_INDEX.md) - Shared packages
- [System Architecture](../system/ARCHITECTURE.md) - Architektúra
""",

    "packages/00_PACKAGES_INDEX.md": """# Packages Documentation Index

**Kategória:** Packages  
**Status:** 🔴 Draft  
**Vytvorené:** 2025-12-15  
**Aktualizované:** 2025-12-15

---

## Účel

Dokumentácia zdieľaných Python balíkov (shared libraries) používaných aplikáciami v monorepo.

---

## Packages

### [nex-shared/](nex-shared/)
**Shared GUI Components & Utilities**

Dokumenty:
- [nex-shared Index](nex-shared/00_NEX_SHARED_INDEX.md) - 🔴 Draft
- [Base Window](nex-shared/BASE_WINDOW.md) - 🔴 Draft
- [Base Grid](nex-shared/BASE_GRID.md) - 🔴 Draft
- [Utilities](nex-shared/UTILITIES.md) - 🔴 Draft

**Popis:**
- BaseWindow - univerzálna window trieda s persistence
- BaseGrid - grid component s quick search, persistence
- Utilities - DB helpers, config loaders, common functions

**Status:** Aktívny (PyQt5), plánovaná migrácia na PySide6

**Štruktúra:** FLAT - `packages/nex-shared/models/` NIE `packages/nex-shared/nex_shared/models/`

---

### [nexdata/](nexdata/)
**NEX Genesis Data Access Layer**

Dokumenty:
- [nexdata Index](nexdata/00_NEXDATA_INDEX.md) - 🔴 Draft
- [Btrieve Access](nexdata/BTRIEVE_ACCESS.md) - 🔴 Draft
- [Data Models](nexdata/DATA_MODELS.md) - 🔴 Draft

**Popis:**
- Btrieve database access (NEX Genesis)
- Data models pre NEX katalógy (GSCAT, PAB, ...)
- Business logic pre data operations

**Status:** Produkcia (stable)

---

## Quick Links

**nex-shared:**
- [nex-shared Index](nex-shared/00_NEX_SHARED_INDEX.md)
- [Base Window](nex-shared/BASE_WINDOW.md) - Window base class
- [Base Grid](nex-shared/BASE_GRID.md) - Grid component

**nexdata:**
- [nexdata Index](nexdata/00_NEXDATA_INDEX.md)
- [Btrieve Access](nexdata/BTRIEVE_ACCESS.md) - NEX Genesis data
- [Data Models](nexdata/DATA_MODELS.md) - Business models

---

## Štatistika

- **Total packages:** 2
- **Total dokumentov:** 7 (všetky draft)
- **Priority:** Vysoká (kritické shared components)

---

## Development Priority

1. **nex-shared** (VYSOKÁ) - používané všetkými GUI apps
2. **nexdata** (VYSOKÁ) - kritický data access layer

---

**See Also:**
- [Documentation Index](../00_DOCUMENTATION_INDEX.md) - Hlavný index
- [Applications Index](../applications/00_APPLICATIONS_INDEX.md) - Apps using packages
- [Migration Index](../migration/00_MIGRATION_INDEX.md) - PySide6 migration
""",

    "development/00_DEVELOPMENT_INDEX.md": """# Development Documentation Index

**Kategória:** Development  
**Status:** 🔴 Draft  
**Vytvorené:** 2025-12-15  
**Aktualizované:** 2025-12-15

---

## Účel

Setup guides, testing stratégie, deployment procesy a development best practices.

---

## Dokumenty v Development

### Draft Dokumenty

**[SETUP_GUIDE.md](SETUP_GUIDE.md)**
- Environment setup (Python, dependencies, databases)
- IDE konfigurácia
- Local development workflow
- Status: 🔴 Draft
- Potrebuje: Step-by-step setup instructions

**[TESTING_STRATEGY.md](TESTING_STRATEGY.md)**
- Testing approach (unit, integration, e2e)
- Test coverage requirements
- Testing tools (pytest, fixtures)
- Status: 🔴 Draft
- Potrebuje: Testing guidelines, examples

**[DEPLOYMENT.md](DEPLOYMENT.md)**
- Deployment proces (Development → Git → Deployment)
- Windows Server setup
- Service management
- Status: 🔴 Draft
- Potrebuje: Deployment procedures, checklists

---

## Deployment .md-old súbory (na migráciu)

V `docs/deployment/` existuje 12 .md-old súborov s deployment dokumentáciou:
- DEPLOYMENT_GUIDE.md-old (13.8 KB)
- GO_LIVE_CHECKLIST.md-old (6.3 KB)
- OPERATIONS_GUIDE.md-old (8.1 KB)
- RECOVERY_GUIDE.md-old (13.6 KB)
- SERVICE_MANAGEMENT.md-old (7.7 KB)
- TROUBLESHOOTING.md-old (9.6 KB)
- a ďalšie...

**Akcia:** Tieto súbory treba systematicky zmigrovať do DEPLOYMENT.md

---

## Quick Links

**Setup:**
- [Setup Guide](SETUP_GUIDE.md) - Environment setup

**Testing:**
- [Testing Strategy](TESTING_STRATEGY.md) - Test approach

**Deployment:**
- [Deployment](DEPLOYMENT.md) - Deployment procedures

---

## Štatistika

- **Total dokumentov:** 3 (všetky draft)
- **.md-old súborov:** 12 (v docs/deployment/)
- **Priority:** Vysoká (kritická pre development)

---

**See Also:**
- [Documentation Index](../00_DOCUMENTATION_INDEX.md) - Hlavný index
- [System Architecture](../system/ARCHITECTURE.md) - Architektúra
- [Applications Index](../applications/00_APPLICATIONS_INDEX.md) - Apps
""",

    "migration/00_MIGRATION_INDEX.md": """# Migration Documentation Index

**Kategória:** Migration  
**Status:** 🔴 Draft  
**Vytvorené:** 2025-12-15  
**Aktualizované:** 2025-12-15

---

## Účel

Migration plány a dokumentácia (PyQt5→PySide6, Btrieve→PostgreSQL).

---

## Dokumenty v Migration

### Draft Dokumenty

**[PYSIDE6_MIGRATION.md](PYSIDE6_MIGRATION.md)**
- Migration plán PyQt5 → PySide6
- BaseWindow, BaseGrid migration
- Breaking changes, compatibility
- Status: 🔴 Draft
- Potrebuje: Detailný migration plan, code examples

**[DATABASE_MIGRATION.md](DATABASE_MIGRATION.md)**
- Migration plán Btrieve → PostgreSQL
- Schema mapping, data transformation
- Migration scripts, testing
- Status: 🔴 Draft
- Potrebuje: Migration strategy, tooling

---

## Related Documentation

**PySide6 Migration súvisí s:**
- [nex-shared package](../packages/nex-shared/00_NEX_SHARED_INDEX.md) - BaseWindow, BaseGrid
- [GUI Framework](../system/GUI_FRAMEWORK.md) - PySide6 standards

**Database Migration súvisí s:**
- [Database Index](../database/00_DATABASE_INDEX.md) - NEX Genesis schema
- [System Architecture](../system/ARCHITECTURE.md) - Database layer

---

## Quick Links

**Migrations:**
- [PySide6 Migration](PYSIDE6_MIGRATION.md) - GUI framework migration
- [Database Migration](DATABASE_MIGRATION.md) - Btrieve → PostgreSQL

---

## Štatistika

- **Total dokumentov:** 2 (všetky draft)
- **Priority:** Vysoká (kritické migrations v progresse)

---

**See Also:**
- [Documentation Index](../00_DOCUMENTATION_INDEX.md) - Hlavný index
- [Packages Index](../packages/00_PACKAGES_INDEX.md) - Packages affected by migration
- [Database Index](../database/00_DATABASE_INDEX.md) - Database schema
""",

    "reference/00_REFERENCE_INDEX.md": """# Reference Documentation Index

**Kategória:** Reference  
**Status:** 🔴 Draft  
**Vytvorené:** 2025-12-15  
**Aktualizované:** 2025-12-15

---

## Účel

Glossary, API reference, collaboration rules a ostatné referenčné materiály.

---

## Dokumenty v Reference

### Draft Dokumenty

**[GLOSSARY.md](GLOSSARY.md)**
- Slovník termínov NEX Genesis a NEX Automat
- Skratky, akronymy
- Status: 🔴 Draft
- Potrebuje: Kompletný glossary
- Note: Čiastočne pokryté v [system/TERMINOLOGY.md](../system/TERMINOLOGY.md)

**[API_REFERENCE.md](API_REFERENCE.md)**
- Quick reference pre API endpoints
- FastAPI routes, parameters
- Status: 🔴 Draft
- Potrebuje: API documentation

---

## Existujúce Referenčné Dokumenty

**COLLABORATION_RULES.md** - V ROOT, treba presunúť sem
- 21 pravidiel spolupráce Claude & Zoltán
- Memory rules, workflow patterns
- **Akcia:** Move to `docs/reference/COLLABORATION_RULES.md`

---

## Quick Links

**Reference:**
- [Glossary](GLOSSARY.md) - Slovník termínov
- [API Reference](API_REFERENCE.md) - API quick ref

**Related:**
- [System Terminology](../system/TERMINOLOGY.md) - NEX terminológia

---

## Štatistika

- **Total dokumentov:** 2 (draft) + 1 (existuje mimo)
- **Priority:** Stredná (doplniť postupne)

---

**See Also:**
- [Documentation Index](../00_DOCUMENTATION_INDEX.md) - Hlavný index
- [System Terminology](../system/TERMINOLOGY.md) - Existing terminology doc
""",

    "archive/00_ARCHIVE_INDEX.md": """# Archive Documentation Index

**Kategória:** Archive  
**Status:** 🟢 Complete  
**Vytvorené:** 2025-12-15  
**Aktualizované:** 2025-12-15

---

## Účel

História vývoja projektu, dokumentácia sessions a archivované dokumenty.

---

## Štruktúra

### [sessions/](sessions/)
**Session History**

Obsahuje archivované session dokumenty z development procesu.

**Status:** Adresár vytvorený, pripravený na session archívy

---

## Archívna Stratégia

### Čo Archivovať

**Session dokumenty:**
- Detailné záznamy významných sessions
- Major milestones, rozhodnutia
- Problem-solving sessions

**Historické dokumenty:**
- Staré verzie dokumentácie
- Deprecated features
- Lessons learned

### Čo NEARCHIVOVAŤ

❌ Draft dokumenty (patria do príslušných kategórií)  
❌ Aktuálna dokumentácia (zostáva v primary locations)  
❌ .md-old súbory (migrujú sa do nových dokumentov)

---

## Quick Links

**Archive:**
- [Sessions Directory](sessions/) - Session history

---

## Štatistika

- **Adresáre:** 1 (sessions/)
- **Dokumenty:** 0 (pripravené na archívne dokumenty)
- **Status:** Ready for use

---

**See Also:**
- [Documentation Index](../00_DOCUMENTATION_INDEX.md) - Hlavný index
- [SESSION_NOTES](../../SESSION_NOTES/) - Current session tracking
"""
}


def main():
    """Hlavná funkcia scriptu"""
    print("=" * 80)
    print("📋 AKTUALIZÁCIA VŠETKÝCH INDEX SÚBOROV - NEX AUTOMAT")
    print("=" * 80)
    print()
    print(f"Monorepo: {MONOREPO_ROOT}")
    print(f"Docs:     {DOCS_ROOT}")
    print()

    # Aktualizuj indexy
    print("1️⃣ Aktualizácia index súborov...")
    print("=" * 80)

    updated_count = 0

    for relative_path, content in INDEXES.items():
        file_path = DOCS_ROOT / relative_path

        # Vytvor adresár ak neexistuje
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Ulož súbor
        file_path.write_text(content, encoding='utf-8')
        print(f"   ✅ Aktualizovaný: {relative_path}")
        updated_count += 1

    print()
    print(f"   Aktualizovaných indexov: {updated_count}")
    print()

    # Sumár
    print("=" * 80)
    print("✅ VŠETKY INDEXY AKTUALIZOVANÉ!")
    print("=" * 80)
    print()
    print("📊 Štatistika:")
    print(f"   Aktualizovaných súborov: {updated_count}")
    print()
    print("📋 Aktualizované indexy:")
    for relative_path in INDEXES.keys():
        print(f"   - {relative_path}")
    print()
    print("🔄 Ďalší krok:")
    print("   1. git add docs/")
    print('   2. git commit -m "docs: Update all index files with content"')
    print("   3. Pokračovať s migráciou .md-old súborov")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()