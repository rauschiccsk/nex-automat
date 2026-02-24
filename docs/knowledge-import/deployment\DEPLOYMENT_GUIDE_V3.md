# NEX Automat v3.0 - Complete Deployment Guide

**Version:** 3.0.0
**Date:** 2025-12-23
**Status:** ✅ PRODUCTION READY

---

## Prehľad zmien v3.0

| Zmena | Popis |
|-------|-------|
| PyQt5 → PySide6 | GUI migrácia na Qt6 |
| psycopg2 → pg8000 | PostgreSQL driver pre 32-bit kompatibilitu |
| n8n → Temporal | Workflow orchestration (pripravené) |
| nex-staging package | Nový package pre PostgreSQL staging operácie |

---

## Pre-requisites na serveri

### Software Requirements

| Software | Verzia | Poznámka |
|----------|--------|----------|
| Windows Server | 2019/2022 | alebo Windows 10/11 Pro |
| Python 32-bit | 3.12.x | Pre Btrieve DLL kompatibilitu |
| Python 64-bit | 3.12.x | Pre PySide6 GUI |
| PostgreSQL | 15.x+ | Staging databáza |
| Git | 2.40+ | Deployment |
| NSSM | 2.24 | Windows Service Manager |
| Pervasive PSQL | 11+ | Btrieve driver |

### Sieťové požiadavky

- Prístup k NEX Genesis serveru (Btrieve súbory)
- SMTP server pre notifikácie (voliteľné)
- LS API prístup pre email polling

---

## Krok 1: Inštalácia Python

### 1.1 Python 32-bit (pre btrieve-loader)

```powershell
# Stiahnuť z python.org
# DÔLEŽITÉ: Zvoliť "Customize installation"
# DÔLEŽITÉ: Zaškrtnúť "Add Python to PATH"
# Inštalovať do: C:\Python312-32\
```

### 1.2 Python 64-bit (pre GUI aplikácie)

```powershell
# Stiahnuť z python.org
# Inštalovať do: C:\Python312\
```

---

## Krok 2: PostgreSQL Setup

### 2.1 Inštalácia PostgreSQL

```powershell
# Stiahnuť PostgreSQL 15.x z postgresql.org
# Inštalovať s default nastaveniami
# Zapamätať si heslo pre postgres user!
```

### 2.2 Nastavenie Environment Variable

```powershell
# KRITICKÉ: Nastaviť POSTGRES_PASSWORD na Machine level
[System.Environment]::SetEnvironmentVariable("POSTGRES_PASSWORD", "VaseHeslo", "Machine")

# Reštartovať PowerShell pre načítanie premennej
```

### 2.3 Vytvorenie databázy

```powershell
# Otvoriť pgAdmin alebo psql
CREATE DATABASE supplier_invoice_staging;
```

---

## Krok 3: Deployment adresáre

### 3.1 Vytvorenie štruktúry

```powershell
# Hlavný deployment adresár
New-Item -ItemType Directory -Path "C:\Deployment\nex-automat" -Force

# NEX priečinky pre faktúry
New-Item -ItemType Directory -Path "C:\NEX\IMPORT\SUPPLIER-INVOICES" -Force
New-Item -ItemType Directory -Path "C:\NEX\IMPORT\SUPPLIER-STAGING" -Force
New-Item -ItemType Directory -Path "C:\NEX\IMPORT\SUPPLIER-ARCHIVE" -Force

# Logy
New-Item -ItemType Directory -Path "C:\Deployment\nex-automat\logs" -Force
```

---

## Krok 4: Git Clone

```powershell
cd C:\Deployment
git clone https://github.com/rauschiccsk/nex-automat.git
cd nex-automat
git checkout develop
```

---

## Krok 5: Virtual Environments

### 5.1 venv32 (pre btrieve-loader service)

