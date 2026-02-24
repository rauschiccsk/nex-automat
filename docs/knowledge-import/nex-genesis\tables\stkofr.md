# STKOFR - Ponuky od dodávateľov

## Kľúčové slová / Aliases

STKOFR, STKOFR.BTR, skladové ponuky, stock offers, rezervácie

## Popis

Tabuľka dostupných množstiev (ponúk) od dodávateľov. Umožňuje evidovať, koľko tovaru je možné objednať u jednotlivých dodávateľov.

## Btrieve súbor

`STKOFR.BTR`

## Umiestnenie

`C:\NEX\YEARACT\STORES\STKOFR.BTR`

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | word | 2 | Číslo skladu |
| GsCode | longint | 4 | Produktové číslo (PLU) |
| PaCode | longint | 4 | Kód dodávateľa |
| OfrQnt | double | 8 | Dostupné množstvo |
| Status | Str1 | 2 | Stav položky (zatiaľ nepoužité) |
| ModUser | Str10 | 11 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (5)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | StkNum | StkNum | Duplicit |
| 1 | StkNum, GsCode | SnGc | Duplicit |
| 2 | StkNum, PaCode | SnPa | Duplicit |
| 3 | StkNum, GsCode, PaCode | SnGcPa | Duplicit |
| 4 | Status | Status | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| StkNum | STKLST.StkNum | Sklad |
| GsCode | STK.GsCode | Skladová karta |
| PaCode | PAB.PaCode | Dodávateľ |

## Business pravidlá

- Jeden tovar môže mať ponuky od viacerých dodávateľov
- Suma OfrQnt pre položku = STK.OfrQnt
- Aktualizácia z cenníkov dodávateľov alebo manuálne

## Príklad dát

| StkNum | GsCode | PaCode | OfrQnt |
|--------|--------|--------|--------|
| 1 | 10001 | 501 | 100 |
| 1 | 10001 | 502 | 50 |
| 1 | 10002 | 501 | 200 |

## Použitie

- Plánovanie nákupu
- Výber dodávateľa pri objednávke
- Sledovanie dostupnosti tovaru

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
