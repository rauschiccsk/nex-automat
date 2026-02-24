# Temporal Deployment - Mágerstav Server

**Dátum nasadenia:** 2025-12-20
**Server:** Mágerstav (testovacie prostredie)
**Status:** ✅ PRODUCTION READY

---

## Prehľad infraštruktúry

### Server špecifikácie

| Parameter | Hodnota |
|-----------|---------|
| OS | Windows (64-bit) |
| Python (Worker) | 3.12 (64-bit) - `C:\Users\Magerstav\AppData\Local\Programs\Python\Python312` |
| Python (FastAPI) | 3.13 (32-bit) - `C:\Python313-32` |
| Disk | ~807 GB voľných |
| Prístup | RustDesk |

### Nasadené komponenty

| Komponenta | Verzia | Status |
|------------|--------|--------|
| Temporal CLI | 1.5.1 | ✅ Running |
| Temporal Server | 1.29.1 | ✅ Running |
| Temporal UI | 2.42.1 | ✅ Running |
| Temporalio Python SDK | 1.21.1 | ✅ Installed |

---

## Adresárová štruktúra

```
C:\Temporal\
├── cli\
│   └── temporal.exe           # Temporal CLI (213 MB)
├── data\
│   └── temporal.db            # SQLite databáza
└── temporal-cli.zip           # Pôvodný ZIP (záloha)

C:\Deployment\nex-automat\
├── apps\
│   ├── btrieve-loader\             # FastAPI API (32-bit Python)
│   └── supplier-invoice-worker\    # Temporal Worker (64-bit Python)
│       ├── activities\
│       ├── config\
│       ├── scheduler\
│       │   └── polling_scheduler.py
│       ├── workers\
│       │   └── main_worker.py
│       ├── workflows\
│       ├── venv\                   # 64-bit Python 3.12 venv
│       ├── .env
│       ├── .gmail_tokens.json
│       └── requirements.txt
└── tools\
    └── nssm\
        └── win32\
            └── nssm.exe            # NSSM 2.24
```

---

## Windows Services (NSSM)

### NEX-Temporal-Server

| Parameter | Hodnota |
|-----------|---------|
| Service Name | `NEX-Temporal-Server` |
| Display Name | `NEX Temporal Server` |
| Description | Temporal workflow orchestration server for NEX Automat |
| Executable | `C:\Temporal\cli\temporal.exe` |
| Arguments | `server start-dev --db-filename C:\Temporal\data\temporal.db --ui-port 8233` |
| Start Type | SERVICE_AUTO_START |
| AppRestartDelay | 5000 ms |

**Porty:**
- 7233 - Temporal Server (gRPC)
- 8233 - Temporal Web UI
- 51680 - Metrics (dynamický)

### NEX-Invoice-Worker

| Parameter | Hodnota |
|-----------|---------|
| Service Name | `NEX-Invoice-Worker` |
| Display Name | `NEX Invoice Worker` |
| Description | Temporal worker for invoice processing |
| Executable | `C:\Deployment\nex-automat\apps\supplier-invoice-worker\venv\Scripts\python.exe` |
| Arguments | `-m workers.main_worker` |
| AppDirectory | `C:\Deployment\nex-automat\apps\supplier-invoice-worker` |
| Start Type | SERVICE_AUTO_START |
| AppRestartDelay | 5000 ms |

**Task Queue:** `supplier-invoice-queue`

### NEX-Polling-Scheduler

| Parameter | Hodnota |
|-----------|---------|
| Service Name | `NEX-Polling-Scheduler` |
| Display Name | `NEX Polling Scheduler` |
| Description | Email polling scheduler for invoice workflows |
| Executable | `C:\Deployment\nex-automat\apps\supplier-invoice-worker\venv\Scripts\python.exe` |
| Arguments | `-m scheduler.polling_scheduler` |
| AppDirectory | `C:\Deployment\nex-automat\apps\supplier-invoice-worker` |
| Start Type | SERVICE_AUTO_START |
| AppRestartDelay | 5000 ms |

**Polling Interval:** 300 sekúnd (5 minút)

### Existujúce služby (predtým nasadené)

| Service Name | Display Name | Cesta |
|--------------|--------------|-------|
| NEXAutomat | NEX Automat v2.0 - Supplier Invoice... | `C:\Deployment\nex-automat\` |
| SupplierInvoiceLoader | (stará verzia) | `C:\invoice-loader\` |
| CloudflaredMagerstav | Cloudflare Tunnel | `C:\invoice-loader\` |

---

## Správa služieb

### Zobrazenie stavu

```powershell
# Všetky NEX služby
Get-Service "NEX-*" | Select-Object Name, Status, DisplayName

# Všetky NSSM služby
Get-WmiObject win32_service | Where-Object {$_.PathName -like "*nssm*"} | Select-Object Name, State
```

### Štart/Stop/Restart

```powershell
# Pomocou NSSM
C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe start NEX-Temporal-Server
C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe stop NEX-Invoice-Worker
C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe restart NEX-Polling-Scheduler

