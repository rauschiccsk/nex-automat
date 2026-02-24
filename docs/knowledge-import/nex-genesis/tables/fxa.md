# FXA - Evidenčné karty dlhodobého majetku

## Kľúčové slová / Aliases

FXA, FXA.BTR, evidenčné, karty, dlhodobého, majetku

## Popis

Hlavná tabuľka evidenčných kariet dlhodobého hmotného a nehmotného majetku. Obsahuje všetky základné údaje o majetku vrátane obstarávania, zaradenia, odpisovania a vyradenia. Každá kniha má vlastný súbor.

## Btrieve súbor

`FXAyynnn.BTR` (yy=rok, nnn=číslo knihy z FXBLST)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\FXAyynnn.BTR`

## Štruktúra polí (43 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SerNum | longint | 4 | Poradové číslo karty - **PK časť** |
| DocNum | Str12 | 13 | Interné (účtovné) číslo majetku |
| ExtNum | Str12 | 13 | Inventárne číslo majetku |
| FxaName | Str30 | 31 | Názov majetku |
| _FxaName | Str30 | 31 | Vyhľadávacie pole názvu |
| DocDate | DateType | 4 | Dátum založenia karty |
| ClasCode | Str10 | 11 | Kód jednotnej klasifikácie (KP) |

### Umiestnenie a zodpovednosť

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WriNum | longint | 4 | Prevádzkové číslo - **FK WRILST** |
| UseName | Str30 | 31 | Meno používateľa majetku |

### Obstaranie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PrvDoc | Str12 | 13 | Číslo dokladu obstarania |
| PrvMode | byte | 1 | Spôsob obstarania (0=Nákup, 1=Dar, 2=Vlastná výroba) |
| PrvDate | DateType | 4 | Dátum obstarania |
| PrvVal | double | 8 | Obstarávacia cena |
| PaCode | longint | 4 | Kód dodávateľa - **FK PARTNER** |
| PaName | Str30 | 31 | Názov dodávateľa |

### Zaradenie do užívania

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BegDoc | Str12 | 13 | Doklad zaradenia |
| BegDate | DateType | 4 | Dátum zaradenia do užívania |

### Vyradenie z užívania

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AsdDoc | Str12 | 13 | Doklad vyradenia |
| AsdDate | DateType | 4 | Dátum vyradenia |
| AsdMode | integer | 2 | Spôsob vyradenia (0-5) |

### Hodnoty a odpisy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ChgVal | double | 8 | Kumulatívna hodnota technických zhodnotení |
| ModVal | double | 8 | Kumulatívna hodnota korekcií vstupnej ceny |
| SuVal | double | 8 | Kumulatívna hodnota daňových odpisov |
| TEndVal | double | 8 | Daňová zostatková cena |
| LEndVal | double | 8 | Účtovná zostatková cena |

### Odpisovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FxaType | byte | 1 | Typ majetku (0=Hmotný, 1=Nehmotný) |
| TsuGrp | byte | 1 | Číslo daňovej odpisovej skupiny (1-6) |
| TsuMode | byte | 1 | Spôsob odpisovania (0=Rovnomerný, 1=Zrýchlený) |
| TsuYear | byte | 1 | Počet rokov daňového odpisovania |
| TItmQnt | byte | 1 | Počet položiek daňového odpisového plánu |
| LsuMode | byte | 1 | Spôsob účtovného odpisovania |
| LsuYear | byte | 1 | Počet rokov účtovného odpisovania |
| LItmQnt | word | 2 | Počet položiek účtovného odpisového plánu |
| FxaGrp | longint | 4 | Číslo účtovnej skupiny |

### Stav

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Status | Str1 | 2 | Príznak (L=účtovné odpisy = daňové) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtName | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (12)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | SerNum | SerNum | Duplicit |
| 1 | DocNum | DocNum | Duplicit |
| 2 | _FxaName | FxaName | Duplicit, Case-insensitive |
| 3 | WriNum | WriNum | Duplicit |
| 4 | BegDate | BegDate | Duplicit |
| 5 | ExtNum | ExtNum | Duplicit |
| 6 | DocDate | DocDate | Duplicit |
| 7 | ClasCode | ClasCode | Duplicit |
| 8 | PrvDoc | PrvDoc | Duplicit |
| 9 | PrvDate | PrvDate | Duplicit |
| 10 | PrvVal | PrvVal | Duplicit |
| 11 | PaCode | PaCode | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| WriNum | WRILST.WriNum | Prevádzková jednotka |
| PaCode | PARTNER.PaCode | Dodávateľ |
| TsuGrp + GrpYear | FXTGRP | Daňová odpisová skupina |
| FxaGrp | FXAGRP | Účtovná skupina |
| DocNum | FXT.DocNum | Daňové odpisy |
| DocNum | FXL.DocNum | Účtovné odpisy |
| DocNum | FXC.DocNum | Technické zhodnotenie |
| DocNum | FXM.DocNum | Korekcia ceny |
| DocNum | FXN.DocNum | Poznámky |
| DocNum | FXAASD.DocNum | Údaje vyradenia |

## Výpočtové pravidlá

### Zostatková cena

```
VstupnáCena = PrvVal + ChgVal - ModVal
TEndVal = VstupnáCena - SuVal  // Daňová
LEndVal = VstupnáCena - ÚčtovnéOdpisy  // Účtovná
```

### Generovanie DocNum

```
DocNum = BookNum + "-" + FormatNumber(SerNum, 6)
Príklad: "A001-000123"
```

## Typy majetku

| FxaType | Typ | Účtová trieda |
|---------|-----|---------------|
| 0 | DHM | 0xx (01x-09x) |
| 1 | DNM | 0xx (01x-07x) |

## Spôsoby vyradenia (AsdMode)

| Hodnota | Spôsob | Daňový dopad |
|---------|--------|--------------|
| 0 | Nevyradený | - |
| 1 | Predaj | Zostatková do nákladov |
| 2 | Likvidácia | Zostatková do nákladov |
| 3 | Škoda | Podľa náhrady |
| 4 | Dar | Zostatková do nákladov |
| 5 | Manko | Nedaňový náklad |

## Použitie

- Kompletná evidencia dlhodobého majetku
- Základná karta pre výpočet odpisov
- Sledovanie životného cyklu majetku
- Inventarizácia majetku

## Business pravidlá

- Majetok sa nedá zmazať ak má odpisy alebo zmeny
- Pri vyradení AsdMode > 0, majetok sa zobrazuje šedo
- Status='L' znamená že účtovné odpisy kopírujú daňové
- TsuGrp musí zodpovedať FXTGRP pre daný rok

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
