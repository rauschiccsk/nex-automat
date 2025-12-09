# INIT PROMPT - NEX Automat v2.4 Service Startup Fix

## PROJECT CONTEXT

**Projekt:** nex-automat  
**Typ:** Monorepo - Multi-customer SaaS for automated invoice processing  
**Development:** `C:\Development\nex-automat`  
**Deployment:** `C:\Deployment\nex-automat`  
**Python:** 3.13.7 (venv32)  
**Git Branch:** develop  
**Current Version:** v2.4 Phase 4 - SERVICE STARTUP BLOCKED

---

## CURRENT STATUS 🔴

### Phase 4: NEX Genesis Product Enrichment
**Status:** CODE COMPLETE - SERVICE STARTUP BLOCKED

**What Works:**
- ✅ Complete GSCAT model with BarCode @ offset 60
- ✅ EAN matching: 81.2% (target >65%)
- ✅ Re-processing: 168/207 items matched
- ✅ Unit tests: 108/108 passing
- ✅ Git: All changes committed and pushed
- ✅ Deployment: Code pulled to C:\Deployment\nex-automat
- ✅ NSSM: Configured with correct PATH and AppDirectory

**What's Blocked:**
- 🔴 **CRITICAL:** Service fails to start with WinError 10106
- 🔴 Asyncio _overlapped module cannot initialize
- 🔴 Winsock Service Provider initialization failure
- 🔴 Service starts then immediately pauses

**Root Cause:**
Python asyncio cannot initialize under LocalSystem service account due to Winsock Service Provider issue (WinError 10106).

---

## IMMEDIATE PRIORITY 🎯

### Test as Console Application FIRST

**Why:** 
- Verify code works (it should - works in Development)
- Isolate if problem is service-specific or code-specific
- Fastest way to unblock Mágerstav Go-Live

**Test Procedure:**
```powershell
# Stop service
net stop "NEX-Automat-Loader"

# Run as console app
cd C:\Deployment\nex-automat\apps\supplier-invoice-loader
C:\Deployment\nex-automat\venv32\Scripts\python.exe main.py

# Expected: FastAPI starts on port 8001
# Test: http://localhost:8001/health
```

**If Console Works:**
→ Problem: Service configuration / LocalSystem account  
→ Solutions: Change service account OR fix Winsock

**If Console Fails:**
→ Problem: Environment / system issue  
→ Solutions: Check Python, venv32, network stack

---

## KEY ERROR

**From service-stderr.log:**
```
Traceback (most recent call last):
  File "C:\Deployment\nex-automat\apps\supplier-invoice-loader\main.py", line 16
    from fastapi import FastAPI...
  ...
  File "C:\Program Files (x86)\Python313-32\Lib\asyncio\windows_events.py", line 8
    import _overlapped
OSError: [WinError 10106] The requested service provider could not be loaded or initialized
```

**Meaning:** 
- Asyncio needs Windows Sockets (_overlapped module)
- Winsock Service Provider cannot load under current service context
- This is NOT a permissions issue (SYSTEM has Full Control everywhere)
- This is NOT a path issue (Btrieve DLL found and accessible)

---

## VERIFIED CONFIGURATIONS

### File System ✅
```
C:\PVSW\bin\w3btrv7.dll          → EXISTS, ACCESSIBLE
C:\NEX\YEARACT\STORES\GSCAT.BTR  → EXISTS, ACCESSIBLE
C:\Deployment\nex-automat        → EXISTS, SYSTEM has Full Control
```

### NSSM Configuration ✅
```
Application:         C:\Deployment\nex-automat\venv32\Scripts\python.exe
AppDirectory:        C:\Deployment\nex-automat\apps\supplier-invoice-loader
AppParameters:       ...main.py
AppEnvironment:      PYTHONIOENCODING=utf-8
AppEnvironmentExtra: +PATH=C:\PVSW\bin
ObjectName:          LocalSystem
```

### Code ✅
```
✅ GSCAT model with BarCode @ offset 60
✅ GSCATRepository.find_by_barcode() fixed
✅ All unit tests passing (108/108)
✅ EAN matching: 81.2%
✅ Zero errors in Development
```

---

## SOLUTIONS TO TRY

### Solution 1: Console App (Testing) - IMMEDIATE
```powershell
cd C:\Deployment\nex-automat\apps\supplier-invoice-loader
C:\Deployment\nex-automat\venv32\Scripts\python.exe main.py
```
**If works:** Code is fine, service config needs fix

