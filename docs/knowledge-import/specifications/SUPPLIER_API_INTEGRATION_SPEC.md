# KNOWLEDGE_2025-01-21_supplier-api-integration

# Supplier API Integration - Technická špecifikácia

## Prehľad

Rozšírenie NEX Automat o podporu načítavania faktúr cez API dodávateľov. Prvý dodávateľ: MARSO, ďalší plánovaný: CONTINENTAL.

**Cieľ:** Multi-dodávateľská architektúra s možnosťou jednoduchého pridania nových dodávateľov.

**Prístup:** Hybridný - Adapter Pattern + YAML konfigurácia

---

## Architektúra

### Umiestnenie v projekte

```
apps/supplier-invoice-worker/
├── activities/
│   ├── email_activities.py           # existujúce
│   ├── invoice_activities.py         # existujúce (zdieľané)
│   └── supplier_api_activities.py    # NOVÉ - API volania
├── workflows/
│   ├── __init__.py
│   ├── pdf_invoice_workflow.py       # PREMENOVANÉ z invoice_workflow.py
│   └── api_invoice_workflow.py       # NOVÉ
├── adapters/
│   ├── __init__.py
│   ├── base_adapter.py               # Abstraktná trieda
│   └── marso_adapter.py              # MARSO implementácia
├── models/
│   ├── __init__.py
│   └── unified_invoice.py            # UnifiedInvoice dataclass
├── config/
│   ├── settings.py
│   └── suppliers/
│       ├── _template.yaml            # Šablóna pre nových dodávateľov
│       └── marso.yaml                # MARSO konfigurácia
```

### Workflow porovnanie

| Aspekt | pdf_invoice_workflow | api_invoice_workflow |
|--------|---------------------|---------------------|
| Trigger | IMAP polling (email) | Schedule / manuálne |
| Zdroj | PDF príloha | XML cez API |
| Identifikácia produktov | OCR / text extraction | Štruktúrované dáta |
| Dodávatelia | Všeobecný | MARSO, CONTINENTAL, ... |

### Diagram toku

```
┌─────────────────────────────────────────────────────────────────┐
│                    api_invoice_workflow                         │
├─────────────────────────────────────────────────────────────────┤
│  1. Load supplier config (YAML)                                 │
│  2. Authenticate (podľa auth_type)                              │
│  3. Fetch invoice list (unprocessed)                            │
│  4. For each invoice:                                           │
│     a) Fetch XML                                                │
│     b) Archive raw XML (filesystem + PostgreSQL)                │
│     c) Parse → UnifiedInvoice                                   │
│     d) Match products (SHARED activity)                         │
│     e) Save to staging (SHARED activity)                        │
│     f) Acknowledge to supplier API                              │
│  5. Trigger NEX Genesis import (SHARED activity)                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Dátové modely

### UnifiedInvoice

Normalizovaný model faktúry - spoločný pre PDF aj API zdroje.

```python
@dataclass
class UnifiedInvoice:
    # Zdroj
    source_type: str            # "api" alebo "pdf"
    supplier_id: str            # napr. "marso", "continental"
    supplier_name: str
    
    # Hlavička faktúry
    invoice_number: str
    invoice_date: datetime
    due_date: Optional[datetime]
    delivery_date: Optional[datetime]
    
    # Dodávateľ
    supplier_ico: Optional[str]
    supplier_dic: Optional[str]
    supplier_ic_dph: Optional[str]
    
    # Sumy
    total_without_vat: float
    total_vat: float
    total_with_vat: float
    currency: str = "EUR"
    
    # Položky
    items: list[InvoiceItem]
    
    # Metadata
    raw_xml: Optional[str]      # Archív pôvodného XML
    fetched_at: datetime
    status: InvoiceStatus
    external_invoice_id: str    # ID v systéme dodávateľa
