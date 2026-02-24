# MARSO Integration - Delphi Source Extraction

**Dátum extrakcie:** 2026-01-27
**Zdroj:** `C:\Development\delpi-source-codes\*.pas`
**Copyright:** ICC s.r.o. 2024
**Autor:** Zoltan Rausch

---

## 1. Nájdené súbory

| Súbor | Účel | Dátum vytvorenia |
|-------|------|------------------|
| `MarsoConverter.pas` | **XML/JSON konvertor (API Key!)** | 2024 |
| `DeliveryOrders_Marso.pas` | SOAP API klient pre objednávky | 2024-11-08 |
| `DeliveryOrders_OrderSender.pas` | Odosielanie objednávok | 2024-10-26 |
| `DeliveryOrders_OrderGenerator.pas` | Generovanie objednávok | 2024-10-23 |
| `MarsoFtpLoaderMain.pas` | FTP download katalógu/skladu | 2024 |
| `MarsoCatalogMain.pas` | Import katalógu do NEX | 2024-10-29 |
| `MarsoCatalogCsv.pas` | CSV parser pre katalóg | 2024-10-29 |
| `MarsoStockMain.pas` | Import skladu do NEX | 2024-08-12 |
| `MarsoStockCsv.pas` | CSV parser pre sklad | 2024-08-12 |

---

## 2. API Endpoint (SOAP)

### 2.1 Extrahované z `DeliveryOrders_Marso.pas:61`

```delphi
oResponseXml := mIdHTTP.Post(
  'http://195.228.175.10:8081/ComaxWS/Comax.asmx?op=CallComax',
  TStringStream.Create(pRequestXml)
);
```

| Parameter | Hodnota |
|-----------|---------|
| **URL** | `http://195.228.175.10:8081/ComaxWS/Comax.asmx?op=CallComax` |
| **Metóda** | POST |
| **Content-Type** | `text/xml` |
| **Protokol** | HTTP (nie HTTPS) |
| **Autentifikácia** | Prázdne (Username='', Password='') |

### 2.2 Poznámky

- Delphi používa **TIdHTTP** (Indy HTTP komponenta)
- SSL handler je pripravený, ale URL je HTTP
- Request XML sa posiela ako string stream
- Toto je **LIVE** endpoint (port 8081)

---

## 3. FTP Prístup

### 3.1 Extrahované z `MarsoFtpLoaderMain.pas:98-102`

```delphi
oFTP.Port     := 21;
oFTP.Passive  := TRUE;
oFTP.Host     := 'marso.icc.sk';
oFTP.UserName := 'marso.icc.sk';
oFTP.Password := 'Andros*2024';
```

| Parameter | Hodnota |
|-----------|---------|
| **Host** | `marso.icc.sk` |
| **Port** | 21 |
| **Username** | `marso.icc.sk` |
| **Password** | `Andros*2024` |
| **Passive mode** | TRUE |

### 3.2 Sťahované súbory

| Vzor na FTP | Lokálny názov | Účel |
|-------------|---------------|------|
| `cikkek_339792.csv` | `marso_stock.csv` | Skladové zásoby |
| `cikkek_339792.csv` | `marso_catalog.csv` | Katalóg produktov |

### 3.3 Lokálne adresáre

```
Import:  {ImpPath}\MARSO\
Archive: {ActArchivePath}\MARSO\STOCK\
         {ActArchivePath}\MARSO\CATALOG\
```

---

## 4. AccountNum / MARSO ID

### 4.1 Extrahované z `MarsoFtpLoaderMain.pas:132`

```delphi
oFTP.List(mDirLst,'cikkek_339792.csv',FALSE);
```

| Parameter | Hodnota | Použitie |
|-----------|---------|----------|
| **AccountNum** | `339792` | Súčasť názvu CSV súboru |

### 4.2 NEX Genesis interné ID

```delphi
// MarsoStockMain.pas:68
oMarsoId := 6690;   // TODO - do inicializačného parametra

// MarsoCatalogMain.pas:61
oContinentalId := 6690;   // TODO - do inicializačného parametra
```

| Parameter | Hodnota | Použitie |
|-----------|---------|----------|
| **PaCode (Partner ID)** | `6690` | ID dodávateľa v NEX Genesis |

---

## 5. CSV Štruktúra

### 5.1 Katalóg (`marso_catalog.csv`)

