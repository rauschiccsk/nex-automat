# STKPOS - Skladové pozičné miesta

## Kľúčové slová / Aliases

STKPOS, STKPOS.BTR, pozičná evidencia, position tracking, umiestnenie tovaru

## Popis

Tabuľka pozičného skladovania (bin locations). Umožňuje evidovať tovar na konkrétnych pozíciách v sklade (regály, priehradky).

## Btrieve súbor

`STKPOS.BTR`

## Umiestnenie

`C:\NEX\YEARACT\STORES\STKPOS.BTR`

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | word | 2 | Číslo skladu |
| ProNum | longint | 4 | Produktové číslo (GsCode) |
| PosCod | Str15 | 16 | Kód pozičného miesta |
| ActPrq | double | 8 | Aktuálna zásoba na pozícii |
| CrtUsr | Str10 | 11 | Používateľ vytvorenia |
| CrtDte | DateType | 4 | Dátum vytvorenia |
| CrtTim | TimeType | 4 | Čas vytvorenia |

## Indexy (4)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | StkNum | StkNum | Duplicit |
| 1 | StkNum, ProNum, PosCod | SnPnPc | Unique (Composite PK) |
| 2 | StkNum, ProNum | SnPn | Duplicit |
| 3 | StkNum, PosCod | SnPc | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| StkNum | STKLST.StkNum | Sklad |
| ProNum | STK.GsCode | Skladová karta |

## Formát pozičného kódu

Typický formát: `AABBCC`
- AA = Číslo regálu
- BB = Políca
- CC = Priehradka

Príklad: `01A3-05` = Regál 01, sekcia A3, pozícia 05

## Business pravidlá

- Jeden tovar môže byť na viacerých pozíciách
- Jedna pozícia môže obsahovať viacero tovarov
- Composite PK: (StkNum, ProNum, PosCod)
- Suma ActPrq pre položku = STK.PosQnt

## Príklad dát

| StkNum | ProNum | PosCod | ActPrq |
|--------|--------|--------|--------|
| 1 | 10001 | A01-01 | 50 |
| 1 | 10001 | A01-02 | 30 |
| 1 | 10002 | A01-01 | 25 |
| 1 | 10003 | B02-05 | 100 |

## Použitie

- WMS (Warehouse Management System)
- Vychystávanie objednávok
- Inventúra podľa pozícií
- Optimalizácia skladovania

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
