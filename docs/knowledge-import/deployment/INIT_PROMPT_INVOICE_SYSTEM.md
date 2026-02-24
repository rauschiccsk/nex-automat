# INIT PROMPT - Invoice Processing System Setup

**Projekt:** nex-automat v3.0  
**Úloha:** Nastavenie jednotného email systému pre spracovanie dodávateľských faktúr  
**Zákazníci:** MAGERSTAV, ANDROS, ICC  
**Developer:** Zoltán Rausch  
**Dátum:** 2026-01-17

---

## 🎯 CIEĽ SESSION

Vytvoriť a nakonfigurovať jednotný email systém pre príjem PDF faktúr od dodávateľov pre troch zákazníkov, vrátane Google Cloud OAuth2 projektu.

---

## 📧 NOVÉ EMAIL ÚČTY

| Zákazník | Email | Status |
|----------|-------|--------|
| MAGERSTAV | magerstav.invoices@gmail.com | ❌ Vytvoriť (nahradí magerstavinvoice@gmail.com) |
| ANDROS | andros.invoices@gmail.com | ❌ Vytvoriť |
| ICC | icc.invoices@gmail.com | ❌ Vytvoriť |

---

## 📋 FÁZY IMPLEMENTÁCIE

### Fáza 1: Gmail účty (3x)
Pre každý účet:
- [ ] Vytvoriť Gmail účet
- [ ] Zapnúť 2FA (dvojfaktorové overenie)
- [ ] Vytvoriť App Password pre SMTP
- [ ] Zaznamenať credentials

### Fáza 2: Google Cloud projekt (1x spoločný)
- [ ] Vytvoriť projekt "nex-invoice-processing"
- [ ] Povoliť Gmail API
- [ ] Vytvoriť OAuth2 credentials (Desktop app)
- [ ] Nastaviť OAuth consent screen
- [ ] Pridať všetky 3 emailové adresy ako test users

### Fáza 3: OAuth2 autorizácia (3x)
Pre každý účet:
- [ ] Spustiť oauth_authorize.py
- [ ] Autorizovať prístup
- [ ] Uložiť .gmail_tokens.json

### Fáza 4: Aktualizácia MAGERSTAV
- [ ] Aktualizovať .env s novým emailom
- [ ] Nová OAuth2 autorizácia
- [ ] Test funkčnosti
- [ ] Presmerovanie z magerstavinvoice@ na magerstav.invoices@

### Fáza 5: Deployment ANDROS
- [ ] Windows VM - adresárová štruktúra
- [ ] Git clone + venv setup
- [ ] Konfigurácia .env
- [ ] OAuth2 autorizácia
- [ ] Windows Services (NSSM)
- [ ] End-to-end test

### Fáza 6: Dokumentácia
- [ ] Aktualizovať CREDENTIALS.md
- [ ] RAG reindex

---

## 🏗️ ARCHITEKTÚRA

### MAGERSTAV (existujúci)
```
Windows Server (standalone)
├── Temporal Server (lokálny, port 7233)
├── PostgreSQL (lokálny, port 5432)
├── NEX-Invoice-Worker (Windows Service)
├── NEX-Polling-Scheduler (Windows Service)
└── NEX-Automat-Loader (FastAPI, port 8001)
```

### ANDROS (nový)
```
Ubuntu 24.04 Host (192.168.100.23)
├── Docker: nex-temporal (port 7233)
├── Docker: nex-postgres (port 5432)
└── Docker: nex-brain, nex-ollama, nex-qdrant...

Windows Server 2025 VM (192.168.122.75)
├── NEX-Invoice-Worker → 192.168.122.1:7233
├── NEX-Polling-Scheduler
├── NEX-Automat-Loader (FastAPI, port 8001)
└── NEX Genesis (Btrieve)
```

### ICC (budúci)
- Interný pilot
- Rovnaká architektúra ako vhodná

---

## 📂 ADRESÁROVÁ ŠTRUKTÚRA

