# Vízia Projektu - NEX Automat

**Vytvorené:** 2025-11-26  
**Aktualizované:** 2025-12-13  
**Status:** 📈 Living document  
**Verzia:** 2.0

---

## Účel Dokumentu

Tento dokument definuje víziu, stratégiu a dlhodobé ciele projektu NEX Automat. Odpoveď na otázky: Prečo projekt existuje? Aký problém rieši? Kam smerujeme?

---

## Súvisiace Dokumenty

- [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md) - Detailný plán fáz
- [TECHNOLOGY_DECISIONS.md](TECHNOLOGY_DECISIONS.md) - Technologické rozhodnutia
- [APPLICATIONS_INDEX.md](../applications/APPLICATIONS_INDEX.md) - Aplikácie
- [DATABASE_INDEX.md](../database/DATABASE_INDEX.md) - Databázová dokumentácia

---

## 1. VÍZIA

**NEX Automat = Kompletná automatizácia podnikových procesov**

Cieľom projektu je nahradiť manuálne, chybové a časovo náročné procesy automatizovanými riešeniami pre zákazníkov používajúcich NEX Genesis ERP.

### 1.1 Kľúčové Princípy

- **Automatizácia** - nahradiť ľudskú prácu strojmi kde je to možné
- **Transparentnosť** - každý krok je logovateľný a sledovateľný
- **Spoľahlivosť** - konzistentné výsledky, minimálna chybovosť
- **Evolúcia** - postupný prechod z manuálnych na automatizované procesy
- **Integrácia** - plynulá integrácia s NEX Genesis ERP

---

## 2. PROBLÉM KTORÝ RIEŠIME

### 2.1 Súčasný Stav (Manuálne Procesy)

**Typický workflow dodávateľskej faktúry:**

1. Email s PDF príde do schránky
2. Operátor otvorí PDF
3. Manuálne prepíše údaje do NEX Genesis:
   - Hlavička faktúry (dodávateľ, dátumy, sumy)
   - Každú položku (EAN, názov, množstvo, cena)
4. Identifikuje produkt podľa EAN v katalógu
5. Ak produkt neexistuje, vytvorí novú kartu
6. Kontroluje marže
7. Zaeviduje dodací list

**Čas:** 10-30 minút na faktúru  
**Chybovosť:** 5-10%

### 2.2 Typické Chyby

| Typ chyby | Príklad | Dopad |
|-----------|---------|-------|
| Preklep | 8594002536213 → 8594002536**2**13 | Nesprávny produkt |
| Zámena | Podobné produkty | Skladová nezhoda |
| Výpočet | Nesprávna marža | Strata zisku |
| Vynechanie | Zabudnutá položka | Neúplný doklad |
| Duplicita | 2x zaevidovaná faktúra | Finančná chyba |

### 2.3 Dôsledky

- ⏱️ **Časová náročnosť** - hodiny denne na faktúry
- 💰 **Chybovosť** - opravy, reklamácie, finančné straty
- 😓 **Frustrácia** - monotónna, repetitívna práca
- 📉 **Škálovateľnosť** - nemožnosť zvýšiť objem

---

## 3. RIEŠENIE

### 3.1 Automatizácia Workflow

Nahradenie manuálnych krokov automatizovanými:

| Krok | Manuálne | Automatizované | Úspora času |
|------|----------|----------------|-------------|
| 1. Príjem | Otvoriť email | IMAP trigger (n8n) | 100% |
| 2. Extrakcia | Čítať PDF | AI/Regex extrakcia | 90% |
| 3. Validácia | Kontrola údajov | Automatická validácia | 80% |
| 4. Identifikácia | Hľadať EAN v katalógu | NEX Lookup (EAN → PLU) | 95% |
| 5. Staging | Prepisovať do systému | XML → PostgreSQL | 100% |
| 6. Kontrola | Manuálna kontrola | GUI zobrazenie + farebné označenie | 50% |
| 7. Evidencia | Zápis do NEX Genesis | Btrieve write (semi-auto) | 70% |

**Celková úspora času:** ~80%  
**Celková úspora chýb:** ~90%

### 3.2 Overený, Dôveryhodný Proces

**Princípy:**

