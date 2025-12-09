# INIT PROMPT - NEX Automat v2.4

## PROJECT CONTEXT

**Projekt:** nex-automat  
**Typ:** Monorepo - Multi-customer SaaS for automated invoice processing  
**Development:** `C:\Development\nex-automat`  
**Deployment:** `C:\Deployment\nex-automat`  
**Python:** 3.13.7 (venv32)  
**Git Branch:** develop  
**Current Version:** v2.4 Phase 4 - COMPLETE

---

## CURRENT STATUS ✅

### Phase 4: NEX Genesis Product Enrichment - COMPLETE

**What Works:**
- ✅ Complete GSCAT model with BarCode @ offset 60
- ✅ EAN matching: 81.2% (target >65%)
- ✅ Re-processing: 168/207 items matched
- ✅ Unit tests: 108/108 passing
- ✅ Git: All changes committed and pushed
- ✅ Production (Mágerstav): NSSM service running perfectly

**Progress:** 6/6 criteria (100%)

---

## DEPLOYMENT CONFIGURATIONS

### Production (Mágerstav) - NSSM Service ✅

```
Service: NEX-Automat-Loader
Method: NSSM Windows Service
Account: LocalSystem
Path: C:\Deployment\nex-automat
Status: RUNNING - No issues
```

**Management:**
```powershell
net start/stop "NEX-Automat-Loader"
sc query "NEX-Automat-Loader"
```

### Test Server - Task Scheduler ⚠️

```
Task: NEX-Automat-Loader
Method: Windows Task Scheduler
User: DESKTOP-6AU0066\Server
Trigger: At system startup
Status: FUNCTIONAL (with limitations)
```

**Limitations:**
- Server has Winsock issues after attempted reset
- W3DBSMGR.EXE must be started manually before NEX Automat
- Server MUST NOT be rebooted (breaks Pervasive)

**Management:**
```powershell
# Start sequence
Start-Process "C:\PVSW\bin\W3DBSMGR.EXE"
Start-ScheduledTask -TaskName "NEX-Automat-Loader"

# Stop
Stop-ScheduledTask -TaskName "NEX-Automat-Loader"
```

---

## RECENT CHANGES

### Code Fixed (2025-12-09)

**BtrieveClient (btrieve_client.py):**
- PATH-based DLL loading prioritized
- Unicode emojis removed (Windows console compatibility)
- Debug output: [DEBUG], [SUCCESS], [ERROR]

**main.py:**
- Unicode emojis removed
- Replaced: ✅→[OK], ❌→[ERROR]

**Commit:**
```
"Fix: BtrieveClient DLL loading and Unicode encoding issues"
Status: Committed and pushed to develop
```

---

## CRITICAL KNOWLEDGE

### Issue: WinError 10106 (Test Server Only)

**Problem:**
```
OSError: [WinError 10106] The requested service provider 
could not be loaded or initialized
```

**Cause:**
- Windows service accounts (LocalSystem/NetworkService) have issues with asyncio `_overlapped` module on this specific test server
- NOT a code issue - server-specific problem
- Works perfectly on Mágerstav production

**Solution:**
- Test server: Use Task Scheduler instead of NSSM
- Production: Use NSSM (preferred method)

### Issue: Winsock/Pervasive (Test Server Only)

**What Happened:**
- Attempted `netsh winsock reset` to fix WinError 10106
- **This broke Pervasive SRDE engine** (Error 8520)
- System Restore was disabled - no rollback possible

**Current State:**
- Pervasive works when manually started
- Breaks after server reboot
- Requires manual W3DBSMGR.EXE startup

**DO NOT:**
- ❌ Reboot test server
- ❌ Run Winsock reset anywhere
- ❌ Modify network configuration without testing

---

## QUICK START COMMANDS

### Development Testing
```powershell
cd C:\Development\nex-automat
python -m pytest packages/nexdata/tests/ -v
```

### Start NEX Automat (Production)
```powershell
net start "NEX-Automat-Loader"
```

### Start NEX Automat (Test Server)
```powershell
Start-Process "C:\PVSW\bin\W3DBSMGR.EXE"
Start-Sleep -Seconds 5
Start-ScheduledTask -TaskName "NEX-Automat-Loader"
```

### Check Status
```powershell
# Port test
Test-NetConnection -ComputerName localhost -Port 8001

# API
Start-Process "http://localhost:8001/docs"

# Health check
curl http://localhost:8001/health
```

### View Logs
```powershell
type C:\Deployment\nex-automat\logs\service-stderr.log | Select-Object -Last 50
```

---

## PROJECT STRUCTURE

