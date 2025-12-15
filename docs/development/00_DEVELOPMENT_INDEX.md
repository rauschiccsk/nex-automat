# Development Documentation Index

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
