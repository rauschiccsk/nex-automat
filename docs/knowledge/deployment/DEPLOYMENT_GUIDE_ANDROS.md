# INIT PROMPT - ANDROS s.r.o. Deployment

**Projekt:** nex-automat v3.0  
**Zákazník:** ANDROS s.r.o.  
**Typ:** Čistá inštalácia od nuly  
**Server OS:** Microsoft Windows Server 2022 (čistá inštalácia)  
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina

⚠️ **KRITICKÉ:** Dodržiavať pravidlá z memory_user_edits!

---

## 🖥️ Hardware Konfigurácia

| Komponent | Špecifikácia |
|-----------|--------------|
| Server | Dell PowerEdge R740XD 24 bay 2U RACK |
| CPU | 2x Intel Xeon Gold 6138 (40 jadier / 80 vlákien) |
| RAM | 512GB DDR4 2666 |
| RAID | H740p controller |
| Storage | 8x 1.2TB SAS 10K RPM |
| Sieť | 2x 1GbE + 2x 10GbE RJ45 |
| Management | iDRAC Enterprise |
| Napájanie | 2x 750W redundant |

---

## 📋 Deployment Checklist

### Phase 1: OS a Základný Software

| Úloha | Status | Poznámka |
|-------|--------|----------|
| Windows Server 2022 inštalácia | ⏳ | Čistá inštalácia |
| Windows Update | ⏳ | Všetky aktualizácie |
| Disk partitioning (RAID) | ⏳ | Nastaviť cez H740p |
| Firewall konfigurácia | ⏳ | Porty 5432, 7233, 8000, 8001, 8233 |
| Remote Desktop povolenie | ⏳ | Pre správu |

### Phase 2: Software Inštalácia

| Software | Verzia | Účel | Status |
|----------|--------|------|--------|
| Python 32-bit | 3.12.x | supplier-invoice-loader (Btrieve) | ⏳ |
| Python 64-bit | 3.12.x | GUI apps, Temporal worker | ⏳ |
| PostgreSQL | 15.x+ | Staging databáza | ⏳ |
| Git | 2.40+ | Deployment | ⏳ |
| NSSM | 2.24 | Windows Service Manager | ⏳ |
| Pervasive PSQL | 11+ | Btrieve driver (ak NEX Genesis) | ⏳ |
| Temporal CLI | 1.5.1+ | Workflow orchestration | ⏳ |

### Phase 3: Adresárová Štruktúra

```
C:\Deployment\nex-automat\          # Hlavný deployment
C:\Temporal\                        # Temporal Server
    ├── cli\temporal.exe
    └── data\temporal.db
C:\NEX\                             # NEX súbory
    ├── IMPORT\SUPPLIER-INVOICES\   # Prijaté PDF
    ├── IMPORT\SUPPLIER-STAGING\    # Staging
    ├── IMPORT\SUPPLIER-ARCHIVE\    # Archív
    └── YEARACT\STORES\             # Btrieve súbory (ak NEX Genesis)
```

### Phase 4: Git Clone a Virtual Environments

```powershell
# Clone repository
cd C:\Deployment
git clone https://github.com/rauschiccsk/nex-automat.git
cd nex-automat
git checkout main  # alebo develop pre testing

# venv32 (32-bit Python pre Btrieve)
C:\Python312-32\python.exe -m venv venv32
.\venv32\Scripts\Activate.ps1
pip install --upgrade pip
pip install -e packages/nex-staging
pip install -e packages/nex-shared
pip install -e apps/supplier-invoice-loader
deactivate

# venv (64-bit Python pre GUI a worker)
C:\Python312\python.exe -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -e packages/nex-staging
pip install -e packages/nex-shared
pip install -e apps/supplier-invoice-staging
deactivate

# Worker venv (64-bit, samostatný)
cd apps\supplier-invoice-worker
C:\Python312\python.exe -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
deactivate
```

### Phase 5: PostgreSQL Setup

```powershell
# 1. Inštalácia PostgreSQL 15.x
# 2. Nastavenie POSTGRES_PASSWORD (Machine level)
[System.Environment]::SetEnvironmentVariable("POSTGRES_PASSWORD", "SecurePassword", "Machine")

# 3. Vytvorenie databázy
psql -U postgres -c "CREATE DATABASE supplier_invoice_staging;"

# 4. Migrácie (z venv32)
cd C:\Deployment\nex-automat
.\venv32\Scripts\Activate.ps1
python -m apps.supplier-invoice-loader.database.migrations
```

