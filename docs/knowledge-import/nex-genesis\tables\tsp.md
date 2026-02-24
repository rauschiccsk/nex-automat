# TSP - Výrobné čísla dodávateľských DL

## Kľúčové slová / Aliases

TSP, TSP.BTR, pokladničné platby, cash payments, spôsoby úhrady

## Popis

Tabuľka výrobných čísel (sériových čísel) prijatých na dodávateľských dodacích listoch. Umožňuje evidenciu individuálnych kusov tovaru.

## Btrieve súbor

`TSPyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\TSPyynnn.BTR`

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Číslo DDL |
| ItmNum | word | 2 | Číslo položky DDL |
| GsCode | longint | 4 | Tovarové číslo (PLU) |
| ProdNum | Str30 | 31 | Výrobné číslo |
| DocDate | DateType | 4 | Dátum príjmu |
| StkNum | word | 2 | Číslo skladu |
| Sended | byte | 1 | Príznak odoslania zmien |
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |

## Indexy (6)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum, ProdNum | DoItPn | Duplicit |
| 1 | DocNum, ItmNum | DoIt | Duplicit |
| 2 | DocNum | DocNum | Duplicit |
| 3 | GsCode | GsCode | Duplicit |
| 4 | ProdNum | ProdNum | Case-insensitive, Duplicit |
| 5 | Sended | Sended | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | TSH.DocNum | Hlavička dokladu |
| DocNum, ItmNum | TSI.(DocNum, ItmNum) | Položka dokladu |
| GsCode | GSCAT.GsCode | Tovar |
| StkNum | STKLST.StkNum | Sklad |

## Workflow

```
1. Príjem tovaru na DDL
   ↓
2. Zaevidovanie výrobných čísel (TSP)
   ↓
3. Príjem na sklad → STKPDN
```

## Business pravidlá

- Jedna položka DDL môže mať viac výrobných čísel
- Počet TSP záznamov = množstvo GsQnt (pre položky s PdnMust=1)
- Pri príjme na sklad sa vytvárajú záznamy v STKPDN

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
