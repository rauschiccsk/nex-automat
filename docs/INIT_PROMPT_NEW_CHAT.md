# Init Prompt for New Chat - DAY 5 Testing Phase

**Project:** NEX Automat v2.0 - Supplier Invoice Loader  
**Customer:** Mágerstav s.r.o.  
**Current Progress:** 95% (Service Recovery Complete, Ready for Testing)  
**Last Session:** DAY 5 Service Recovery & Performance Baseline (2025-11-22)  
**Next Phase:** DAY 5 Error Handling & Final Validation  

---

## Quick Context

Pokračujeme v projekte NEX Automat v2.0 - automatizované spracovanie dodávateľských faktúr pre zákazníka Mágerstav s.r.o.

**Stav projektu:**
- DAY 1-4: ✅ Complete (Migration, Backup, Service, Integration)
- DAY 5: ✅ Service Recovery Complete → 🔜 Testing Phase
- Target Go-Live: 2025-11-27 (4 dni zostáva)

**Preflight Status:** 6/6 PASS 🟢 READY

---

## Last Session Achievements (2025-11-22)

### Critical Fixes Completed

1. **manage_service.py Reconstruction**
   - Was corrupt (453 bytes) → Reconstructed (8.8 KB)
   - Recovered from chat history
   - All functions working: status, start, stop, restart, logs, tail

2. **NSSM UTF-16LE Encoding Fix**
   - Issue: NSSM returns UTF-16LE with `\x00` null bytes
   - Fixed: manage_service.py + day5_preflight_check.py
   - Solution: Decode bytes + strip null bytes

3. **Performance Baseline Created**
   - Script: create_baseline.py (no psutil dependency)
   - Metrics: PDF processing, DB operations, system info
   - Location: test_results/performance_baseline.json

4. **Preflight Checks: 6/6 PASS**
   - ✅ Service Status: RUNNING
   - ✅ Database Connectivity: PostgreSQL OK
   - ✅ Dependencies: All installed
   - ✅ Known Issues: Documented
   - ✅ Test Data: 18 PDFs ready
   - ✅ Performance Baseline: Created

---

## Current System State

### Development Environment
```
Location: C:\Development\nex-automat
Status: ✅ All fixes applied, ready for Git commit
Config: apps/supplier-invoice-loader/config/config.yaml
Python: 3.13.7 32-bit (venv32)
Git: Ready to commit service recovery changes
```

### Deployment Environment
```
Location: C:\Deployment\nex-automat
Service: NEX-Automat-Loader (RUNNING) ✅
Database: PostgreSQL localhost:5432/invoice_staging ✅
Dependencies: All installed ✅
Performance: Baseline created ✅
Status: 🟢 READY for DAY 5 testing
```

### Preflight Check Results
```
Checks: 6/6 passed
Status: 🟢 READY
✅ Service Status
✅ Database Connectivity
✅ Dependencies
✅ Known Issues
✅ Test Data
✅ Performance Baseline
```

---

## Immediate Next Steps

### PRIORITY 1: Git Commit (First thing!)

**What to commit:**
- Service recovery scripts (manage_service.py reconstruction)
- UTF-16 encoding fixes (manage_service.py, day5_preflight_check.py)
- Performance baseline (create_baseline.py)
- Deployment updates (deploy_to_deployment.py)
- All diagnostic/fix scripts

**Git workflow:**
```bash
cd C:\Development\nex-automat
git status
git add .
git commit -m "[your commit message]"
git push
```

### PRIORITY 2: DAY 5 Error Handling Testing

**Test Scenarios:**
1. Service crash recovery
2. Database connection failures
3. PDF processing errors
4. Concurrent request handling
5. Memory leak detection
6. Error logging validation

**Expected outcomes:**
- Service auto-restarts after crash
- Graceful database reconnection
- Proper error messages in logs
- No memory leaks under load
- Error rates within acceptable limits

### PRIORITY 3: Recovery Procedures

**Document and test:**
1. Service restart procedures
2. Backup restoration
3. Rollback scenarios
4. Emergency contacts
5. Troubleshooting guides

---

## Key Scripts & Locations

### Service Management
```
scripts/manage_service.py (8.8 KB) - Service control + UTF-16 fix
scripts/recreate_manage_service.py - Service reconstruction script
```

### Testing & Validation
```
scripts/day5_preflight_check.py (9.8 KB) - 6/6 checks
scripts/create_baseline.py (7.3 KB) - Performance baseline
scripts/test_preflight_in_development.py - Dev testing
```

### Deployment
```
scripts/deploy_to_deployment.py (4.5 KB) - Automated sync
```

### Test Data
```
apps/supplier-invoice-loader/tests/samples/ - 18 PDF invoices
test_results/performance_baseline.json - Performance metrics
```

---

## Important Technical Details

### UTF-16LE Encoding Fix
**Problem:** NSSM returns mixed encoding
- Service name: ASCII
- Status value: UTF-16LE with `\x00` null bytes

**Solution in manage_service.py:**
```python
def decode_nssm_output(result):
    try:
        if isinstance(result.stdout, bytes):
            stdout = result.stdout.decode('utf-16le').rstrip('\x00')
        else:
            stdout = result.stdout.replace('\x00', '')
    except:
        stdout = str(result.stdout).replace('\x00', '')
    return stdout
```

**Solution in day5_preflight_check.py:**
```python
result = subprocess.run(..., text=False)  # Get bytes
stdout = result.stdout.decode("utf-8", errors="ignore")
stdout = stdout.replace("\x00", "")  # Strip null bytes
```

