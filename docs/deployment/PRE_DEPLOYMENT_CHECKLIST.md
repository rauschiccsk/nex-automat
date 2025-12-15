# Pre-Deployment Checklist - NEX Automat

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
psql -U postgres -d invoice_staging -c "\dt"
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

- [ ] Production directory exists: C:\Deployment\nex-automat\
- [ ] Storage directories created and writable:
  - C:\NEX\IMPORT\pdf\
  - C:\NEX\IMPORT\xml\
  - C:\NEX\IMPORT\temp\
  - C:\NEX\IMPORT\archive\
  - C:\NEX\IMPORT\error\
- [ ] Backup directory created: C:\Deployment\nex-automat\backups\
- [ ] Log directory created: C:\Deployment\nex-automat\logs\
- [ ] Sufficient disk space (minimum 50 GB free)

**Verification Command:**

```powershell
Get-PSDrive C | Select-Object Used,Free
```

---

## Application Verification

### Python Environment

- [ ] Python 3.13 32-bit installed
- [ ] Virtual environment created: venv32\
- [ ] All dependencies installed (requirements.txt)
- [ ] Shared packages installed:
  - nex-shared
  - nexdata

**Verification Command:**

```bash
cd C:\Deployment\nex-automat
venv32\Scripts\activate
pip list | findstr nex
```

### Configuration

- [ ] Production config exists: apps\supplier-invoice-loader\config\config.yaml
- [ ] All required settings configured:
  - customer
  - storage paths
  - database connection
  - PostgreSQL staging enabled
- [ ] No sensitive data in config (using environment variables)
- [ ] Config validated successfully

**Verification Command:**

```bash
python scripts\validate_config.py
```

### Tests

- [ ] All unit tests passing
- [ ] Functional tests skipped (expected)
- [ ] No test errors or failures
- [ ] Test coverage acceptable (85%+)

**Verification Command:**

```bash
cd apps\supplier-invoice-loader
pytest tests/ -v
```

---

## Windows Service

### NSSM Installation

- [ ] NSSM 2.24+ downloaded and extracted
- [ ] NSSM executable verified: tools\nssm\win32\nssm.exe
- [ ] NSSM version command works

**Verification Command:**

```powershell
C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe version
```

### Service Configuration

- [ ] Service created: NEX-Automat-Loader
- [ ] Display name set correctly
- [ ] Description set correctly
- [ ] Python executable path correct
- [ ] Main script path correct: apps\supplier-invoice-loader\main.py
- [ ] Working directory set correctly
- [ ] Startup type: Automatic (Delayed Start)
- [ ] Recovery: Restart on failure (0s delay)
- [ ] Logging configured (stdout/stderr)

**Verification Command:**

```powershell
C:\Deployment\nex-automat\tools\nssm\win32\nssm.exe status NEX-Automat-Loader
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
python scripts\manage_service.py status
Invoke-WebRequest -Uri http://localhost:8000/health
python scripts\manage_service.py logs
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

- `logs\service-stdout.log` - Service output
- `logs\service-stderr.log` - Service errors
- `logs\app-*.log` - Application logs

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
