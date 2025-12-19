# NEX Brain - Product Strategy Document

**Produkt:** NEX Brain  
**Typ:** Core komponent NEX ekosystému  
**Status:** 📋 Planning  
**Vytvorené:** 2025-12-18  
**Autori:** Zoltán Rausch, Claude

---

## 1. EXECUTIVE SUMMARY

**NEX Brain** je inteligentné rozhranie pre NEX ekosystém, ktoré umožňuje používateľom pristupovať ku všetkým firemným informáciám pomocou prirodzeného jazyka. Kombinuje RAG (Retrieval-Augmented Generation) technológiu s lokálnym LLM (Ollama) pre maximálnu bezpečnosť a ochranu dát.

**Kľúčová hodnota:** Jeden vstupný bod pre všetky firemné vedomosti - ERP dáta, procesy, dokumentáciu, HR materiály.

---

## 2. VÍZIA A POSITIONING

### 2.1 Problém

Veľké a stredné firmy čelia kritickým výzvam:

- **Fragmentácia vedomostí** - informácie rozsypané v hlavách zamestnancov, dokumentoch, systémoch
- **Závislosť na kľúčových ľuďoch** - odchod zamestnanca = strata know-how
- **Pomalý onboarding** - noví zamestnanci týždne hľadajú informácie
- **Neefektívne vyhľadávanie** - navigácia v ERP menu, prehľadávanie priečinkov
- **Strata kontinuity** - rozhodnutia a dôvody sa strácajú

### 2.2 Riešenie

NEX Brain poskytuje:

- **Centralizovaný knowledge base** - všetky informácie na jednom mieste
- **Prirodzené rozhranie** - otázky v ľudskom jazyku
- **Okamžité odpovede** - AI spracuje dotaz a vráti relevantnú odpoveď
- **On-premise riešenie** - dáta zostávajú v sieti firmy (Ollama)
- **Integrácia s NEX Genesis** - priamy prístup k ERP dátam

### 2.3 Positioning

```
NEX Brain - Inteligentné rozhranie pre váš NEX systém

"Opýtajte sa svojho ERP systému ľudským jazykom"
```

NEX Brain nie je samostatný produkt - je to **evolúcia NEX ekosystému**, ktorá pridáva AI vrstvu nad všetky existujúce komponenty.

---

## 3. ARCHITEKTÚRA

### 3.1 Vysokoúrovňová architektúra

```
┌─────────────────────────────────────────────────────────────┐
│                         POUŽÍVATEĽ                          │
│                    (Web UI / Desktop App)                   │
└─────────────────────────────┬───────────────────────────────┘
                              │ Otázka v prirodzenom jazyku
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        NEX BRAIN API                        │
│                         (FastAPI)                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Query     │  │   Context   │  │      Response       │  │
│  │  Analyzer   │→ │  Retriever  │→ │     Generator       │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└───────────┬─────────────────┬─────────────────┬─────────────┘
            │                 │                 │
            ▼                 ▼                 ▼
┌───────────────────┐ ┌─────────────┐ ┌───────────────────────┐
│    RAG Engine     │ │   Ollama    │ │    NEX Genesis        │
│  (pgvector + API) │ │   (LLM)     │ │    (Btrieve API)      │
└───────────────────┘ └─────────────┘ └───────────────────────┘
            │                                   │
            ▼                                   ▼
┌───────────────────┐               ┌───────────────────────┐
│  Knowledge Base   │               │     ERP Data          │
│  - Dokumenty      │               │  - Objednávky         │
│  - Procesy        │               │  - Faktúry            │
│  - HR materiály   │               │  - Sklady             │
│  - Manuály        │               │  - Partneri           │
└───────────────────┘               └───────────────────────┘
```

### 3.2 Komponenty

| Komponent | Technológia | Účel |
|-----------|-------------|------|
| **Web UI** | React / PySide6 | Používateľské rozhranie |
| **API** | FastAPI | Backend služba |
| **RAG Engine** | pgvector + sentence-transformers | Vyhľadávanie v dokumentoch |
| **LLM** | Ollama (Llama 3.1 8B) | Generovanie odpovedí |
| **NEX Connector** | nexdata package | Prístup k ERP dátam |
| **Knowledge Base** | PostgreSQL + Markdown | Uloženie dokumentov |

