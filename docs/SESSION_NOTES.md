# NEX Automat - Session Notes

**Project:** nex-automat  
**Location:** C:/Development/nex-automat  
**Current Phase:** DAY 5 Preparation - Pre-Flight Check System

---

## 🎯 Current Status

### DAY 5 - Pre-Flight Check System (2025-11-22) ✅ COMPLETE

**Goal:** Pripravit validačný systém pre DAY 5 testing (Error Handling & Recovery)

**Úlohy:**
- [x] Vytvorený day5_preflight_check.py s all fixes
- [x] Nainštalovaný pillow do Development venv32
- [x] Pridaný pillow do requirements.txt
- [x] Opravený PostgreSQL password handling (environment variable)
- [x] Opravený SQLite path detection (config.yaml + multiple locations)
- [x] Vytvorený deployment helper script
- [x] Opravené všetky escape sequence warnings
- [x] Pridané nové workflow pravidlo: Development → Git → Deployment

**Vytvorené scripty:**
1. `scripts/day5_preflight_check.py` - Validačný script pre DAY 5
2. `scripts/create_day5_preflight_check.py` - Utility na vytvorenie preflight
3. `scripts/fix_day5_preflight_issues.py` - Auto-fix pre common issues
4. `scripts/deploy_to_deployment.py` - Deployment helper
5. `scripts/fix_escape_sequence_warning.py` - Warning fixer

**Fixes aplikované:**
- ✅ PostgreSQL password z `POSTGRES_PASSWORD` environment variable
- ✅ SQLite path detection z config.yaml + fallback locations
- ✅ Pillow dependency nainštalovaný a pridaný do requirements.txt
- ✅ Žiadne escape sequence warnings
- ✅ Správny Development → Git → Deployment workflow

**Critical Learning:**
- **NEVER fix directly in Deployment** - vždy Development → Git → Deployment
- Zabezpečuje konzistenciu medzi prostredimi
- Umožňuje čistý redeploy bez straty fixes
- Predchádza "deployment drift" problémom

**Next Steps:**
1. Git commit + push
2. Deploy to Deployment: `python scripts/deploy_to_deployment.py`
3. Install pillow in Deployment: `pip install pillow`
4. Run preflight check: `python scripts/day5_preflight_check.py`
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
1. ✅ Missing pdfplumber - RESOLVED
2. ✅ Missing pg8000 - RESOLVED
3. ✅ Missing LS_API_KEY - DOCUMENTED
4. ✅ Missing POSTGRES_PASSWORD - DOCUMENTED

**Target:** Go-Live 2025-11-27 (5 days remaining)

---

## 🗂️ Monorepo Structure

```
C:/Development/nex-automat/
├── apps/
│   ├── supplier-invoice-loader/        ✅ 61/72 tests passing (85%)
│   │   ├── src/
│   │   ├── tests/
│   │   ├── scripts/
│   │   └── pyproject.toml
│   └── supplier-invoice-editor/        ✅ 10/14 tests passing (71%)
│       ├── src/
│       ├── tests/
│       └── pyproject.toml
│
├── packages/
│   ├── invoice-shared/                 ✅ Shared utilities
│   │   └── invoice_shared/
│   │       ├── database/
│   │       ├── utils/
│   │       ├── models/
│   │       └── schemas/
│   └── nex-shared/                     ✅ Placeholder
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
├── scripts/
│   ├── day5_preflight_check.py        ✅ NEW (DAY 5)
│   ├── create_day5_preflight_check.py ✅ NEW (DAY 5)
│   ├── fix_day5_preflight_issues.py   ✅ NEW (DAY 5)
│   ├── deploy_to_deployment.py        ✅ NEW (DAY 5)
│   ├── manage_service.py
│   ├── test_e2e_workflow.py
│   └── test_performance.py
│
├── venv32/                            (Python 3.13.7 32-bit)
├── pyproject.toml                     (UV workspace config)
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
- pillow>=10.0.0 ✅ (added DAY 5)
- pg8000, httpx, pydantic ✅

**Development:**
- pytest, pytest-asyncio, black, ruff ✅

### Configuration Management
- `config/config.yaml` - Main configuration
- `POSTGRES_PASSWORD` - Environment variable (required)
- `LS_API_KEY` - Environment variable (required)

### Database Setup
- **PostgreSQL:** localhost:5432/invoice_staging
- **SQLite:** Configurable path via config.yaml

---

## 📊 Test Coverage

**Overall:** 71/86 tests passing (83%)

**supplier-invoice-loader:**
- Unit tests: 61/72 (85%)
- E2E tests: 8/8 (100%)
- Performance: Baseline established

**supplier-invoice-editor:**
- Unit tests: 10/14 (71%)

---

## 🚀 Deployment Workflow

### Development → Git → Deployment

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

**DAY 5 (Pre-Flight System):**
1. **Development → Git → Deployment workflow is MANDATORY**
2. Never apply fixes only to Deployment (causes inconsistency)
3. Preflight checks catch environment issues before testing
4. Environment variables better than hardcoded passwords
5. Config.yaml should be source of truth for paths
6. Escape sequences in docstrings cause warnings

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

---

## 📋 Next Session Priorities

### DAY 5: Error Handling & Recovery Testing

**Phase 1: Error Handling (2 hours)**
- Invalid PDF formats
- Network failures
- Database connection loss
- Disk full scenarios
- NEX Genesis unavailable

**Phase 2: Recovery Testing (2 hours)**
- Service crash recovery
- Database restore procedures
- Configuration rollback
- Backup validation

**Phase 3: Stability Test (overnight)**
- 24-hour continuous operation
- Memory leak detection
- Log rotation validation
- Performance consistency

**Phase 4: Go-Live Preparation (2 hours)**
- Final checklist review
- Deployment package creation
- Customer documentation
- Rollback plan finalization

**Target:** 2025-11-27 Go-Live (5 days)

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
**Status:** 🟢 DAY 5 PREPARATION COMPLETE  
**Progress:** 90/100 (ON TRACK for 2025-11-27)