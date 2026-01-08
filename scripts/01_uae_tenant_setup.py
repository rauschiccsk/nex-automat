#!/usr/bin/env python3
"""
UAE Tenant Setup Script
=======================
Vytvorí nový tenant 'uae' pre UAE právnu dokumentáciu v NexBrain multi-tenant architektúre.

Projekt: nex-automat / NexBrain
Autor: Zoltán Rausch
Dátum: 2026-01-08
"""

import sys
from pathlib import Path
from datetime import datetime


# Farby pre terminálový output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text):
    """Vytlačí hlavičku sekcie"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}\n")


def print_success(text):
    """Vytlačí success správu"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_info(text):
    """Vytlačí info správu"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")


def print_warning(text):
    """Vytlačí warning správu"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")


def print_error(text):
    """Vytlačí error správu"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def create_directory(path: Path) -> bool:
    """Vytvorí adresár ak neexistuje"""
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print_error(f"Chyba pri vytváraní adresára {path}: {e}")
        return False


def create_file(path: Path, content: str) -> bool:
    """Vytvorí súbor s obsahom"""
    try:
        path.write_text(content, encoding='utf-8')
        return True
    except Exception as e:
        print_error(f"Chyba pri vytváraní súboru {path}: {e}")
        return False


def update_env_file(env_path: Path) -> bool:
    """Aktualizuje .env súbor - pridá 'uae' do TENANTS"""
    try:
        if not env_path.exists():
            print_error(f".env súbor neexistuje: {env_path}")
            return False

        content = env_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        updated = False

        for i, line in enumerate(lines):
            if line.startswith('TENANTS='):
                current_tenants = line.split('=')[1].strip()
                if 'uae' not in current_tenants:
                    lines[i] = f"TENANTS={current_tenants},uae"
                    updated = True
                    print_success(f"Aktualizované: {lines[i]}")
                else:
                    print_info("Tenant 'uae' už existuje v .env")
                break

        if updated:
            env_path.write_text('\n'.join(lines), encoding='utf-8')
            return True
        return True

    except Exception as e:
        print_error(f"Chyba pri aktualizácii .env: {e}")
        return False


def main():
    """Hlavná funkcia setupu"""
    print_header("UAE TENANT SETUP - NexBrain Multi-Tenant RAG")

    # Základné cesty
    project_root = Path(r"C:\Development\nex-automat")
    tenant_root = project_root / "docs" / "knowledge" / "tenants" / "uae"
    env_file = project_root / "apps" / "nex-brain" / ".env"

    print_info(f"Project root: {project_root}")
    print_info(f"Tenant root: {tenant_root}")
    print_info(f"Env file: {env_file}")

    # Zoznam adresárov na vytvorenie
    directories = [
        tenant_root / "federal_laws",
        tenant_root / "emirate_laws",
        tenant_root / "court_decisions",
        tenant_root / "legal_procedures"
    ]

    # 1. Vytvorenie adresárovej štruktúry
    print_header("1. Vytvorenie adresárovej štruktúry")
    for directory in directories:
        if create_directory(directory):
            print_success(f"Vytvorený adresár: {directory.relative_to(project_root)}")

    # 2. Vytvorenie hlavného README.md
    print_header("2. Vytvorenie hlavného README.md")

    main_readme = """# UAE Legal Documentation Repository

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
"""

    if create_file(tenant_root / "README.md", main_readme):
        print_success(f"Vytvorený: README.md")

    # 3. Vytvorenie README.md pre každý podadresár
    print_header("3. Vytvorenie README pre podadresáre")

    subdirs_readme = {
        "federal_laws": """# Federal Laws / Federálne zákony

## Účel
Tento adresár obsahuje federálne zákony UAE, ktoré sú platné na celom území federácie.

## Štruktúra dokumentov
Každý zákon by mal obsahovať:
- Číslo zákona
- Dátum vydania a účinnosti
- Kompletný text s paragrafmi
- Referencie na súvisiace zákony
- Status (platný/novelizovaný/zrušený)

## Príklady kľúčových zákonov
- Federal Law No. 5 of 1985 (Civil Transactions Law)
- Federal Law No. 3 of 1987 (Penal Code)
- Federal Law No. 8 of 1980 (Labour Law)
- Federal Decree-Law No. 18 of 2018 (Commercial Companies Law)

## Naming convention
`fed_law_[number]_[year]_[short_title].md`

Príklad: `fed_law_05_1985_civil_transactions.md`
""",
        "emirate_laws": """# Emirate Laws / Zákony emirátov