### 3.3 Dátové zdroje

**Tier 1 - Dokumenty (RAG):**
- Firemné procesy a postupy
- HR dokumentácia (onboarding, pravidlá)
- Technické manuály
- Zápisnice z porád
- Projektová dokumentácia

**Tier 2 - ERP dáta (Live queries):**
- Objednávky a faktúry
- Skladové stavy
- Partneri a kontakty
- Finančné reporty
- Cenníky

**Tier 3 - Historické dáta:**
- Archívne dokumenty
- Staré rozhodnutia a dôvody
- Lessons learned

---

## 4. USE CASES

### 4.1 Operatívne dotazy

```
Používateľ: "Aký je stav objednávky 12345?"
NEX Brain: "Objednávka 12345 pre ACME s.r.o.:
           - Stav: Čiastočne expedovaná
           - Expedované: 3 z 5 položiek
           - Zostáva: Monitor LCD (2ks) - na sklade 0, objednané u dodávateľa
           - Očakávaná expedícia: 20.12.2025"
```

### 4.2 Procesné dotazy

```
Používateľ: "Ako spracujem reklamáciu od zákazníka?"
NEX Brain: "Postup spracovania reklamácie:
           1. Vytvorte reklamačný protokol v module SALES-CLAIM
           2. Priložte fotodokumentáciu
           3. Odošlite na schválenie vedúcemu (do 24h)
           4. Po schválení vytvorte dobropis alebo náhradnú expedíciu

           Dokument: Reklamačný poriadok v2.3 (link)"
```

### 4.3 HR dotazy

```
Používateľ: "Koľko dní dovolenky mi zostáva?"
NEX Brain: "Podľa HR systému máte zostatok 8 dní dovolenky.
           Čerpané: 12 dní, Nárok: 20 dní.
           Poznámka: Do konca roka musíte vyčerpať min. 4 dni."
```

### 4.4 Analytické dotazy

```
Používateľ: "Aké boli tržby za november podľa kategórií?"
NEX Brain: "Tržby november 2025:
           - Potraviny: 45,230 EUR (52%)
           - Nápoje: 28,100 EUR (32%)
           - Drogéria: 13,670 EUR (16%)
           - SPOLU: 87,000 EUR

           Medziročne: +12% oproti nov 2024"
```

### 4.5 Onboarding dotazy

```
Nový zamestnanec: "Kde nájdem telefónne čísla kolegov?"
NEX Brain: "Telefónny zoznam nájdete:
           1. V NEX Genesis: Modul EMPLOYEES → Tlač → Telefónny zoznam
           2. Na intranete: \\server\shared\HR\kontakty.xlsx
           3. Rýchle kontakty: IT podpora: 123, Účtovníctvo: 124"
```

---

## 5. IMPLEMENTAČNÉ FÁZY

### Fáza 1: Foundation (2 týždne)

**Cieľ:** Základná infraštruktúra a proof-of-concept

- [ ] Vytvorenie `apps/nex-brain/` štruktúry
- [ ] Inštalácia a konfigurácia Ollama
- [ ] Integrácia existujúceho RAG API
- [ ] Základné FastAPI endpointy
- [ ] CLI rozhranie pre testovanie
- [ ] Dokumentácia setup procesu

**Deliverable:** Funkčný CLI kde sa dá pýtať na dokumentáciu

### Fáza 2: Knowledge Base (2 týždne)

**Cieľ:** Naplnenie knowledge base pre pilotných zákazníkov

- [ ] ICC s.r.o. - interná dokumentácia
- [ ] ANDROS s.r.o. - firemné procesy
- [ ] Nástroj na import dokumentov (Word, PDF, Markdown)
- [ ] Automatická indexácia nových dokumentov
- [ ] Kvalita odpovedí - tuning embeddingov

**Deliverable:** Knowledge base s reálnym obsahom

### Fáza 3: NEX Genesis Integration (2 týždne)

**Cieľ:** Live prístup k ERP dátam

- [ ] Definícia bezpečných query patterns
- [ ] Connector pre objednávky, faktúry, sklady
- [ ] Caching stratégia pre časté dotazy
- [ ] Oprávnenia - kto sa môže pýtať na čo

