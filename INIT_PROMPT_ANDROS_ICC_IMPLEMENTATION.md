# INIT PROMPT - ANDROS/ICC Multi-Tenant Implementation

**Projekt:** nex-automat v3.0
**Úloha:** Implementácia izolovaných invoice processing systémov pre ANDROS a ICC
**Developer:** Zoltán Rausch
**Dátum:** 2026-01-20

---

## 🎯 CIEĽ SESSION

Implementovať úplne izolované invoice processing systémy pre dvoch zákazníkov (ANDROS, ICC) na zdieľanom serveri s využitím Docker kontajnerov a Windows Services.

---

## 📚 RAG DOKUMENTY

Pred začatím práce načítať z RAG:
```
https://rag-api.icc.sk/search?query=STRATEGIC+PLAN+MULTI+TENANT&limit=3
https://rag-api.icc.sk/search?query=CREDENTIALS+webglobe+email&limit=3
https://rag-api.icc.sk/search?query=temporal+docker+compose&limit=3
```

---

## ✅ DOKONČENÉ (predchádzajúce sessions)

- [x] ANDROS Server - Ubuntu 24.04 + KVM
- [x] ANDROS Server - Windows VM (192.168.122.75)
- [x] Python 32-bit a 64-bit na Windows VM
- [x] NEX Genesis nainštalovaný (C:\ANDROS\NEX\, C:\ICC\NEX\)
- [x] Webglobe email účty vytvorené (3x)
- [x] Strategický plán schválený
- [x] Git clone C:\ANDROS\nex-automat\ (develop branch)

---

## 🏗️ ARCHITEKTÚRA

### Ubuntu Host (192.168.100.23)

| Stack | PostgreSQL | Temporal | Temporal UI |
|-------|------------|----------|-------------|
| ANDROS | 5432 | 7233 | 8080 |
| ICC | 5433 | 7234 | 8081 |

### Windows VM (192.168.122.75)

| Zákazník | nex-automat | FastAPI | Temporal |
|----------|-------------|---------|----------|
| ANDROS | C:\ANDROS\nex-automat\ | :8001 | 192.168.122.1:7233 |
| ICC | C:\ICC\nex-automat\ | :8002 | 192.168.122.1:7234 |

---

## 📧 EMAIL KONFIGURÁCIA

| Zákazník | Email | Server | IMAP/SMTP |
|----------|-------|--------|-----------|
| ANDROS | andros.invoices@icc.sk | mail.webglobe.sk | 993/465 |
| ICC | icc.invoices@icc.sk | mail.webglobe.sk | 993/465 |

Heslá: pozri CREDENTIALS.md v RAG

---

## 📋 IMPLEMENTAČNÉ FÁZY

### Fáza 1: Docker Compose - ANDROS stack (Ubuntu)
- [ ] Vytvoriť docker-compose.andros.yml
- [ ] PostgreSQL kontajner (port 5432)
- [ ] Temporal kontajner (port 7233)
- [ ] Temporal UI kontajner (port 8080)
- [ ] Vytvoriť .env.andros
- [ ] Otestovať: docker compose -f docker-compose.andros.yml up -d

### Fáza 2: Docker Compose - ICC stack (Ubuntu)
- [ ] Vytvoriť docker-compose.icc.yml
- [ ] PostgreSQL kontajner (port 5433)
- [ ] Temporal kontajner (port 7234)
- [ ] Temporal UI kontajner (port 8081)
- [ ] Vytvoriť .env.icc
- [ ] Otestovať: docker compose -f docker-compose.icc.yml up -d

### Fáza 3: nex-automat ANDROS (Windows VM)
- [ ] Vytvoriť venv (64-bit): C:\ANDROS\nex-automat\venv\
- [ ] Vytvoriť venv32 (32-bit): C:\ANDROS\nex-automat\venv32\
- [ ] pip install dependencies
- [ ] Vytvoriť .env pre supplier-invoice-worker
- [ ] Vytvoriť .env pre supplier-invoice-loader
- [ ] Test konektivity na Docker služby

