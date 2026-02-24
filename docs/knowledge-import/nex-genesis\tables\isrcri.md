# ISRCRI - Položky koncoročného prekurzovania DF

## Kľúčové slová / Aliases

ISRCRI, ISRCRI.BTR, reklamácie položky, claims items, reklamované položky

## Popis

Položková tabuľka koncoročného prekurzovania dodávateľských faktúr. Obsahuje detailné údaje o každej faktúre s kurzovým rozdielom.

## Btrieve súbor

`ISRCRI.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ISRCRI.BTR`

## Polia (26)

### Identifikácia faktúry

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo faktúry - **PRIMARY KEY** |
| ExtNum | Str12 | 13 | Variabilný symbol |
| DvzName | Str3 | 4 | Mena faktúry |

### Dodávateľ

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Číselný kód dodávateľa |
| PaName | Str30 | 31 | Názov dodávateľa |
| _PaName | Str30 | 31 | Vyhľadávacie pole |
| PaIno | Str10 | 11 | IČO dodávateľa |
| PaTin | Str14 | 15 | DIČ dodávateľa |

### Staré hodnoty (pred prekurzovaním)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OCourse | double | 8 | Pôvodný kurz |
| OAEndVal | double | 8 | Zostatok v tuzemskej mene |
| OFEndVal | double | 8 | Zostatok v zahraničnej mene |
| OCrdVal | double | 8 | Kurzový rozdiel predchádzajúci rok |

### Nové hodnoty (po prekurzovaní)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| NCourse | double | 8 | Nový (koncoročný) kurz |
| NAEndVal | double | 8 | Zostatok v tuzemskej mene |
| NFEndVal | double | 8 | Zostatok v zahraničnej mene |
| NCrdVal | double | 8 | Kurzový rozdiel aktuálny rok |

### Výsledok

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrdVal | double | 8 | Celkový kurzový rozdiel |
| AccDoc | Str12 | 13 | Číslo účtovného dokladu |

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
| 0 | DocNum | DocNum | Duplicit |
| 1 | ExtNum | ExtNum | Duplicit |
| 2 | _PaName | PaName | Case-insensitive, Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | ISH.DocNum | Hlavička faktúry |
| PaCode | PAB.PaCode | Dodávateľ |
| DvzName | ISRCRH.DvzName | Hlavička prekurzovania |

## Príklad výpočtu

```
Faktúra: 100 USD, kurz 0.95 = 95 EUR
Koncoročný kurz: 0.92

Výpočet:
- OFEndVal = 100 USD
- OAEndVal = 95 EUR (pôvodný zostatok)
- OCourse = 0.95

- NFEndVal = 100 USD
- NCourse = 0.92
- NAEndVal = 100 × 0.92 = 92 EUR

- CrdVal = 92 - 95 = -3 EUR (kurzová strata)
```

## Business pravidlá

- Každá neuhradená faktúra v cudzej mene má záznam
- CrdVal > 0 = kurzový zisk
- CrdVal < 0 = kurzová strata
- Po prekurzovaní sa aktualizuje ISH.EyCourse a ISH.EyCrdVal

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