- ✅ **Konzistentnosť** - rovnaký vstup = rovnaký výstup
- ✅ **Transparentnosť** - každý krok je logovateľný
- ✅ **Kontrola** - operátor validuje pred finálnym zápisom
- ✅ **Audit trail** - história všetkých zmien
- ✅ **Rollback** - možnosť vrátiť zmeny pri chybe

---

## 4. STRATÉGIA IMPLEMENTÁCIE

### 4.1 Postupná Cesta

```
Manuálne procesy → Čiastočná automatizácia → Úplná automatizácia
```

**Fáza 1 (v2.0-v2.4) ✅ COMPLETE:** Human-in-the-loop
- Automatické spracovanie až po GUI
- Operátor kontroluje a schvaľuje
- Systém zapisuje do NEX Genesis
- **Status:** Deployed @ Mágerstav

**Fáza 2 (v3.0) 🟡 IN PROGRESS:** Enhanced UI & Validation
- Nová PySide6 aplikácia (supplier-invoice-staging)
- Lepšia vizualizácia a editácia
- Vytvorenie produktových kariet
- Zaevidovanie dodávateľských DL

**Fáza 3 (budúcnosť) ⚪ PLANNED:** AI Validation
- AI validácia nahrádza časť operátora
- Automatické priradenie tovarových skupín
- Inteligentné návrhy riešení

**Fáza 4 (budúcnosť) ⚪ VISION:** Plná automatizácia
- Priamy email od dodávateľa
- Automatické naskladnenie
- Zero-touch processing

### 4.2 Prečo Postupne?

**1. Dôvera zákazníka**
- Musí vidieť, že systém funguje správne
- Postupné zvykanie na automatizáciu
- Možnosť kedykoľvek zasiahnuť

**2. Učenie systému**
- Zbieranie dát pre AI zlepšovanie
- Identifikácia edge cases
- Optimalizácia procesov

**3. Minimalizácia rizika**
- Chyby zachytí operátor
- Postupné testovanie na reálnych dátach
- Nie big bang deployment

---

## 5. HODNOTA PRE ZÁKAZNÍKA

### 5.1 Kvantifikovateľné Prínosy

| Metrika | Pred | Po | Zlepšenie |
|---------|------|----|-----------|
| Čas na faktúru | 10-30 min | 1-2 min | **80-90% ↓** |
| Chybovosť | 5-10% | <1% | **90% ↓** |
| Denne spracovaných | 10-20 | 50-100+ | **300% ↑** |
| Stres operátora | Vysoký | Nízky | **Dramaticky ↓** |

### 5.2 Úspora FTE (Full-Time Equivalent)

**Výpočet pre Mágerstav:**
- Predtým: ~15 min/faktúra × 50 faktúr/deň = **12.5 hodín/deň**
- Teraz: ~2 min/faktúra × 50 faktúr/deň = **1.7 hodín/deň**
- **Úspora: 10.8 hodín/deň = 1.35 FTE**

**Projekcia pre väčších zákazníkov:**
- 200+ faktúr denne = **2-3 FTE úspora**
- ROI: 6-12 mesiacov

### 5.3 Kvalitatívne Prínosy

- ✅ **Eliminácia ľudských chýb** - konzistentné výsledky
- ✅ **Rýchlejšie naskladnenie** - tovar skôr k dispozícii
- ✅ **Lepšia kontrola marží** - automatické výpočty
- ✅ **Audit trail** - kompletná história zmien
- ✅ **Skalovateľnosť** - ľahké zvýšenie objemu
- ✅ **Spokojnosť zamestnancov** - menej monotónnej práce

---

## 6. CIEĽOVÉ SKUPINY

### 6.1 Pilotní Zákazníci

| Zákazník | Typ | Objem faktúr/mesiac | Status |
|----------|-----|---------------------|--------|
| Mágerstav s.r.o. | Stavebný materiál | ~1000 | ✅ PRODUCTION |
| ANDROS | TBD | TBD | ⚪ Plánovaný Q3 2026 |
| ICC Komárno | Interný | ~500 | ⚪ Plánovaný Q4 2026 |

### 6.2 Ideálny Zákazník - Profil

**Technické kritériá:**
- ✅ Používa NEX Genesis ERP
- ✅ Vysoký objem dodávateľských faktúr (50+ mesačne)
- ✅ Štandardizovaní dodávatelia (konzistentný formát PDF)
- ✅ Windows Server infraštruktúra

