# SUVCALC - Kalkulačné vzorce súvahy

## Kľúčové slová / Aliases

SUVCALC, SUVCALC.BTR, kalkulačné, vzorce, súvahy

## Popis

Tabuľka kalkulačných vzorcov pre výpočet súvahy. Definuje, ktoré účty z účtovnej osnovy sa majú sčítať do jednotlivých riadkov výkazu súvahy. Obsahuje aj medzivýsledky výpočtu.

## Btrieve súbor

`SUVCALC.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\SUVCALC.BTR`

## Štruktúra polí (10 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RowNum | word | 2 | Číslo riadku výkazu - **FK SUVDEF** |
| AccSnt | Str3 | 4 | Syntetický účet |
| AccAnl | Str6 | 7 | Analytický účet (* = všetky) |

### Výpočtové pravidlo

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Formula | Str18 | 19 | Vzorec výpočtu (C-D, D-C, C, D) |
| SignSpc | Str1 | 2 | Filter znamienka (+, -, prázdne) |
| Collum | byte | 1 | Stĺpec výkazu (0=Brutto, 1=Korekcia) |

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
| RowNum | SUVDEF.RowNum | Riadok výkazu |
| AccSnt | ACCSNT.AccSnt | Syntetický účet |
| AccSnt + AccAnl | ACCANL | Analytický účet |

## Vzorce (Formula)

| Hodnota | Výpočet | Typické použitie |
|---------|---------|------------------|
| C-D | MD - Dal | Aktívne účty |
| D-C | Dal - MD | Pasívne účty |
| C | MD | Len strana MD |
| D | Dal | Len strana Dal |

## Filter znamienka (SignSpc)

| Hodnota | Význam | Príklad |
|---------|--------|---------|
| (prázdne) | Všetky hodnoty | Štandardné účty |
| + | Len kladné zostatky | Pohľadávky (aktivácia) |
| - | Len záporné zostatky | Pohľadávky (pasivizácia) |

## Stĺpec (Collum)

| Hodnota | Stĺpec | Príklad |
|---------|--------|---------|
| 0 | Brutto | Majetkové účty (01x, 02x, 03x) |
| 1 | Korekcia | Oprávky (07x, 08x, 09x) |

## Wildcard účet

Ak AccAnl = '*', spracujú sa všetky analytické účty daného syntetického účtu.

```
AccSnt='311', AccAnl='*' → všetky účty 311xxx
AccSnt='022', AccAnl='*' → všetky účty 022xxx
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
5. Pripočítaj do SUV.ExBrutVal alebo SUV.ExCorrVal podľa Collum
```

## Príklady konfigurácie

### Dlhodobý hmotný majetok (Brutto)

| RowNum | AccSnt | AccAnl | Formula | SignSpc | Collum |
|--------|--------|--------|---------|---------|--------|
| 10 | 021 | * | C-D | | 0 |
| 10 | 022 | * | C-D | | 0 |
| 10 | 029 | * | C-D | | 0 |

### Oprávky k DHM (Korekcia)

| RowNum | AccSnt | AccAnl | Formula | SignSpc | Collum |
|--------|--------|--------|---------|---------|--------|
| 10 | 081 | * | D-C | | 1 |
| 10 | 082 | * | D-C | | 1 |
| 10 | 089 | * | D-C | | 1 |

### Pohľadávky s rozlíšením znamienka

| RowNum | AccSnt | AccAnl | Formula | SignSpc | Collum |
|--------|--------|--------|---------|---------|--------|
| 35 | 311 | * | C-D | + | 0 |
| 90 | 311 | * | C-D | - | 0 |

## Použitie

- Definícia mapovaní účtov na riadky súvahy
- Medzivýsledky pre kontrolu výpočtu
- Konfigurácia výpočtových pravidiel
- Prispôsobenie legislatívnym zmenám

## Business pravidlá

- Jeden účet môže byť v riadkoch Brutto aj Korekcia
- SignSpc umožňuje rozdeliť saldo podľa znamienka
- AccAnl='*' spracuje všetky analytiky
- Medzivýsledky sa vynulujú pred každým výpočtom

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