**Deliverable:** Dotazy nad ERP dátami fungujú

### Fáza 4: User Interface (2 týždne)

**Cieľ:** Používateľsky prívetivé rozhranie

- [ ] Web UI (React) - základná verzia
- [ ] Alebo Desktop app (PySide6) - integrácia do NEX Automat
- [ ] História konverzácií
- [ ] Feedback mechanizmus (palec hore/dole)

**Deliverable:** Používatelia môžu pracovať s NEX Brain

### Fáza 5: Pilot Deployment (2 týždne)

**Cieľ:** Nasadenie u pilotných zákazníkov

- [ ] ICC s.r.o. - interný pilot
- [ ] ANDROS s.r.o. - produkčný pilot
- [ ] Zbieranie feedbacku
- [ ] Iterácie na základe spätnej väzby
- [ ] Dokumentácia pre používateľov

**Deliverable:** Fungujúci produkt u 2 zákazníkov

### Fáza 6: Refinement (ongoing)

**Cieľ:** Kontinuálne zlepšovanie

- [ ] Rozšírenie knowledge base
- [ ] Nové ERP integrácie
- [ ] Vylepšenie kvality odpovedí
- [ ] Škálovanie na ďalších zákazníkov

---

## 6. TECHNICKÉ POŽIADAVKY

### 6.1 Server (On-premise u zákazníka)

| Parameter | Minimum | Odporúčané |
|-----------|---------|------------|
| CPU | 8 cores | 16 cores |
| RAM | 16 GB | 32 GB |
| GPU | - | NVIDIA 8GB+ (pre rýchlejší Ollama) |
| Disk | 100 GB SSD | 500 GB SSD |
| OS | Windows Server 2019+ | Windows Server 2022 |

### 6.2 Software stack

- Python 3.11+
- PostgreSQL 15+ s pgvector
- Ollama (latest)
- FastAPI
- sentence-transformers

### 6.3 Ollama modely - Podrobné porovnanie

#### Prehľadová tabuľka

| Model | Parametre | VRAM/RAM | Rýchlosť | Kvalita | Slovak | Odporúčanie |
|-------|-----------|----------|----------|---------|--------|-------------|
| llama3.2:1b | 1B | 1-2 GB | ⚡⚡⚡⚡⚡ | ⭐⭐ | ❌ | Embedded/IoT |
| llama3.2:3b | 3B | 2-3 GB | ⚡⚡⚡⚡ | ⭐⭐⭐ | ❌ | Slabší HW, rýchle odpovede |
| llama3.1:8b | 8B | 5-8 GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | ✅ | **ODPORÚČANÉ pre NEX Brain** |
| mistral:7b | 7B | 4-6 GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | ⚠️ | Alternatíva k Llama |
| llama3.1:70b | 70B | 40-48 GB | ⚡⚡ | ⭐⭐⭐⭐⭐ | ✅ | Enterprise, silný HW |
| mixtral:8x7b | 8x7B | 26-32 GB | ⚡⚡ | ⭐⭐⭐⭐⭐ | ⚠️ | Premium kvalita |
| mistral-small:24b | 24B | 14-16 GB | ⚡⚡ | ⭐⭐⭐⭐⭐ | ⚠️ | Stredná cesta |

#### Llama 3.2 (1B, 3B) - Malé modely

**Plusy:**
- Extrémne rýchle (~76% rýchlejšie ako Mistral 7B)
- Nízke HW požiadavky (2-3 GB RAM)
- Optimalizované pre mobilné zariadenia a edge deployment
- Dobré pre jednoduché úlohy (summarizácia, klasifikácia)

**Mínusy:**
- Obmedzená multilingválna podpora (SK/HU NIE sú oficiálne podporované)
- Slabšie reasoning a komplexné úlohy
- Kratší context window
- Horšia kvalita pri dlhších odpovediach

**Vhodné pre:** Rýchle, jednoduché dotazy, slabší hardware, embedded systémy

---

#### Llama 3.1:8B - **ODPORÚČANÝ PRE NEX BRAIN**

