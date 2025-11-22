# NEX Automat - Session Notes

**Project:** nex-automat  
**Location:** C:/Development/nex-automat  
**Current Phase:** DAY 5 Preparation - Pre-Flight Check System (90% Complete)

---

## 🎯 Current Status

### DAY 5 - Pre-Flight Check System & Critical Recovery (2025-11-22) ⚠️ IN PROGRESS

**Goal:** Pripraviť validačný systém pre DAY 5 testing a vyriešiť kritické deployment issues

**Completed:**
- [x] Vytvorený day5_preflight_check.py s all fixes
- [x] Nainštalovaný pillow do Development venv32
- [x] Pridaný pillow + PyYAML do requirements.txt
- [x] Opravený PostgreSQL password handling (environment variable)
- [x] Opravený SQLite path detection (config.yaml + multiple locations)
- [x] Opravený Pillow import name ("pillow" → "PIL")
- [x] Testing v Development: 4/4 tests passing ✅
- [x] Deployment testing: 4/6 checks passing (service issue, baseline missing)
- [x] Pridané KRITICKÉ pravidlo: Development → Git → Deployment workflow
- [x] Identifikovaný corrupt manage_service.py (453 bytes)
- [x] Rekonštruovaný manage_service.py z predchádzajúcich chatov

**In Progress:**
- [ ] Finálny redeploy s obnoveným manage_service.py
- [ ] Service status validation
- [ ] Performance baseline creation
- [ ] Kompletný preflight check (6/6 passing)

**Critical Discovery:**
- **manage_service.py bol v Git už corrupt** (453 bytes v commite 50cdf14)
- Neexistujú backupy v Deployment
- Úspešná rekonštrukcia z conversation_search artifacts
- Demonštruje dôležitosť systematic backups

**Vytvorené scripty (16 total):**
1. `scripts/day5_preflight_check.py` - Validačný script pre DAY 5
2. `scripts/create_day5_preflight_check.py` - Utility na vytvorenie preflight
3. `scripts/fix_day5_preflight_issues.py` - Auto-fix pre common issues
4. `scripts/deploy_to_deployment.py` - Deployment helper (updated)
5. `scripts/fix_escape_sequence_warning.py` - Warning fixer
6. `scripts/diagnose_pillow_import.py` - Pillow diagnostika
7. `scripts/fix_preflight_config_path.py` - Config path fixer
8. `scripts/fix_sqlite_check_final.py` - SQLite check update
9. `scripts/fix_pillow_import_name.py` - Pillow import fixer
10. `scripts/test_preflight_in_development.py` - Testing script
11. `scripts/diagnose_deployment_issues.py` - Deployment diagnostika
12. `scripts/analyze_config_location.py` - Config analysis
13. `scripts/diagnose_service_status_check.py` - Service status diagnostika
14. `scripts/fix_manage_service_emoji.py` - Emoji removal (unused)
15. `scripts/fix_manage_service_complete.py` - Service script update
16. `scripts/recreate_manage_service.py` - Service reconstruction ⭐ NEW

**Fixes aplikované:**
- ✅ Config path: `apps/supplier-invoice-loader/config/config.yaml`
- ✅ PostgreSQL password z `POSTGRES_PASSWORD` environment variable
- ✅ SQLite check: Optional (len ak je v config)
- ✅ Pillow dependency: Pridaný do requirements.txt
- ✅ Pillow import: `"pillow"` → `"PIL"` (correct import name)
- ✅ PyYAML: Pridaný do requirements.txt (loader + scripts)
- ✅ Žiadne escape sequence warnings
- ✅ manage_service.py: Rekonštruovaný bez emoji (pure ASCII)

**Critical Learning:**
1. **NEVER fix directly in Deployment** - vždy Development → Git → Deployment
2. Git môže obsahovať už corrupt súbory - backupy sú kritické
3. Conversation search v Claude je powerful tool na recovery
4. Package name ≠ Import name (pillow vs PIL)
5. Config.yaml môže byť v subdirectories (apps/), nie len v root

**Next Steps:**
1. Redeploy s recreate_manage_service.py
2. Test service status v Deployment
3. Vytvorit performance baseline
4. Dosiahnuť 6/6 preflight checks
5. Start DAY 5 testing (Error Handling & Recovery)

