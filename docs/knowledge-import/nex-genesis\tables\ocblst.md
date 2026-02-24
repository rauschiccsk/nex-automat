# OCBLST - Zoznam kníh odberateľských zákaziek

## Kľúčové slová / Aliases

OCBLST, OCBLST.BTR, zoznam kníh objednávok, order books list

## Popis

Konfiguračná tabuľka definujúca knihy (série) odberateľských zákaziek. Každá kniha má vlastné číslovanie a môže mať rôzne nastavenia pre generovanie nadväzných dokladov.

## Btrieve súbor

`OCBLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OCBLST.BTR`

## Štruktúra polí (45 polí)

### Identifikácia knihy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BokNum | word | 2 | Číslo knihy - **PRIMARY KEY** |
| BokName | Str20 | 21 | Názov knihy |
| BokMark | Str3 | 4 | Značka knihy (OCB) |
| Active | byte | 1 | Aktívna kniha (1=áno) |

### Číslovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SerNum | longint | 4 | Posledné poradové číslo |
| SerPfx | Str5 | 6 | Prefix číslovania |
| SerSfx | Str5 | 6 | Suffix číslovania |
| Year | Str2 | 3 | Aktuálny rok |

### Predvolené hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | word | 2 | Predvolený sklad |
| PlsNum | word | 2 | Predvolený cenník |
| DscPrc | double | 8 | Predvolená zľava % |
| PayCode | Str3 | 4 | Predvolená forma úhrady |
| TrsCode | Str3 | 4 | Predvolený spôsob dopravy |

### Väzby na generované doklady

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| TcdBook | word | 2 | Kniha pre odberateľský DL |
| IcdBook | word | 2 | Kniha pre odberateľskú faktúru |
| PcdBook | word | 2 | Kniha pre zálohovú faktúru |
| CpdBook | word | 2 | Kniha pre pokladničný doklad |
| ExdBook | word | 2 | Kniha pre expedičný príkaz |
| OsdBook | word | 2 | Kniha pre dodávateľskú objednávku |

### Nastavenia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AutoRes | byte | 1 | Automatická rezervácia (1=áno) |
| AutoExd | byte | 1 | Automatická expedícia (1=áno) |
| ReqDep | byte | 1 | Vyžadovať zálohu (1=áno) |
| DepPrc | double | 8 | Percento zálohy |
| ShpImp | byte | 1 | Povolený import z e-shopu (1=áno) |

### E-shop integrácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ShpCode | Str10 | 11 | Kód e-shopu |
| ShpName | Str30 | 31 | Názov e-shopu |
| ShpUrl | Str100 | 101 | URL e-shopu |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BokNum | BokNum | Unique |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| StkNum | STKLST.StkNum | Predvolený sklad |
| TcdBook | TCBLST.BokNum | Kniha DL |
| IcdBook | ICBLST.BokNum | Kniha faktúr |
| PlsNum | PLSLST.PlsNum | Cenník |

## Použitie

- Definícia sérií zákaziek (napr. e-shop, veľkoobchod, maloobchod)
- Nastavenie automatických procesov
- Prepojenie na nadväzné doklady
- Import z e-shopov

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
