# NEX Automat v2.4 - Session Notes

**Aktualizované:** 2025-12-09 16:00  
**Status:** ✅ Phase 4 COMPLETE - Production Ready

---

## Current Status

### Phase 4: NEX Genesis Product Enrichment - ✅ COMPLETE

**Čo funguje:**
- ✅ Complete GSCAT model with BarCode @ offset 60
- ✅ EAN matching: 81.2% (cieľ >65%)
- ✅ Re-processing: 168/207 items matched (81.2%)
- ✅ Unit tests: 108/108 passing
- ✅ BtrieveClient: PATH-based DLL loading + Unicode fix
- ✅ Git: All committed and pushed
- ✅ Production u Mágerstav: NSSM service funguje perfektne

**Progress:** 6/6 criteria (100%)

---

## Deployment Configurations

### Production (Mágerstav) - NSSM Service ✅

**Konfigurácia:**
```
Service Name: NEX-Automat-Loader
Manager: NSSM
Account: LocalSystem
Path: C:\Deployment\nex-automat
Status: RUNNING
```

**Management:**
```powershell
# Start service
net start "NEX-Automat-Loader"

# Stop service
net stop "NEX-Automat-Loader"

# Check status
sc query "NEX-Automat-Loader"

# View logs
type C:\Deployment\nex-automat\logs\service-stderr.log
```

### Test Server - Task Scheduler ⚠️

**Konfigurácia:**
```
Task Name: NEX-Automat-Loader
Trigger: At system startup
User: DESKTOP-6AU0066\Server
Python: C:\Deployment\nex-automat\venv32\Scripts\python.exe
Script: C:\Deployment\nex-automat\apps\supplier-invoice-loader\main.py
Status: RUNNING (s obmedzeniami)
```

**Obmedzenia:**
- ⚠️ W3DBSMGR.EXE musí byť manuálne spustený pred NEX Automat
- ⚠️ Server NESMIE byť reštartovaný (pokazí Pervasive)
- ⚠️ Winsock je rozbitý po reset-e

**Management:**
```powershell
# 1. Spustiť Pervasive FIRST
Start-Process "C:\PVSW\bin\W3DBSMGR.EXE"

# 2. Spustiť NEX Automat
Start-ScheduledTask -TaskName "NEX-Automat-Loader"

# Stop
Stop-ScheduledTask -TaskName "NEX-Automat-Loader"

# Status
Get-ScheduledTask -TaskName "NEX-Automat-Loader" | Get-ScheduledTaskInfo

# Test API
Start-Process "http://localhost:8001/docs"
```

---

## Recent Changes (2025-12-09)

### Code Changes

**packages/nexdata/nexdata/btrieve/btrieve_client.py:**
- Pridané PATH-based DLL loading ako priorita
- Odstránené emoji unicode characters
- Debug output: [DEBUG], [SUCCESS], [ERROR]

**apps/supplier-invoice-loader/main.py:**
- Odstránené emoji unicode characters
- Nahradené: ✅→[OK], ❌→[ERROR]

**Git Status:**
```
Commit: "Fix: BtrieveClient DLL loading and Unicode encoding issues"
Branch: develop
Status: Pushed
```

### Issues Resolved

1. **WinError 10106** - asyncio pod service účtom
   - Riešenie: Task Scheduler namiesto NSSM (test server only)

2. **BtrieveClient DLL loading** - nenačítavala z PATH
   - Riešenie: PATH loading ako priorita

3. **Unicode encoding** - emojis v Windows console
   - Riešenie: Textové prefixy namiesto emojis

---

## Next Steps

### Immediate

- [ ] Monitor stability na production (Mágerstav)
- [ ] Test MÃ¡gerstav verification workflow
- [ ] Document any issues

### Short-term

- [ ] Test server: Vytvoriť automatický W3DBSMGR startup script
- [ ] Consider Phase 5 features (ak sú plánované)

### Long-term

- [ ] Test server: Kontaktovať IT administrátora
- [ ] Test server: Fix Winsock/Pervasive issues
- [ ] Test server: Enable System Restore

---

## Known Issues

### Test Server Only

**Winsock/Pervasive Issue:**
- Cause: Winsock reset rozbil Pervasive SRDE
- Impact: Server nesmie byť reštartovaný
- Workaround: Manuálny štart W3DBSMGR
- Long-term: Vyžaduje IT administrátora alebo reinstall Windows

**NOT an issue:**
- Kód funguje perfektne
- Production u Mágerstav bez problémov
- Development environment v poriadku

---

## Testing

### Unit Tests
```bash
cd C:\Development\nex-automat
python -m pytest packages/nexdata/tests/ -v
```
**Status:** 108/108 passing ✅

### EAN Matching Test
```bash
python scripts/test_ean_lookup.py
```
**Result:** 81.2% match rate (target: >65%) ✅

### API Test
```
http://localhost:8001/docs
http://localhost:8001/health
```
**Status:** Accessible ✅

---

## Important Notes

### DO NOT on Test Server
- ❌ NEVER reboot (pokazí Pervasive)
- ❌ NEVER run Winsock reset again
- ❌ NEVER modify network configuration

### DO on Test Server
- ✅ Keep running without reboot
- ✅ Start W3DBSMGR before NEX Automat
- ✅ Monitor logs regularly
- ✅ Document any issues

### Production (Mágerstav)
- ✅ NSSM service is preferred method
- ✅ No special workarounds needed
- ✅ Standard Windows service management

---

## Contact & Escalation

**Ak NEX Automat nefunguje:**
1. Check service/task status
2. Check logs: `C:\Deployment\nex-automat\logs\`
3. Verify port 8001 is open
4. Check Pervasive/Btrieve status

**Ak Pervasive nefunguje (test server):**
1. Manuálne spustiť W3DBSMGR.EXE
2. Test NEX Genesis
3. Ak stále problém, kontaktovať IT administrátora

**Ak production (Mágerstav) nefunguje:**
1. Check NSSM service logs
2. Verify všetky dependencies
3. Eskalovať Zoltánovi

---

## Quick Reference

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

# API health
curl http://localhost:8001/health

# Browser
Start-Process "http://localhost:8001/docs"
```

### View Logs
```powershell
# Latest errors
type C:\Deployment\nex-automat\logs\service-stderr.log | Select-Object -Last 50

# Latest output
type C:\Deployment\nex-automat\logs\service-stdout.log | Select-Object -Last 50
```

---

**Last Updated:** 2025-12-09 16:00  
**Maintained By:** Zoltán  
**Production Status:** ✅ READY (Mágerstav)  
**Test Server Status:** ⚠️ FUNCTIONAL (with workarounds)