# Pomocou PowerShell
Start-Service "NEX-Temporal-Server"
Stop-Service "NEX-Invoice-Worker"
Restart-Service "NEX-Polling-Scheduler"
```

### Editácia služby

```powershell
# GUI editor
C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe edit NEX-Invoice-Worker

# Zmena parametra
C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe set NEX-Invoice-Worker AppRestartDelay 10000
```

### Odstránenie služby

```powershell
# Najprv zastav
C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe stop NEX-Invoice-Worker

# Potom odstráň
C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe remove NEX-Invoice-Worker confirm
```

---

## Temporal CLI príkazy

### Server

```powershell
# Manuálny štart (development)
C:\Temporal\cli\temporal.exe server start-dev --db-filename C:\Temporal\data\temporal.db --ui-port 8233

# Verzia
C:\Temporal\cli\temporal.exe --version
```

### Workflows

```powershell
# Zoznam workflows
C:\Temporal\cli\temporal.exe workflow list

# Detail workflow
C:\Temporal\cli\temporal.exe workflow describe --workflow-id <WORKFLOW_ID>

# Zrušenie workflow
C:\Temporal\cli\temporal.exe workflow cancel --workflow-id <WORKFLOW_ID>
```

### Namespaces

```powershell
# Zoznam namespaces
C:\Temporal\cli\temporal.exe operator namespace list
```

---

## Prístupy a URL

| Služba | URL | Poznámka |
|--------|-----|----------|
| Temporal UI | http://localhost:8233 | Web dashboard |
| Temporal Server | localhost:7233 | gRPC endpoint |
| FastAPI Invoice Loader | http://localhost:8000 | REST API |
| Cloudflare Tunnel | https://magerstav-invoices.icc.sk | Externý prístup |

---

## Konfigurácia

### .env súbor (supplier-invoice-worker)

```env
# Temporal
TEMPORAL_HOST=localhost
TEMPORAL_PORT=7233

# IMAP (Gmail OAuth2)
IMAP_HOST=imap.gmail.com
IMAP_PORT=993
IMAP_USER=magerstavinvoice@gmail.com

# FastAPI
FASTAPI_URL=http://localhost:8000

# Polling
POLL_INTERVAL_SECONDS=300
```

### Gmail OAuth2 tokeny

Súbor: `C:\Deployment\nex-automat\apps\supplier-invoice-worker\.gmail_tokens.json`

---

## Diagnostika

### Test pripojenia na Temporal

```powershell
cd C:\Deployment\nex-automat\apps\supplier-invoice-worker
.\venv\Scripts\Activate.ps1

# Test temporalio
python -c "import temporalio; print('Temporalio OK:', temporalio.__version__)"

# Test pripojenia
python -c "import asyncio; from temporalio.client import Client; asyncio.run(Client.connect('localhost:7233')); print('Temporal connection OK')"
```

### Test portov

```powershell
Test-NetConnection -ComputerName localhost -Port 7233
Test-NetConnection -ComputerName localhost -Port 8233
Test-NetConnection -ComputerName localhost -Port 8000
```

### Kontrola logov

```powershell
# NSSM logy (ak sú nakonfigurované)
Get-Content "C:\Deployment\nex-automat\logs\temporal-server.log" -Tail 50
Get-Content "C:\Deployment\nex-automat\logs\invoice-worker.log" -Tail 50
```

---

## Workflow architektúra

```
┌─────────────────────┐
│  Polling Scheduler  │ (každých 300s)
└──────────┬──────────┘
           │ spúšťa
           ▼
┌─────────────────────┐
│ InvoiceProcessing   │
│     Workflow        │
└──────────┬──────────┘
           │ orchestruje
           ▼
┌─────────────────────────────────────────────┐
│              Activities                      │
├─────────────┬─────────────┬─────────────────┤
│ fetch_emails│process_email│ send_to_loader  │
│  (Gmail)    │  (parse)    │   (FastAPI)     │
└─────────────┴─────────────┴─────────────────┘
```

---

## Dôležité poznámky

1. **64-bit Python pre Worker** - Temporalio SDK vyžaduje 64-bit Python kvôli Rust kompilácii
2. **32-bit Python pre FastAPI** - NEX Genesis kompatibilita (Btrieve)
3. **SQLite persistence** - Development/test režim, pre production zvážiť PostgreSQL
4. **n8n paralelný beh** - n8n stále beží, Temporal je v testovacom režime
5. **Auto-restart** - Všetky služby sa automaticky reštartujú pri zlyhaní (5s delay)

---

## História nasadenia

| Dátum | Akcia | Poznámka |
|-------|-------|----------|
| 2025-12-20 | Initial deployment | Temporal Server, Worker, Scheduler |
| 2025-12-20 | NSSM services created | 3 nové služby |
| 2025-12-20 | First workflows | 2 Completed v Temporal UI |