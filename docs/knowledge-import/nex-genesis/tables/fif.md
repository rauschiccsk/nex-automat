# FIF - FIFO karty tovarov

## Kľúčové slová / Aliases

FIF, FIF.BTR, FIFO evidencia, first in first out, šarže, dávky, batches

## Popis

Tabuľka FIFO kariet pre oceňovanie skladových zásob. Každý príjem tovaru vytvára novú FIFO kartu s nákupnou cenou. Pri výdaji sa čerpá z najstaršej karty (First In, First Out).

## Btrieve súbor

`FIFxxxxx.BTR` (x = číslo skladu)

## Umiestnenie

`C:\NEX\YEARACT\STORES\FIFxxxxx.BTR`

## Polia

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FifNum | longint | 4 | Poradové číslo FIFO karty - **PRIMARY KEY** |
| GsCode | longint | 4 | Tovarové číslo (PLU) |
| DocNum | Str12 | 13 | Číslo príjmového dokladu |
| ItmNum | longint | 4 | Číslo riadku príjmového dokladu |
| DocDate | DateType | 4 | Dátum príjmu |

### Množstvá

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| InQnt | double | 8 | Prijaté množstvo |
| OutQnt | double | 8 | Vydané množstvo |
| ActQnt | double | 8 | Zostatok k výdaju (InQnt - OutQnt) |
| PdnQnt | double | 8 | Množstvo s evidovaným výrobným číslom |

### Ceny a stav

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| InPrice | double | 8 | Nákupná cena bez DPH |
| Status | Str1 | 2 | Stav FIFO karty (A/W/X) |

### Trvanlivosť a šarža

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DrbDate | DateType | 4 | Dátum ukončenia trvanlivosti |
| RbaCode | Str30 | 31 | Kód výrobnej šarže |
| RbaDate | DateType | 4 | Dátum výrobnej šarže |

### Obstaranie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AcqStat | Str1 | 2 | Príznak obstarania (R=riadny, K=komisionálny) |
| PaCode | longint | 4 | Kód dodávateľa |
| BegStat | Str1 | 2 | Príznak počiatočného stavu (B) |

### Synchronizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Sended | byte | 1 | Príznak odoslania zmien (0/1) |

## Indexy (11)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | FifNum | FifNum | Duplicit |
| 1 | DocNum, ItmNum | DoIt | Duplicit |
| 2 | GsCode | GsCode | Duplicit |
| 3 | GsCode, Status | GsSt | Duplicit |
| 4 | GsCode, Status, DocDate | GsStDa | Duplicit (FIFO výber) |
| 5 | GsCode, Status, DrbDate | GsStDr | Duplicit (FEFO výber) |
| 6 | DocDate | DocDate | Duplicit |
| 7 | DrbDate | DrbDate | Duplicit |
| 8 | Sended | Sended | Duplicit |
| 9 | GsCode, RbaCode | GcRc | Duplicit |
| 10 | RbaCode | RbaCode | Duplicit |

## Stavy FIFO karty

| Status | Popis |
|--------|-------|
| A | Aktívna - obsahuje zásobu na výdaj |
| W | Čakajúca - čaká na aktiváciu |
| X | Spotrebovaná - ActQnt = 0 |

## FIFO princíp

```
Príjem 100 ks @ 10 EUR → FIF#1 (Status=A, ActQnt=100, InPrice=10)
Príjem 50 ks @ 12 EUR  → FIF#2 (Status=A, ActQnt=50, InPrice=12)

Výdaj 80 ks:
  - FIF#1: OutQnt += 80, ActQnt = 20 (zostáva)

Výdaj 40 ks:
  - FIF#1: OutQnt += 20, ActQnt = 0, Status = X (spotrebovaná)
  - FIF#2: OutQnt += 20, ActQnt = 30 (zostáva)
```

## FEFO variant

Index GsStDr umožňuje FEFO (First Expired, First Out) - výber podľa dátumu trvanlivosti namiesto dátumu príjmu.

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| GsCode | STK.GsCode | Skladová karta |
| DocNum, ItmNum | ISC položky | Príjmový doklad |
| PaCode | PAB.PaCode | Dodávateľ |

## Business pravidlá

- Jedna položka môže mať viac FIFO kariet
- Výdaj sa robí vždy z najstaršej aktívnej karty
- Hodnota výdaja = množstvo × InPrice danej FIFO karty
- Pri prekročení ActQnt sa pokračuje na ďalšiu kartu

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
