# Init Prompt - NEX Automat v2.1 Post-Production

**Project:** NEX Automat v2.0 - Supplier Invoice Processing  
**Customer:** Mágerstav s.r.o.  
**Current Version:** v2.1 (Production)  
**Status:** ✅ DEPLOYED AND OPERATIONAL  
**Last Session:** Production Go-Live & Bug Fixes (2025-12-02)  
**This Session:** Monitoring, Improvements, or Next Customer

---

## Quick Context

**NEX Automat v2.1** je úspešne nasadený v produkcii u zákazníka **Mágerstav s.r.o.**

### What It Does
- Automaticky spracováva dodávateľské faktúry z emailu
- Email workflow (n8n) → FastAPI → Database → ISDOC XML
- GUI aplikácia pre manuálny review faktúr
- PostgreSQL staging databáza pre integráciu s NEX Genesis

### Current Status
- **Production:** ✅ Running, 9 faktúr spracovaných, 0 chýb
- **Duplicate Detection:** ✅ Fixed and working
- **Desktop App:** ✅ Funkčná ikona "NEX - Správa faktúr"
- **Health Check:** ✅ https://magerstav-invoices.icc.sk/health (200 OK)

---

## System Architecture (Production)

```
ICC Server (n8n)
  │
  ├─ n8n Workflow: SupplierInvoiceEmailLoader
  │  - Email: magerstavinvoice@gmail.com
  │  - API Key: magerstav-PWjo...
  │
  │ (HTTPS POST via Cloudflare Tunnel)
  │
  ▼
Mágerstav Server (Production)
  │
  ├─ NEXAutomat Service (Port 8001)
  │  - Status: Running, Automatic
  │  - Duplicate Detection: FIXED ✅
  │
  ├─ Supplier Invoice Editor (PyQt5 GUI)
  │  - Desktop Shortcut: "NEX - Správa faktúr"
  │  - PostgreSQL Connection: Working ✅
  │
  ├─ Databases
  │  - SQLite: 9 invoices, 0 duplicates
  │  - PostgreSQL staging: 9 invoices
  │
  └─ Cloudflare Tunnel
     - Public: https://magerstav-invoices.icc.sk
     - Status: Active
```

---

## Recent Changes (v2.1)

### Critical Bug Fix - Duplicate Detection

**Problem:** Duplicate faktúry neboli detegované

**Root Cause:**
```python
# Multi-tenant logic v single-tenant prostredí
database.is_duplicate(
    file_hash=hash,
    customer_name=config.CUSTOMER_NAME  # ← Problém
)

# Porovnávalo:
# Config: "Magerstav s.r.o."
# PDF:    "MAGERSTAV, spol. s r.o."
# → Never matched → Duplicates NOT detected
```

**Solution Applied:**
```python
# main.py (line 300)
customer_name=None  # ← Fixed

# database.py (lines 119-155)
if customer_name is None:
    # Single-tenant: Check only file_hash
    cursor.execute("SELECT id FROM invoices WHERE file_hash = ?", (file_hash,))
else:
    # Multi-tenant: Check file_hash AND customer_name
    cursor.execute("SELECT id FROM invoices WHERE file_hash = ? AND customer_name = ?", ...)
```

**Testing:**
- ✅ New invoice → Processed
- ✅ Duplicate invoice → Detected, not inserted
- ✅ Database: 0 duplicates confirmed

### Desktop Application Deployed

**Setup:**
- Installed PyQt5 dependencies
- Created `config.yaml` (PostgreSQL connection)
- Desktop shortcut: "NEX - Správa faktúr"
- Status: ✅ Fully functional

---

## File Locations

### Production (Mágerstav Server)

