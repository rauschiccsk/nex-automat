# PQI - Položky prevodných príkazov

## Kľúčové slová / Aliases

PQI, PQI.BTR, položky, prevodných, príkazov

## Popis

Položky prevodných príkazov. Každá položka reprezentuje jednu platbu v rámci prevodného príkazu s údajmi o príjemcovi a faktúre.

## Btrieve súbor

`PQIyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARyy\DOCS\PQIyynnn.BTR`

## Štruktúra polí (26 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo prevodného príkazu - **FK** |
| ItmNum | word | 2 | Poradové číslo položky |
| SerNum | longint | 4 | Pomocné poradové číslo |
| DocDate | DateType | 4 | Dátum vystavenia prevodného príkazu |

### Prepojenie na faktúru

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| IsDocNum | Str12 | 13 | Interné číslo uhrádzanej faktúry |
| IsExtNum | Str12 | 13 | Variabilný symbol uhrádzanej faktúry |

### Údaje platby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayVal | double | 8 | Uhrádzaná čiastka |
| Describe | Str30 | 31 | Popis prevodu (názov dodávateľa) |
| _Describe | Str30 | 31 | Vyhľadávacie pole popisu |

### Bankové spojenie príjemcu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ContoNum | Str20 | 21 | Číslo bankového účtu dodávateľa |
| BankCode | Str4 | 5 | Numerický smerovací kód banky |
| BankName | Str35 | 36 | Názov banky |
| BankSeat | Str30 | 31 | Sídlo banky |
| IbanCode | Str30 | 31 | IBAN kód |
| SwftCode | Str11 | 12 | SWIFT kód banky |

### Platobné symboly

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CsyCode | Str4 | 5 | Konštantný symbol |
| SpcSymb | Str12 | 13 | Špecifický symbol |

### Príznak

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Mark | Str1 | 2 | Pomocný príznak |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (7)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum | DocNum | Duplicit |
| 1 | DocNum, ItmNum | DoIt | Duplicit |
| 2 | SerNum | SerNum | Duplicit |
| 3 | DocDate | DocDate | Duplicit |
| 4 | _Describe | Describe | Duplicit |
| 5 | IsDocNum | IsDocNum | Duplicit |
| 6 | IsExtNum | IsExtNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | PQH.DocNum | Hlavička prevodného príkazu |
| IsDocNum | ISH.DocNum | Uhrádzaná dodávateľská faktúra |

## SEPA polia

Pre SEPA platby sa používajú:
- **IbanCode** - IBAN príjemcu (medzinárodný formát)
- **SwftCode** - BIC/SWIFT kód banky príjemcu

## Použitie

- Detaily jednotlivých platieb
- Prepojenie na faktúry
- Podklad pre bankový export

## Business pravidlá

- IsDocNum prepája položku na konkrétnu faktúru v ISH
- IsExtNum = variabilný symbol pre párovanie v banke
- PayVal môže byť čiastočná úhrada faktúry
- Describe zvyčajne obsahuje názov dodávateľa
- Bankové údaje sa preberajú z PAB (katalóg partnerov)

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
