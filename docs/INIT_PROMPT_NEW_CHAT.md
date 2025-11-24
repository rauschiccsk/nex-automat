# Init Prompt - Go-Live Deployment

**Project:** NEX Automat v2.0 - Supplier Invoice Loader  
**Customer:** Mágerstav s.r.o.  
**Current Progress:** 100% (Ready for Go-Live)  
**Last Session:** Fresh Deployment Test - SUCCESS (2025-11-24)  
**This Session:** Go-Live Deployment @ Customer  

---

## Quick Context

Projekt NEX Automat v2.0 - Go-Live nasadenie u zákazníka Mágerstav s.r.o.

**Stav projektu:**
- DAY 1-6: ✅ Complete
- Dress Rehearsal: ✅ Complete
- Fresh Deployment Test: ✅ Complete (all tests PASS)
- This Session: Go-Live @ Customer
- Target Date: 2025-11-27

---

## Session Goal

Nasadiť NEX Automat v2.0 na produkčný server zákazníka Mágerstav.

---

## Pre-Deployment Checklist

### On Customer Server (verify before deployment)

```
[ ] Python 3.13 32-bit installed
[ ] Git installed
[ ] PostgreSQL running
[ ] Database invoice_staging exists
[ ] NSSM at C:\Tools\nssm
[ ] Environment variable POSTGRES_PASSWORD set
[ ] Network access to GitHub
```

---

## Deployment Steps

### Step 1: Download and Run Deployment Script

```powershell
cd C:\Deployment

# Download deployment script
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/rauschiccsk/nex-automat/main/scripts/deploy_fresh.py" -OutFile "deploy_fresh.py"

# Run deployment
python deploy_fresh.py
```

### Step 2: Configure for Customer

Edit config files with customer-specific values:

```powershell
notepad C:\Deployment\nex-automat\apps\supplier-invoice-loader\config\config.yaml
notepad C:\Deployment\nex-automat\apps\supplier-invoice-loader\config\config_customer.py
```

**Key values to update:**
- `customer.name`: MAGERSTAV
- `customer.full_name`: Mágerstav s.r.o.
- `customer.ico`: actual IČO
- `email.operator`: actual operator email
- `security.encryption_key`: generate new key
- `NEX_GENESIS_API_URL`: actual server URL
- `OPERATOR_EMAIL`: actual email

### Step 3: Generate New Encryption Key

```powershell
cd C:\Deployment\nex-automat
.\venv32\Scripts\Activate.ps1
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy output to `config.yaml` → `security.encryption_key`

### Step 4: Restart Service

```powershell
python scripts\manage_service.py restart
```

### Step 5: Validate Deployment

```powershell
python scripts\preflight_check.py
python scripts\error_handling_tests.py
python scripts\performance_tests.py
```

**Expected Results:**
- Preflight: 6/6 PASS
- Error Handling: 12/12 PASS
- Performance: 6/6 PASS

---

## Service Management Commands

```powershell
cd C:\Deployment\nex-automat
.\venv32\Scripts\Activate.ps1

# Status
python scripts\manage_service.py status

# Start/Stop/Restart
python scripts\manage_service.py start
python scripts\manage_service.py stop
python scripts\manage_service.py restart

# View logs
python scripts\manage_service.py logs
```

---

## Troubleshooting

### Service won't start
```powershell
# Check logs
type logs\service-stderr.log

# Verify config
python scripts\validate_config.py
```

### Database connection failed
```powershell
# Test connection
python scripts\test_database_connection.py

# Check POSTGRES_PASSWORD
$env:POSTGRES_PASSWORD
```

### Missing dependencies
```powershell
.\venv32\Scripts\pip.exe install -r apps\supplier-invoice-loader\requirements.txt
```

---

## Success Criteria

Deployment is successful when:
- [ ] Service status: SERVICE_RUNNING
- [ ] Preflight: 6/6 PASS
- [ ] Error Handling: 12/12 PASS
- [ ] Performance: 6/6 PASS
- [ ] Health endpoint responds: http://localhost:8000/health

---

## Post-Deployment

After successful deployment:
1. Document any customer-specific configurations
2. Provide customer with service management commands
3. Schedule follow-up check (1 week)

---

## Contact

**ICC Support:** rausch@icc.sk  
**Customer:** Mágerstav s.r.o.

---

**Last Updated:** 2025-11-24  
**Status:** 🟢 READY FOR GO-LIVE