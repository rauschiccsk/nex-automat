# OMI - Položky interných skladových výdajok

## Kľúčové slová / Aliases

OMI, OMI.BTR, interné výdaje položky, internal issue items

## Popis

Položková tabuľka interných skladových výdajok. Obsahuje detailné informácie o vydávanom tovare vrátane množstva, cien a stavu vyskladnenia.

## Btrieve súbor

`OMIyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OMIyynnn.BTR`

## Štruktúra polí (51 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | word | 2 | Číslo skladu výdaja |
| DocNum | Str12 | 13 | Interné číslo dokladu - **FK → OMH.DocNum** |
| ItmNum | word | 2 | Poradové číslo položky |
| DocDate | DateType | 4 | Dátum dokladu |

### Tovar

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| MgCode | word | 2 | Číslo tovarovej skupiny |
| GsCode | longint | 4 | Tovarové číslo (PLU) - **FK → GSCAT.GsCode** |
| GsName | Str30 | 31 | Názov tovaru |
| BarCode | Str15 | 16 | Identifikačný kód tovaru |
| StkCode | Str15 | 16 | Skladový kód tovaru |
| MsName | Str10 | 11 | Merná jednotka |

### Množstvá

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsQnt | double | 8 | Vydávané množstvo |
| ExpQnt | double | 8 | Množstvo pripravené na expedíciu |

### Ceny a hodnoty v NC

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc | double | 8 | Sadzba DPH v % |
| CPrice | double | 8 | Nákupná cena bez DPH |
| EPrice | double | 8 | Nákupná cena s DPH |
| CValue | double | 8 | Hodnota v NC bez DPH |
| EValue | double | 8 | Hodnota v NC s DPH |

### Ceny a hodnoty v PC

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BPrice | double | 8 | Predajná cena s DPH |
| AValue | double | 8 | Hodnota v PC bez DPH |
| BValue | double | 8 | Hodnota v PC s DPH |

### Stavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkStat | Str1 | 2 | Stav položky (N=zaevidované, S=vyskladnené) |
| ConStk | word | 2 | Číslo protiskladu príjmu/výdaja |

### Zdrojový doklad

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SrcDoc | Str12 | 13 | Číslo zdrojového dokladu |
| SrcItm | word | 2 | Číslo riadku zdrojového dokladu |

### Zákazka

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OcdNum | Str12 | 13 | Číslo zákazkového dokladu |
| OcdItm | longint | 4 | Číslo riadku zákazky |

### Pozícia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PosCode | Str15 | 16 | Skladový pozičný kód |

### Šarže

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RbaCode | Str30 | 31 | Kód výrobnej šarže |
| RbaDate | DateType | 4 | Dátum výrobnej šarže |

### Ostatné

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Notice | Str40 | 41 | Poznámka k položke |
| ModNum | word | 2 | Poradové číslo modifikácie |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (15)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | StkNum, DocNum, ItmNum | StDoIt | Duplicit |
| 1 | DocNum, ItmNum | DoIt | Duplicit |
| 2 | ItmNum | ItmNum | Duplicit |
| 3 | GsCode | GsCode | Duplicit |
| 4 | MgCode, GsCode | MgGs | Duplicit |
| 5 | GsName | GsName | Duplicit, Case insensitive |
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
| DocNum | OMH.DocNum | Hlavička výdajky |
| GsCode | GSCAT.GsCode | Tovar |
| MgCode | MGLST.MgCode | Tovarová skupina |
| StkNum | STKLST.StkNum | Sklad |
| SrcDoc | OMH.DocNum / TSH.DocNum | Zdrojový doklad |

## Stavy položky (StkStat)

| Hodnota | Popis |
|---------|-------|
| N | Zaevidované (čaká na vyskladnenie) |
| S | Vyskladnené (odpočítané zo skladu) |

## Použitie

- Evidencia položiek interných výdajok
- Sledovanie stavu vyskladnenia
- Prepojenie na zákazky
- Traceability cez šarže

## Business pravidlá

- CValue = CPrice × GsQnt
- EValue = EPrice × GsQnt
- StkStat='N' → položka ešte nebola vyskladnená
- StkStat='S' → položka bola odpočítaná zo skladu
- Pri medziskladovom presune sa vytvorí zodpovedajúca IMI položka

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