```powershell
cd C:\Deployment\nex-automat

# Vytvorenie venv s 32-bit Python
C:\Python312-32\python.exe -m venv venv32

# Aktivácia
.\venv32\Scripts\Activate.ps1

# Inštalácia dependencies
pip install --upgrade pip
pip install -e packages/nex-staging
pip install -e packages/nex-shared
pip install -e apps/btrieve-loader

# Deaktivácia
deactivate
```

### 5.2 venv64 (pre GUI aplikácie)

```powershell
cd C:\Deployment\nex-automat

# Vytvorenie venv s 64-bit Python
C:\Python312\python.exe -m venv venv64

# Aktivácia
.\venv64\Scripts\Activate.ps1

# Inštalácia dependencies
pip install --upgrade pip
pip install -e packages/nex-staging
pip install -e packages/shared-pyside6
pip install PySide6

# Deaktivácia
deactivate
```

---

## Krok 6: Database Migration

### 6.1 Aplikovanie schémy

```powershell
cd C:\Deployment\nex-automat

# Aplikovať všetky migrácie
$migrations = @(
    "apps/btrieve-loader/database/migrations/001_supplier_invoice_staging.sql",
    "apps/btrieve-loader/database/migrations/002_add_nex_columns.sql",
    "apps/btrieve-loader/database/migrations/003_add_file_tracking_columns.sql"
)

foreach ($sql in $migrations) {
    if (Test-Path $sql) {
        .\venv32\Scripts\python.exe -c "
import pg8000.native
import os
conn = pg8000.native.Connection(
    host='localhost', 
    port=5432, 
    database='supplier_invoice_staging', 
    user='postgres', 
    password=os.environ['POSTGRES_PASSWORD']
)
sql = open('$sql').read()
conn.run(sql)
print('Applied: $sql')
conn.close()
"
    }
}
```

---

## Krok 7: Konfigurácia

### 7.1 config_customer.py

```powershell
# Upraviť apps/btrieve-loader/config/config_customer.py

# Nastaviť:
# - CUSTOMER_NAME
# - NEX_DATA_PATH (cesta k NEX Genesis STORES)
# - LS_API_KEY (pre email polling)
# - RECEIVED_DIR, STAGING_DIR, ARCHIVE_DIR
```

### 7.2 config.yaml

```powershell
# Upraviť apps/btrieve-loader/config/config.yaml

# Nastaviť:
# - database.host: localhost
# - database.port: 5432
# - database.database: supplier_invoice_staging
# - database.user: postgres
# - api.port: 8001
```

---

## Krok 8: Windows Service (NSSM)

### 8.1 Inštalácia NSSM

```powershell
# Stiahnuť NSSM z nssm.cc
# Rozbaliť do C:\Deployment\nex-automat\tools\nssm\
```

### 8.2 Vytvorenie služby

```powershell
$nssm = "C:\Deployment\nex-automat\tools\nssm\win64\nssm.exe"

# Inštalácia služby
& $nssm install NEXAutomat "C:\Deployment\nex-automat\venv32\Scripts\python.exe"
& $nssm set NEXAutomat AppParameters "C:\Deployment\nex-automat\apps\btrieve-loader\main.py"
& $nssm set NEXAutomat AppDirectory "C:\Deployment\nex-automat\apps\btrieve-loader"
& $nssm set NEXAutomat DisplayName "NEX Automat v3.0 - Supplier Invoice Loader"
& $nssm set NEXAutomat Description "Automated invoice processing system"
& $nssm set NEXAutomat Start SERVICE_AUTO_START
& $nssm set NEXAutomat AppStdout "C:\Deployment\nex-automat\logs\service-stdout.log"
& $nssm set NEXAutomat AppStderr "C:\Deployment\nex-automat\logs\service-stderr.log"
& $nssm set NEXAutomat AppRotateFiles 1
& $nssm set NEXAutomat AppRotateBytes 10485760

# Spustenie služby
Start-Service NEXAutomat
```

---

## Krok 9: GUI Shortcut

### 9.1 Vytvorenie zástupcu na ploche

