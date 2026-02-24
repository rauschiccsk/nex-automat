# PAYJRN - Denník úhrad faktúr

## Kľúčové slová / Aliases

PAYJRN, PAYJRN.BTR, denník, úhrad, faktúr

## Popis

Denník úhrad faktúr. Centrálna evidencia všetkých úhrad faktúr z bankových výpisov a hotovostných pokladní. Obsahuje kompletné informácie o platbe vrátane prepojenia na faktúru, kurzové rozdiely a údaje o partnerovi.

## Btrieve súbor

`PAYJRN.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\PAYJRN.BTR`

## Štruktúra polí (38 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo dokladu úhrady |
| ItmNum | word | 2 | Poradové číslo položky úhrady |
| CitNum | word | 2 | Poradové číslo riadku súhrnnej platby |
| DocYer | Str2 | 3 | Rok dokladu |

### Platobné symboly

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VarSym | Str15 | 16 | Variabilný symbol úhrady |
| SpcSym | Str20 | 21 | Špecifický symbol úhrady |
| ConSym | Str4 | 5 | Konštantný symbol úhrady |

### Údaje platby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayDte | DateType | 4 | Dátum úhrady položky |
| PayIba | Str25 | 26 | IBAN protiúčtu |
| PayCon | Str20 | 21 | Číslo protiúčtu |
| PayDes | Str60 | 61 | Textový popis úhrady |

### Partner

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ParNum | longint | 4 | Registračný kód firmy z uhrádzanej faktúry |
| ParNam | Str60 | 61 | Názov firmy z uhrádzanej faktúry |
| _ParNam | Str60 | 61 | Názov firmy - vyhľadávacie pole |

### Mena účtu (Pay*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayDvz | Str3 | 4 | Mena bankového účtu |
| PayCrs | double | 8 | Kurz úhrady |
| PayCdt | DateType | 4 | Dátum kurzu úhrady |
| PayVal | double | 8 | Hodnota úhrady v mene bankového účtu |
| PayAcv | double | 8 | Zaúčtovaná hodnota položky |

### Kurzové a cenové rozdiely

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PdvAcv | double | 8 | Rozdiel úhrady účtovaný do zaokrúhlenia |
| CdvAcv | double | 8 | Kurzový rozdiel (kurz FA vs kurz úhrady) |

### Prepojenie na faktúru

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| InvDoc | Str12 | 13 | Interné číslo uhrádzanej faktúry |
| InvTyp | Str1 | 2 | Typ faktúry (S=dodávateľská, C=odberateľská) |
| InvDvz | Str3 | 4 | Mena uhrádzanej faktúry |
| InvVal | double | 8 | Hodnota úhrady v mene faktúry |
| InvCrs | double | 8 | Kurz, ktorým bola faktúra zaevidovaná |
| InvAcv | double | 8 | Hodnota faktúry v účtovnej mene |

### Organizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WriNum | word | 2 | Číslo prevádzkovej jednotky |
| EcuNum | word | 2 | Číslo hospodárskej jednotky |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUsr | Str10 | 11 | Prihlasovacie meno používateľa vytvorenia |
| CrtUsn | Str30 | 31 | Meno a priezvisko používateľa vytvorenia |
| CrtDte | DateType | 4 | Dátum vytvorenia položky |
| CrtTim | TimeType | 4 | Čas vytvorenia položky |
| ModUsr | Str10 | 11 | Prihlasovacie meno používateľa zmeny |
| ModUsn | Str30 | 31 | Meno a priezvisko používateľa zmeny |
| ModDte | DateType | 4 | Dátum poslednej zmeny položky |
| ModTim | TimeType | 4 | Čas poslednej zmeny položky |

## Indexy (9)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum, CitNum | DoItCn | Duplicit |
| 1 | DocNum, ItmNum | DoIt | Duplicit |
| 2 | DocNum | DocNum | Duplicit |
| 3 | InvDoc | InvDoc | Duplicit |
| 4 | VarSym | VarSym | Duplicit |
| 5 | SpcSym | SpcSym | Duplicit |
| 6 | PayDte | PayDte | Duplicit |
| 7 | _ParNam | ParNam | Duplicit |
| 8 | DocYer | DocYer | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | BSMDOC/CSH.DocNum | Zdrojový doklad (výpis/pokladňa) |
| InvDoc | ISH/ICH.DocNum | Uhrádzaná faktúra |
| ParNum | PAB.ParNum | Obchodný partner |

## Použitie

- Centrálna evidencia úhrad faktúr
- Výkaz úhrad za obdobie
- Prehľad platieb podľa partnera
- Podklad pre účtovné výkazy

## Business pravidlá

- InvTyp='S' pre dodávateľské faktúry (ISH), 'C' pre odberateľské (ICH)
- CdvAcv = kurzový rozdiel = InvAcv - PayAcv (pri rôznych kurzoch)
- Záznam sa vytvára pri párovaní platby s faktúrou v BSMITM alebo CSI
- ParNum a ParNam sa preberajú z faktúry pre rýchle vyhľadávanie

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
