# BSMITM - Položky bankových výpisov

## Kľúčové slová / Aliases

BSMITM, BSMITM.BTR, položky, bankových, výpisov

## Popis

Položky bankových výpisov. Každá položka reprezentuje jednu bankovú transakciu - príjem alebo výdaj. Obsahuje platobné symboly, prepojenie na faktúry, kurzy a účty pre zaúčtovanie.

## Btrieve súbor

`BSMITM.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\BSMITM.BTR`

## Štruktúra polí (46 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo bankového výpisu - **FK** |
| ItmNum | word | 2 | Poradové číslo riadku |
| CitNum | word | 2 | Poradové číslo riadku súhrnnej platby |
| BokNum | Str3 | 4 | Číslo knihy |
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
| CdvSnt | Str3 | 4 | Syntetický účet kurzového rozdielu |
| CdvAnl | Str6 | 7 | Analytický účet kurzového rozdielu |
| PdvSnt | Str3 | 4 | Syntetický účet cenového rozdielu |
| PdvAnl | Str6 | 7 | Analytický účet cenového rozdielu |

### Prepojenie na faktúru

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| InvDoc | Str12 | 13 | Interné číslo uhrádzanej faktúry |
| InvTyp | Str1 | 2 | Typ faktúry (S=dodávateľská, C=odberateľská) |
| InvDvz | Str3 | 4 | Mena uhrádzanej faktúry |
| InvVal | double | 8 | Hodnota úhrady v mene faktúry |
| InvCrs | double | 8 | Kurz, ktorým bola faktúra zaevidovaná |
| InvAcv | double | 8 | Hodnota faktúry v účtovnej mene |

### Účtovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ItmSnt | Str3 | 4 | Syntetický účet pre rozúčtovanie položky |
| ItmAnl | Str6 | 7 | Analytický účet pre rozúčtovanie položky |

### Organizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ParNum | longint | 4 | Registračný kód firmy |
| WriNum | word | 2 | Číslo prevádzkovej jednotky |
| EcuNum | word | 2 | Číslo hospodárskej jednotky |

### Súhrnná platba

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CitQnt | word | 2 | Počet detailných položiek súhrnnej platby |
| CitVal | double | 8 | Kumulatívna hodnota položiek súhrnnej platby |

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
| 7 | PayCon | PayCon | Duplicit |
| 8 | PayIba | PayIba | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | BSMDOC.DocNum | Hlavička výpisu |
| InvDoc | ISH/ICH.DocNum | Uhrádzaná faktúra |
| ParNum | PAB.ParNum | Obchodný partner |
| ItmSnt+ItmAnl | ACCLST | Účet položky |
| CdvSnt+CdvAnl | ACCLST | Účet kurzového rozdielu |
| PdvSnt+PdvAnl | ACCLST | Účet cenového rozdielu |

## Použitie

- Evidencia jednotlivých bankových transakcií
- Párovanie platieb s faktúrami
- Výpočet kurzových rozdielov
- Podklad pre zaúčtovanie

## Business pravidlá

- InvTyp='S' pre dodávateľské faktúry, 'C' pre odberateľské
- CdvAcv = kurzový rozdiel medzi kurzom faktúry (InvCrs) a kurzom úhrady (PayCrs)
- CitNum > 0 pre položky súhrnnej platby (viac faktúr v jednej platbe)
- PayAcv = zaúčtovaná hodnota = PayVal / PayCrs (ak PayDvz ≠ účtovná mena)

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
