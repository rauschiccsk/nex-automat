# Init Prompt for New Chat - Service Recovery & DAY 5 Completion

**Project:** NEX Automat v2.0 - Supplier Invoice Loader  
**Customer:** Mágerstav s.r.o.  
**Current Progress:** 90% (Service Recovery Phase)  
**Last Session:** DAY 5 Preparation - Pre-Flight System & Critical Recovery (2025-11-22)  
**Next Phase:** Service Recovery → DAY 5 Final Validation

---

## Quick Context

Pokračujeme v projekte NEX Automat v2.0 - automatizované spracovanie dodávateľských faktúr pre zákazníka Mágerstav s.r.o.

**Stav projektu:**
- DAY 1: ✅ Monorepo Migration (Complete)
- DAY 2: ✅ Backup & Recovery Systems (Complete)
- DAY 3: ✅ Service Installation & Validation (Complete)
- DAY 4: ✅ Integration & E2E Testing (Complete)
- DAY 5: ⚠️ Pre-Flight System Created, Service Recovery Needed

**Target Go-Live:** 2025-11-27 (4 dni zostáva)

---

## Critical Situation

### Problem Discovered

**manage_service.py corrupt:**
- Súbor má len 453 bytes (should be ~10KB)
- V Git už corrupt (commit 50cdf14)
- Žiadne backupy v Deployment
- Service management nefunguje

### Solution Prepared

**Rekonštrukcia z predchádzajúcich chatov:**
- ✅ Vytvorený `scripts/recreate_manage_service.py`
- ✅ Rekonštruuje manage_service.py od základov
- ✅ Bez emoji (pure ASCII)
- ✅ Všetky funkcie: start, stop, restart, status, logs, tail

**Čo treba dokončiť:**
1. Spustiť recreate_manage_service.py v Development
2. Overiť veľkosť súboru (~10KB)
3. Deploy do Deployment
4. Test service commands
5. Dosiahnuť 6/6 preflight checks

---

## Last Session Summary (2025-11-22)

### Major Achievements
1. **Pre-Flight System:** 100% functional (4/4 tests v Development)
2. **Config Fixes:** PostgreSQL env variable, SQLite optional
3. **Dependency Fixes:** PyYAML, Pillow (PIL import)
4. **New Critical Rule:** Development → Git → Deployment workflow
5. **Service Recovery:** Rekonštrukcia manage_service.py prepared

### Issues Resolved
1. ✅ Config path → `apps/supplier-invoice-loader/config/config.yaml`
2. ✅ PostgreSQL password → `POSTGRES_PASSWORD` environment variable
3. ✅ SQLite detection → Optional, config-based
4. ✅ Pillow import → `"pillow"` → `"PIL"`
5. ✅ PyYAML → Added to requirements.txt

### Critical Discovery
- manage_service.py bol v Git už corrupt (453 bytes)
- Úspešná rekonštrukcia z conversation_search
- Demonštruje dôležitosť backups + Git verification

---

## Current System State

### Development Environment
```
Location: C:\Development\nex-automat
Status: ✅ Pre-flight check: 4/4 passing
Dependencies: ✅ All installed (pillow, PyYAML, etc.)
Config: ✅ Correct path (apps/supplier-invoice-loader/config/config.yaml)
manage_service.py: ⚠️ Corrupt (453 bytes)
recreate script: ✅ Ready
```

### Deployment Environment
```
Location: C:\Deployment\nex-automat
Status: ⚠️ Pre-flight check: 4/6 passing
Service: ❌ Cannot check (manage_service.py corrupt)
Database: ✅ PostgreSQL working
Dependencies: ✅ All installed
Performance: ⚠️ Baseline missing (not critical)
```

### Pre-Flight Check Results (Development)
```
✅ Config Loading: PASS
✅ Database Connectivity: PASS (PostgreSQL + SQLite detection)
✅ Dependencies: PASS (9/9 including PIL, yaml)
✅ Preflight Script Syntax: PASS
```

### Pre-Flight Check Results (Deployment)
```
❌ Service Status: FAIL (manage_service.py corrupt)
✅ Database Connectivity: PASS
✅ Dependencies: PASS
✅ Known Issues: PASS
✅ Test Data: PASS (18 PDFs)
⚠️ Performance Baseline: MISSING (not critical)
```

---

## Immediate Next Steps

### PRIORITY 1: Service Recovery (CRITICAL)

**Step 1: Recreate manage_service.py**
```bash
cd C:\Development\nex-automat
python scripts\recreate_manage_service.py
```

**Expected:**
- ✅ Creates scripts/manage_service.py
- ✅ Size: ~10KB (not 453 bytes!)
- ✅ Pure ASCII (no emoji)
- ✅ All functions working

**Step 2: Verify Script**
```bash
dir scripts\manage_service.py
# Should show ~10KB, not 453 bytes
```

