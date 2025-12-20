"""
Create NEX_BRAIN_PRODUCT.md - Complete Document
Vytvorí kompletný strategický dokument s UI rozhodnutím
"""
from pathlib import Path

PRODUCT_DOC = Path("docs/knowledge/strategic/NEX_BRAIN_PRODUCT.md")


def create_full_document():
    """Vytvorí kompletný NEX_BRAIN_PRODUCT.md dokument"""
    return '''# NEX Brain - Product Strategy Document

**Produkt:** NEX Brain  
**Typ:** Core komponent NEX ekosystému  
**Status:** 🚧 In Development (Fáza 1 Complete)  
**Vytvorené:** 2025-12-18  
**Aktualizované:** 2025-12-19  
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
│              (Telegram Bot / PySide6 Panel)                 │
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
| **UI MVP** | Telegram Bot | Rýchle nasadenie, testovanie |
| **UI Finálne** | PySide6 Panel | Integrácia do NEX Automat |
| **API** | FastAPI | Backend služba |
| **RAG Engine** | pgvector + sentence-transformers | Vyhľadávanie v dokumentoch |
| **LLM** | Ollama (llama3.1:8b) | Generovanie odpovedí |
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
           - Zostáva: Monitor LCD (2ks) - na sklade 0
           - Očakávaná expedícia: 20.12.2025"
```

### 4.2 Procesné dotazy

```
Používateľ: "Ako spracujem reklamáciu od zákazníka?"
NEX Brain: "Postup spracovania reklamácie:
           1. Vytvorte reklamačný protokol v module SALES-CLAIM
           2. Priložte fotodokumentáciu
           3. Odošlite na schválenie vedúcemu (do 24h)
           4. Po schválení vytvorte dobropis"
```

### 4.3 HR dotazy

```
Používateľ: "Koľko dní dovolenky mi zostáva?"
NEX Brain: "Podľa HR systému máte zostatok 8 dní dovolenky.
           Čerpané: 12 dní, Nárok: 20 dní."
```

---

## 5. IMPLEMENTAČNÉ FÁZY

### Fáza 1: Foundation (2 týždne) ✅ COMPLETE

**Cieľ:** Základná infraštruktúra a proof-of-concept

- [x] Vytvorenie `apps/nex-brain/` štruktúry
- [x] Inštalácia a konfigurácia Ollama
- [x] Integrácia existujúceho RAG API
- [x] Základné FastAPI endpointy
- [x] CLI rozhranie pre testovanie
- [x] Multi-tenant architektúra (ICC, ANDROS)
- [x] Tenant filtering v RAG

**Deliverable:** Funkčný CLI kde sa dá pýtať na dokumentáciu ✅

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

**ROZHODNUTIE (2025-12-19):** Dvojfázový prístup

#### Fáza 4a: Telegram Bot (MVP) - 2-3 dni
- [ ] python-telegram-bot integrácia
- [ ] Základné dotazy cez chat
- [ ] Multi-user bez dodatočnej práce
- [ ] Push notifikácie

**Výhody MVP:**
- Žiadna inštalácia u používateľov
- Mobilný + desktopový prístup
- Overenie konceptu pred veľkou investíciou
- Feedback od reálnych používateľov

#### Fáza 4b: PySide6 Panel (Finálne) - 2 týždne
- [ ] Integrovaný panel v NEX Automat
- [ ] Kontextové dotazy (viď aktuálnu faktúru)
- [ ] História konverzácií
- [ ] Feedback mechanizmus (palec hore/dole)

**Prečo PySide6 ako finálne riešenie:**
- Konzistentné s NEX Automat ekosystémom
- Jeden tech stack (Python)
- Hlbšia integrácia - kontextové awareness
- Zdieľané komponenty so shared-pyside6

**Deliverable:** 
- MVP: Telegram bot pre pilotných používateľov
- Finálne: Integrovaný panel v NEX Automat

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
- python-telegram-bot (pre MVP)

### 6.3 Ollama modely

| Model | Veľkosť | Use case |
|-------|---------|----------|
| **llama3.1:8b** | 5 GB | Odporúčané - dobrá SK podpora |
| llama3.2:3b | 2 GB | Rýchle odpovede, slabší HW |
| mistral:7b | 4 GB | Alternatíva |

---

## 7. BEZPEČNOSŤ A PRIVACY

### 7.1 Princípy

1. **On-premise only** - žiadne dáta neopúšťajú firemnú sieť
2. **Lokálny LLM** - Ollama beží na zákazníkovom serveri
3. **Role-based access** - používateľ vidí len to, na čo má oprávnenie
4. **Audit log** - všetky dotazy sa logujú
5. **Tenant isolation** - multi-tenant architektúra s oddelenými dátami

---

## 8. PILOT ZÁKAZNÍCI

| Zákazník | Typ | Status | Knowledge Base |
|----------|-----|--------|----------------|
| ICC s.r.o. | Interný | 🚧 Preparing | docs/knowledge/tenants/icc/ |
| ANDROS s.r.o. | Externý | 🚧 Preparing | docs/knowledge/tenants/andros/ |

---

**Dokument aktualizovaný:** 2025-12-19
'''


