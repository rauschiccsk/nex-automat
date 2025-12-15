# NEX Automat v2.0 - Aktuálny stav (Historical Snapshot)

**Kategória:** Archive  
**Status:** 📦 Archived  
**Snapshot Date:** 2025-11-26  
**GO-LIVE Date:** 2025-11-27  
**Note:** Historical document - reflects project state at v2.0 GO-LIVE

---

## ⚠️ ARCHIVAL NOTICE

This document represents the project state as of **2025-11-26**, the day before GO-LIVE for Mágerstav preview/demo.

**Since this snapshot:**
- n8n workflows → migrated to Temporal
- Many "⚪ NÁVRH" items → implemented
- Btrieve WRITE operations → completed
- Architecture evolved significantly

For current project state, see:
- [PROJECT_VISION.md](../strategic/PROJECT_VISION.md)
- [PROJECT_ROADMAP.md](../strategic/PROJECT_ROADMAP.md)
- [ARCHITECTURE.md](../system/ARCHITECTURE.md)

---

## 1. PREHĽAD PROJEKTU

### 1.1 Vízia
NEX Automat = Kompletná automatizácia podnikových procesov pre zákazníkov používajúcich NEX Genesis ERP.

### 1.2 Stratégia
Postupná cesta: Čiastočná → Úplná automatizácia

### 1.3 Pilotný zákazník
**Mágerstav s.r.o.** - spracovanie dodávateľských faktúr od L&Š s.r.o.

---

## 2. ARCHITEKTÚRA SYSTÉMU

**ICC Server (Dev Center)**
- n8n Workflows (IMAP → PDF → API)
- Email: magerstavinvoice@gmail.com (dedikovaná schránka)

↓ HTTPS via Cloudflare Tunnel ↓

**Zákazník Server (Mágerstav)**
- FastAPI (supplier-invoice-loader)
- File Storage: C:\NEX\IMPORT\PDF\ + XML\
- PostgreSQL: DB invoice_staging (invoices + invoice_items)
- GUI (PyQt5): supplier-invoice-editor
- NEX Genesis (Btrieve): C:\NEX\DATA\

---

## 3. MANUÁLNY PROCES vs NEX AUTOMAT

### 3.1 Pôvodný 21-krokový manuálny proces

| # | Krok | NEX Automat | Poznámka |
|---|------|-------------|----------|
| 1 | Faktúra príde emailom (PDF) | ✅ HOTOVÉ | n8n IMAP trigger |
| 2 | Operátor otvorí PDF v prehliadači | ✅ HOTOVÉ | Automatické spracovanie |
| 3 | Otvorí NEX Genesis → Editor DL | ⚪ NÁVRH | GUI aplikácia |
| 4 | Zaeviduje hlavičku dokladu | ⚪ NÁVRH | TSH zápis |
| 5 | Otvorí položky dodacieho listu | ⚪ NÁVRH | TSI zápis |
| 6a | Identifikácia tovaru podľa EAN | ✅ HOTOVÉ | NEX Lookup Service |
| 6b | Ak tovar neexistuje → vytvorenie karty | ⚪ NÁVRH | GSCAT + BARCODE zápis |
| 6c | Výber tovaru z katalógu | ✅ HOTOVÉ | Staging DB |
| 6d | Zadanie množstva a ceny z PDF | ✅ HOTOVÉ | AI extrakcia (regex) |
| 6e | Uloženie položky | ⚪ NÁVRH | TSI zápis |
| 7 | Kontrola: Suma PDF = Suma NEX | ⚪ NÁVRH | Validácia v GUI |
| 8 | Ak nesedí → hľadanie a oprava | ⚪ NÁVRH | GUI editácia |
| 9 | Status: "Pripravený" | ⚪ NÁVRH | TSH status |
| 10 | Kontrola percentuálnej marže | ⚪ NÁVRH | GUI kalkulácia |
| 11 | Ak marža < min → Požiadavka na zmenu cien | ⚪ NÁVRH | RPC zápis |
| 12-21 | Naskladnenie + Recovery | ❌ MIMO SCOPE | Robí NEX Genesis |

