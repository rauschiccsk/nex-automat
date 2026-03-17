# NEX Automat — Test Summary

## Backend Tests (nex-manager-api)

| Test suite | Počet | Súbor |
|---|---|---|
| MuFis Integration | 39 | `tests/test_mufis_integration.py` |
| Payment Endpoints | varies | `tests/test_payment_endpoints.py` |
| Eshop Customers | varies | `tests/test_eshop_customers.py` |
| Partners | varies | `tests/test_partners.py` |
| PAB | varies | `tests/test_pab.py` |
| Migration | varies | `tests/test_migration.py` |

**Celkový počet backend testov:** 177

## Spustenie

```bash
cd apps/nex-manager-api
python3 -m pytest tests/ -v
```

### Len MuFis testy
```bash
python3 -m pytest tests/test_mufis_integration.py -v
```
