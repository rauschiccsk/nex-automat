# NEX Automat - Roadmap

**Projekt:** NEX Automat  
**Verzia dokumentu:** 1.0  
**Dátum:** 2025-11-26  

---

## 1. PREHĽAD FÁZ

| Fáza | Názov | Status |
|------|-------|--------|
| 1 | Email → Staging → GUI Zobrazenie | ✅ COMPLETE |
| 2 | GO-LIVE Preview/Demo | 🟡 IN PROGRESS |
| 3 | Btrieve Models (TSH, TSI, PLS, RPC) | ⚪ TODO |
| 4 | GUI Editácia + Farebné rozlíšenie | ⚪ TODO |
| 5 | Vytvorenie produktových kariet | ⚪ TODO |
| 6 | Zaevidovanie dodávateľského DL | ⚪ TODO |
| 7 | Požiadavky na zmenu cien | ⚪ TODO |
| 8 | Testovanie + Production Hardening | ⚪ TODO |
| 9 | Ďalší zákazníci + Rozšírenia | ⚪ FUTURE |

---

## 2. DETAILNÝ POPIS FÁZ

### FÁZA 1: Email → Staging → GUI Zobrazenie ✅ COMPLETE

**Cieľ:** Automatické spracovanie faktúr až po zobrazenie v GUI

**Deliverables:**

| Úloha | Status |
|-------|--------|
| n8n workflow (IMAP → PDF → FastAPI) | ✅ |
| PDF extrakcia (pdfplumber + regex) | ✅ |
| ISDOC XML generátor | ✅ |
| FastAPI service | ✅ |
| PostgreSQL staging DB | ✅ |
| NEX Lookup (EAN → PLU) | ✅ |
| GUI zobrazenie faktúr a položiek | ✅ |
| Windows Service deployment | ✅ |
| Cloudflare Tunnel konfigurácia | ✅ |

---

### FÁZA 2: GO-LIVE Preview/Demo 🟡 IN PROGRESS

**Cieľ:** Prezentácia systému zákazníkovi (Mágerstav)

**Deliverables:**

| Úloha | Status |
|-------|--------|
| End-to-end test na reálnych dátach | ✅ |
| Deployment na zákaznícky server | ✅ |
| Cloudflare Tunnel ako Windows Service | ⚪ TODO |
| Dokumentácia pre operátora | ⚪ TODO |
| Demo session so zákazníkom | ⚪ TODO |

**Scope:**
- Operátor uvidí faktúru v GUI
- Bez zápisu do NEX Genesis
- Validácia AI extrakcie

---

### FÁZA 3: Btrieve Models ⚪ TODO

**Cieľ:** Vytvorenie modelov pre zvyšné Btrieve tabuľky

**Deliverables:**

| Úloha | Status |
|-------|--------|
| TSH Model (hlavička DL) | ⚪ TODO |
| TSI Model (položky DL) | ⚪ TODO |
| PLS Model (predajný cenník) | ⚪ TODO |
| RPC Model (požiadavky na zmeny cien) | ⚪ TODO |

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

| Úloha | Status |
|-------|--------|
| Farebné rozlíšenie položiek (PLU = 0) | ⚪ TODO |
| Výber tovarovej skupiny (MGLST lookup) | ⚪ TODO |
| Editácia názvu položky | ⚪ TODO |
| Kontrola marže (nákupná vs predajná) | ⚪ TODO |
| Editácia predajnej ceny | ⚪ TODO |
| Označenie položiek so zmenenou cenou | ⚪ TODO |

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

| Úloha | Status |
|-------|--------|
| Btrieve WRITE pre GSCAT | ⚪ TODO |
| Automatické generovanie PLU (MAX+1) | ⚪ TODO |
| Btrieve WRITE pre BARCODE | ⚪ TODO |
| Refresh PLU po vytvorení | ⚪ TODO |
| Validácia (žiadny PLU = 0) | ⚪ TODO |
| Error handling a rollback | ⚪ TODO |

**Workflow:**
1. Operátor priradí skupinu všetkým novým položkám
2. Klikne "Vytvoriť nové položky"
3. Systém vytvorí GSCAT + BARCODE záznamy
4. Systém refreshne PLU
5. Validácia: všetky položky majú PLU > 0

---

### FÁZA 6: Zaevidovanie dodávateľského DL ⚪ TODO

**Cieľ:** Systém vie vytvoriť DL v NEX Genesis

**Deliverables:**

| Úloha | Status |
|-------|--------|
| Btrieve WRITE pre TSH (hlavička) | ⚪ TODO |
| Btrieve WRITE pre TSI (položky) | ⚪ TODO |
| Automatické číslovanie dokladu | ⚪ TODO |
| Väzba na dodávateľa (PAB) | ⚪ TODO |
| Spätná kontrola súm | ⚪ TODO |
| Nastavenie status "Pripravený" | ⚪ TODO |

**Workflow:**
1. Všetky položky majú PLU > 0
2. Operátor klikne "Zaevidovať DL"
3. Systém vytvorí TSH hlavičku
4. Systém vytvorí TSI položky
5. Spätná kontrola: suma TSI = suma XML
6. Označenie faktúry v staging ako completed

