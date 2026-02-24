# BSMDOC - Hlavičky bankových výpisov

## Kľúčové slová / Aliases

BSMDOC, BSMDOC.BTR, hlavičky, bankových, výpisov

## Popis

Hlavičky bankových výpisov. Každý výpis obsahuje obdobie (začiatok a koniec), počiatočný a konečný stav účtu, súčty príjmov a výdajov v mene účtu aj účtovnej mene.

## Btrieve súbor

`BSMDOC.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\BSMDOC.BTR`

## Štruktúra polí (29 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BokNum | Str3 | 4 | Číslo knihy - **FK** |
| DocYer | Str2 | 3 | Rok dokladu |
| SerNum | longint | 4 | Poradové číslo dokladu |
| DocNum | Str12 | 13 | Interné číslo dokladu - **PRIMARY KEY** |

### Obdobie výpisu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BegDte | DateType | 4 | Počiatočný dátum bankového výpisu |
| EndDte | DateType | 4 | Konečný dátum bankového výpisu |
| LasDte | DateType | 4 | Posledný dátum v položkách výpisu |

### Mena účtu (Pay*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayDvz | Str3 | 4 | Mena bankového účtu |
| PayCrs | double | 8 | Devízový kurz bankového výpisu |
| PayBeg | double | 8 | Počiatočný stav účtu - mena účtu |
| PayCrd | double | 8 | Súčet príjmov - mena účtu |
| PayDeb | double | 8 | Súčet výdajov - mena účtu |
| PayEnd | double | 8 | Konečný stav - mena účtu |
| PayDif | double | 8 | Rozdiel medzi položkami a konečným stavom |

### Účtovná mena (Acc*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AccBeg | double | 8 | Počiatočný stav účtu - účtovná mena |
| AccCrd | double | 8 | Súčet príjmov - účtovná mena |
| AccDeb | double | 8 | Súčet výdajov - účtovná mena |
| AccEnd | double | 8 | Konečný stav - účtovná mena |

### Štatistiky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PrnCnt | byte | 1 | Počet vytlačených kópií dokladu |
| ItmQnt | word | 2 | Počet položiek bankového výpisu |
| CitQnt | word | 2 | Počet položiek súhrnnej platby |

### Stav dokladu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DstLck | Str1 | 2 | Príznak uzamknutosti (L=uzamknutý) |
| DstDif | Str1 | 2 | Príznak rozdielu konečného stavu (!=rozdiel) |
| DstAcc | Str1 | 2 | Príznak zaúčtovanosti (A=zaúčtovaný) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUsr | Str10 | 11 | Prihlasovacie meno používateľa vytvorenia |
| CrtUsn | Str30 | 31 | Meno a priezvisko používateľa vytvorenia |
| CrtDte | DateType | 4 | Dátum vytvorenia dokladu |
| CrtTim | TimeType | 4 | Čas vytvorenia dokladu |

## Indexy (9)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum | DocNum | Unikátny |
| 1 | BokNum | BokNum | Duplicit |
| 2 | DocYer, SerNum | DySn | Duplicit |
| 3 | DocYer, BokNum, SerNum | DyBnSn | Duplicit |
| 4 | BegDte | BegDte | Duplicit |
| 5 | EndDte | EndDte | Duplicit |
| 6 | DstLck | DstLck | Duplicit |
| 7 | DstDif | DstDif | Duplicit |
| 8 | DstAcc | DstAcc | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| BokNum | BOK | Kniha bankových výpisov |

## Použitie

- Evidencia bankových výpisov
- Sledovanie stavov bankového účtu
- Párování s položkami (BSMITM)
- Zaúčtovanie do účtovného denníka

## Business pravidlá

- PayEnd = PayBeg + PayCrd - PayDeb
- DstDif='!' ak PayDif ≠ 0 (rozdiel medzi očakávaným a skutočným stavom)
- DstAcc='A' po zaúčtovaní do denníka
- ItmQnt sleduje počet položiek pre farebné rozlíšenie prázdnych výpisov

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
