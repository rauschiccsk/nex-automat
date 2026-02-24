# ACBLST - Knihy akciových precenení

## Kľúčové slová / Aliases

ACBLST, ACBLST.BTR, knihy, akciových, precenení

## Popis

Konfiguračná tabuľka kníh akciových precenení tovaru. Obsahuje nastavenia knihy vrátane väzby na predajný cenník, spôsobu zaokrúhľovania a tlače etikiet.

## Btrieve súbor

`ACBLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ACBLST.BTR`

## Štruktúra polí (17 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy dokladov akciových precenení - **PK** |
| BookName | Str30 | 31 | Názov knihy |
| _BookName | Str30 | 31 | Vyhľadávacie pole názvu |
| BookYear | Str4 | 5 | Rok, na ktorý je založená kniha |
| SerNum | byte | 1 | Poradové číslo knihy |

### Konfigurácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PlsNum | longint | 4 | Poradové číslo predajného cenníka - **FK PLSLST** |
| RndType | byte | 1 | Spôsob zaokrúhľovania predajnej ceny |
| Weight | byte | 1 | Rezervované |
| LabPrn | byte | 1 | Prepínač automatickej tlače cenovkovej etikety |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BookNum | BookNum | Duplicit |
| 1 | _BookName | BookName | Duplicit, Case-insensitive |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PlsNum | PLSLST.PlsNum | Predajný cenník |
| BookNum | ACH.BookNum | Hlavičky dokladov |
| BookNum | ACI.BookNum | Položky dokladov |

## Spôsoby zaokrúhľovania (RndType)

| Hodnota | Popis |
|---------|-------|
| 0 | Bez zaokrúhľovania |
| 1 | Na 0.01 EUR |
| 2 | Na 0.05 EUR |
| 3 | Na 0.10 EUR |
| 5 | Na 0.50 EUR |
| 10 | Na 1.00 EUR |

## Použitie

- Konfigurácia kníh akciových precenení
- Väzba na predajný cenník (PLS)
- Nastavenie zaokrúhľovania a tlače

## Business pravidlá

- PlsNum určuje, ktorý cenník sa aktualizuje
- LabPrn=1 aktivuje automatickú tlač etikiet
- Kniha musí mať väzbu na existujúci PLSLST

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
