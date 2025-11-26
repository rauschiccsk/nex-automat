# NEX Automat - Architektúra systému

**Projekt:** NEX Automat  
**Verzia dokumentu:** 1.1  
**Dátum:** 2025-11-26  

---

## 1. PREHĽAD ARCHITEKTÚRY

### 1.1 High-Level Diagram

**ICC Server (Dev Center)**
- n8n Workflows (zdieľané pre všetkých zákazníkov)
- Komunikácia cez HTTPS (Cloudflare Tunnel)

↓ HTTPS/CF Tunnel ↓

**Zákazník Server** (všetko beží lokálne)
- FastAPI (supplier-invoice-loader)
- PostgreSQL (invoice_staging)
- GUI Application (supplier-invoice-editor)
- NEX Genesis (Btrieve)

### 1.2 Princípy

- **Centralizované workflow** - n8n na ICC serveri pre všetkých zákazníkov
- **Decentralizované dáta** - každý zákazník má vlastný server
- **Priamy Btrieve prístup** - bez middleware (nex-genesis-server)
- **Human-in-the-loop** - operátor validuje pred zápisom

---

## 2. KOMPONENTY

### 2.1 n8n Workflow Server (ICC)

**Účel:** Spracovanie emailov a PDF pre všetkých zákazníkov

**Technológie:**
- n8n (workflow automation)
- IMAP (email trigger)
- HTTP (API volania)

**Workflow:** `n8n-SupplierInvoiceEmailLoader`

```
Email Trigger (IMAP)
    ↓
Split PDF (JavaScript)
    ↓
Has PDF? (Switch)
    ├── Yes → HTTP POST → Zákazník FastAPI
    └── No  → Error Notification (Gmail)
```

---

### 2.2 FastAPI Service (Zákazník)

**Účel:** Príjem, extrakcia a uloženie faktúr

**Aplikácia:** `supplier-invoice-loader`

**Technológie:**
- Python 3.x
- FastAPI
- pdfplumber (PDF čítanie)
- Regex (extrakcia dát)
- ISDOC XML generátor

**Deployment:**
- Windows Service
- Port 8000
- Cloudflare Tunnel (HTTPS)

**Štruktúra:**

```
supplier-invoice-loader/
├── main.py                    # FastAPI app
├── src/
│   ├── api/                   # API models
│   ├── extractors/            # PDF → Data
│   │   ├── ls_extractor.py    # L&Š špecifický
│   │   └── generic_extractor.py
│   ├── business/
│   │   └── isdoc_service.py   # XML generátor
│   ├── database/
│   │   └── database.py        # SQLite (lokálny log)
│   ├── monitoring/            # Health, alerts, logs
│   ├── backup/                # Backup & restore
│   └── utils/                 # Config, notifications
├── config/
│   └── config.yaml
└── deploy/
    └── service_installer.py   # Windows Service
```

---

### 2.3 PostgreSQL Staging (Zákazník)

**Účel:** Dočasné úložisko pre spracovávané faktúry

**Databáza:** `invoice_staging`

**Tabuľky:**

```sql
-- Hlavičky faktúr
CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,
    supplier_ico VARCHAR(20),
    supplier_name VARCHAR(255),
    invoice_number VARCHAR(50),
    invoice_date DATE,
    due_date DATE,
    total_amount DECIMAL(15,2),
    total_vat DECIMAL(15,2),
    currency VARCHAR(3) DEFAULT 'EUR',
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Položky faktúr
CREATE TABLE invoice_items (
    id SERIAL PRIMARY KEY,
    invoice_id INTEGER REFERENCES invoices(id),
    line_number INTEGER,
    original_name VARCHAR(255),
    original_ean VARCHAR(20),
    original_quantity DECIMAL(15,3),
    original_unit VARCHAR(10),
    original_price_unit DECIMAL(15,4),
    original_price_total DECIMAL(15,2),
    original_vat_rate DECIMAL(5,2),
    edited_name VARCHAR(255),
    edited_mglst_code VARCHAR(20),
    edited_price_buy DECIMAL(15,4),
    edited_price_sell DECIMAL(15,4),
    nex_plu INTEGER,
    nex_name VARCHAR(255),
    nex_category VARCHAR(20),
    in_nex BOOLEAN DEFAULT FALSE
);
```

