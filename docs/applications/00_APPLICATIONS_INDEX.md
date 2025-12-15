# Applications Documentation Index

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
