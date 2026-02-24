# USRLST - Zoznam používateľov systému

## Kľúčové slová / Aliases

USRLST, USRLST.BTR, User List, používatelia, zoznam používateľov,
prihlásenie, login, autentifikácia, prístupové práva, heslo, password,
užívatelia systému, správa používateľov, user management

## Popis

Tabuľka zoznamu používateľov NEX Genesis systému. Obsahuje prihlasovacie údaje, oprávnenia a základné nastavenia pre každého používateľa. Globálny súbor.

## Btrieve súbor

`USRLST.BTR`

## Umiestnenie

`C:\NEX\SYSTEM\USRLST.BTR`

## Štruktúra polí (19 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| LoginName | Str8 | 9 | Prihlasovacie meno používateľa (primárny kľúč) |
| LoginOwnr | Str20 | 21 | Vlastník záznamu |
| UserName | Str30 | 31 | Meno a priezvisko používateľa |
| Language | Str2 | 3 | Pracovný jazyk (SK, CZ, HU, RU, UA) |

### Prístupové práva

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GrpNum | word | 2 | Skupina prístupových práv (0 = individuálne práva) |
| UsrLev | byte | 1 | Úroveň zaradenia používateľa (1-admin, 2-power, 3-user) |
| DefSet1 | word | 2 | Základné nastavenia - skupina 1 |
| DefSet2 | word | 2 | Základné nastavenia - skupina 2 |
| DefSet3 | word | 2 | Základné nastavenia - skupina 3 |
| DefSet4 | byte | 1 | Základné nastavenia - skupina 4 |

### Obchodné údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DlrCode | word | 2 | Kód obchodného zástupcu |
| MaxDsc | byte | 1 | Maximálna zľava (%) ktorú môže zadať používateľ |
| UsrNum | word | 2 | Číselný kód používateľa |
| SmaIdc | Str10 | 11 | Kód pre rýchly vstup (smart card) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (3)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | LoginName | LoginName | Unikátny, Case-insensitive |
| 1 | LoginName, LoginOwnr | LnLo | Duplicit, Case-insensitive |
| 2 | SmaIdc | SmaIdc | Duplicit |

## Úrovne používateľov (UsrLev)

| Hodnota | Popis | Oprávnenia |
|---------|-------|------------|
| 1 | Administrátor | Plný prístup, servisné funkcie |
| 2 | Power User | Rozšírený prístup, bez servisu |
| 3 | Štandardný | Základný prístup podľa skupiny |

## Príklad

```
LoginName = "JAN.KOV"
UserName  = "Ján Kováč"
Language  = "SK"
GrpNum    = 2 (Skupina: Účtovníctvo)
UsrLev    = 3 (Štandardný používateľ)
DlrCode   = 5 (Obchodný zástupca č. 5)
MaxDsc    = 15 (Max. zľava 15%)
UsrNum    = 1234
```

## Použitie

- Autentifikácia používateľov pri prihlásení
- Určenie skupiny práv pre autorizáciu
- Identifikácia používateľa v audit záznamoch
- Obmedzenie zliav podľa používateľa
- Priradenie obchodného zástupcu

## Business pravidlá

- LoginName je unikátny identifikátor (max 8 znakov)
- GrpNum = 0 znamená individuálne práva (admin)
- UsrLev určuje úroveň prístupu nezávisle na skupine
- MaxDsc = 0 znamená bez obmedzenia zliav
- Heslo NIE JE uložené v tejto tabuľke (externý systém)

## Súvisiace tabuľky

| Tabuľka | Vzťah | Popis |
|---------|-------|-------|
| USRGRP | GrpNum → GrpNum | Definícia skupiny |
| APMDEF | GrpNum → GrpNum | Práva modulov skupiny |
| BKGRGHT | GrpNum → RghtGrp | Práva kníh skupiny |
| USRSET | LoginName → LoginName | Nastavenia formulárov |
| USRMON | LoginName → LoginName | Monitorovanie session |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
