# SAG - Tržby podľa tovarových skupín

## Kľúčové slová / Aliases

SAG, SAG.BTR, tržby, podľa, tovarových, skupín

## Popis

Agregovaná tabuľka finančných hodnôt z maloobchodného predaja členených podľa tovarových skupín. Slúži pre analytické účely a rýchle reporty.

## Btrieve súbor

`SAGyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\SAGyynnn.BTR`

## Štruktúra polí (11 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo dokladu - **FK → SAH.DocNum** |
| DocDate | DateType | 4 | Dátum predaja |
| MgCode | longint | 4 | Tovarová skupina - **FK → MGLST.MgCode** |

### Hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CValue | double | 8 | Hodnota v NC bez DPH |
| AValue | double | 8 | Hodnota v PC bez DPH |
| BValue | double | 8 | Hodnota v PC s DPH |
| DscVal | double | 8 | Hodnota zľavy |

### Zisk

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PrfPrc | double | 8 | Percentuálna hodnota zisku |
| PrfVal | double | 8 | Hodnota zisku |

## Indexy (4)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum | DocNum | Duplicit |
| 1 | DocDate | DocDate | Duplicit |
| 2 | MgCode | MgCode | Duplicit |
| 3 | DocNum, MgCode | DoMg | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | SAH.DocNum | Hlavička dokladu |
| MgCode | MGLST.MgCode | Tovarová skupina |

## Použitie

- Analýza predaja podľa tovarových skupín
- Rýchle reporty bez prepočtu položiek
- Sledovanie ziskovosti skupín
- Denné/mesačné štatistiky

## Business pravidlá

- Vytvárajú sa automaticky pri spracovaní predaja
- Agregácia z položiek SAI podľa MgCode
- PrfVal = AValue - CValue
- PrfPrc = (PrfVal / CValue) * 100

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
