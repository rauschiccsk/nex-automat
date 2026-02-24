# CSI - Položky hotovostných pokladničných dokladov

## Kľúčové slová / Aliases

CSI, CSI.BTR, položky, hotovostných, pokladničných, dokladov

## Popis

Položková tabuľka hotovostných pokladničných dokladov. Obsahuje jednotlivé položky príjmov a výdajov vrátane prepojenia na faktúry, kurzových rozdielov a predkontácií.

## Btrieve súbor

`CSIyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\CSIyynnn.BTR`

## Štruktúra polí (47 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo dokladu - **FK → CSH.DocNum** |
| ItmNum | word | 2 | Poradové číslo položky |
| DocDate | DateType | 4 | Dátum dokladu |
| DocType | Str1 | 2 | Typ dokladu (I=príjem, E=výdaj) |

### Popis

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Describe | Str30 | 31 | Popis úhrady |

### Prevádzkové údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WriNum | word | 2 | Číslo prevádzkovej jednotky |
| CentNum | word | 2 | Číslo hospodárskeho strediska |

### Partner

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Číselný kód partnera |

### Vodič

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DrvCode | word | 2 | Kód vodiča |
| DrvName | Str30 | 31 | Meno a priezvisko vodiča |
| CarMark | Str10 | 11 | ŠPZ vozidla |
| OcdNum | Str12 | 13 | Číslo objednávky |

### DPH

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc | byte | 1 | Sadzba DPH (%) |

### Hodnoty v pokladničnej mene (Py*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PyDvzName | Str3 | 4 | Mena pokladne |
| PyCourse | double | 8 | Kurz medzi ÚM a PM |
| PyAValue | double | 8 | Hodnota bez DPH |
| PyBValue | double | 8 | Hodnota s DPH |
| PyPdfVal | double | 8 | Rozdiel úhrady v PM |

### Hodnoty v účtovnej mene (Ac*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AcDvzName | Str3 | 4 | Účtovná mena |
| AcAValue | double | 8 | Hodnota bez DPH |
| AcBValue | double | 8 | Hodnota s DPH |
| AcCrdVal | double | 8 | Hodnota kurzového rozdielu |
| AcPdfVal | double | 8 | Rozdiel úhrady v ÚM |

### Hodnoty v mene faktúry (Fg*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FgDvzName | Str3 | 4 | Mena faktúry |
| FgCourse | double | 8 | Kurz medzi ÚM a FM |
| FgPayVal | double | 8 | Hodnota úhrady v mene faktúry |

### Prepojený doklad

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ConDoc | Str12 | 13 | Interné číslo prepojeného dokladu |
| ConExt | Str12 | 13 | Externé číslo prepojeného dokladu |

### Účtovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AccSnt | Str3 | 4 | Syntetický účet pre rozúčtovanie |
| AccAnl | Str6 | 7 | Analytický účet pre rozúčtovanie |
| CrdSnt | Str3 | 4 | Syntetický účet kurzového rozdielu |
| CrdAnl | Str6 | 7 | Analytický účet kurzového rozdielu |
| PdfSnt | Str3 | 4 | Syntetický účet cenového rozdielu |
| PdfAnl | Str6 | 7 | Analytický účet cenového rozdielu |

### Vylúčené hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ExcCosPrc | double | 8 | % vylúčenej čiastky z nákladov |
| ExcCosVal | double | 8 | Hodnota vylúčenej čiastky z nákladov |
| ExcVatPrc | double | 8 | % vylúčenej čiastky z DPH |
| ExcVatVal | double | 8 | Hodnota vylúčenej čiastky z DPH |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |
| ModNum | word | 2 | Počítadlo modifikácií |

## Indexy (7)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum | DoIt | Duplicit |
| 1 | DocNum | DocNum | Duplicit, Case insensitive |
| 2 | ConDoc | ConDoc | Duplicit, Case insensitive |
| 3 | ItmNum | ItmNum | Duplicit |
| 4 | PaCode | PaCode | Duplicit |
| 5 | DrvCode | DrvCode | Duplicit |
| 6 | CarMark | CarMark | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | CSH.DocNum | Hlavička dokladu |
| ConDoc | ICD/ISD.DocNum | Prepojená faktúra |
| PaCode | PAB.PaCode | Partner |
| AccSnt+AccAnl | ACCLST | Účet |
| DrvCode | DRVLST.DrvCode | Vodič |

## Použitie

- Položky pokladničných dokladov
- Úhrady faktúr (ConDoc)
- Kurzové rozdiely (AcCrdVal)
- Predkontácie (AccSnt/AccAnl)

## Business pravidlá

- ConDoc prepája položku na faktúru (ICD/ISD)
- FgPayVal = úhrada v mene faktúry
- AcCrdVal = kurzový rozdiel vzniknutý pri úhrade
- ExcCosVal/ExcVatVal pre vylúčené čiastky z DPH

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
