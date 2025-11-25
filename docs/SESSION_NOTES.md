# Session Notes - NEX Automat v2.0

**Date:** 2025-11-24  
**Session:** Fresh Deployment Test (Dress Rehearsal)  
**Project:** NEX Automat v2.0 - Supplier Invoice Loader  
**Customer:** Mágerstav s.r.o.

---

## Session Summary

Úspešne otestovaný automatizovaný deployment skript `deploy_fresh.py` pre čistú inštaláciu od nuly.

---

## Completed Tasks

### 1. Fix uvicorn[standard] Dependency

- **Problem:** `uvicorn[standard]` obsahuje `httptools` ktorý vyžaduje C++ kompilátor
- **Solution:** Zmenené na `uvicorn==0.32.0` bez [standard] extras
- **Files:** `apps/supplier-invoice-loader/requirements.txt`

### 2. Config Templates for Clean Installation

- **Problem:** `deploy_fresh.py` vyžadoval backup pre config súbory
- **Solution:** Vytvorené template súbory + funkcia `copy_from_templates()`
- **Files created:**
  - `apps/supplier-invoice-loader/config/config.yaml.template`
  - `apps/supplier-invoice-loader/config/config_customer.py.template`
- **Files updated:**
  - `scripts/deploy_fresh.py` - pridaná `copy_from_templates()` funkcia

### 3. Fresh Deployment Test - SUCCESS

- Deployment od nuly pomocou jedného príkazu
- Všetky validačné testy PASS

---

## Test Results

| Test Suite      | Result  |
| --------------- | ------- |
| Preflight Check | 6/6 ✅   |
| Error Handling  | 12/12 ✅ |
| Performance     | 6/6 ✅   |

---

## Verified Go-Live Workflow

```powershell
# Na zákazníkovom serveri:
cd C:\Deployment

# 1. Stiahnuť deployment skript
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/rauschiccsk/nex-automat/main/scripts/deploy_fresh.py" -OutFile "deploy_fresh.py"

# 2. Spustiť deployment
python deploy_fresh.py

# 3. Upraviť config súbory
# 4. Reštart služby: python nex-automat\scripts\manage_service.py restart
# 5. Validácia: python nex-automat\scripts\day5_preflight_check.py
```

---

## Prerequisites for Go-Live

- [ ] Python 3.13 32-bit installed
- [ ] Git installed  
- [ ] NSSM v `C:\Tools\nssm`
- [ ] PostgreSQL running
- [ ] Database `invoice_staging` exists
- [ ] Environment variable `POSTGRES_PASSWORD` set

---

## Current Status

```
✅ Deployment script tested
✅ Clean installation verified
✅ All validation tests PASS
✅ Ready for Go-Live: 2025-11-27
```

---

## Next Steps

1. Cleanup nepotrebných opravných skriptov
2. Go-Live u zákazníka Mágerstav (2025-11-27)

---

## Files Changed This Session

### New Files

- `apps/supplier-invoice-loader/config/config.yaml.template`
- `apps/supplier-invoice-loader/config/config_customer.py.template`
- `scripts/fix_uvicorn_requirement.py`
- `scripts/add_config_templates.py`

### Modified Files

- `apps/supplier-invoice-loader/requirements.txt`
- `scripts/deploy_fresh.py`

---

**Progress:** 100% - Ready for Go-Live  
**Next Session:** Go-Live Deployment @ Mágerstav