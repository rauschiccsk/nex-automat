# NEX Automat - New Chat Initialization

**Project:** nex-automat  
**Location:** C:/Development/nex-automat  
**GitHub:** https://github.com/rauschiccsk/nex-automat  
**Session:** DAY 2 - Backup & Recovery System  
**Date:** 2025-11-21

---

## 📋 Quick Context

Claude, prosím načítaj kontext projektu pomocou týchto manifestov:

### Root Overview
```
web_fetch('https://raw.githubusercontent.com/rauschiccsk/nex-automat/main/docs/PROJECT_MANIFEST.json')
```

### Session Notes
```
web_fetch('https://raw.githubusercontent.com/rauschiccsk/nex-automat/main/docs/SESSION_NOTES.md')
```

### Supplier Invoice Loader (pracujeme na tomto)
```
web_fetch('https://raw.githubusercontent.com/rauschiccsk/nex-automat/main/docs/apps/supplier-invoice-loader.json')
```

---

## 🎯 Current Project Status

### ✅ COMPLETE - DAY 1 (2025-11-20)
**Monitoring & Health Checks System:**
- ✅ Health Monitor (7 tests passing)
  - System metrics (CPU, RAM, Disk)
  - Database status checking
  - Invoice statistics tracking
  - Uptime monitoring
  - File: `src/monitoring/health_monitor.py`

- ✅ Alert Manager (9 tests passing)
  - Critical/Warning/Info alerts
  - Email notifications (HTML)
  - Daily summaries
  - Weekly reports
  - Multiple recipients
  - File: `src/monitoring/alert_manager.py`

- ✅ Log Manager (12 tests passing)
  - Automatic rotation (10 MB)
  - Retention (30 days)
  - JSON structured logging
  - Log analysis utilities
  - File: `src/monitoring/log_manager.py`

**Test Status:** 28/28 monitoring tests passing (100%) ✅  
**Dependencies:** psutil>=5.9.0 installed

---

## 🚀 TODAY'S PRIORITY - DAY 2

### Backup & Recovery System (3 hours)

**Tasks:**
1. **Database Backup Script** (1.5h)
   - PostgreSQL automated backup
   - Incremental backups
   - Backup rotation (7 daily, 4 weekly)
   - Compression (gzip)
   - Backup verification
   - Cloud storage support (optional)

2. **Configuration Backup** (0.5h)
   - Config files backup
   - Environment variables backup
   - Encryption for sensitive data

3. **Recovery Documentation** (1h)
   - Step-by-step recovery guide
   - RTO/RPO definitions
   - Disaster recovery scenarios
   - Recovery testing checklist

**Deliverables:**
- `scripts/backup_database.py`
- `scripts/restore_database.py`
- `scripts/backup_config.py`
- `docs/deployment/RECOVERY_GUIDE.md`
- Windows Task Scheduler config
- Tests for backup scripts

---

## 🗂️ Project Structure

```
nex-automat/
├── apps/
│   ├── supplier-invoice-loader/
│   │   ├── src/
│   │   │   ├── monitoring/              ✅ NEW (DAY 1)
│   │   │   │   ├── health_monitor.py
│   │   │   │   ├── alert_manager.py
│   │   │   │   └── log_manager.py
│   │   │   ├── api/
│   │   │   ├── business/
│   │   │   ├── database/
│   │   │   ├── extractors/
│   │   │   └── utils/
│   │   ├── tests/
│   │   │   └── unit/
│   │   │       ├── test_health_monitor.py    ✅ 7 passing
│   │   │       ├── test_alert_manager.py     ✅ 9 passing
│   │   │       └── test_log_manager.py       ✅ 12 passing
│   │   ├── scripts/                     ⏳ TODAY: backup scripts
│   │   ├── docs/
│   │   │   └── deployment/              ⏳ TODAY: RECOVERY_GUIDE.md
│   │   ├── main.py
│   │   ├── requirements.txt             ✅ UPDATED (psutil)
│   │   └── pyproject.toml
│   └── supplier-invoice-editor/
├── packages/
│   ├── invoice-shared/
│   └── nex-shared/
├── docs/
│   ├── SESSION_NOTES.md                 ✅ UPDATED
│   ├── INIT_PROMPT_NEW_CHAT.md          ✅ THIS FILE
│   └── PROJECT_MANIFEST.json
└── venv32/                              ✅ Python 3.13.7 32-bit
```

---

## 🔧 Environment

**Python:** 3.13.7 32-bit (Btrieve compatibility)  
**venv:** venv32 (gitignored)  
**Package Manager:** pip  
**IDE:** PyCharm

**Key Dependencies:**
- FastAPI, Uvicorn (loader)
- PyQt5, PyYAML (editor)
- asyncpg, pg8000 (PostgreSQL)
- psutil>=5.9.0 (system metrics)
- invoice-shared (workspace package)

---

## 🧪 Testing Status