### Fáza 4: nex-automat ICC (Windows VM)
- [ ] Git clone C:\ICC\nex-automat\ (develop branch)
- [ ] Vytvoriť venv (64-bit)
- [ ] Vytvoriť venv32 (32-bit)
- [ ] pip install dependencies
- [ ] Vytvoriť .env súbory
- [ ] Test konektivity

### Fáza 5: Windows Services (Windows VM)
- [ ] NSSM inštalácia (ak chýba)
- [ ] NEX-Invoice-Worker-ANDROS
- [ ] NEX-Polling-Scheduler-ANDROS
- [ ] NEX-Automat-Loader-ANDROS
- [ ] NEX-Invoice-Worker-ICC
- [ ] NEX-Polling-Scheduler-ICC
- [ ] NEX-Automat-Loader-ICC

### Fáza 6: Testovanie
- [ ] ANDROS: Email → Processing → Staging
- [ ] ICC: Email → Processing → Staging
- [ ] Monitoring (Temporal UI, logs)

### Fáza 7: Dokumentácia
- [ ] Aktualizovať CREDENTIALS.md
- [ ] Vytvoriť DEPLOYMENT_ANDROS_ICC.md
- [ ] RAG reindex

---

## 🔧 WORKFLOW

```
Development PC                    ANDROS Server (Ubuntu)           Windows VM
─────────────                    ─────────────────────            ──────────
Claude Code                            SSH                           RDP
    │                                   │                             │
    ├─► docker-compose.andros.yml       │                             │
    ├─► docker-compose.icc.yml          │                             │
    ├─► .env.andros.example             │                             │
    ├─► .env.icc.example                │                             │
    │                                   │                             │
    └─► Git push ──────────────────────►│                             │
                                        │                             │
                                   git pull                           │
                                   docker compose up                  │
                                        │                             │
                                        └────────────────────────────►│
                                                                 git pull
                                                                 venv setup
                                                                 services
```

---

## 🖥️ PRÍSTUPY

### Ubuntu Host
```bash
ssh andros@192.168.100.23
# Password: Andros-2026
```

### Windows VM
```
RDP: 100.107.134.104 (Tailscale)
User: Administrator
```

### Docker služby (z Windows VM)
- Temporal ANDROS: 192.168.122.1:7233
- Temporal ICC: 192.168.122.1:7234
- PostgreSQL ANDROS: 192.168.122.1:5432
- PostgreSQL ICC: 192.168.122.1:5433

---

## 📂 SÚBOROVÁ ŠTRUKTÚRA (vytvoriť)

### V repozitári (Claude Code)
```
deployment/
├── docker/
│   ├── docker-compose.andros.yml
│   ├── docker-compose.icc.yml
│   ├── .env.andros.example
│   └── .env.icc.example
└── scripts/
    ├── setup-andros-venv.ps1
    └── setup-icc-venv.ps1
```

---

## ⚠️ DÔLEŽITÉ POZNÁMKY

1. **Hybridný workflow:** Claude Chat = plánovanie, Claude Code = implementácia
2. **Git branch:** develop
3. **Úplná izolácia:** Žiadne zdieľanie DB ani Temporal medzi zákazníkmi
4. **Webglobe email:** Štandardný IMAP/SMTP, bez OAuth2
5. **32-bit Python:** Potrebný pre Btrieve DLL (supplier-invoice-loader)
6. **Porty:** ANDROS (5432, 7233, 8001), ICC (5433, 7234, 8002)

---

## 🚀 ZAČAŤ S

### Krok 1: Claude Code session

```powershell
cd C:\Development\nex-automat
claude
```

### Krok 2: Prvá úloha

"Vytvor deployment/docker/docker-compose.andros.yml pre ANDROS stack:
- PostgreSQL 15 na porte 5432
- Temporal 1.24.2 na porte 7233
- Temporal UI na porte 8080
- Použiť volumes pre perzistenciu
- Network: nex-andros-network"

---

## ⏱️ ČASOVÝ ODHAD

| Fáza | Čas |
|------|-----|
| Docker Compose ANDROS | 30 min |
| Docker Compose ICC | 15 min |
| nex-automat ANDROS | 45 min |
| nex-automat ICC | 30 min |
| Windows Services | 45 min |
| Testovanie | 1 hod |
| Dokumentácia | 30 min |
| **Celkom** | **~4-5 hodín** |