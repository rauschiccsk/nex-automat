# NXBDEF - Centrálny register kníh NEX

## Kľúčové slová / Aliases

NXBDEF, NXBDEF.BTR, centrálny, register, kníh, nex

## Popis

Centrálna tabuľka definícií všetkých kníh v systéme NEX Genesis. Obsahuje základné informácie o každej knihe bez ohľadu na typ modulu. Slúži ako spoločný register pre všetky knižné moduly.

## Btrieve súbor

`NXBDEF.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\NXBDEF.BTR`

## Štruktúra polí (13 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PmdMark | Str3 | 4 | Typové označenie programového modulu |
| BookNum | Str5 | 6 | Číslo knihy |
| BookName | Str30 | 31 | Názov knihy |
| BookType | Str1 | 2 | Typ knihy |
| Reserved | Str2 | 3 | Rezervované (pôvodne BookYear) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | PmdMark | PmdMark | Duplicit |
| 1 | PmdMark, BookNum | PmBn | Duplicit |

## Programové moduly (PmdMark)

| Mark | Modul | Popis |
|------|-------|-------|
| OFB | ICB | Odberateľské faktúry |
| DFB | ISB | Dodávateľské faktúry |
| PQB | PQB | Prevodné príkazy |
| SOB | BSM | Bankové výpisy |
| SVB | SVB | Faktúry zálohových platieb |
| CSB | CSB | Pokladne |
| STK | STK | Sklady |
| CMB | CMB | Kompletizácia |
| IVD | IVD | Inventarizácia |
| IDB | IDB | Interné doklady |
| DLB | DLB | Dodacie listy |

## Typy kníh (BookType)

| Hodnota | Popis |
|---------|-------|
| (prázdne) | Štandardná kniha |
| A | Archívna kniha |
| S | Systémová kniha |

## Použitie

- Centrálny register všetkých kníh
- Kontrola duplicitných čísel kníh
- Základ pre výber kníh v moduloch
- Audit vytvorenia a modifikácie kníh

## Business pravidlá

- PmdMark + BookNum je unikátna kombinácia
- Každý modul má vlastnú *LST tabuľku s detailmi
- NXBDEF obsahuje len základné metadáta
- Pri mazaní knihy sa vymaže aj záznam z NXBDEF

## Vzťah k špecifickým tabuľkám

| NXBDEF | Špecifická tabuľka |
|--------|-------------------|
| PmdMark='OFB' | ICBLST |
| PmdMark='DFB' | ISBLST |
| PmdMark='SVB' | SVBLST |
| PmdMark='SOB' | PQBLST |
| PmdMark='CSB' | CSBLST |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