**Legenda:**
- ✅ HOTOVÉ - Implementované v NEX Automat v2.0
- ⚪ NÁVRH - Navrhnuté, čaká na implementáciu
- ❌ MIMO SCOPE - Nebude súčasťou v2.0

---

## 4. KOMPONENTY - DETAILNÝ POPIS

### 4.1 n8n Workflow

**Názov:** `n8n-SupplierInvoiceEmailLoader`  
**ID:** `yBsDIpw6oMs96hi6`  
**Status:** ✅ ACTIVE  

**Flow:**
```
Email Trigger (IMAP)
    ↓
Split PDF (JavaScript)
    ↓
Has PDF Attachment? (Switch)
    ├── Has PDF → HTTP POST → FastAPI /invoice
    └── No PDF → Gmail Error Notification
```

**Parametre:**

| Parameter | Hodnota |
|-----------|---------|
| Mailbox | magerstavinvoice@gmail.com |
| Endpoint | https://magerstav-invoices.icc.sk/invoice |
| Auth | X-API-Key (env: LS_API_KEY) |
| Timeout | 120s |
| Error notify | rausch@em-1.sk |

**Aktuálny model:** Human-in-the-loop
- Operátor Mágerstav kontroluje prichádzajúce faktúry
- Len schválené preposiela do dedikovanej schránky
- n8n spracuje všetko z tejto schránky

**Roadmap:**
- Budúcnosť: Priamy email od dodávateľa → Automatizácia (bez operátora)

---

### 4.2 PDF Extrakcia (supplier-invoice-loader)

**Metóda:** Regex-first (bez AI tokenov)

**Architektúra:**
```
PDF → pdfplumber → Regex Extractor → InvoiceData → ISDOC Generator → XML
                        ↓
              (budúcnosť: AI validácia)
```

**Súbory:**
- `src/extractors/ls_extractor.py` - L&Š špecifický extraktor
- `src/extractors/generic_extractor.py` - Pripravený pre ďalších dodávateľov
- `src/business/isdoc_service.py` - ISDOC 6.0.1 XML generátor

**Úspešnosť:** 100% pre L&Š faktúry

**Stratégia:**
1. Regex-first: Každý dodávateľ = vlastný regex extraktor
2. AI validácia (TODO): Kontrola výsledku regex pomocou Claude
3. AI fallback (TODO): Ak regex zlyhá, použiť AI extrakciu

---

### 4.3 FastAPI (supplier-invoice-loader)

**Verzia:** 2.0.0  
**Deployment:** Windows Service  
**Port:** 8000 (default)  

**Endpoints:**

| Endpoint | Auth | Popis |
|----------|------|-------|
| `GET /` | ❌ | Service info |
| `GET /health` | ❌ | Health check |
| `GET /metrics` | ❌ | JSON metrics |
| `GET /metrics/prometheus` | ❌ | Prometheus format |
| `GET /stats` | ❌ | DB statistics |
| `GET /status` | ✅ | Detailed status |
| `GET /invoices` | ✅ | List invoices |
| `POST /invoice` | ✅ | **Main processing** |
| `POST /admin/test-email` | ✅ | Test SMTP |
| `POST /admin/send-summary` | ✅ | Daily summary |

**Cloudflare Tunnel:**

| Parameter | Stav |
|-----------|------|
| Konfigurácia | ✅ Hotová |
| Test u zákazníka | ✅ Funguje |
| Windows Service | ⚠️ TODO |

---

### 4.4 supplier-invoice-loader (celkovo)

**Lokácia:** `apps/supplier-invoice-loader`  
**Python súbory:** 53  
**Test coverage:** 85% (72 testov, 61 passed, 11 skipped)  

**File Storage:**
```
C:\NEX\IMPORT\
├── PDF\     ← originálne faktúry
└── XML\     ← ISDOC výstup
```

**TODO:**
- [ ] Automatický backup (Task Scheduler)
- [ ] Overiť SMTP konfiguráciu
- [ ] Cloudflare Tunnel ako Windows Service

---

### 4.5 supplier-invoice-editor

