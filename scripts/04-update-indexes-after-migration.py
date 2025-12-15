#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update Index Files After .md-old Migration - NEX Automat
Location: C:/Development/nex-automat/scripts/04-update-indexes-after-migration.py

Aktualizuje index súbory po migrácii .md-old dokumentov.
Pridáva nové dokumenty a aktualizuje štatistiky.
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

Strategická dokumentácia obsahuje dlhodobé plány, vízie projektu, technologické rozhodnutia a roadmap.

---

## Dokumenty v Strategic

### Kompletné Dokumenty

**[QUICK_WINS_TECHNOLOGIES.md](QUICK_WINS_TECHNOLOGIES.md)**
- Quick wins technológie (Redis, Sentry, Streamlit, Docker, Grafana, GitHub Actions)
- Implementačný plán, náklady €0-312/rok, benefity
- Status: 🟢 Complete
- Veľkosť: ~19 KB

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
- [Quick Wins Technologies](QUICK_WINS_TECHNOLOGIES.md) - Okamžité benefity
- [AI/ML Technologies](AI_ML_TECHNOLOGIES.md) - Schválené AI/ML nástroje
- [Technology Decisions](TECHNOLOGY_DECISIONS.md) - História rozhodnutí

---

## Štatistika

- **Total dokumentov:** 5
- **Complete:** 4
- **Draft:** 1
- **Total veľkosť:** ~71 KB

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

**[MONOREPO_GUIDE.md](MONOREPO_GUIDE.md)**
- Kompletný guide pre prácu s monorepo
- Getting started, workflow, testing, troubleshooting
- Status: 🟢 Complete
- Veľkosť: ~11 KB

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
- [Monorepo Guide](MONOREPO_GUIDE.md) - Práca s monorepo
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

- **Total dokumentov:** 7
- **Complete:** 3
- **Draft:** 4
- **Total veľkosť:** ~59 KB

---

**See Also:**
- [Documentation Index](../00_DOCUMENTATION_INDEX.md) - Hlavný index
- [Development Guide](../development/00_DEVELOPMENT_INDEX.md) - Setup a deployment
- [Packages Index](../packages/00_PACKAGES_INDEX.md) - Shared packages
""",

    "development/00_DEVELOPMENT_INDEX.md": """# Development Documentation Index

**Kategória:** Development  
**Status:** 🟡 In Progress  
**Vytvorené:** 2025-12-15  
**Aktualizované:** 2025-12-15

---

## Účel

Setup guides, Git workflow, contributing guidelines, testing stratégie, deployment procesy a development best practices.

---

## Dokumenty v Development

### Kompletné Dokumenty

**[GIT_WORKFLOW.md](GIT_WORKFLOW.md)**
- Git branching strategy (main/develop/hotfix)
- PyCharm Git operations
- Commit/Push/Merge workflows
- Status: 🟢 Complete
- Veľkosť: ~5 KB

**[CONTRIBUTING.md](CONTRIBUTING.md)**
- Contributing guidelines a code of conduct
- Development workflow, code style, commit messages
- Testing requirements, PR process
- Status: 🟢 Complete
- Veľkosť: ~12 KB

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

**Akcia:** Tieto súbory treba systematicky zmigrovat do DEPLOYMENT.md

---

## Quick Links

**Workflow:**
- [Git Workflow](GIT_WORKFLOW.md) - Git branching a operations
- [Contributing](CONTRIBUTING.md) - Contributing guidelines

**Setup:**
- [Setup Guide](SETUP_GUIDE.md) - Environment setup

**Testing:**
- [Testing Strategy](TESTING_STRATEGY.md) - Test approach

**Deployment:**
- [Deployment](DEPLOYMENT.md) - Deployment procedures

---

## Štatistika

- **Total dokumentov:** 5
- **Complete:** 2
- **Draft:** 3
- **.md-old súborov:** 12 (v docs/deployment/)
- **Priority:** Vysoká (kritická pre development)

