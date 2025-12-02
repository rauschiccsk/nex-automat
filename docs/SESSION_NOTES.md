# NEX Automat - Session Notes

**Date:** 2025-12-02  
**Project:** nex-automat  
**Location:** C:/Development/nex-automat  
**Session:** n8n Recovery & Workflow Setup - COMPLETE ✅

---

## 🎯 Session Goal

Obnoviť prístup do n8n a nakonfigurovať workflow pre Mágerstav deployment.

---

## 📋 Initial Problem

**User nemohol sa prihlásiť do n8n:**
- Error: "Wrong username or password"
- Zabudnutý email používateľa
- n8n beží ako Windows Service "n8n-service"

---

## ✅ Completed Tasks

### 1. n8n User Recovery ✅

**Problém:** Zabudnutý email pre login

**Riešenie:**
- Vytvorený script: `scripts/read_n8n_email.py`
- Prečítaný email z SQLite databázy
- Nájdený user: **automation@isnex.ai** (Zoltán Rausch)

**Database Location:** `C:\Users\ZelenePC\.n8n\database.sqlite`

---

### 2. Workflows Recovery ✅

**Problém:** Po prihlásení n8n UI ukazovalo prázdne (žiadne workflows)

**Root Cause Analysis:**
1. n8n beží ako Windows Service cez NSSM
2. Service account: **LocalSystem** (nie ZelenePC user)
3. LocalSystem má vlastný home directory:
   - 64-bit: `C:\Windows\System32\config\systemprofile\.n8n\`
   - **32-bit: `C:\Windows\SysWOW64\config\systemprofile\.n8n\`** ← používané
4. n8n je 32-bit Node.js → číta z SysWOW64
5. Databáza v SysWOW64 bola prázdna (nová inštancia)

**Discovery Process:**
- Script: `scripts/read_n8n_workflows.py` - overené 24 workflows v originálnej DB
- Script: `scripts/read_n8n_projects.py` - overený project "Zoltán Rausch"
- Zistené 3 databázy:
  - `C:\Users\ZelenePC\.n8n\` - 53.98 MB, 24 workflows ✅
  - `C:\Windows\System32\...\systemprofile\.n8n\` - 507 KB, prázdna
  - `C:\Windows\SysWOW64\...\systemprofile\.n8n\` - prázdna (active)

**Migration Solution:**
- Script: `scripts/migrate_n8n_database.py`
- Kopírovaná databáza z user profile do System32
- Zistené že n8n používa SysWOW64 (32-bit)
- Manuálne dokopírované do správnej lokácie

**Final Database Location:**
```
C:\Windows\System32\config\systemprofile\.n8n\database.sqlite (51.48 MB)
C:\Windows\SysWOW64\config\systemprofile\.n8n\database.sqlite (53.98 MB) ✅ ACTIVE
```

---

### 3. Credentials Decryption Fix ✅

**Problém:** Po migration všetky credentials hlásili "Needs first setup"

**Error:** "Credentials could not be decrypted. Different encryptionKey was used"

**Root Cause:**
- Credentials zašifrované s pôvodným encryption key
- n8n service nemal tento encryption key

**Riešenie:**
- Prečítaný encryption key z: `C:\Users\ZelenePC\.n8n\config`
- **Encryption Key:** `OpvW9Fyd3Wi0x3lJJtpPW0ULcyHeDdK7`
- Kopírovaný config file do:
  - `C:\Windows\System32\config\systemprofile\.n8n\config`
  - `C:\Windows\SysWOW64\config\systemprofile\.n8n\config`

**Result:**
- ✅ Všetky credentials dešifrované
- ✅ 8 credentials funkčných (IMAP, Gmail, Postgres, Telegram, Anthropic, Header Auth x2)
- ✅ 24 workflows viditeľných

---

### 4. Mágerstav Workflow Configuration ✅

**Target Workflow:** `n8n-SupplierInvoiceEmailLoader`

**Konfigurácia Overená:**

**A) Email Trigger (IMAP):**
- Credential: IMAP account ✅
- Email: **magerstavinvoice@gmail.com** ✅
- Mailbox: INBOX ✅
- Action: Mark as Read ✅
- Format: Resolved ✅
- Attachments: attachment_ prefix ✅

**B) HTTP Request Node:**
- URL: `https://magerstav-invoices.icc.sk/invoice` ✅
- Method: POST ✅
- Header: X-API-Key = `{{ $env.LS_API_KEY || 'CHANGE_ME_PRODUCTION_KEY' }}`
- Body: JSON payload with base64 PDF ✅