### Solution 2: Fix Winsock (Requires Reboot)
```powershell
# Run as Administrator
netsh winsock reset
netsh int ip reset
# Reboot server
# Restart service
```
**If works:** Winsock stack was corrupted

### Solution 3: Change Service Account
```powershell
# Option A: NetworkService
sc config "NEX-Automat-Loader" obj= "NT AUTHORITY\NetworkService"

# Option B: Dedicated user (requires user creation + permissions)
sc config "NEX-Automat-Loader" obj= "DOMAIN\nexservice" password= "***"
```
**If works:** LocalSystem has limitations with asyncio

### Solution 4: Different Service Manager
- Try Windows Task Scheduler instead of NSSM
- Try direct sc.exe service creation
- Try running under IIS with reverse proxy

---

## TECHNICAL BACKGROUND

### WinError 10106 Explanation

**Error Code:** WSASYSNOTREADY (10091) or WSAVERNOTSUPPORTED (10092)  
**Meaning:** Windows Sockets implementation cannot function at this time

**Common Causes:**
1. Winsock LSP (Layered Service Provider) corruption
2. Service runs without proper desktop/session context
3. Antivirus/firewall blocking socket initialization
4. Missing/corrupted Winsock2 DLL

**Why LocalSystem Affected:**
- LocalSystem runs without interactive desktop
- Some Winsock features require user context
- Asyncio _overlapped uses advanced socket features
- May not be available in system service context

---

## DEPLOYMENT WORKFLOW

```
Current State:
✅ Development → Git → Deployment
✅ Code deployed and verified
✅ NSSM configured correctly
🔴 Service cannot start (WinError 10106)

Next Steps:
1. Test as console app (verify code works)
2. If console works:
   - Try NetworkService account
   - OR fix Winsock (netsh reset + reboot)
   - OR use Task Scheduler instead of NSSM
3. Once service runs:
   - Resume service (sc continue)
   - Verify port 8001
   - Test Mágerstav verification
4. Document solution for future deployments
```

---

## SUCCESS CRITERIA

**Phase 4 Complete When:**
- [x] Complete GSCAT model deployed
- [x] EAN lookup: >15% success (achieved 100%)
- [x] Re-processing: >70% match rate (achieved 81.2%)
- [x] Unit tests passing (108/108)
- [ ] **Service starts successfully** ← BLOCKED HERE
- [ ] **Mágerstav verification** ← Waiting for service

**Progress:** 4/6 criteria (67%)

---

## CRITICAL RULES

1. **DO NOT modify code** - it works correctly
2. **Test console app FIRST** - fastest diagnostic
3. **Document solution** - for future reference
4. **One solution at a time** - systematic approach
5. **If console works, problem is service-specific** - focus on service config

---

## ENVIRONMENT DETAILS

**Production Server:**
- OS: Windows Server (specific version unknown)
- Python: 3.13.7 32-bit
- Location: C:\Deployment\nex-automat
- Service: NEX-Automat-Loader (NSSM managed)
- Account: LocalSystem

**Database:**
- PostgreSQL: localhost:5432/invoice_staging
- NEX Genesis: C:\NEX\YEARACT\STORES (Btrieve)
- Btrieve DLL: C:\PVSW\bin\w3btrv7.dll

**Network:**
- Service Port: 8001
- API: FastAPI + Uvicorn
- Asyncio: Required for FastAPI

---

## SCRIPTS AVAILABLE

### Testing
- `scripts/test_ean_lookup.py` - Test EAN matching
- `scripts/reprocess_nex_enrichment.py` - Re-process enrichment
- `scripts/27_check_service_logs.py` - Check service logs

### Diagnostics
- `scripts/28_check_deployment_config.py` - Verify config
- `scripts/29_check_permissions.py` - Check file permissions
- `scripts/30_check_nssm_config.py` - NSSM configuration

### Service Control
- `scripts/22_restart_service.py` - Restart service
- `scripts/26_resume_service.py` - Resume paused service

---

## NOTES

**DO NOT:**
- Modify GSCAT model (it's correct now)
- Modify repository code (it's correct now)
- Assume permissions issue (already verified)
- Skip console test (crucial step)

**DO:**
- Test console app immediately
- Document what works / doesn't work
- Try solutions systematically
- Keep logs of each attempt

---

**Init Prompt Created:** 2025-12-09 14:30  
**Version:** v2.4 Phase 4 - Service Startup Fix  
**Status:** 🔴 Blocked by WinError 10106  
**Next Action:** Test as console application to isolate issue