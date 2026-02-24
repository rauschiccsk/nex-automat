# APL - Zoznam akciových tovarov (legacy)

## Kľúčové slová / Aliases

APL, APL.BTR, zoznam, akciových, tovarov, legacy

## Popis

Staršia verzia tabuľky akciových tovarov. Používa sa v kombinácii s APLLST/APLITM pre spätnú kompatibilitu. Obsahuje základné údaje o akciovom tovare bez rozšírených funkcií.

## Btrieve súbor

`APLnnnnn.BTR` (nnnnn = číslo cenníka)

## Umiestnenie

`C:\NEX\YEARACT\STK\APLnnnnn.BTR`

## Štruktúra polí (18 polí)

### Identifikácia tovaru

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo (PLU) |
| GsName | Str30 | 31 | Názov tovaru |
| _GsName | Str20 | 21 | Vyhľadávacie pole názvu |
| BarCode | Str15 | 16 | Identifikačný kód tovaru |

### Obdobie akcie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BegDate | DateType | 4 | Dátum začiatku akcie |
| EndDate | DateType | 4 | Dátum ukončenia akcie |

### Ceny

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| APrice | double | 8 | Aktuálna predajná cena bez DPH |
| BPrice | double | 8 | Aktuálna predajná cena s DPH |

### Stav

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
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

## Indexy (4)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | GsCode | GsCode | Duplicit |
| 1 | _GsName | GsName | Duplicit, Case-insensitive |
| 2 | BarCode | BarCode | Duplicit, Case-insensitive |
| 3 | Sended | Sended | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| GsCode | GSCAT.GsCode | Katalóg produktov |

## Použitie

- Legacy podpora pre staršie inštalácie
- Jednoduchá evidencia akciových cien
- Bez rozšírených funkcií (periodicita, minimálne množstvo)

## Business pravidlá

- Jednoduchšia štruktúra ako APLITM
- Akcia platí od BegDate do EndDate
- APrice/BPrice sú priamo akciové ceny (nie je PcAPrice/PcBPrice)

## Poznámka

Táto tabuľka je nahradená kombináciou APLLST + APLITM, ktoré poskytujú viac funkcií (periodicita, časový interval, minimálne množstvo, typ akcie).

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