---

## 📋 Previous Sessions

### DAY 1-4: NEX Automat v2.0 Deployment (2025-11-19 - 2025-11-21)

**Completed Phases:**
- DAY 1: ✅ Monorepo Migration (Complete)
- DAY 2: ✅ Backup & Recovery Systems (Complete)
- DAY 3: ✅ Service Installation & Validation (Complete)
- DAY 4: ✅ Integration & E2E Testing (Complete)

**Major Achievements:**
- Complete monorepo migration (2 apps, 2 packages)
- Windows Service installation (NSSM)
- PostgreSQL integration
- E2E testing: 100% success (8/8 tests passed)
- Performance baseline: 6ms health, 5s/invoice
- 4 critical deployment bugs fixed

**Known Issues from DAY 4:**
1. ✅ Missing pdfplumber - RESOLVED (added to requirements.txt)
2. ✅ Missing pg8000 - RESOLVED (added to requirements.txt)
3. ✅ Missing LS_API_KEY - DOCUMENTED
4. ✅ Missing POSTGRES_PASSWORD - DOCUMENTED + environment variable solution

**Target:** Go-Live 2025-11-27 (4 days remaining)

---

## 🗂️ Monorepo Structure

```
C:/Development/nex-automat/
├── apps/
│   ├── supplier-invoice-loader/        ✅ Main application
│   │   ├── src/
│   │   ├── tests/
│   │   ├── config/
│   │   │   └── config.yaml            ⭐ Config location!
│   │   ├── scripts/
│   │   └── requirements.txt           ✅ Updated (pillow, PyYAML)
│   └── supplier-invoice-editor/
│       └── config/config.yaml
│
├── packages/
│   ├── invoice-shared/                 ✅ Shared utilities
│   └── nex-shared/
│
├── docs/
│   ├── guides/
│   ├── deployment/
│   │   ├── DEPLOYMENT_GUIDE.md
│   │   ├── KNOWN_ISSUES.md
│   │   └── TROUBLESHOOTING.md
│   ├── SESSION_NOTES.md               (this file)
│   └── PROJECT_MANIFEST.json
│
├── scripts/                            ⭐ 16 utility scripts
│   ├── day5_preflight_check.py
│   ├── recreate_manage_service.py     ✅ NEW - Service recovery
│   ├── deploy_to_deployment.py
│   ├── manage_service.py              ⚠️ TO BE RECREATED
│   ├── test_e2e_workflow.py
│   └── ... (11 more)
│
├── tools/
│   └── nssm/                          ✅ Windows Service Manager
│
├── venv32/                            (Python 3.13.7 32-bit)
├── pyproject.toml
├── README.md
└── .gitignore
```

---

## 🔧 Technical Details

### Python Environment
- **Version:** Python 3.13.7 32-bit
- **Virtual Environment:** venv32
- **Reason:** Btrieve requires 32-bit (NEX Genesis ERP)
- **Package Manager:** pip

### Key Dependencies
**supplier-invoice-loader:**
- fastapi, uvicorn, pypdf, pdfplumber ✅
- pillow>=10.0.0 ✅ (ADDED DAY 5)
- PyYAML>=6.0.0 ✅ (ADDED DAY 5)
- pg8000, httpx, pydantic ✅

**Development:**
- pytest, pytest-asyncio, black, ruff ✅

### Configuration Management
- **Main config:** `apps/supplier-invoice-loader/config/config.yaml`
- **Environment variables (CRITICAL):**
  - `POSTGRES_PASSWORD` - PostgreSQL authentication
  - `LS_API_KEY` - API authentication

### Database Setup
- **PostgreSQL:** localhost:5432/invoice_staging (PRIMARY)
- **SQLite:** Optional (not used by default)

---

## 📊 Test Coverage

**Overall:** 71/86 tests passing (83%)

**supplier-invoice-loader:**
- Unit tests: 61/72 (85%)
- E2E tests: 8/8 (100%)
- Performance: Baseline established

**DAY 5 Preflight Tests (Development):**
- Config Loading: ✅ PASS
- Database Connectivity: ✅ PASS (PostgreSQL + SQLite detection)
- Dependencies: ✅ PASS (all 9 including PIL, yaml)
- Preflight Script Syntax: ✅ PASS

