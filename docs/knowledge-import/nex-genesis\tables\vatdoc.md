# VATDOC - Súhrnné daňové doklady

## Kľúčové slová / Aliases

VATDOC, VATDOC.BTR, súhrnné, daňové, doklady

## Popis

Súhrnná tabuľka daňových dokladov s detailom DPH podľa 6 skupín sadzieb. Používa sa pre uzávierky DPH a podporuje tuzemské aj zahraničné doklady.

## Btrieve súbor

`VATDOC.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\VATDOC.BTR`

## Štruktúra polí (32 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo daňového dokladu - **FK** |
| ExtNum | Str12 | 13 | Externé číslo dokladu |
| ClsNum | Str5 | 6 | Číslo uzávierky DPH - **FK VTRLST** |

### Partner a dátum

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaName | Str30 | 31 | Názov partnera |
| VatDate | DateType | 4 | Dátum uplatnenia DPH |

### Sadzby DPH (6 skupín)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc1 | byte | 1 | Sadzba DPH v % - skupina 1 |
| VatPrc2 | byte | 1 | Sadzba DPH v % - skupina 2 |
| VatPrc3 | byte | 1 | Sadzba DPH v % - skupina 3 |
| VatPrc4 | byte | 1 | Sadzba DPH v % - skupina 4 |
| VatPrc5 | byte | 1 | Sadzba DPH v % - skupina 5 |
| VatPrc6 | byte | 1 | Sadzba DPH v % - skupina 6 |

### Hodnoty DPH (6 skupín)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatVal1 | double | 8 | Hodnota DPH - skupina 1 |
| VatVal2 | double | 8 | Hodnota DPH - skupina 2 |
| VatVal3 | double | 8 | Hodnota DPH - skupina 3 |
| VatVal4 | double | 8 | Hodnota DPH - skupina 4 |
| VatVal5 | double | 8 | Hodnota DPH - skupina 5 |
| VatVal6 | double | 8 | Hodnota DPH - skupina 6 |

### Hodnoty s DPH (6 skupín)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BValue1 | double | 8 | Hodnota s DPH - skupina 1 |
| BValue2 | double | 8 | Hodnota s DPH - skupina 2 |
| BValue3 | double | 8 | Hodnota s DPH - skupina 3 |
| BValue4 | double | 8 | Hodnota s DPH - skupina 4 |
| BValue5 | double | 8 | Hodnota s DPH - skupina 5 |
| BValue6 | double | 8 | Hodnota s DPH - skupina 6 |

### Súhrnné hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatVal | double | 8 | Celková hodnota DPH |
| BValue | double | 8 | Celková hodnota s DPH |

### Klasifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPart | Str1 | 2 | Strana DPH (I=vstup, O=výstup) |
| Foreign | byte | 1 | Zahraničný doklad (0=tuzemský, 1=zahraničný) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |

## Indexy (6)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum | DocNum | Duplicit, Case-insensitive |
| 1 | ExtNum | ExtNum | Duplicit, Case-insensitive |
| 2 | VatDate | VatDate | Duplicit |
| 3 | OutPart | OutPart | Duplicit |
| 4 | Foreign | Foreign | Duplicit |
| 5 | ClsNum | ClsNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | ISH.DocNum / ICH.DocNum | Zdrojový doklad |
| ClsNum | VTRLST.ClsNum | Uzávierka DPH |

## Typické sadzby DPH

| Skupina | Sadzba | Použitie |
|---------|--------|----------|
| 1 | 20% | Základná sadzba |
| 2 | 10% | Znížená sadzba |
| 3 | 0% | Oslobodené plnenia |
| 4-6 | - | Rezerva pre špeciálne prípady |

## Použitie

- Súhrnná evidencia DPH po skupinách
- Podklad pre výpočet uzávierky
- Rozlíšenie tuzemských a zahraničných dokladov

## Business pravidlá

- Jeden doklad = jeden záznam (na rozdiel od VTR)
- VatVal = SUM(VatVal1..VatVal6)
- BValue = SUM(BValue1..BValue6)
- Foreign=1 pre zahraničné doklady (EÚ, tretie krajiny)
- ClsNum prepája doklad s konkrétnou uzávierkou

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
