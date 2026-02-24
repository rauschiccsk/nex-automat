# MCBLST - Zoznam kníh odberateľských cenových ponúk

## Kľúčové slová / Aliases

MCBLST, MCBLST.BTR, zoznam, kníh, odberateľských, cenových, ponúk

## Popis

Konfiguračná tabuľka kníh odberateľských cenových ponúk. Definuje základné nastavenia vrátane meny, prepojenia na ďalšie moduly a bankových údajov.

## Btrieve súbor

`MCBLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\MCBLST.BTR`

## Štruktúra polí (42 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy - **PRIMARY KEY** |
| BookName | Str30 | 31 | Názov knihy |
| BookYear | Str4 | 5 | Rok založenia knihy |
| SerNum | word | 2 | Poradové číslo knihy |

### Mena

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DvzBook | byte | 1 | Typ knihy (0=tuzemská, 1=valutová) |
| DvzName | Str3 | 4 | Skratka meny |

### Štatistiky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocQnt | word | 2 | Počet dokladov v knihe |

### Základné nastavenia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | word | 2 | Číslo skladu výdaja |
| WriNum | word | 2 | Číslo prevádzky (0=centrála) |
| PlsNum | word | 2 | Predvolený cenník |
| SalCode | word | 2 | Kód obchodného zástupcu |

### Prepojené knihy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PabBook | word | 2 | Kniha obchodných partnerov |
| OcdBook | Str5 | 6 | Kniha odberateľských zákaziek |
| TcdBook | Str5 | 6 | Kniha dodacích listov |
| IcdBook | Str5 | 6 | Kniha faktúr |

### Formáty a nastavenia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ExnFrm | Str12 | 13 | Formát externého čísla |
| SerMod | byte | 1 | Povolenie zmeny poradového čísla |
| PrnCls | byte | 1 | Uzatvorenie po tlači |
| ItmForm | byte | 1 | Formulár editora položiek |
| DocForm | byte | 1 | Formulár editora hlavičky |
| DsHide | byte | 1 | Skryť diskrétne údaje (NC, zisk) |

### Zaokrúhľovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FgVatRnd | byte | 1 | Zaokrúhľovanie DPH z PC (VM) |
| FgValRnd | byte | 1 | Zaokrúhľovanie PC s DPH (VM) |
| AcVatRnd | byte | 1 | Zaokrúhľovanie DPH z PC (UM) |
| AcValRnd | byte | 1 | Zaokrúhľovanie PC s DPH (UM) |

### Bankové údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| MyConto | Str30 | 31 | Bankový účet dodávateľa |
| IbanCode | Str10 | 11 | IBAN kód |
| SwftCode | Str30 | 31 | SWIFT kód |
| BankName | Str30 | 31 | Názov banky |
| BankAddr | Str30 | 31 | Adresa banky |
| BankCity | Str30 | 31 | Sídlo banky |
| BankStat | Str30 | 31 | Štát banky |

### Synchronizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Shared | byte | 1 | Zdieľanie cez FTP (1=áno) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |
| ModNum | word | 2 | Poradové číslo modifikácie |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BookNum | BookNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| StkNum | STKLST.StkNum | Sklad |
| PlsNum | PLSLST.PlsNum | Cenník |
| PabBook | PABLST.PabBook | Kniha partnerov |
| OcdBook | OCBLST.BookNum | Kniha zákaziek |
| TcdBook | TCBLST.BookNum | Kniha DDL |
| IcdBook | ICBLST.BookNum | Kniha faktúr |

## Použitie

- Konfigurácia kníh cenových ponúk
- Nastavenie meny a zaokrúhľovania
- Prepojenie na nadväzné moduly
- Bankové údaje pre fakturáciu

## Business pravidlá

- DvzBook=0 pre tuzemské ponuky
- DvzBook=1 pre valutové ponuky
- OcdBook definuje kam sa generujú zákazky
- TcdBook definuje kam sa generujú DDL

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
