# NEX Automat - Strategic Plan: Multi-Tenant Invoice Processing

**Location:** docs/knowledge/development/
**Created:** 2026-01-20
**Status:** APPROVED

---

## Prehľad

Tri zákazníci, každý s úplne izolovaným systémom spracovania dodávateľských faktúr.

| Zákazník | Segment | Dodávatelia | Server |
|----------|---------|-------------|--------|
| MAGERSTAV | Stavebný materiál | ~50         | Vlastný Windows Server |
| ANDROS | Pneumatiky | ~30         | ANDROS Server (VM) |
| ICC | IT, software | ~5          | ANDROS Server (VM) |

---

## Filozofia: Úplná izolácia

Každý zákazník má:
- Vlastnú PostgreSQL databázu
- Vlastný Temporal server
- Vlastný nex-automat deployment
- Vlastné Windows Services
- Vlastný email účet
- Vlastné pravidlá párovania produktov

---

## Architektúra

### MAGERSTAV (Existujúci - standalone)

```
Windows Server (standalone)
├── PostgreSQL (localhost:5432)
├── Temporal Server (localhost:7233)
├── NEX-Invoice-Worker (Windows Service)
├── NEX-Polling-Scheduler (Windows Service)
├── NEX-Automat-Loader (FastAPI :8001)
└── NEX Genesis (Btrieve)
```

### ANDROS Server - Ubuntu Host (192.168.100.23)

```
Ubuntu 24.04 Host
│
├── ANDROS Docker Stack
│   ├── nex-postgres-andros (:5432)
│   ├── nex-temporal-andros (:7233)
│   └── nex-temporal-ui-andros (:8080)
│
└── ICC Docker Stack
    ├── nex-postgres-icc (:5433)
    ├── nex-temporal-icc (:7234)
    └── nex-temporal-ui-icc (:8081)
```

### ANDROS Server - Windows VM (192.168.122.75)

```
Windows Server 2025 VM
│
├── C:\ANDROS\
│   ├── NEX\YEARACT\                    # Btrieve data
│   └── nex-automat\                    # Git clone
│       ├── venv\                       # 64-bit Python
│       ├── venv32\                     # 32-bit Python
│       └── apps\supplier-invoice-worker\.env
│
└── C:\ICC\
    ├── NEX\YEARACT\                    # Btrieve data
    └── nex-automat\                    # Git clone
        ├── venv\                       # 64-bit Python
        ├── venv32\                     # 32-bit Python
        └── apps\supplier-invoice-worker\.env
```

---

## Sieťová topológia

```
┌─────────────────────────────────────────────────────────────────┐
│  DEVELOPMENT PC (Zoltán)                                        │
│  C:\Development\nex-automat\                                    │
│  Claude Code → Git push                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Git (GitHub)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ANDROS SERVER - Ubuntu (192.168.100.23)                        │
│  Git pull → Docker Compose                                      │
│  ANDROS: postgres:5432, temporal:7233                           │
│  ICC: postgres:5433, temporal:7234                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ virbr0 (192.168.122.1)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ANDROS VM - Windows (192.168.122.75)                           │
│  Git pull → Windows Services                                    │
│  C:\ANDROS\nex-automat\ → :5432, :7233                          │
│  C:\ICC\nex-automat\ → :5433, :7234                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Email systém (Webglobe)

| Zákazník | Email | Server | IMAP | SMTP |
|----------|-------|--------|------|------|
| ANDROS | andros.invoices@icc.sk | mail.webglobe.sk | 993 | 465 |
| ICC | icc.invoices@icc.sk | mail.webglobe.sk | 993 | 465 |
| MAGERSTAV | magerstav.invoices@icc.sk | mail.webglobe.sk | 993 | 465 |

**Výhody oproti Gmail:**
- Žiadne OAuth2
- Štandardné IMAP/SMTP heslo
- Profesionálna doména
- Plná kontrola

---

## Windows Services (ANDROS VM)

| Service | Zákazník | Python | Port/Queue |
|---------|----------|--------|------------|
| NEX-Invoice-Worker-ANDROS | ANDROS | venv (64-bit) | temporal:7233 |
| NEX-Polling-Scheduler-ANDROS | ANDROS | venv (64-bit) | - |
| NEX-Automat-Loader-ANDROS | ANDROS | venv32 (32-bit) | :8001 |
| NEX-Invoice-Worker-ICC | ICC | venv (64-bit) | temporal:7234 |
| NEX-Polling-Scheduler-ICC | ICC | venv (64-bit) | - |
| NEX-Automat-Loader-ICC | ICC | venv32 (32-bit) | :8002 |

---

## Implementačné fázy

| Fáza | Úloha | Prostredie | Nástroj |
|------|-------|------------|---------|
| 1 | Docker Compose - ANDROS stack | Ubuntu | Claude Code → SSH |
| 2 | Docker Compose - ICC stack | Ubuntu | Claude Code → SSH |
| 3 | nex-automat deployment ANDROS | Windows VM | Git pull |
| 4 | nex-automat deployment ICC | Windows VM | Git pull |
| 5 | Windows Services (6x) | Windows VM | NSSM |
| 6 | Konfigurácia dodávateľov ANDROS | Databáza | SQL |
| 7 | End-to-end testovanie | Všetko | Manual |
| 8 | Dokumentácia | RAG | Claude Chat |

---

## Workflow: Development → Production

```
1. Claude Code (Development PC)
   └── Vytvára/upravuje súbory
   └── Git commit + push

2. ANDROS Server - Ubuntu (SSH)
   └── cd /opt/nex-automat
   └── git pull
   └── docker compose up -d

3. ANDROS VM - Windows (RDP)
   └── cd C:\ANDROS\nex-automat
   └── git pull
   └── Restart Windows Services
```

---

## Konfiguračné súbory

### ANDROS .env (supplier-invoice-worker)
```env
TEMPORAL_HOST=192.168.122.1
TEMPORAL_PORT=7233
IMAP_HOST=mail.webglobe.sk
IMAP_PORT=993
IMAP_USER=andros.invoices@icc.sk
IMAP_PASSWORD=Nex-Andros2026-Inv
FASTAPI_URL=http://localhost:8001
SMTP_HOST=mail.webglobe.sk
SMTP_PORT=465
```

### ICC .env (supplier-invoice-worker)
```env
TEMPORAL_HOST=192.168.122.1
TEMPORAL_PORT=7234
IMAP_HOST=mail.webglobe.sk
IMAP_PORT=993
IMAP_USER=icc.invoices@icc.sk
IMAP_PASSWORD=Nex-Icc2026-Inv
FASTAPI_URL=http://localhost:8002
SMTP_HOST=mail.webglobe.sk
SMTP_PORT=465
```

---

## Poznámky

1. **Úplná izolácia** - žiadne zdieľanie databáz ani služieb medzi zákazníkmi
2. **Jednotný kód** - rovnaký nex-automat repozitár, rôzna konfigurácia
3. **Webglobe email** - jednoduchšie ako Gmail OAuth2
4. **Claude Code** - len na Development PC, nie na serveroch
5. **Git** - jediný spôsob prenosu kódu medzi prostrediami