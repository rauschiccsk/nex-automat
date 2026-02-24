# VTR - Zoznam daňových dokladov

## Kľúčové slová / Aliases

VTR, VTR.BTR, zoznam, daňových, dokladov

## Popis

Evidencia daňových dokladov pre uzávierky DPH. Každý záznam reprezentuje jeden doklad s jeho DPH hodnotami a zaradením.

## Btrieve súbor

`VTR.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\VTR.BTR`

## Štruktúra polí (19 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo daňového dokladu - **FK** |
| VatGrp | byte | 1 | Skupina DPH |
| ExtNum | Str12 | 13 | Externé číslo daňového dokladu |

### Partner

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaName | Str30 | 31 | Názov partnera |
| PaCode | longint | 4 | Kód firmy - **FK PAB** |

### DPH údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPart | Str1 | 2 | Strana DPH (I=vstup, O=výstup) |
| VatDate | DateType | 4 | Dátum uplatnenia DPH |
| VatPrc | byte | 1 | Percentuálna sadzba DPH |
| AValue | double | 8 | Hodnota dokladu bez DPH (základ dane) |
| VatVal | double | 8 | Hodnota DPH |

### Klasifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CorDoc | byte | 1 | Opravný doklad (dobropis/ťarchopis) |
| DocSpc | byte | 1 | Špecifikácia dokladu |
| VtdSpc | byte | 1 | Špecifikácia pre výpočet daňového priznania |
| RowTyp | Str2 | 3 | Typ riadku kontrolného výkazu |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |

## Indexy (7)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum | DocNum | Duplicit |
| 1 | DocNum, VatGrp | DnVg | Duplicit |
| 2 | ExtNum | ExtNum | Duplicit, Case-insensitive |
| 3 | VatDate | VatDate | Duplicit |
| 4 | VatPart | VatPart | Duplicit |
| 5 | VtdSpc | VtdSpc | Duplicit |
| 6 | RowTyp, DocNum | RtDn | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | ISH.DocNum / ICH.DocNum | Zdrojový doklad |
| PaCode | PAB.Code | Partner |
| VtdSpc | VTDSPC.VtdSpc | Špecifikácia dokladu |

## Strana DPH (VatPart)

| Hodnota | Popis | Zdroj |
|---------|-------|-------|
| I | Vstup (Input) | Dodávateľské faktúry ISB |
| O | Výstup (Output) | Odberateľské faktúry ICB |

## Typy riadkov kontrolného výkazu (RowTyp)

| Hodnota | Popis |
|---------|-------|
| A1 | Dodanie tovaru/služby |
| A2 | Oprava dodania |
| B1 | Nadobudnutie tovaru z EÚ |
| B2 | Nadobudnutie služby z EÚ |
| B3 | Tuzemské samozdanenie |
| C1 | Dovoz tovaru |
| C2 | Odložená platba DPH |
| D1 | Súhrnný riadok |
| D2 | Oprava súhrnného riadku |

## Použitie

- Evidencia DPH dokladov pre výpočet dane
- Podklad pre daňové priznanie
- Generovanie kontrolného výkazu

## Business pravidlá

- Jeden doklad môže mať viacero záznamov (podľa VatGrp)
- VatPart určuje smer DPH (vstup/výstup)
- AValue = základ dane, VatVal = hodnota DPH
- RowTyp určuje zaradenie do kontrolného výkazu

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
