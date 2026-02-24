# STM - Denník skladových pohybov

## Kľúčové slová / Aliases

STM, STM.BTR, skladové miesta, storage locations, pozície, lokácie, regály

## Popis

Tabuľka všetkých skladových pohybov (príjmy, výdaje, presuny). Každý pohyb je prepojený na FIFO kartu pre správne oceňovanie.

## Btrieve súbor

`STMxxxxx.BTR` (x = číslo skladu)

## Umiestnenie

`C:\NEX\YEARACT\STORES\STMxxxxx.BTR`

## Polia

### Identifikácia pohybu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StmNum | longint | 4 | Poradové číslo pohybu - **PRIMARY KEY** |
| DocNum | Str12 | 13 | Interné číslo skladového dokladu |
| ItmNum | longint | 4 | Poradové číslo položky v doklade |
| DocDate | DateType | 4 | Dátum skladového dokladu |
| SmCode | word | 2 | Kód skladového pohybu (FK → SMLST) |

### Tovar

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo (PLU) |
| MgCode | longint | 4 | Tovarová skupina |
| GsName | Str30 | 31 | Názov tovaru |

### FIFO a množstvo

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FifNum | longint | 4 | Číslo FIFO karty |
| GsQnt | double | 8 | Množstvo tovaru |

### Hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CValue | double | 8 | Hodnota v NC bez DPH |
| BValue | double | 8 | Hodnota v PC s DPH |
| BPrice | double | 8 | PC s DPH za MJ |

### Objednávka

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OcdNum | Str12 | 13 | Číslo zákazky (došlej objednávky) |
| OcdItm | longint | 4 | Číslo riadku zákazky |

### Partner

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Kód partnera (dodávateľ/odberateľ) |
| SpaCode | longint | 4 | Kód dodávateľa |

### Presun a stav

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ConStk | word | 2 | Protisklad (odkiaľ/kam presun) |
| AcqStat | Str1 | 2 | Príznak obstarania (R=riadny, K=komisionálny) |
| BegStat | Str1 | 2 | Príznak počiatočného stavu (B) |
| Sended | byte | 1 | Príznak odoslania zmien (0/1) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (10)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | StmNum | StmNum | Duplicit |
| 1 | DocNum, ItmNum | DoIt | Duplicit |
| 2 | GsCode | GsCode | Duplicit |
| 3 | DocDate | DocDate | Duplicit |
| 4 | SmCode | SmCode | Duplicit |
| 5 | FifNum | FifNum | Duplicit |
| 6 | OcdNum, OcdItm | OdOi | Duplicit |
| 7 | PaCode | PaCode | Duplicit |
| 8 | SpaCode | SpaCode | Duplicit |
| 9 | Sended | Sended | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| GsCode | STK.GsCode | Skladová karta |
| MgCode | MGLST.MgCode | Tovarová skupina |
| SmCode | SMLST.SmCode | Typ pohybu |
| FifNum | FIF.FifNum | FIFO karta |
| PaCode | PAB.PaCode | Partner |
| SpaCode | PAB.PaCode | Dodávateľ |
| DocNum | ISC/OSC.DocNum | Skladový doklad |

## Typy pohybov

Pohyby sú definované v SMLST:
- Príjem (+): príjemka od dodávateľa
- Výdaj (-): výdajka na predaj/spotrebu
- Presun príjem (+): príjem z iného skladu
- Presun výdaj (-): výdaj do iného skladu

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
