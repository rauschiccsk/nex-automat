# APLITM - Položky akciových cenníkov

## Kľúčové slová / Aliases

APLITM, APLITM.BTR, položky, akciových, cenníkov

## Popis

Položky akciových cenníkov. Každá položka definuje tovar s akciovou cenou, časovým intervalom platnosti, periodicitou a minimálnym množstvom pre uplatnenie zľavy.

## Btrieve súbor

`APLITM.BTR`

## Umiestnenie

`C:\NEX\YEARACT\STK\APLITM.BTR`

## Štruktúra polí (31 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AplNum | word | 2 | Poradové číslo akciového cenníka - **FK** |
| GsCode | longint | 4 | Tovarové číslo (PLU) |
| GsName | Str30 | 31 | Názov tovaru |
| _GsName | Str20 | 21 | Vyhľadávacie pole názvu |
| BarCode | Str15 | 16 | Identifikačný kód tovaru |
| ActName | Str10 | 11 | Krátke pomenovanie akcie |

### Dátumové obdobie akcie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BegDate | DateType | 4 | Dátum začiatku akcie |
| EndDate | DateType | 4 | Dátum ukončenia akcie |
| BegTime | TimeType | 4 | Čas začiatku akcie |
| EndTime | TimeType | 4 | Čas ukončenia akcie |
| TimeInt | byte | 1 | Terminovanie (0=v období, 1=časový interval) |
| Period | Str7 | 8 | Periodicita podľa dní (1=aktívny deň) |

### Ceny

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc | byte | 1 | Sadzba DPH v % |
| PcAPrice | double | 8 | Cenníková cena bez DPH |
| PcBPrice | double | 8 | Cenníková cena s DPH |
| AcAPrice | double | 8 | Akciová cena bez DPH |
| AcBPrice | double | 8 | Akciová cena s DPH |
| DifPrc | double | 8 | Percentuálny rozdiel (zľava) |

### Podmienky akcie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| MinQnt | double | 8 | Minimálne predané množstvo pre akciu |
| AcType | Str1 | 2 | Typ akcie (V=výpredaj) |

### Prepojenie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ScdNum | Str12 | 13 | Zdrojový doklad položky |
| Sended | byte | 1 | Príznak odoslania (0=zmenený, 1=odoslaný) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Počítadlo modifikácií |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (8)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | AplNum, GsCode | AnGs | Duplicit |
| 1 | GsCode | GsCode | Duplicit |
| 2 | _GsName | GsName | Duplicit, Case-insensitive |
| 3 | BarCode | BarCode | Duplicit, Case-insensitive |
| 4 | Sended | Sended | Duplicit |
| 5 | ActName | ActName | Duplicit |
| 6 | ScdNum | ScdNum | Duplicit |
| 7 | ScdNum, GsCode | SnGs | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| AplNum | APLLST.AplNum | Akciový cenník |
| GsCode | GSCAT.GsCode | Katalóg produktov |
| GsCode | PLS.GsCode | Predajný cenník |

## Príklady Period

| Period | Popis |
|--------|-------|
| "1111111" | Každý deň |
| "1111100" | Pondelok až piatok |
| "0000011" | Víkend |
| "1000000" | Len pondelok |

## Použitie

- Definícia akciových cien
- Časové ohraničenie platnosti
- Periodicita počas týždňa
- Minimálne množstvo pre zľavu
- Synchronizácia s pokladňami

## Business pravidlá

- DifPrc = (1 - AcBPrice/PcBPrice) * 100
- Akcia je aktívna ak: BegDate ≤ dnes ≤ EndDate AND Period[deň]=1
- TimeInt=1 znamená, že BegTime a EndTime sa uplatňujú
- MinQnt > 0 podmieňuje akciu minimálnym množstvom
- AcType='V' označuje výpredaj

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
