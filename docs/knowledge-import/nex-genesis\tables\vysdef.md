# VYSDEF - Definícia výkazu výsledovky

## Kľúčové slová / Aliases

VYSDEF, VYSDEF.BTR, definícia, výkazu, výsledovky

## Popis

Definícia štruktúry výkazu ziskov a strát (Profit & Loss Statement). Obsahuje zoznam riadkov výkazu s ich názvami a spôsobom výpočtu. Slúži ako šablóna pre generovanie konkrétnych výkazov.

## Btrieve súbor

`VYSDEF.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\VYSDEF.BTR`

## Štruktúra polí (7 polí)

### Identifikácia riadku

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RowNum | word | 2 | Číslo riadku výkazu - **PRIMARY KEY** |
| Marking | Str10 | 11 | Označenie riadku (napr. I., II.1) |
| Text | Str160 | 161 | Text/názov riadku výkazu |

### Historické hodnoty (minulé obdobie)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ActVal | double | 8 | Hodnota aktuálneho obdobia (nepoužíva sa) |
| OldVal | double | 8 | Hodnota minulého obdobia (manuálne zadaná) |

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
| RowNum | VYSCALC.RowNum | Kalkulačné vzorce |

## Typy riadkov

### Kalkulačný riadok (RowSum = 0)

- Hodnota sa počíta z účtov v VYSCALC
- CalcRows je prázdne
- Príklad: "Tržby za vlastné výrobky" - súčet účtov 601, 602

### Súčtový riadok (RowSum = 1)

- Hodnota sa počíta zo súčtu iných riadkov
- CalcRows obsahuje vzorec
- Príklad: "Výnosy z hospodárskej činnosti" = SUM(riadky výnosov)

## Formát CalcRows

```
Základné operácie:
"SUM(1..10)"      - Súčet riadkov 1 až 10
"1+2+3"           - Súčet riadkov 1, 2 a 3
"10-5"            - Riadok 10 mínus riadok 5
"-5"              - Záporná hodnota riadku 5

Kombinované:
"SUM(1..5)+SUM(10..15)"  - Kombinácia súčtov
```

## Štruktúra výsledovky

### Výnosy z hospodárskej činnosti

| Rozsah | Skupina |
|--------|---------|
| 1-10 | Tržby za vlastné výrobky a služby |
| 11-20 | Ostatné výnosy |

### Náklady na hospodársku činnosť

| Rozsah | Skupina |
|--------|---------|
| 21-40 | Materiálové náklady |
| 41-50 | Osobné náklady |
| 51-55 | Odpisy a opravné položky |

### Výsledky

| Riadok | Popis |
|--------|-------|
| 56-60 | Finančný výsledok |
| 61 | Výsledok hospodárenia (mikro: 38) |
| 99 | Kontrolný súčet |

## Porovnanie s SUVDEF

| Vlastnosť | VYSDEF | SUVDEF |
|-----------|--------|--------|
| Stĺpce | 2 (Akt, Min) | 4 (Brutto, Kor, Netto, Min) |
| ActVal/OldVal | Áno | Nie |
| Typický počet riadkov | 60-70 | 120+ |

## Použitie

- Definícia štruktúry výkazu ziskov a strát
- Šablóna pre generovanie VYSnnnnn
- Konfigurácia výpočtových pravidiel
- Manuálne zadanie hodnôt minulého obdobia

## Business pravidlá

- Štruktúra zodpovedá slovenskej legislatíve
- Riadky s RowSum=0 musia mať záznamy v VYSCALC
- Riadky s RowSum=1 musia mať vyplnený CalcRows
- OldVal umožňuje manuálne zadanie pre porovnanie

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
