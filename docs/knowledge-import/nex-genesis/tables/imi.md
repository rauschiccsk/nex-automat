# IMI - Položky interných príjemok

## Kľúčové slová / Aliases

IMI, IMI.BTR, interné príjmy položky, internal receipt items

## Popis

Tabuľka položiek interných skladových príjemok. Obsahuje údaje o prijímanom tovare, množstvách, cenách a stave naskladnenia.

## Btrieve súbor

`IMIyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\IMIyynnn.BTR`

## Štruktúra polí (52 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo príjemky - **FK → IMH.DocNum** |
| ItmNum | word | 2 | Poradové číslo položky |
| StkNum | word | 2 | Číslo skladu príjmu |
| ConStk | word | 2 | Číslo protiskladu |

### Tovar

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| MgCode | word | 2 | Číslo tovarovej skupiny |
| GsCode | longint | 4 | Tovarové číslo (PLU) |
| GsName | Str30 | 31 | Názov tovaru |
| BarCode | Str15 | 16 | Čiarový kód |
| StkCode | Str15 | 16 | Skladový kód |
| MsName | Str10 | 11 | Merná jednotka |

### Množstvo a ceny

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsQnt | double | 8 | Prijaté množstvo |
| VatPrc | double | 8 | Sadzba DPH (%) |
| CPrice | double | 8 | Nákupná cena bez DPH |
| EPrice | double | 8 | Nákupná cena s DPH |
| CValue | double | 8 | Hodnota v NC bez DPH |
| EValue | double | 8 | Hodnota v NC s DPH |
| RndVal | double | 8 | Hodnota zaokrúhlenia |
| BPrice | double | 8 | Predajná cena s DPH |
| AValue | double | 8 | Hodnota v PC bez DPH |
| BValue | double | 8 | Hodnota v PC s DPH |

### Väzby na iné doklady

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Kód dodávateľa |
| OcdNum | Str12 | 13 | Číslo zákazky |
| OcdItm | longint | 4 | Riadok zákazky |
| SrcDoc | Str12 | 13 | Číslo zdrojového dokladu |
| SrcItm | word | 2 | Riadok zdrojového dokladu |

### Pozícia a šarže

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PosCode | Str15 | 16 | Skladový pozičný kód |
| RbaCode | Str30 | 31 | Kód výrobnej šarže |
| RbaDate | DateType | 4 | Dátum výrobnej šarže |

### Stav a poznámky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocDate | DateType | 4 | Dátum dokladu |
| StkStat | Str1 | 2 | Stav položky (N/S) |
| Notice | Str40 | 41 | Poznámka k položke |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |
| ModNum | word | 2 | Poradové číslo zmeny |

## Indexy (15)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | StkNum, DocNum, ItmNum | StDoIt | Duplicit |
| 1 | DocNum, ItmNum | DoIt | Duplicit |
| 2 | ItmNum | ItmNum | Duplicit |
| 3 | GsCode | GsCode | Duplicit |
| 4 | MgCode, GsCode | MgGs | Duplicit |
| 5 | x_GsName | GsName | Duplicit, Case insensitive |
| 6 | CPrice | CPrice | Duplicit |
| 7 | BarCode | BarCode | Duplicit |
| 8 | StkCode | StkCode | Duplicit, Case insensitive |
| 9 | GsQnt | GsQnt | Duplicit |
| 10 | StkStat | StkStat | Duplicit, Case insensitive |
| 11 | ConStk | ConStk | Duplicit |
| 12 | DocNum | DocNum | Duplicit |
| 13 | PosCode | PosCode | Duplicit, Case insensitive |
| 14 | RbaCode | RbaCode | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | IMH.DocNum | Hlavička príjemky |
| GsCode | GSCAT.GsCode | Tovar |
| MgCode | MGLST.MgCode | Tovarová skupina |
| StkNum | STKLST.StkNum | Sklad |
| PaCode | PAB.PaCode | Dodávateľ |
| OcdNum | OCH.DocNum | Zákazka |

## Stav položky (StkStat)

| Hodnota | Popis |
|---------|-------|
| N | Zaevidovaná (nezaskladnená) |
| S | Naskladnená |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
