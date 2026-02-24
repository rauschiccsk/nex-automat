# VYSCALC - Kalkulačné vzorce výsledovky

## Kľúčové slová / Aliases

VYSCALC, VYSCALC.BTR, kalkulačné, vzorce, výsledovky

## Popis

Tabuľka kalkulačných vzorcov pre výpočet výsledovky (Výkazu ziskov a strát). Definuje, ktoré účty z účtovnej osnovy sa majú sčítať do jednotlivých riadkov výkazu. Obsahuje aj medzivýsledky výpočtu.

## Btrieve súbor

`VYSCALC.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\VYSCALC.BTR`

## Štruktúra polí (9 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RowNum | word | 2 | Číslo riadku výkazu - **FK VYSDEF** |
| AccSnt | Str3 | 4 | Syntetický účet |
| AccAnl | Str6 | 7 | Analytický účet (* = všetky) |

### Výpočtové pravidlo

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Formula | Str18 | 19 | Vzorec výpočtu (C-D, D-C, C, D) |
| SignSpc | Str1 | 2 | Filter znamienka (+, -, prázdne) |

### Medzivýsledky aktuálneho obdobia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ActCVal | double | 8 | Súčet strany MD - aktuálny rok |
| ActDVal | double | 8 | Súčet strany Dal - aktuálny rok |

### Medzivýsledky minulého obdobia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PrvCVal | double | 8 | Súčet strany MD - minulý rok |
| PrvDVal | double | 8 | Súčet strany Dal - minulý rok |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | RowNum | RowNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| RowNum | VYSDEF.RowNum | Riadok výkazu |
| AccSnt | ACCSNT.AccSnt | Syntetický účet |
| AccSnt + AccAnl | ACCANL | Analytický účet |

## Rozdiel oproti SUVCALC

| Vlastnosť | VYSCALC | SUVCALC |
|-----------|---------|---------|
| Collum | Nie | Áno (Brutto/Korekcia) |
| Počet polí | 9 | 10 |
| Typické účty | 5xx, 6xx | 0xx-4xx |

## Vzorce (Formula)

| Hodnota | Výpočet | Typické použitie |
|---------|---------|------------------|
| C-D | MD - Dal | Výnosové účty (6xx) |
| D-C | Dal - MD | Nákladové účty (5xx) |
| C | MD | Špeciálne prípady |
| D | Dal | Špeciálne prípady |

## Filter znamienka (SignSpc)

| Hodnota | Význam | Príklad |
|---------|--------|---------|
| (prázdne) | Všetky hodnoty | Štandardné účty |
| + | Len kladné zostatky | Výnosy |
| - | Len záporné zostatky | Náklady |

## Wildcard účet

Ak AccAnl = '*', spracujú sa všetky analytické účty daného syntetického účtu.

```
AccSnt='601', AccAnl='*' → všetky účty 601xxx
AccSnt='518', AccAnl='*' → všetky účty 518xxx
```

## Algoritmus výpočtu

```
1. Vynulovanie ActCVal, ActDVal, PrvCVal, PrvDVal
2. Pre každý záznam:
   a. Nájdi účty v JOURNAL podľa AccSnt + AccAnl
   b. Sčítaj CredVal → ActCVal/PrvCVal
   c. Sčítaj DebVal → ActDVal/PrvDVal
3. Výpočet hodnoty podľa Formula:
   - C-D: ActCVal - ActDVal
   - D-C: ActDVal - ActCVal
   - C: ActCVal
   - D: ActDVal
4. Aplikuj SignSpc filter
5. Pripočítaj do VYS.ExActVal a VYS.ExPrevVal
```

## Príklady konfigurácie

### Tržby za vlastné výrobky

| RowNum | AccSnt | AccAnl | Formula | SignSpc |
|--------|--------|--------|---------|---------|
| 1 | 601 | * | C-D | |
| 1 | 602 | * | C-D | |

### Spotreba materiálu a energie

| RowNum | AccSnt | AccAnl | Formula | SignSpc |
|--------|--------|--------|---------|---------|
| 10 | 501 | * | D-C | |
| 10 | 502 | * | D-C | |
| 10 | 503 | * | D-C | |

### Osobné náklady

| RowNum | AccSnt | AccAnl | Formula | SignSpc |
|--------|--------|--------|---------|---------|
| 15 | 521 | * | D-C | |
| 15 | 524 | * | D-C | |
| 15 | 527 | * | D-C | |

## Mapovanie účtových tried

| Trieda | Typ | Formula |
|--------|-----|---------|
| 5xx | Náklady | D-C |
| 6xx | Výnosy | C-D |

## Použitie

- Definícia mapovaní účtov na riadky výsledovky
- Medzivýsledky pre kontrolu výpočtu
- Konfigurácia výpočtových pravidiel
- Prispôsobenie legislatívnym zmenám

## Business pravidlá

- Výnosy (6xx) používajú C-D (MD mínus Dal)
- Náklady (5xx) používajú D-C (Dal mínus MD)
- AccAnl='*' spracuje všetky analytiky
- Medzivýsledky sa vynulujú pred každým výpočtom

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
