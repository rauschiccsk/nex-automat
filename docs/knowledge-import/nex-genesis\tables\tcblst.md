# TCBLST - Zoznam kníh odberateľských dodacích listov

## Kľúčové slová / Aliases

TCBLST, TCBLST.BTR, zoznam kníh dodacích listov, delivery books list

## Popis

Konfiguračná tabuľka definujúca knihy (série) odberateľských dodacích listov. Každá kniha má vlastné číslovanie, nastavenia meny, skladu a prepojenie na knihu faktúr.

## Btrieve súbor

`TCBLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\TCBLST.BTR`

## Štruktúra polí (45 polí)

### Identifikácia knihy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy - **PRIMARY KEY** |
| BookName | Str30 | 31 | Názov knihy |
| BookYear | Str4 | 5 | Rok založenia knihy |

### Číslovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SerNum | word | 2 | Posledné poradové číslo |
| ExnFrm | Str12 | 13 | Formát externého čísla DL |
| SerMod | byte | 1 | Povolenie zmeny poradového čísla (1=áno) |
| DocQnt | word | 2 | Počet dokladov v knihe |

### Mena a sklad

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DvzBook | byte | 1 | Typ knihy (0=tuzemská, 1=valutová) |
| DvzName | Str3 | 4 | Skratka meny |
| StkNum | word | 2 | Základný sklad |
| StkMod | byte | 1 | Povolenie zmeny skladu (1=áno) |
| PlsNum | word | 2 | Predvolený cenník |
| SmCode | word | 2 | Základný skladový pohyb |

### Väzby na iné moduly

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PabBook | word | 2 | Kniha partnerov - odberatelia |
| IcdBook | Str5 | 6 | Kniha odberateľských faktúr |

### Zaokrúhľovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FgVatRnd | byte | 1 | Typ zaokrúhlenia DPH - VM |
| FgValRnd | byte | 1 | Typ zaokrúhlenia PC s DPH - VM |
| AcVatRnd | byte | 1 | Typ zaokrúhlenia DPH - UM |
| AcValRnd | byte | 1 | Typ zaokrúhlenia PC s DPH - UM |
| FgCalc | byte | 1 | Spôsob výpočtu VM (0=základ s DPH, 1=základ bez DPH) |

### Automatizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AutoLst | byte | 1 | Automatické zobrazenie zoznamu tovaru (1=áno) |
| AutoAcc | byte | 1 | Automatické rozúčtovanie (1=áno) |
| Online | byte | 1 | Priamy odpočet zo skladu (1=áno) |
| PrnCls | byte | 1 | Uzatvorenie po tlači (1=áno) |
| OcnVer | byte | 1 | Kontrola duplicity čísla zákazky (1=áno) |

### Integrácia s ERP

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CasReg | byte | 1 | Vyúčtovanie cez ERP (1=áno) |
| DsHide | byte | 1 | Skryť diskrétne údaje (NC, zisk) |

### Prenos dokladov

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Shared | byte | 1 | Zdieľaný sklad - zmeny cez FTP (1=áno) |
| DocSnd | byte | 1 | Online odoslanie na inú prevádzku (1=áno) |
| DocRcv | byte | 1 | Online príjem z inej prevádzky (1=áno) |

### Ostatné

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WriNum | word | 2 | Číslo prevádzky (0=centrála) |
| SalCode | word | 2 | Kód obchodného zástupcu |
| MyTelNum | Str20 | 21 | Telefónne číslo prevádzky |
| MyFaxNum | Str20 | 21 | Faxové číslo prevádzky |
| MyWebSite | Str30 | 31 | Webová stránka |
| MyEmail | Str30 | 31 | E-mailová adresa |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Poradové číslo modifikácie |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BookNum | BookNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| StkNum | STKLST.StkNum | Predvolený sklad |
| IcdBook | ICBLST.BookNum | Kniha faktúr |
| PabBook | PABLST.BookNum | Kniha partnerov |
| PlsNum | PLSLST.PlsNum | Cenník |
| SmCode | SMLST.SmCode | Typ pohybu |

## Typy kníh (DvzBook)

| Hodnota | Popis |
|---------|-------|
| 0 | Tuzemská kniha (EUR) |
| 1 | Valutová kniha (cudzia mena) |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
