# RMH - Hlavičky medziskladových presunov

## Kľúčové slová / Aliases

RMH, RMH.BTR, hlavičky, medziskladových, presunov

## Popis

Hlavičková tabuľka medziskladových presunov. Obsahuje základné údaje o presune medzi dvoma skladmi vrátane súčtov hodnôt a stavov spracovania.

## Btrieve súbor

`RMHyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\RMHyynnn.BTR`

## Štruktúra polí (71 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Year | Str2 | 3 | Rok dokladu |
| SerNum | longint | 4 | Poradové číslo presunu |
| DocNum | Str12 | 13 | Interné číslo presunu - **PRIMARY KEY** |
| DocDate | DateType | 4 | Dátum vystavenia |

### Sklady a pohyby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ScStkNum | word | 2 | Číslo zdrojového skladu (výdaj) |
| TgStkNum | word | 2 | Číslo cieľového skladu (príjem) |
| ScSmCode | word | 2 | Skladový pohyb výdaja |
| TgSmCode | word | 2 | Skladový pohyb príjmu |

### Nadväznosti

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OcdNum | Str20 | 21 | Interné číslo zákazky |
| SrdNum | Str12 | 13 | Zdrojový doklad (základ presunu) |

### Množstvá

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ItmQnt | word | 2 | Počet položiek dokladu |
| PlsNum | word | 2 | Číslo použitého cenníka |
| PrnCnt | byte | 1 | Počet vytlačených kópií |

### DPH skupiny

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc1 | double | 8 | Sadzba DPH skupiny č.1 |
| VatPrc2 | double | 8 | Sadzba DPH skupiny č.2 |
| VatPrc3 | double | 8 | Sadzba DPH skupiny č.3 |
| VatPrc4 | double | 8 | Sadzba DPH skupiny č.4 |
| VatPrc5 | double | 8 | Sadzba DPH skupiny č.5 |

### Hodnoty v NC bez DPH

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CValue1 | double | 8 | Hodnota v NC bez DPH - skupina 1 |
| CValue2 | double | 8 | Hodnota v NC bez DPH - skupina 2 |
| CValue3 | double | 8 | Hodnota v NC bez DPH - skupina 3 |
| CValue4 | double | 8 | Hodnota v NC bez DPH - skupina 4 |
| CValue5 | double | 8 | Hodnota v NC bez DPH - skupina 5 |
| CValue | double | 8 | Hodnota v NC bez DPH - spolu |

### DPH z NC

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatVal1 | double | 8 | DPH z NC - skupina 1 |
| VatVal2 | double | 8 | DPH z NC - skupina 2 |
| VatVal3 | double | 8 | DPH z NC - skupina 3 |
| VatVal | double | 8 | DPH z NC - spolu |

### Hodnoty v NC s DPH

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| EValue1 | double | 8 | Hodnota v NC s DPH - skupina 1 |
| EValue2 | double | 8 | Hodnota v NC s DPH - skupina 2 |
| EValue3 | double | 8 | Hodnota v NC s DPH - skupina 3 |
| EValue4 | double | 8 | Hodnota v NC s DPH - skupina 4 |
| EValue5 | double | 8 | Hodnota v NC s DPH - skupina 5 |
| EValue | double | 8 | Hodnota v NC s DPH - spolu |

### Hodnoty v PC

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AValue | double | 8 | Hodnota v PC bez DPH |
| BValue | double | 8 | Hodnota v PC s DPH |

### Stavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DstLck | byte | 1 | Uzatvorenie (1=uzatvorený) |
| DstAcc | Str1 | 2 | Zaúčtovanie (A=zaúčtovaný) |
| DstStk | Str1 | 2 | Stav skladu (N=nezrealizovaný, S=zrealizovaný) |
| Sended | byte | 1 | Príznak odoslania zmien |

### Šarže

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RbaCode | Str30 | 31 | Kód výrobnej šarže |
| RbaDate | DateType | 4 | Dátum výrobnej šarže |

### Ostatné

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Describe | Str30 | 31 | Popis dokladu |
| RspName | Str30 | 31 | Celé meno používateľa |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (13)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | ScStkNum, SerNum | ScStSn | Duplicit |
| 1 | Year, SerNum | YearSerNum | Unique |
| 2 | DocNum | DocNum | Duplicit |
| 3 | DocDate | DocDate | Duplicit |
| 4 | TgStkNum | TgStkNum | Duplicit |
| 5 | EValue | EValue | Duplicit |
| 6 | BValue | BValue | Duplicit |
| 7 | CValue | CValue | Duplicit |
| 8 | AValue | AValue | Duplicit |
| 9 | OcdNum | OcdNum | Duplicit |
| 10 | Describe | Describe | Duplicit, Case insensitive |
| 11 | Sended | Sended | Duplicit |
| 12 | RbaCode | RbaCode | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| ScStkNum | STKLST.StkNum | Zdrojový sklad |
| TgStkNum | STKLST.StkNum | Cieľový sklad |
| ScSmCode | SMLST.SmCode | Pohyb výdaja |
| TgSmCode | SMLST.SmCode | Pohyb príjmu |
| OcdNum | OCH.DocNum | Zákazka |
| SrdNum | *.DocNum | Zdrojový doklad |

## Použitie

- Medziskladové presuny tovaru
- Presun medzi prevádzkami
- Centrálna distribúcia
- Inventory balancing

## Business pravidlá

- Jeden doklad = simultánny výdaj a príjem
- ScStkNum ≠ TgStkNum (inak nemá zmysel)
- DstLck=1 znemožňuje ďalšie úpravy
- Pri realizácii sa aktualizujú oba sklady atomicky

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