## Účel
Tento adresár obsahuje zákony jednotlivých emirátov (Abu Dhabi, Dubai, Sharjah, atď.)

## Organizácia
Dokumenty organizované podľa emirátu:
- Abu Dhabi
- Dubai
- Sharjah
- Ajman
- Umm Al Quwain
- Ras Al Khaimah
- Fujairah

## Príklady
- Dubai Law No. 13 of 2011 (Free Zones Regulations)
- Abu Dhabi Law No. 1 of 2013 (Civil Law)

## Naming convention
`[emirate]_law_[number]_[year]_[short_title].md`

Príklad: `dubai_law_13_2011_free_zones.md`
""",
        "court_decisions": """# Court Decisions / Súdne rozhodnutia

## Účel
Tento adresár obsahuje súdne rozhodnutia a precedensy UAE súdov.

## Kategórie
- **Federal Supreme Court** - najvyššie súdne rozhodnutia
- **Court of Cassation** - kasačné súdy
- **Lower Courts** - rozhodnutia nižších súdov

## Štruktúra dokumentu
- Číslo prípadu
- Dátum rozhodnutia
- Súd
- Zhrnutie prípadu
- Právne otázky
- Rozhodnutie súdu
- Dôsledky a precedensy

## Naming convention
`[court]_[year]_[case_number]_[short_title].md`

Príklad: `federal_supreme_2023_001_contract_dispute.md`
""",
        "legal_procedures": """# Legal Procedures / Právne procedúry

## Účel
Tento adresár obsahuje právne procedúry, postupy a praktické návody.

## Kategórie

### Court Procedures
- Podávanie žalôb
- Odvolania
- Vykonávacie konanie

### Administrative Procedures
- Licencie a povolenia
- Registrácie
- Notárske úkony

### Business Procedures
- Založenie spoločnosti
- Zmeny v obchodnom registri
- Ukončenie podnikania

### Templates
- Vzory zmlúv
- Právne formuláre
- Dokumentácia

## Naming convention
`proc_[category]_[specific_procedure].md`

Príklad: `proc_court_filing_civil_claim.md`
"""
    }

    for subdir_name, readme_content in subdirs_readme.items():
        subdir_path = tenant_root / subdir_name
        readme_path = subdir_path / "README.md"
        if create_file(readme_path, readme_content):
            print_success(f"Vytvorený: {subdir_name}/README.md")

    # 4. Vytvorenie inicializačného dokumentu
    print_header("4. Vytvorenie úvodného dokumentu")

    intro_doc = """# UAE Legal System Overview

**Dokument:** Úvod do právneho systému UAE  
**Vytvorené:** 2026-01-08  
**Tenant:** uae  
**Typ:** Prehľadový dokument

## Úvod

Spojené arabské emiráty (UAE) majú unikátny právny systém, ktorý kombinuje islámske právo (Sharia), civilné právo a common law princípy.

## Štruktúra právneho systému

### 1. Federálny systém
UAE je federácia siedmich emirátov:
- Abu Dhabi (hlavné mesto)
- Dubai
- Sharjah
- Ajman
- Umm Al Quwain
- Ras Al Khaimah
- Fujairah

### 2. Hierarchia právnych predpisov

#### Ústava (1971)
Najvyšší právny dokument UAE definujúci štruktúru štátu a základné práva.

#### Federálne zákony
Zákony vydané federálnou vládou, platné vo všetkých emirátoch.

#### Emirátne zákony
Zákony jednotlivých emirátov v oblastiach, kde majú jurisdikciu.

#### Výkonné nariadenia
Ministerskými rozhodnutiami a nariadeniami.

### 3. Súdny systém

#### Federálne súdy
- Federal Supreme Court
- Federal Courts of Appeal
- Federal Courts of First Instance

#### Emirátne súdy
- Abu Dhabi Judicial Department
- Dubai Courts
- Ostatné emirátne súdne systémy

#### Špecializované súdy
- DIFC Courts (Dubai International Financial Centre)
- ADGM Courts (Abu Dhabi Global Market)

## Právne oblasti

### Civil Law
Občianske právo upravujúce zmluvy, vlastníctvo, dedičstvo.

### Commercial Law
Obchodné právo vrátane spoločností, obchodu, bankového práva.

### Labour Law
Pracovné právo upravujúce pracovné vzťahy.

### Criminal Law
Trestné právo s vplyvom Sharia princípov.

### Family Law
Rodinné právo prevažne založené na islamskom práve.

## Kľúčové charakteristiky

### Sharia Law
Islamské právo ovplyvňuje najmä rodinné právo, dedičstvo a niektoré oblasti trestného práva.

