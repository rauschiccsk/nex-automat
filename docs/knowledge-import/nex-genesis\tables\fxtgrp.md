# FXTGRP - Daňové odpisové skupiny

## Kľúčové slová / Aliases

FXTGRP, FXTGRP.BTR, daňové, odpisové, skupiny

## Popis

Konfiguračná tabuľka daňových odpisových skupín podľa Zákona o dani z príjmov. Obsahuje sadzby rovnomerného a koeficienty zrýchleného odpisovania pre jednotlivé skupiny a roky. Údaje sa menia pri legislatívnych zmenách.

## Btrieve súbor

`FXTGRP.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\FXTGRP.BTR`

## Štruktúra polí (21 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GrpYear | Str4 | 5 | Rok, na ktorý platí odpis - **PK časť 1** |
| GrpNum | byte | 1 | Číslo odpisovej skupiny (1-6) - **PK časť 2** |
| GrpName | Str20 | 21 | Názov odpisovej skupiny |
| _GrpName | Str20 | 21 | Vyhľadávacie pole názvu |

### Doba odpisovania

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| TsuYear | byte | 1 | Doba odpisovania v rokoch |

### Sadzby rovnomerného odpisovania

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| LiPrcOne | double | 8 | Sadzba pre prvý rok (%) |
| LiPrcNxt | double | 8 | Sadzba pre ďalšie roky (%) |
| LiPrcInc | double | 8 | Sadzba pre zvýšenú cenu (%) |

### Koeficienty zrýchleného odpisovania

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| QcKfcOne | double | 8 | Koeficient pre prvý rok |
| QcKfcNxt | double | 8 | Koeficient pre ostatné roky |
| QcKfcInc | double | 8 | Koeficient pre zvýšenú cenu |

### Vizualizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Emphas | byte | 1 | Farebné zvýraznenie |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ModNum | word | 2 | Počet modifikácií |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |

## Indexy (3)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | GrpYear | GrpYear | Duplicit |
| 1 | GrpYear, GrpNum | YeGn | Duplicit |
| 2 | _GrpName | GrpName | Duplicit, Case-insensitive |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| GrpNum | FXA.TsuGrp | Daňová skupina majetku |

## Odpisové skupiny podľa zákona (aktuálne)

| GrpNum | TsuYear | Príklady majetku |
|--------|---------|------------------|
| 1 | 4 | Osobné automobily, počítače, kancelársky nábytok |
| 2 | 6 | Nákladné vozidlá, stroje, prístroje |
| 3 | 8 | Technologické zariadenia, lode, lietadlá |
| 4 | 12 | Niektoré budovy, trezory |
| 5 | 20 | Väčšina budov, cesty |
| 6 | 40 | Trvalé budovy, mosty, tunely |

## Príklad sadzieb (rok 2024)

### Skupina 1 (4 roky)

| Typ | Prvý rok | Ďalšie roky | Zvýšená cena |
|-----|----------|-------------|--------------|
| Rovnomerné | 25% | 25% | 25% |
| Zrýchlené | 4 | 5 | 4 |

### Skupina 2 (6 rokov)

| Typ | Prvý rok | Ďalšie roky | Zvýšená cena |
|-----|----------|-------------|--------------|
| Rovnomerné | 16.67% | 16.67% | 16.67% |
| Zrýchlené | 6 | 7 | 6 |

## Vzorce odpisovania

### Rovnomerný odpis

```
Prvý rok:    Odpis = VstupnáCena × LiPrcOne / 100
Ďalšie roky: Odpis = VstupnáCena × LiPrcNxt / 100
Zvýšená:     Odpis = ZvýšenáCena × LiPrcInc / 100
```

### Zrýchlený odpis

```
Prvý rok:    Odpis = VstupnáCena / QcKfcOne
Ďalší rok n: Odpis = (2 × Zostatková) / (QcKfcNxt - n + 1)
Zvýšená:     Odpis = (2 × ZvýšenáZostatková) / (QcKfcInc - PočetRokov + 1)
```

## Historické zmeny

| Rok | Zmena |
|-----|-------|
| 2003 | Zvýšenie tech. zhodnotenia na 30 000 SKK |
| 2009 | Konverzia na EUR |
| 2015 | Zmena sadzieb pre niektoré skupiny |
| 2020 | Nové pravidlá pre elektromobily |

## Použitie

- Výpočet daňových odpisov majetku
- Určenie doby odpisovania
- Legislatívna evidencia sadzieb
- Historizácia zmien v zákonoch

## Business pravidlá

- GrpYear určuje platnosť sadzieb
- Pre nový majetok sa použije skupina platná v roku zaradenia
- Pri tech. zhodnotení sa použije LiPrcInc/QcKfcInc
- Skupiny 1-6 sú definované zákonom o dani z príjmov

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
