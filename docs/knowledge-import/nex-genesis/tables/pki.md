# PKI - Položky prebaľovacích dokladov

## Kľúčové slová / Aliases

PKI, PKI.BTR, položky, prebaľovacích, dokladov

## Popis

Položky prebaľovacích dokladov. Každá položka definuje transformáciu zdrojového tovaru na cieľový tovar s množstvami, cenami a skladovými pohybmi.

## Btrieve súbor

`PKIyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARyy\STK\PKIyynnn.BTR`

## Štruktúra polí (47 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | word | 2 | Číslo skladu |
| DocNum | Str12 | 13 | Interné číslo dokladu - **FK** |
| ItmNum | word | 2 | Poradové číslo položky |
| DocDate | DateType | 4 | Dátum vystavenia dokladu |

### Cieľový tovar (Tg* = Target)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| TgMgCode | word | 2 | Tovarová skupina cieľového tovaru |
| TgGsCode | longint | 4 | Tovarové číslo cieľového tovaru |
| TgGsName | Str30 | 31 | Názov cieľového tovaru |
| TgBarCode | Str15 | 16 | Identifikačný kód cieľového tovaru |
| TgStkCode | Str15 | 16 | Skladový kód cieľového tovaru |
| TgMsName | Str10 | 11 | Merná jednotka cieľového tovaru |
| TgGsQnt | double | 8 | Množstvo cieľového tovaru |
| TgCPrice | double | 8 | NC/MJ bez DPH cieľového tovaru |
| TgCValue | double | 8 | NC bez DPH cieľového tovaru |
| TgBPrice | double | 8 | PC bez DPH cieľového tovaru |
| TgSmCode | word | 2 | Kód skladového pohybu príjmu |

### Zdrojový tovar (Sc* = Source)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ScMgCode | word | 2 | Tovarová skupina zdrojového tovaru |
| ScGsCode | longint | 4 | Tovarové číslo zdrojového tovaru |
| ScGsName | Str30 | 31 | Názov zdrojového tovaru |
| ScBarCode | Str15 | 16 | Identifikačný kód zdrojového tovaru |
| ScStkCode | Str15 | 16 | Skladový kód zdrojového tovaru |
| ScMsName | Str10 | 11 | Merná jednotka zdrojového tovaru |
| ScGsQnt | double | 8 | Množstvo zdrojového tovaru |
| ScCPrice | double | 8 | NC/MJ bez DPH zdrojového tovaru |
| ScCValue | double | 8 | NC bez DPH zdrojového tovaru |
| ScBPrice | double | 8 | PC bez DPH zdrojového tovaru |
| ScSmCode | word | 2 | Kód skladového pohybu výdaja |

### Prepojenie na zdrojový doklad

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ScdNum | Str12 | 13 | Interné číslo zdrojového dokladu |
| ScdItm | word | 2 | Číslo riadku zdrojového dokladu |
| OcdNum | Str12 | 13 | Číslo zákazkového dokladu |
| OcdItm | word | 2 | Číslo riadku zákazkového dokladu |

### Stav a špeciálne údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkStat | Str1 | 2 | Príznak položky (N=neprebalený, S=prebalený) |
| DrbDate | DateType | 4 | Dátum trvanlivosti - expirácie |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

### Nepoužívané polia (x_*)

| Pole | Typ | Popis |
|------|-----|-------|
| x_TGsName, x_SGSName | Str30 | Staré vyhľadávacie polia |
| x_Flag | byte | Starý príznak |
| x_FIFOStr | Str220 | Stará FIFO štruktúra |
| x_Note1-3 | Str60 | Staré poznámky |

## Indexy (15)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum | DoIt | Duplicit |
| 1 | DocNum | DocNum | Duplicit |
| 2 | ItmNum | ItmNum | Duplicit |
| 3 | TgGsCode | TgGsCode | Duplicit |
| 4 | TgMgCode, TgGsCode | TgMgGs | Duplicit |
| 5 | x_TGSName | x_TGSName | Duplicit, Case-insensitive |
| 6 | TgBarCode | TgBarCode | Duplicit |
| 7 | TgStkCode | TgStkCode | Duplicit, Case-insensitive |
| 8 | StkNum, ScGsCode | SnSg | Duplicit |
| 9 | ScGsCode | ScGsCode | Duplicit |
| 10 | ScMgCode, ScGsCode | ScMgGs | Duplicit |
| 11 | x_SGSName | x_SGSName | Duplicit, Case-insensitive |
| 12 | ScBarCode | ScBarCode | Duplicit |
| 13 | ScStkCode | ScStkCode | Duplicit, Case-insensitive |
| 14 | StkStat | StkStat | Duplicit, Case-insensitive |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | PKH.DocNum | Hlavička dokladu |
| TgGsCode | GSCAT.GsCode | Cieľový produkt |
| ScGsCode | GSCAT.GsCode | Zdrojový produkt |
| TgMgCode | MGLST.MgCode | Tovarová skupina cieľa |
| ScMgCode | MGLST.MgCode | Tovarová skupina zdroja |

## Použitie

- Definícia transformácie zdrojového na cieľový tovar
- Sledovanie množstiev a hodnôt
- Prepojenie na zdrojové a zákazkové doklady
- Evidencia dátumov expirácie

## Business pravidlá

- StkStat='N' = položka ešte nebola vyskladnená/naskladnená
- StkStat='S' = prebalenie dokončené
- TgCValue = TgGsQnt * TgCPrice (hodnota cieľového tovaru)
- ScCValue = ScGsQnt * ScCPrice (hodnota zdrojového tovaru)
- Výsledný rozdiel = TgCValue - ScCValue

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