```
C:\Deployment\nex-automat\
├── apps\
│   ├── supplier-invoice-loader\
│   │   ├── main.py                    [FIXED: line 300]
│   │   ├── src\database\database.py   [FIXED: lines 119-155]
│   │   ├── config\
│   │   │   ├── config_customer.py
│   │   │   └── invoices.db            [9 invoices, 0 duplicates]
│   │   └── data\
│   │       ├── pdf\                   [Invoice PDFs]
│   │       └── xml\                   [ISDOC XMLs]
│   │
│   └── supplier-invoice-editor\
│       ├── main.py
│       ├── config\
│       │   └── config.yaml            [PostgreSQL: invoice_staging]
│       └── logs\
│
└── venv32\                            [Python 3.13]
```

### Development (ICC Server)

```
C:\Development\nex-automat\
├── apps\
│   ├── supplier-invoice-loader\
│   │   ├── main.py                    [SYNCED ✅]
│   │   └── database\database.py       [SYNCED ✅]
│   │
│   └── supplier-invoice-editor\
│       └── config\config.yaml         [SYNCED ✅]
│
└── .git\
```

**Note:** Development uses `database/` but Production uses `src/database/` for loader

---

## Connection Details

### NEX Automat API
- **Public URL:** https://magerstav-invoices.icc.sk
- **Endpoints:**
  - GET /health (public)
  - POST /invoice (protected, X-API-Key)
  - GET /stats (protected)
- **API Key:** magerstav-PWjoMerqzZc-EJZPuT0wN9iBzM8eK_t1Rh-HFZT4IbY
- **Internal Port:** 8001

### n8n Workflow (ICC Server)
- **Web UI:** http://localhost:5678
- **User:** automation@isnex.ai
- **Workflow:** n8n-SupplierInvoiceEmailLoader
- **Email:** magerstavinvoice@gmail.com
- **Status:** Active

### PostgreSQL (Mágerstav Server)
- **Host:** localhost
- **Port:** 5432
- **Database:** invoice_staging
- **User:** postgres
- **Password:** Nex1968

### SQLite (Mágerstav Server)
- **Path:** C:\Deployment\nex-automat\apps\supplier-invoice-loader\config\invoices.db
- **Records:** 9 invoices
- **Duplicates:** 0

---

## Known Issues

### Minor Issues (Non-blocking)

**1. Git Sync Delays**
- `git pull` sometimes reports "Already up to date" when changes exist
- Workaround: Manual file transfer for critical deployments
- Impact: Low

**2. Config Files Not in Git**
- `config.yaml` in `.gitignore` (contains passwords)
- Workaround: Manual file transfer
- TODO: Create `config.yaml.example` template

### Architecture Considerations

**Single-Tenant vs Multi-Tenant:**
- Code has multi-tenant support (customer_name filtering)
- Currently bypassed with `customer_name=None`
- Decision: Keep for potential future use, or simplify?

---

## Possible Next Steps

### Option 1: Monitoring & Improvements (Mágerstav)

**Monitoring:**
- Setup Prometheus metrics collection
- Create Grafana dashboard
- Configure UptimeRobot for health check
- Add Slack/Teams notifications

**Automation:**
- Automated confirmation email after processing
- Daily summary email report
- Database backup automation

**Configuration:**
- Create `config.yaml.example` template
- Add configuration validation script
- Document deployment process

### Option 2: Next Customer Deployment (ANDROS)

**Pilot Customers:**
- ✅ Mágerstav s.r.o. (DEPLOYED)
- ⏳ ANDROS (Next)
- ⏳ ICC itself (Internal use)

**Deployment Steps:**
1. Create new n8n workflow for ANDROS
2. Setup dedicated email (e.g., androsinvoice@gmail.com)
3. Configure customer-specific config
4. Deploy to ANDROS server (or shared server)
5. Test complete flow
6. Customer training

### Option 3: NEX Genesis Integration

**Automated Sync:**
- Sync from PostgreSQL staging to NEX Genesis
- Bi-directional status tracking
- Error handling and retry logic
- Monitoring dashboard

**Requirements:**
- NEX Genesis API/database access
- Field mapping (staging → NEX Genesis)
- Transaction handling
- Rollback capability

### Option 4: Web Dashboard