**DAY 5 Preflight Tests (Deployment):**
- Service Status: ❌ FAIL (manage_service.py corrupt)
- Database Connectivity: ✅ PASS
- Dependencies: ✅ PASS
- Known Issues: ✅ PASS
- Test Data: ✅ PASS
- Performance Baseline: ⚠️ MISSING (not critical)

---

## 🚀 Deployment Workflow

### Development → Git → Deployment (MANDATORY)

**1. Development (C:\Development\nex-automat)**
- All code changes here
- Install dependencies in venv32
- Run tests
- Fix issues

**2. Git Operations**
- `git add .`
- `git commit -m "..."`
- `git push`

**3. Deployment (C:\Deployment\nex-automat)**
- `python scripts/deploy_to_deployment.py`
- Install missing dependencies
- Run preflight check
- Start/restart service

**CRITICAL:** Never fix directly in Deployment!

---

## 💡 Lessons Learned

### Session History

**DAY 1-4 (Monorepo + Deployment):**
1. 32-bit Python required for Btrieve compatibility
2. NSSM excellent for Windows Service management
3. PostgreSQL requires proper password handling
4. E2E testing catches deployment issues early
5. Performance baseline essential for validation

**DAY 5 (Pre-Flight System + Recovery):**
1. **Development → Git → Deployment workflow is MANDATORY**
2. Never apply fixes only to Deployment (causes inconsistency)
3. Git can contain corrupt files - verify before restore
4. Conversation search powerful for code recovery
5. Config.yaml location: app-specific, not root
6. Package name ≠ Import name (pillow package → import PIL)
7. Environment variables better than hardcoded passwords
8. SQLite can be optional if PostgreSQL is primary
9. Preflight checks essential before production testing
10. Backups critical - even in Development

---

## 📝 Work Rules & Guidelines

### Critical Rules (from memory_user_edits)
1. Single solution only, no alternatives unless requested
2. One step at a time, wait for confirmation
3. Token usage stats at end of each response
4. Slovak language, English for technical terms
5. All code/configs in artifacts
6. Step-by-step approach, never multiple steps at once
7. Quality over speed
8. All changes via scripts
9. User does Git operations himself
10. **Development → Git → Deployment workflow (MANDATORY)**

### Script Naming Convention
- `fix_*.py` - Fixes issues
- `create_*.py` - Creates new files
- `test_*.py` - Testing scripts
- `deploy_*.py` - Deployment helpers
- `manage_*.py` - Management utilities
- `diagnose_*.py` - Diagnostic tools
- `recreate_*.py` - Recovery/reconstruction

---

## 📋 Next Session Priorities

### IMMEDIATE: Complete DAY 5 Preparation

**Phase 1: Service Recovery (HIGH PRIORITY)**
1. Run recreate_manage_service.py v Development
2. Verify script size (~10KB, not 453 bytes)
3. Deploy to Deployment
4. Test service status command
5. Achieve 6/6 preflight checks

**Phase 2: Performance Baseline (MEDIUM)**
- Create test_performance.py if missing
- Run performance tests
- Generate baseline.json
- Document metrics

**Phase 3: Start DAY 5 Testing**
- Error handling tests (invalid PDFs, network failures)
- Recovery tests (service crash, DB restore)
- 24-hour stability test (overnight)
- Go-live preparation

**Target:** 2025-11-27 Go-Live (4 days remaining)

---

## 🔗 Resources

**GitHub Repository:**
- https://github.com/rauschiccsk/nex-automat

**Key Documentation:**
- `docs/deployment/DEPLOYMENT_GUIDE.md`
- `docs/deployment/KNOWN_ISSUES.md`
- `docs/deployment/TROUBLESHOOTING.md`
- `docs/SESSION_NOTES.md` (this file)

**Customer:** Mágerstav s.r.o.  
**Developer:** Zoltán Rausch (rausch@icc.sk)  
**Company:** ICC Komárno - Innovation & Consulting Center

---

**Last Updated:** 2025-11-22  
**Status:** ⚠️ SERVICE RECOVERY IN PROGRESS  
**Progress:** 90/100 (ON TRACK for 2025-11-27 with recovery complete)