**C) Environment Variable Added:**
- Script: `scripts/add_n8n_api_key_env.py`
- Added `LS_API_KEY` to NSSM service
- **API Key:** `magerstav-PWjoMerqzZc-EJZPuT0wN9iBzM8eK_t1Rh-HFZT4IbY`
- Registry Path: `HKLM:\SYSTEM\CurrentControlSet\Services\n8n-service\Parameters\AppEnvironmentExtra`

**NSSM Service Environment:**
```
N8N_PORT=5678
N8N_HOST=0.0.0.0
LS_API_KEY=magerstav-PWjoMerqzZc-EJZPuT0wN9iBzM8eK_t1Rh-HFZT4IbY
```

**D) Error Notification:**
- Node: Send Error Notification
- Credential: Gmail account (OAuth2) ✅
- Recipient: it@magerstav.sk (needs update)
- Subject: "⚠️ Nerozpoznaná faktúra"
- Trigger: When email has no PDF attachment

**E) Workflow Status:**
- Active: ✅ YES
- Status: 🟢 ACTIVE
- Ready for testing: ✅ YES

---

## 📊 Final Configuration Summary

### n8n Service

**Service Name:** n8n-service  
**Manager:** NSSM (Non-Sucking Service Manager)  
**Executable:** `C:\Users\ZelenePC\AppData\Roaming\npm\n8n.cmd`  
**Parameters:** `start --tunnel`  
**Working Directory:** `C:\n8n-data`  
**Account:** LocalSystem  
**Status:** Running ✅

**Logs:**
- stdout: `C:\n8n-data\logs\n8n-output.log`
- stderr: `C:\n8n-data\logs\n8n-error.log`

**Environment Variables:**
```
N8N_PORT=5678
N8N_HOST=0.0.0.0
LS_API_KEY=magerstav-PWjoMerqzZc-EJZPuT0wN9iBzM8eK_t1Rh-HFZT4IbY
```

### n8n Database

**Active Database:** `C:\Windows\SysWOW64\config\systemprofile\.n8n\database.sqlite`  
**Size:** 53.98 MB  
**Workflows:** 24 total  
**Credentials:** 8 total  
**Encryption Key:** `OpvW9Fyd3Wi0x3lJJtpPW0ULcyHeDdK7`

**Projects:**
- Name: "Zoltán Rausch <automation@isnex.ai>"
- Type: personal
- Workflows: 24 (all in this project)

**User:**
- Email: automation@isnex.ai
- Name: Zoltán Rausch
- Role: project:personalOwner

### Mágerstav Workflow

**Workflow Name:** `n8n-SupplierInvoiceEmailLoader`  
**Workflow ID:** `yBsDIpw6oMs96hi6`  
**Status:** 🟢 ACTIVE  

**Email Monitoring:**
- Account: **magerstavinvoice@gmail.com**
- Protocol: IMAP
- Mailbox: INBOX
- Action: Mark as Read
- Polling: Continuous

**Processing Flow:**
1. Email Trigger (IMAP) → 2. Split PDF (Code Node) → 3. Has PDF? (Switch)
   - **Has PDF:** → HTTP Request → Mágerstav API
   - **No PDF:** → Send Error Notification → it@magerstav.sk

