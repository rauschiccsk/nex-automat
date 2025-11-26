# NEX Automat - Roadmap

**Projekt:** NEX Automat  
**Verzia dokumentu:** 1.0  
**Dátum:** 2025-11-26  

---

## 1. PREHĽAD FÁZ

```
┌─────────────────────────────────────────────────────────────────────────┐
│  FÁZA 1: Email → Staging → GUI Zobrazenie          ✅ COMPLETE         │
├─────────────────────────────────────────────────────────────────────────┤
│  FÁZA 2: GO-LIVE Preview/Demo                      🟡 IN PROGRESS      │
├─────────────────────────────────────────────────────────────────────────┤
│  FÁZA 3: Btrieve Models (TSH, TSI, PLS, RPC)       ⚪ TODO             │
├─────────────────────────────────────────────────────────────────────────┤
│  FÁZA 4: GUI Editácia + Farebné rozlíšenie         ⚪ TODO             │
├─────────────────────────────────────────────────────────────────────────┤
│  FÁZA 5: Vytvorenie produktových kariet            ⚪ TODO             │
├─────────────────────────────────────────────────────────────────────────┤
│  FÁZA 6: Zaevidovanie dodávateľského DL            ⚪ TODO             │
├─────────────────────────────────────────────────────────────────────────┤
│  FÁZA 7: Požiadavky na zmenu cien                  ⚪ TODO             │
├─────────────────────────────────────────────────────────────────────────┤
│  FÁZA 8: Testovanie + Production Hardening         ⚪ TODO             │
├─────────────────────────────────────────────────────────────────────────┤
│  FÁZA 9: Ďalší zákazníci + Rozšírenia              ⚪ FUTURE           │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. DETAILNÝ POPIS FÁZ

### FÁZA 1: Email → Staging → GUI Zobrazenie ✅ COMPLETE

**Cieľ:** Automatické spracovanie faktúr až po zobrazenie v GUI

**Deliverables:**
- [x] n8n workflow (IMAP → PDF → FastAPI)
- [x] PDF extrakcia (pdfplumber + regex)
- [x] ISDOC XML generátor
- [x] FastAPI service
- [x] PostgreSQL staging DB
- [x] NEX Lookup (EAN → PLU)
- [x] GUI zobrazenie faktúr a položiek
- [x] Windows Service deployment
- [x] Cloudflare Tunnel konfigurácia

---

### FÁZA 2: GO-LIVE Preview/Demo 🟡 IN PROGRESS

**Cieľ:** Prezentácia systému zákazníkovi (Mágerstav)

**Deliverables:**
- [x] End-to-end test na reálnych dátach
- [x] Deployment na zákaznícky server
- [ ] Cloudflare Tunnel ako Windows Service
- [ ] Dokumentácia pre operátora
- [ ] Demo session so zákazníkom

**Scope:**
- Operátor uvidí faktúru v GUI
- Bez zápisu do NEX Genesis
- Validácia AI extrakcie

---

### FÁZA 3: Btrieve Models ⚪ TODO

**Cieľ:** Vytvorenie modelov pre zvyšné Btrieve tabuľky

**Deliverables:**
- [ ] TSH Model (hlavička DL)
- [ ] TSI Model (položky DL)
- [ ] PLS Model (predajný cenník)
- [ ] RPC Model (požiadavky na zmeny cien)

**Technické úlohy:**
1. Analyzovať štruktúru TSHA-001.BTR
2. Analyzovať štruktúru TSIA-001.BTR
3. Analyzovať štruktúru PLSnnnnn.BTR
4. Analyzovať štruktúru RPCnnnnn.BTR
5. Vytvoriť Python modely
6. Unit testy pre READ operácie

---

### FÁZA 4: GUI Editácia + Farebné rozlíšenie ⚪ TODO

**Cieľ:** Operátor vie editovať položky a vidí stav

**Deliverables:**
- [ ] Farebné rozlíšenie položiek (PLU = 0)
- [ ] Výber tovarovej skupiny (MGLST lookup)
- [ ] Editácia názvu položky
- [ ] Kontrola marže (nákupná vs predajná)
- [ ] Editácia predajnej ceny
- [ ] Označenie položiek so zmenenou cenou

**UI Farby:**
| Stav | Farba | Význam |
|------|-------|--------|
| PLU > 0 | Biela | Existuje v GSCAT |
| PLU = 0, bez skupiny | Červená | Treba priradiť skupinu |
| PLU = 0, so skupinou | Oranžová | Pripravené na vytvorenie |
| Cena zmenená | Žltá | Pôjde do RPC |

---

### FÁZA 5: Vytvorenie produktových kariet ⚪ TODO

**Cieľ:** Systém vie vytvoriť nové produkty v GSCAT

**Deliverables:**
- [ ] Btrieve WRITE pre GSCAT
- [ ] Automatické generovanie PLU (MAX+1)
- [ ] Btrieve WRITE pre BARCODE
- [ ] Refresh PLU po vytvorení
- [ ] Validácia (žiadny PLU = 0)
- [ ] Error handling a rollback

**Workflow:**
```
1. Operátor priradí skupinu všetkým novým položkám
2. Klikne "Vytvoriť nové položky"
3. Systém vytvorí GSCAT + BARCODE záznamy
4. Systém refreshne PLU
5. Validácia: všetky položky majú PLU > 0
```

---

### FÁZA 6: Zaevidovanie dodávateľského DL ⚪ TODO

**Cieľ:** Systém vie vytvoriť DL v NEX Genesis

**Deliverables:**
- [ ] Btrieve WRITE pre TSH (hlavička)
- [ ] Btrieve WRITE pre TSI (položky)
- [ ] Automatické číslovanie dokladu
- [ ] Väzba na dodávateľa (PAB)
- [ ] Spätná kontrola súm
- [ ] Nastavenie status "Pripravený"

**Workflow:**
```
1. Všetky položky majú PLU > 0
2. Operátor klikne "Zaevidovať DL"
3. Systém vytvorí TSH hlavičku
4. Systém vytvorí TSI položky
5. Spätná kontrola: suma TSI = suma XML
6. Označenie faktúry v staging ako completed
```

---

### FÁZA 7: Požiadavky na zmenu cien ⚪ TODO

**Cieľ:** Systém vie vytvoriť RPC záznamy

**Deliverables:**
- [ ] Btrieve READ pre PLS (aktuálne ceny)
- [ ] Btrieve WRITE pre RPC
- [ ] Automatické vytvorenie pri ukladaní DL
- [ ] Väzba na PLU produktu

**Workflow:**
```
1. Operátor zmení predajnú cenu (položka → žltá)
2. Pri ukladaní DL systém identifikuje žlté položky
3. Pre každú žltú položku vytvorí RPC záznam
4. RPC obsahuje: PLU, nová cena, dátum
```

---

### FÁZA 8: Testovanie + Production Hardening ⚪ TODO

**Cieľ:** Stabilný, produkčne pripravený systém

**Deliverables:**
- [ ] End-to-end testy celého workflow
- [ ] Stress testing (veľké faktúry)
- [ ] Error recovery testy
- [ ] Automatický backup (Task Scheduler)
- [ ] SMTP notifikácie overenie
- [ ] Monitoring a alerting
- [ ] Dokumentácia pre operátora
- [ ] Troubleshooting guide

---

### FÁZA 9: Ďalší zákazníci + Rozšírenia ⚪ FUTURE

**Cieľ:** Škálovanie a vylepšenia

**Deliverables:**
- [ ] Onboarding ANDROS
- [ ] Onboarding ďalších zákazníkov
- [ ] Extractory pre ďalších dodávateľov
- [ ] AI validácia extrakcie
- [ ] AI automatické priradenie skupín
- [ ] Priamy email bez operátora
- [ ] Dashboard a reporting

---

## 3. ZÁVISLOSTI MEDZI FÁZAMI

```
FÁZA 1 ──→ FÁZA 2 ──→ FÁZA 3 ──┬──→ FÁZA 4 ──→ FÁZA 5 ──┬──→ FÁZA 6 ──→ FÁZA 7
                               │                        │
                               │                        │
                               └────────────────────────┘
                                    (paralelne možné)

