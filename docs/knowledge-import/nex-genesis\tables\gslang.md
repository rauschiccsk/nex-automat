# GSLANG - Jazykové mutácie názvov

## Kľúčové slová / Aliases

GSLANG, GSLANG.BTR, jazykové mutácie, language variants, preklady názvov

## Popis
Tabuľka prekladov názvov tovarov do iných jazykov. Používa sa pre viacjazyčné prostredie (napr. export do zahraničia, e-shop).

## Btrieve súbor
`GSLANG.BTR`

## Umiestnenie
`C:\NEX\YEARACT\STORES\GSLANG.BTR`

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| LngCode | Str2 | 3 | Kód jazyka (napr. "EN", "DE", "HU") |
| GsCode | longint | 4 | Tovarové číslo (PLU) - **FK → GSCAT** |
| GsName | Str60 | 61 | Názov tovaru v danom jazyku |
| BarCode | Str15 | 16 | Identifikačný kód tovaru |

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | LngCode, GsCode | LnGs | Duplicit (composite) |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| GsCode | GSCAT.GsCode | Tovarová položka |

## Kódy jazykov

| Kód | Jazyk |
|-----|-------|
| SK | Slovenčina |
| CZ | Čeština |
| EN | Angličtina |
| DE | Nemčina |
| HU | Maďarčina |
| PL | Poľština |

## Stav migrácie

- [ ] Model vytvorený
- [ ] PostgreSQL model
- [ ] API endpoint