### Phase 6: Temporal Server Setup

```powershell
# 1. Stiahnuť Temporal CLI
# https://github.com/temporalio/cli/releases
# Extrahovať do C:\Temporal\cli\

# 2. Test spustenie
C:\Temporal\cli\temporal.exe server start-dev --db-filename C:\Temporal\data\temporal.db

# 3. NSSM Windows Service
nssm install NEX-Temporal-Server "C:\Temporal\cli\temporal.exe" server start-dev --db-filename "C:\Temporal\data\temporal.db"
nssm set NEX-Temporal-Server AppDirectory "C:\Temporal"
nssm set NEX-Temporal-Server Start SERVICE_AUTO_START
```

### Phase 7: Gmail OAuth2 Setup (ANDROS špecifické)

**Google Cloud Console:**
1. Vytvoriť nový projekt: `andros-invoice-worker`
2. OAuth consent screen → External
3. Credentials → Desktop app
4. Pridať test user: `[ANDROS_EMAIL]@gmail.com`
5. Enable Gmail API

**Autorizácia:**
```powershell
cd C:\Deployment\nex-automat\apps\supplier-invoice-worker
.\venv\Scripts\Activate.ps1
python -m config.oauth_authorize
# Otvorí prehliadač, autorizovať Gmail účet
# Tokeny sa uložia do .gmail_tokens.json
```

### Phase 8: Environment Variables

**System Environment Variables (Machine level):**
```powershell
[System.Environment]::SetEnvironmentVariable("POSTGRES_PASSWORD", "SecurePassword", "Machine")
[System.Environment]::SetEnvironmentVariable("LS_API_KEY", "andros-api-key-2025", "Machine")
```

**Worker .env súbor:** `apps/supplier-invoice-worker/.env`
```env
# Temporal Server
TEMPORAL_HOST=localhost
TEMPORAL_PORT=7233
TEMPORAL_NAMESPACE=default
TEMPORAL_TASK_QUEUE=supplier-invoice-queue

# IMAP (Gmail) - OAuth2
IMAP_HOST=imap.gmail.com
IMAP_PORT=993
IMAP_USER=[ANDROS_EMAIL]@gmail.com
IMAP_PASSWORD=
IMAP_FOLDER=INBOX

# FastAPI Invoice Service
FASTAPI_URL=http://localhost:8000
LS_API_KEY=andros-api-key-2025

# Polling
POLL_INTERVAL_SECONDS=300

# Logging
LOG_LEVEL=INFO
```

### Phase 9: Windows Services (NSSM)

```powershell
$nssm = "C:\Deployment\nex-automat\tools\nssm\win64\nssm.exe"

# 1. NEX-Temporal-Server (už vytvorené v Phase 6)

# 2. NEX-Invoice-Loader (FastAPI)
& $nssm install NEX-Invoice-Loader "C:\Deployment\nex-automat\venv32\Scripts\python.exe" "-m" "uvicorn" "main:app" "--host" "0.0.0.0" "--port" "8000"
& $nssm set NEX-Invoice-Loader AppDirectory "C:\Deployment\nex-automat\apps\supplier-invoice-loader"
& $nssm set NEX-Invoice-Loader Start SERVICE_AUTO_START

# 3. NEX-Invoice-Worker (Temporal Worker)
& $nssm install NEX-Invoice-Worker "C:\Deployment\nex-automat\apps\supplier-invoice-worker\venv\Scripts\python.exe" "-m" "workers.main_worker"
& $nssm set NEX-Invoice-Worker AppDirectory "C:\Deployment\nex-automat\apps\supplier-invoice-worker"
& $nssm set NEX-Invoice-Worker Start SERVICE_AUTO_START

# 4. NEX-Polling-Scheduler
& $nssm install NEX-Polling-Scheduler "C:\Deployment\nex-automat\apps\supplier-invoice-worker\venv\Scripts\python.exe" "-m" "scheduler.polling_scheduler"
& $nssm set NEX-Polling-Scheduler AppDirectory "C:\Deployment\nex-automat\apps\supplier-invoice-worker"
& $nssm set NEX-Polling-Scheduler Start SERVICE_AUTO_START

# Štart služieb
Start-Service NEX-Temporal-Server
Start-Service NEX-Invoice-Loader
Start-Service NEX-Invoice-Worker
Start-Service NEX-Polling-Scheduler
```