**Biznis kritériá:**
- ✅ Motivácia zefektívniť procesy
- ✅ Ochota investovať do automatizácie
- ✅ Existujúci IT support
- ✅ Otvorenosť k inovácii

### 6.3 Exklúzie (Nie je pre)

- ❌ Zákazníci bez NEX Genesis
- ❌ Malý objem faktúr (<20 mesačne)
- ❌ Chaotické procesy bez štandardizácie
- ❌ Žiadna IT infraštruktúra

---

## 7. SCOPE A PRIORITY

### 7.1 V Scope - v2.0-v2.4 ✅

| Funkcia | Status | Popis |
|---------|--------|-------|
| Email monitoring | ✅ | n8n IMAP trigger |
| PDF extraction | ✅ | pdfplumber + regex |
| XML generation | ✅ | ISDOC standard |
| NEX Lookup | ✅ | EAN → PLU matching |
| Staging DB | ✅ | PostgreSQL |
| GUI zobrazenie | ✅ | supplier-invoice-editor (PyQt5) |

### 7.2 V Scope - v3.0 (In Progress) 🟡

| Funkcia | Status | Popis |
|---------|--------|-------|
| supplier-invoice-staging | 🟡 | Nová PySide6 aplikácia |
| Farebné rozlíšenie | ⚪ | Matched vs unmatched items |
| Vytvorenie produktov | ⚪ | GSCAT WRITE |
| Evidencia DL | ⚪ | TSH/TSI WRITE |
| Zmeny cien | ⚪ | RPC workflow |

### 7.3 Mimo Scope - v3.0 ❌

| Funkcia | Dôvod | Kedy |
|---------|-------|------|
| Automatické naskladnenie | Robí NEX Genesis | N/A |
| AI priradenie skupín | Potrebné dáta pre tréning | v4.0 |
| Priamy email | Potrebná validácia | v4.0 |
| Multi-tenant dashboard | Príliš skoro | v5.0 |

---

## 8. KRITÉRIÁ ÚSPECHU

### 8.1 Technické - v2.4 ✅

| Kritérium | Target | Actual | Status |
|-----------|--------|--------|--------|
| Úspešnosť extrakcie | 95%+ | 98%+ | ✅ |
| Doba spracovania | <5s | ~2s | ✅ |
| Dátové straty | 0% | 0% | ✅ |
| Uptime service | 99%+ | 99.5% | ✅ |
| Match rate (EAN) | 70%+ | 77.4% | ✅ |

### 8.2 Biznis - v2.4 ✅

| Kritérium | Target | Actual | Status |
|-----------|--------|--------|--------|
| Denné používanie | Áno | Áno | ✅ |
| Zníženie času | 80%+ | ~85% | ✅ |
| Spokojnosť zákazníka | Pozitívna | Pozitívna | ✅ |
| Zero critical bugs | Áno | Áno | ✅ |

### 8.3 GO-LIVE Kritériá - v3.0 ⚪

| Kritérium | Status |
|-----------|--------|
| End-to-end workflow | ⚪ In progress |
| Vytvorenie produktov | ⚪ Planned Q1 2026 |
| Evidencia DL | ⚪ Planned Q1 2026 |
| Dokumentácia kompletná | 🟡 In progress |
| Training dokončený | ⚪ TBD |

---

## 9. DLHODOBÁ VÍZIA

### 9.1 NEX Automat ako Platforma

```
NEX Automat Platform
│
├── 1. Procurement Automation ✅
│   ├── supplier-invoice-loader (v2.4) ✅ PRODUCTION
│   ├── supplier-invoice-staging (v3.0) 🟡 IN PROGRESS
│   └── supplier-order-automation (v4.0) ⚪ FUTURE
│
├── 2. Sales Automation ⚪ FUTURE
│   ├── customer-order-processing
│   ├── customer-invoice-automation
│   └── eshop-integration
│
├── 3. Inventory Management ⚪ FUTURE
│   ├── stock-level-monitoring
│   ├── reorder-automation
│   └── inventory-optimization
│
├── 4. Financial Automation ⚪ FUTURE
│   ├── bank-statement-processing
│   ├── payment-automation
│   └── financial-reporting
│
└── 5. AI/ML Services ⚪ FUTURE
    ├── document-classification
    ├── anomaly-detection
    └── predictive-analytics
```

