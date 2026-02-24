# MARSO API Documentation - Extracted from NEX Sources

**Dátum extrakcie:** 2026-01-27
**Zdroje:** nex-automat, nex-genesis-server
**Status:** Kompletné

---

## 1. Prehľad zdrojov

### 1.1 Prehľadané lokácie

| Lokácia | Typ súborov | MARSO obsah |
|---------|-------------|-------------|
| `C:\Development\delphi-source-codes\` | - | **Neexistuje** |
| `C:\Development\nex-genesis-server\delphi-sources\` | *.pas | Len Btrieve API (žiadne MARSO) |
| `C:\Development\nex-automat\apps\supplier-invoice-worker\` | *.py, *.yaml | **Kompletná implementácia** |
| `C:\Development\nex-automat\apps\supplier-invoice-loader\` | *.py | PDF extractor (nie API) |

### 1.2 Súbory obsahujúce MARSO referencie

```
nex-automat/apps/supplier-invoice-worker/
├── adapters/marso_adapter.py           # SOAP klient
├── converters/marso_to_isdoc.py        # JSON → ISDOC konvertor
├── config/suppliers/marso.yaml         # Konfigurácia
├── tests/test_marso_adapter.py         # Unit testy
└── tests/test_marso_converter.py       # Unit testy

nex-automat/apps/supplier-invoice-loader/
└── src/extractors/marso_extractor.py   # PDF extrakcia (nie API)

nex-automat/docs/knowledge/specifications/
└── 2026-01-26_marso-api-phase2.md      # Kompletná špecifikácia
```

---

## 2. API Endpoints

### 2.1 SOAP WSDL

| Prostredie | URL |
|------------|-----|
| **TEST** | `http://195.228.175.10:8082/ComaxWS/Comax.asmx?wsdl` |
| **LIVE** | `http://195.228.175.10:8081/ComaxWS/Comax.asmx?wsdl` |

### 2.2 SOAP Metóda

```
Method: CallComax
Protocol: SOAP 1.1/1.2
Response Format: JSON (nie XML!)
```

### 2.3 MessageTypes (virtuálne endpointy)

| MessageType | Účel | Použitie |
|-------------|------|----------|
| `CustInvoiceList` | Kompletné faktúry (hlavičky + riadky) | **Primárny** |
| `CustInvoices` | Len hlavičky faktúr | Sekundárny |
| `CustInvoiceLines` | Riadky konkrétnej faktúry | Detail |

---

## 3. Autentifikácia

### 3.1 Typ autentifikácie

```
Typ: API Key v XML body (nie HTTP header!)
```

### 3.2 Parametre

| Parameter | Hodnota | Zdroj |
|-----------|---------|-------|
| AccountNum | `339792` | Environment / hardcoded |
| Key | `***` | `MARSO_API_KEY` v .env |
| Sender | `WebCatHU` | Statické |
| Receiver | `Ax` | Statické |

### 3.3 Environment premenné

```bash
# .env súbor
MARSO_API_KEY=<api_key_hodnota>
MARSO_ACCOUNT_NUM=339792
MARSO_USE_TEST=true
```

---

## 4. Request/Response štruktúry

### 4.1 Request XML (CustInvoiceList)

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
    <DatumTol>2026-01-01</DatumTol>
    <DatumIg>2026-01-31</DatumIg>
    <SzlSzamResz></SzlSzamResz>
    <Key>{MARSO_API_KEY}</Key>
  </Message>
</Document>
```

### 4.2 Request XML (CustInvoiceLines - detail)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Document>
  <ComaxEnvelope>
    <Sender>WebCatHU</Sender>
    <Receiver>Ax</Receiver>
    <MessageType>CustInvoiceLines</MessageType>
    <MessageId/>
    <RespMessageId/>
    <test>0</test>
  </ComaxEnvelope>
  <Message>
    <AccountNum>339792</AccountNum>
    <SzlSzamResz>11926-00447</SzlSzamResz>
    <Key>{MARSO_API_KEY}</Key>
  </Message>
</Document>
```

### 4.3 Response JSON (faktúra)

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
  "InvStreet": "Hradná 123",
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

---

## 5. Mapovanie polí

### 5.1 Hlavička faktúry

