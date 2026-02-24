# BLCLST - Zoznam účtovných výkazov

## Kľúčové slová / Aliases

BLCLST, BLCLST.BTR, zoznam, účtovných, výkazov

## Popis

Zoznam uložených účtovných výkazov (Súvaha a Výsledovka). Každý záznam reprezentuje jednu uzávierku s vypočítanou súvahou a výsledovkou. Položky výkazov sú uložené v samostatných súboroch SUVnnnnn.BTR a VYSnnnnn.BTR.

## Btrieve súbor

`BLCLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\BLCLST.BTR`

## Štruktúra polí (12 polí)

### Identifikácia výkazu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SerNum | longint | 4 | Poradové číslo výkazu - **PRIMARY KEY** |
| BegDate | DateType | 4 | Začiatočný dátum vyhotovenia výkazu |
| EndDate | DateType | 4 | Konečný dátum vyhotovenia výkazu |
| Describe | Str30 | 31 | Textový popis výkazu |
| _Describe | Str30 | 31 | Vyhľadávacie pole popisu |

### Hospodársky výsledok

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ExSuvVal | double | 8 | Hospodársky výsledok zo súvahy - presný |
| ExVysVal | double | 8 | Hospodársky výsledok z výsledovky - presný |
| RdSuvVal | longint | 4 | Hospodársky výsledok zo súvahy - zaokrúhlený |
| RdVysVal | longint | 4 | Hospodársky výsledok z výsledovky - zaokrúhlený |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |

## Indexy (3)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | SerNum | SerNum | Duplicit |
| 1 | EndDate | EndDate | Duplicit |
| 2 | _Describe | Describe | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| SerNum | SUVnnnnn (súbor) | Výkaz súvahy |
| SerNum | VYSnnnnn (súbor) | Výkaz výsledovky |

## Vzťah k SUV/VYS súborom

Každý záznam v BLCLST má priradené dva súbory:

```
BLCLST.SerNum = nnnnn → SUVnnnnn.BTR (súvaha)
                      → VYSnnnnn.BTR (výsledovka)
```

Príklad:
- BLCLST.SerNum = 1 → SUV00001.BTR, VYS00001.BTR
- BLCLST.SerNum = 25 → SUV00025.BTR, VYS00025.BTR

## Hospodársky výsledok

Porovnanie hodnôt zo súvahy a výsledovky:

| Zdroj | Riadok | Pole |
|-------|--------|------|
| Súvaha | 100 (štandard) / 33 (mikro) | ExNettVal/RdNettVal |
| Výsledovka | 61 (štandard) / 38 (mikro) | ExActVal/RdActVal |

**Kontrola:** ExSuvVal by mal byť rovný ExVysVal

## Použitie

- Evidencia vyhotovených účtovných uzávierok
- Rýchle vyhľadávanie podľa obdobia alebo popisu
- Prehľad hospodárskych výsledkov
- Prístup k archívnym výkazom

## Business pravidlá

- SerNum je automaticky generované poradové číslo
- Pri vytvorení výkazu sa vytvárajú aj súbory SUVnnnnn.BTR a VYSnnnnn.BTR
- Pri zmazaní výkazu sa vymažú aj oba súbory s položkami
- ExSuvVal a ExVysVal by mali byť zhodné (kontrola správnosti výpočtu)

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