---

### 2.4 GUI Application (Zákazník)

**Účel:** Zobrazenie, editácia a schválenie faktúr

**Aplikácia:** `supplier-invoice-editor`

**Technológie:**
- Python 3.x
- PyQt5 (GUI framework)
- asyncpg (PostgreSQL)
- Btrieve client (NEX Genesis)

**Štruktúra:**

```
supplier-invoice-editor/
├── main.py                    # Entry point
├── src/
│   ├── ui/
│   │   ├── main_window.py     # Zoznam faktúr
│   │   ├── invoice_detail_window.py
│   │   └── widgets/
│   │       ├── invoice_list_widget.py
│   │       └── invoice_items_grid.py
│   ├── business/
│   │   ├── invoice_service.py      # CRUD
│   │   └── nex_lookup_service.py   # EAN → PLU
│   ├── database/
│   │   └── postgres_client.py
│   ├── btrieve/
│   │   └── btrieve_client.py
│   └── models/
│       ├── gscat.py           # Produkty
│       ├── barcode.py         # EAN kódy
│       ├── pab.py             # Partneri
│       └── mglst.py           # Skupiny
└── config/
    └── config.yaml
```

---

### 2.5 NEX Genesis (Btrieve)

**Účel:** Produkčný ERP systém zákazníka

**Technológia:** Pervasive/Btrieve databázy

**Lokácia:** `C:\NEX\DATA\`

**Tabuľky:**

| Tabuľka | Súbor | Účel |
|---------|-------|------|
| GSCAT | GSCAT.BTR | Katalóg produktov |
| BARCODE | BARCODE.BTR | EAN kódy |
| PAB | PAB.BTR | Partneri |
| MGLST | MGLST.BTR | Tovarové skupiny |
| TSH | TSHA-001.BTR | Hlavičky DL |
| TSI | TSIA-001.BTR | Položky DL |
| PLS | PLSnnnnn.BTR | Predajný cenník |
| RPC | RPCnnnnn.BTR | Požiadavky na zmeny cien |

---

## 3. DÁTOVÝ TOK

### 3.1 End-to-End Flow

**KROK 1: EMAIL**
- Dodávateľ → Operátor Mágerstav → magerstavinvoice@gmail.com

↓

**KROK 2: N8N WORKFLOW (ICC Server)**
- IMAP Trigger → Split PDF → HTTP POST

↓ HTTPS (Cloudflare Tunnel) ↓

**KROK 3: FASTAPI (Zákazník Server)**
- Receive → Extract (Regex) → Generate XML → Save Files

↓ (3 výstupy) ↓

- PDF File: C:\NEX\IMPORT\PDF\
- XML File: C:\NEX\IMPORT\XML\
- PostgreSQL: invoice_staging

↓

**KROK 4: NEX LOOKUP**
- Pre každú položku: EAN → GSCAT.BTR → PLU
- Výsledok uložený do PostgreSQL (nex_plu, in_nex)

↓

**KROK 5: GUI (supplier-invoice-editor)**
- Zobrazenie → Editácia → Validácia → Schválenie

↓

**KROK 6: BTRIEVE ZÁPIS**
- GSCAT (nové produkty) → BARCODE → TSH → TSI → RPC

↓

**KROK 7: VÝSLEDOK**
- Dodávateľský DL v NEX Genesis (status "Pripravený")
- Operátor dokončí naskladnenie v NEX Genesis

---

## 4. BEZPEČNOSŤ

### 4.1 Autentifikácia

| Komponent | Metóda |
|-----------|--------|
| n8n → FastAPI | X-API-Key header |
| FastAPI endpoints | API key verification |
| Cloudflare Tunnel | HTTPS encryption |

### 4.2 Sieťová bezpečnosť

- FastAPI počúva na localhost:8000
- Cloudflare Tunnel zabezpečuje HTTPS
- Žiadne otvorené porty na internete

### 4.3 Dátová bezpečnosť

- PDF/XML súbory na zákazníckom serveri
- PostgreSQL na zákazníckom serveri
- Btrieve na zákazníckom serveri
- Žiadne dáta na ICC serveri (okrem workflow logs)

---

## 5. KONFIGURÁCIA

### 5.1 supplier-invoice-loader

```yaml
# config/config.yaml
customer:
  name: "Mágerstav"
  code: "MAGERSTAV"

