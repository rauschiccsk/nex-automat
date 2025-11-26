# NEX Automat - Požiadavky

**Projekt:** NEX Automat  
**Verzia dokumentu:** 1.0  
**Dátum:** 2025-11-26  

---

## 1. FUNKCIONÁLNE POŽIADAVKY

### 1.1 Email Processing (✅ IMPLEMENTOVANÉ)

| ID | Požiadavka | Status |
|----|------------|--------|
| REQ-EMAIL-01 | Systém monitoruje dedikovanú emailovú schránku | ✅ |
| REQ-EMAIL-02 | Systém extrahuje PDF prílohy z emailov | ✅ |
| REQ-EMAIL-03 | Systém podporuje viacero PDF v jednom emaili | ✅ |
| REQ-EMAIL-04 | Systém notifikuje pri chýbajúcej PDF prílohe | ✅ |
| REQ-EMAIL-05 | Systém ukladá email metadáta (from, subject, date) | ✅ |

### 1.2 PDF Extrakcia (✅ IMPLEMENTOVANÉ)

| ID | Požiadavka | Status |
|----|------------|--------|
| REQ-PDF-01 | Systém extrahuje dáta z PDF faktúr L&Š | ✅ |
| REQ-PDF-02 | Extrakcia hlavičky: číslo, dátum, splatnosť | ✅ |
| REQ-PDF-03 | Extrakcia dodávateľa: názov, IČO, DIČ, IČ DPH | ✅ |
| REQ-PDF-04 | Extrakcia odberateľa: názov, IČO, DIČ, IČ DPH | ✅ |
| REQ-PDF-05 | Extrakcia položiek: EAN, názov, množstvo, cena | ✅ |
| REQ-PDF-06 | Extrakcia súm: základ, DPH, celkom | ✅ |
| REQ-PDF-07 | Extrakcia bankových údajov: IBAN, VS | ✅ |
| REQ-PDF-08 | Generovanie ISDOC 6.0.1 XML | ✅ |

### 1.3 Staging Database (✅ IMPLEMENTOVANÉ)

| ID | Požiadavka | Status |
|----|------------|--------|
| REQ-DB-01 | Uloženie hlavičky faktúry do PostgreSQL | ✅ |
| REQ-DB-02 | Uloženie položiek faktúry do PostgreSQL | ✅ |
| REQ-DB-03 | Detekcia duplicít (rovnaké číslo faktúry) | ✅ |
| REQ-DB-04 | Status tracking (pending/completed) | ✅ |

### 1.4 NEX Lookup (✅ IMPLEMENTOVANÉ)

| ID | Požiadavka | Status |
|----|------------|--------|
| REQ-LOOKUP-01 | Vyhľadanie produktu podľa EAN v GSCAT | ✅ |
| REQ-LOOKUP-02 | Získanie PLU (GsCode) pre existujúci produkt | ✅ |
| REQ-LOOKUP-03 | Označenie položiek bez PLU (in_nex = false) | ✅ |
| REQ-LOOKUP-04 | Data sanitization (null bytes z Btrieve) | ✅ |

### 1.5 GUI - Zobrazenie (✅ IMPLEMENTOVANÉ)

| ID | Požiadavka | Status |
|----|------------|--------|
| REQ-GUI-01 | Zobrazenie zoznamu nevybavených faktúr | ✅ |
| REQ-GUI-02 | Zobrazenie detailu faktúry | ✅ |
| REQ-GUI-03 | Zobrazenie položiek faktúry v gridu | ✅ |
| REQ-GUI-04 | Zobrazenie NEX údajov (PLU, názov, skupina) | ✅ |

### 1.6 GUI - Editácia (⚪ NÁVRH)

| ID | Požiadavka | Status |
|----|------------|--------|
| REQ-EDIT-01 | Farebné rozlíšenie položiek podľa PLU | ⚪ |
| REQ-EDIT-02 | Editácia názvu položky | ⚪ |
| REQ-EDIT-03 | Výber tovarovej skupiny z MGLST | ⚪ |
| REQ-EDIT-04 | Editácia predajnej ceny | ⚪ |
| REQ-EDIT-05 | Automatický výpočet marže | ⚪ |
| REQ-EDIT-06 | Označenie položiek so zmenenou cenou | ⚪ |

### 1.7 Vytvorenie produktových kariet (⚪ NÁVRH)

| ID | Požiadavka | Status |
|----|------------|--------|
| REQ-GSCAT-01 | Vytvorenie novej karty v GSCAT.BTR | ⚪ |
| REQ-GSCAT-02 | Automatické generovanie PLU (MAX+1) | ⚪ |
| REQ-GSCAT-03 | Nastavenie tovarovej skupiny (MGLST) | ⚪ |
| REQ-GSCAT-04 | Nastavenie nákupnej a predajnej ceny | ⚪ |
| REQ-GSCAT-05 | Vytvorenie záznamu v BARCODE.BTR | ⚪ |
| REQ-GSCAT-06 | Refresh PLU po vytvorení | ⚪ |

