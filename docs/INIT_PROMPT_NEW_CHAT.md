# Init Prompt - Post Go-Live / Next Development Phase

**Project:** NEX Automat v2.0 - Supplier Invoice Loader  
**Customer:** Mágerstav s.r.o.  
**Last Session:** 2025-11-25 (Git workflow, documentation)  
**This Session:** TBD (Go-Live or Development continuation)  

---

## Quick Context

NEX Automat v2.0 je pripravený na produkčné nasadenie u zákazníka Mágerstav s.r.o.

**Aktuálny stav:**
- Version: 2.0.0 (tagged)
- Status: 🟢 Ready for Production
- Go-Live Target: 2025-11-27
- All tests: PASS

---

## Git Structure

**Branches:**
- `main` - Production (v2.0.0 tagged, ready for deployment)
- `develop` - Active development (uncommitted changes from last session)
- `hotfix_v2.0` - Bugfixes for production

**Workflow:**
- New features → `develop` → `main` (at release)
- Bugfixes → `hotfix_v2.0` → `main` + merge to `develop`

**See:** `docs/GIT_GUIDE.md` for PyCharm workflow

---

## Pending Actions from Last Session

### Must Complete Before Go-Live

1. **Commit Pending Changes**
   ```
   Branch: develop
   Files: GIT_GUIDE.md, scripts (branching, shortcuts, cleanup), deployment docs
   Message: See COMMIT_MESSAGE.txt artifact from last session
   ```

2. **Run Cleanup**
   ```
   scripts/cleanup_backups.ps1
   - Removes temp fix scripts
   - Removes backup files (*.md.backup, *.md.corrupted)
   ```

3. **Verify Desktop Shortcuts**
   ```
   scripts/create_desktop_shortcuts.ps1
   Location: Desktop/NEX Automat Docs
   ```

---

## Possible Session Scenarios

### Scenario A: Go-Live Deployment (2025-11-27)

**Follow:** `docs/deployment/DEPLOYMENT_GUIDE.md`

**Key Steps:**
1. Pre-deployment checklist (PRE_DEPLOYMENT_CHECKLIST.md)
2. Run deploy_fresh.py at customer
3. Configure customer settings
4. Install Windows service
5. Validation tests (preflight, error handling, performance)
6. Monitor for 4+ hours

**Documents needed:**
- DEPLOYMENT_GUIDE.md
- GO_LIVE_CHECKLIST.md
- SERVICE_MANAGEMENT.md
- TROUBLESHOOTING.md

### Scenario B: Post Go-Live Support

**Focus:**
- Monitor production service
- Handle any issues (see TROUBLESHOOTING.md)
- Customer support
- Performance optimization

### Scenario C: Next Development Phase

**Focus:**
- New features in `develop` branch
- Customer feedback implementation
- Performance improvements
- Additional customers

---

## Project Files Structure

```
C:\Development\nex-automat\
├── docs\
│   ├── SESSION_NOTES.md (current status)
│   ├── GIT_GUIDE.md (PyCharm workflow)
│   └── deployment\
│       ├── DEPLOYMENT_GUIDE.md
│       ├── GO_LIVE_CHECKLIST.md
│       ├── PRE_DEPLOYMENT_CHECKLIST.md
│       ├── SERVICE_MANAGEMENT.md
│       └── TROUBLESHOOTING.md
├── scripts\
│   ├── create_branches.ps1
│   ├── create_desktop_shortcuts.ps1
│   ├── cleanup_backups.ps1
│   ├── deploy_fresh.py (for customer deployment)
│   ├── manage_service.py
│   └── [validation scripts]
└── apps\
    └── supplier-invoice-loader\
```

---

## Key Information

### Customer Details
**Name:** Mágerstav s.r.o.  
**Deployment Path:** C:\Deployment\nex-automat  
**Database:** PostgreSQL - invoice_staging  
**Service:** NEX-Automat-Loader

### System Requirements
- Windows Server 2019/2022
- Python 3.13.0 32-bit
- PostgreSQL 15.14+
- NSSM 2.24

### Critical Configuration
- Environment variable: POSTGRES_PASSWORD
- Config: apps/supplier-invoice-loader/config/config.yaml
- Customer: MAGERSTAV
- Storage paths: C:\NEX\IMPORT\*

---

## Common Commands

### Git Operations
```powershell
# Check current branch
git branch --show-current

# Switch to develop
git checkout develop

# Commit changes
git add .
git commit -m "message"
git push origin develop
```

### Service Management (at customer)
```powershell
cd C:\Deployment\nex-automat
venv32\Scripts\activate

# Status
python scripts\manage_service.py status

# Logs
python scripts\manage_service.py logs

# Restart
python scripts\manage_service.py restart
```

### Deployment
```powershell
# At customer server
cd C:\Deployment
python deploy_fresh.py
```

---

## Testing Status

**Last Full Test:** 2025-11-24  
**Results:**
- Preflight: 6/6 PASS ✅
- Error Handling: 12/12 PASS ✅
- Performance: 6/6 PASS ✅
- Fresh Deployment: SUCCESS ✅

---

## Desktop Shortcuts

**Location:** Desktop/NEX Automat Docs

**Contents:**
- All Markdown documentation from Development
- Prefix "DEPLOY -" for deployment docs
- Opens with MarkText (or VS Code if configured)

**Refresh:** Run `scripts\create_desktop_shortcuts.ps1`

---

## Next Steps Checklist

**Before starting work:**
- [ ] Load SESSION_NOTES.md to understand current state
- [ ] Check Git branch (should be on `develop` or `hotfix_v2.0`)
- [ ] Review pending actions above
- [ ] Determine session scenario (A, B, or C)

**If Go-Live deployment:**
- [ ] Review DEPLOYMENT_GUIDE.md
- [ ] Review GO_LIVE_CHECKLIST.md
- [ ] Ensure all tools ready (USB with scripts, credentials)

**If continuing development:**
- [ ] Check for uncommitted changes
- [ ] Review GitHub issues/backlog
- [ ] Plan feature implementation

---

## Important Notes

- **Always check current branch before commits**
- **Development changes go to `develop` branch**
- **Production bugfixes go to `hotfix_v2.0` branch**
- **Never commit directly to `main`**
- **Desktop shortcuts point to Development, not Deployment**

---

## Contact

**Developer:** Zoltán Rausch  
**Company:** ICC Komárno  
**Email:** zoltan.rausch@icc.sk

---

**Last Updated:** 2025-11-25  
**Version:** 1.0  
**Status:** 🟢 Ready for Go-Live