```

### InvoiceItem

```python
@dataclass
class InvoiceItem:
    line_number: int
    product_code: str           # Kód od dodávateľa
    product_code_type: str      # "ean", "marso_code", "continental_code"
    product_name: str
    quantity: float
    unit: str
    unit_price: float
    total_price: float
    vat_rate: float
    vat_amount: float
    
    # Voliteľné
    ean: Optional[str]
    supplier_product_code: Optional[str]
    
    # NEX Genesis mapovanie (po product matching)
    nex_product_id: Optional[str]
    nex_product_code: Optional[str]
    match_confidence: Optional[float]
```

### InvoiceStatus

```python
class InvoiceStatus(Enum):
    PENDING = "pending"
    FETCHED = "fetched"
    PROCESSED = "processed"
    ACKNOWLEDGED = "acknowledged"
    ERROR = "error"
```

---

## Adapter Pattern

### BaseSupplierAdapter (abstraktná trieda)

```python
class BaseSupplierAdapter(ABC):
    def __init__(self, config: SupplierConfig):
        self.config = config
    
    @abstractmethod
    async def authenticate(self) -> bool:
        """Autentifikácia podľa auth_type."""
        pass
    
    @abstractmethod
    async def fetch_invoice_list(self) -> list[str]:
        """Získa zoznam ID nespracovaných faktúr."""
        pass
    
    @abstractmethod
    async def fetch_invoice(self, invoice_id: str) -> str:
        """Stiahne XML faktúry."""
        pass
    
    @abstractmethod
    async def acknowledge_invoice(self, invoice_id: str) -> bool:
        """Označí faktúru ako spracovanú u dodávateľa."""
        pass
    
    @abstractmethod
    def parse_invoice(self, xml_content: str) -> UnifiedInvoice:
        """Parsuje XML do UnifiedInvoice."""
        pass
```

### SupplierConfig

```python
@dataclass
class SupplierConfig:
    supplier_id: str
    supplier_name: str
    auth_type: AuthType         # api_key, basic, oauth2, certificate
    base_url: str
    
    # Credentials (zo secure storage / .env)
    api_key: Optional[str]
    username: Optional[str]
    password: Optional[str]
    
    # Endpointy
    endpoint_list_invoices: str
    endpoint_get_invoice: str
    endpoint_acknowledge: str
    
    # Product code mapovanie
    product_code_field: str     # Názov poľa v XML
    product_code_type: str      # Typ: ean, marso_code, ...
    
    # Settings
    timeout_seconds: int = 30
    max_retries: int = 3
```

### AuthType

```python
class AuthType(Enum):
    API_KEY = "api_key"
    BASIC = "basic"
    OAUTH2 = "oauth2"
    CERTIFICATE = "certificate"
```

---

## YAML Konfigurácia

### Šablóna: _template.yaml

```yaml
# Supplier API Configuration Template
# Skopíruj a uprav pre nového dodávateľa

supplier_id: "supplier_code"
supplier_name: "Supplier Name s.r.o."

# Authentication
auth_type: "api_key"  # api_key | basic | oauth2 | certificate
# Credentials sa načítavajú z environment variables:
# {SUPPLIER_ID}_API_KEY, {SUPPLIER_ID}_USERNAME, {SUPPLIER_ID}_PASSWORD

# API Endpoints
base_url: "https://api.supplier.com"
endpoints:
  list_invoices: "/api/v1/invoices?status=pending"
  get_invoice: "/api/v1/invoices/{invoice_id}"
  acknowledge: "/api/v1/invoices/{invoice_id}/ack"

# Product Code Mapping
product_code:
  xml_field: "EAN"              # Názov elementu/atribútu v XML
  type: "ean"                   # ean | supplier_code | catalog_number
  nex_genesis_field: "EAN"      # Stĺpec v NEX Genesis produkt. katalógu

# Optional Settings
timeout_seconds: 30
max_retries: 3
rate_limit_per_minute: 60
```

### marso.yaml (doplniť po získaní dokumentácie)

```yaml
supplier_id: "marso"
supplier_name: "MARSO Slovakia s.r.o."

auth_type: "api_key"  # TODO: overiť podľa dokumentácie