---

### FÁZA 7: Požiadavky na zmenu cien ⚪ TODO

**Cieľ:** Systém vie vytvoriť RPC záznamy

**Deliverables:**

| Úloha | Status |
|-------|--------|
| Btrieve READ pre PLS (aktuálne ceny) | ⚪ TODO |
| Btrieve WRITE pre RPC | ⚪ TODO |
| Automatické vytvorenie pri ukladaní DL | ⚪ TODO |
| Väzba na PLU produktu | ⚪ TODO |

**Workflow:**
1. Operátor zmení predajnú cenu (položka → žltá)
2. Pri ukladaní DL systém identifikuje žlté položky
3. Pre každú žltú položku vytvorí RPC záznam
4. RPC obsahuje: PLU, nová cena, dátum

---

### FÁZA 8: Testovanie + Production Hardening ⚪ TODO

**Cieľ:** Stabilný, produkčne pripravený systém

**Deliverables:**

| Úloha | Status |
|-------|--------|
| End-to-end testy celého workflow | ⚪ TODO |
| Stress testing (veľké faktúry) | ⚪ TODO |
| Error recovery testy | ⚪ TODO |
| Automatický backup (Task Scheduler) | ⚪ TODO |
| SMTP notifikácie overenie | ⚪ TODO |
| Monitoring a alerting | ⚪ TODO |
| Dokumentácia pre operátora | ⚪ TODO |
| Troubleshooting guide | ⚪ TODO |

---

### FÁZA 9: Ďalší zákazníci + Rozšírenia ⚪ FUTURE

**Cieľ:** Škálovanie a vylepšenia

**Deliverables:**

| Úloha | Status |
|-------|--------|
| Onboarding ANDROS | ⚪ FUTURE |
| Onboarding ďalších zákazníkov | ⚪ FUTURE |
| Extractory pre ďalších dodávateľov | ⚪ FUTURE |
| AI validácia extrakcie | ⚪ FUTURE |
| AI automatické priradenie skupín | ⚪ FUTURE |
| Priamy email bez operátora | ⚪ FUTURE |
| Dashboard a reporting | ⚪ FUTURE |

---

## 3. ZÁVISLOSTI MEDZI FÁZAMI

| Fáza | Závisí na |
|------|-----------|
| 1 | — |
| 2 | 1 |
| 3 | 2 |
| 4 | 3 |
| 5 | 4 |
| 6 | 5 |
| 7 | 6 |
| 8 | 5, 6, 7 |
| 9 | 8 |

**Poznámka:** Fázy 4-7 môžu byť čiastočne paralelné.

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

| Funkcia | Popis |
|---------|-------|
| AI validácia extrakcie | Claude API kontrola regex výstupu |
| AI priradenie skupín | Automatické na základe názvu |
| AI fallback | Pri zlyhaní regex použiť AI |

### 6.2 Automatizácia

| Funkcia | Popis |
|---------|-------|
| Priamy email | Bez operátora v strede |
| Auto-naskladnenie | Integrácia s NEX Genesis |
| Scheduled processing | Batch mód |

### 6.3 Multi-tenant

| Funkcia | Popis |
|---------|-------|
| Dashboard | Pre všetkých zákazníkov |
| Reporting | Centralizované štatistiky |
| Self-service | Customer portal |

### 6.4 Ďalšie moduly

| Modul | Popis |
|-------|-------|
| Customer Orders | Spracovanie zákazníckych objednávok |
| Inventory | Správa zásob |
| Financial | Reporting |

---

## 7. MILESTONE CHECKLIST

### Milestone 1: GO-LIVE Preview

| Úloha | Status |
|-------|--------|
| Email → Staging funguje | ✅ |
| GUI zobrazuje faktúry | ✅ |
| Demo zákazníkovi | ⚪ TODO |

### Milestone 2: Produktové karty

| Úloha | Status |
|-------|--------|
| GSCAT WRITE funguje | ⚪ TODO |
| BARCODE WRITE funguje | ⚪ TODO |
| Operátor vie vytvoriť nové produkty | ⚪ TODO |

### Milestone 3: Dodací list

| Úloha | Status |
|-------|--------|
| TSH WRITE funguje | ⚪ TODO |
| TSI WRITE funguje | ⚪ TODO |
| Operátor vie zaevidovať DL | ⚪ TODO |

### Milestone 4: Zmeny cien

| Úloha | Status |
|-------|--------|
| PLS READ funguje | ⚪ TODO |
| RPC WRITE funguje | ⚪ TODO |
| Automatické vytvorenie RPC | ⚪ TODO |

### Milestone 5: Production Ready

| Úloha | Status |
|-------|--------|
| Kompletný workflow testovaný | ⚪ TODO |
| Error handling kompletný | ⚪ TODO |
| Dokumentácia kompletná | ⚪ TODO |
| Zákazník používa denne | ⚪ TODO |

---

**Dokument vytvorený:** 2025-11-26  
**Autor:** Claude AI + Zoltán Rausch