**Features:**
- Web-based invoice viewer (alternative to PyQt5)
- Real-time statistics
- Invoice search and filtering
- Export functionality
- Multi-user access

**Tech Stack:**
- Frontend: React/Vue.js
- Backend: FastAPI (extend existing)
- Auth: JWT tokens
- Deployment: Same server or separate

---

## Success Criteria (Current Status)

### Must Have ✅
- [x] Production deployment successful
- [x] All services running and auto-start
- [x] Duplicate detection working
- [x] Health check accessible
- [x] Database integrity verified
- [x] Desktop application deployed
- [x] Customer documentation delivered

### Should Have ✅
- [x] Error notifications configured
- [x] n8n workflow backed up
- [x] Manual testing completed
- [x] Production validation passed

### Nice to Have (Future)
- [ ] Monitoring dashboard
- [ ] Automated alerts
- [ ] Performance metrics baseline
- [ ] Automated backups
- [ ] Second customer deployed

---

## Quick Commands

### Check Production Status (Mágerstav Server)

```powershell
# Service status
Get-Service NEXAutomat,postgresql-x64-15,CloudflaredMagerstav | Select-Object Name, Status, StartType

# Health check
curl https://magerstav-invoices.icc.sk/health

# Database stats
cd C:\Deployment\nex-automat\apps\supplier-invoice-loader\config
C:\Deployment\nex-automat\venv32\Scripts\python.exe -c "import sqlite3; conn = sqlite3.connect('invoices.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM invoices'); print(f'Total: {cursor.fetchone()[0]}'); cursor.execute('SELECT COUNT(*) FROM invoices GROUP BY file_hash HAVING COUNT(*) > 1'); print(f'Duplicates: {len(cursor.fetchall())}')"
```

### Restart Services

```powershell
Restart-Service NEXAutomat
Start-Sleep -Seconds 3
Get-Service NEXAutomat
```

### View Recent Logs

```powershell
Get-Content C:\Deployment\nex-automat\logs\service-stderr.log -Tail 50
```

---

## Troubleshooting

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

### Duplicate Detection Issues

```powershell
# Verify fix is applied
Select-String -Path "C:\Deployment\nex-automat\apps\supplier-invoice-loader\main.py" -Pattern "customer_name=None" -Context 2,2

Select-String -Path "C:\Deployment\nex-automat\apps\supplier-invoice-loader\src\database\database.py" -Pattern "if customer_name is None" -Context 2,5
```

### Desktop Application Won't Start

```powershell
# Test with console output (see errors)
cd C:\Deployment\nex-automat\apps\supplier-invoice-editor
C:\Deployment\nex-automat\venv32\Scripts\python.exe main.py

# Check config
Test-Path "config\config.yaml"
Get-Content "config\config.yaml"

# Check PostgreSQL connection
# (Connection test is automatic on app startup - check console output)
```

---

## Documentation References

### Customer Documentation
- **MAGERSTAV_ONBOARDING_GUIDE.md** - User guide, FAQ, contacts

### Technical Documentation
- **SESSION_NOTES.md** - Complete session history
- **PROJECT_MANIFEST.json** - Project structure
- **n8n-SupplierInvoiceEmailLoader.json** - Workflow backup

### Code Documentation
- Inline comments in main.py and database.py
- Fix scripts with explanations

---

## Contact Information

**Technical Support:**
- Email: rausch@icc.sk
- Error notifications: Automatic to rausch@icc.sk

**Customer:**
- Company: Mágerstav s.r.o.
- Email endpoint: magerstavinvoice@gmail.com

---

**Session Type:** Post-Production Monitoring / Next Feature / Next Customer  
**Expected Focus:** Based on user request  
**Status:** ✅ **PRODUCTION STABLE - READY FOR NEXT TASK**  

---

**Last Updated:** 2025-12-02 21:45  
**Previous Session:** Production Go-Live & Bug Fixes  
**Version:** v2.1  
**Release Date:** 2025-12-02