```powershell
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:PUBLIC\Desktop\Supplier Invoice Staging.lnk")
$Shortcut.TargetPath = "C:\Deployment\nex-automat\venv64\Scripts\pythonw.exe"
$Shortcut.Arguments = '"C:\Deployment\nex-automat\apps\supplier-invoice-staging\app.py"'
$Shortcut.WorkingDirectory = "C:\Deployment\nex-automat\apps\supplier-invoice-staging"
$Shortcut.Description = "Supplier Invoice Staging v3.0"
$Shortcut.Save()
```

---

## Krok 10: Verifikácia

### 10.1 Test služby

```powershell
# Skontrolovať stav služby
Get-Service NEXAutomat

# Skontrolovať health endpoint
Invoke-RestMethod http://localhost:8001/health

# Sledovať logy
Get-Content C:\Deployment\nex-automat\logs\service-stdout.log -Tail 30 -Wait
```

### 10.2 Test GUI

```powershell
# Spustiť GUI
.\venv64\Scripts\python.exe apps\supplier-invoice-staging\app.py

# Overiť:
# - Okno sa otvorí bez chýb
# - Faktúry sa načítajú z DB
# - QuickSearch funguje
```

### 10.3 E2E Test

1. Poslať faktúru na nastavenú emailovú adresu
2. Sledovať logy - malo by sa objaviť:
   ```
   [OK] PDF saved: ...
   [OK] Data extracted: Invoice XXXXX
   [OK] Saved to SQLite: XXXXX
   [OK] PDF renamed: ...
   [OK] ISDOC XML generated: ...
   [OK] Saved to PostgreSQL staging: invoice_id=X
   [OK] PDF moved to staging: ...
   [OK] XML moved to staging: ...
   [OK] Updated file_status to 'staged' for invoice X
   ```
3. Otvoriť GUI - faktúra by mala byť viditeľná

---

## Troubleshooting

### Problém: "list index out of range" pri INSERT

**Príčina:** pg8000.native používa named parameters (`:p0`), nie positional (`$1`)

**Riešenie:** Skontrolovať že nex-staging package je aktuálny:
```powershell
pip install -e packages/nex-staging --force-reinstall
```

### Problém: "column X does not exist"

**Príčina:** Migrácie neboli aplikované

**Riešenie:** Aplikovať všetky SQL migrácie (pozri Krok 6)

### Problém: "Duplicate invoice detected"

**Príčina:** SQLite obsahuje staré záznamy

**Riešenie:**
```powershell
Remove-Item apps\btrieve-loader\config\invoices.db
Stop-Service NEXAutomat
Start-Service NEXAutomat
```

### Problém: Qt6 RDP warning

**Príčina:** Qt6 má problém s detekciou monitorov cez RDP

**Riešenie:** Aktualizovať app.py - pridať:
```python
import os
os.environ["QT_LOGGING_RULES"] = "qt.qpa.screen=false"
```

### Problém: Btrieve DLL not found

**Príčina:** Pervasive PSQL nie je nainštalovaný alebo nie je v PATH

**Riešenie:** 
1. Inštalovať Pervasive PSQL
2. Pridať do PATH: `C:\Program Files (x86)\Pervasive Software\PSQL\bin`

---

## Údržba

### Aktualizácia systému

```powershell
cd C:\Deployment\nex-automat
git pull
Stop-Service NEXAutomat
pip install -e packages/nex-staging --force-reinstall
Start-Service NEXAutomat
```

### Zálohovanie

```powershell
# PostgreSQL backup
pg_dump -U postgres supplier_invoice_staging > backup_$(Get-Date -Format "yyyyMMdd").sql

# SQLite backup
Copy-Item apps\btrieve-loader\config\invoices.db backup\
```

### Logy

```powershell
# Sledovanie logov
Get-Content logs\service-stdout.log -Tail 50 -Wait
Get-Content logs\service-stderr.log -Tail 50 -Wait
```

---

## Kontakty

- **Development:** ICC Komárno
- **Support:** support@icc.sk
- **Repository:** https://github.com/rauschiccsk/nex-automat