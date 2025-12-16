# Session Archive: RAG Planning & Design

**Dátum:** 2025-12-16  
**Trvanie:** ~2 hodiny  
**Projekt:** nex-automat  
**Fáza:** Strategic Planning - RAG Implementation  
**Tokeny použité:** ~77,000 / 190,000 (41%)

---

## 🎯 Cieľ Session

Navrhnúť a zdokumentovať kompletný RAG (Retrieval-Augmented Generation) systém pre efektívne využívanie dokumentácie projektu NEX Automat.

---

## 📋 Čo Sme Dosiahli

### 1. RAG Koncept a Vysvetlenie

**Témy:**
- ✅ Vysvetlenie embeddings (all-MiniLM-L6-v2)
- ✅ MLM vs LLM rozdiel
- ✅ RAG architektúra (PostgreSQL + pgvector)
- ✅ Ollama lokálne LLM
- ✅ Offline schopnosti (100% bez internetu po setup)
- ✅ Licencie (Apache 2.0 - všetko zadarmo)

**Kľúčové Poznatky:**
- Embedding model = preklad textu na vektor čísel (384 dimenzií)
- RAG = smart vyhľadávač dokumentov (nie LLM)
- LLM (Claude/Ollama) = generuje odpovede
- RAG + LLM = kompletný systém

### 2. Strategická Analýza - 3 Varianty

**Variant 1: RAG Najprv**
- 2-3 týždne delay
- Potom PySide6 + Temporal rýchlejšie (30-40%)
- Total: 9-11 týždňov

**Variant 2: PySide6 + Temporal Najprv**
- Žiadny delay
- Ale celkovo pomalšie (13-15 týždňov)
- Viac tokenov (2.5M vs 900k)

**Variant 3: HYBRID (ROZHODNUTIE)**
- RAG MVP (1 týždeň)
- Potom PySide6 s RAG pomocou (30% rýchlejšie)
- Potom Temporal s RAG pomocou (30% rýchlejšie)
- Total: 10 týždňov
- ✅ Best of both worlds

**Rozhodnutie:** Hybrid Variant 3
- Minimálny delay (1 týždeň)
- RAG benefit takmer okamžite
- Pragmatický kompromis

### 3. RAG_IMPLEMENTATION.md Dokument

**Vytvorený:** Kompletný 45KB implementačný plán

**Obsah:**
- Architektúra systému (PostgreSQL + pgvector + sentence-transformers)
- Tech stack a hardvérové požiadavky
- 6 implementačných fáz (step-by-step)
- Všetky Python skripty (ready-to-use)
- SQL schémy (kompletné databázové tabuľky)
- Testovacie procedúry (unit tests + query tests)
- Claude integrácia (API wrapper + CLI tools)
- Troubleshooting guide

**Fázy:**
1. PostgreSQL Setup (2-3 hodiny)
2. Python Environment (1 hodina)
3. Ingestion Pipeline (4-6 hodín)
4. Query Pipeline (3-4 hodiny)
5. Testovanie (2-3 hodiny)
6. Claude Integrácia (1-2 hodiny)

**Total čas:** 1 týždeň (RAG MVP)

### 4. Dokumentácia Update

**Aktualizované súbory:**
- ✅ `docs/strategic/RAG_IMPLEMENTATION.md` (nový)
- ✅ `docs/strategic/00_STRATEGIC_INDEX.md` (update)

**Zmeny v indexe:**
- Pridaná sekcia "Ready for Implementation"
- RAG Implementation s HIGH prioritou
- Implementačné priority (HIGH/MEDIUM/LOW)

---

## 💡 Kľúčové Rozhodnutia

### 1. Technológie

**Stack:**
- PostgreSQL 16+ (databáza)
- pgvector 0.5.1+ (vector extension)
- sentence-transformers 2.2.2+ (embeddings)
- all-MiniLM-L6-v2 (embedding model)
- Python 3.11+

**Licencie:**
- Všetko Apache 2.0 / MIT / PostgreSQL License
- 100% zadarmo pre komerčné použitie
- Žiadne runtime poplatky

### 2. Architektúra

**RAG = Smart Vyhľadávač:**
```
Dokumentácia → Chunks → Embeddings → PostgreSQL
    ↓
Otázka → RAG Search → Top chunks → Claude/Ollama
```

**Chunking stratégia:**
- Malé dokumenty (<5k tokens): celý dokument
- Stredné (5k-15k): split by H2
- Veľké (>15k): split by H3
- Target chunk size: 750 tokens
- Overlap: 150 tokens