### Free Zones
Špeciálne ekonomické zóny s vlastnými právnymi rámcami (DIFC, ADGM, DMCC, atď.)

### Foreign Investment
Progresívne zákony podporujúce zahraničné investície a 100% vlastníctvo pre cudzincov v určitých sektoroch.

## Právne jazyky

### Arabčina
Oficiálny jazyk všetkých právnych dokumentov.

### Angličtina
Široko používaná v obchodnom práve a vo free zones.

## Právne zastúpenie

### Advocates & Legal Consultants
- UAE národní advokáti
- Zahraniční právni konzultanti
- In-house legal counsel

### Licensing
Praktizovanie práva vyžaduje licenciu od príslušného emirátu alebo free zone.

## Zdroje práva

### Primárne zdroje
1. Ústava UAE
2. Federálne zákony
3. Emirátne zákony
4. Islamské právo (Sharia)

### Sekundárne zdroje
1. Súdne precedensy
2. Legal doctrine
3. Právna literatúra

## Aktuálne trendy

### Modernizácia
Kontinuálna modernizácia právneho systému v súlade s globálnymi štandardami.

### Digitalizácia
E-government a digitálne právne služby.

### Transparency
Zvyšovanie transparentnosti a prístupnosti právnych informácií.

## Dôležité poznámky

### Legal Advice Disclaimer
Tento dokument poskytuje všeobecný prehľad a nepredstavuje právne poradenstvo. Pre špecifické právne otázky konzultujte licencovaného právnika.

### Updates
Právny systém UAE sa neustále vyvíja. Vždy overujte aktuálnosť právnych informácií.

## Ďalšie zdroje

### Oficiálne portály
- UAE Government Portal
- Federal National Council
- Dubai Courts
- Abu Dhabi Judicial Department

### Legal Databases
- UAE Official Gazette
- Legislation website
- Court judgments databases

---

**Poznámka:** Tento dokument slúži ako úvod do UAE právneho systému. Pre detailné informácie o konkrétnych zákonoch a rozhodnutiach konzultujte príslušné dokumenty v tomto repozitári.
"""

    if create_file(tenant_root / "uae_legal_system_overview.md", intro_doc):
        print_success("Vytvorený: uae_legal_system_overview.md")

    # 5. Aktualizácia .env konfigurácie
    print_header("5. Aktualizácia .env konfigurácie")
    if update_env_file(env_file):
        print_success("Úspešne aktualizovaný .env súbor")

    # 6. Záverečný report
    print_header("SETUP DOKONČENÝ")

    print_success("UAE tenant bol úspešne vytvorený!")
    print()
    print_info("Vytvorená štruktúra:")
    print(f"  📁 {tenant_root.relative_to(project_root)}/")
    print(f"     📄 README.md")
    print(f"     📄 uae_legal_system_overview.md")
    print(f"     📁 federal_laws/")
    print(f"        📄 README.md")
    print(f"     📁 emirate_laws/")
    print(f"        📄 README.md")
    print(f"     📁 court_decisions/")
    print(f"        📄 README.md")
    print(f"     📁 legal_procedures/")
    print(f"        📄 README.md")
    print()
    print_info(f"Aktualizovaný: {env_file.relative_to(project_root)}")
    print(f"  TENANTS=icc,andros,uae")
    print()

    print_header("ĎALŠIE KROKY")
    print()
    print("1️⃣  Reštartujte NexBrain služby:")
    print(f"    cd {project_root / 'apps' / 'nex-brain'}")
    print("    docker-compose restart")
    print()
    print("2️⃣  Pridajte prvé dokumenty:")
    print(f"    - Umiestnite .md alebo .pdf súbory do {tenant_root / 'federal_laws'}")
    print()
    print("3️⃣  Indexujte nové dokumenty:")
    print("    python tools/rag/rag_update.py --new")
    print()
    print("4️⃣  Testujte RAG vyhľadávanie:")
    print("    curl 'https://rag-api.icc.sk/search?query=test&tenant=uae&limit=5'")
    print()
    print("5️⃣  Skontrolujte štatistiky:")
    print("    python tools/rag/rag_update.py --stats")
    print()

    print_header("DOKUMENTÁCIA")
    print()
    print(f"📖 Hlavný README: {tenant_root / 'README.md'}")
    print(f"📖 Úvodný dokument: {tenant_root / 'uae_legal_system_overview.md'}")
    print()

    print_success("Setup dokončený úspešne! ✨")
    print()


if __name__ == "__main__":
    main()