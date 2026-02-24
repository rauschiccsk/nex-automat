# ACCANLC - Obratová predvaha podľa stredísk

## Kľúčové slová / Aliases

ACCANLC, ACCANLC.BTR, obratová, predvaha, podľa, stredísk

## Popis

Analytické účty s mesačnými obratmi rozčlenené podľa hospodárskych stredísk a prevádzkových jednotiek. Umožňuje sledovanie nákladov a výnosov po strediskách.

## Btrieve súbor

`ACCANLC.BTR`

## Umiestnenie

`C:\NEX\YEARyy\DOCS\ACCANLC.BTR`

## Štruktúra polí (45 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CentNum | word | 2 | Číslo hospodárskeho strediska |
| WriNum | word | 2 | Číslo prevádzkovej jednotky |
| AccSnt | Str3 | 4 | Syntetická časť účtu |
| AccAnl | Str6 | 7 | Analytická časť účtu |
| AnlName | Str30 | 31 | Názov analytického účtu |
| _AnlName | Str30 | 31 | Vyhľadávacie pole názvu |

### Počiatočné a konečné stavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CBegVal | double | 8 | Počiatočný stav - MD |
| DBegVal | double | 8 | Počiatočný stav - Dal |
| CTurnVal | double | 8 | Celkový obrat - MD |
| DTurnVal | double | 8 | Celkový obrat - Dal |
| CEndVal | double | 8 | Konečný stav - MD |
| DEndVal | double | 8 | Konečný stav - Dal |
| DiffVal | double | 8 | Konečný zostatok |

### Mesačné obraty - MD (CTurn01-12)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CTurn01-12 | double | 8×12 | Obraty za mesiace 01-12 - MD |

### Mesačné obraty - Dal (DTurn01-12)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DTurn01-12 | double | 8×12 | Obraty za mesiace 01-12 - Dal |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtName | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (3)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | CentNum, WriNum, AccSnt, AccAnl | CeWrAsAn | Duplicit |
| 1 | AccSnt, AccAnl | SntAnl | Duplicit |
| 2 | _AnlName | AnlName | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| AccSnt, AccAnl | ACCANL.AccSnt, AccAnl | Analytický účet |
| CentNum | ECUNIT.CentNum | Hospodárske stredisko |
| WriNum | WRILST.WriNum | Prevádzková jednotka |

## Použitie

- Sledovanie nákladov a výnosov po strediskách
- Controlling
- Porovnanie prevádzok
- Mesačné reporty po strediskách

## Business pravidlá

- Záznam sa vytvára pre kombináciu CentNum + WriNum + AccSnt + AccAnl
- Obraty sa aktualizujú z JOURNAL zápisov
- Umožňuje detailnú analýzu po organizačnej štruktúre

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
