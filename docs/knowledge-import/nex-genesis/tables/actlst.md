# ACTLST - Zoznam výkazov obratovej predvahy

## Kľúčové slová / Aliases

ACTLST, ACTLST.BTR, zoznam, výkazov, obratovej, predvahy

## Popis

Tabuľka hlavičiek (zoznam) archívnych výkazov obratovej predvahy. Každý záznam reprezentuje jeden vygenerovaný výkaz s definovaným obdobím a parametrami filtrovania. Položky výkazu sú uložené v samostatnom súbore ACTnnnnn.BTR.

## Btrieve súbor

`ACTLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ACTLST.BTR`

## Štruktúra polí (15 polí)

### Identifikácia výkazu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SerNum | longint | 4 | Poradové číslo výkazu - **PRIMARY KEY** |
| Describe | Str60 | 61 | Textový popis výkazu |
| _Describe | Str60 | 61 | Vyhľadávacie pole popisu (case-insensitive) |

### Obdobie výkazu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FrsDate | DateType | 4 | Počiatočný dátum roka |
| BegDate | DateType | 4 | Začiatočný dátum vyhotovenia výkazu |
| EndDate | DateType | 4 | Konečný dátum vyhotovenia výkazu |
| MthNum | byte | 1 | Číslo mesiaca (1-12), na ktorý je vyhotovený výkaz |
| MthName | Str10 | 11 | Názov mesiaca (napr. "Január") |

### Filtrovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CntNum | word | 2 | Číslo strediska - **FK CNTLST** |
| WriNums | Str60 | 61 | Prevádzkové jednotky (čiarkou oddelený zoznam) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |

## Indexy (5)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | SerNum | SerNum | Duplicit |
| 1 | BegDate | BegDate | Duplicit |
| 2 | EndDate | EndDate | Duplicit |
| 3 | _Describe | Describe | Duplicit, Case-insensitive |
| 4 | MthNum | MthNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| CntNum | CNTLST.CntNum | Stredisko |
| SerNum | ACTnnnnn (súbor) | Položky výkazu |

## Vzťah k ACT súborom

Každý záznam v ACTLST má priradený súbor s položkami:

```
ACTLST.SerNum = nnnnn → ACTnnnnn.BTR
```

Príklad:
- ACTLST.SerNum = 123 → ACT00123.BTR
- ACTLST.SerNum = 1 → ACT00001.BTR

## Filtrovanie WriNums

Pole WriNums obsahuje zoznam prevádzkových jednotiek oddelených čiarkou:

```
WriNums = "1,2,5,8"  → Výkaz za prevádzkové jednotky 1, 2, 5 a 8
WriNums = "1"        → Výkaz za prevádzkovu jednotku 1
WriNums = ""         → Výkaz za všetky prevádzkové jednotky
```

## Použitie

- Evidencia vygenerovaných výkazov
- Rýchle vyhľadávanie podľa obdobia alebo popisu
- Archivácia výkazov obratovej predvahy
- Prehľad histórie výkazov

## Business pravidlá

- SerNum je automaticky generované poradové číslo
- Pri vytvorení výkazu sa vytvorí aj súbor ACTnnnnn.BTR s položkami
- Pri zmazaní výkazu sa vymaže aj súbor s položkami
- MthNum automaticky nastaví BegDate a EndDate na prvý/posledný deň mesiaca
- CntNum automaticky načíta príslušné WriNums zo strediska

## Porovnanie s ACCTRN

| Vlastnosť | ACTLST/ACT | ACCTRN |
|-----------|------------|--------|
| Typ | Archívne výkazy | Operatívna predvaha |
| Životnosť | Trvalá | Regenerovaná |
| Počet súborov | Viac (ACTnnnnn) | Jeden (ACCTRN) |
| Mesačné obraty | Nie (len celkové) | Áno (01-12) |
| Predchádzajúce obdobie | Áno (CPrvVal/DPrvVal) | Nie |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
