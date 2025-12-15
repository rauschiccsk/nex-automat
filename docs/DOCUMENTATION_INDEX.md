# Dokumentácia NEX Automat - Hlavný Index

**Vytvorené:** 2025-12-15  
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
- **Jednotlivé moduly:** `applications/{module-name}/`
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
**Dátum:** 2025-12-15