# Nový obsah pre Fázu 4
NEW_PHASE_4 = '''### Fáza 4: User Interface (2 týždne)

**Cieľ:** Používateľsky prívetivé rozhranie

**ROZHODNUTIE (2025-12-19):** Dvojfázový prístup

#### Fáza 4a: Telegram Bot (MVP) - 2-3 dni
- [x] Rýchle nasadenie pre testovanie
- [ ] python-telegram-bot integrácia
- [ ] Základné dotazy cez chat
- [ ] Multi-user bez dodatočnej práce
- [ ] Push notifikácie

**Výhody MVP:**
- Žiadna inštalácia u používateľov
- Mobilný + desktopový prístup
- Overenie konceptu pred veľkou investíciou
- Feedback od reálnych používateľov

#### Fáza 4b: PySide6 Panel (Finálne) - 2 týždne
- [ ] Integrovaný panel v NEX Automat
- [ ] Kontextové dotazy (viď aktuálnu faktúru)
- [ ] História konverzácií
- [ ] Feedback mechanizmus (palec hore/dole)

**Prečo PySide6 ako finálne riešenie:**
- Konzistentné s NEX Automat ekosystémom
- Jeden tech stack (Python)
- Hlbšia integrácia - kontextové awareness
- Zdieľané komponenty so shared-pyside6

**Deliverable:** 
- MVP: Telegram bot pre pilotných používateľov
- Finálne: Integrovaný panel v NEX Automat'''


def main():
    print("=" * 70)
    print("CREATE NEX_BRAIN_PRODUCT.md - Complete Document")
    print("=" * 70)

    # Vytvor adresár ak neexistuje
    PRODUCT_DOC.parent.mkdir(parents=True, exist_ok=True)
    print(f"✅ Adresár: {PRODUCT_DOC.parent}")

    # Vytvor kompletný dokument
    content = create_full_document()
    PRODUCT_DOC.write_text(content, encoding='utf-8')
    print(f"✅ Vytvorený: {PRODUCT_DOC}")

    print("\n" + "=" * 70)
    print("OBSAH DOKUMENTU:")
    print("=" * 70)
    print("- Executive Summary")
    print("- Vízia a Positioning")
    print("- Architektúra (Telegram Bot MVP + PySide6 Finálne)")
    print("- Use Cases")
    print("- Implementačné Fázy (1-6)")
    print("- Technické Požiadavky")
    print("- Bezpečnosť a Privacy")
    print("- Pilot Zákazníci")
    print("=" * 70)
    print("\n✅ UI ROZHODNUTIE (2025-12-19):")
    print("   Fáza 4a: Telegram Bot (MVP) - 2-3 dni")
    print("   Fáza 4b: PySide6 Panel (Finálne) - 2 týždne")
    print("=" * 70)

    return True


if __name__ == "__main__":
    main()