```
nex-automat/
├── apps/
│   ├── supplier-invoice-editor/      # PyQt5 desktop app
│   └── supplier-invoice-loader/      # FastAPI service (port 8001)
├── packages/
│   ├── nex-shared/                   # Shared models (FLAT structure)
│   └── nexdata/                      # Btrieve access layer
├── scripts/                          # Utility scripts
└── tools/                            # Claude Tools automation
```

**CRITICAL:** nex-shared uses FLAT structure:
- ✅ `packages/nex-shared/models/`
- ❌ NOT `packages/nex-shared/nex_shared/models/`

---

## DEVELOPMENT WORKFLOW

```
1. Development → Git → Deployment
2. All fixes via Development first
3. Test locally
4. Commit and push
5. Pull in Deployment
6. Restart service/task
```

**Git:**
```powershell
git add .
git commit -m "message"
git push
```

**Deployment:**
```powershell
cd C:\Deployment\nex-automat
git pull
```

---

## TESTING

### Unit Tests
```bash
python -m pytest packages/nexdata/tests/ -v
```
**Status:** 108/108 passing

### EAN Matching
```bash
python scripts/test_ean_lookup.py
```
**Result:** 81.2% (target: >65%)

### API Endpoints
```
http://localhost:8001/docs       # Swagger UI
http://localhost:8001/health     # Health check
```

---

## COMMON TASKS

### Add New Script
```python
# scripts/XX_description.py
# Temporary scripts: numbered 01-99
# Permanent scripts: not numbered
```

### Update Dependencies
```powershell
cd C:\Development\nex-automat
pip install -r requirements.txt
```

### Regenerate Manifests
```powershell
python scripts/generate_manifests.py
```

---

## NEXT STEPS

### Immediate
- [ ] Monitor production stability (Mágerstav)
- [ ] Test Mágerstav verification workflow
- [ ] Document any production issues

### Short-term
- [ ] Test server: Create W3DBSMGR auto-start script
- [ ] Consider Phase 5 features (if planned)

### Long-term  
- [ ] Test server: Contact IT administrator
- [ ] Test server: Fix Winsock/Pervasive permanently
- [ ] Test server: Enable System Restore

---

## IMPORTANT REMINDERS

### Communication
- All communication in Slovak language
- Project names: Exact terminology (nex-automat, NEX Genesis)
- One solution at a time, wait for confirmation

### Code Standards
- ALL code/configs/docs in artifacts (ALWAYS)
- Python files, configs, docs >10 lines → artifacts
- Scripts numbered 01-99 (temporary only)
- Flat structure in nex-shared package

### Deployment
- Development → Git → Deployment workflow
- Never fix directly in Deployment
- Always commit before deployment
- Test after every deployment

### Critical Rules
- NEVER start work if GitHub files fail to load
- NEVER use localStorage/sessionStorage in artifacts
- NEVER reboot test server (Pervasive breaks)
- NEVER do Winsock reset on any server

---

## ENVIRONMENT DETAILS

**Production Server (Mágerstav):**
- OS: Windows Server
- Python: 3.13.7 32-bit
- Database: PostgreSQL + Btrieve
- Service: NSSM (working perfectly)

**Test Server:**
- OS: Windows Server
- Python: 3.13.7 32-bit
- Database: PostgreSQL + Btrieve (manual start)
- Method: Task Scheduler (workaround)
- Issues: Winsock broken, Pervasive unstable

**Development:**
- Location: C:\Development\nex-automat
- Python: venv32 (3.13.7 32-bit)
- Git: develop branch

---

## SUPPORT & TROUBLESHOOTING

### Service Won't Start
1. Check logs: `C:\Deployment\nex-automat\logs\`
2. Verify port 8001 not in use
3. Test as console app first
4. Check Pervasive/Btrieve status

### Btrieve Errors
1. Verify W3DBSMGR.EXE is running
2. Check DLL: `C:\PVSW\bin\w3btrv7.dll`
3. Test NEX Genesis access
4. If test server: Avoid reboot

### API Not Responding
1. Check if service/task is running
2. Test port: `Test-NetConnection localhost -Port 8001`
3. View logs for errors
4. Restart service/task

---

## KEY CONTACTS

**Developer:** Zoltán  
**Company:** ICC Komárno  
**Customer:** Mágerstav s.r.o.  
**Environment:** Production + Test servers

---

**Init Prompt Created:** 2025-12-09 16:00  
**Version:** v2.4 Phase 4 - COMPLETE  
**Status:** ✅ Production Ready (Mágerstav)  
**Next:** Continue monitoring or start Phase 5