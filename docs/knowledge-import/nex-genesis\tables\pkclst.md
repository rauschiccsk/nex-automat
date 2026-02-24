# PKCLST - Zoznam koeficientov prebalenia

## Kľúčové slová / Aliases

PKCLST, PKCLST.BTR, zoznam, koeficientov, prebalenia

## Popis

Číselník prebaľovacích predpisov (receptúr). Definuje koeficienty transformácie medzi zdrojovým a cieľovým tovarom. Umožňuje rýchle zadávanie prebalenia s preddefinovanými množstvami.

## Btrieve súbor

`PKCLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\PKCLST.BTR`

## Štruktúra polí (19 polí)

### Zdrojový tovar (Sc* = Source)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ScGsCode | longint | 4 | Tovarové číslo zdrojového tovaru - **PK časť** |
| ScGsName | Str30 | 31 | Názov zdrojového tovaru |
| _ScGsName | Str30 | 31 | Názov zdrojového tovaru - vyhľadávanie |
| ScBarCode | Str15 | 16 | Identifikačný kód zdrojového tovaru |
| ScGsKfc | double | 8 | Množstvo/koeficient zdrojového tovaru |

### Cieľový tovar (Tg* = Target)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| TgGsCode | longint | 4 | Tovarové číslo cieľového tovaru - **PK časť** |
| TgGsName | Str30 | 31 | Názov cieľového tovaru |
| _TgGsName | Str30 | 31 | Názov cieľového tovaru - vyhľadávanie |
| TgBarCode | Str15 | 16 | Identifikačný kód cieľového tovaru |
| TgGsKfc | double | 8 | Množstvo/koeficient cieľového tovaru |

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

## Indexy (7)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | ScGsCode, TgGsCode | SgTg | Duplicit |
| 1 | ScGsCode | ScGsCode | Duplicit |
| 2 | ScGsName | ScGsName | Duplicit, Case-insensitive |
| 3 | ScBarCode | ScBarCode | Duplicit |
| 4 | TgGsCode | TgGsCode | Duplicit |
| 5 | TgGsName | TgGsName | Duplicit, Case-insensitive |
| 6 | TgBarCode | TgBarCode | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| ScGsCode | GSCAT.GsCode | Zdrojový produkt |
| TgGsCode | GSCAT.GsCode | Cieľový produkt |

## Príklady prebaľovacích predpisov

| ScGsCode | ScGsKfc | TgGsCode | TgGsKfc | Popis |
|----------|---------|----------|---------|-------|
| 1001 | 1 | 1002 | 12 | 1 kartón = 12 kusov |
| 2001 | 1 | 2002 | 100 | 1 paleta = 100 kusov |
| 3001 | 10 | 3002 | 1 | 10 kg = 1 vrece |

## Použitie

- Predpisy pre opakujúce sa prebalenia
- Rýchle zadávanie položiek
- Štandardizácia prebaľovacích operácií

## Business pravidlá

- ScGsKfc : TgGsKfc definuje pomer prebalenia
- Jeden zdrojový tovar môže mať viac cieľových tovarov
- Koeficienty sa používajú na výpočet množstiev v položkách
- Príklad: ak ScGsKfc=1 a TgGsKfc=12, potom 1 zdroj = 12 cieľov

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