### 1.8 Zaevidovanie dodávateľského DL (⚪ NÁVRH)

| ID | Požiadavka | Status |
|----|------------|--------|
| REQ-DL-01 | Vytvorenie hlavičky DL v TSH | ⚪ |
| REQ-DL-02 | Automatické číslovanie dokladu | ⚪ |
| REQ-DL-03 | Nastavenie dodávateľa z PAB | ⚪ |
| REQ-DL-04 | Vytvorenie položiek DL v TSI | ⚪ |
| REQ-DL-05 | Väzba položiek na PLU | ⚪ |
| REQ-DL-06 | Nastavenie status "Pripravený" | ⚪ |
| REQ-DL-07 | Spätná kontrola súm | ⚪ |

### 1.9 Požiadavky na zmenu cien (⚪ NÁVRH)

| ID | Požiadavka | Status |
|----|------------|--------|
| REQ-RPC-01 | Vytvorenie záznamu v RPC pre zmenenú cenu | ⚪ |
| REQ-RPC-02 | Väzba na PLU produktu | ⚪ |
| REQ-RPC-03 | Nastavenie novej predajnej ceny | ⚪ |
| REQ-RPC-04 | Automatické vytvorenie pri ukladaní DL | ⚪ |

---

## 2. NEFUNKCIONÁLNE POŽIADAVKY

### 2.1 Výkon

| ID | Požiadavka | Hodnota |
|----|------------|---------|
| NFR-PERF-01 | Doba spracovania PDF | < 5 sekúnd |
| NFR-PERF-02 | Doba NEX Lookup pre 100 položiek | < 10 sekúnd |
| NFR-PERF-03 | Doba zápisu do Btrieve | < 3 sekundy |
| NFR-PERF-04 | GUI response time | < 1 sekunda |

### 2.2 Spoľahlivosť

| ID | Požiadavka | Hodnota |
|----|------------|---------|
| NFR-REL-01 | Úspešnosť extrakcie L&Š | 100% |
| NFR-REL-02 | Dostupnosť FastAPI | 99.9% |
| NFR-REL-03 | Dátová integrita | 0% strát |
| NFR-REL-04 | Recovery po výpadku | < 5 minút |

### 2.3 Bezpečnosť

| ID | Požiadavka |
|----|------------|
| NFR-SEC-01 | API autentifikácia pomocou API key |
| NFR-SEC-02 | HTTPS komunikácia (Cloudflare Tunnel) |
| NFR-SEC-03 | Dáta uložené lokálne u zákazníka |
| NFR-SEC-04 | Audit log všetkých operácií |

### 2.4 Údržba

| ID | Požiadavka |
|----|------------|
| NFR-MAINT-01 | Windows Service deployment |
| NFR-MAINT-02 | Konfigurácia cez YAML súbory |
| NFR-MAINT-03 | Centralizované logovanie |
| NFR-MAINT-04 | Prometheus metrics endpoint |

---

## 3. WORKFLOW POŽIADAVKY

### 3.1 Kompletný workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│  FÁZA A: Email → Staging                                                │
│                                                                         │
│  VSTUP: Email s PDF faktúrou                                           │
│                                                                         │
│  KROKY:                                                                 │
│  1. [REQ-EMAIL-01] Trigger na novom emaili                             │
│  2. [REQ-EMAIL-02] Extrakcia PDF prílohy                               │
│  3. [REQ-PDF-01..08] Extrakcia dát a generovanie XML                   │
│  4. [REQ-DB-01..04] Uloženie do PostgreSQL                             │
│  5. [REQ-LOOKUP-01..04] NEX Lookup pre položky                         │
│                                                                         │
│  VÝSTUP: Faktúra v staging DB s NEX údajmi                             │
│                                                                         │
│  STATUS: ✅ IMPLEMENTOVANÉ                                              │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  FÁZA B: GUI Kontrola a príprava                                        │
│                                                                         │
│  VSTUP: Faktúra v staging DB                                           │
│                                                                         │
│  KROKY:                                                                 │
│  1. [REQ-GUI-01..04] Zobrazenie faktúry a položiek                     │
│  2. [REQ-EDIT-01] Farebné rozlíšenie:                                  │
│     - BIELA: PLU > 0 (existuje v GSCAT)                                │
│     - ČERVENÁ: PLU = 0, skupina nepriradená                            │
│     - ORANŽOVÁ: PLU = 0, skupina priradená                             │
│     - ŽLTÁ: cena zmenená (pôjde do RPC)                                │
│  3. [REQ-EDIT-02..03] Pre ČERVENÉ: priradiť skupinu, upraviť názov     │
│  4. [REQ-EDIT-04..06] Kontrola marže, úprava predajnej ceny            │
│                                                                         │
│  VÝSTUP: Všetky položky pripravené (ORANŽOVÉ alebo BIELE/ŽLTÉ)         │
│                                                                         │
│  STATUS: ⚪ NÁVRH                                                       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  FÁZA C: Vytvorenie produktových kariet                                 │
│                                                                         │
│  VSTUP: ORANŽOVÉ položky (PLU = 0, skupina priradená)                  │
│                                                                         │
│  PODMIENKA: Všetky nové položky majú skupinu                           │
│                                                                         │
│  KROKY:                                                                 │
│  1. [REQ-GSCAT-01..04] Vytvorenie GSCAT záznamov                       │
│  2. [REQ-GSCAT-05] Vytvorenie BARCODE záznamov                         │
│  3. [REQ-GSCAT-06] Refresh PLU z GSCAT                                 │
│                                                                         │
│  VALIDÁCIA: Žiadna položka s PLU = 0                                   │
│                                                                         │
│  VÝSTUP: Všetky položky majú PLU > 0                                   │
│                                                                         │
│  STATUS: ⚪ NÁVRH                                                       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  FÁZA D: Zaevidovanie dodávateľského DL                                 │
│                                                                         │
│  VSTUP: Faktúra so všetkými PLU > 0                                    │
│                                                                         │
│  PODMIENKA: Všetky položky majú PLU                                    │
│                                                                         │
│  KROKY:                                                                 │
│  1. [REQ-DL-01..03] Vytvorenie hlavičky TSH                            │
│  2. [REQ-DL-04..05] Vytvorenie položiek TSI                            │
│  3. [REQ-RPC-01..04] Pre ŽLTÉ: vytvorenie RPC záznamov                 │
│  4. [REQ-DL-06] Nastavenie status "Pripravený"                         │
│  5. [REQ-DL-07] Spätná kontrola súm                                    │
│  6. Označenie faktúry ako vybavenej (staging)                          │
│                                                                         │
│  VÝSTUP: DL v NEX Genesis, faktúra completed                           │
│                                                                         │
│  STATUS: ⚪ NÁVRH                                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. BTRIEVE POŽIADAVKY

