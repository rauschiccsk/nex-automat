# SUVDEF - Definícia výkazu súvahy

## Kľúčové slová / Aliases

SUVDEF, SUVDEF.BTR, definícia, výkazu, súvahy

## Popis

Definícia štruktúry výkazu súvahy (Balance Sheet). Obsahuje zoznam riadkov výkazu s ich názvami a spôsobom výpočtu. Slúži ako šablóna pre generovanie konkrétnych výkazov.

## Btrieve súbor

`SUVDEF.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\SUVDEF.BTR`

## Štruktúra polí (5 polí)

### Identifikácia riadku

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RowNum | word | 2 | Číslo riadku výkazu - **PRIMARY KEY** |
| Marking | Str10 | 11 | Označenie riadku (napr. A., B.I., C.II.1) |
| Text | Str160 | 161 | Text/názov riadku výkazu |

### Výpočet

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RowSum | byte | 1 | Typ riadku (0=kalkulačný, 1=súčtový) |
| CalcRows | Str100 | 101 | Vzorec pre súčtové riadky |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | RowNum | RowNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| RowNum | SUVCALC.RowNum | Kalkulačné vzorce |

## Typy riadkov

### Kalkulačný riadok (RowSum = 0)

- Hodnota sa počíta z účtov v SUVCALC
- CalcRows je prázdne
- Príklad: "Pohľadávky" - súčet účtov triedy 31x

### Súčtový riadok (RowSum = 1)

- Hodnota sa počíta zo súčtu iných riadkov
- CalcRows obsahuje vzorec
- Príklad: "Obežný majetok spolu" = SUM(riadky obežného majetku)

## Formát CalcRows

```
Základné operácie:
"SUM(1..10)"      - Súčet riadkov 1 až 10
"1+2+3"           - Súčet riadkov 1, 2 a 3
"10-5"            - Riadok 10 mínus riadok 5
"-5"              - Záporná hodnota riadku 5

Kombinované:
"SUM(1..5)+SUM(10..15)"  - Kombinácia súčtov
"SUM(1..10)-20"          - Súčet mínus jeden riadok
```

## Štruktúra súvahy

### Aktíva (riadky 1-64)

| Rozsah | Skupina |
|--------|---------|
| 1-20 | Neobežný majetok |
| 21-40 | Obežný majetok |
| 41-64 | Časové rozlíšenie |

### Pasíva (riadky 65-118)

| Rozsah | Skupina |
|--------|---------|
| 65-80 | Vlastné imanie |
| 81-100 | Záväzky |
| 101-118 | Časové rozlíšenie |

### Kontrolné riadky

| Riadok | Účel |
|--------|------|
| 888 | Kontrolný súčet Aktív |
| 999 | Kontrolný súčet Pasív |

## Použitie

- Definícia štruktúry výkazu súvahy
- Šablóna pre generovanie SUVnnnnn
- Konfigurácia výpočtových pravidiel
- Prispôsobenie legislatívnym zmenám

## Business pravidlá

- Štruktúra zodpovedá slovenskej legislatíve (Opatrenie MF SR)
- Riadky s RowSum=0 musia mať záznamy v SUVCALC
- Riadky s RowSum=1 musia mať vyplnený CalcRows
- Označenia (Marking) zodpovedajú oficiálnemu formuláru

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