### 9.2 Technologická Evolúcia

**Fáza 1 (Current):** Hybrid Architecture
- NEX Genesis (Delphi/Btrieve) = Core ERP
- NEX Automat (Python/PostgreSQL) = Automation Layer
- Read/Write Btrieve integration

**Fáza 2 (2026-2027):** Expanded Automation
- Viac automatizovaných modulov
- Centralizovaný dashboard
- Multi-customer support

**Fáza 3 (2028+):** Full Migration
- Postupná migrácia NEX Genesis funkcionalít
- Pure Python/PostgreSQL stack
- Btrieve len pre legacy data

### 9.3 Obchodný Model

**Current:** Custom deployment per customer
- One-time setup fee
- Monthly maintenance fee

**Future:** SaaS Model
- Subscription-based pricing
- Centralized hosting
- Self-service onboarding

---

## 10. KĽÚČOVÉ ROZHODNUTIA

### 10.1 Technologické

| Rozhodnutie | Dôvod | Status |
|-------------|-------|--------|
| Python | Modern, maintainable | ✅ |
| PostgreSQL | Reliable, scalable | ✅ |
| PySide6 | Better licensing than PyQt5 | 🟡 |
| n8n | Visual workflow automation | ✅ |
| FastAPI | Modern async API | ✅ |

Viac v: [TECHNOLOGY_DECISIONS.md](TECHNOLOGY_DECISIONS.md)

### 10.2 Biznis

| Rozhodnutie | Dôvod | Status |
|-------------|-------|--------|
| Human-in-the-loop first | Build trust | ✅ |
| Pilot customers | Validate approach | ✅ |
| Iterative development | Minimize risk | ✅ |
| Documentation first | Enable scaling | 🟡 |

---

## 11. MERATEĽNÉ VÝSLEDKY

### 11.1 Mágerstav - 3 Mesiace Production

**Vstupné dáta:**
- Priemer: 50 faktúr/deň
- Priemer: 15 položiek/faktúra
- Celkom: 750 položiek/deň

**Výsledky:**
- ⏱️ Čas: Z 12.5h → 2h (84% úspora)
- ✅ Match rate: 77.4% (cieľ: 70%+)
- 🐛 Kritické chyby: 0
- 😊 Spokojnosť: Vysoká

**ROI Calculation:**
- Úspora: 10.5h/deň × 20 dní = 210h/mesiac
- @ 15€/h = 3,150€/mesiac
- ROI: <12 mesiacov

---

## 12. RIZIKA A VÝZVY

### 12.1 Technické Riziká

| Riziko | Dopad | Mitigácia |
|--------|-------|-----------|
| Btrieve WRITE problémy | Vysoký | Postupné testovanie, rollback |
| Performance issues | Stredný | Async operations, caching |
| Data corruption | Kritický | Backups, validácia, audit |

### 12.2 Biznis Riziká

| Riziko | Dopad | Mitigácia |
|--------|-------|-----------|
| Zákazník neschváli | Vysoký | Iteratívne demo, feedback |
| Konkurencia | Stredný | First-mover advantage |
| Škálovateľnosť | Stredný | Architecture design |

---

## ZÁVER

NEX Automat predstavuje strategický krok v modernizácii podnikových procesov pre zákazníkov NEX Genesis ERP. Postupnou cestou od čiastočnej k úplnej automatizácii vytvárame **overenú, dôveryhodnú platformu** pre spracovanie obchodných dokumentov.

**Kľúčové výhody:**
- ✅ Dramatická úspora času (80%+)
- ✅ Eliminácia chýb (90%+)
- ✅ Skalovateľnosť
- ✅ ROI <12 mesiacov

**Ďalšie kroky:**
1. Dokončiť supplier-invoice-staging (v3.0)
2. Rozšíriť na ďalších zákazníkov
3. Pridať ďalšie moduly (sales, inventory)
4. Evolúcia smerom k plnej automatizácii

---

**Vytvoril:** Zoltán Rausch & Claude AI  
**Naposledy aktualizované:** 2025-12-13  
**Status:** 📈 Living document  
**Verzia:** 2.0