# Dokumentácia NEX Automat - Hlavný Index

**Vytvorené:** 2025-12-15  
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
- [Session Notes](../init_chat/SESSION_NOTES.md)
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
**Dátum:** 2025-12-15  
**Status:** ✅ Ready for Use