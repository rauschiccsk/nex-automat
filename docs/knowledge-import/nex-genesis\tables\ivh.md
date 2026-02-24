# IVH - Hlavičky inventúrnych dokladov

## Kľúčové slová / Aliases

IVH, IVH.BTR, inventúry hlavičky, inventory header, inventarizácia, inventár

## Popis

Hlavičky inventúrnych dokladov. Každý doklad reprezentuje jednu inventúru (čiastočnú alebo úplnú) pre konkrétny sklad.

## Btrieve súbor

`IVHyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARyy\STK\IVHyynnn.BTR`

## Štruktúra polí (32 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | word | 2 | Číslo skladu - **FK** |
| SerNum | longint | 4 | Poradové číslo dokladu |
| DocNum | Str12 | 13 | Interné číslo dokladu - **PRIMARY KEY** |
| Year | Str2 | 3 | Rok dokladu |

### Údaje inventúry

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Describe | Str30 | 31 | Popis inventúry |
| DocDate | DateType | 4 | Dátum inventúry |
| InvType | Str1 | 2 | Typ inventúry (U=úplná, C=čiastočná) |

### Stav dokladu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DstStk | Str1 | 2 | Stav inventúry (N=otvorená, S=uzatvorená) |
| DstLck | byte | 1 | Príznak uzamknutia |
| SndStat | Str1 | 2 | Stav internetového prenosu |
| Sended | byte | 1 | Príznak odoslania (0=zmenený, 1=odoslaný) |

### Prepojenie na vyrovnávacie doklady

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OmbDocNum | Str12 | 13 | Číslo výdajky (manká) |
| ImbDocNum | Str12 | 13 | Číslo príjemky (prebytky) |

### Štatistiky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ItmQnt | word | 2 | Počet položiek inventúry |
| DifQnt | word | 2 | Počet položiek s rozdielom |
| MnkQnt | word | 2 | Počet položiek s mankom |
| PrbQnt | word | 2 | Počet položiek s prebytkom |

### Hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AccVal | double | 8 | Celková účtovná hodnota |
| RealVal | double | 8 | Celková skutočná hodnota |
| DifVal | double | 8 | Hodnota rozdielu |
| MnkVal | double | 8 | Hodnota mánk |
| PrbVal | double | 8 | Hodnota prebytkov |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (8)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | Year, SerNum | YearSerNum | Unikátny |
| 1 | StkNum, SerNum | StSn | Duplicit |
| 2 | DocNum | DocNum | Duplicit |
| 3 | DocDate | DocDate | Duplicit |
| 4 | DstStk | DstStk | Duplicit |
| 5 | Sended | Sended | Duplicit |
| 6 | OmbDocNum | OmbDocNum | Duplicit |
| 7 | ImbDocNum | ImbDocNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| StkNum | STKLST.StkNum | Sklad |
| OmbDocNum | OMH.DocNum | Výdajka (manká) |
| ImbDocNum | IMH.DocNum | Príjemka (prebytky) |

## Použitie

- Evidencia inventúrnych operácií
- Sledovanie stavu inventúry
- Prepojenie na vyrovnávacie doklady
- Farebné rozlíšenie otvorených inventúr

## Business pravidlá

- DstStk='N' = otvorená inventúra (červená farba)
- DstStk='S' = uzatvorená inventúra
- InvType='U' = úplná inventúra celého skladu
- InvType='C' = čiastočná inventúra vybraných položiek
- Po uzatvorení sa aktualizuje STK.InvDate
- OmbDocNum obsahuje číslo vygenerovanej výdajky pre manká
- ImbDocNum obsahuje číslo vygenerovanej príjemky pre prebytky

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
