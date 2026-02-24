# MARSO API Integration - Phase 2 Strategy

**Dátum:** 2026-01-26  
**Projekt:** nex-automat  
**Zákazník:** ANDROS s.r.o.  
**Dodávateľ:** MARSO Slovakia s.r.o. (MARSO Hungary Kft.)  
**Status:** Phase 2 - Implementation Ready

---

## 1. Executive Summary

### 1.1 Cieľ
Automatizované získavanie faktúr od MARSO cez SOAP API a konverzia do ISDOC XML pre jednotný pipeline.

### 1.2 Kľúčový princíp
```
MARSO SOAP API → JSON Response → ISDOC XML → POST /invoice → Existujúci pipeline
```

### 1.3 Výhoda
Nulové zmeny v existujúcom spracovaní. API faktúry vstupujú rovnakou cestou ako PDF.

---

## 2. MARSO API Špecifikácia

### 2.1 Pripojenie

| Parameter | Test | Produkcia |
|-----------|------|-----------|
| WSDL | `http://195.228.175.10:8082/ComaxWS/Comax.asmx?wsdl` | `http://195.228.175.10:8081/ComaxWS/Comax.asmx?wsdl` |
| Protocol | SOAP 1.1/1.2 | SOAP 1.1/1.2 |
| Method | CallComax | CallComax |
| Response | **JSON** | **JSON** |

### 2.2 Autentifikácia

| Parameter | Hodnota |
|-----------|---------|
| AccountNum | 339792 |
| Key | *(MARSO_API_KEY v .env)* |
| Typ | API key v XML body (nie HTTP header) |

### 2.3 Endpoint: CustInvoiceList

**Request XML:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Document>
  <ComaxEnvelope>
    <Sender>WebCatHU</Sender>
    <Receiver>Ax</Receiver>
    <MessageType>CustInvoiceList</MessageType>
    <MessageId/>
    <RespMessageId/>
    <test>0</test>
  </ComaxEnvelope>
  <Message>
    <AccountNum>339792</AccountNum>
    <DatumTol>{date_from}</DatumTol>
    <DatumIg>{date_to}</DatumIg>
    <SzlSzamResz></SzlSzamResz>
    <Key>{api_key}</Key>
  </Message>