### 3. Implementačná Stratégia

**Priorita: HYBRID Approach**
- Týždeň 1: RAG MVP (basic ale fungujúce)
- Týždeň 2-6: PySide6 migrácia (s RAG)
- Týždeň 7-9: Temporal migrácia (s RAG)
- Týždeň 10: RAG full features

**Výhody:**
- Minimálny delay (1 týždeň)
- RAG benefit od týždňa 2
- 30% rýchlejší vývoj PySide6 + Temporal
- Token efektivita (64% úspora)

---

## 📊 Metriky

### Token Použitie
- Použité: ~77,000 tokens
- Zostáva: ~113,000 tokens
- Progress: 41%

### Dokumentácia
- Nové dokumenty: 1 (RAG_IMPLEMENTATION.md, ~45KB)
- Aktualizované: 1 (00_STRATEGIC_INDEX.md)
- Total strategic docs: 7

### Časové Odhady
- RAG MVP: 1 týždeň
- PySide6 (s RAG): 4-5 týždňov (namiesto 6-7)
- Temporal (s RAG): 2-3 týždne (namiesto 4-5)
- Total: 10 týždňov (namiesto 13-15)

---

## 🔄 Ďalšie Kroky

### Immediate Next (Nový Chat)
1. **Fáza 1: PostgreSQL Setup** (2-3 hodiny)
   - Inštalácia PostgreSQL 16
   - Vytvorenie nex_automat_rag databázy
   - Inštalácia pgvector extension
   - Vytvorenie tabuliek (rag_documents, rag_chunks, rag_keywords)
   - Testovanie vector operations

### Follow-up Fázy
2. Python Environment setup
3. Ingestion Pipeline
4. Query Pipeline
5. Testovanie
6. Claude Integrácia

---

## 📝 Dôležité Poznámky

### Claude Perspektíva
> "RAG zlepší MOJU schopnosť ti pomôcť!"

**Prečo:**
- Bez RAG: 40% času na reload dokumentov, 8-10 chatov na migráciu
- S RAG: 90% času produktívna práca, 3-4 chaty na migráciu
- RAG = okamžitý prístup k presným dokumentom

### Licenčné Náklady
- PostgreSQL: 0 €
- pgvector: 0 €
- all-MiniLM-L6-v2: 0 €
- Ollama + Llama 3.1: 0 €
- **TOTAL: 0 € (vs €42,000/rok cloud)** 🎉

### Offline Schopnosti
- Po setup: 100% offline fungovanie
- Žiadna závislosť na internete
- Perfektné pre corporate product (privacy)

---

## 🎯 Success Criteria Pre RAG MVP

**Po týždni 1 musí fungovať:**
- ✅ PostgreSQL s pgvector
- ✅ 45 dokumentov nahrané
- ✅ ~300-500 chunks v databáze
- ✅ Query funguje (<100ms)
- ✅ CLI tool `rag_query.py` funguje
- ✅ Test queries 90%+ úspešnosť

---

## 🔗 Súvisiace Dokumenty

**Vytvorené:**
- `docs/strategic/RAG_IMPLEMENTATION.md` - Kompletný implementačný plán

**Aktualizované:**
- `docs/strategic/00_STRATEGIC_INDEX.md` - Pridaný RAG link

**Related:**
- `docs/strategic/N8N_TO_TEMPORAL_MIGRATION.md` - Temporal migrácia (po RAG)
- `docs/migration/PYSIDE6_MIGRATION.md` - PySide6 migrácia (po RAG, TODO)

---

## 💭 Reflections

**Čo fungovalo dobre:**
- Systematický prístup k vysvetleniu RAG konceptu
- Detailná analýza 3 variantov (pomohla rozhodnutiu)
- Kompletný ready-to-use implementačný dokument
- Jasné časové odhady a metriky

**Strategické rozhodnutie:**
- Hybrid variant = pragmatický kompromis
- 1 týždeň delay je prijateľný pre 30% speedup potom
- RAG benefit je dlhodobá investícia

**Next session focus:**
- Čisto technická implementácia (Fáza 1)
- PostgreSQL setup
- Hands-on scripting
- Testing

---

**Status:** ✅ Planning Complete  
**Next:** 🔧 Fáza 1 Implementation  
**Priority:** 🔴 HIGH

**Dátum ukončenia:** 2025-12-16  
**Autor:** Zoltán & Claude