### Performance Baseline Structure
```json
{
  "timestamp": "2025-11-22T19:54:34.701284",
  "location": "C:\\Deployment\\nex-automat",
  "pdf_processing": {
    "count": 5,
    "avg_time": 2.160,
    "min_time": 2.083,
    "max_time": 2.248,
    "throughput_per_second": 0.463
  },
  "database_operations": {
    "connection_time": 0.XXX,
    "simple_select_time": 0.XXX,
    "table_query_time": 0.XXX
  },
  "system_info": {
    "cpu_cores": 24,
    "platform": "Windows",
    "python_version": "3.13.7"
  }
}
```

---

## Environment Variables (CRITICAL)

### Required in Deployment
```
POSTGRES_PASSWORD - PostgreSQL authentication (MUST BE SET!)
LS_API_KEY - API authentication
```

### Verification
```bash
# In PowerShell (Deployment)
$env:POSTGRES_PASSWORD
$env:LS_API_KEY
```

---

## Commands Quick Reference

### Service Management (Deployment only)
```bash
cd C:\Deployment\nex-automat

# Status
python scripts\manage_service.py status

# Control (requires Admin)
python scripts\manage_service.py start
python scripts\manage_service.py stop
python scripts\manage_service.py restart

# Logs
python scripts\manage_service.py logs      # Last 50 lines
python scripts\manage_service.py tail      # Live tail
```

### Preflight Checks
```bash
# Development
cd C:\Development\nex-automat
python scripts\test_preflight_in_development.py

# Deployment
cd C:\Deployment\nex-automat
python scripts\day5_preflight_check.py
```

### Performance Baseline
```bash
# Create/Update
python scripts\create_baseline.py

# View results
type test_results\performance_baseline.json
```

### Deployment Sync
```bash
# From Development
cd C:\Development\nex-automat
python scripts\deploy_to_deployment.py
```

---

## Known Limitations

1. **Performance Baseline in Development**
   - Database metrics show error (no PostgreSQL in Dev)
   - Expected behavior - not a problem
   - Full baseline only works in Deployment

2. **KNOWN_ISSUES.md Outdated**
   - Shows old critical issues (already resolved)
   - Preflight warns but passes
   - Needs update during DAY 5 cleanup

3. **Service Logs Location**
   - Windows Service logs: Windows Event Viewer
   - Application logs: logs/service-*.log
   - Both locations should be monitored

---

## Testing Checklist for DAY 5

### Error Handling Tests
- [ ] Service crash and auto-restart
- [ ] Database connection loss and recovery
- [ ] Invalid PDF handling
- [ ] Missing environment variables
- [ ] Disk space exhaustion
- [ ] Memory pressure scenarios
- [ ] Concurrent request overload

### Performance Tests
- [ ] Single invoice processing time
- [ ] Concurrent processing (5, 10, 20 invoices)
- [ ] Memory usage under load
- [ ] CPU usage patterns
- [ ] Database query performance
- [ ] API response times

### Recovery Tests
- [ ] Service stop/start cycle
- [ ] Database restore from backup
- [ ] Config rollback
- [ ] Emergency shutdown procedure
- [ ] Data corruption recovery

### Documentation Tests
- [ ] All procedures executable by customer
- [ ] Troubleshooting guide accurate
- [ ] Error messages clear and actionable
- [ ] Monitoring setup functional
- [ ] Backup/restore documented

---

## Success Criteria

### For This Session
1. **Git Commit Complete**
   - All service recovery changes committed
   - Clean git status
   - Pushed to GitHub

2. **Error Handling Validated**
   - Service recovers from crashes
   - Database reconnection works
   - Error logs are comprehensive
   - No critical failure modes

3. **Recovery Procedures Documented**
   - Step-by-step guides created
   - Tested and verified
   - Customer-friendly format

### For Go-Live (2025-11-27)
1. Service stable for 48h continuous operation
2. Error rate < 1% under normal load
3. All documentation complete
4. Customer trained and comfortable
5. Monitoring and alerting functional

---

## Critical Reminders

### Workflow (MANDATORY)
```
Development → Git commit → Git push → Deploy to Deployment
NEVER fix directly in Deployment!
```

### Before Starting Any Work
1. Check GitHub for latest changes
2. Load SESSION_NOTES.md for context
3. Verify preflight: 6/6 PASS
4. Ensure Service is RUNNING

### When Problems Occur
1. Check service logs first: `python scripts\manage_service.py logs`
2. Verify environment variables set
3. Check database connectivity
4. Review KNOWN_ISSUES.md
5. Search conversation history if needed

### Communication Style
- One solution at a time
- Wait for confirmation before next step
- Generate all outputs into artifacts
- End each response with token usage
- No alternatives unless explicitly requested

---

## File Locations Map

### Configuration
```
apps/supplier-invoice-loader/config/config.yaml - Main config
```

### Logs
```
logs/service-*.log - Application logs
Windows Event Viewer - Service logs
```

### Data
```
apps/supplier-invoice-loader/tests/samples/ - Test PDFs
test_results/performance_baseline.json - Performance data
```

### Documentation
```
docs/SESSION_NOTES.md - This file
docs/deployment/ - Deployment guides
docs/KNOWN_ISSUES.md - Issue tracking
```

---

## Next Steps Summary

**IMMEDIATE:**
1. Git commit all service recovery changes
2. Start DAY 5 error handling testing
3. Document recovery procedures

**THEN:**
1. Performance validation under load
2. Final documentation review
3. Customer training preparation
4. Go-live checklist completion

---

**Last Updated:** 2025-11-22  
**Progress:** 95/100  
**Status:** 🟢 READY FOR DAY 5 TESTING  
**Target:** Complete testing + documentation by 2025-11-25