</Document>
```

**Response JSON:**
```json
{
  "InvoiceId": "11926-00447",
  "SalesId": "VR1234567",
  "Kelt": "2026-01-15",
  "Teljesites": "2026-01-15",
  "Hatarido": "2026-01-30",
  "InvName": "ANDROS s.r.o.",
  "InvZipCode": "94501",
  "InvCity": "Komárno",
  "InvStreet": "...",
  "InvCountryRegionId": "SK",
  "Netto": 1000.00,
  "Afa": 200.00,
  "Brutto": 1200.00,
  "Penznem": "EUR",
  "Lines": [
    {
      "ItemId": "ABC123456",
      "ItemName": "Michelin Pilot Sport 4 225/45R17",
      "Qty": 4,
      "SalesUnit": "Db",
      "Netto": 250.00,
      "Afa": 50.00,
      "Brutto": 300.00,
      "ItemGroupid": "140"
    }
  ]
}
```

### 2.4 Alternatívne endpointy

| MessageType | Účel |
|-------------|------|
| CustInvoiceList | Kompletné faktúry (hlavičky + riadky) - **PRIMÁRNY** |
| CustInvoices | Len hlavičky faktúr |
| CustInvoiceLines | Riadky konkrétnej faktúry (podľa InvoiceId) |

---

## 3. Mapovanie MARSO → ISDOC

### 3.1 Hlavička faktúry

| MARSO JSON | ISDOC XML | DB stĺpec |
|------------|-----------|-----------|
| InvoiceId | `<ID>` | xml_invoice_number |
| Kelt | `<IssueDate>` | xml_issue_date |
| Teljesites | `<TaxPointDate>` | xml_tax_point_date |
| Hatarido | `<DueDate>` | xml_due_date |
| Penznem | `<LocalCurrencyCode>` | xml_currency |
| Netto | `<TaxExclusiveAmount>` | xml_total_without_vat |
| Afa | `<TaxAmount>` | xml_total_vat |
| Brutto | `<TaxInclusiveAmount>` | xml_total_with_vat |

### 3.2 Dodávateľ (hardcoded)

| ISDOC Element | Hodnota |
|---------------|---------|
| PartyIdentification/ID | MARSO |
| PartyName | MARSO Hungary Kft. |
| CompanyID (IČO) | 10428342 |
| VATRegistrationID | HU10428342 |
| Country | HU |

### 3.3 Riadky faktúry

| MARSO JSON | ISDOC XML | DB stĺpec |
|------------|-----------|-----------|
| ItemId | `<SellersItemIdentification/ID>` | xml_seller_code |
| ItemName | `<Description>` | xml_product_name |
| Qty | `<InvoicedQuantity>` | xml_quantity |
| SalesUnit | `@unitCode` ("Db"→"PCE") | xml_unit |
| Netto (line) | `<LineExtensionAmount>` | xml_total_price |
| Brutto (line) | `<LineExtensionAmountTaxInclusive>` | xml_total_price_vat |

---

## 4. Phase 1 Analysis - Existujúci kód

### 4.1 Kompletné komponenty ✅

| Súbor | Využitie |
|-------|----------|
| `adapters/base_adapter.py` | AuthType, SupplierConfig, BaseSupplierAdapter |
| `models/unified_invoice.py` | InvoiceStatus, InvoiceItem, UnifiedInvoice |
| `config/config_loader.py` | load_supplier_config(), list_available_suppliers() |

### 4.2 Skeleton komponenty ⚠️

| Súbor | Hotové | TODO |
|-------|--------|------|
| `supplier_api_activities.py` | load_supplier_config() | 6 activities |
| `api_invoice_workflow.py` | Štruktúra 100% | Závisí na activities |
| `marso.yaml` | Štruktúra | Nesprávne hodnoty |

### 4.3 GAP - Predpoklady vs Realita

| Aspekt | Phase 1 predpoklad | MARSO realita |
|--------|-------------------|---------------|
| Protokol | REST API | **SOAP** |
| Response | XML | **JSON** |
| Endpoint | `/invoices?status=pending` | `CustInvoiceList` |
| Auth | Header/query param | **Key v XML body** |

---

## 5. Architektúra

```
┌─────────────────────────────────────────────────────────────────────┐
│                        VSTUPNÉ ADAPTÉRY                             │
├──────────────────────────┬──────────────────────────────────────────┤
│   PDF Faktúry (email)    │         API Faktúry (MARSO)              │
│                          │                                          │
│   Email IMAP             │    api_invoice_workflow                  │
│       ↓                  │         ↓                                │
│   pdf_invoice_workflow   │    marso_adapter.py (SOAP)               │
│       ↓                  │         ↓                                │
│   POST /invoice + PDF    │    JSON response                         │
│       ↓                  │         ↓                                │
│   marso_extractor.py     │    marso_to_isdoc.py                     │
│       ↓                  │         ↓                                │
│   ISDOC XML              │    ISDOC XML                             │
│                          │         ↓                                │
│                          │    POST /invoice (source: "api")         │
└──────────┬───────────────┴──────────────┬───────────────────────────┘
           │                              │
           └──────────────┬───────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────────┐
│              JEDNOTNÝ PIPELINE (supplier-invoice-loader)            │
│   POST /invoice → Validácia ISDOC → PostgreSQL → Staging GUI        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 6. Workflow

### 6.1 Temporal Workflow: api_invoice_workflow

```
1. LOAD CONFIG
   Activity: load_supplier_config("marso")
   
2. FETCH INVOICES  
   Activity: fetch_invoices_soap(config, date_range)
   SOAP call: CustInvoiceList
   Output: List[JSON]
   
3. PRE KAŽDÚ FAKTÚRU:
   a) convert_to_isdoc(marso_json) → ISDOC XML
   b) archive_raw_response(marso_json) → audit
   c) send_to_loader(isdoc_xml) → POST /invoice
   
4. EXISTUJÚCI PIPELINE
   - PostgreSQL staging
   - Staging GUI
   - NEX Genesis import
```

### 6.2 Scheduling

| Parameter | Hodnota |
|-----------|---------|
| Frekvencia | Denne o 06:00 |
| Rozsah | Posledných 7 dní |
| Deduplikácia | Podľa InvoiceId (DB constraint) |

