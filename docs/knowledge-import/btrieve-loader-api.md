# Btrieve-Loader REST API

Universal REST API pre prístup k NEX Genesis Btrieve databáze.

## Prehľad

### Účel
Btrieve-Loader poskytuje moderné REST API pre čítanie dát z legacy NEX Genesis Btrieve databázy. Umožňuje:
- Vyhľadávanie produktov, partnerov, čiarových kódov
- Fuzzy matching produktov pre invoice processing
- Prístup k dokumentom (faktúry, dodacie listy)
- Stromovú štruktúru tovarových skupín

### Architektúra

```
┌─────────────────────────────────────────────────────────────┐
│                    Btrieve-Loader API                       │
│                     (Python 3.11+)                          │
├─────────────────────────────────────────────────────────────┤
│  FastAPI Application                                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ /api/v1/*   │  │ /api/legacy │  │ /staging/*  │         │
│  │ Btrieve API │  │ Invoice API │  │ Web UI API  │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                │                │                 │
│  ┌──────┴────────────────┴────────────────┴──────┐         │
│  │              nexdata Package                   │         │
│  │  (Repositories, Models, BtrieveClient)        │         │
│  └──────────────────────┬────────────────────────┘         │
└─────────────────────────┼───────────────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────────────┐
│                         ▼                                   │
│  ┌────────────────────────────────────────────┐            │
│  │         Btrieve MKDE (32-bit)              │            │
│  │      C:\NEX\YEARACT\STORES\*.BTR           │            │
│  └────────────────────────────────────────────┘            │
│                    Windows Server                           │
└─────────────────────────────────────────────────────────────┘
```

**Hybridný model:**
- API beží ako 64-bit Python proces
- nexdata používa ctypes pre volanie 32-bit Btrieve MKDE DLL
- Vyžaduje Windows s nainštalovaným Pervasive/Actian PSQL

---

## Konfigurácia

### Environment premenné

| Premenná | Popis | Default |
|----------|-------|---------|
| `BTRIEVE_PATH` | Cesta k STORES adresáru | `C:\NEX\YEARACT\STORES` |
| `BTRIEVE_DIALS_PATH` | Cesta k DIALS adresáru | `C:\NEX\YEARACT\DIALS` |
| `BTRIEVE_ENCODING` | Kódovanie dát | `cp852` |
| `API_KEY` | API kľúč pre autentifikáciu | (prázdny = bez auth) |
| `PORT` | Port API servera | `8001` |
| `HOST` | Bind adresa | `0.0.0.0` |
| `DEBUG` | Debug mód | `false` |

### Príklad .env súboru

```env
BTRIEVE_PATH=C:\NEX\YEARACT\STORES
BTRIEVE_DIALS_PATH=C:\NEX\YEARACT\DIALS
API_KEY=your-secret-api-key-here
PORT=8001
```

### Windows Service Setup

```powershell
# Inštalácia ako Windows Service (NSSM)
nssm install NEX-BtrieveLoader "C:\opt\nex-automat-src\apps\btrieve-loader\.venv\Scripts\python.exe"
nssm set NEX-BtrieveLoader AppParameters "-m uvicorn main:app --host 0.0.0.0 --port 8001"
nssm set NEX-BtrieveLoader AppDirectory "C:\opt\nex-automat-src\apps\btrieve-loader"
nssm set NEX-BtrieveLoader AppEnvironmentExtra "BTRIEVE_PATH=C:\NEX\YEARACT\STORES"

# Štart služby
nssm start NEX-BtrieveLoader
```

---

## API Reference

Base URL: `http://localhost:8001/api/v1`

### Autentifikácia

Všetky endpointy (okrem health) vyžadujú `X-API-Key` header:

```http
X-API-Key: your-api-key
```

Ak `API_KEY` nie je nastavený, autentifikácia je vypnutá.

---

### Products `/api/v1/products`

#### GET /products
Zoznam produktov s pagináciou.

**Query params:**
- `page` (int, default=1) - Číslo stránky
- `page_size` (int, default=50, max=1000) - Počet záznamov

**Response:**
```json
{
  "data": [
    {
      "gs_code": 1001,
      "gs_name": "Chlieb biely 500g",
      "bar_code": "8590001000010",
      "supplier_code": "LS001",
      "mg_code": "KS"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 50,
    "total_items": 15420,
    "total_pages": 309
  }
}
```

#### GET /products/search
Vyhľadávanie produktov podľa názvu alebo EAN.

**Query params:**
- `q` (string, min 2 znaky) - Hľadaný výraz

**Príklad:**
```bash
curl -H "X-API-Key: xxx" "http://localhost:8001/api/v1/products/search?q=chlieb"
```

#### GET /products/{code}
Konkrétny produkt podľa GsCode.

