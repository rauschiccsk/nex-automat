# FXAASD - Údaje vyradenia majetku

## Kľúčové slová / Aliases

FXAASD, FXAASD.BTR, údaje, vyradenia, majetku

## Popis

Tabuľka detailných údajov o vyradení dlhodobého majetku z užívania. Obsahuje kompletné informácie pre protokol o vyradení vrátane dôvodu, účastníkov, technického stavu a finančného vyúčtovania.

## Btrieve súbor

`FXAASD.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\FXAASD.BTR`

## Štruktúra polí (68 polí)

### Identifikácia majetku

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo majetku - **PK, FK FXA** |
| ExtNum | Str12 | 13 | Inventárne číslo |
| ClasCode | Str10 | 11 | Kód klasifikácie |
| FxaName | Str30 | 31 | Názov majetku |
| _FxaName | Str30 | 31 | Vyhľadávacie pole |

### Dátumy a prevádzkové údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocDate | DateType | 4 | Dátum založenia karty |
| AsdDate | DateType | 4 | Dátum vyradenia |
| WriNum | longint | 4 | Prevádzkové číslo |

### Spôsob vyradenia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AsdDoc | Str12 | 13 | Doklad zaúčtovania vyradenia |
| AsdReas | Str30 | 31 | Dôvod vyradenia |
| AsmCode | word | 2 | Kód spôsobu vyradenia |
| AsmText | Str30 | 31 | Text spôsobu vyradenia |

### Technický stav (3 riadky)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| TechStat1 | Str160 | 161 | Technický stav - riadok 1 |
| TechStat2 | Str160 | 161 | Technický stav - riadok 2 |
| TechStat3 | Str160 | 161 | Technický stav - riadok 3 |

### Príslušenstvo (3 riadky)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Appurten1 | Str160 | 161 | Príslušenstvo - riadok 1 |
| Appurten2 | Str160 | 161 | Príslušenstvo - riadok 2 |
| Appurten3 | Str160 | 161 | Príslušenstvo - riadok 3 |

### Vyjadrenie účastníkov (3 riadky)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PartStat1 | Str160 | 161 | Vyjadrenie - riadok 1 |
| PartStat2 | Str160 | 161 | Vyjadrenie - riadok 2 |
| PartStat3 | Str160 | 161 | Vyjadrenie - riadok 3 |

### Poznámky (5 riadkov)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| NotiLine1 | Str160 | 161 | Poznámka - riadok 1 |
| NotiLine2 | Str160 | 161 | Poznámka - riadok 2 |
| NotiLine3 | Str160 | 161 | Poznámka - riadok 3 |
| NotiLine4 | Str160 | 161 | Poznámka - riadok 4 |
| NotiLine5 | Str160 | 161 | Poznámka - riadok 5 |

### Účastníci vyradenia (8 osôb)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PartName1-8 | Str30 | 31 | Meno a priezvisko účastníka |
| PartFunc1-8 | Str20 | 21 | Funkcia účastníka |

### Zodpovedná osoba

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AccName | Str30 | 31 | Osoba zodpovedná za účtovný prípad |

### Finančné hodnoty - Daňové (L)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| LPrvVal | double | 8 | Obstarávacia cena - daňová |
| LAmrVal | double | 8 | Uplatnené odpisy - daňové |
| LEndVal | double | 8 | Zostatková cena - daňová |
| LAsdVal | double | 8 | Náklady vyradenia - daňové |
| LMatVal | double | 8 | Cena získaného materiálu - daňová |
| LTrnVal | double | 8 | Tržba za predaj - daňová |
| LDmgVal | double | 8 | Náhrada za škodu - daňová |
| LPrfVal | double | 8 | Zisk (strata) pri vyradení - daňová |

### Finančné hodnoty - Účtovné (T)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| TPrvVal | double | 8 | Obstarávacia cena - účtovná |
| TAmrVal | double | 8 | Uplatnené odpisy - účtovné |
| TEndVal | double | 8 | Zostatková cena - účtovná |
| TAsdVal | double | 8 | Náklady vyradenia - účtovné |
| TMatVal | double | 8 | Cena získaného materiálu - účtovná |
| TTrnVal | double | 8 | Tržba za predaj - účtovná |
| TDmgVal | double | 8 | Náhrada za škodu - účtovná |
| TPrfVal | double | 8 | Zisk (strata) pri vyradení - účtovná |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Počet modifikácií |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (3)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum | DocNum | Duplicit |
| 1 | ExtNum | ExtNum | Duplicit |
| 2 | _FxaName | FxaName | Duplicit, Case-insensitive |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | FXA.DocNum | Evidenčná karta majetku |

## Výpočet zisku/straty

```
Zisk/Strata = Tržba + Náhrada + MateriálCena - Zostatková - NákladyVyradenia
PrfVal = TrnVal + DmgVal + MatVal - EndVal - AsdVal
```

## Spôsoby vyradenia (AsmCode)

| Kód | Spôsob | Daňový dopad |
|-----|--------|--------------|
| 1 | Predaj | Zostatková do daňových nákladov |
| 2 | Likvidácia | Zostatková do daňových nákladov |
| 3 | Škoda | Podľa výšky náhrady |
| 4 | Dar | Zostatková do nákladov |
| 5 | Manko | Nedaňový náklad |

## Použitie

- Kompletná dokumentácia vyradenia majetku
- Tlač protokolu o vyradení
- Finančné vyúčtovanie vyradenia
- Evidencia účastníkov a rozhodnutí

## Business pravidlá

- Vytvára sa pri nastavení FXA.AsdMode > 0
- Obsahuje 8 polí pre účastníkov vyradenia
- Rozlišuje daňové (L*) a účtovné (T*) hodnoty
- Slúži ako podklad pre účtovanie vyradenia

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
