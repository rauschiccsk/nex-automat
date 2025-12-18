# Session: RAG Knowledge System & DB Schema Design

**Dátum:** 2025-12-18  
**Poradové číslo:** 01  
**Projekt:** nex-automat  
**Stav:** COMPLETED

---

## Prehľad Session

Riešenie kritického problému s únikom informácií z RAG systému a návrh novej DB schémy pre supplier_invoice_staging.

---

## Dokončené Úlohy

### 1. Analýza RAG problému
- ✅ Identifikovaný únik: `rag_update.py --new` neindexoval `docs/` súbory
- ✅ Len Python súbory sa konvertovali na .md a indexovali
- ✅ Session archívy sa nikdy nedostali do RAG

### 2. Nový Knowledge System
- ✅ Vytvorená štruktúra `docs/knowledge/`
  - `decisions/` - architektonické rozhodnutia
  - `development/` - dev poznatky
  - `deployment/` - deployment postupy
  - `scripts/` - permanentné scripty ako .md
  - `specifications/` - technické špecifikácie (DB, API)
- ✅ Script `01_create_knowledge_structure.py`

### 3. Upravený rag_update.py (v2)
- ✅ Odstránená generácia .py → .md
- ✅ `--new` indexuje `docs/knowledge/*.md` zmenené dnes
- ✅ `--all` indexuje celý `docs/` priečinok
- ✅ Stats zobrazuje počet knowledge dokumentov

### 4. Upravený new_chat.py (v2)
- ✅ Poradové číslo pre sessions (`{NN}`)
- ✅ Interaktívne pridávanie knowledge dokumentov
- ✅ Multiline input pre obsah
- ✅ Automatické spustenie RAG update

### 5. DB Schéma - supplier_invoice_staging
- ✅ Konvencia `xml_*` / `nex_*` prefixov
- ✅ `supplier_invoice_heads` - 15 XML + 8 NEX polí
- ✅ `supplier_invoice_items` - 11 XML + 10 NEX polí
- ✅ Workflow stavy: pending → matched → approved → imported
- ✅ Matching metódy: ean, seller_code, name, manual
- ✅ Triggery pre updated_at a štatistiky

---

## Modifikované Súbory

### Nové súbory:
- `docs/knowledge/` - nová štruktúra priečinkov
- `scripts/01_create_knowledge_structure.py`

### Upravené súbory:
- `tools/rag/rag_update.py` - v2 s knowledge indexovaním
- `new_chat.py` - v2 s poradovým číslom a knowledge docs

---

## Kľúčové Rozhodnutia

### 1. Konvencia názvov DB polí
- `xml_*` = polia z ISDOC XML (IMMUTABLE)
- `nex_*` = polia z NEX Genesis (obohatenie)
- **Pravidlo:** XML údaje len ukladáme, nič nepočítame

### 2. Session naming convention
- Formát: `SESSION_{YYYY-MM-DD}_{NN}_{topic}.md`
- `{NN}` = poradové číslo v daný deň (01, 02, 03...)

### 3. Knowledge docs naming
- Formát: `{YYYY-MM-DD}_{topic}.md`
- Ukladajú sa do `docs/knowledge/{category}/`

---

## Ďalšie Kroky (Nový Chat)

### Priority #1: Aplikovať DB schému
1. Vytvoriť SQL súbor na disk
2. Spustiť migráciu v PostgreSQL
3. Overiť štruktúru tabuliek

### Priority #2: Connect GUI to Real Data
1. Pridať database service do supplier-invoice-staging
2. Implementovať queries pre reálne dáta
3. Nahradiť test data

---

## Technické Poznámky

### RAG Workflow (nový)
1. Počas session vytvárať knowledge dokumenty
2. Na konci session: `python new_chat.py`
3. Script uloží session + knowledge + spustí RAG update
4. Knowledge dokumenty sa automaticky indexujú

### Naming conventions
- Session: `SESSION_2025-12-18_01_topic.md`
- Knowledge: `2025-12-18_topic.md`

---

**Session ukončená:** 2025-12-18