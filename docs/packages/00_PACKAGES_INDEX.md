# Packages Documentation Index

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
