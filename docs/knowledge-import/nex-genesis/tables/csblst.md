# CSBLST - Zoznam kníh hotovostných pokladní

## Kľúčové slová / Aliases

CSBLST, CSBLST.BTR, zoznam, kníh, hotovostných, pokladní

## Popis

Konfiguračná tabuľka kníh hotovostných pokladní. Definuje menu pokladne, počiatočné a konečné stavy, účty pre zaúčtovanie, nastavenia DPH a zaokrúhľovania.

## Btrieve súbor

`CSBLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\CSBLST.BTR`

## Štruktúra polí (45 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy - **PRIMARY KEY** |
| BookName | Str20 | 21 | Názov knihy pokladne |
| BookYear | Str4 | 5 | Rok založenia knihy |

### Mena pokladne (Py*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PyDvzName | Str3 | 4 | Názov pokladničnej meny |
| PyBegVal | double | 8 | Počiatočný stav - PM |
| PyIncVal | double | 8 | Celkový príjem - PM |
| PyExpVal | double | 8 | Celkový výdaj - PM |
| PyEndVal | double | 8 | Konečný stav - PM |
| PyMaxPdf | double | 8 | Max. hodnota rozdielu úhrady |

### Účtovná mena (Ac*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AcBegVal | double | 8 | Počiatočný stav - ÚM |
| AcIncVal | double | 8 | Celkový príjem - ÚM |
| AcExpVal | double | 8 | Celkový výdaj - ÚM |
| AcEndVal | double | 8 | Konečný stav - ÚM |
| EyCourse | double | 8 | Koncoročný kurz |
| EyCrdVal | double | 8 | Kurzový rozdiel z koncoročného prekurzovania |

### Štatistiky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocQnt | word | 2 | Počet dokladov |
| IDocQnt | word | 2 | Počet príjmových dokladov |
| EDocQnt | word | 2 | Počet výdajových dokladov |

### Účty pokladne

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AccSnt | Str3 | 4 | Syntetický účet pokladne |
| AccAnl | Str6 | 7 | Analytický účet pokladne |

### Účty DPH

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| IVatSnt | Str3 | 4 | Syntetický účet DPH - vstup |
| IVatAnl | Str6 | 7 | Analytický účet DPH - vstup |
| OVatSnt | Str3 | 4 | Syntetický účet DPH - výstup |
| OVatAnl | Str6 | 7 | Analytický účet DPH - výstup |

### Nastavenia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatRnd | byte | 1 | Typ zaokrúhľovania DPH |
| ValRnd | byte | 1 | Typ zaokrúhľovania dokladu |
| DocSpc | byte | 1 | Špecifikácia dokladu |
| VatCls | byte | 1 | Započítať do DPH (1=áno) |
| AutoAcc | byte | 1 | Automatické zaúčtovanie (1=zapnuté) |
| RndVer | byte | 1 | Kontrola zaokrúhlenia na 0.50 (1=zapnuté) |
| SumAcc | byte | 1 | Kumulatívne účtovanie |
| WriAdd | byte | 1 | Povinné zadávanie PJ (1=zapnuté) |
| DateDis | byte | 1 | Zákaz zmeny dátumu |

### Prevádzka

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WriNum | word | 2 | Číslo prevádzkovej jednotky |
| PabBook | word | 2 | Kniha obchodných partnerov |
| Shared | byte | 1 | Zdieľanie cez FTP (1=zdieľaný) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |
| ModNum | word | 2 | Počítadlo modifikácií |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BookNum | BookNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| WriNum | WRILST.WriNum | Prevádzková jednotka |
| PabBook | PABLST.PabBook | Kniha partnerov |
| AccSnt+AccAnl | ACCLST | Účet pokladne |
| IVatSnt+IVatAnl | ACCLST | Účet DPH vstup |
| OVatSnt+OVatAnl | ACCLST | Účet DPH výstup |

## Použitie

- Konfigurácia hotovostných pokladní
- Nastavenie meny a účtov
- Sledovanie stavov pokladne
- Nastavenia DPH a zaokrúhľovania

## Business pravidlá

- PyEndVal = PyBegVal + PyIncVal - PyExpVal
- AutoAcc=1 automaticky účtuje po uložení dokladu
- RndVer=1 kontroluje zaokrúhlenie na 0.50
- Jedna kniha = jedna pokladňa (mena)

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
