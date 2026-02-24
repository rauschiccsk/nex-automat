# OSRHIS - História zmien termínov dodávok

## Kľúčové slová / Aliases

OSRHIS, OSRHIS.BTR, história nákupných objednávok, PO history

## Popis

Tabuľka histórie zmien termínov dodávok od dodávateľov. Sleduje všetky zmeny termínov pre jednotlivé položky objednávok.

## Btrieve súbor

`OSRHIS.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OSRHIS.BTR`

## Štruktúra polí (19 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Číslo objednávky - **FK → OSHLST.DocNum** |
| ItmNum | word | 2 | Poradové číslo položky |
| ProNum | longint | 4 | Produktové číslo |
| ProNam | Str60 | 61 | Názov produktu |
| _ProNam | Str60 | 61 | Vyhľadávacie pole |

### Termíny

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RatPrv | DateType | 4 | Predchádzajúci termín dodávky |
| RatDte | DateType | 4 | Aktuálny termín dodávky |
| RatNot | Str50 | 51 | Poznámka k termínu |
| RatChg | byte | 1 | Číslo zmeny termínu |

### Vytvorenie záznamu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtDte | DateType | 4 | Dátum vyhotovenia záznamu |
| CrtTim | TimeType | 4 | Čas vyhotovenia záznamu |

### Notifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SndSta | Str1 | 2 | Stav odoslania upozornenia |

### Akceptácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AcpSta | Str1 | 2 | Stav akceptácie |
| AcpUsr | Str15 | 16 | Používateľ akceptácie |
| AcpUsn | Str30 | 31 | Meno akceptujúceho |
| AcpDte | DateType | 4 | Dátum akceptácie |
| AcpTim | TimeType | 4 | Čas akceptácie |

## Indexy (7)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum | DocNum | Duplicit |
| 1 | DocNum, ItmNum | DoIt | Duplicit |
| 2 | DocNum, AcpSta | DnAs | Duplicit |
| 3 | ProNum | ProNum | Duplicit |
| 4 | _ProNam | ProNam | Duplicit |
| 5 | SndSta | SndSta | Duplicit |
| 6 | AcpSta | AcpSta | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | OSHLST.DocNum | Hlavička objednávky |
| ProNum | GSCAT.GsCode | Tovar |

## Stav odoslania (SndSta)

| Hodnota | Popis |
|---------|-------|
| W | Čaká na odoslanie |
| S | Odoslané upozornenie |

## Stav akceptácie (AcpSta)

| Hodnota | Popis |
|---------|-------|
| (prázdne) | Neakceptované |
| A | Akceptované |

## Workflow

```
1. Dodávateľ oznámi zmenu termínu
   ↓
2. Import zmeny do systému
   ↓
3. Zápis do OSRHIS (RatChg sa inkrementuje)
   ↓
4. Označenie OSHLST.DstRat = 'R'
   ↓
5. Notifikácia zodpovedných osôb (SndSta = 'W' → 'S')
   ↓
6. Akceptácia zmeny používateľom (AcpSta = 'A')
```

## Použitie

- Sledovanie zmien termínov dodávok
- Audit zmien od dodávateľov
- Analýza spoľahlivosti dodávateľov
- Notifikácie zodpovedných osôb

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