api:
  host: "0.0.0.0"
  port: 8000
  api_key: "${LS_API_KEY}"

storage:
  pdf_dir: "C:\\NEX\\IMPORT\\PDF"
  xml_dir: "C:\\NEX\\IMPORT\\XML"

postgres:
  enabled: true
  host: "localhost"
  port: 5432
  database: "invoice_staging"
  user: "${POSTGRES_USER}"
  password: "${POSTGRES_PASSWORD}"
```

### 5.2 supplier-invoice-editor

```yaml
# config/config.yaml
postgres:
  host: "localhost"
  port: 5432
  database: "invoice_staging"
  user: "${POSTGRES_USER}"
  password: "${POSTGRES_PASSWORD}"

btrieve:
  data_path: "C:\\NEX\\DATA"
  
nex:
  price_list_number: "00001"  # PLSnnnnn, RPCnnnnn
  min_margin_percent: 15.0
```

---

## 6. DEPLOYMENT

### 6.1 ICC Server

| Služba | Typ | Status |
|--------|-----|--------|
| n8n | Docker/Service | ✅ Beží |

### 6.2 Zákazník Server

| Služba | Typ | Status |
|--------|-----|--------|
| FastAPI (loader) | Windows Service | ✅ Beží |
| PostgreSQL | Windows Service | ✅ Beží |
| Cloudflare Tunnel | Windows Service | ⚪ TODO |
| GUI (editor) | Desktop App | Manuálne spúšťanie |
| NEX Genesis | Existujúci systém | ✅ Beží |

### 6.3 File Storage

```
C:\NEX\
├── DATA\           # Btrieve databázy (NEX Genesis)
│   ├── GSCAT.BTR
│   ├── BARCODE.BTR
│   ├── PAB.BTR
│   ├── MGLST.BTR
│   ├── TSHA-001.BTR
│   ├── TSIA-001.BTR
│   ├── PLS00001.BTR
│   └── RPC00001.BTR
└── IMPORT\         # NEX Automat súbory
    ├── PDF\        # Originálne faktúry
    └── XML\        # ISDOC výstup
```

---

## 7. MONITORING

### 7.1 Endpoints

| Endpoint | Účel |
|----------|------|
| GET /health | Health check |
| GET /metrics | JSON metrics |
| GET /metrics/prometheus | Prometheus format |
| GET /stats | Database statistics |

### 7.2 Logging

- FastAPI: `logs/` adresár
- n8n: Workflow execution history
- PostgreSQL: Standard logs

### 7.3 Alerting

- Email notifikácie pri chybách
- n8n error notifications (Gmail)

---

## 8. ŠKÁLOVATEĽNOSŤ

### 8.1 Multi-customer

```
n8n Server (ICC)
├── Workflow: Mágerstav → magerstav-invoices.icc.sk
├── Workflow: ANDROS → andros-invoices.icc.sk
└── Workflow: CustomerX → customerx-invoices.icc.sk
```

### 8.2 Pridanie nového zákazníka

1. Vytvor nový n8n workflow (kópia template)
2. Nakonfiguruj email trigger (nová schránka)
3. Nastav endpoint URL (nový Cloudflare Tunnel)
4. Deploy FastAPI + PostgreSQL na zákaznícky server
5. Nakonfiguruj GUI aplikáciu

---

**Dokument vytvorený:** 2025-11-26  
**Autor:** Claude AI + Zoltán Rausch  
**Revízia:** 1.1 (Fixed per pravidlo 18)