**Plusy:**
- Výborný pomer výkon/kvalita (sweet spot)
- 128K context window (dlhé dokumenty)
- Multilingválna podpora vrátane stredoeurópskych jazykov
- Beží na bežnom gaming PC (RTX 3060/4060 8GB)
- Kvalita blízka GPT-3.5
- Rýchla inferencia (~40+ tokens/s na GPU)
- Apache 2.0 licencia (komerčné použitie OK)

**Mínusy:**
- Vyžaduje 8GB VRAM pre plný výkon
- Na CPU pomalší (ale stále použiteľný)
- Občas halucinácie pri špecifických doménach

**HW požiadavky:**
- GPU: 6-8 GB VRAM (RTX 3060, 4060, 4070)
- CPU-only: 16 GB RAM, pomalšie (~5-10 tokens/s)
- Disk: ~5 GB pre model

**Vhodné pre:** NEX Brain pilot, produkčné nasadenie u zákazníkov

---

#### Mistral 7B

**Plusy:**
- Veľmi dobrá kvalita pre svoju veľkosť
- Menej náchylný na halucinácie ako Llama 2
- Dobrý pre code generation
- Rýchla inferencia

**Mínusy:**
- Slabšia multilingválna podpora (primárne EN/FR)
- Slovenčina/Maďarčina problematická
- Kratší context window (32K vs 128K)
- Benchmark testy ukazujú Llama 3.1 8B je lepší

**Vhodné pre:** Anglické prostredie, code-heavy úlohy

---

#### Mixtral 8x7B (Mixture of Experts)

**Plusy:**
- State-of-the-art kvalita v open-source
- MoE architektúra - aktivuje len 13B parametrov naraz
- Výborné reasoning a analýza
- Veľmi dobré pre komplexné úlohy

**Mínusy:**
- Vysoké VRAM požiadavky (26-32 GB)
- Potrebuje enterprise GPU (RTX 4090, A100)
- Pomalšia inferencia
- Drahší hardware u zákazníka

**HW požiadavky:**
- GPU: 24+ GB VRAM (RTX 4090, A6000)
- Alebo 2x RTX 3090/4090

**Vhodné pre:** Enterprise zákazníci s vysokými nárokmi na kvalitu

---

#### Llama 3.1:70B

**Plusy:**
- Frontier-level kvalita (blízko GPT-4)
- Excelentný pre komplexné reasoning
- Najlepšia multilingválna podpora
- 128K context window

**Mínusy:**
- Vyžaduje 40-48 GB VRAM
- Potrebuje dual GPU setup alebo datacenter GPU
- Vysoké náklady na hardware
- Pomalšia inferencia

**HW požiadavky:**
- GPU: 2x RTX 4090 (48 GB) alebo A100 40GB+
- RAM: 64+ GB

**Vhodné pre:** Veľké enterprise, maximálna kvalita

---

#### Odporúčanie pre NEX Brain

**Fáza 1 (Pilot - ICC, ANDROS):**
```
Primárny:   llama3.1:8b-instruct-q5_K_M
Fallback:   llama3.2:3b (pre rýchle jednoduché dotazy)
```

**Fáza 2 (Škálovanie):**
```
Štandard:   llama3.1:8b
Premium:    mixtral:8x7b alebo llama3.1:70b
```

**Quantization odporúčanie:**
- `q5_K_M` - najlepší pomer kvalita/veľkosť (odporúčané)
- `q4_K_M` - menšia veľkosť, mierne nižšia kvalita
- `q8_0` - vyššia kvalita, väčšie VRAM požiadavky

---

#### Slovenčina a Maďarčina

**Dôležité:** Llama 3.1 má lepšiu podporu stredoeurópskych jazykov ako Mistral.

Pre optimálnu SK/HU podporu:
1. Použiť `llama3.1:8b` ako základ
2. System prompt v slovenčine
3. RAG dokumenty v pôvodnom jazyku (SK)
4. Testovať kvalitu odpovedí v SK pred produkciou

---

## 6.4 Kedy sa oplatí premium model?

### Porovnanie na praktických príkladoch

