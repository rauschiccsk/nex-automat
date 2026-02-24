# PLD - Zoznam zrušených položiek cenníka

## Kľúčové slová / Aliases

PLD, PLD.BTR, zoznam, zrušených, položiek, cenníka

## Popis

Archív zrušených položiek predajného cenníka. Keď sa položka vymaže z cenníka, presunie sa do tohto súboru pre možnosť obnovenia alebo audit.

## Btrieve súbor

`PLDnnnnn.BTR` (nnnnn = číslo cenníka)

## Umiestnenie

`C:\NEX\YEARACT\STK\PLDnnnnn.BTR`

## Štruktúra polí (31 polí)

### Identifikácia tovaru

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo (PLU) |
| GsName | Str30 | 31 | Názov tovaru |
| _GsName | Str20 | 21 | Vyhľadávacie pole názvu |
| MgCode | longint | 4 | Číslo tovarovej skupiny |
| FgCode | longint | 4 | Číslo finančnej skupiny |
| BarCode | Str15 | 16 | Prvotný identifikačný kód |
| StkCode | Str15 | 16 | Skladový kód tovaru |
| MsName | Str10 | 11 | Merná jednotka |

### Nastavenie tovaru

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PackGs | longint | 4 | Tovarové číslo pripojeného obalu |
| StkNum | word | 2 | Číslo skladu |
| VatPrc | byte | 1 | Sadzba DPH |
| GsType | Str1 | 2 | Typ položky (T/W/O) |
| DrbMust | byte | 1 | Povinná trvanlivosť |
| PdnMust | byte | 1 | Povinné výrobné čísla |
| GrcMth | word | 2 | Záruka (mesiacov) |
| OrdPrn | byte | 1 | Číslo oddelenia pre tlač |
| OpenGs | byte | 1 | Otvorené PLU |

### Cenové údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Profit | double | 8 | Percentuálna sadzba zisku |
| APrice | double | 8 | Predajná cena bez DPH |
| BPrice | double | 8 | Predajná cena s DPH |
| UPrice | double | 8 | Predchádzajúca cena s DPH |

### Príznaky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DisFlag | byte | 1 | Vyradenie z evidencie |
| ChgItm | Str1 | 2 | Príznak zmeny |
| Action | Str1 | 2 | Príznak akcie |
| Sended | byte | 1 | Príznak odoslania |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ModNum | word | 2 | Počítadlo modifikácií |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny (=zrušenia) |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (12)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | GsCode | GsCode | Duplicit |
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

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| GsCode | GSCAT.GsCode | Katalóg produktov |
| MgCode | MGLST.MgCode | Tovarová skupina |

## Použitie

- Archív zrušených položiek
- Možnosť obnovenia zmazaných položiek
- Audit zmien cenníka
- Sledovanie histórie cenníka

## Business pravidlá

- Pri zmazaní položky z PLS sa skopíruje do PLD
- ModDate/ModTime obsahuje čas zrušenia
- Štruktúra je identická s PLS (bez cenových hladín D1-D3)
- Položky v PLD nie sú aktívne v predaji

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