**API Integration:**
- Endpoint: https://magerstav-invoices.icc.sk/invoice
- Method: POST
- Authentication: X-API-Key header
- API Key: magerstav-PWjoMerqzZc-EJZPuT0wN9iBzM8eK_t1Rh-HFZT4IbY
- Payload: JSON with base64 PDF + metadata

---

## 🛠️ Scripts Created

### 1. read_n8n_email.py
**Purpose:** Read user email from n8n SQLite database  
**Location:** scripts/read_n8n_email.py  
**Usage:** `python scripts/read_n8n_email.py`  
**Result:** automation@isnex.ai

### 2. read_n8n_workflows.py
**Purpose:** Read workflows and credentials from n8n database  
**Location:** scripts/read_n8n_workflows.py  
**Usage:** `python scripts/read_n8n_workflows.py`  
**Result:** 24 workflows, 8 credentials

### 3. read_n8n_projects.py
**Purpose:** Read projects and workflow assignments  
**Location:** scripts/read_n8n_projects.py  
**Usage:** `python scripts/read_n8n_projects.py`  
**Result:** 1 project (personal) with 24 workflows

### 4. migrate_n8n_database.py
**Purpose:** Migrate database from user profile to LocalSystem profile  
**Location:** scripts/migrate_n8n_database.py  
**Features:**
- Stop/start n8n-service
- Backup current database
- Copy source database (53.98 MB)
- Validation and rollback support
**Result:** Database migrated to System32 (later manually to SysWOW64)

### 5. add_n8n_api_key_env.py
**Purpose:** Add LS_API_KEY environment variable to NSSM service  
**Location:** scripts/add_n8n_api_key_env.py  
**Features:**
- Read current NSSM environment
- Add LS_API_KEY with Mágerstav API key
- Update registry
- Restart service
**Result:** API key available to workflow via $env.LS_API_KEY

---

## 🔍 Key Learnings

### 1. Windows Services & User Profiles
- LocalSystem má vlastný home directory: `C:\Windows\System32\config\systemprofile\`
- 32-bit aplikácie používajú SysWOW64 namiesto System32
- n8n defaultne hľadá `.n8n` v home directory aktuálneho účtu

### 2. n8n Architecture
- SQLite databáza obsahuje workflows, credentials, executions
- Credentials sú zašifrované s encryption key (v config file)
- Bez správneho encryption key sa credentials nedajú dešifrovať
- Projects organizujú workflows (personal vs team projects)

### 3. NSSM Configuration
- Environment variables v registry: `AppEnvironmentExtra`
- Format: multiline string s `\n` separátormi
- Registry path: `HKLM:\SYSTEM\CurrentControlSet\Services\[service-name]\Parameters`
- Changes require service restart

### 4. 32-bit vs 64-bit Paths
- System32 = 64-bit executables
- SysWOW64 = 32-bit executables (Windows-on-Windows64)
- 32-bit Node.js používa SysWOW64 paths
- Critical pre správnu lokáciu databáz a konfiguračných súborov

---

## 📁 File Locations

### n8n Databases
```
C:\Users\ZelenePC\.n8n\database.sqlite              (53.98 MB - original)
C:\Windows\System32\config\systemprofile\.n8n\      (migrated, unused)
C:\Windows\SysWOW64\config\systemprofile\.n8n\      (53.98 MB - ACTIVE) ✅
```

### n8n Configuration
```
C:\Users\ZelenePC\.n8n\config                       (original encryption key)
C:\Windows\SysWOW64\config\systemprofile\.n8n\config (active) ✅
```

### n8n Service
```
Executable: C:\Users\ZelenePC\AppData\Roaming\npm\n8n.cmd
NSSM: C:\Tools\nssm\win64\nssm.exe
Working Dir: C:\n8n-data
Logs: C:\n8n-data\logs\
```

### Project Scripts
```
C:\Development\nex-automat\scripts\
├── read_n8n_email.py
├── read_n8n_workflows.py
├── read_n8n_projects.py
├── migrate_n8n_database.py
└── add_n8n_api_key_env.py
```

---

## ⚠️ Important Notes

### Encryption Key
**CRITICAL:** Encryption key musí byť zálohovaný!  
**Location:** `C:\Windows\SysWOW64\config\systemprofile\.n8n\config`  
**Key:** `OpvW9Fyd3Wi0x3lJJtpPW0ULcyHeDdK7`

Bez tohto kľúča sa credentials nedajú dešifrovať!

### Database Backup
**Before any changes:**
```powershell
Copy-Item "C:\Windows\SysWOW64\config\systemprofile\.n8n\database.sqlite" "backup-$(Get-Date -Format 'yyyyMMdd').sqlite"
```

### Service Management
```powershell
# Status
Get-Service n8n-service