FÁZA 8 závisí na: FÁZA 5, 6, 7 (kompletný workflow)
FÁZA 9 závisí na: FÁZA 8 (stabilný systém)
```

---

## 4. RIZIKÁ A MITIGÁCIE

| Riziko | Dopad | Mitigácia |
|--------|-------|-----------|
| Btrieve WRITE zlyhá | Vysoký | Postupné testovanie, rollback mechanizmus |
| Neznáma štruktúra TSH/TSI | Stredný | Analýza existujúcich dokladov v NEX Genesis |
| Výkon pri veľkých faktúrach | Stredný | Batch processing, async operácie |
| Zákazník neschváli workflow | Vysoký | Iteratívne demo, úpravy podľa feedback |

---

## 5. TECHNICKÉ DLHY

| Položka | Popis | Priorita |
|---------|-------|----------|
| Cloudflare Tunnel Service | Nie je ako Windows Service | Vysoká |
| SMTP konfigurácia | Neoverené | Stredná |
| Automatický backup | Neexistuje | Stredná |
| Test coverage editor | Nízke | Nízka |

---

## 6. BUDÚCE ROZŠÍRENIA (Backlog)

### 6.1 AI Vylepšenia
- AI validácia extrakcie (Claude API)
- AI automatické priradenie tovarových skupín
- AI fallback pri zlyhaní regex extrakcie

### 6.2 Automatizácia
- Priamy email od dodávateľa (bez operátora)
- Automatické naskladnenie (integrácia s NEX Genesis)
- Scheduled processing (batch mód)

### 6.3 Multi-tenant
- Dashboard pre všetkých zákazníkov
- Centralizované reporting
- Customer self-service portal

### 6.4 Ďalšie moduly
- Customer Order Processing
- Inventory Management
- Financial Reporting

---

## 7. MILESTONE CHECKLIST

### Milestone 1: GO-LIVE Preview ✅
- [x] Email → Staging funguje
- [x] GUI zobrazuje faktúry
- [ ] Demo zákazníkovi

### Milestone 2: Produktové karty
- [ ] GSCAT WRITE funguje
- [ ] BARCODE WRITE funguje
- [ ] Operátor vie vytvoriť nové produkty

### Milestone 3: Dodací list
- [ ] TSH WRITE funguje
- [ ] TSI WRITE funguje
- [ ] Operátor vie zaevidovať DL

### Milestone 4: Zmeny cien
- [ ] PLS READ funguje
- [ ] RPC WRITE funguje
- [ ] Automatické vytvorenie RPC

### Milestone 5: Production Ready
- [ ] Kompletný workflow testovaný
- [ ] Error handling kompletný
- [ ] Dokumentácia kompletná
- [ ] Zákazník používa denne

---

**Dokument vytvorený:** 2025-11-26  
**Autor:** Claude AI + Zoltán Rausch