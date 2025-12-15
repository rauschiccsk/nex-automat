# Deployment Guide - NEX Automat

Complete guide for deploying NEX Automat to production.

**Customer:** [CUSTOMER_NAME]  
**Target Date:** [YYYY-MM-DD]  
**Version:** [VERSION]

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Infrastructure Setup](#infrastructure-setup)
3. [Application Deployment](#application-deployment)
4. [Service Installation](#service-installation)
5. [Verification & Testing](#verification--testing)
6. [Go-Live Checklist](#go-live-checklist)
7. [Rollback Procedures](#rollback-procedures)

---

## Prerequisites

### System Requirements

- **OS:** Windows Server 2019/2022 or Windows 10/11 Pro
- **CPU:** 2+ cores
- **RAM:** 4+ GB
- **Disk:** 50+ GB free space
- **Network:** Local network access to NEX Genesis Server

### Software Requirements

- **Python:** 3.13 32-bit
- **PostgreSQL:** 15+
- **NEX Genesis:** Latest version
- **NSSM:** 2.24 (included in deployment)

### Access Requirements

- **Administrator privileges** for:
  - Service installation
  - PostgreSQL configuration
  - File system permissions
- **PostgreSQL admin** access for:
  - Database creation
  - User management
- **NEX Genesis** access for:
  - API integration
  - Data directory access

---

## Infrastructure Setup

### Step 1: PostgreSQL Installation

**If not already installed:**

1. Download PostgreSQL 15+ from https://www.postgresql.org/download/windows/
2. Run installer: `postgresql-15-windows-x64.exe`
3. Configuration:
   - Port: **5432** (default)
   - Superuser: **postgres**
   - Password: **[secure password]**
   - Locale: **Slovak** or **English**

**Verify installation:**

```powershell
Get-Service postgresql*
# Should show: Running
```

### Step 2: Database Setup

```powershell
# 1. Create database
psql -U postgres -c "CREATE DATABASE invoice_staging;"

# 2. Create tables (run from deployment package)
cd C:\Deployment\nex-automat\apps\supplier-invoice-loader
..\..\venv32\Scripts\python.exe -m database.migrations
```

**Verify:**

```sql
psql -U postgres -d invoice_staging

-- List tables
\dt

-- Should see required tables
```

### Step 3: Create Storage Directories

```powershell
# Create all required directories
$dirs = @(
    "C:\NEX\IMPORT\pdf",
    "C:\NEX\IMPORT\xml",
    "C:\NEX\IMPORT\temp",
    "C:\NEX\IMPORT\archive",
    "C:\NEX\IMPORT\error",
    "C:\Deployment\nex-automat\logs",
    "C:\Deployment\nex-automat\backups"
)

foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Path $dir -Force
    Write-Host "Created: $dir"
}
```

### Step 4: Environment Variables

```powershell
# Set PostgreSQL password
setx POSTGRES_PASSWORD "your_secure_password"

# Verify
$env:POSTGRES_PASSWORD
# Should display your password

# NOTE: May need to restart PowerShell for changes to take effect
```

---

## Application Deployment

### Step 1: Prepare Deployment Package

**From Development:**

```powershell
# Navigate to development repo
cd C:\Development\nex-automat

# Run deployment script
python scripts\deploy_to_production.py

# This creates:
# - C:\Deployment\nex-automat\
# - Copies all application files
# - Creates virtual environment
# - Installs dependencies
```

**Manual Deployment (if script unavailable):**

```powershell
# 1. Create deployment directory
New-Item -ItemType Directory -Path "C:\Deployment\nex-automat" -Force

# 2. Copy files
Copy-Item -Recurse "C:\Development\nex-automat\apps" "C:\Deployment\nex-automat\"
Copy-Item -Recurse "C:\Development\nex-automat\packages" "C:\Deployment\nex-automat\"
Copy-Item -Recurse "C:\Development\nex-automat\scripts" "C:\Deployment\nex-automat\"

# 3. Create virtual environment
cd C:\Deployment\nex-automat
python -m venv venv32

# 4. Activate and install dependencies
venv32\Scripts\activate
pip install -r apps\supplier-invoice-loader\requirements.txt

# 5. Install shared packages
pip install -e packages\nex-shared
pip install -e packages\nexdata
```

### Step 2: Configure Application

```powershell
cd C:\Deployment\nex-automat

# Edit production config
notepad apps\supplier-invoice-loader\config\config.yaml
```

**Key settings:**

```yaml
customer: [CUSTOMER_CODE]

storage:
  pdf_path: C:/NEX/IMPORT/pdf
  xml_path: C:/NEX/IMPORT/xml
  temp_path: C:/NEX/IMPORT/temp
  archive_path: C:/NEX/IMPORT/archive
  error_path: C:/NEX/IMPORT/error

database:
  use_postgresql_staging: true
  postgres:
    host: localhost
    port: 5432
    database: invoice_staging
    user: postgres
    # Password from environment variable POSTGRES_PASSWORD

nex_api:
  base_url: http://localhost:8080/api
  # api_key: ""  # Leave empty for local

logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### Step 3: Validate Configuration

```powershell
# Validate config file
python scripts\validate_config.py

# Expected output:
# ✅ Configuration valid
# ✅ All required settings present
# ✅ Paths exist
# ✅ Database connection successful
```

---

## Service Installation

### Step 1: Install NSSM

```powershell
cd C:\Deployment\nex-automat
venv32\Scripts\activate

# Download and install NSSM
python scripts\install_nssm.py

# Verify
tools\nssm\win32\nssm.exe version
# Should show: NSSM 2.24
```

### Step 2: Create Windows Service

**⚠️ MUST RUN AS ADMINISTRATOR**

```powershell
# Open PowerShell AS ADMINISTRATOR
# Navigate to deployment
cd C:\Deployment\nex-automat
venv32\Scripts\activate

# Create service
python scripts\create_windows_service.py

# Expected output:
# ✅ Service created successfully
# Service Name: NEX-Automat-Loader
# Display Name: NEX Automat - Supplier Invoice Loader
```

### Step 3: Configure Service Auto-Restart

```powershell
# Set immediate restart on failure (AS ADMINISTRATOR)
C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe set NEX-Automat-Loader AppRestartDelay 0

# Verify
C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe get NEX-Automat-Loader AppRestartDelay
# Should show: 0
```

### Step 4: Start Service

```powershell
# Start service (AS ADMINISTRATOR)
python scripts\manage_service.py start

# or direct NSSM
C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe start NEX-Automat-Loader

# Check status
python scripts\manage_service.py status
# Should show: SERVICE_RUNNING
```

---

## Verification & Testing

### 1. Service Status

```powershell
# Check service is running
python scripts\manage_service.py status

# Expected: SERVICE_RUNNING
```

### 2. API Health Check

```powershell
# Test API
Invoke-WebRequest -Uri http://localhost:8000/health

# Expected response:
# StatusCode: 200
# Content: {"status":"healthy","timestamp":"..."}
```

### 3. Check Logs

```powershell
# View recent logs
python scripts\manage_service.py logs

# Should see:
# Starting Supplier Invoice Loader
# Customer: [CUSTOMER_CODE]
# PostgreSQL: localhost:5432/invoice_staging
# INFO: Uvicorn running on http://0.0.0.0:8000

# No errors!
```

### 4. Database Connection

```powershell
# Test database
python scripts\test_database_connection.py

# Expected:
# ✅ PostgreSQL connection successful
# ✅ Database 'invoice_staging' accessible
# ✅ Tables found
```

### 5. API Endpoints

```powershell
# API Documentation
Start-Process http://localhost:8000/docs

# Test endpoints:
Invoke-WebRequest -Uri http://localhost:8000/api/invoices
Invoke-WebRequest -Uri http://localhost:8000/api/staging/invoices
```

### 6. Auto-Restart Test

```powershell
# Get current PID
$pid = (netstat -ano | findstr :8000 | Select-Object -First 1) -replace '\s+', ' ' | ForEach-Object { ($_ -split ' ')[-1] }

# Kill process
taskkill /F /PID $pid

# Wait 5 seconds
Start-Sleep -Seconds 5

# Verify restarted
python scripts\manage_service.py status
Invoke-WebRequest -Uri http://localhost:8000/health

# Expected: Both should work (service auto-restarted)
```

### 7. File Processing Test

```powershell
# Create test invoice file
Copy-Item "test-data\sample-invoice.xml" "C:\NEX\IMPORT\xml\"

# Monitor logs for processing
python scripts\manage_service.py tail

# Should see file processed and moved to archive
```

---

## Go-Live Checklist

See [GO_LIVE_CHECKLIST.md](GO_LIVE_CHECKLIST.md) for detailed checklist.

---

## Rollback Procedures

### Quick Rollback (< 5 minutes)

**If critical issue in first hour:**

```powershell
# 1. Stop new service
python scripts\manage_service.py stop

# 2. Restore old version
Copy-Item -Recurse "backups\loader-[DATE]" "apps\supplier-invoice-loader" -Force

# 3. Start service
python scripts\manage_service.py start

# 4. Verify
python scripts\manage_service.py status
Invoke-WebRequest -Uri http://localhost:8000/health
```

### Full Rollback (< 30 minutes)

**If issues persist:**

```powershell
# 1. Stop and remove service
C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe stop NEX-Automat-Loader
C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe remove NEX-Automat-Loader confirm

# 2. Restore database
psql -U postgres -d invoice_staging -f "backups\database-[DATE].sql"

# 3. Restore application
Remove-Item -Recurse "C:\Deployment\nex-automat" -Force
Copy-Item -Recurse "backups\full-backup-[DATE]" "C:\Deployment\nex-automat"

# 4. Recreate service
cd C:\Deployment\nex-automat
venv32\Scripts\activate
python scripts\create_windows_service.py

# 5. Start and verify
python scripts\manage_service.py start
python scripts\manage_service.py logs
```

---

## Backup Procedures

### Before Deployment

```powershell
# 1. Backup database
pg_dump -U postgres -d invoice_staging -F c -f "backups\database-$(Get-Date -Format 'yyyyMMdd').backup"

# 2. Backup application
Copy-Item -Recurse "apps\supplier-invoice-loader" "backups\loader-$(Get-Date -Format 'yyyyMMdd')"

# 3. Backup configuration
Copy-Item "apps\supplier-invoice-loader\config\config.yaml" "backups\config-$(Get-Date -Format 'yyyyMMdd').yaml"

# 4. Create full backup
Compress-Archive -Path "C:\Deployment\nex-automat\*" -DestinationPath "backups\full-backup-$(Get-Date -Format 'yyyyMMdd').zip"
```

---

## Post-Deployment Tasks

### Immediate (Day 1)

1. Monitor service continuously for first 8 hours
2. Review all logs every hour
3. Test all major workflows
4. Verify data accuracy in NEX Genesis
5. Be ready for quick rollback

### Short-term (Week 1)

1. Daily status reports
2. Performance monitoring
3. Error rate tracking
4. Customer feedback collection
5. Minor tuning/optimization

### Long-term (Month 1)

1. Weekly performance reviews
2. Optimization opportunities
3. Feature requests
4. Integration improvements
5. Documentation updates

---

## Support & Escalation

### Level 1: Self-Service

- Check logs: `python scripts\manage_service.py logs`
- Review TROUBLESHOOTING.md
- Restart service: `python scripts\manage_service.py restart`

### Level 2: Remote Support

- Collect diagnostic report
- Email to: [SUPPORT_EMAIL]
- Include: logs, config, error messages

### Level 3: On-Site Support

- Critical issues only
- Schedule via email/phone
- Preparation: full system access

---

## Contacts

**Developer:** [DEVELOPER_NAME]  
**Company:** [COMPANY_NAME]  
**Email:** [SUPPORT_EMAIL]  
**Phone:** [PHONE_NUMBER]

**Customer:** [CUSTOMER_NAME]  
**Contact:** [CUSTOMER_CONTACT]  
**Email:** [CUSTOMER_EMAIL]

---

**Document Version:** 1.0  
**Last Updated:** 2025-12-15