### Development (Zoltán PC)
```
C:\Development\nex-automat\
├── apps\
│   ├── btrieve-loader\    # FastAPI (32-bit)
│   ├── supplier-invoice-worker\    # Temporal worker (64-bit)
│   └── supplier-invoice-staging\   # GUI aplikácia
├── packages\
│   ├── nex-shared\
│   └── nex-staging\
└── docs\knowledge\                  # RAG indexed
```

### ANDROS Windows VM
```
C:\Deployment\nex-automat\          # Git clone
├── venv32\                         # 32-bit Python (Btrieve)
├── venv\                           # 64-bit Python
└── apps\supplier-invoice-worker\.env

C:\NEX\
├── IMPORT\
│   ├── SUPPLIER-INVOICES\          # Received PDFs
│   ├── SUPPLIER-STAGING\           # Staging PDF+XML
│   └── SUPPLIER-ARCHIVE\           # Temp
└── YEARACT\
    ├── STORES\                     # Btrieve files
    └── ARCHIV\SUPPLIER-INVOICES\   # Final archive
        ├── PDF\
        └── XML\
```

---

## ⚙️ KONFIGURÁCIA

### Google Cloud OAuth2 (spoločný projekt)
```
Project: nex-invoice-processing
OAuth2 Client: Desktop app
Test users:
  - magerstav.invoices@gmail.com
  - andros.invoices@gmail.com
  - icc.invoices@gmail.com
```

### ANDROS .env (supplier-invoice-worker)
```env
# Temporal Server (Docker na Ubuntu)
TEMPORAL_HOST=192.168.122.1
TEMPORAL_PORT=7233
TEMPORAL_NAMESPACE=default
TEMPORAL_TASK_QUEUE=andros-invoice-queue

# IMAP (Gmail OAuth2)
IMAP_HOST=imap.gmail.com
IMAP_PORT=993
IMAP_USER=andros.invoices@gmail.com
IMAP_FOLDER=INBOX

# FastAPI (lokálne na Windows VM)
FASTAPI_URL=http://localhost:8001
LS_API_KEY=andros-api-key-2026

# SMTP Notifications
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=andros.invoices@gmail.com
SMTP_PASSWORD=<app-password>
NOTIFY_EMAIL=rausch@icc.sk

# Logging
LOG_LEVEL=INFO
```

### ANDROS .env (btrieve-loader)
```env
# Database (Docker PostgreSQL na Ubuntu)
DATABASE_URL=postgresql://nex_admin:Nex1968@192.168.122.1:5432/nex_automat

# API
LS_API_KEY=andros-api-key-2026

# Paths
NEX_IMPORT_PATH=C:\NEX\IMPORT
NEX_STAGING_PATH=C:\NEX\IMPORT\SUPPLIER-STAGING
NEX_ARCHIVE_PATH=C:\NEX\YEARACT\ARCHIV\SUPPLIER-INVOICES
```

---

## 🔧 WINDOWS SERVICES (ANDROS)

| Service | Python | Working Dir | Command |
|---------|--------|-------------|---------|
| NEX-Invoice-Worker | venv (64-bit) | apps\supplier-invoice-worker | python -m workers.main_worker |
| NEX-Polling-Scheduler | venv (64-bit) | apps\supplier-invoice-worker | python -m scheduler.polling_scheduler |
| NEX-Automat-Loader | venv32 (32-bit) | apps\btrieve-loader | python -m uvicorn main:app --host 0.0.0.0 --port 8001 |

---

## 📚 RAG QUERIES

```
https://rag-api.icc.sk/search?query=supplier+invoice+worker+temporal+oauth&limit=5
https://rag-api.icc.sk/search?query=MAGERSTAV+gmail+IMAP+config&limit=5
https://rag-api.icc.sk/search?query=ANDROS+Windows+VM+deployment&limit=5
https://rag-api.icc.sk/search?query=NSSM+windows+service+nex&limit=5
```