# Stop/Start
Stop-Service n8n-service
Start-Service n8n-service

# Logs
Get-Content C:\n8n-data\logs\n8n-output.log -Tail 50
```

---

## 🚀 Next Session Tasks

### Priority 1: Complete Mágerstav Go-Live

**Current Status:**
- ✅ Server deployed (NEX Automat API running)
- ✅ Database ready (invoice_staging)
- ✅ Cloudflare Tunnel active (magerstav-invoices.icc.sk)
- ✅ n8n workflow configured and active
- ⏳ End-to-end testing pending

**Remaining Tasks:**

1. **Update Error Notification Email**
   - Current: it@magerstav.sk (generic)
   - Update to: správny kontaktný email

2. **End-to-End Testing**
   - Test 1: Happy Path (email with PDF invoice)
     - Send to: magerstavinvoice@gmail.com
     - Verify: n8n execution success
     - Verify: Database record created
     - Verify: NEX Automat logs
   
   - Test 2: Error Path (email without PDF)
     - Send to: magerstavinvoice@gmail.com
     - Verify: Alert email received
     - Verify: No database record created
   
   - Test 3: Duplicate Detection
     - Send same PDF twice
     - Verify: Second attempt marked as duplicate
   
   - Test 4: Large PDF Handling (5-10 MB)
     - Verify: Processing completes within timeout

3. **Validation & Monitoring**
   - Health check: https://magerstav-invoices.icc.sk/health
   - Database integrity check
   - Service auto-start verification
   - Log monitoring setup

4. **Production Handoff**
   - Customer onboarding guide
   - Operator email configuration
   - Support contact setup
   - Documentation handoff

### Priority 2: n8n Maintenance & Backup

1. **Backup Strategy**
   - Database: weekly backup to safe location
   - Encryption key: secure storage
   - Workflow export: JSON backups

2. **Monitoring Setup**
   - n8n execution monitoring
   - Service uptime monitoring
   - Error alerting

3. **Documentation**
   - n8n recovery procedure (this session documented)
   - Common troubleshooting guide
   - Environment variable reference

---

## 📊 Session Statistics

**Duration:** ~2.5 hours  
**Scripts Created:** 5  
**Database Migrations:** 2 (System32, SysWOW64)  
**Service Restarts:** 4  
**Workflows Recovered:** 24  
**Credentials Recovered:** 8  
**Status:** ✅ **COMPLETE SUCCESS**

---

## 🎯 Success Criteria - ALL MET ✅

- [x] n8n login recovered (email found)
- [x] Workflows visible (24 workflows)
- [x] Credentials decrypted (8 credentials)
- [x] Mágerstav workflow configured
- [x] IMAP email monitoring active (magerstavinvoice@gmail.com)
- [x] API integration configured (magerstav-invoices.icc.sk)
- [x] Environment variables set (LS_API_KEY)
- [x] Workflow active and ready for testing

---

**Last Updated:** 2025-12-02  
**Next Session:** Mágerstav Go-Live Completion & End-to-End Testing  
**Status:** 🎯 **READY FOR PRODUCTION TESTING**