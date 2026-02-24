# GSCLNK - Príslušenstvo a súvisiaci tovar

## Kľúčové slová / Aliases

GSCLNK, GSCLNK.BTR, prepojenia tovaru, product links, súvisiace položky

## Popis
Tabuľka väzieb medzi tovarmi. Definuje príslušenstvo, doplnky alebo súvisiace produkty k hlavnému tovaru.

## Btrieve súbor
`GSLNK.BTR`

## Umiestnenie
`C:\NEX\YEARACT\STORES\GSLNK.BTR`

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo (PLU) - hlavný tovar |
| LnkGsc | longint | 4 | Tovarové číslo súvisiaceho tovaru |
| LnkGsn | Str60 | 61 | Názov súvisiaceho tovaru (cache) |
| MinQnt | double | 8 | Minimálne potrebné množstvo |
| CrtUser | Str8 | 9 | Používateľ vytvorenia záznamu |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| LnkTyp | Str1 | 2 | Typ súvislosti (B-základný, O-voliteľný) |

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | GsCode, LnkGsc | GsLn | Unique (composite) |
| 1 | GsCode | GsCode | Duplicit |
| 2 | LnkGsc | LnkGsc | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| GsCode | GSCAT.GsCode | Hlavný tovar |
| LnkGsc | GSCAT.GsCode | Súvisiaci tovar |

## Typy väzieb

| LnkTyp | Popis |
|--------|-------|
| B | Základné príslušenstvo (povinné) |
| O | Voliteľné príslušenstvo |

## Príklady použitia

- Tlačiareň → Tonery, Papier
- Notebook → Puzdro, Myš, Nabíjačka
- Kamera → Pamäťová karta, Statív

## Stav migrácie

- [ ] Model vytvorený
- [ ] PostgreSQL model
- [ ] API endpoint