**Response 404:**
```json
{"detail": "Product 99999 not found"}
```

#### POST /products/match
Fuzzy matching produktu pre invoice processing.

**Request body:**
```json
{
  "original_name": "CHLIEB BIELY KRÁJANÝ 500G",
  "edited_name": null,
  "original_ean": "8590001000010",
  "edited_ean": null,
  "min_confidence": 0.6
}
```

**Response:**
```json
{
  "is_match": true,
  "confidence": 0.95,
  "confidence_level": "high",
  "method": "ean",
  "product": {
    "gs_code": 1001,
    "gs_name": "Chlieb biely 500g",
    "bar_code": "8590001000010"
  },
  "alternatives": []
}
```

---

### Partners `/api/v1/partners`

#### GET /partners
Zoznam partnerov (dodávatelia/odberatelia).

**Query params:**
- `partner_type` (1=supplier, 2=customer, 3=both)
- `active` (bool) - Filtrovať aktívnych
- `page`, `page_size`

#### GET /partners/search
Vyhľadávanie podľa názvu, IČO, mesta.

**Príklad:**
```bash
curl -H "X-API-Key: xxx" "http://localhost:8001/api/v1/partners/search?q=12345678"
```

#### GET /partners/{pab_code}
Partner podľa kódu.

**Response:**
```json
{
  "pab_code": 101,
  "name1": "L & Š, s.r.o.",
  "name2": "",
  "ico": "12345678",
  "dic": "SK2020123456",
  "city": "Bratislava",
  "partner_type": 1,
  "active": true
}
```

---

### Barcodes `/api/v1/barcodes`

#### GET /barcodes/{ean}
Vyhľadanie produktu podľa EAN (primárny aj sekundárny).

**Príklad:**
```bash
curl -H "X-API-Key: xxx" "http://localhost:8001/api/v1/barcodes/8590001000010"
```

**Response:**
```json
{
  "gs_code": 1001,
  "bar_code": "8590001000010",
  "product_name": "Chlieb biely 500g",
  "product_supplier_code": "LS001"
}
```

#### GET /barcodes/product/{product_code}
Všetky čiarové kódy pre produkt.

---

### Stores `/api/v1/stores`

Tovarové skupiny (MGLST tabuľka).

#### GET /stores
Plochý zoznam skupín.

**Query params:**
- `parent_code` (int) - Filtrovať podľa rodiča
- `level` (int) - Filtrovať podľa úrovne
- `active` (bool)

#### GET /stores/tree
Hierarchický strom skupín.

**Response:**
```json
[
  {
    "mglst_code": 1,
    "name": "Potraviny",
    "level": 1,
    "children": [
      {
        "mglst_code": 2,
        "name": "Pečivo",
        "level": 2,
        "children": []
      }
    ]
  }
]
```

#### GET /stores/{mglst_code}
Konkrétna skupina.

#### GET /stores/{mglst_code}/children
Priame potomky skupiny.

---

### Documents `/api/v1/documents`

Dokumenty (TSH/TSI - faktúry, dodacie listy).

#### GET /documents
Zoznam hlavičiek dokumentov.

**Query params:**
- `book_id` (string, default="001") - Kniha dokladov
- `doc_type` (int) - Typ dokumentu
- `pab_code` (int) - Filtrovať podľa partnera
- `date_from`, `date_to` (YYYY-MM-DD)

#### GET /documents/{doc_number}
Dokument s položkami.

**Response:**
```json
{
  "header": {
    "doc_number": "2025001",
    "doc_type": 1,
    "doc_date": "2025-01-15",
    "pab_code": 101,
    "total_amount": 1234.56
  },
  "items": [
    {
      "line_number": 1,
      "gs_code": 1001,
      "gs_name": "Chlieb biely 500g",
      "quantity": 10,
      "unit_price": 1.50
    }
  ]
}
```

#### GET /documents/{doc_number}/items
Len položky dokumentu.

---

### Health & Metrics

#### GET /api/v1/health (bez auth)
```json
{
  "status": "healthy",
  "timestamp": "2025-01-30T10:15:30",
  "uptime_seconds": 3600
}
```

#### GET /api/v1/metrics (bez auth)
Prometheus formát:
```
# HELP btrieve_loader_info Service information
# TYPE btrieve_loader_info gauge
btrieve_loader_info{version="1.0.0"} 1

# HELP btrieve_loader_uptime_seconds Service uptime
# TYPE btrieve_loader_uptime_seconds counter
btrieve_loader_uptime_seconds 3600
```

#### GET /api/v1/ready (bez auth)
```json
{"ready": true, "timestamp": "..."}
```

---

## Príklady použitia

### cURL

