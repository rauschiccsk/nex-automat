"""
Script 13: Extract Pre-Deployment Checklist Template
Creates generic template + archives Mágerstav-specific version
"""

import os
import shutil
from pathlib import Path


def create_generic_template():
    """Create generic Pre-Deployment checklist template"""
    template = """# Pre-Deployment Checklist - NEX Automat

**Customer:** [CUSTOMER_NAME]  
**Target Deployment:** [YYYY-MM-DD]  
**Version:** [VERSION]

---

## Infrastructure Verification

### Database

- [ ] PostgreSQL 15+ running
- [ ] Database `invoice_staging` exists
- [ ] All tables created and verified
- [ ] Test data inserted and queried successfully
- [ ] Connection from production environment tested
- [ ] Password configured in environment variable `POSTGRES_PASSWORD`

**Verification Command:**

```bash
psql -U postgres -d invoice_staging -c "\\dt"
```

### NEX Genesis Integration

- [ ] NEX Genesis Server running on localhost:8080
- [ ] API endpoint accessible: http://localhost:8080/api
- [ ] NEX data directory accessible
- [ ] Test API call successful
- [ ] API key configured (if required)

**Verification Command:**

```bash
curl http://localhost:8080/api/health
```

### File System

- [ ] Production directory exists: C:\\Deployment\\nex-automat\\
- [ ] Storage directories created and writable:
  - C:\\NEX\\IMPORT\\pdf\\
  - C:\\NEX\\IMPORT\\xml\\
  - C:\\NEX\\IMPORT\\temp\\
  - C:\\NEX\\IMPORT\\archive\\
  - C:\\NEX\\IMPORT\\error\\
- [ ] Backup directory created: C:\\Deployment\\nex-automat\\backups\\
- [ ] Log directory created: C:\\Deployment\\nex-automat\\logs\\
- [ ] Sufficient disk space (minimum 50 GB free)

**Verification Command:**

```powershell
Get-PSDrive C | Select-Object Used,Free
```

---

## Application Verification

### Python Environment

- [ ] Python 3.13 32-bit installed
- [ ] Virtual environment created: venv32\\
- [ ] All dependencies installed (requirements.txt)
- [ ] Shared packages installed:
  - nex-shared
  - nexdata

**Verification Command:**

```bash
cd C:\\Deployment\\nex-automat
venv32\\Scripts\\activate
pip list | findstr nex
```

### Configuration

- [ ] Production config exists: apps\\supplier-invoice-loader\\config\\config.yaml
- [ ] All required settings configured:
  - customer
  - storage paths
  - database connection
  - PostgreSQL staging enabled
- [ ] No sensitive data in config (using environment variables)
- [ ] Config validated successfully

**Verification Command:**

```bash
python scripts\\validate_config.py
```

### Tests

- [ ] All unit tests passing
- [ ] Functional tests skipped (expected)
- [ ] No test errors or failures
- [ ] Test coverage acceptable (85%+)

**Verification Command:**

```bash
cd apps\\supplier-invoice-loader
pytest tests/ -v
```

---

## Windows Service

### NSSM Installation

- [ ] NSSM 2.24+ downloaded and extracted
- [ ] NSSM executable verified: tools\\nssm\\win32\\nssm.exe
- [ ] NSSM version command works

**Verification Command:**

```powershell
C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe version
```

### Service Configuration

- [ ] Service created: NEX-Automat-Loader
- [ ] Display name set correctly
- [ ] Description set correctly
- [ ] Python executable path correct
- [ ] Main script path correct: apps\\supplier-invoice-loader\\main.py
- [ ] Working directory set correctly
- [ ] Startup type: Automatic (Delayed Start)
- [ ] Recovery: Restart on failure (0s delay)
- [ ] Logging configured (stdout/stderr)

**Verification Command:**

```powershell
C:\\Deployment\\nex-automat\\tools\\nssm\\win32\\nssm.exe status NEX-Automat-Loader
```

### Service Functionality

- [ ] Service starts successfully
- [ ] Service status: RUNNING
- [ ] API accessible: http://localhost:8000/health
- [ ] No Unicode errors in logs
- [ ] Logs being written correctly
- [ ] Service survives manual stop/start
- [ ] Auto-restart works after process kill

**Verification Commands:**

```powershell
python scripts\\manage_service.py status
Invoke-WebRequest -Uri http://localhost:8000/health
python scripts\\manage_service.py logs
```

---

## API Endpoints Verification

- [ ] Health check: GET http://localhost:8000/health
- [ ] API documentation: http://localhost:8000/docs
- [ ] ReDoc: http://localhost:8000/redoc
- [ ] Invoice endpoints respond correctly
- [ ] Database queries work through API

**Test Commands:**

```powershell
# Health check
Invoke-WebRequest -Uri http://localhost:8000/health

# List invoices
Invoke-WebRequest -Uri http://localhost:8000/api/invoices

# Check staging
Invoke-WebRequest -Uri http://localhost:8000/api/staging/invoices
```

---

## Security & Permissions

- [ ] Service runs with appropriate privileges
- [ ] File system permissions set correctly
- [ ] Database credentials secure (environment variables)
- [ ] No sensitive data in logs
- [ ] No hardcoded passwords in code
- [ ] Production config not committed to Git

---

## Monitoring & Logging

- [ ] Log rotation configured (daily, 10MB max)
- [ ] Logs readable and parseable
- [ ] No sensitive data in logs
- [ ] Log directory has sufficient space
- [ ] Backup logs created for service
- [ ] Application logs operational

**Log Files:**

- `logs\\service-stdout.log` - Service output
- `logs\\service-stderr.log` - Service errors
- `logs\\app-*.log` - Application logs

---

## Backup & Recovery

- [ ] Backup directory created
- [ ] Backup scripts tested
- [ ] Database backup tested
- [ ] Configuration backup tested
- [ ] Recovery procedures documented
- [ ] Restore tested successfully

---

## Documentation

- [ ] DEPLOYMENT_GUIDE.md complete
- [ ] SERVICE_MANAGEMENT.md complete
- [ ] TROUBLESHOOTING.md complete
- [ ] PRE_DEPLOYMENT_CHECKLIST.md complete (this file)
- [ ] README updated with production info
- [ ] API documentation generated

---

## Final Verification

### Smoke Tests

- [ ] Service starts automatically after server reboot
- [ ] Application survives 24-hour run
- [ ] No memory leaks detected
- [ ] No CPU spikes observed
- [ ] Log rotation working
- [ ] Auto-restart working

### Performance

- [ ] API response time < 500ms
- [ ] Database queries optimized
- [ ] No connection pool exhaustion
- [ ] Memory usage stable
- [ ] Disk I/O acceptable

### Integration

- [ ] NEX Genesis API integration working
- [ ] PostgreSQL staging working
- [ ] File processing working
- [ ] Email notifications working (if enabled)
- [ ] n8n webhooks working (if enabled)

---

## Sign-Off

**Checklist Completed By:** _________________  
**Date:** _________________  
**Approved By:** _________________  
**Deployment Date:** _________________

---

## Notes

*Add any additional notes, concerns, or observations here:*

---

**Status:** [ ] READY FOR PRODUCTION  
**Last Updated:** 2025-12-15  
**Version:** 1.0
"""
    return template


