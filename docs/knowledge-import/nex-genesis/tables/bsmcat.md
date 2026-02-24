# BSMCAT - Katalóg bankových operácií

## Kľúčové slová / Aliases

BSMCAT, BSMCAT.BTR, katalóg, bankových, operácií

## Popis

Číselník bankových operácií (predkontácie). Definuje typy bankových transakcií s prednastavenými symbolmi, účtami a textami pre rýchle zadávanie položiek.

## Btrieve súbor

`BSMCAT.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\BSMCAT.BTR`

## Štruktúra polí (20 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OprNum | word | 2 | Numerický kód operácie - **PRIMARY KEY** |
| OprCod | Str15 | 16 | Identifikačný kód operácie |

### Platobné symboly

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VarSym | Str12 | 13 | Variabilný symbol |
| SpcSym | Str12 | 13 | Špecifický symbol |
| ConSym | Str4 | 5 | Konštantný symbol |

### Údaje platby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayDes | Str60 | 61 | Popis úhrady |
| _PayDes | Str60 | 61 | Popis úhrady - vyhľadávacie pole |
| PayVal | double | 8 | Čiastka úhrady |

### Účtovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AccSnt | Str3 | 4 | Syntetický účet pre rozúčtovanie položky |
| AccAnl | Str6 | 7 | Analytický účet pre rozúčtovanie položky |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUsr | Str10 | 11 | Prihlasovacie meno používateľa vytvorenia |
| CrtUsn | Str30 | 31 | Meno a priezvisko používateľa vytvorenia |
| CrtDte | DateType | 4 | Dátum vytvorenia záznamu |
| CrtTim | TimeType | 4 | Čas vytvorenia záznamu |
| ModUsr | Str10 | 11 | Prihlasovacie meno používateľa zmeny |
| ModUsn | Str30 | 31 | Meno a priezvisko používateľa zmeny |
| ModDte | DateType | 4 | Dátum poslednej zmeny záznamu |
| ModTim | TimeType | 4 | Čas poslednej zmeny záznamu |

## Indexy (5)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | OprNum | OprNum | Unikátny |
| 1 | OprCod | OprCod | Duplicit |
| 2 | VarSym | VarSym | Duplicit |
| 3 | _PayDes | PayDes | Duplicit |
| 4 | AccSnt, AccAnl | SnAn | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| AccSnt+AccAnl | ACCLST | Účet |
| ConSym | CSYLST | Konštantný symbol |

## Príklady operácií

| OprNum | OprCod | PayDes | AccSnt | Popis |
|--------|--------|--------|--------|-------|
| 1 | UHRFA | Úhrada faktúry | 321 | Záväzky |
| 2 | UHRFAC | Úhrada FA odberateľ | 311 | Pohľadávky |
| 3 | POPL | Bankové poplatky | 568 | Bankové poplatky |
| 4 | UROK | Úroky z účtu | 662 | Úroky |
| 5 | PREVOD | Prevod medzi účtami | 261 | Peniaze na ceste |

## Použitie

- Predkontácie pre bankové položky
- Rýchle zadávanie opakujúcich sa transakcií
- Štandardizácia účtovania
- Výber z katalógu pri zadávaní položiek

## Business pravidlá

- Výber operácie automaticky doplní účet a symboly
- PayVal = predvolená suma (môže sa zmeniť)
- OprCod slúži ako textový identifikátor pre elektronické bankovníctvo
- Zjednodušuje prácu pri spracovaní výpisov

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
