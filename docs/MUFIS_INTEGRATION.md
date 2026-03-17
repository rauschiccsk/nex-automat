# MuFis Integration Documentation

MuFis je ERP systém pre skladovanie a logistiku. Integrácia prebieha cez 4 API endpointy.

## Endpointy

| Endpoint | Metóda | Popis |
|---|---|---|
| `/api/eshop/mufis/getOrder` | POST | Zoznam objednávok pre MuFis |
| `/api/eshop/mufis/setOrder` | POST | Update statusu/tracking objednávky |
| `/api/eshop/mufis/getProduct` | POST | Zoznam produktov pre MuFis |
| `/api/eshop/mufis/setProduct` | POST | Update stock_quantity produktu |

## Autentifikácia

- Header `API-KEY` s API kľúčom priradeným tenantovi
- Voliteľná IP whitelist kontrola (`MUFIS_IP_CHECK_ENABLED`, `MUFIS_ALLOWED_IPS`)

## setProduct

### Single mode
```
POST /api/eshop/mufis/setProduct
Content-Type: application/x-www-form-urlencoded

sku=SKU-001&stock_quantity=42
```

Response:
```json
{"ok": 1, "error": ""}
```

### Batch mode
```
POST /api/eshop/mufis/setProduct
Content-Type: application/x-www-form-urlencoded

data=[{"sku":"SKU-001","stock_quantity":10},{"sku":"SKU-002","stock_quantity":25}]
```

Response:
```json
{
  "products": [
    {"sku": "SKU-001", "ok": 1, "error": ""},
    {"sku": "SKU-002", "ok": 1, "error": ""}
  ]
}
```

Per-item chyby (neplatné SKU, chýbajúca hodnota) sa vracajú v `error` poli pre každý item zvlášť.

## setOrder

### Single mode
```
POST /api/eshop/mufis/setOrder
Content-Type: application/x-www-form-urlencoded

order_number=ORD-001&status=futárnak átadva&package_number=PKG001&tracking_link=https://track.com
```

Response:
```json
{"ok": 1, "error": ""}
```

### Batch mode
```
POST /api/eshop/mufis/setOrder
Content-Type: application/x-www-form-urlencoded

data=[{"order_number":"ORD-001","status":"futárnak átadva","package_number":"PKG001"}]
```

Response:
```json
{
  "orders": [
    {"order_number": "ORD-001", "ok": 1, "error": ""}
  ]
}
```

## Webhook Trigger (W1)

Pri novej objednávke alebo zmene statusu webshop posiela HTTP GET na MuFis URL.
MuFis potom zavolá `getOrder` endpoint namiesto čakania na hodinový poll.

### Konfigurácia

| Env var | Default | Popis |
|---|---|---|
| `MUFIS_WEBHOOK_URL` | (prázdny) | URL pre GET notify |
| `MUFIS_DRY_RUN` | `true` | Ak `true`, webhook sa nevolá (len log) |

### Správanie
- **Fire-and-forget** — nesmie blokovať response
- Zlyhanie je len `WARNING` log
- Timeout: 10 sekúnd
- Volá sa z:
  - `create_order` (POST /api/eshop/orders)
  - `admin_update_order` (PATCH /api/eshop/admin/orders/{id}) — len pri zmene statusu

### Implementácia
Modul: `apps/nex-manager-api/eshop/mufis_webhook.py`

## Status Mapping

MuFis posiela maďarské statusy, mapované na interné:

| MuFis status | Interný status |
|---|---|
| `összeszedve` | `processing` |
| `futárnak átadva` | `shipped` |
| `kézbesítve` | `delivered` |
| (neznámy) | `processing` (default) |

## Testy

39 integračných testov v `tests/test_mufis_integration.py`:
- AUTH: 3 testy
- getOrder: 8 testov (basic + G1/G4 filters + pagination)
- setOrder: 8 testov (basic + S1/S2 batch + multiple_packages)
- getProduct: 7 testov (basic + P1/P2/P3)
- setProduct: 6 testov (basic + SP1/SP3 batch)
- Webhook: 2 testy (dry-run + sends GET)
- Unit: 2 testy (status mapping)
- Audit gaps: 3 testy (A1 + G2)
