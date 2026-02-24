# RMI - Položky medziskladových presunov

## Kľúčové slová / Aliases

RMI, RMI.BTR, položky, medziskladových, presunov

## Popis

Položková tabuľka medziskladových presunov. Obsahuje detailné informácie o presúvanom tovare vrátane množstva, cien, pozícií v oboch skladoch a stavu realizácie.

## Btrieve súbor

`RMIyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\RMIyynnn.BTR`

## Štruktúra polí (53 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ScStkNum | word | 2 | Číslo zdrojového skladu |
| DocNum | Str12 | 13 | Interné číslo dokladu - **FK → RMH.DocNum** |
| ItmNum | word | 2 | Poradové číslo položky |
| DocDate | DateType | 4 | Dátum dokladu |

### Sklady a pohyby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| TgStkNum | word | 2 | Číslo cieľového skladu |
| ScSmCode | word | 2 | Skladový pohyb výdaja |
| TgSmCode | word | 2 | Skladový pohyb príjmu |

### Tovar

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| MgCode | word | 2 | Číslo tovarovej skupiny |
| GsCode | longint | 4 | Tovarové číslo (PLU) - **FK → GSCAT.GsCode** |
| GsName | Str30 | 31 | Názov tovaru |
| _GsName | Str30 | 31 | Názov pre vyhľadávanie |
| BarCode | Str15 | 16 | Identifikačný kód tovaru |
| StkCode | Str15 | 16 | Skladový kód tovaru |
| MsName | Str10 | 11 | Merná jednotka |

### Množstvá

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsQnt | double | 8 | Presúvané množstvo |
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
| APrice | double | 8 | Predajná cena bez DPH |
| BPrice | double | 8 | Predajná cena s DPH |
| AValue | double | 8 | Hodnota v PC bez DPH |
| BValue | double | 8 | Hodnota v PC s DPH |

### Pozície (WMS)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SrcPos | Str15 | 16 | Pozícia v zdrojovom sklade |
| TrgPos | Str15 | 16 | Pozícia v cieľovom sklade |

### Zdrojový doklad

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SrdNum | Str12 | 13 | Číslo zdrojového dokladu |
| SrdItm | word | 2 | Číslo riadku zdrojového dokladu |
| CndNum | Str12 | 13 | Číslo pripojeného dokladu |

### Zákazka

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OcdNum | Str12 | 13 | Číslo zákazkového dokladu |

### Expirácia a šarže

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DrbDate | DateType | 4 | Dátum trvanlivosti (expirácia) |
| RbaCode | Str30 | 31 | Kód výrobnej šarže |
| RbaDate | DateType | 4 | Dátum výrobnej šarže |

### Stavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkStat | Str1 | 2 | Stav položky (N=čaká, S=zrealizovaná) |

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
| 0 | ScStkNum, DocNum, ItmNum | StDoIt | Duplicit |
| 1 | DocNum, ItmNum | DoIt | Duplicit |
| 2 | DocNum | DocNum | Duplicit |
| 3 | ItmNum | ItmNum | Duplicit |
| 4 | GsCode | GsCode | Duplicit |
| 5 | MgCode, GsCode | MgGs | Duplicit |
| 6 | _GsName | GsName | Duplicit, Case insensitive |
| 7 | CPrice | CPrice | Duplicit |
| 8 | BarCode | BarCode | Duplicit |
| 9 | StkCode | StkCode | Duplicit, Case insensitive |
| 10 | GsQnt | GsQnt | Duplicit |
| 11 | StkStat | StkStat | Duplicit, Case insensitive |
| 12 | SrcPos | SrcPos | Duplicit, Case insensitive |
| 13 | TrgPos | TrgPos | Duplicit, Case insensitive |
| 14 | RbaCode | RbaCode | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | RMH.DocNum | Hlavička presunu |
| GsCode | GSCAT.GsCode | Tovar |
| MgCode | MGLST.MgCode | Tovarová skupina |
| ScStkNum | STKLST.StkNum | Zdrojový sklad |
| TgStkNum | STKLST.StkNum | Cieľový sklad |

## Stavy položky (StkStat)

| Hodnota | Popis |
|---------|-------|
| N | Čaká na presun (nezrealizovaná) |
| S | Presun vykonaný (zrealizovaná) |

## Použitie

- Evidencia položiek medziskladových presunov
- Sledovanie stavu realizácie
- WMS pozície pre oba sklady
- Traceability cez šarže

## Business pravidlá

- CValue = CPrice × GsQnt
- EValue = EPrice × GsQnt
- StkStat='N' → položka ešte nebola presúvaná
- StkStat='S' → položka bola presúvaná (odpočítaná zo zdroja, pripočítaná k cieľu)
- Pri presune sa kontroluje dostupnosť v zdrojovom sklade

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
