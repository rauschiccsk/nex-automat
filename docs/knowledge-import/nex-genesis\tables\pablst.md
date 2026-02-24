# PABLST - Zoznam kníh partnerov

## Kľúčové slová / Aliases

PABLST, PABLST.BTR, zoznam kníh partnerov, partner books list, evidencia partnerov

## Popis

Tabuľka zoznamu kníh obchodných partnerov. Umožňuje organizovať partnerov do viacerých samostatných kníh (napr. dodávatelia, odberatelia, interné).

## Btrieve súbor

`PABLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\FIRMS\PABLST.BTR`

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | word | 2 | Číslo knihy partnerov - **PRIMARY KEY** |
| BookName | Str30 | 31 | Názov knihy partnerov |
| SrchHole | byte | 1 | Hľadať prázdne poradové čísla (0=nasledujúce, 1=hľadať medzery) |
| Shared | byte | 1 | Zdieľanie cez FTP (1=zdieľaný) |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BookNum | BookNum | Duplicit |

## Multi-book architektúra

Systém podporuje viacero kníh partnerov:

```
PABLST.BTR          → Zoznam kníh
├── BookNum=1       → PAB00001.BTR (napr. "Dodávatelia")
├── BookNum=2       → PAB00002.BTR (napr. "Odberatelia")
└── BookNum=3       → PAB00003.BTR (napr. "Interné")
```

## Príklad použitia

Typická konfigurácia:

| BookNum | BookName | Popis |
|---------|----------|-------|
| 1 | Dodávatelia | Všetci dodávatelia |
| 2 | Odberatelia | Všetci odberatelia |
| 3 | Interné | Vlastné firmy, pobočky |

## Business pravidlá

- Číslo knihy (BookNum) určuje názov súboru PABxxxxx.BTR
- SrchHole=1 umožňuje znovupoužitie vymazaných PaCode
- Shared=1 synchronizuje zmeny cez FTP na pobočky

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