```bash
# Current test status
pytest apps/supplier-invoice-loader/tests/unit/ -v

# Expected results:
# - test_health_monitor.py: 7 passed
# - test_alert_manager.py: 9 passed
# - test_log_manager.py: 12 passed
# Total: 28 passed
```

---

## 📊 Deployment Timeline

```
✅ DAY 1 (2025-11-20): Monitoring & Health Checks - COMPLETE
⏳ DAY 2 (2025-11-21): Backup & Recovery - TODAY
⏳ DAY 3 (2025-11-22): Error Handling & Retry Logic
⏳ DAY 4 (2025-11-23): Configuration & Security
⏳ DAY 5 (2025-11-24): Production Testing & Performance
⏳ DAY 6 (2025-11-25): Documentation & Runbooks
⏳ DAY 7 (2025-11-27): Final Deployment & Handover
```

**Target Deployment:** 2025-11-27  
**Customer:** Mágerstav s.r.o.  
**Approach:** Comprehensive production-ready deployment

---

## 🎯 Success Criteria

**Technical:**
- ✅ 99.9% uptime target
- ✅ <2s API response time (p95)
- ✅ <5min invoice processing time
- ✅ Automated daily backups (TODAY)
- ✅ Real-time alerting functional (DONE)
- ✅ All tests passing (target: 100+)
- ✅ Zero critical security issues
- ✅ Complete documentation

**Business:**
- ✅ Customer can process invoices independently
- ✅ Support team can troubleshoot issues
- ✅ Recovery procedures tested (TODAY)
- ✅ SLA commitments met
- ✅ Customer satisfaction achieved

---

## 💡 Key Reminders

### Critical Rules:
1. **Provide single solution only** - no alternatives unless requested
2. **One step at a time** - wait for confirmation
3. **Generate everything into artifacts** - code, configs, docs
4. **All fixes via .py scripts** - never .ps1 alternatives
5. **Quality over speed** - systematic approach
6. **No emoji in scripts** - Windows encoding issues

### Technical:
- **32-bit Python only** (Btrieve requirement)
- **Install order matters:** packages first, then apps
- **Always run tests** before committing
- **psutil installation:** use `--only-binary :all:`

### Git Operations:
- User handles commits and pushes himself
- User generates manifests himself
- Claude provides commit messages in plain text

---

## 📋 Today's Work Plan (DAY 2)

### Step 1: Database Backup Script (1.5h)
Create `scripts/backup_database.py`:
- PostgreSQL pg_dump wrapper
- Incremental backup support
- Backup rotation logic (7 daily, 4 weekly)
- Compression (gzip)
- Backup verification
- Email notifications on failure
- Tests

### Step 2: Configuration Backup (0.5h)
Create `scripts/backup_config.py`:
- Backup config.yaml, .env files
- Encrypt sensitive data
- Store in secure location
- Tests

### Step 3: Restore Script (0.5h)
Create `scripts/restore_database.py`:
- PostgreSQL restore from backup
- Verify data integrity
- Tests

### Step 4: Recovery Documentation (1h)
Create `docs/deployment/RECOVERY_GUIDE.md`:
- Step-by-step procedures
- RTO/RPO definitions
- Disaster scenarios
- Testing checklist
- Contact information

### Step 5: Windows Task Scheduler (0.5h)
- Daily backup schedule configuration
- PowerShell script for Task Scheduler
- Logging configuration

---

## 🔒 Database Configuration

**Database:** invoice_staging (PostgreSQL)  
**Main Table:** invoices_pending  
**Connection:** pg8000 driver (pure Python)

**Connection Details:**
```yaml
database:
  postgres:
    host: localhost
    port: 5432
    database: invoice_staging
    user: postgres
    password: ${ENV:POSTGRES_PASSWORD}
```

---

## 🚨 Important Notes

### Backup Strategy:
- **Daily backups:** Keep 7 days
- **Weekly backups:** Keep 4 weeks
- **Compression:** gzip level 6
- **Verification:** SHA256 checksums
- **Storage:** Local + optional cloud
- **Encryption:** AES-256 for configs

### Recovery Objectives:
- **RTO (Recovery Time Objective):** <1 hour
- **RPO (Recovery Point Objective):** <24 hours
- **Data Loss Tolerance:** Max 1 day

---

## ✅ Pre-Session Checklist

Before starting work:
- [ ] Load PROJECT_MANIFEST.json
- [ ] Read SESSION_NOTES.md for current status
- [ ] Verify venv32 is activated
- [ ] Confirm monitoring modules working
- [ ] Review DAY 2 requirements

---

## 📞 Support Information

**Developer:** Zoltán Rausch (rausch@icc.sk)  
**Organization:** ICC Komárno - Innovation & Consulting Center  
**Customer:** Mágerstav s.r.o.  
**Project Version:** 2.0.0  
**Status:** DAY 1 Complete ✅, DAY 2 In Progress ⏳

---

**Ready to start DAY 2 - Backup & Recovery System!**