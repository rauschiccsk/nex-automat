# UAE Legal Documentation Repository

## Účel
Tento repozitár obsahuje právnu dokumentáciu Spojených arabských emirátov (UAE) pre použitie v NexBrain multi-tenant RAG systéme.

## Tenant ID
`uae`

## Štruktúra

### federal_laws/
Federálne zákony UAE platné na celom území federácie.

**Príklady:**
- Federal Law No. 5 of 1985 (Civil Transactions Law)
- Federal Law No. 3 of 1987 (Penal Code)
- Federal Decree-Law No. 18 of 2018 (Commercial Companies Law)

### emirate_laws/
Zákony jednotlivých emirátov (Abu Dhabi, Dubai, Sharjah, atď.)

**Príklady:**
- Dubai Law No. 13 of 2011 (Free Zones Regulations)
- Abu Dhabi Law No. 1 of 2013 (Civil Law)

### court_decisions/
Súdne rozhodnutia a precedensy.

**Kategórie:**
- Federal Supreme Court decisions
- Court of Cassation judgments
- Lower court precedents

### legal_procedures/
Právne procedúry, postupy a praktické návody.

**Obsah:**
- Court filing procedures
- Administrative processes
- Licensing requirements
- Contract templates

## Formát dokumentov

### Podporované formáty
- **Markdown (.md)** - preferovaný formát pre primárne texty
- **PDF** - pre originálne právne dokumenty
- **TXT** - pre čisté textové verzie

### Štruktúra markdown dokumentov
```markdown
# [Názov zákona/rozhodnutia]

**Číslo:** [Číslo zákona]  
**Dátum vydania:** [YYYY-MM-DD]  
**Jurisdikcia:** [Federal/Emirate]  
**Status:** [Platný/Zrušený/Novelizovaný]

## Obsah
[Text dokumentu s paragrafmi]

## Súvisiace zákony
- [Zoznam súvisiacich zákonov]
```

## Použitie RAG API

### Vyhľadávanie v UAE tenant
```bash
# Základné vyhľadávanie
curl "https://rag-api.icc.sk/search?query=commercial%20contract&tenant=uae&limit=5"

# S dodatočnými filtrami
curl "https://rag-api.icc.sk/search?query=company%20formation&tenant=uae&limit=10"
```

### Python príklad
```python
import requests

response = requests.get(
    "https://rag-api.icc.sk/search",
    params={
        "query": "employment contract termination",
        "tenant": "uae",
        "limit": 5
    }
)

results = response.json()
for result in results:
    print(f"Dokument: {result['source']}")
    print(f"Relevancia: {result['score']}")
    print(f"Text: {result['text'][:200]}...")
```

## Indexácia dokumentov

### Pridanie nových dokumentov
1. Umiestnite dokumenty do príslušného podadresára
2. Spustite denný update:
```bash
python tools/rag/rag_update.py --new
```

### Úplná reindexácia
Pre úplnú reindexáciu všetkých UAE dokumentov:
```bash
python tools/rag/rag_update.py --all
```

### Kontrola štatistík
```bash
python tools/rag/rag_update.py --stats
```

## Metadata

Každý dokument v indexe obsahuje:
- `tenant`: 'uae'
- `source`: Relatívna cesta k súboru
- `created_at`: Timestamp vytvorenia
- `updated_at`: Timestamp poslednej aktualizácie
- `document_type`: federal_law | emirate_law | court_decision | legal_procedure
- `jurisdiction`: federal | abu_dhabi | dubai | sharjah | ...
- `law_number`: Číslo zákona (ak aplikovateľné)
- `effective_date`: Dátum nadobudnutia účinnosti
- `status`: active | repealed | amended

## Správa verziování

### Legislatívne zmeny
Pri novelizácii zákonov:
1. Pôvodný zákon označte v metadátach ako `amended`
2. Vytvorte nový dokument s novelizovanou verziou
3. V oboch dokumentoch uveďte vzájomné referencie

### História zmien
Adresár `_archive/` obsahuje historické verzie zrušených alebo významne zmenených zákonov.

## Best Practices

### Naming conventions
- Používajte anglické názvy súborov
- Formát: `law_number_year_short_title.md`
- Príklad: `fed_law_05_1985_civil_transactions.md`

### Chunking stratégia
- Právne dokumenty sa členitia podľa paragrafov
- Každý chunk obsahuje kontext (názov zákona, časť, kapitola)
- Zachováva sa štruktúra a hierarchia dokumentu

### Embedding optimalizácia
- Právne texty používajú špecifické embedding modely
- Priorizuje sa presnosť nad všeobecnosť
- Zachováva sa právna terminológia

## Compliance a Audit

### Audit logging
Všetky vyhľadávania v UAE tenant sú logované pre právne účely.

### Access control
Prístup k UAE tenant môže vyžadovať dodatočnú autorizáciu v závislosti od konfigurácie.

### Data retention
Dokumenty sa uchovávajú v súlade s archivačnými požiadavkami.

## Kontakt

**Správca repozitára:** Zoltán Rausch  
**Projekt:** nex-automat / NexBrain  
**Organizácia:** ICC s.r.o.

## Verzia
- **Vytvorené:** 2026-01-08
- **Verzia:** 1.0.0
- **Posledná aktualizácia:** 2026-01-08
