# SAP - Hotovostné úhrady faktúr

## Kľúčové slová / Aliases

SAP, SAP.BTR, hotovostné, úhrady, faktúr

## Popis

Tabuľka hotovostných úhrad odberateľských faktúr realizovaných priamo na ERP pokladni. Umožňuje zákazníkom uhradiť faktúry v hotovosti pri návšteve predajne.

## Btrieve súbor

`SAPyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\SAPyynnn.BTR`

## Štruktúra polí (10 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo dokladu MO predaja - **FK → SAH.DocNum** |
| DocDate | DateType | 4 | Dátum predaja/úhrady |

### Faktúra

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| IcdNum | Str12 | 13 | Interné číslo faktúry - **FK → ICH.DocNum** |
| IceNum | Str20 | 21 | Externé číslo faktúry |

### Odberateľ

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Kód odberateľa - **FK → PAB.PaCode** |
| PaName | Str30 | 31 | Názov odberateľa |

### Úhrada

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayVal | double | 8 | Hodnota úhrady |
| CsdNum | Str12 | 13 | Interné číslo pokladničného dokladu |

## Indexy (5)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, IceNum | DnIe | Duplicit |
| 1 | DocNum | DocNum | Duplicit |
| 2 | IceNum | IceNum | Duplicit |
| 3 | DocDate | DocDate | Duplicit |
| 4 | DocNum, PaCode | DnPc | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | SAH.DocNum | Doklad MO predaja |
| IcdNum | ICH.DocNum | Faktúra |
| PaCode | PAB.PaCode | Odberateľ |
| CsdNum | CSD.DocNum | Pokladničný doklad |

## Použitie

- Úhrady faktúr na ERP pokladni
- Prepojenie MO predaja s pohľadávkami
- Evidencia hotovostných príjmov za faktúry

## Business pravidlá

- Jeden doklad SAH môže obsahovať viacero úhrad FA
- CsdNum odkazuje na vytvorený príjmový PD
- PayVal = uhradená čiastka (môže byť čiastočná úhrada)

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