| MARSO JSON | Popis | ISDOC XML |
|------------|-------|-----------|
| `InvoiceId` | Číslo faktúry | `<ID>` |
| `SalesId` | Interné číslo objednávky | `<Note>` |
| `Kelt` | Dátum vystavenia | `<IssueDate>` |
| `Teljesites` | Dátum plnenia | `<TaxPointDate>` |
| `Hatarido` | Dátum splatnosti | `<PaymentDueDate>` |
| `Penznem` | Mena (EUR, HUF) | `<LocalCurrencyCode>` |
| `Netto` | Suma bez DPH | `<TaxExclusiveAmount>` |
| `Afa` | DPH | `<TaxAmount>` |
| `Brutto` | Suma s DPH | `<TaxInclusiveAmount>` |

### 5.2 Adresa zákazníka

| MARSO JSON | Popis |
|------------|-------|
| `InvName` | Názov firmy |
| `InvStreet` | Ulica |
| `InvCity` | Mesto |
| `InvZipCode` | PSČ |
| `InvCountryRegionId` | Kód krajiny (SK, HU, CZ) |

### 5.3 Riadky faktúry

| MARSO JSON | Popis | ISDOC XML |
|------------|-------|-----------|
| `ItemId` | EAN kód produktu | `<SellersItemIdentification/ID>` |
| `ItemName` | Názov produktu | `<Description>` |
| `Qty` | Množstvo | `<InvoicedQuantity>` |
| `SalesUnit` | Jednotka (Db, Pr, Kg, M) | `@unitCode` |
| `Netto` | Cena bez DPH | `<LineExtensionAmount>` |
| `Afa` | DPH | `<LineExtensionTaxAmount>` |
| `Brutto` | Cena s DPH | `<LineExtensionAmountTaxInclusive>` |
| `ItemGroupid` | Skupina tovaru | - |

### 5.4 Mapovanie jednotiek

| MARSO | UN/ECE | Popis |
|-------|--------|-------|
| `Db` | `PCE` | Kus (piece) |
| `Pr` | `PR` | Pár (pair) |
| `Kg` | `KGM` | Kilogram |
| `M` | `MTR` | Meter |
| `L` | `LTR` | Liter |

---

## 6. Dodávateľ (hardcoded)

```
ID: MARSO
Názov: MARSO Hungary Kft.
IČO: 10428342
DIČ: HU10428342
Krajina: HU
Mesto: Budapest
Ulica: Maglódi út 6.
PSČ: 1106
```

---

## 7. Konštanty a konfigurácia

### 7.1 marso.yaml

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
  invoice_detail: CustInvoiceLines

response:
  format: json
  invoice_id_field: InvoiceId
  lines_field: Lines
  product_code_field: ItemId
  product_code_type: ean

schedule:
  cron: "0 6 * * *"
  lookback_days: 7
```

---

## 8. Implementačné poznámky

### 8.1 SOAP špecifiká

1. **Response je JSON, nie XML** - MARSO API vracia JSON string cez SOAP
2. **Autentifikácia v body** - API key nie je v HTTP hlavičke, ale v XML tele
3. **Zeep knižnica** - Python SOAP klient pre komunikáciu

### 8.2 Chybové stavy

| Stav | Správanie |
|------|-----------|
| Neplatný Key | Prázdna odpoveď |
| Neplatný AccountNum | Prázdna odpoveď |
| Neexistujúca faktúra | Prázdny JSON list `[]` |
| Timeout | SOAP TransportError |

### 8.3 Deduplikácia

- Faktúry sa identifikujú podľa `InvoiceId`
- DB constraint zabraňuje duplikátom
- Workflow spracováva len nové faktúry

---

## 9. Kontakty MARSO

| Osoba | Email | Téma |
|-------|-------|------|
| Imre Belinszki | imre@marso.hu | API parametre, ERP chyby |
| Tamás Nagy | nagy.tamas@marso.hu | Technické problémy |

---

## 10. Súvisiace súbory

| Súbor | Účel |
|-------|------|
| `marso_adapter.py` | SOAP klient implementácia |
| `marso_to_isdoc.py` | JSON → ISDOC XML konvertor |
| `marso.yaml` | Konfigurácia dodávateľa |
| `supplier_api_activities.py` | Temporal activities |
| `api_invoice_workflow.py` | Temporal workflow |
| `marso_extractor.py` | PDF extrakcia (alternatívny vstup) |

---

*Dokument vygenerovaný z existujúcich zdrojov v nex-automat projekte.*
