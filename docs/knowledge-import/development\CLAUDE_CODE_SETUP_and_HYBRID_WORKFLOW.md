# Zhrnutie: Claude Code Setup a Hybridný Workflow

**Dátum:** 17.1.2026
**Téma:** Inštalácia Claude Code, konfigurácia pre NEX Automat, nový hybridný workflow

---

## Čo bolo spravené

### 1. Claude Code nainštalovaný a nakonfigurovaný
- Verzia: 2.1.7
- Autentifikácia: Claude Max (automation@isnex.ai)
- Model: Opus 4.5
- Projekt: `C:\Development\nex-automat`

### 2. CLAUDE.md vytvorený a commitnutý
- Commit: `a88f3b9` na develop branch
- Pushed do `rauschiccsk/nex-automat`
- Obsahuje:
  - Project overview a monorepo štruktúru
  - Common commands (RAG, Python apps, web frontend)
  - Architecture (multi-tenant RAG, invoice pipeline)
  - Code style (Black, Ruff, Python 3.11+)
  - **Critical Rules** (GitHub org, RAG URL, POSTGRES_PASSWORD, sys.executable, sensitive data)
  - Collaboration rules z COLLABORATION_RULES.md

### 3. Hybridný workflow dohodnutý

| Fáza | Nástroj | Účel |
|------|---------|------|
| Plánovanie a analýza | Claude Chat | Diskusia, architektúra, rozhodnutia |
| Implementácia | Claude Code | Písanie kódu, testy, commity |
| Code review | Claude Chat | Diskusia o kvalite |
| Opravy a iterácie | Claude Code | Bug fixes, refaktoring |

### 4. Prvý test Claude Code úspešný
- Analýza `apps/` štruktúry
- Identifikované services: nex-brain, supplier-invoice-loader/worker/staging/editor
- Deployment targets: magerstav, andros

---

## Čo zostáva rovnaké

- Všetky pravidlá z memory (30 položiek)
- RAG systém pre knowledge base
- Session notes workflow
- Slovenčina, token tracking
- Step-by-step prístup, single solution

## Čo sa mení

- **Implementácia** ide cez Claude Code (nie artifacts + copy-paste)
- Claude Code má priamy prístup k súborom a terminálu
- Git operácie môže robiť Claude Code priamo

---

## Ako používať Claude Code

```powershell
cd C:\Development\nex-automat
claude
```

Základné príkazy:
- `/help` - všetky príkazy
- `/model` - prepnutie modelu
- `/compact` - kompresia kontextu
- `/status` - stav session

---

## Budúce rozšírenia (optional)

- Slash commands pre opakované workflow (`/fix-issue`, `/migrate-table`)
- Skills pre automatické procesy
- MCP server pre RAG integráciu

---

## Pre nový chat

Tento setup je hotový. V novom chate môžeš pokračovať s bežnou prácou. Claude Code je pripravený na implementačné úlohy.