base_url: "https://api.marso.sk"  # TODO: doplniť
endpoints:
  list_invoices: "/invoices?status=pending"  # TODO: doplniť
  get_invoice: "/invoices/{invoice_id}"       # TODO: doplniť
  acknowledge: "/invoices/{invoice_id}/ack"   # TODO: doplniť

product_code:
  xml_field: "MarsoCode"        # TODO: doplniť podľa vzorového XML
  type: "marso_code"
  nex_genesis_field: "MARSO_KOD"  # TODO: overiť názov stĺpca v NEX Genesis

timeout_seconds: 30
max_retries: 3
```

---

## Temporal Activities

### supplier_api_activities.py

```python
@activity.defn
async def load_supplier_config(supplier_id: str) -> SupplierConfig:
    """Načíta YAML konfiguráciu dodávateľa."""
    pass

@activity.defn
async def authenticate_supplier(config: SupplierConfig) -> str:
    """Autentifikuje sa a vráti token/session."""
    pass

@activity.defn
async def fetch_pending_invoices(supplier_id: str) -> list[str]:
    """Získa zoznam ID nespracovaných faktúr."""
    pass

@activity.defn
async def fetch_invoice_xml(supplier_id: str, invoice_id: str) -> str:
    """Stiahne XML konkrétnej faktúry."""
    pass

@activity.defn
async def archive_raw_xml(supplier_id: str, invoice_id: str, xml: str) -> str:
    """Uloží surové XML (filesystem + DB). Vráti cestu k súboru."""
    pass

@activity.defn
async def parse_invoice_xml(supplier_id: str, xml: str) -> UnifiedInvoice:
    """Parsuje XML do UnifiedInvoice pomocou príslušného adaptera."""
    pass

@activity.defn
async def acknowledge_invoice(supplier_id: str, invoice_id: str) -> bool:
    """Označí faktúru ako spracovanú u dodávateľa."""
    pass
```

### Zdieľané activities (invoice_activities.py)

Tieto activities sa použijú aj pre api_invoice_workflow:

```python
@activity.defn
async def match_products(invoice: UnifiedInvoice) -> UnifiedInvoice:
    """Mapuje product_code na NEX Genesis produkty."""
    pass

@activity.defn
async def save_to_staging(invoice: UnifiedInvoice) -> int:
    """Uloží do PostgreSQL staging tabuliek. Vráti ID."""
    pass

@activity.defn
async def import_to_nex_genesis(staging_id: int) -> bool:
    """Importuje do NEX Genesis."""
    pass
```

---

## Archivácia

Rovnaká stratégia ako pre PDF:

```
C:\NEX\IMPORT\SUPPLIER-INVOICES\           # received (nové)
C:\NEX\IMPORT\SUPPLIER-STAGING\            # staged (spracované)
C:\NEX\YEARACT\ARCHIV\SUPPLIER-INVOICES\
    ├── PDF\                               # PDF faktúry
    └── XML\                               # XML z API
        └── MARSO\
            └── 2025\
                └── 01\
                    └── 20250121_FV2025001.xml
```

**Pomenovanie:** `{timestamp}_{invoice_number}.xml`

---

## Environment Variables

```bash
# MARSO
MARSO_API_KEY=xxx
MARSO_BASE_URL=https://api.marso.sk

# CONTINENTAL (budúcnosť)
CONTINENTAL_API_KEY=xxx
CONTINENTAL_USERNAME=xxx
CONTINENTAL_PASSWORD=xxx
```

---

## TODO: Doplniť po získaní dokumentácie

- [ ] MARSO API endpointy (presné URL)
- [ ] MARSO autentifikačná metóda
- [ ] Štruktúra MARSO XML faktúry
- [ ] Názov poľa s MARSO product code v XML
- [ ] Názov stĺpca v NEX Genesis pre MARSO kód
- [ ] Rate limity MARSO API

---

## Referencie

- Existujúci PDF workflow: `apps/supplier-invoice-worker/workflows/pdf_invoice_workflow.py`
- Staging DB schéma: `apps/supplier-invoice-loader/`
- Product matching: `apps/supplier-invoice-loader/services/`