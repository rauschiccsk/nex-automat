# IDI - Položky interných účtovných dokladov

## Kľúčové slová / Aliases

IDI, IDI.BTR, položky, interných, účtovných, dokladov

## Popis

Položková tabuľka interných účtovných dokladov. Každá položka predstavuje jeden účtovný zápis s účtom a hodnotou na strane MD alebo Dal.

## Btrieve súbor

`IDIyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\IDIyynnn.BTR`

## Štruktúra polí (35 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo dokladu - **FK → IDH.DocNum** |
| ItmNum | word | 2 | Poradové číslo položky |
| DocDate | DateType | 4 | Dátum účtovného dokladu |
| DocType | byte | 1 | Typ dokladu (0=bežný, 1=otvorenie, 2=uzatvorenie) |

### Prevádzkové údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WriNum | word | 2 | Číslo prevádzkovej jednotky |

### Súvzťažný doklad

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ConDoc | Str12 | 13 | Odkaz na súvzťažný doklad - interné číslo |
| ConExt | Str12 | 13 | Odkaz na súvzťažný doklad - externé číslo |

### Účtovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AccSnt | Str3 | 4 | Syntetický účet |
| AccAnl | Str6 | 7 | Analytický účet |
| Describe | Str30 | 31 | Textový popis položky |

### Partner

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Číselný kód firmy |

### Hodnoty v účtovnej mene

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CredVal | double | 8 | Hodnota strany MD |
| DebVal | double | 8 | Hodnota strany Dal |

### DPH

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc | byte | 1 | Sadzba DPH (%) |
| AcAValue | double | 8 | Hodnota bez DPH |
| AcVatVal | double | 8 | Hodnota DPH |
| AcBValue | double | 8 | Hodnota s DPH |

### Cudzia mena (pre kurzové rozdiely)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FgDvzName | Str3 | 4 | Mena faktúry |
| FgCourse | double | 8 | Kurz medzi ÚM a FM zo dňa úhrady |
| FgPayVal | double | 8 | Hodnota úhrady v mene faktúry |
| FgCrdVal | double | 8 | Hodnota strany MD - vyúčtovacia mena |
| FgDebVal | double | 8 | Hodnota strany Dal - vyúčtovacia mena |

### Platba v zahraničnej mene

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PyCourse | double | 8 | Kurz zahraničnej meny |
| PyPayVal | double | 8 | Uhradená čiastka v zahraničnej mene |

### Stav

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Status | Str1 | 2 | Stav riadku |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |
| ModNum | longint | 4 | Počítadlo modifikácií |

## Indexy (6)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum | DoIt | Duplicit |
| 1 | ItmNum | ItmNum | Duplicit |
| 2 | DocNum | DocNum | Duplicit |
| 3 | DocDate | DocDate | Duplicit |
| 4 | AccSnt, AccAnl | SntAnl | Duplicit |
| 5 | PaCode | PaCode | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | IDH.DocNum | Hlavička dokladu |
| AccSnt+AccAnl | ACCLST | Účet |
| PaCode | PAB.PaCode | Partner |
| ConDoc | rôzne doklady | Súvzťažný doklad |

## Použitie

- Jednotlivé účtovné zápisy
- Kurzové rozdiely (Fg* polia)
- Zápočty (ConDoc referencie)
- Analytické členenie

## Business pravidlá

- Každá položka má buď CredVal ALEBO DebVal (nie oboje)
- CredVal = strana Má dať
- DebVal = strana Dal
- Suma CredVal všetkých položiek = suma DebVal
- FgDvzName, FgCourse používané pri kurzových rozdieloch
- ConDoc odkazuje na pôvodný doklad pri zápočtoch

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
