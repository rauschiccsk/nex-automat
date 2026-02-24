# VYS - Výkaz ziskov a strát

## Kľúčové slová / Aliases

VYS, VYS.BTR, výkaz, ziskov, strát

## Popis

Archívny výkaz ziskov a strát (Profit & Loss Statement / Income Statement). Obsahuje vypočítané hodnoty všetkých riadkov výsledovky za konkrétne obdobie. Každý výkaz má vlastný súbor VYSnnnnn.BTR kde nnnnn je SerNum z BLCLST.

## Btrieve súbor

`VYSnnnnn.BTR` (nnnnn = SerNum z BLCLST)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\VYSnnnnn.BTR`

## Štruktúra polí (8 polí)

### Identifikácia riadku

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RowNum | word | 2 | Číslo riadku výkazu - **PRIMARY KEY** |
| Marking | Str10 | 11 | Označenie riadku (napr. I., II.1) |
| Text | Str160 | 161 | Text/názov riadku |

### Presné hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ExActVal | double | 8 | Hodnota aktuálneho obdobia - presná |
| ExPrevVal | double | 8 | Hodnota minulého obdobia - presná |

### Zaokrúhlené hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RdActVal | longint | 4 | Hodnota aktuálneho obdobia - zaokrúhlená |
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

### Zaokrúhľovanie

```
RdActVal = Round(ExActVal)
RdPrevVal = Round(ExPrevVal)
```

## Štruktúra stĺpcov

| Stĺpec | Ex* pole | Rd* pole | Popis |
|--------|----------|----------|-------|
| Bežné obdobie | ExActVal | RdActVal | Aktuálny rok |
| Minulé obdobie | ExPrevVal | RdPrevVal | Predchádzajúci rok |

## Rozdiel oproti SUV

| Vlastnosť | VYS | SUV |
|-----------|-----|-----|
| Počet stĺpcov | 2 | 4 |
| Brutto/Korekcia | Nie | Áno |
| Typický počet riadkov | 60-70 | 120+ |
| Polí | 8 | 11 |

## Špeciálne riadky

| RowNum | Účel | Výpočet |
|--------|------|---------|
| 61 | Hospodársky výsledok (štandard) | Výnosy - Náklady |
| 38 | Hospodársky výsledok (mikro) | Výnosy - Náklady |
| 99 | Kontrolný súčet | Súčet všetkých riadkov |

## Kontrola hospodárskeho výsledku

Hospodársky výsledok z výsledovky by mal súhlasiť so súvahou:

```
VYS.ExActVal(r.61) = SUV.ExNettVal(r.100)
VYS.RdActVal(r.61) = SUV.RdNettVal(r.100)
```

## Varianty výkazu

### Štandardný výkaz
- Plná štruktúra podľa legislatívy
- Celkom 60-70 riadkov
- Riadok 61 = hospodársky výsledok

### Mikro výkaz
- Zjednodušená štruktúra (≤45 riadkov)
- Pre mikro účtovné jednotky
- Riadok 38 = hospodársky výsledok

## Interpretácia hodnôt

| ExActVal | Význam |
|----------|--------|
| > 0 | Zisk (pre výsledkové riadky) |
| < 0 | Strata (pre výsledkové riadky) |
| > 0 | Výnos (pre výnosové riadky) |
| < 0 | Náklad (pre nákladové riadky) |

## Použitie

- Archivácia vypočítaných výsledoviek
- Tlač výkazu (VYS, VYS_M)
- Porovnávanie období
- Audit účtovnej závierky
- Výpočet hospodárskeho výsledku

## Business pravidlá

- Každý výkaz má vlastný súbor (archív)
- Výnosy = účty triedy 6
- Náklady = účty triedy 5
- Hospodársky výsledok = Výnosy - Náklady
- Hodnoty sa preberajú z VYSDEF pri vytvorení

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