**Lokácia:** `apps/supplier-invoice-editor`  
**Technológia:** PyQt5 GUI  
**Python súbory:** 48  

**Štruktúra:**
```
src/
├── ui/
│   ├── main_window.py          # Zoznam faktúr
│   ├── invoice_detail_window.py # Detail faktúry
│   └── widgets/
│       ├── invoice_list_widget.py
│       └── invoice_items_grid.py
├── business/
│   ├── invoice_service.py      # CRUD operácie
│   └── nex_lookup_service.py   # EAN → GSCAT lookup
├── database/
│   └── postgres_client.py      # PostgreSQL prístup
├── btrieve/
│   └── btrieve_client.py       # Btrieve prístup
└── models/
    ├── gscat.py                # Produkty
    ├── barcode.py              # EAN kódy
    ├── pab.py                  # Partneri
    └── mglst.py                # Tovarové skupiny
```

**Čo funguje:**
- ✅ GUI zobrazenie faktúr a položiek
- ✅ PostgreSQL čítanie/zápis
- ✅ Btrieve READ (GSCAT, BARCODE, PAB, MGLST)
- ✅ NEX Lookup Service (EAN → produkt)
- ✅ Data sanitization (null bytes)

**Čo chýba (Phase 5):**
- ⚪ Btrieve WRITE operácie
- ⚪ Vytvorenie produktových kariet (GSCAT + BARCODE)
- ⚪ Vytvorenie dodávateľského DL (TSH + TSI)
- ⚪ Požiadavky na zmenu cien (RPC)

---

## 5. NAVRHNUTÝ WORKFLOW PRE v2.0

### 5.1 Kompletný workflow

**FÁZA A: Email → Staging** (✅ HOTOVÉ)

KROKY:
1. Email s PDF príde do magerstavinvoice@gmail.com
2. n8n IMAP trigger zachytí email
3. PDF extrakcia (pdfplumber + regex)
4. ISDOC XML generovanie
5. HTTP POST na FastAPI (cez Cloudflare Tunnel)
6. Uloženie PDF + XML do C:\NEX\IMPORT\
7. Zápis do PostgreSQL staging (invoices + invoice_items)
8. NEX Lookup - pre každú položku nájdi PLU podľa EAN

---

**FÁZA B: GUI Kontrola a príprava** (⚪ NÁVRH)

KROKY:
1. Operátor otvorí GUI (supplier-invoice-editor)
2. Vyberie faktúru zo zoznamu
3. Otvorí detail faktúry s položkami

VIZUÁLNE ROZLÍŠENIE POLOŽIEK:

| Stav | Farba | Význam |
|------|-------|--------|
| PLU > 0, skupina OK | BIELA | Existuje v GSCAT |
| PLU = 0, skupina NONE | ČERVENÁ | Nová, treba priradiť sk. |
| PLU = 0, skupina OK | ORANŽOVÁ | Pripravená na vytvorenie |
| Cena zmenená | ŽLTÁ | Pôjde do RPC |

4. Pre ČERVENÉ položky (PLU = 0):
   - Operátor otvorí zoznam tovarových skupín (MGLST)
   - Vyberie skupinu pre každú novú položku
   - Voliteľne: upraví názov z XML
   - Položka zmení farbu na ORANŽOVÚ

5. Kontrola marže pre každú položku:
   - Nákupná cena (z XML)
   - Aktuálna predajná cena (z PLS)
   - Marža = (predajná - nákupná) / predajná * 100
   - Ak marža < minimum → operátor zmení predajnú cenu
   - Položka s novou cenou → ŽLTÁ (pôjde do RPC)

---

**FÁZA C: Vytvorenie produktových kariet** (⚪ NÁVRH)

PODMIENKA: Všetky nové položky majú priradenú skupinu (ORANŽOVÉ)

KROKY:
1. Operátor klikne "Vytvoriť nové položky"

2. Pre každú položku s PLU = 0:
   - a) Vygeneruj nové PLU: MAX(GSCAT.GsCode) + 1
   - b) Zapíš do GSCAT.BTR:
     * GsCode (PLU)
     * Name (názov z XML alebo upravený)
     * MGLST (tovarová skupina)
     * NakupC (nákupná cena)
     * PredajC (predajná cena)
   - c) Zapíš do BARCODE.BTR:
     * CaRKod (EAN z XML)
     * GS (PLU väzba na GSCAT)