**Step 3: Deploy to Deployment**
```bash
python scripts\deploy_to_deployment.py
```

**Step 4: Test in Deployment**
```bash
cd C:\Deployment\nex-automat
python scripts\manage_service.py status
# Should show: Service: NEX-Automat-Loader, Status: SERVICE_RUNNING
```

**Step 5: Run Preflight Check**
```bash
python scripts\day5_preflight_check.py
# Target: 6/6 passing (or 5/6 if performance baseline missing)
```

---

## Important Files & Locations

### Development Environment
```
Location: C:\Development\nex-automat
Config: apps/supplier-invoice-loader/config/config.yaml
Tests: apps/supplier-invoice-loader/tests/
Scripts: scripts/ (16 utility scripts)
Docs: docs/deployment/
```

### Deployment Environment
```
Location: C:\Deployment\nex-automat
Service: NEX-Automat-Loader (Windows Service via NSSM)
Logs: logs/service-*.log
Config: apps/supplier-invoice-loader/config/config.yaml
Database: localhost:5432/invoice_staging (PostgreSQL)
```

### Key Scripts Created This Session
```
scripts/day5_preflight_check.py          - Pre-flight validation
scripts/recreate_manage_service.py       - Service recovery ⭐ NEW
scripts/deploy_to_deployment.py          - Deployment helper (updated)
scripts/diagnose_service_status_check.py - Service diagnostics
scripts/fix_pillow_import_name.py        - Pillow fix
scripts/fix_preflight_config_path.py     - Config fix
... (10 more diagnostic/fix scripts)
```

---

## Critical Reminders

### Before Starting Work
1. Load session notes: `docs/SESSION_NOTES.md`
2. Run recreate_manage_service.py v Development
3. Verify file size (must be ~10KB!)
4. Deploy to Deployment
5. Test service commands

### Environment Variables (CRITICAL)
```
POSTGRES_PASSWORD - PostgreSQL authentication (SET!)
LS_API_KEY - API authentication
```

### Test Data
```
Sample PDFs: apps/supplier-invoice-loader/tests/samples/
Test invoices: 18 real customer PDFs available
```

### Deployment Workflow (MANDATORY)
```
Development → Git commit → Git push → Deploy to Deployment
NEVER fix directly in Deployment!
```

---

## Success Criteria for Next Session

### Immediate Goals (1-2 hours)
- [ ] Recreate manage_service.py v Development
- [ ] Verify script size (~10KB)
- [ ] Deploy to Deployment
- [ ] Service commands working
- [ ] Preflight check: 5/6 or 6/6 passing
- [ ] Git commit all changes

### Optional (if time permits)
- [ ] Create performance baseline
- [ ] Test service auto-restart
- [ ] Update KNOWN_ISSUES.md
- [ ] Start DAY 5 error handling tests

---

## Known Limitations

1. **manage_service.py Corruption**
   - Was 453 bytes (should be ~10KB)
   - In Git already corrupt
   - No backups available
   - Solution: Reconstruction from chat history

2. **Performance Baseline Missing**
   - Not critical for preflight
   - Can be created later
   - test_performance.py script exists

3. **SQLite Not Used**
   - System uses PostgreSQL primary
   - SQLite check is optional
   - Working as designed

---

## Commands Quick Reference

### Service Recovery
```bash
# Development
cd C:\Development\nex-automat
python scripts\recreate_manage_service.py
dir scripts\manage_service.py

# Deploy
python scripts\deploy_to_deployment.py

# Deployment test
cd C:\Deployment\nex-automat
python scripts\manage_service.py status
python scripts\manage_service.py start
```

### Pre-Flight Check
```bash
# Development
cd C:\Development\nex-automat
python scripts\test_preflight_in_development.py

# Deployment
cd C:\Deployment\nex-automat
python scripts\day5_preflight_check.py
```

### Service Management
```bash
cd C:\Deployment\nex-automat

# Status
python scripts\manage_service.py status

# Start/Stop/Restart (requires Admin)
python scripts\manage_service.py start
python scripts\manage_service.py stop
python scripts\manage_service.py restart

# Logs
python scripts\manage_service.py logs
python scripts\manage_service.py tail
```

---

## Next Steps Summary

**IMMEDIATE (HIGH PRIORITY):**
1. Run recreate_manage_service.py
2. Verify script (~10KB)
3. Deploy + test
4. Achieve 6/6 preflight
5. Git commit

**THEN:**
1. Performance baseline (optional)
2. Start DAY 5 testing
3. Error handling validation
4. Recovery procedures
5. Go-live preparation

---

**Last Updated:** 2025-11-22  
**Progress:** 90/100  
**Status:** ⚠️ SERVICE RECOVERY READY  
**Target:** Complete recovery + 6/6 preflight checks, then proceed to DAY 5