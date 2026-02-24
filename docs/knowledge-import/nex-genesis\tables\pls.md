# PLS - Položky predajného cenníka

## Kľúčové slová / Aliases

PLS, PLS.BTR, položky, predajného, cenníka

## Popis

Položky predajného cenníka. Každá položka obsahuje tovar s predajnými cenami v 4 hladinách (základná + D1-D3), ziskovosť, príznaky akcií a synchronizáciu.

## Btrieve súbor

`PLSnnnnn.BTR` (nnnnn = číslo cenníka)

## Umiestnenie

`C:\NEX\YEARACT\STK\PLSnnnnn.BTR`

## Štruktúra polí (50 polí)

### Identifikácia tovaru

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo (PLU) - **PRIMARY KEY** |
| GsName | Str30 | 31 | Názov tovaru |
| _GsName | Str20 | 21 | Vyhľadávacie pole názvu |
| GaName | Str60 | 61 | Doplnkový názov tovaru |
| _GaName | Str60 | 61 | Doplnkový názov - vyhľadávanie |
| MgCode | longint | 4 | Číslo tovarovej skupiny |
| FgCode | longint | 4 | Číslo finančnej skupiny |
| BarCode | Str15 | 16 | Prvotný identifikačný kód (EAN) |
| StkCode | Str15 | 16 | Skladový kód tovaru |
| OsdCode | Str30 | 31 | Objednávací kód tovaru |
| MsName | Str10 | 11 | Merná jednotka |

### Nastavenie tovaru

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PackGs | longint | 4 | Tovarové číslo pripojeného obalu |
| StkNum | word | 2 | Číslo skladu na odpočítanie |
| VatPrc | byte | 1 | Percentuálna sadzba DPH |
| GsType | Str1 | 2 | Typ položky (T=tovar, W=váhový, O=obal) |
| DrbMust | byte | 1 | Povinná trvanlivosť (0/1) |
| PdnMust | byte | 1 | Povinné výrobné čísla (0/1) |
| GrcMth | word | 2 | Záruka (mesiacov) |
| MinQnt | double | 8 | Minimálne predajné množstvo |
| OrdPrn | byte | 1 | Číslo oddelenia pre tlač objednávky |
| OpenGs | byte | 1 | Otvorené PLU - možno meniť cenu |

### Základná cena

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Profit | double | 8 | Percentuálna sadzba zisku |
| APrice | double | 8 | Aktuálna predajná cena bez DPH |
| BPrice | double | 8 | Aktuálna predajná cena s DPH |
| UPrice | double | 8 | Predchádzajúca cena s DPH |
| CpcSrc | Str1 | 2 | Zdroj nákupnej ceny (A/L/B/P) |

### Cenová hladina D1

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DscPrc1 | double | 8 | Percentuálna zľava pre D1 |
| PrfPrc1 | double | 8 | Percentuálna sadzba zisku D1 |
| APrice1 | double | 8 | Predajná cena D1 bez DPH |
| BPrice1 | double | 8 | Predajná cena D1 s DPH |

### Cenová hladina D2

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DscPrc2 | double | 8 | Percentuálna zľava pre D2 |
| PrfPrc2 | double | 8 | Percentuálna sadzba zisku D2 |
| APrice2 | double | 8 | Predajná cena D2 bez DPH |
| BPrice2 | double | 8 | Predajná cena D2 s DPH |

### Cenová hladina D3

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DscPrc3 | double | 8 | Percentuálna zľava pre D3 |
| PrfPrc3 | double | 8 | Percentuálna sadzba zisku D3 |
| APrice3 | double | 8 | Predajná cena D3 bez DPH |
| BPrice3 | double | 8 | Predajná cena D3 s DPH |

### Príznaky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DisFlag | byte | 1 | Vyradenie z evidencie (1=vyradený) |
| ChgItm | Str1 | 2 | Príznak zmeny (X=zmenený, P=po etikete) |
| Action | Str1 | 2 | Príznak akcie (A=akciový tovar) |
| Sended | byte | 1 | Príznak odoslania (0=zmenený, 1=odoslaný) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ModNum | word | 2 | Počítadlo modifikácií |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |
| OvsUser | Str8 | 9 | Používateľ posledného precenenia |
| OvsDate | DateType | 4 | Dátum posledného precenenia |

## Indexy (16)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | GsCode | GsCode | Unikátny |
| 1 | MgCode, GsCode | MgGs | Duplicit |
| 2 | _GsName | GsName | Duplicit, Case-insensitive |
| 3 | BarCode | BarCode | Duplicit, Case-insensitive |
| 4 | StkCode | StkCode | Duplicit, Case-insensitive |
| 5 | Profit | Profit | Duplicit |
| 6 | APrice | APrice | Duplicit |
| 7 | BPrice | BPrice | Duplicit |
| 8 | ChgItm | ChgItm | Duplicit |
| 9 | DisFlag | DisFlag | Duplicit |
| 10 | Action | Action | Duplicit |
| 11 | Sended | Sended | Duplicit |
| 12 | _GaName | GaName | Duplicit, Case-insensitive |
| 13 | MgCode, StkCode | MgSc | Duplicit |
| 14 | OsdCode | OsdCode | Duplicit |
| 15 | OvsUser | OvsUser | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| GsCode | GSCAT.GsCode | Katalóg produktov |
| MgCode | MGLST.MgCode | Tovarová skupina |
| FgCode | FGLST.FgCode | Finančná skupina |
| StkNum | STKLST.StkNum | Sklad |
| PackGs | GSCAT.GsCode | Obal |

## Použitie

- Cenotvorba a správa predajných cien
- Podpora 4 cenových hladín
- Sledovanie ziskovosti
- Akcie a zľavy
- Synchronizácia s pokladňami

## Business pravidlá

- BPrice = APrice * (1 + VatPrc/100)
- Profit = (APrice - NC) / NC * 100
- Action='A' označuje akciový tovar
- ChgItm='X' po zmene, 'P' po tlači etikety
- Sended=0 po zmene, 1 po synchronizácii

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
