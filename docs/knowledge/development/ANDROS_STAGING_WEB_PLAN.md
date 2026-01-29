# ANDROS Supplier Invoice Staging Web - Implementačný plán

**Dátum:** 2026-01-21
**Status:** AKTÍVNY

---

## 1. Scope definícia

### Fáza 1 - TERAZ
| Funkcia | Popis |
|---------|-------|
| Zobrazenie faktúr | Grid so zoznamom pending faktúr |
| Detail faktúry | Hlavička + položky |
| Match status | Ktoré položky nájdené / nenájdené v NEX Genesis |
| Editácia cien | ❌ Zakázaná (read-only) |

### Fáza 2 - NESKÔR
| Funkcia | Popis |
|---------|-------|
| NEX Genesis zápis | Schválenie → zápis do NEX |
| Rozdiely MÁGERSTAV/ANDROS | Špecifikácia neskôr |

---

## 2. Čo už existuje na ANDROS

| Komponent | Status | Port |
|-----------|--------|------|
| PostgreSQL | ✅ Beží | 5432 |
| btrieve-loader (FastAPI) | ✅ Beží | 8001 |
| staging_routes.py endpointy | ✅ Existujú | - |
| supplier-invoice-staging-web | ❌ Chýba | 3000/nginx |

---

## 3. Implementačné kroky pre Claude Code

### Krok 1: Konfigurácia pre multi-tenant

**Súbor:** `apps/btrieve-loader/config/config_customer.py`

```python
# Pridať na koniec existujúceho súboru:

# Staging Web UI konfigurácia
STAGING_WEB_CONFIG = {
    "allow_price_edit": False,      # ANDROS=False, MÁGERSTAV=True
    "allow_margin_edit": False,     # ANDROS=False, MÁGERSTAV=True
    "customer_name": CUSTOMER_ID,   # Pre zobrazenie v UI
}
```

### Krok 2: Nový endpoint /staging/config

**Súbor:** `apps/btrieve-loader/src/api/staging_routes.py`

```python
# Pridať import
from config.config_customer import STAGING_WEB_CONFIG

# Pridať endpoint
@router.get("/staging/config")
async def get_staging_config():
    """Vráti konfiguráciu staging web UI."""
    return STAGING_WEB_CONFIG
```

### Krok 3: Frontend - načítanie konfigurácie

**Nový súbor:** `apps/supplier-invoice-staging-web/src/api/config.ts`

```typescript
import api from './client';

export interface StagingConfig {
    allow_price_edit: boolean;
    allow_margin_edit: boolean;
    customer_name: string;
}

export async function getStagingConfig(): Promise<StagingConfig> {
    const response = await api.get('/staging/config');
    return response.data;
}
```

### Krok 4: Frontend - podmienená editovateľnosť

**Súbor:** `apps/supplier-invoice-staging-web/src/pages/InvoiceDetail.tsx`

Upraviť InvoiceItemsGrid - stĺpce `margin_percent` a `sale_price`:
- `editable: config.allow_margin_edit` 
- `editable: config.allow_price_edit`

### Krok 5: ANDROS deployment

**Na ANDROS Windows VM:**

```powershell
# 1. Git pull
cd C:\ANDROS\nex-automat
git pull origin develop

# 2. Build frontend
cd apps\supplier-invoice-staging-web
npm install
npm run build

# 3. Skopírovať build do FastAPI static
xcopy /E /Y dist\* ..\btrieve-loader\static\app\

# 4. Restart služby
Restart-Service -Name "NEX-SupplierInvoiceLoader-ANDROS"
```

---

## 4. Overenie funkčnosti

| Test | URL | Očakávaný výsledok |
|------|-----|-------------------|
| API config | http://localhost:8001/staging/config | JSON s allow_*=false |
| Web UI | http://localhost:8001/app | Načíta sa React app |
| Faktúry | http://localhost:8001/app/invoices | Grid s faktúrami |
| Detail | http://localhost:8001/app/invoices/1 | Detail + položky |
| Editácia | Klik na cenu | Bunka NIE JE editovateľná |

---

## 5. Claude Code príkazy

```bash
# 1. Otvoriť projekt
cd C:\Development\nex-automat

# 2. Spustiť Claude Code
claude

# 3. Zadať úlohu:
"Implementuj multi-tenant konfiguráciu pre supplier-invoice-staging-web 
podľa plánu v docs/knowledge/ANDROS_STAGING_WEB_PLAN.md"
```

---

## 6. Časový odhad

| Krok | Odhad |
|------|-------|
| Krok 1-2: Backend konfig | 30 min |
| Krok 3-4: Frontend úpravy | 1-2 hod |
| Krok 5: ANDROS deployment | 30 min |
| Testovanie | 30 min |
| **CELKOM** | **2.5-3.5 hod** |

---

## 7. Ďalší krok

**Uložiť tento plán** do `docs/knowledge/development/` a spustiť Claude Code s úlohou implementácie.