3. Refresh - znovu načítaj údaje z GSCAT pre všetky položky

4. Validácia:
   - Žiadny riadok s PLU = 0 → ✅ OK, pokračuj
   - Ak ešte existuje PLU = 0 → ⚠️ Chyba, riešiť

---

**FÁZA D: Zaevidovanie dodávateľského DL** (⚪ NÁVRH)

PODMIENKA: Všetky položky majú PLU > 0

KROKY:
1. Operátor klikne "Zaevidovať dodací list"

2. Vytvor hlavičku dokladu (TSH):
   - Číslo dokladu (automaticky generované)
   - Dátum vystavenia
   - Dátum dodania
   - Dodávateľ IČO (z XML → PAB)
   - Status: "Pripravený"

3. Vytvor položky dokladu (TSI):
   - Pre každú položku faktúry:
     * Väzba na hlavičku (TSH)
     * PLU (GsCode)
     * Množstvo
     * Nákupná cena
     * Celková cena

4. Pre položky so zmenenou cenou (ŽLTÉ):
   - Zapíš do RPC (Požiadavky na zmeny cien):
     * PLU (GsCode)
     * Nová predajná cena
     * Dátum platnosti

5. Spätná kontrola:
   - Suma položiek TSI = Suma z XML?
   - Počet položiek TSI = Počet z XML?

6. Označenie faktúry ako vybavenú:
   - PostgreSQL staging: status = "completed"

---

**VÝSLEDOK**

✅ Dodávateľský DL v NEX Genesis (status "Pripravený")  
✅ Nové produkty v katalógu (GSCAT + BARCODE)  
✅ Požiadavky na zmenu cien (RPC)  
✅ Faktúra v staging označená ako vybavená  

⏳ Naskladnenie robí operátor v NEX Genesis (MIMO SCOPE v2.0)

---

## 6. BTRIEVE TABUĽKY

### 6.1 Kompletný zoznam pre v2.0

| Tabuľka | Súbor | Účel | Model | READ | WRITE |
|---------|-------|------|-------|------|-------|
| GSCAT | GSCAT.BTR | Katalóg produktov | ✅ | ✅ | ⚪ TODO |
| BARCODE | BARCODE.BTR | EAN kódy | ✅ | ✅ | ⚪ TODO |
| PAB | PAB.BTR | Partneri (dodávatelia) | ✅ | ✅ | — |
| MGLST | MGLST.BTR | Tovarové skupiny | ✅ | ✅ | — |
| TSH | TSHA-001.BTR | Hlavička DL | ⚪ TODO | ⚪ TODO | ⚪ TODO |
| TSI | TSIA-001.BTR | Položky DL | ⚪ TODO | ⚪ TODO | ⚪ TODO |
| PLS | PLSnnnnn.BTR | Predajný cenník | ⚪ TODO | ⚪ TODO | — |
| RPC | RPCnnnnn.BTR | Požiadavky na zmeny cien | ⚪ TODO | ⚪ TODO | ⚪ TODO |

### 6.2 Konfigurácia

```yaml
# Číslo cenníka (rovnaké pre PLS aj RPC)
price_list_number: "00001"  # → PLS00001.BTR, RPC00001.BTR
```

### 6.3 TODO - Modely na vytvorenie

1. **TSH Model** - Hlavička dodacieho listu
   - Číslo dokladu
   - Dátum vystavenia
   - Dátum dodania
   - Dodávateľ (IČO)
   - Status

2. **TSI Model** - Položky dodacieho listu
   - Väzba na TSH
   - PLU (GsCode)
   - Množstvo
   - Cena
   
3. **PLS Model** - Predajný cenník
   - PLU (GsCode)
   - Predajná cena
   
4. **RPC Model** - Požiadavky na zmeny cien
   - PLU (GsCode)
   - Nová predajná cena
   - Dátum platnosti

---

## 7. PostgreSQL STAGING

