# NEX Automat v3.2 - Staging Web Deployment

**Dátum:** 2025-12-27
**Status:** ✅ DONE

---

## Dokončené úlohy

- ✅ Deployment v3.2 na Mágerstav server
- ✅ Windows služba NEX-SupplierInvoiceLoader (nahradila NEXAutomat)
- ✅ NSSM konfigurácia s POSTGRES_PASSWORD environment variable
- ✅ Frontend build (Vite + React) s base="/app/"
- ✅ Static files serving cez FastAPI na /app
- ✅ STATUS_CONFIG fix - pridaný 'staged' status
- ✅ match_percent null fallback fix
- ✅ Temporal workflow spracovanie emailov funguje
- ✅ Web UI zobrazuje faktúry a položky

## Windows služby Mágerstav

| Služba | Port | Status |
|--------|------|--------|
| NEX-SupplierInvoiceLoader | 8001 | ✅ Running |
| NEX-Invoice-Worker | - | ✅ Running |
| NEX-Polling-Scheduler | - | ✅ Running |
| NEX-Temporal-Server | 7233 | ✅ Running |

## Dôležité príkazy

```powershell
# Služby
Get-Service | Where-Object {$_.Name -like "*NEX*"}
Restart-Service NEX-SupplierInvoiceLoader

# NSSM edit
C:\Tools\nssm\nssm.exe edit NEX-SupplierInvoiceLoader

# Frontend build (Dev PC)
cd C:\Development\nex-automat\apps\supplier-invoice-staging-web
npx vite build
# Skopírovať dist na server

# Test API
curl http://localhost:8001/staging/invoices
```

## Cesty

- Dev: C:\Development\nex-automat\
- Deploy: C:\Deployment\nex-automat\
- Frontend dist: apps\supplier-invoice-staging-web\dist\
- Web UI: http://localhost:8001/app
