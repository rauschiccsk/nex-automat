# STS - Rezervácie maloobchodného predaja

## Kľúčové slová / Aliases

STS, STS.BTR, stavy zásob, stock status, aktuálne stavy, zostatky

## Popis

Tabuľka neodpočítaných položiek maloobchodného predaja. Obsahuje rezervácie z pokladní, ktoré ešte neboli vyskladnené (odpočítané zo skladu).

## Btrieve súbor

`STSxxxxx.BTR` (x = číslo skladu)

## Umiestnenie

`C:\NEX\YEARACT\STORES\STSxxxxx.BTR`

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo (PLU) |
| SalDate | DateType | 4 | Dátum predaja |
| CasNum | word | 2 | Číslo pokladne |
| SalQnt | double | 8 | Rezervované množstvo |
| DocNum | Str12 | 13 | Interné číslo rezervačného dokladu |
| ItmNum | longint | 4 | Číslo riadku dokladu |
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |

## Indexy (5)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | GsCode | GsCode | Duplicit |
| 1 | SalDate | SalDate | Duplicit |
| 2 | DocNum, ItmNum | DoIt | Duplicit |
| 3 | GsCode, SalDate, CasNum | GcSdCn | Duplicit |
| 4 | GsCode, CasNum | GcCn | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| GsCode | STK.GsCode | Skladová karta |

## Workflow

```
POS predaj → STS záznam (SalQnt)
              ↓
STK.SalQnt += SalQnt
STK.FreQnt -= SalQnt
              ↓
Uzávierka → STM výdaj
              ↓
STS záznam vymazaný
STK.SalQnt -= SalQnt
```

## Účel

- Dočasná rezervácia tovaru pri POS predaji
- Umožňuje real-time aktualizáciu voľného množstva
- Batch spracovanie výdajov pri uzávierke

## Business pravidlá

- Suma STS.SalQnt pre položku = STK.SalQnt
- Pri uzávierke sa vytvorí hromadný STM výdaj
- FreQnt = ActQnt - SalQnt - OcdQnt

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
