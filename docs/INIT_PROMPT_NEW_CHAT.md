# Init Prompt - Fresh Deployment Test

**Project:** NEX Automat v2.0 - Supplier Invoice Loader  
**Customer:** Mágerstav s.r.o.  
**Current Progress:** 99% (Deployment Script Ready)  
**Last Session:** Dress Rehearsal Complete (2025-11-24)  
**This Session:** Test Automated Deployment Script  

---

## Quick Context

Projekt NEX Automat v2.0 - testujeme automatizovaný deployment skript pred Go-Live u zákazníka.

**Stav projektu:**
- DAY 1-6: ✅ Complete
- Dress Rehearsal: ✅ Complete (manual deployment tested)
- Deployment Script: ✅ Created (deploy_fresh.py)
- This Session: Test deploy_fresh.py from scratch
- Go-Live: 2025-11-27

---

## Session Goal

Otestovať `deploy_fresh.py` - automatizovaný deployment od nuly:

1. Vymazať C:\Deployment\nex-automat (backup už existuje)
2. Spustiť deploy_fresh.py
3. Overiť že všetky testy prejdú
4. Ak OK → Ready for customer Go-Live

---

## Pre-Deployment State

### Backup (MUST EXIST)
```
C:\Deployment\nex-automat.backup\
├── apps\supplier-invoice-loader\config\
│   ├── config.yaml          # Customer config
│   └── config_customer.py   # Customer settings
├── tools\nssm\               # NSSM binaries
└── apps\supplier-invoice-loader\tests\samples\  # Test PDFs
```

### Environment Variables (MUST BE SET)
```
POSTGRES_PASSWORD - PostgreSQL password
```

### Prerequisites
```
- Python 3.13 32-bit installed
- Git installed
- PostgreSQL running on localhost:5432
- Database invoice_staging exists
```

---

## Deployment Command

```powershell
cd C:\Deployment

# Remove existing deployment (keep backup!)
Remove-Item nex-automat -Recurse -Force

# Run automated deployment
python nex-automat.backup\scripts\deploy_fresh.py --backup-path C:\Deployment\nex-automat.backup
```

Alternative (if script not in backup):
```powershell
# Clone first, then run
git clone https://github.com/rauschiccsk/nex-automat.git
cd nex-automat
python scripts\deploy_fresh.py --backup-path C:\Deployment\nex-automat.backup
```

---

## Expected Results

### Deployment Script Output
```
[OK] Python: 3.13.x
[OK] Git: installed
[OK] PostgreSQL: Running
[OK] Repository cloned
[OK] Virtual environment created
[OK] Dependencies installed
[OK] Directories created
[OK] Config files copied
[OK] Service installed
[OK] Service started: SERVICE_RUNNING
[OK] Preflight check: 6/6 PASS
```

### Validation
```
Preflight: 6/6 PASS
Error Handling: 12/12 PASS
Performance: 6/6 PASS
```

---

## Post-Deployment Validation

```powershell
cd C:\Deployment\nex-automat
.\venv32\Scripts\Activate.ps1

# Service status
python scripts\manage_service.py status

# Full validation
python scripts\day5_preflight_check.py
python scripts\day5_error_handling_tests.py
python scripts\day5_performance_tests.py
```

---

## Troubleshooting

### If deployment fails
1. Check error message
2. Fix issue
3. Remove failed deployment: `Remove-Item nex-automat -Recurse -Force`
4. Retry

### Common Issues
| Issue | Solution |
|-------|----------|
| Python not found | Install Python 3.13 32-bit |
| POSTGRES_PASSWORD not set | Set environment variable |
| Service won't start | Check logs\service-stderr.log |
| Missing config | Verify backup path correct |

---

## Success Criteria

Deployment is successful when:
- [ ] Script completes without errors
- [ ] Service status: SERVICE_RUNNING
- [ ] Preflight: 6/6 PASS
- [ ] Error Handling: 12/12 PASS
- [ ] Performance: 6/6 PASS

If all pass → Ready for customer Go-Live (2025-11-27)

---

## Communication

**[DEV]** = C:\Development\nex-automat PowerShell  
**[DEPLOY]** = C:\Deployment\nex-automat PowerShell

Jasne označovať ktorý PowerShell použiť pre príkazy.

---

**Last Updated:** 2025-11-24  
**Status:** 🟢 READY FOR DEPLOYMENT TEST