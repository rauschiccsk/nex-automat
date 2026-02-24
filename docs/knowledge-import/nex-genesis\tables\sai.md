# SAI - Položky výdajok MO predaja

## Kľúčové slová / Aliases

SAI, SAI.BTR, položky, výdajok, predaja

## Popis

Položková tabuľka skladových výdajok z maloobchodného predaja. Obsahuje jednotlivé predané položky s množstvami, cenami a stavom vysporiadania so skladom.

## Btrieve súbor

`SAIyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\SAIyynnn.BTR`

## Štruktúra polí (28 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo dokladu - **FK → SAH.DocNum** |
| DocDate | DateType | 4 | Dátum predaja |

### Tovar

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo (PLU) - **FK → GSCAT.GsCode** |
| MgCode | word | 2 | Tovarová skupina - **FK → MGLST.MgCode** |
| GsName | Str30 | 31 | Názov tovaru |
| BarCode | Str15 | 16 | Identifikačný kód (EAN) |
| StkCode | Str15 | 16 | Skladový kód tovaru |

### Množstvá

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SeQnt | double | 8 | Predané množstvo |
| SuQnt | double | 8 | Vysporiadané (odpočítané) množstvo |
| CpSeQnt | double | 8 | Potrebné množstvo komponentov |
| CpSuQnt | double | 8 | Vysporiadané množstvo komponentov |

### Sklad

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | longint | 4 | Číslo skladu výdaja |
| StkStat | Str1 | 2 | Stav položky (N/S/C) |

### Hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CPrice | double | 8 | Nákupná cena tovaru |
| CValue | double | 8 | Hodnota v NC bez DPH |
| VatPrc | byte | 1 | Sadzba DPH (%) |
| DscVal | double | 8 | Hodnota zľavy |
| AValue | double | 8 | Hodnota v PC bez DPH |
| BValue | double | 8 | Hodnota v PC s DPH |

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

## Indexy (6)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum | DocNum | Duplicit |
| 1 | GsCode | GsCode | Duplicit |
| 2 | DocNum, GsCode, StkNum | DoGsSt | Duplicit |
| 3 | MgCode | MgCode | Duplicit |
| 4 | BarCode | BarCode | Duplicit |
| 5 | StkStat | StkStat | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | SAH.DocNum | Hlavička dokladu |
| GsCode | GSCAT.GsCode | Tovar |
| MgCode | MGLST.MgCode | Tovarová skupina |
| StkNum | STKLST.StkNum | Sklad |

## Stavy položky (StkStat)

| Hodnota | Popis |
|---------|-------|
| N | Neodpočítaný zo skladu |
| S | Vyskladnený |
| C | Rozdelený na komponenty (výrobok) |

## Použitie

- Položky denného predaja
- Sledovanie vysporiadania so skladom
- Analýza predaja podľa tovarov
- Podklad pre rozpad komponentov

## Business pravidlá

- SeQnt = predané množstvo
- SuQnt = odpočítané zo skladu (SeQnt=SuQnt po vysporiadaní)
- StkStat='C' znamená výrobok - komponenty v SAC
- CpSeQnt/CpSuQnt pre sledovanie komponentov

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