### 7.1 Databáza

**Názov:** `invoice_staging`  
**Lokácia:** Zákaznícky server  

### 7.2 Tabuľky

**invoices:**
- id
- supplier_ico
- supplier_name
- invoice_number
- invoice_date
- due_date
- total_amount
- status (pending/completed)
- created_at

**invoice_items:**
- id
- invoice_id (FK)
- line_number
- original_name
- original_ean
- original_quantity
- original_price
- edited_name
- edited_price_sell
- nex_plu (GsCode z GSCAT)
- nex_name
- nex_category (MGLST)
- in_nex (boolean)

---

## 8. SCOPE v2.0 SUMARIZÁCIA

### 8.1 GO-LIVE 2025-11-27 (Preview/Demo)

**Čo bude fungovať:**
- ✅ Email → PDF → XML → Staging → GUI zobrazenie
- ✅ NEX Lookup (EAN → produkt)
- ✅ Vizuálne rozlíšenie položiek

**Čo nebude fungovať (post GO-LIVE):**
- ⚪ Vytvorenie produktových kariet
- ⚪ Zaevidovanie dodávateľského DL
- ⚪ Požiadavky na zmenu cien

### 8.2 Post GO-LIVE implementácia

**Poradie:**
1. Modely pre TSH, TSI, PLS, RPC
2. Btrieve WRITE operácie
3. GUI funkcie (tlačidlá, validácie)
4. Testovanie na reálnych dátach

### 8.3 MIMO SCOPE v2.0

- Automatické naskladnenie (kroky 12-21)
- AI automatické priradenie tovarových skupín
- Priamy email od dodávateľa (bez operátora)

---

## 9. TODO ZOZNAM

### 9.1 Infraštruktúra
- [ ] Cloudflare Tunnel ako Windows Service
- [ ] Automatický backup (Task Scheduler)
- [ ] Overiť SMTP konfiguráciu

### 9.2 Btrieve Modely
- [ ] TSH Model (hlavička DL)
- [ ] TSI Model (položky DL)
- [ ] PLS Model (predajný cenník)
- [ ] RPC Model (požiadavky na zmeny cien)

### 9.3 Btrieve WRITE
- [ ] GSCAT zápis (nové produkty)
- [ ] BARCODE zápis (EAN väzby)
- [ ] TSH zápis (hlavička DL)
- [ ] TSI zápis (položky DL)
- [ ] RPC zápis (požiadavky na zmeny cien)

### 9.4 GUI Funkcie
- [ ] Farebné rozlíšenie položiek (PLU = 0)
- [ ] Výber tovarovej skupiny (MGLST lookup)
- [ ] Editácia názvu položky
- [ ] Kontrola a editácia marže
- [ ] Tlačidlo "Vytvoriť nové položky"
- [ ] Tlačidlo "Zaevidovať dodací list"
- [ ] Validácie a spätná kontrola

### 9.5 Konfigurácia
- [ ] Parameter: číslo cenníka (nnnnn)
- [ ] Parameter: minimálna marža (%)

---

## 10. TERMINOLÓGIA

**Kľúčové pojmy pre tento projekt:**
- **GSCAT** - Katalóg produktov (Product Catalog)
- **BARCODE** - Tabuľka EAN kódov
- **MGLST** - Tovarové skupiny (Product Categories)
- **PAB** - Partneri/Dodávatelia (Business Partners)
- **TSH** - Hlavička dodacieho listu (Delivery Note Header)
- **TSI** - Položky dodacieho listu (Delivery Note Items)
- **PLS** - Predajný cenník (Sales Price List)
- **RPC** - Požiadavky na zmeny cien (Price Change Requests)
- **DL** - Dodací list (Delivery Note)
- **PLU** - Product Lookup Unit (GsCode v GSCAT)

---

**See Also:**
- [PROJECT_VISION.md](../strategic/PROJECT_VISION.md) - Current project vision
- [PROJECT_ROADMAP.md](../strategic/PROJECT_ROADMAP.md) - Current roadmap
- [ARCHITECTURE.md](../system/ARCHITECTURE.md) - Current architecture