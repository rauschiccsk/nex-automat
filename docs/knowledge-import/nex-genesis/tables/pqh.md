# PQH - Hlavičky prevodných príkazov

## Kľúčové slová / Aliases

PQH, PQH.BTR, hlavičky, prevodných, príkazov

## Popis

Hlavičky prevodných príkazov. Každý doklad reprezentuje jeden prevodný príkaz s jednou alebo viacerými platbami.

## Btrieve súbor

`PQHyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARyy\DOCS\PQHyynnn.BTR`

## Štruktúra polí (17 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo prevodného príkazu - **PRIMARY KEY** |
| SerNum | longint | 4 | Poradové číslo prevodného príkazu |
| Year | Str2 | 3 | Rok dokladu |

### Údaje dokladu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocDate | DateType | 4 | Dátum vystavenia prevodného príkazu |
| DocVal | double | 8 | Celková hodnota prevodného príkazu |
| ItmQnt | word | 2 | Počet položiek dokladu |

### Elektronické bankovníctvo

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AboStat | Str1 | 2 | Stav ABO (O=odoslaný) |
| AboDate | DateType | 4 | Dátum odoslania prevodného príkazu |
| AboTime | TimeType | 4 | Čas odoslania prevodného príkazu |

### Tlač

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PrnCnt | byte | 1 | Počet vytlačených kópií |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (4)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum | DocNum | Duplicit |
| 1 | Year, SerNum | YearSerNum | Unikátny |
| 2 | DocDate | DocDate | Duplicit |
| 3 | DocVal | DocVal | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| (BookNum) | PQBLST.BookNum | Kniha prevodných príkazov |

## Stavy odoslania (AboStat)

| Hodnota | Popis | Farba |
|---------|-------|-------|
| (prázdne) | Neodoslaný | Čierna |
| O | Odoslaný do banky | Zelená |

## Použitie

- Evidencia prevodných príkazov
- Sledovanie stavu odoslania
- Podklad pre elektronické bankovníctvo

## Business pravidlá

- DocVal = súčet PayVal zo všetkých PQI položiek
- ItmQnt = počet položiek v PQI
- AboStat='O' zabraňuje opätovnému odoslaniu
- AboDate/AboTime sa nastavia pri exporte do banky

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
