# Init Prompt - Magerstav Sync & Testing Completion

**Project:** NEX Automat v2.0 - Supplier Invoice Loader  
**Customer:** Magerstav s.r.o.  
**Current Progress:** 90% (Production Fixed, Development OUT OF SYNC)  
**Last Session:** Go-Live Testing - PARTIAL (2025-12-02)  
**This Session:** CRITICAL - Sync Development + Complete Testing  

---

## CRITICAL SITUATION - MUST READ

**WORKFLOW VIOLATION OCCURRED:**

- Fixes boli aplikovane priamo v Production (ad-hoc)
- Development je OUT OF SYNC s Production
- Dalsi deployment prepise production fixes
- MUST FIX FIRST pred pokracovanim testingu

---

## Quick Context

### Production (Magerstav Server) - WORKING

**Status:** Service bezi, duplicate detection fixed

- NEXAutomat service: Running on port 8001
- API: https://magerstav-invoices.icc.sk/health (200 OK)
- Database: SQLite (6 invoices) + PostgreSQL staging (1 invoice)
- n8n workflow: ACTIVE, processing emails

**Applied Fixes (ad-hoc in Production):**

```python
# main.py line 298-301: Duplicate detection
is_duplicate_found = database.is_duplicate(
    file_hash=file_hash,
    customer_name=None  # Fixnute - ignoruje customer name mismatch
)

# main.py line ~530: Port
port=8001  # Fixnute z 8000
```

### Development (ICC Server) - OUT OF SYNC

**Status:** Chybaju production fixes

**Location:** `C:\Development\nex-automat\apps\supplier-invoice-loader\main.py`

**Missing fixes:**

1. `customer_name=None` v duplicate check
2. Early return pre duplicates
3. Port verification (pravdepodobne ma 8001, ale treba overit)

---

## System Architecture

**Flow Diagram:**

```
ICC Server (n8n)
  |
  +-- n8n Workflow: ACTIVE
  |   - Email: magerstavinvoice@gmail.com
  |   - API Key: magerstav-PWjo...
  |
  +-- Development (OUT OF SYNC)
      - Location: C:\Development\nex-automat
      - Status: Missing production fixes
  |
  | (HTTPS POST via Cloudflare Tunnel)
  |
  v
Magerstav Server (Production)
  |
  +-- NEXAutomat Service
  |   - Port: 8001
  |   - Status: WORKING
  |   - Duplicate detection: FIXED
  |
  +-- Databases
      - SQLite: 6 invoices
      - PostgreSQL staging: 1 invoice
```

---

## Session Goals

### Priority 1: SYNC Development with Production (BLOCKING)

**Objective:** Zosynchronizovat Production fixes do Development pred dalsim deploymentom

#### Task 1.1: Overit Production State

**Na Magerstav serveri:**

```powershell
# Zobrazit production main.py kriticke sekcie
Select-String -Path "C:\Deployment\nex-automat\apps\supplier-invoice-loader\main.py" -Pattern "is_duplicate|port=" -Context 1,2
```

**Ocakavane:**

- `customer_name=None` v duplicate check
- `port=8001` v uvicorn.run

#### Task 1.2: Sync do Development

**Na ICC serveri:**

1. Zalohovat aktualny Development main.py
2. Prepisat s Production verziou
3. Overit zmeny
4. Testovat lokalne (ak mozne)

**Metody:**

- **Option A:** Manualny copy (RDP/network share)
- **Option B:** Python script na sync
- **Option C:** Git pull/push (ak uz commitnute)

#### Task 1.3: Git Commit

```bash
git add apps/supplier-invoice-loader/main.py
git commit -m "fix: Duplicate detection and port configuration for Magerstav deployment"
git push origin main
```

**Commit message je prilozeny v separatnom artifacte.**

---

### Priority 2: Complete Testing (Unblocked after Sync)

#### Test 1.3: Duplicate Detection - RETEST

**Prerequisite:** Development synced

**Steps:**

1. Odoslat novu fakturu -> Ocakavam SUCCESS
2. Odoslat rovnaku fakturu -> Ocakavam `{"duplicate": true}`
3. Overit databazu: Stale len 1 zaznam

**Success Criteria:**

- Prvy pokus: Creates record
- Druhy pokus: Returns `{"success": true, "duplicate": true}`
- Database: Len 1 zaznam (ziadny duplicate insert)

#### Test 1.4: Large PDF Handling

**Objective:** Overit spracovanie vacsich PDF (5-10 MB)

**Steps:**

1. Najst/vytvorit PDF 5-10 MB
2. Odoslat na magerstavinvoice@gmail.com
3. Monitorovat n8n execution time
4. Overit database record

**Success Criteria:**

- Execution completes within 120s
- Database record created
- No timeout errors

---

### Priority 3: Production Validation

#### Validation 3.1: Health Check Availability

**From external network:**

```bash
curl https://magerstav-invoices.icc.sk/health
```

**Expected:** `{"status":"healthy","timestamp":"..."}`

#### Validation 3.2: Database Integrity

**On Magerstav server:**

```sql
-- Check table structure
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

-- Check for duplicates
SELECT file_hash, COUNT(*) 
FROM invoices 
GROUP BY file_hash 
HAVING COUNT(*) > 1;
```

#### Validation 3.3: Service Auto-Start

**Test after reboot:**