### Phase 10: Verifikácia

```powershell
# Stav služieb
Get-Service "NEX-*"

# Health checks
Invoke-WebRequest -Uri "http://localhost:8000/health"  # Invoice Loader
# Temporal UI: http://localhost:8233

# Test workflow
cd C:\Deployment\nex-automat\apps\supplier-invoice-worker
.\venv\Scripts\Activate.ps1
python -m scheduler.polling_scheduler --once
```

---

## 🔧 Customer-Specific Konfigurácia

**Súbor:** `apps/supplier-invoice-loader/config/config_customer.py`

```python
# ANDROS s.r.o. konfigurácia
CUSTOMER_NAME = "ANDROS"
CUSTOMER_ID = "andros"

# NEX Genesis (ak existuje)
NEX_GENESIS_ENABLED = True  # alebo False
NEX_DATA_PATH = "C:\\NEX\\YEARACT\\STORES"

# API
API_KEY = os.getenv("LS_API_KEY", "andros-api-key-2025")

# Paths
PDF_INPUT_PATH = "C:\\NEX\\IMPORT\\SUPPLIER-INVOICES"
STAGING_PATH = "C:\\NEX\\IMPORT\\SUPPLIER-STAGING"
ARCHIVE_PATH = "C:\\NEX\\IMPORT\\SUPPLIER-ARCHIVE"
```

---

## 📊 Success Criteria

| Kritérium | Cieľ |
|-----------|------|
| Všetky Windows Services Running | ✅ |
| Health endpoint 200 OK | ✅ |
| Temporal UI dostupné | ✅ |
| Gmail OAuth2 funguje | ✅ |
| Test faktúra spracovaná | ✅ |
| PostgreSQL data uložené | ✅ |

---

## 🔗 RAG Queries

```
https://rag-api.icc.sk/search?query=DEPLOYMENT_GUIDE_V3+installation&limit=5
https://rag-api.icc.sk/search?query=Temporal+NSSM+Windows+Service&limit=5
https://rag-api.icc.sk/search?query=Gmail+OAuth2+setup+credentials&limit=5
https://rag-api.icc.sk/search?query=PostgreSQL+staging+database+setup&limit=5
```

---

## ⚠️ Dôležité Poznámky

1. **Čistá inštalácia** - žiadne legacy software, ideálne podmienky
2. **Windows Server 2022** - plná kompatibilita, žiadne workaroundy
3. **512GB RAM** - môžeme uvažovať o rozšírených funkciách (caching, etc.)
4. **10GbE sieť** - vysoká priepustnosť pre veľké PDF súbory

---

## 💾 Phase 0: RAID Konfigurácia (PRED inštaláciou OS)

**Konfigurácia: RAID 10** (8 diskov → 4.8TB užitočnej kapacity)

| Parameter | Hodnota |
|-----------|---------|
| RAID Level | RAID 10 |
| Disky | 8x 1.2TB SAS 10K |
| Kapacita | ~4.8TB |
| Redundancia | Až 4 disky môžu zlyhať |
| Výkon | Najlepší pre databázy |

**Postup:**
1. Zapnúť server
2. Počas POST stlačiť **F2** (System Setup) alebo **Ctrl+R** (RAID BIOS)
3. Vojsť do **Device Settings → RAID Controller (H740p)**
4. **Configuration Management → Create Virtual Disk**
5. Vybrať RAID Level: **RAID 10**
6. Vybrať všetkých 8 diskov
7. Strip Size: **256KB** (default, dobré pre mixed workload)
8. Read Policy: **Adaptive Read Ahead**
9. Write Policy: **Write Back** (ak je BBU/battery backup)
10. Potvrdiť a uložiť
11. Reštart → inštalácia Windows Server 2022

---

## 📝 Session Priority

**Immediate:** Phase 1-3 (OS, Software, Adresáre)  
**Next:** Phase 4-6 (Git, PostgreSQL, Temporal)  
**Final:** Phase 7-10 (OAuth2, Services, Verifikácia)

**Estimated Time:** 4-6 hodín pre kompletný deployment