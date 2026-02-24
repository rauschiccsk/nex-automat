# VTRAWR - Hodnoty daňového priznania

## Kľúčové slová / Aliases

VTRAWR, VTRAWR.BTR, hodnoty, daňového, priznania

## Popis

Kumulatívna tabuľka hodnôt daňového priznania. Obsahuje 40 riadkov formulára daňového priznania k DPH podľa predpísaného vzoru Finančnej správy SR.

## Btrieve súbor

`VTRAWR.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\VTRAWR.BTR`

## Štruktúra polí (41 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ClsNum | Str5 | 6 | Číslo uzávierky DPH (yynnn) - **FK VTRLST** |

### Hodnoty riadkov daňového priznania

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Value01 | double | 8 | Hodnota riadku 01 |
| Value02 | double | 8 | Hodnota riadku 02 |
| Value03 | double | 8 | Hodnota riadku 03 |
| Value04 | double | 8 | Hodnota riadku 04 |
| Value05 | double | 8 | Hodnota riadku 05 |
| Value06 | double | 8 | Hodnota riadku 06 |
| Value07 | double | 8 | Hodnota riadku 07 |
| Value08 | double | 8 | Hodnota riadku 08 |
| Value09 | double | 8 | Hodnota riadku 09 |
| Value10 | double | 8 | Hodnota riadku 10 |
| Value11 | double | 8 | Hodnota riadku 11 |
| Value12 | double | 8 | Hodnota riadku 12 |
| Value13 | double | 8 | Hodnota riadku 13 |
| Value14 | double | 8 | Hodnota riadku 14 |
| Value15 | double | 8 | Hodnota riadku 15 |
| Value16 | double | 8 | Hodnota riadku 16 |
| Value17 | double | 8 | Hodnota riadku 17 |
| Value18 | double | 8 | Hodnota riadku 18 |
| Value19 | double | 8 | Hodnota riadku 19 |
| Value20 | double | 8 | Hodnota riadku 20 |
| Value21 | double | 8 | Hodnota riadku 21 |
| Value22 | double | 8 | Hodnota riadku 22 |
| Value23 | double | 8 | Hodnota riadku 23 |
| Value24 | double | 8 | Hodnota riadku 24 |
| Value25 | double | 8 | Hodnota riadku 25 |
| Value26 | double | 8 | Hodnota riadku 26 |
| Value27 | double | 8 | Hodnota riadku 27 |
| Value28 | double | 8 | Hodnota riadku 28 |
| Value29 | double | 8 | Hodnota riadku 29 |
| Value30 | double | 8 | Hodnota riadku 30 |
| Value31 | double | 8 | Hodnota riadku 31 |
| Value32 | double | 8 | Hodnota riadku 32 |
| Value33 | double | 8 | Hodnota riadku 33 |
| Value34 | double | 8 | Hodnota riadku 34 |
| Value35 | double | 8 | Hodnota riadku 35 |
| Value36 | double | 8 | Hodnota riadku 36 |
| Value37 | double | 8 | Hodnota riadku 37 |
| Value38 | double | 8 | Hodnota riadku 38 |
| Value39 | double | 8 | Hodnota riadku 39 |
| Value40 | double | 8 | Hodnota riadku 40 |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | ClsNum | ClsNum | Unikátny |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| ClsNum | VTRLST.ClsNum | Uzávierka DPH |

## Mapovanie riadkov daňového priznania

### Sekcia I - Daň na výstupe

| Riadok | Popis |
|--------|-------|
| 01-02 | Dodanie tovarov a služieb (základná sadzba) |
| 03-04 | Dodanie tovarov a služieb (znížená sadzba) |
| 05-06 | Nadobudnutie tovaru z EÚ |
| 07-08 | Prijatie služby z EÚ (§ 69 ods. 3) |

### Sekcia II - Daň na vstupe

| Riadok | Popis |
|--------|-------|
| 19-20 | Odpočítanie dane z tuzemských nákupov |
| 21-22 | Odpočítanie dane z dovozu |
| 23-24 | Odpočítanie dane z nadobudnutia v EÚ |

### Sekcia III - Výsledná daň

| Riadok | Popis |
|--------|-------|
| 33 | Vlastná daňová povinnosť |
| 34 | Nadmerný odpočet |
| 35 | Odpočet v ďalšom období |

## Použitie

- Podklad pre XML export daňového priznania
- Tlač formulára daňového priznania
- Archivácia hodnôt podania

## Business pravidlá

- Jeden záznam na jednu uzávierku (1:1 s VTRLST)
- Hodnoty sa počítajú z VTR dokladov
- Formát zodpovedá tlačivu Finančnej správy SR
- Pri oprave sa vytvára nový záznam (SttTyp='O')

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
