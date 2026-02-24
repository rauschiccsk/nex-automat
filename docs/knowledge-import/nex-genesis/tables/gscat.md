# GSCAT - Evidencia tovaru

## Kľúčové slová / Aliases

GSCAT, GSCAT.BTR, katalóg, produkty, tovar, товар, árukatalógus, product catalog, items, PLU, položky, sortiment

## Popis
Hlavná tabuľka katalógu produktov. Obsahuje všetky tovarové položky vrátane základných údajov, cien, DPH sadzieb, skupín a ďalších atribútov.

## Btrieve súbor
`GSCAT.BTR`

## Umiestnenie
`C:\NEX\YEARACT\STORES\GSCAT.BTR`

## Veľkosť záznamu
~705 bytes

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo (PLU) - **PRIMARY KEY** |
| GsName | Str30 | 31 | Názov tovaru |
| _GsName | Str15 | 16 | Vyhľadávacie pole názvu tovaru |
| MgCode | longint | 4 | Číslo tovarovej skupiny (FK → MGLST) |
| FgCode | longint | 4 | Číslo finančnej skupiny (FK → FGLST) |
| BarCode | Str15 | 16 | Prvotný identifikačný kód tovaru |
| StkCode | Str15 | 16 | Skladový kód tovaru |
| MsName | Str10 | 11 | Názov mernej jednotky |
| PackGs | longint | 4 | Tovarové číslo pripojeného obalu |
| GsType | Str1 | 2 | Typ položky (T-tovar, W-váhový, O-obal) |
| DrbMust | byte | 1 | Povinné zadávanie trvanlivosti (0/1) |
| PdnMust | byte | 1 | Povinné sledovanie výrobných čísel (0/1) |
| GrcMth | word | 2 | Záručná doba (mesiace) |
| VatPrc | byte | 1 | Percentuálna sadzba DPH |
| Volume | double | 8 | Objem tovaru (MJ na 1 m³) |
| Weight | double | 8 | Váha tovaru (váha jednej MJ) |
| MsuQnt | double | 8 | Množstvo tovaru v základnej jednotke |
| MsuName | Str5 | 6 | Názov základnej jednotky (kg, m, l, m², m³) |
| SbcCnt | word | 2 | Počet druhotných identifikačných kódov |
| DisFlag | byte | 1 | Vyradenie z evidencie (1=vyradený) |
| LinPrice | double | 8 | Posledná nákupná cena tovaru |
| LinDate | DateType | 4 | Dátum posledného príjmu |
| LinStk | word | 2 | Číslo skladu posledného príjmu |
| Sended | byte | 1 | Príznak odoslania zmien (0/1) |
| ModNum | word | 2 | Poradové číslo modifikácie |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |
| LinPac | longint | 4 | Kód posledného dodávateľa |
| SecNum | word | 2 | Číslo váhovej sekcie |
| WgCode | word | 2 | Váhové tovarové číslo (váhové PLU) |
| CrtUser | Str8 | 9 | Používateľ vytvorenia záznamu |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| BasGsc | longint | 4 | Odkaz na základný tovar |
| GscKfc | word | 2 | Počet kusov v kartónovom balení |
| GspKfc | word | 2 | Počet kartónov v paletovom balení |
| QliKfc | double | 8 | Hmotnosť kartónu |
| DrbDay | word | 2 | Počet dní trvanlivosti |
| OsdCode | Str15 | 16 | Objednávací kód tovaru |
| MinOsq | double | 8 | Minimálne objednávacie množstvo |
| SpcCode | Str30 | 31 | Špecifikačný kód položky |
| PrdPac | longint | 4 | Kód výrobcu |
| SupPac | longint | 4 | Kód dodávateľa |
| SpirGs | byte | 1 | Príznak liehovín (1=liehový výrobok) |
| GaName | Str60 | 61 | Doplnkový názov tovaru |
| _GaName | Str60 | 61 | Doplnkový názov - vyhľadávacie pole |
| DivSet | byte | 1 | Deliteľnosť (0-voľne, 1-nedeliteľný, 2-1/2...) |
| SgCode | longint | 4 | Číslo špecifikačnej skupiny (FK → SGLST) |
| Notice | Str240 | 241 | Poznámkový riadok |
| NewVatPrc | Str2 | 3 | Nová pripravená sadzba DPH |
| Reserve | Str4 | 5 | Rezerva |
| ShpNum | byte | 1 | Číslo elektronického obchodu |
| SndShp | byte | 1 | Príznak uloženia do e-shopu |
| PlsNum1-5 | word | 2×5 | Čísla predajných cenníkov |
| RbaTrc | byte | 1 | Povinné sledovanie výrobnej šarže (0/1) |
| CctCod | Str10 | 11 | Kód jednotnej tarify colného sadzobníka |
| IsiSnt | Str3 | 4 | Syntetická časť účtu (DF) |
| IsiAnl | Str6 | 7 | Analytická časť účtu (DF) |
| IciSnt | Str3 | 4 | Syntetická časť účtu (OF) |
| IciAnl | Str6 | 7 | Analytická časť účtu (OF) |
| ProTyp | Str1 | 2 | Typ produktu (M-materiál, T-tovar, S-služba) |

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | GsCode | GsCode | Unique, Primary |
| 1 | MgCode, GsCode | MgGs | Duplicit |
| 2 | FgCode | FgCode | Duplicit |
| 3 | _GsName | GsName | Case-insensitive, Duplicit |
| 4 | BarCode | BarCode | Duplicit |
| 5 | StkCode | StkCode | Duplicit |
| 6 | SpcCode | SpcCode | Duplicit |
| 7 | OsdCode | OsdCode | Duplicit |
| 8 | GsType | GsType | Duplicit |
| 9 | PackGs | PackGs | Duplicit |
| 10 | DisFlag | DisFlag | Duplicit |
| 11 | SecNum, WgCode | SnWc | Duplicit |
| 12 | Sended | Sended | Duplicit |
| 13 | _GaName | GaName | Case-insensitive, Duplicit |
| 14 | MgCode, StkCode | MgSc | Duplicit |
| 15 | MsName | MsName | Case-insensitive, Duplicit |
| 16 | CctCod | CctCod | Duplicit |
| 17 | ProTyp | ProTyp | Case-insensitive, Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| MgCode | MGLST.MgCode | Tovarová skupina |
| FgCode | FGLST.FgCode | Finančná skupina |
| SgCode | SGLST.SgCode | Špecifikačná skupina |
| PackGs | GSCAT.GsCode | Pripojený obal |
| BasGsc | GSCAT.GsCode | Základný tovar |
| PrdPac | PAB.PabCode | Výrobca |
| SupPac | PAB.PabCode | Dodávateľ |
| LinPac | PAB.PabCode | Posledný dodávateľ |

## Stav migrácie

- [x] Model vytvorený (`packages/nexdata/nexdata/models/gscat.py`)
- [x] Kamenický dekódovanie
- [ ] PostgreSQL model
- [ ] API endpoint
- [ ] Desktop UI (PySide6)