| Index | Pole | Popis |
|-------|------|-------|
| 1 | `SupplierId` | MARSO ID produktu |
| 2 | `ArticleName` | Názov produktu |
| 4 | `ArticleDesc` | Popis (groupname) |
| 6 | `BrandText` | Značka (brandname) |
| 7 | `ArticleInfo` | Info (pattern) |
| 11 | `Diameter` | Priemer pneumatiky (Coll) |
| 24 | `ArticleEan` | EAN-13 kód |
| 29 | `Weight` | Hmotnosť |

**Separator:** `;` (bodkočiarka)

### 5.2 Sklad (`marso_stock.csv`)

| Index | Pole | Popis |
|-------|------|-------|
| 1 | `SupplierId` | MARSO ID produktu |
| 24 | `ArticleEan` | EAN-13 kód |
| 25 | `AvailQuantity` | Dostupné množstvo |

**Separator:** `;` (bodkočiarka)

---

## 6. NEX Genesis databázové tabuľky

### 6.1 Použité handlery

| Handler | Tabuľka | Účel |
|---------|---------|------|
| `TDlvCatHnd` (hDLVCAT) | DLVCAT | Katalóg dodávateľov |
| `TStkOfrHnd` (hSTKOFR) | STKOFR | Ponuka na sklade |
| `TStkHnd` (hSTK) | STK | Skladové karty |
| `TGsi` | GSCAT | Produktový katalóg |

### 6.2 Mapovanie polí (DLVCAT)

| CSV pole | DB pole | Popis |
|----------|---------|-------|
| SupplierId | OrdCode | Objednávací kód |
| ArticleName | ProdName | Názov produktu |
| ArticleDesc | ProdDesc | Popis produktu |
| ArticleInfo | ProdInfo | Info o produkte |
| BrandText | BrandText | Značka |
| Weight | Weight | Hmotnosť |
| Diameter | Diameter | Priemer |
| ArticleEan | BarCode | Čiarový kód |

---

## 7. Workflow v Delphi

### 7.1 FTP Loader (`MarsoFtpLoaderMain`)

```
1. Connect to FTP (marso.icc.sk)
2. List files matching 'cikkek_339792.csv'
3. Download to {ImpPath}\MARSO\
4. Rename to marso_stock.csv / marso_catalog.csv
5. Launch NexService_MarsoStock.exe
```

### 7.2 Stock Import (`MarsoStockMain`)

```
1. Read marso_stock.csv from {ImpPath}\MARSO\
2. For each line:
   - Lookup EAN in GSCAT (TGsi.LocateBarCode)
   - Update/Insert STKOFR (offer quantity)
3. Recalculate STK cards (OfrQnt sum)
4. Archive CSV to {ActArchivePath}\MARSO\STOCK\
```

### 7.3 Catalog Import (`MarsoCatalogMain`)

```
1. Read marso_catalog.csv from {ImpPath}\MARSO\
2. For each line with valid EAN (>=13 chars):
   - Lookup EAN in DLVCAT (TDlvCatHnd.LocPcBc)
   - Update/Insert product data
3. Archive CSV to {ActArchivePath}\MARSO\CATALOG\
```

---

## 8. API Key

### 8.1 Extrahované z `MarsoConverter.pas:63,131`

```delphi
// InquiryRequest (riadok 62-63)
mXmlData.Add('                <AccountNum>339792</AccountNum>');
mXmlData.Add('                <Key>feixRjG254zft3zqnxx4kACZHEyX01</Key>');

// OrderRequest (riadok 130-131)
mXmlData.Add('                <AccountNum>339792</AccountNum>');
mXmlData.Add('                <Key>feixRjG254zft3zqnxx4kACZHEyX01</Key>');
```

| Parameter | Hodnota | Zdroj |
|-----------|---------|-------|
| **API Key** | `feixRjG254zft3zqnxx4kACZHEyX01` | MarsoConverter.pas:63,131 |
| **AccountNum** | `339792` | MarsoConverter.pas:62,130 |

### 8.2 SOAP Request parametre

| Parameter | Hodnota | Zdroj |
|-----------|---------|-------|
| Sender | `WebCatHU` | MarsoConverter.pas:53 |
| Receiver | `Ax` | MarsoConverter.pas:54 |

### 8.3 MessageTypes

| Typ | MessageType | Použitie |
|-----|-------------|----------|
| Inquiry | `ItemQty` | Dopyt na dostupnosť tovaru |
| Order | `CreateSalesOrder` | Vytvorenie objednávky |