| Aspekt | llama3.1:8b | mixtral:8x7b | llama3.1:70b |
|--------|-------------|--------------|--------------|
| **Jednoduchý dotaz** | ✅ Rovnaký výsledok | ✅ Rovnaký výsledok | ✅ Rovnaký výsledok |
| **Komplexná analýza** | ⚠️ Občas povrchná | ✅ Hlbšia | ✅✅ Najhlbšia |
| **Reasoning (logika)** | ⚠️ Chyby pri 3+ krokoch | ✅ Lepší | ✅✅ Najlepší |
| **Slovenčina** | ✅ Dobrá | ⚠️ Slabšia | ✅✅ Najlepšia |
| **Halucinácie** | ⚠️ Občas | ✅ Menej | ✅✅ Najmenej |
| **Dlhé dokumenty** | ✅ OK | ✅ OK | ✅✅ Excelentný |

### Príklady z NEX Brain kontextu

**Jednoduchý dotaz:** "Aký je telefón na IT oddelenie?"
→ Všetky modely: Rovnaká odpoveď, žiadny rozdiel

**Procesný dotaz:** "Ako spracujem reklamáciu?"
→ 8B: Správny postup, základné kroky
→ 8x7B/70B: + edge cases + tipy + súvisiace dokumenty

**Analytický dotaz:** "Porovnaj tržby Q3 vs Q4 a vysvetli rozdiely"
→ 8B: Číselné porovnanie, základná interpretácia
→ 8x7B: + trendy, sezónnosť
→ 70B: + hlbšia analýza príčin, odporúčania

**Komplexný reasoning:** "Zákazník reklamuje tovar, faktúra je po splatnosti a má neuhradené iné faktúry. Čo robiť?"
→ 8B: Môže dať neúplnú odpoveď (príliš veľa faktorov)
→ 8x7B: Správne zváži všetky faktory
→ 70B: + právne aspekty, alternatívne riešenia

### Realistické zhodnotenie

**80% dotazov v bežnej firme** (8B postačuje):
- Kde nájdem dokument X?
- Aký je postup pre Y?
- Aký je stav objednávky Z?
- Kto je zodpovedný za...?

**20% dotazov** (premium pomôže):
- Komplexné analýzy
- Rozhodnutia s viacerými faktormi
- Právne a compliance otázky
- Strategické plánovanie

### Nákladová analýza

| Model | HW požiadavka | Cena HW (odhad) | Mesačný náklad |
|-------|---------------|-----------------|----------------|
| llama3.1:8b | RTX 4060 8GB | ~350 EUR | ~5 EUR (elektrina) |
| mixtral:8x7b | RTX 4090 24GB | ~2,000 EUR | ~15 EUR |
| llama3.1:70b | 2x RTX 4090 | ~4,000 EUR | ~30 EUR |

---

## 6.5 Migrácia medzi modelmi

### Prečo je migrácia triviálna

Ollama používa jednotné API pre všetky modely:

```python
# Dnešný kód s 8B
response = ollama.chat(model="llama3.1:8b", messages=[...])

# Zajtra s 70B - zmena JEDNÉHO parametra
response = ollama.chat(model="llama3.1:70b", messages=[...])
```

**Žiadne zmeny potrebné v:** RAG systéme, API endpointoch, databáze, UI aplikácii, promptoch.

### Kroky pri upgrade

| Krok | Náročnosť | Čas |
|------|-----------|-----|
| Stiahnutie nového modelu | `ollama pull llama3.1:70b` | 30 min |
| Zmena config parametra | 1 riadok | 1 min |
| HW upgrade (ak treba) | Kúpa GPU | 1-2 dni |
| Testovanie | Smoke test | 1 hodina |

### Možné scenáre upgradu

**Scenár A - Rovnaký HW:**
`llama3.1:8b → llama3.1:8b-q8_0` (vyššia kvalita quantization)

**Scenár B - Lepší model:**
`llama3.1:8b → mixtral:8x7b` (+ kúpa RTX 4090)

**Scenár C - Hybrid architektúra (budúcnosť):**
```python
if is_complex_query(question):
    model = "llama3.1:70b"  # presný, pomalší
else:
    model = "llama3.1:8b"   # rýchly, lacný
```

### Čo zostáva rovnaké pri upgrade