```powershell
# Check service StartType
Get-Service NEXAutomat,postgresql-x64-15,CloudflaredMagerstav | 
    Select-Object Name, Status, StartType

# Expected: All Automatic, All Running
```

---

### Priority 4: Production Handoff

#### Task 4.1: Update Error Notification Email

**Current:** it@magerstav.sk (needs confirmation)

**In n8n workflow:**

1. Edit node: "Send Error Notification"
2. Update "Send To" field
3. Save workflow

#### Task 4.2: Customer Onboarding Guide

**Create documentation:**

- How to forward supplier invoices to magerstavinvoice@gmail.com
- Expected email format
- How to check if invoice was processed
- What to do if error occurs
- Contact for support

#### Task 4.3: Export Workflow Backup

**Export n8n workflow to:**

```
apps/supplier-invoice-loader/n8n-workflows/n8n-SupplierInvoiceEmailLoader.json
```

---

## Critical Files

### Production (Magerstav Server)

```
C:\Deployment\nex-automat\apps\supplier-invoice-loader\
|-- main.py                           [HAS FIXES]
|-- config\
|   |-- config_customer.py
|   +-- invoices.db                   [SQLite database]
+-- src\
    +-- database\
        +-- database.py
```

### Development (ICC Server)

```
C:\Development\nex-automat\apps\supplier-invoice-loader\
|-- main.py                           [NEEDS SYNC]
|-- config\
|   +-- config_customer.py
+-- src\
    +-- database\
        +-- database.py
```

---

## Connection Details

### NEX Automat API

- Public URL: https://magerstav-invoices.icc.sk
- Endpoint: /invoice (POST)
- Health: /health (GET)
- API Key: magerstav-PWjoMerqzZc-EJZPuT0wN9iBzM8eK_t1Rh-HFZT4IbY

### n8n Workflow

- Service: n8n-service (LocalSystem)
- Web UI: http://localhost:5678 (ICC server)
- User: automation@isnex.ai
- Workflow: n8n-SupplierInvoiceEmailLoader
- Email: magerstavinvoice@gmail.com

### Database

- SQLite: `C:\Deployment\nex-automat\apps\supplier-invoice-loader\config\invoices.db`
- PostgreSQL: localhost:5432/invoice_staging
- User: postgres
- Password: Nex1968

---

## Known Issues (from Last Session)

### Critical (Blocking)

1. **Development/Production out of sync** - MUST FIX FIRST

### Architecture Decision Needed

**Topic:** Multi-tenant vs Single-tenant design

**Current Implementation:**

```python
def is_duplicate(file_hash: str, customer_name: Optional[str] = None) -> bool:
    # Checks file_hash + customer_name combination
```

**Problem:**

- Config: "Magerstav s.r.o."
- Database: "MAGERSTAV, spol. s r.o." (from PDF)
- Never match -> Duplicate check fails

**Current Fix:**

```python
is_duplicate_found = database.is_duplicate(
    file_hash=file_hash,
    customer_name=None  # Skip customer check
)
```

**User Decision:**

> "V ziadnom pripade nechcem miesat zakaznikov. Kazdy zakaznik bude mat vlastny workflow."

**Implication:** Single-tenant approach is correct for this deployment

**Future Consideration:** Should we simplify database.py to remove multi-tenant logic?

---

## Success Criteria

### Must Have (Blocking)

- Development synced with Production fixes
- Git commit with production changes
- Test 1.3: Duplicate detection works
- Test 1.4: Large PDF handling works
- All services auto-start on reboot

### Should Have (Important)

- Health check accessible from internet
- Database integrity verified
- Error notification email updated
- Customer onboarding guide created

### Nice to Have (Optional)

- Monitoring/alerting configured
- Workflow backup exported
- Performance baseline established
- Documentation complete

---

## Troubleshooting Reference

### Service Won't Start

```powershell
# Check logs
Get-Content C:\Deployment\nex-automat\logs\service-stderr.log -Tail 50

# Check port conflicts
netstat -ano | findstr :8001

# Manual start for debugging
cd C:\Deployment\nex-automat\apps\supplier-invoice-loader
C:\Deployment\nex-automat\venv32\Scripts\python.exe main.py
```

### Duplicate Detection Fails

```powershell
# Verify customer_name=None in main.py
Select-String -Path main.py -Pattern "is_duplicate" -Context 0,3

# Check database for existing hashes
cd C:\Deployment\nex-automat\apps\supplier-invoice-loader\config
C:\Deployment\nex-automat\venv32\Scripts\python.exe -c "import sqlite3; conn = sqlite3.connect('invoices.db'); cursor = conn.cursor(); cursor.execute('SELECT file_hash FROM invoices'); print([r[0] for r in cursor.fetchall()])"
```

---

## Session Workflow

**Step 1:** Overit production state  
**Step 2:** Sync fixes do Development  
**Step 3:** Test lokalne (optional)  
**Step 4:** Git commit & push  
**Step 5:** Complete testing suite  
**Step 6:** Production validation  
**Step 7:** Handoff documentation

---

**Session Type:** Critical Sync + Testing Completion  
**Expected Duration:** 2-3 hours  
**Blocking Issues:** Development/Production out of sync  
**Status:** CRITICAL - Must sync first

---

**Last Updated:** 2025-12-02  
**Previous Session:** Go-Live Testing (Partial)  
**This Session:** Sync & Complete Testing