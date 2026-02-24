# JOURNAL - Denník účtovných zápisov

## Kľúčové slová / Aliases

JOURNAL, JOURNAL.BTR, denník, účtovných, zápisov

## Popis

Hlavná tabuľka účtovného denníka. Obsahuje všetky účtovné zápisy zo všetkých modulov systému. Každý riadok reprezentuje jeden účtovný pohyb na strane Má dať alebo Dal.

## Btrieve súbor

`JOURNAL.BTR`

## Umiestnenie

`C:\NEX\YEARyy\DOCS\JOURNAL.BTR`

## Štruktúra polí (29 polí)

### Identifikácia zápisu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo rozúčtovaného dokladu |
| ItmNum | word | 2 | Riadok rozúčtovaného dokladu |
| ExtNum | Str12 | 13 | Externé číslo rozúčtovaného dokladu |

### Účtovné údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AccSnt | Str3 | 4 | Syntetická časť účtu (napr. 321) |
| AccAnl | Str6 | 7 | Analytická časť účtu (napr. 001) |
| CredVal | double | 8 | Hodnota strany Má dať (MD) |
| DebVal | double | 8 | Hodnota strany Dal (D) |
| Describe | Str30 | 31 | Popis účtovného zápisu |
| _Describe | Str30 | 31 | Vyhľadávacie pole popisu |

### Dátumové údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocDate | DateType | 4 | Dátum rozúčtovaného dokladu |

### Organizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WriNum | word | 2 | Číslo prevádzkovej jednotky |
| CentNum | word | 2 | Číslo hospodárskeho strediska |
| StkNum | word | 2 | Číslo skladu |

### Partner a zákazka

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Číselný kód partnera |
| SpaCode | longint | 4 | Číselný kód príjemcu tovaru |
| OcdNum | Str12 | 13 | Interné číslo zákazkového dokladu |
| OceNum | Str12 | 13 | Externé číslo zákazkového dokladu |

### Prepojenia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ConDoc | Str12 | 13 | Číslo pripojeného dokladu (DL-FA) |
| SmCode | word | 2 | Kód skladového pohybu |
| BegRec | byte | 1 | Príznak počiatočného stavu (1=poč.stav, 0=riadny ÚZ) |

### Cudzia mena

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FgCourse | double | 8 | Kurz vyúčtovacej meny |
| FgCrdVal | double | 8 | Hodnota strany MD - vyúčtovacia mena |
| FgDebVal | double | 8 | Hodnota strany Dal - vyúčtovacia mena |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtName | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (9)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum | DocNum | Duplicit, Case-insensitive |
| 1 | ExtNum | ExtNum | Duplicit, Case-insensitive |
| 2 | DocDate | DocDate | Duplicit |
| 3 | AccSnt, AccAnl | SnAn | Duplicit |
| 4 | DocNum, WriNum, AccSnt, AccAnl | DoWrSnAn | Duplicit |
| 5 | DocNum, ItmNum | DoIt | Duplicit |
| 6 | _Describe | Describe | Duplicit |
| 7 | CredVal | CredVal | Duplicit |
| 8 | DebVal | DebVal | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| AccSnt | ACCSNT.AccSnt | Syntetický účet |
| AccSnt+AccAnl | ACCANL.AccSnt+AccAnl | Analytický účet |
| PaCode | PAB.PaCode | Obchodný partner |
| WriNum | WRILST.WriNum | Prevádzkové stredisko |
| CentNum | ECUNIT.CentNum | Hospodárske stredisko |
| StkNum | STKLST.StkNum | Sklad |
| SmCode | SMLST.SmCode | Skladový pohyb |

## Použitie

- Centrálna evidencia účtovných zápisov
- Hlavná kniha
- Výkazy obratov a zostatkov
- Podklad pre súvahu a výsledovku
- Audit účtovných operácií

## Business pravidlá

- Jeden doklad = viacej zápisov (MD a Dal musia byť v rovnováhe)
- DocNum obsahuje identifikátor zdrojového dokladu (ISH, ICH, CSH, BSM...)
- CredVal > 0 XOR DebVal > 0 (jeden zápis = jedna strana)
- Suma CredVal = suma DebVal pre skupinu zápisov z jedného dokladu
- BegRec=1 označuje počiatočný stav účtu

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
