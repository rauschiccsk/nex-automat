# ICBLST - Zoznam kníh odberateľských faktúr

## Kľúčové slová / Aliases

ICBLST, ICBLST.BTR, zoznam kníh faktúr, invoice books list

## Popis

Konfiguračná tabuľka definujúca knihy (série) odberateľských faktúr. Obsahuje nastavenia číslovania, účtov, zaokrúhľovania a prepojenia na iné moduly.

## Btrieve súbor

`ICBLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ICBLST.BTR`

## Štruktúra polí (75 polí)

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
| ExnFrm | Str12 | 13 | Formát variabilného symbolu |
| DocQnt | word | 2 | Počet dokladov v knihe |

### Mena a sklad

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DvzBook | byte | 1 | Typ knihy (0=tuzemská, 1=valutová) |
| DvzName | Str3 | 4 | Skratka meny |
| StkNum | word | 2 | Základný sklad |
| PlsNum | word | 2 | Predvolený cenník |

### Väzby na iné moduly

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PabBook | word | 2 | Kniha partnerov |
| TcdBook | Str5 | 6 | Kniha odberateľských DL |
| TcBook | Str5 | 6 | Kniha DL pre túto knihu FA |
| CsdBook | Str5 | 6 | Kniha hotovostných dokladov |
| NicBook | Str5 | 6 | Kniha pre automatický dobropis |

### Bankové údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DefConto | byte | 1 | Predvolený bankový účet |
| MyConto | Str30 | 31 | Číslo bankového účtu |
| BankName | Str30 | 31 | Názov banky |
| BankAddr | Str30 | 31 | Adresa banky |
| BankCity | Str30 | 31 | Sídlo banky |
| BankStat | Str30 | 31 | Štát banky |
| IbanCode | Str10 | 11 | IBAN kód |
| SwftCode | Str30 | 31 | SWIFT kód |

### Predkontácie účtov

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocSnt | Str3 | 4 | Syntetický účet faktúry |
| DocAnl | Str6 | 7 | Analytický účet faktúry |
| VatSnt | Str3 | 4 | Účet DPH - 2. sadzba SYN |
| VatAnl | Str6 | 7 | Účet DPH - 2. sadzba ANL |
| VatSnt3 | Str3 | 4 | Účet DPH - 3. sadzba SYN |
| VatAnl3 | Str6 | 7 | Účet DPH - 3. sadzba ANL |
| GscSnt | Str3 | 4 | Účet tovarových položiek SYN |
| GscAnl | Str6 | 7 | Účet tovarových položiek ANL |
| SecSnt | Str3 | 4 | Účet služieb SYN |
| SecAnl | Str6 | 7 | Účet služieb ANL |
| PCrdSnt | Str3 | 4 | Účet kurzového zisku SYN |
| PCrdAnl | Str6 | 7 | Účet kurzového zisku ANL |
| NCrdSnt | Str3 | 4 | Účet kurzovej straty SYN |
| NCrdAnl | Str6 | 7 | Účet kurzovej straty ANL |
| PPdfSnt | Str3 | 4 | Účet preplatku SYN |
| PPdfAnl | Str6 | 7 | Účet preplatku ANL |
| NPdfSnt | Str3 | 4 | Účet nedoplatku SYN |
| NPdfAnl | Str6 | 7 | Účet nedoplatku ANL |

### Zaokrúhľovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FgVatRnd | byte | 1 | Typ zaokrúhlenia DPH - VM |
| FgValRnd | byte | 1 | Typ zaokrúhlenia PC s DPH - VM |
| AcVatRnd | byte | 1 | Typ zaokrúhlenia DPH - UM |
| AcValRnd | byte | 1 | Typ zaokrúhlenia PC s DPH - UM |
| RndType | byte | 1 | Typ zaokrúhlenia (0=klasické, 1=samostatná položka) |
| FgCalc | byte | 1 | Spôsob výpočtu VM |

### Automatizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AutoAcc | byte | 1 | Automatické rozúčtovanie (1=áno) |
| AccTcd | byte | 1 | Automatické rozúčtovanie DL (1=áno) |
| PrnCls | byte | 1 | Uzatvorenie po tlači (1=áno) |
| OcnVer | byte | 1 | Kontrola duplicity zákazky (1=áno) |
| SumAcc | byte | 1 | Kumulatívne účtovanie |

### DPH

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatCls | byte | 1 | Započítať do evidencie DPH (1=áno) |
| DocSpc | byte | 1 | Predvolená špecifikácia dokladu |

### Integrácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Shared | byte | 1 | Zdieľaný sklad (1=áno) |
| DocSnd | byte | 1 | Online odoslanie (1=áno) |
| DocRcv | byte | 1 | Online príjem (1=áno) |
| DsHide | byte | 1 | Skryť diskrétne údaje |
| ExCalc | byte | 1 | Výpočet splatnosti (0=od vystavenia, 1=od odoslania, 2=od dodania) |
| CsyCode | Str4 | 5 | Prednastavený konštantný symbol |

### Kontakt

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WriNum | word | 2 | Číslo prevádzky |
| SalCode | word | 2 | Kód obchodného zástupcu |
| MyTelNum | Str20 | 21 | Telefón |
| MyFaxNum | Str20 | 21 | Fax |
| MyWebSite | Str30 | 31 | Web |
| MyEmail | Str30 | 31 | Email |

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
| TcdBook | TCBLST.BookNum | Kniha DL |
| CsdBook | CSBLST.BookNum | Kniha pokladne |
| PlsNum | PLSLST.PlsNum | Cenník |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