### 4.1 Tabuľky - READ

| Tabuľka | Model | Status |
|---------|-------|--------|
| GSCAT.BTR | ✅ | ✅ Implementované |
| BARCODE.BTR | ✅ | ✅ Implementované |
| PAB.BTR | ✅ | ✅ Implementované |
| MGLST.BTR | ✅ | ✅ Implementované |
| PLSnnnnn.BTR | ⚪ | ⚪ TODO |

### 4.2 Tabuľky - WRITE

| Tabuľka | Model | Status |
|---------|-------|--------|
| GSCAT.BTR | ✅ | ⚪ TODO |
| BARCODE.BTR | ✅ | ⚪ TODO |
| TSHA-001.BTR | ⚪ | ⚪ TODO |
| TSIA-001.BTR | ⚪ | ⚪ TODO |
| RPCnnnnn.BTR | ⚪ | ⚪ TODO |

### 4.3 Modely na vytvorenie

**TSH (Hlavička DL):**
- Číslo dokladu (auto)
- Dátum vystavenia
- Dátum dodania
- Dodávateľ IČO
- Status

**TSI (Položky DL):**
- Väzba na TSH
- PLU (GsCode)
- Množstvo
- Nákupná cena
- Celková cena

**PLS (Predajný cenník):**
- PLU (GsCode)
- Predajná cena
- Dátum platnosti

**RPC (Požiadavky na zmeny cien):**
- PLU (GsCode)
- Nová predajná cena
- Dátum platnosti

---

## 5. KONFIGURAČNÉ POŽIADAVKY

### 5.1 Systémové parametre

| Parameter | Popis | Príklad |
|-----------|-------|---------|
| price_list_number | Číslo cenníka (PLS, RPC) | "00001" |
| min_margin_percent | Minimálna marža (%) | 15.0 |
| data_path | Cesta k Btrieve | "C:\\NEX\\DATA" |

### 5.2 Zákaznícke parametre

| Parameter | Popis | Príklad |
|-----------|-------|---------|
| customer_name | Názov zákazníka | "Mágerstav" |
| customer_code | Kód zákazníka | "MAGERSTAV" |
| email_address | Dedikovaná schránka | "magerstavinvoice@gmail.com" |

---

## 6. AKCEPTAČNÉ KRITÉRIÁ

### 6.1 GO-LIVE (Preview/Demo)

- [ ] Email → PDF → XML → Staging funguje end-to-end
- [ ] NEX Lookup správne identifikuje produkty
- [ ] GUI zobrazuje faktúry a položky
- [ ] Farebné rozlíšenie položiek funguje
- [ ] Operátor vie faktúru otvoriť a prezerať

### 6.2 Post GO-LIVE (Plná funkcionalita)

- [ ] Vytvorenie produktových kariet (GSCAT + BARCODE)
- [ ] Zaevidovanie dodávateľského DL (TSH + TSI)
- [ ] Požiadavky na zmeny cien (RPC)
- [ ] Spätná kontrola súm
- [ ] Označenie faktúry ako vybavenej

---

**Dokument vytvorený:** 2025-11-26  
**Autor:** Claude AI + Zoltán Rausch