---

**See Also:**
- [Documentation Index](../00_DOCUMENTATION_INDEX.md) - Hlavný index
- [System Architecture](../system/ARCHITECTURE.md) - Architektúra
- [Monorepo Guide](../system/MONOREPO_GUIDE.md) - Monorepo workflow
""",

    "reference/00_REFERENCE_INDEX.md": """# Reference Documentation Index

**Kategória:** Reference  
**Status:** 🟡 In Progress  
**Vytvorené:** 2025-12-15  
**Aktualizované:** 2025-12-15

---

## Účel

Workflow reference, glossary, API reference, collaboration rules a ostatné referenčné materiály.

---

## Dokumenty v Reference

### Kompletné Dokumenty

**[WORKFLOW_REFERENCE.md](WORKFLOW_REFERENCE.md)**
- Workflow quick reference pre prácu s Claude
- Session workflow, file access commands
- Quick decision tree, troubleshooting
- Status: 🟢 Complete
- Veľkosť: ~5 KB

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

**Workflow:**
- [Workflow Reference](WORKFLOW_REFERENCE.md) - Quick reference

**Reference:**
- [Glossary](GLOSSARY.md) - Slovník termínov
- [API Reference](API_REFERENCE.md) - API quick ref

**Related:**
- [System Terminology](../system/TERMINOLOGY.md) - NEX terminológia

---

## Štatistika

- **Total dokumentov:** 3
- **Complete:** 1
- **Draft:** 2 + 1 (existuje mimo)
- **Priority:** Stredná (doplniť postupne)

---

**See Also:**
- [Documentation Index](../00_DOCUMENTATION_INDEX.md) - Hlavný index
- [System Terminology](../system/TERMINOLOGY.md) - Existing terminology doc
- [Workflow Reference](WORKFLOW_REFERENCE.md) - Session workflow
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

## Archivované Dokumenty

### Historical Snapshots

**[CURRENT_STATE_2025-11-26.md](CURRENT_STATE_2025-11-26.md)**
- Snapshot projektu k GO-LIVE dátumu (2025-11-27)
- Kompletný inventory v2.0 (architektúra, komponenty, workflow)
- Status: 📦 Archived
- Veľkosť: ~14 KB
- Note: Historical reference, obsahuje outdated info (n8n→Temporal)

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
- [Current State Snapshot](CURRENT_STATE_2025-11-26.md) - GO-LIVE snapshot

---

## Štatistika

- **Adresáre:** 1 (sessions/)
- **Dokumenty:** 1 (historical snapshot)
- **Status:** Ready for use

---

**See Also:**
- [Documentation Index](../00_DOCUMENTATION_INDEX.md) - Hlavný index
- [SESSION_NOTES](../../SESSION_NOTES/) - Current session tracking
- [Project Roadmap](../strategic/PROJECT_ROADMAP.md) - Current roadmap
"""
}


def main():
    """Hlavná funkcia scriptu"""
    print("=" * 80)
    print("📋 AKTUALIZÁCIA INDEX SÚBOROV PO MIGRÁCII - NEX AUTOMAT")
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
    print("📈 Pridané nové dokumenty:")
    print("   Strategic:")
    print("     ✅ QUICK_WINS_TECHNOLOGIES.md")
    print("   System:")
    print("     ✅ MONOREPO_GUIDE.md")
    print("   Development:")
    print("     ✅ GIT_WORKFLOW.md")
    print("     ✅ CONTRIBUTING.md")
    print("   Reference:")
    print("     ✅ WORKFLOW_REFERENCE.md")
    print("   Archive:")
    print("     📦 CURRENT_STATE_2025-11-26.md")
    print()
    print("📝 Ďalší krok:")
    print("   1. git add docs/")
    print('   2. git commit -m "docs: Update indexes after .md-old migration (batch 1)"')
    print("   3. Pokračovať s migráciou ďalších .md-old súborov")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()