- ✅ RAG knowledge base (embeddings nezávislé od LLM)
- ✅ Všetky dokumenty a indexy
- ✅ API štruktúra
- ✅ UI aplikácia
- ✅ Používateľské nastavenia
- ✅ História konverzácií

**Záver:** Začať s `llama3.1:8b` je bezrizikové. Upgrade je otázka minút (softvér) alebo dní (hardvér).

---

## 7. BEZPEČNOSŤ A PRIVACY

### 7.1 Princípy

1. **On-premise only** - žiadne dáta neopúšťajú firemnú sieť
2. **Lokálny LLM** - Ollama beží na zákazníkovom serveri
3. **Role-based access** - používateľ vidí len to, na čo má oprávnenie
4. **Audit log** - všetky dotazy sa logujú
5. **No training** - firemné dáta sa nepoužívajú na trénovanie modelu

### 7.2 Oprávnenia

```
Admin       → všetko
Manager     → všetky dokumenty + agregované ERP dáta
Employee    → procesná dokumentácia + vlastné ERP dáta
Guest       → len verejná dokumentácia
```

---

## 8. PILOT PLÁN

### 8.1 ICC s.r.o. (Dev/Test)

**Časový rámec:** Január 2026

**Knowledge base:**
- NEX Automat dokumentácia (už v RAG)
- NEX Genesis manuály
- Interné IT procesy

**Používatelia:** 3-5 (vývojový tím)

**Cieľ:** Validácia technológie, rýchla iterácia

### 8.2 ANDROS s.r.o. (Production pilot)

**Časový rámec:** Február 2026

**Knowledge base:**
- Firemné procesy a postupy
- HR dokumentácia
- Produktové katalógy
- Skladové procedúry

**Používatelia:** 10-15 (vybrané oddelenia)

**Cieľ:** Validácia hodnoty produktu v reálnom prostredí

---

## 9. SUCCESS METRICS

### 9.1 Kvantitatívne

| Metrika | Cieľ (3 mesiace) |
|---------|------------------|
| Počet dotazov/deň | 50+ |
| Úspešnosť odpovede | >80% |
| Priemerný čas odpovede | <5 sekúnd |
| User satisfaction | >4/5 |

### 9.2 Kvalitatívne

- Zníženie času na onboarding nových zamestnancov
- Menej prerušení "kľúčových ľudí" rutinnými otázkami
- Dokumentované know-how (nie len v hlavách)
- Pozitívny feedback od používateľov

---

## 10. RIZIKÁ A MITIGÁCIA

| Riziko | Pravdepodobnosť | Dopad | Mitigácia |
|--------|-----------------|-------|-----------|
| Nízka kvalita odpovedí | Stredná | Vysoký | Tuning embeddingov, lepšie prompty |
| Pomalé odpovede | Nízka | Stredný | GPU akcelerácia, caching |
| Nedostatok obsahu | Stredná | Vysoký | Systematický import dokumentov |
| Odpor používateľov | Nízka | Stredný | Training, ukázky hodnoty |
| HW požiadavky | Nízka | Stredný | Menšie modely, cloud fallback |

---

## 11. ROADMAP

```
2025-Q4 (December)
├── ✅ Strategický dokument
├── ✅ RAG systém funkčný
└── 📋 Ollama evaluácia

2026-Q1 (Jan-Mar)
├── Fáza 1-2: Foundation + Knowledge Base
├── Fáza 3: NEX Genesis Integration
├── ICC pilot spustený
└── ANDROS pilot spustený

2026-Q2 (Apr-Jun)
├── Fáza 4: User Interface
├── Refinement na základe feedbacku
├── Rozšírenie na ďalších zákazníkov
└── Marketing materiály

2026-H2
├── Škálovanie
├── Advanced features (voice, mobile)
└── Samostatný produkt (ak validované)
```

---

## 12. SÚVISIACE DOKUMENTY

- [RAG Implementation](RAG_IMPLEMENTATION.md) - Technická dokumentácia RAG
- [Project Roadmap](PROJECT_ROADMAP.md) - NEX Automat roadmap
- [AI/ML Technologies](AI_ML_TECHNOLOGIES.md) - Schválené technológie

---

**Dokument Version:** 1.0  
**Status:** 📋 Planning  
**Next Review:** Po dokončení Fázy 1