```bash
# Health check
curl http://localhost:8001/api/v1/health

# Zoznam produktov
curl -H "X-API-Key: your-key" "http://localhost:8001/api/v1/products?page=1&page_size=10"

# Vyhľadanie produktu
curl -H "X-API-Key: your-key" "http://localhost:8001/api/v1/products/search?q=mlieko"

# Lookup EAN
curl -H "X-API-Key: your-key" "http://localhost:8001/api/v1/barcodes/8590001000010"

# Product match
curl -X POST -H "X-API-Key: your-key" -H "Content-Type: application/json" \
  -d '{"original_name": "Chlieb", "original_ean": "8590001000010"}' \
  "http://localhost:8001/api/v1/products/match"
```

### Python requests

```python
import requests

BASE_URL = "http://localhost:8001/api/v1"
HEADERS = {"X-API-Key": "your-api-key"}

# Zoznam produktov
response = requests.get(f"{BASE_URL}/products", headers=HEADERS, params={"page_size": 100})
products = response.json()["data"]

# Vyhľadanie partnera
response = requests.get(f"{BASE_URL}/partners/search", headers=HEADERS, params={"q": "12345678"})
partners = response.json()["data"]

# EAN lookup
response = requests.get(f"{BASE_URL}/barcodes/8590001000010", headers=HEADERS)
if response.status_code == 200:
    product = response.json()
    print(f"Nájdený produkt: {product['product_name']}")
else:
    print("Produkt nenájdený")

# Product matching
match_response = requests.post(
    f"{BASE_URL}/products/match",
    headers=HEADERS,
    json={
        "original_name": "CHLIEB BIELY",
        "original_ean": "8590001000010",
        "min_confidence": 0.6
    }
)
result = match_response.json()
if result["is_match"]:
    print(f"Match: {result['product']['gs_name']} (confidence: {result['confidence']:.0%})")
```

---

## Legacy API

Pôvodné invoice processing endpointy sú dostupné pod `/api/legacy/`:

| Endpoint | Popis |
|----------|-------|
| `GET /api/legacy/` | Service info |
| `GET /api/legacy/health` | Health check |
| `GET /api/legacy/metrics` | Metrics (JSON) |
| `GET /api/legacy/stats` | Database statistics |
| `GET /api/legacy/status` | Detailed status (auth) |
| `GET /api/legacy/invoices` | List invoices (auth) |
| `POST /api/legacy/invoice` | Process invoice (auth) |
| `POST /api/legacy/admin/test-email` | Test email (auth) |
| `POST /api/legacy/admin/send-summary` | Daily summary (auth) |

### Staging API

Pre supplier-invoice-staging-web frontend:

| Endpoint | Popis |
|----------|-------|
| `GET /staging/config` | UI konfigurácia |
| `GET /staging/invoices` | Zoznam faktúr |
| `GET /staging/invoices/{id}` | Detail faktúry |
| `PUT /staging/items/{id}` | Update ceny |
| `PUT /staging/invoices/{id}/approve` | Schválenie |

---

## Troubleshooting

### Btrieve connection error

**Symptóm:** `Failed to open gscat: File not found`

**Riešenie:**
1. Overiť cestu `BTRIEVE_PATH`
2. Skontrolovať či beží Pervasive/Actian PSQL služba
3. Overiť prístupové práva k súborom

```powershell
# Kontrola služby
Get-Service -Name "Pervasive*"

# Test prístupu k súborom
Test-Path "C:\NEX\YEARACT\STORES\GSCAT.BTR"
```

### API key error

**Symptóm:** `422 Missing X-API-Key header`

**Riešenie:**
- Pridať header `X-API-Key: your-key`
- Alebo nastaviť prázdny `API_KEY` pre vypnutie auth

### Encoding issues

**Symptóm:** Pokazené slovenské znaky (ä, č, ľ, ...)

**Riešenie:**
```env
BTRIEVE_ENCODING=cp852
```

### Port conflict

**Symptóm:** `Address already in use`

**Riešenie:**
```powershell
# Nájsť proces na porte
netstat -ano | findstr :8001

# Zabiť proces
taskkill /PID <pid> /F
```

### Slow queries

**Symptóm:** Pomalé odpovede (>5s)

**Možné príčiny:**
1. Prvý request otvára Btrieve súbory (cold start)
2. Veľké množstvo dát bez paginácie
3. Nedostatok RAM pre Btrieve cache

**Riešenie:**
- Použiť pagináciu (`page_size=50`)
- Warmup request pri štarte služby
- Zvýšiť Btrieve cache v `mkde.cfg`

---

## Verzie

| Verzia | Dátum | Zmeny |
|--------|-------|-------|
| 1.0.0 | 2025-01 | Initial release - Phase 1-4 |
