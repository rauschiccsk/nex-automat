# VTCLST - Kalkulačné obdobia DPH

## Kľúčové slová / Aliases

VTCLST, VTCLST.BTR, kalkulačné, obdobia, dph

## Popis

Číselník kalkulačných období pre uzávierky DPH. Definuje časové obdobia (mesačné alebo kvartálne) pre výpočet daňovej povinnosti.

## Btrieve súbor

`VTCLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\VTCLST.BTR`

## Štruktúra polí (12 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VtcNum | word | 2 | Číslo kalkulačného obdobia - **PRIMARY KEY** |
| Describe | Str30 | 31 | Textový popis obdobia |

### Obdobie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BegDate | DateType | 4 | Počiatočný dátum obdobia |
| EndDate | DateType | 4 | Konečný dátum obdobia |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | VtcNum | VtcNum | Duplicit |

## Typické obdobia

### Mesačné obdobia

| VtcNum | Describe | BegDate | EndDate |
|--------|----------|---------|---------|
| 1 | Január 2024 | 01.01.2024 | 31.01.2024 |
| 2 | Február 2024 | 01.02.2024 | 29.02.2024 |
| 3 | Marec 2024 | 01.03.2024 | 31.03.2024 |
| ... | ... | ... | ... |
| 12 | December 2024 | 01.12.2024 | 31.12.2024 |

### Kvartálne obdobia

| VtcNum | Describe | BegDate | EndDate |
|--------|----------|---------|---------|
| 1 | Q1 2024 | 01.01.2024 | 31.03.2024 |
| 2 | Q2 2024 | 01.04.2024 | 30.06.2024 |
| 3 | Q3 2024 | 01.07.2024 | 30.09.2024 |
| 4 | Q4 2024 | 01.10.2024 | 31.12.2024 |

## Použitie

- Definícia zdaňovacích období
- Prepojenie s uzávierkami DPH (VTRLST.VtcNum)
- Automatické nastavenie rozsahu dátumov

## Business pravidlá

- Mesačné obdobie pre platiteľov s obratom > 100 000 EUR
- Kvartálne obdobie pre ostatných platiteľov
- Obdobia sa nesmú prekrývať
- VtcNum sa používa v VTRLST pre výber obdobia

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
