# NEX Genesis - Overview

## Popis systému

NEX Genesis je komplexný podnikový informačný systém vyvíjaný od roku 1995 v Delphi (aktuálne Delphi 6/7). Pokrýva kompletné firemné procesy od nákupu, skladovej evidencie, predaja až po účtovníctvo.

## Technické parametre

| Parameter | Hodnota |
|-----------|---------|
| **Jazyk** | Object Pascal (Delphi 6/7) |
| **Databáza** | Pervasive Btrieve / PSQL |
| **Platforma** | Windows 32-bit |
| **Zdrojový kód** | 1,000,000+ riadkov |
| **Pascal súbory (.pas)** | 4,277 |
| **Form súbory (.dfm)** | 2,036 |
| **Tabuľkové definície (.bdf)** | 678 |

## Hlavné moduly

| Modul | Prefix | Popis |
|-------|--------|-------|
| **GSC** | Gsc_* | Katalóg produktov (evidencia tovaru) |
| **STK** | Stk_* | Skladová evidencia |
| **PLS** | Pls_* | Predajné cenníky |
| **PAB** | Pab_* | Obchodní partneri |
| **TSH/TSI** | Ts*_* | Dodacie listy (hlavičky/položky) |
| **ICH/ICI** | Ic*_* | Odberateľské faktúry |
| **ISH/ISI** | Is*_* | Dodávateľské faktúry |
| **CAS** | Cas_* | Pokladňa |
| **ACC** | Acc_* | Účtovníctvo |
| **FXB** | Fxb_* | Majetok |

## Migrácia do NEX Automat

NEX Genesis sa migruje do modernej platformy **NEX Automat**:

| Aspekt | NEX Genesis | NEX Automat |
|--------|-------------|-------------|
| Jazyk | Delphi/Pascal | Python 3.11+ |
| Databáza | Btrieve | PostgreSQL |
| Desktop UI | VCL | PySide6 |
| Web UI | - | React + Vite |
| API | - | FastAPI |
| Workflow | - | Temporal.io |

## Kódovanie textu

NEX Genesis používa **Kamenický (KEYBCS2)** kódovanie pre české a slovenské znaky. Toto je DOS-era kódovanie z rokov 1985-1995.

Pri migrácii je potrebná konverzia:
- KEYBCS2 → UTF-8
- Implementované v `packages/nexdata/nexdata/utils/encoding.py`

## Štruktúra dokumentácie

```
docs/knowledge/nex-genesis/
├── 00-overview.md          # Tento súbor
├── 01-project-structure.md # Štruktúra projektu
├── modules/                # Dokumentácia modulov
│   └── gsc-katalog-produktov.md
├── tables/                 # Dokumentácia tabuliek
│   ├── gscat.md
│   ├── barcode.md
│   └── ...
└── methodology/            # Metodika analýzy
    └── analysis-template.md
```

## Súvisiace zdroje

- Zdrojový kód: `C:\Development\nex-genesis\`
- BDF definície: `C:\Development\nex-genesis\DefFiles\`
- NEX Automat repo: `C:\Development\nex-automat\`
- Btrieve modely: `packages/nexdata/nexdata/models/`