### 8.4 Konfigurácia v nex-automat

```bash
# apps/supplier-invoice-worker/.env
MARSO_API_KEY=feixRjG254zft3zqnxx4kACZHEyX01
MARSO_ACCOUNT_NUM=339792
MARSO_USE_TEST=false
```

**Jeden API Key** sa používa pre všetky operácie (objednávky, inquiry, faktúry).

---

## 9. Zhrnutie extrahovaných hodnôt

### Credentials

| Typ | Hodnota | Zdroj |
|-----|---------|-------|
| **API Key** | `feixRjG254zft3zqnxx4kACZHEyX01` | MarsoConverter.pas:63,131 |
| **AccountNum** | `339792` | MarsoConverter.pas:62 |
| **SOAP URL** | `http://195.228.175.10:8081/ComaxWS/Comax.asmx?op=CallComax` | DeliveryOrders_Marso.pas:61 |
| **FTP Host** | `marso.icc.sk` | MarsoFtpLoaderMain.pas:100 |
| **FTP User** | `marso.icc.sk` | MarsoFtpLoaderMain.pas:101 |
| **FTP Pass** | `Andros*2024` | MarsoFtpLoaderMain.pas:102 |
| **NEX PaCode** | `6690` | MarsoStockMain.pas:68 |

### Endpointy

| Typ | URL/Adresa |
|-----|------------|
| SOAP LIVE | `http://195.228.175.10:8081/ComaxWS/Comax.asmx` |
| SOAP TEST | `http://195.228.175.10:8082/ComaxWS/Comax.asmx` |
| FTP | `ftp://marso.icc.sk:21` |

---

## 10. SOAP Request štruktúry (MarsoConverter.pas)

### 10.1 ItemQty Request (Inquiry)

```xml
<Document>
  <ComaxEnvelope>
    <Sender>WebCatHU</Sender>
    <Receiver>Ax</Receiver>
    <MessageType>ItemQty</MessageType>
    <test>0</test>
  </ComaxEnvelope>
  <Message>
    <Customer>
      <AccountNum>339792</AccountNum>
      <Key>feixRjG254zft3zqnxx4kACZHEyX01</Key>
    </Customer>
    <Item>
      <ItemId>{MARSO_ITEM_ID}</ItemId>
      <InventLocationId>DH02</InventLocationId>
      <MaxAgeMonth>20</MaxAgeMonth>
    </Item>
  </Message>
</Document>
```

### 10.2 CreateSalesOrder Request

```xml
<Document>
  <ComaxEnvelope>
    <Sender>WebCatHU</Sender>
    <Receiver>Ax</Receiver>
    <MessageType>CreateSalesOrder</MessageType>
    <test>0</test>
  </ComaxEnvelope>
  <Message>
    <RendelesFej>
      <AccountNum>339792</AccountNum>
      <Key>feixRjG254zft3zqnxx4kACZHEyX01</Key>
      <RendelesForrasa>Web</RendelesForrasa>
      <CimTipus>1</CimTipus>
      <Name>Andros s.r.o.</Name>
      <ZipCode>81102</ZipCode>
      <City>Bratislava</City>
      <Street>Tallerova 4.</Street>
      <CountryRegionId>SK</CountryRegionId>
      <Phone>00421908235971</Phone>
      <Email>haburova@pneueshop.sk</Email>
      <Reszleg>111</Reszleg>
      <Szallitasi_Mod>5</Szallitasi_Mod>
      <SenderOrderId>{ORDER_ID}</SenderOrderId>
    </RendelesFej>
    <RendelesSorok>
      <RendelesSor>
        <ItemId>{ITEM_ID}</ItemId>
        <Qty>{QUANTITY}</Qty>
        <MegrendeloRendelesSorAzonosito>{LINE_NUM}</MegrendeloRendelesSorAzonosito>
      </RendelesSor>
    </RendelesSorok>
  </Message>
</Document>
```

### 10.3 Delivery modes (Szallitasi_Mod)

| Kód | Dopravca |
|-----|----------|
| 1 | MPL (HU Post) |
| 5 | *(aktuálne použité)* |
| 50 | DPD |
| 51 | DACHSER |
| 52 | GLS |
| 60 | Nemo Express |

---

*Dokument vygenerovaný z Delphi zdrojových kódov NEX Genesis.*
*Aktualizované: 2026-01-27 - pridaný API Key z MarsoConverter.pas*
