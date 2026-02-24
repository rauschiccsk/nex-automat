# OCC - Obchodné zmluvy k zákazkám

## Kľúčové slová / Aliases

OCC, OCC.BTR, objednávky potvrdenia, order confirmations, potvrdené objednávky

## Popis

Tabuľka obchodných zmlúv prepojených so zákazkami. Obsahuje údaje o zmluvných podmienkach, termínoch a hodnotách.

## Btrieve súbor

`OCCyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OCCyynnn.BTR`

## Štruktúra polí (36 polí)

### Identifikácia zmluvy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Číslo zákazky - **FK → OCH.DocNum** |
| ConNum | Str12 | 13 | Číslo zmluvy |
| ConDate | DateType | 4 | Dátum zmluvy |
| ConType | Str1 | 2 | Typ zmluvy |

### Partner

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Kód partnera |
| PaName | Str30 | 31 | Názov partnera |
| _PaName | Str30 | 31 | Vyhľadávacie pole |

### Platnosť

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ValidFrom | DateType | 4 | Platnosť od |
| ValidTo | DateType | 4 | Platnosť do |
| Status | Str1 | 2 | Stav zmluvy |

### Hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AcDvzName | Str3 | 4 | Účtovná mena |
| AcValue | double | 8 | Hodnota v účtovnej mene |
| FgDvzName | Str3 | 4 | Cudzí mena |
| FgValue | double | 8 | Hodnota v cudzej mene |
| FgCourse | double | 8 | Kurz |

### Podmienky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayCode | Str3 | 4 | Forma úhrady |
| PayDays | word | 2 | Splatnosť v dňoch |
| DscPrc | double | 8 | Zľava % |
| DepPrc | double | 8 | Záloha % |

### Poznámky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Note1 | Str100 | 101 | Poznámka 1 |
| Note2 | Str100 | 101 | Poznámka 2 |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (3)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum | DocNum | Case-insensitive, Duplicit |
| 1 | ConNum | ConNum | Case-insensitive, Duplicit |
| 2 | _PaName | PaName | Case-insensitive, Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | OCH.DocNum | Hlavička zákazky |
| PaCode | PAB.PaCode | Partner |

## Typy zmlúv

| Hodnota | Popis |
|---------|-------|
| R | Rámcová zmluva |
| K | Kúpna zmluva |
| D | Zmluva o dielo |
| S | Servisná zmluva |

## Stavy zmluvy

| Hodnota | Popis |
|---------|-------|
| A | Aktívna |
| E | Expirovaná |
| C | Zrušená |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