def extract_and_archive():
    """Extract template and archive Mágerstav version"""

    repo_root = Path(r"C:\Development\nex-automat")
    old_file = repo_root / "docs" / "deployment" / "PRE_DEPLOYMENT_CHECKLIST.md-old"
    template_file = repo_root / "docs" / "deployment" / "PRE_DEPLOYMENT_CHECKLIST.md"
    archive_dir = repo_root / "docs" / "archive" / "deployments"
    archive_file = archive_dir / "PRE_DEPLOYMENT_CHECKLIST_MAGERSTAV_2025-11-27.md"
    archive_index = repo_root / "docs" / "archive" / "00_ARCHIVE_INDEX.md"

    print("🔄 Extracting Pre-Deployment Checklist Template...")
    print()

    # 1. Create generic template
    template = create_generic_template()
    with open(template_file, 'w', encoding='utf-8') as f:
        f.write(template)
    print(f"✅ Created: {template_file.relative_to(repo_root)}")
    print("   Generic Pre-Deployment checklist template")
    print()

    # 2. Archive Mágerstav-specific version
    if old_file.exists():
        shutil.move(str(old_file), str(archive_file))
        print(f"✅ Archived: {old_file.name}")
        print(f"   → {archive_file.relative_to(repo_root)}")
    else:
        print(f"❌ Not found: {old_file}")
        return

    print()

    # 3. Update archive index
    if archive_index.exists():
        with open(archive_index, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find Deployment Records section and add entry
        if "## Deployment Records" in content:
            lines = content.split('\n')
            # Find the checklist entry and add after it
            insert_idx = None
            for i, line in enumerate(lines):
                if "Mágerstav Go-Live Checklist" in line:
                    insert_idx = i + 1
                    break

            if insert_idx:
                new_entry = "- **2025-11-27** - [Mágerstav Pre-Deployment Checklist](deployments/PRE_DEPLOYMENT_CHECKLIST_MAGERSTAV_2025-11-27.md) - Infrastructure and application verification"
                lines.insert(insert_idx, new_entry)
                content = '\n'.join(lines)

        with open(archive_index, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Updated: {archive_index.relative_to(repo_root)}")
        print("   Added pre-deployment checklist entry")

    print()
    print("=" * 60)
    print("✅ MIGRATION COMPLETE")
    print("=" * 60)
    print()
    print("Summary:")
    print(f"  • Created: docs/deployment/PRE_DEPLOYMENT_CHECKLIST.md (template)")
    print(f"  • Archived: PRE_DEPLOYMENT_CHECKLIST_MAGERSTAV_2025-11-27.md")
    print(f"  • Updated: Archive index")
    print()


if __name__ == "__main__":
    extract_and_archive()