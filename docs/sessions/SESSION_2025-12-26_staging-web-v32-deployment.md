# Supplier Invoice Staging Web - v3.2 Deployment

**Dátum:** 2025-12-26
**Status:** 🔄 IN PROGRESS

---

## Dokončené úlohy (táto session)

### Backend - staging_routes.py
- ✅ Vytvorené nové FastAPI endpointy pre staging:
  - GET /staging/invoices - zoznam faktúr
  - GET /staging/invoices/{id} - detail s položkami
  - PUT /staging/items/{id} - editácia ceny položky
  - PUT /staging/items/batch - batch editácia
  - PUT /staging/invoices/{id}/approve - schválenie faktúry
- ✅ Registrácia routera v main.py

### Opravy pg8000
- ✅ Fix connection.py - named parameters (:p1, :p2) namiesto positional ($1, $2)
- ✅ Fix invoice_repository.py - params handling pre prázdny list

### Frontend - supplier-invoice-staging-web
- ✅ Prepnutie z mock data na reálne API
- ✅ Oprava endpointov /invoices → /staging/invoices
- ✅ Disabled USE_MOCK_DATA
- ✅ Frontend zobrazuje prázdny grid (0 faktúr - korektne)

### Konfigurácia portov (Dev PC)
| Služba | Port |
|--------|------|
| RAG API | 8765 |
| Temporal Server | 7233 |
| Temporal UI | 8233 |
| NEX Brain API | 8003 (zmenené z 8001) |
| supplier-invoice-loader | 8001 |

## Súbory zmenené

| Súbor | Zmena |
|-------|-------|
| apps/supplier-invoice-loader/src/api/staging_routes.py | NOVÝ |
| apps/supplier-invoice-loader/main.py | import + include_router |
| packages/nex-staging/nex_staging/connection.py | named params fix |
| packages/nex-staging/nex_staging/repositories/invoice_repository.py | params fix |
| apps/nex-brain/.env | API_PORT=8003 |
| apps/supplier-invoice-staging-web/src/api/invoices.ts | /staging/* endpointy |
| apps/supplier-invoice-staging-web/src/api/mockData.ts | USE_MOCK_DATA=false |

## Next Steps - v3.2 Deployment na Mágerstav

1. Git commit a push všetkých zmien
2. Deploy na server Mágerstav
3. Testovanie s reálnymi faktúrami
4. Aktualizácia NSSM služby ak potrebné

## Dôležité príkazy

```powershell
# Dev - spustenie
cd C:\Development\nex-automat\apps\supplier-invoice-loader
python main.py

cd C:\Development\nex-automat\apps\supplier-invoice-staging-web
npm run dev

# Mágerstav - deployment
cd C:\Deployment\nex-automat
git pull origin develop
```
