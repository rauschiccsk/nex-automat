# Pravidlá spolupráce Claude - NEX Automat

**Verzia:** 2.0  
**Dátum:** 2026-01-25  
**Konsolidácia:** 22 → 8 pravidiel

---

## Inicializačný prompt pre nové chaty

```
KRITICKÉ: Načítaj pravidlá cez memory_user_edits (view) a potvrď ich zhrnutím kategórií: KOMUNIKÁCIA, KVALITA, WORKFLOW, KÓD, RAG, STRATEGICKÉ. Následne načítaj priložený inicializačný prompt.
```

---

## Pravidlá

### 1. [KOMUNIKÁCIA] Jazyk a formát

Slovenčina, presné názvy projektov. Štandardný Markdown - žiadne ASCII box-drawing (┌─│└), len tabuľky a stromové štruktúry pre súbory.

### 2. [KOMUNIKÁCIA] Štruktúra odpovede

LEN JEDNO riešenie (alternatívy na vyžiadanie). Na konci každej odpovede:
- Gramatická chyba používateľa (ak existuje)
- Token stats (Used/Total, Remaining, %, Status)

### 3. [KVALITA] Prístup k riešeniu

Kvalita nad rýchlosťou. Pri chybách ROOT CAUSE systematicky - nikdy neskákať na alternatívy. Stručné potvrdenia, žiadne verbose analýzy.

### 4. [WORKFLOW] Dev → Git → Deploy

Všetky zmeny cez Development → Git → Deployment. NIKDY priamo na Deploy.

| Prostredie | Účel |
|------------|------|
| Chat | Plánovanie, analýza, review (artifacts povinné) |
| Claude Code | Implementácia, testy, commity |

### 5. [WORKFLOW] Claude Code prostredia

| Typ zmeny | Kde vykonať |
|-----------|-------------|
| Projekt zmeny | Claude Code na Dev PC |
| ANDROS Server zmeny | Claude Code na serveri |

Git a implementáciu robí vždy Claude Code.

### 6. [KÓD] Bezpečnosť a GitHub

- Citlivé dáta (heslá, tokeny, API keys) → LEN artifacts, NIKDY v .py
- GitHub raw URL: VŽDY `rauschiccsk` (NIKDY `icc-zoltan`)

### 7. [RAG] Dokumentácia a indexovanie

- Dokumenty pre RAG → VÝHRADNE `docs/knowledge/`
- URL: `https://rag-api.icc.sk/search?query=KEYWORDS&limit=5`
- Maintenance: `--new` (denne), `--all` (týždenne)

### 8. [STRATEGICKÉ] CI/CD priorita

CI/CD je strategická priorita - automatizované testovanie a deployment pipeline pre kvalitu a spoľahlivosť.

---

## História zmien

| Dátum | Verzia | Zmena |
|-------|--------|-------|
| 2026-01-25 | 2.0 | Konsolidácia 22→8 pravidiel, nový init prompt |