---

## 🖥️ SERVERY

### ANDROS Ubuntu Host
- **LAN IP:** 192.168.100.23
- **Tailscale IP:** 100.107.134.104
- **SSH:** ssh andros@192.168.100.23
- **User/Pass:** andros / Andros-2026

### ANDROS Windows VM
- **Internal IP:** 192.168.122.75
- **RDP:** 100.107.134.104 (cez Tailscale DNAT)
- **User:** Administrator
- **Python 32-bit:** C:\Python311-32
- **Python 64-bit:** C:\Python311-64

### Docker služby (z Windows VM)
- **Temporal:** 192.168.122.1:7233
- **Temporal UI:** 192.168.122.1:8080
- **PostgreSQL:** 192.168.122.1:5432

---

## ✅ AKTUÁLNY STAV

### Hotové
- [x] ANDROS server - Ubuntu + Docker stack
- [x] ANDROS server - Windows VM s RDS
- [x] ANDROS server - Monitoring (Prometheus/Grafana)
- [x] MAGERSTAV - fungujúci invoice processing (starý email)

### Rozpracované
- [ ] Gmail účty (0/3 vytvorených)
- [ ] Google Cloud OAuth2 projekt
- [ ] ANDROS invoice deployment

---

## 🚀 ZAČAŤ S

### Krok 1: Vytvorenie Gmail účtov

Otvoriť https://accounts.google.com/signup (inkognito) a vytvoriť:

**1. magerstav.invoices@gmail.com**
| Pole | Hodnota |
|------|---------|
| Meno | Magerstav |
| Priezvisko | Invoices |
| Email | magerstav.invoices |
| Heslo | (zapísať do CREDENTIALS.md) |

**2. andros.invoices@gmail.com**
| Pole | Hodnota |
|------|---------|
| Meno | Andros |
| Priezvisko | Invoices |
| Email | andros.invoices |
| Heslo | (zapísať do CREDENTIALS.md) |

**3. icc.invoices@gmail.com**
| Pole | Hodnota |
|------|---------|
| Meno | ICC |
| Priezvisko | Invoices |
| Email | icc.invoices |
| Heslo | (zapísať do CREDENTIALS.md) |

### Krok 2: 2FA + App Passwords

Pre každý účet:
1. Prihlásiť sa do Gmail
2. Ísť na https://myaccount.google.com/security
3. Zapnúť 2-Step Verification
4. Vytvoriť App Password (Mail)
5. Zapísať App Password do CREDENTIALS.md

### Krok 3: Google Cloud Console

1. Ísť na https://console.cloud.google.com
2. Vytvoriť nový projekt: "nex-invoice-processing"
3. APIs & Services → Enable APIs → Gmail API
4. APIs & Services → Credentials → Create OAuth Client ID
5. Application type: Desktop app
6. Name: NEX Invoice Worker
7. OAuth consent screen → Add test users (všetky 3 emaily)

---

## ⏱️ ČASOVÝ ODHAD

| Fáza | Čas |
|------|-----|
| Gmail účty (3x) | 30 min |
| 2FA + App Passwords | 20 min |
| Google Cloud projekt | 30 min |
| MAGERSTAV migrácia | 30 min |
| ANDROS deployment | 2 hod |
| Testovanie | 1 hod |
| Dokumentácia | 30 min |
| **Celkom** | **~5-6 hodín** |

---

## ⚠️ DÔLEŽITÉ POZNÁMKY

1. **Jeden Google Cloud projekt** pre všetkých zákazníkov (jednoduchšia správa)
2. **OAuth2 tokeny** sa ukladajú do `.gmail_tokens.json` (v .gitignore)
3. **App Passwords** sú potrebné pre SMTP notifikácie
4. **32-bit Python** je nutný pre Btrieve DLL kompatibilitu
5. **CREDENTIALS.md** nikdy do Gitu - len RAG indexed