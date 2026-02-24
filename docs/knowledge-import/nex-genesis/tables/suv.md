# SUV - Výkaz súvahy

## Kľúčové slová / Aliases

SUV, SUV.BTR, výkaz, súvahy

## Popis

Archívny výkaz súvahy (Balance Sheet). Obsahuje vypočítané hodnoty všetkých riadkov súvahy za konkrétne obdobie. Každý výkaz má vlastný súbor SUVnnnnn.BTR kde nnnnn je SerNum z BLCLST.

## Btrieve súbor

`SUVnnnnn.BTR` (nnnnn = SerNum z BLCLST)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\SUVnnnnn.BTR`

## Štruktúra polí (11 polí)

### Identifikácia riadku

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RowNum | word | 2 | Číslo riadku výkazu - **PRIMARY KEY** |
| Marking | Str10 | 11 | Označenie riadku (napr. A., B.I.) |
| Text | Str160 | 161 | Text/názov riadku |

### Presné hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ExBrutVal | double | 8 | Brutto hodnota - presná |
| ExCorrVal | double | 8 | Korekcia - presná |
| ExNettVal | double | 8 | Netto hodnota - presná |
| ExPrevVal | double | 8 | Hodnota minulého obdobia - presná |

### Zaokrúhlené hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RdBrutVal | longint | 4 | Brutto hodnota - zaokrúhlená na EUR |
| RdCorrVal | longint | 4 | Korekcia - zaokrúhlená na EUR |
| RdNettVal | longint | 4 | Netto hodnota - zaokrúhlená na EUR |
| RdPrevVal | longint | 4 | Hodnota minulého obdobia - zaokrúhlená |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | RowNum | RowNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| (súbor) | BLCLST.SerNum | Hlavička výkazu |

## Výpočtové pravidlá

### Netto hodnota

```
ExNettVal = ExBrutVal - ExCorrVal
RdNettVal = RdBrutVal - RdCorrVal
```

### Zaokrúhľovanie

```
RdBrutVal = Round(ExBrutVal)
RdCorrVal = Round(ExCorrVal)
RdNettVal = RdBrutVal - RdCorrVal  (nie Round(ExNettVal)!)
RdPrevVal = Round(ExPrevVal)
```

## Štruktúra stĺpcov

| Stĺpec | Ex* pole | Rd* pole | Popis |
|--------|----------|----------|-------|
| Brutto | ExBrutVal | RdBrutVal | Hrubá hodnota aktív |
| Korekcia | ExCorrVal | RdCorrVal | Oprávky, opravné položky |
| Netto | ExNettVal | RdNettVal | Čistá hodnota (Brutto - Korekcia) |
| Min. obdobie | ExPrevVal | RdPrevVal | Porovnávacie obdobie |

## Špeciálne riadky

| RowNum | Účel | Výpočet |
|--------|------|---------|
| 64 | Aktíva spolu | SUM(1..64) |
| 118 | Pasíva spolu | SUM(65..118) |
| 100 | Hospodársky výsledok | Výsledok bežného obdobia |
| 888 | Kontrolný súčet Aktív | Súčet všetkých riadkov Aktív |
| 999 | Kontrolný súčet Pasív | Súčet všetkých riadkov Pasív |

## Bilančná kontrola

Správny výkaz musí spĺňať:

```
RdNettVal(r.64) = RdNettVal(r.118)  // Aktíva = Pasíva
RdNettVal(r.888) = kontrolný súčet aktív
RdNettVal(r.999) = kontrolný súčet pasív
```

## Varianty výkazu

### Štandardný výkaz
- Riadky 1-64 (Aktíva), 65-118 (Pasíva)
- Celkom cca 120+ riadkov

### Mikro výkaz
- Zjednodušená štruktúra (≤45 riadkov)
- Pre mikro účtovné jednotky
- Riadky 1-23 (Aktíva), 24-33 (Pasíva)

## Použitie

- Archivácia vypočítaných súvah
- Tlač výkazu (SUV_A, SUV_P)
- Porovnávanie období
- Audit účtovnej závierky

## Business pravidlá

- Každý výkaz má vlastný súbor (archív)
- Brutto = účty triedy 0-3 (aktíva)
- Korekcia = účty oprávok (08x, 09x)
- Pasíva nemajú Brutto/Korekcia (len Netto)
- Hodnoty sa preberajú z SUVDEF pri vytvorení

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
