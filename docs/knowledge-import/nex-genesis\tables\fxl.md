# FXL - Účtovné odpisy investičného majetku

## Kľúčové slová / Aliases

FXL, FXL.BTR, účtovné, odpisy, investičného, majetku

## Popis

Tabuľka mesačných účtovných odpisov dlhodobého majetku. Obsahuje odpisový plán s mesačným rozpisom a zostatkovými cenami. Každá kniha majetku má vlastný súbor.

## Btrieve súbor

`FXLyynnn.BTR` (yy=rok, nnn=číslo knihy z FXBLST)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\FXLyynnn.BTR`

## Štruktúra polí (21 polí)

### Identifikácia obdobia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Year | word | 2 | Rok účtovného odpisu |
| Mounth | byte | 1 | Mesiac účtovného odpisu (1-12) |

### Identifikácia majetku

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo karty majetku - **FK FXA** |
| WriNum | word | 2 | Číslo prevádzkové jednotky |
| FxaGrp | longint | 4 | Číslo účtovnej skupiny |

### Hodnoty odpisu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BegVal | double | 8 | Vstupná hodnota na začiatku obdobia |
| ChgVal | double | 8 | Kumulatívna hodnota tech. zhodnotení v danom roku |
| ModVal | double | 8 | Kumulatívna hodnota korekcií v danom roku |
| SuPrc | double | 8 | Odpisová sadzba |
| SuVal | double | 8 | Hodnota mesačného účtovného odpisu |
| EndVal | double | 8 | Zostatková cena na konci obdobia |

### Stav

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Status | Str1 | 2 | Príznak (N=riadny, M=modifikovaný) |
| AccDoc | Str12 | 13 | Číslo účtovného dokladu |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtName | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (5)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | Year | Year | Duplicit |
| 1 | Year, Mounth | YeMo | Duplicit |
| 2 | DocNum | DocNum | Duplicit |
| 3 | Year, Mounth, DocNum | YeMoDo | Duplicit |
| 4 | DocNum, Year, Mounth | DoYeMo | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | FXA.DocNum | Evidenčná karta majetku |
| WriNum | WRILST.WriNum | Prevádzková jednotka |
| FxaGrp | FXAGRP.GrpNum | Účtovná skupina |

## Výpočtové pravidlá

### Mesačný odpis

```
SuVal = (BegVal + ChgVal - ModVal) × SuPrc / 100 / 12
```

### Zostatková cena

```
EndVal = BegVal + ChgVal - ModVal - SuVal
```

### Prepojenie mesiacov

```
BegVal[n+1] = EndVal[n]
```

## Rozdiel FXL vs FXT

| Vlastnosť | FXL (Účtovné) | FXT (Daňové) |
|-----------|---------------|--------------|
| Frekvencia | Mesačne | Ročne |
| Pole Mounth | Áno | Nie |
| Základ | Vlastná sadzba | Zákonná sadzba |
| Účel | Účtovníctvo | Daňové priznanie |

## Status odpisu

| Hodnota | Význam | Popis |
|---------|--------|-------|
| N | Normálny | Štandardný vypočítaný odpis |
| M | Modifikovaný | Manuálne upravený odpis |

## Použitie

- Evidencia účtovných odpisov majetku
- Mesačné účtovanie odpisov
- Výpočet účtovnej zostatkovej ceny
- Tlač odpisového plánu

## Business pravidlá

- Mesačné odpisy sa vytvárajú od BegDate majetku
- Odpisy končia keď EndVal = 0 alebo pri vyradení
- Status='M' označuje manuálne upravené odpisy
- AccDoc obsahuje číslo zaúčtovaného dokladu

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