---

## 7. Komponenty Phase 2

### 7.1 Nové a upravené súbory

```
apps/supplier-invoice-worker/
├── adapters/
│   ├── base_adapter.py            # UPDATE - SOAP support
│   └── marso_adapter.py           # NOVÝ - SOAP client (zeep)
├── converters/
│   ├── __init__.py                # NOVÝ
│   └── marso_to_isdoc.py          # NOVÝ - JSON → ISDOC
├── activities/
│   └── supplier_api_activities.py # UPDATE - implementovať activities
├── config/
│   ├── config_loader.py           # UPDATE - SOAP fields
│   └── suppliers/
│       └── marso.yaml             # UPDATE - SOAP konfigurácia
└── workflows/
    └── api_invoice_workflow.py    # UPDATE - minor
```

### 7.2 Rozhrania

**MARSOAdapter:**
```python
class MARSOAdapter(BaseSupplierAdapter):
    async def authenticate(self) -> bool
    async def fetch_invoice_list(self, date_from, date_to) -> List[dict]
    # acknowledge_invoice - MARSO nemá
```

**MARSOToISDOCConverter:**
```python
class MARSOToISDOCConverter:
    def convert(self, marso_json: dict) -> str  # ISDOC XML
    def validate(self, isdoc_xml: str) -> bool
```

---

## 8. Konfigurácia

### 8.1 marso.yaml (nový formát)

```yaml
supplier_id: marso
supplier_name: MARSO Hungary Kft.
supplier_country: HU
supplier_ico: "10428342"
supplier_vat: HU10428342

connection:
  protocol: soap
  wsdl_test: http://195.228.175.10:8082/ComaxWS/Comax.asmx?wsdl
  wsdl_live: http://195.228.175.10:8081/ComaxWS/Comax.asmx?wsdl
  method: CallComax
  timeout: 30

auth:
  type: api_key_in_body
  key_field: Key
  account_field: AccountNum

request:
  sender: WebCatHU
  receiver: Ax
  test_mode: "0"

endpoints:
  invoice_list: CustInvoiceList
  invoice_lines: CustInvoiceLines

response:
  format: json
  invoice_id_field: InvoiceId
  lines_field: Lines
  product_code_field: ItemId

schedule:
  cron: "0 6 * * *"
  lookback_days: 7
```

### 8.2 Environment (.env)

```bash
MARSO_API_KEY=szcLyD2YMR0A1uqcOpYxV50qTJ37qX
MARSO_ACCOUNT_NUM=339792
MARSO_USE_TEST=true
```

---

## 9. Implementačné fázy

### 9.1 Priorita 1 - Core (~15h)

| Fáza | Úloha | Súbor |
|------|-------|-------|
| F1.1 | Rozšíriť SupplierConfig pre SOAP | base_adapter.py |
| F1.2 | Aktualizovať config_loader | config_loader.py |
| F1.3 | Prepísať MARSO config | marso.yaml |
| F1.4 | MARSO SOAP adapter | marso_adapter.py |
| F1.5 | JSON → ISDOC konvertor | marso_to_isdoc.py |
| F1.6 | Implementovať activities | supplier_api_activities.py |
| F1.7 | Unit testy | test_marso_*.py |

### 9.2 Priorita 2 - Integrácia (~6h)

| Fáza | Úloha | Súbor |
|------|-------|-------|
| F2.1 | Upraviť workflow | api_invoice_workflow.py |
| F2.2 | POST /invoice rozšírenie | main.py (loader) |
| F2.3 | E2E test | - |
| F2.4 | Dokumentácia | docs/knowledge/ |

---

## 10. Kontakty

### MARSO
| Osoba | Email | Téma |
|-------|-------|------|
| Imre Belinszki | imre@marso.hu | API parametre, ERP chyby |
| Tamás Nagy | nagy.tamas@marso.hu | Spojenie, technické |

---

## 11. Referencie

- Phase 1 dokumentácia: `KNOWLEDGE_2025-01-21_supplier-api-phase1.md`
- Špecifikácia: `SUPPLIER_API_INTEGRATION_SPEC.md`
- DB schéma: `2025-12-18_supplier-invoice-staging-db.md`
- Existujúci MARSO extractor (PDF): `marso_extractor.py`