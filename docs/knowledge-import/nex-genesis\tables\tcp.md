# TCP - Výrobné čísla ODL

## Kľúčové slová / Aliases

TCP, TCP.BTR, dodacie listy platby, delivery payments

## Popis

Tabuľka výrobných (sériových) čísel tovaru vydaného na odberateľských dodacích listoch. Umožňuje sledovanie konkrétnych kusov tovaru s výrobným číslom.

## Btrieve súbor

`TCPyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\TCPyynnn.BTR`

## Štruktúra polí (12 polí)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Číslo DL - **FK → TCH.DocNum** |
| ItmNum | word | 2 | Číslo položky DL |
| GsCode | longint | 4 | Tovarové číslo (PLU) |
| ProdNum | Str30 | 31 | Výrobné číslo tovaru |
| DocDate | DateType | 4 | Dátum výdaja tovaru |
| StkNum | word | 2 | Číslo skladu výdaja |
| Sended | byte | 1 | Príznak odoslania (0/1) |
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
| DocNum | TCH.DocNum | Hlavička DL |
| DocNum, ItmNum | TCI.DocNum, TCI.ItmNum | Položka DL |
| GsCode | GSCAT.GsCode | Tovar |
| StkNum | STKLST.StkNum | Sklad |

## Použitie

- Sledovanie konkrétnych kusov tovaru (elektronika, stroje)
- Záručné reklamácie
- Spätná dohľadateľnosť
- Inventarizácia podľa výrobných čísel

## Workflow

```
1. Výdaj tovaru s výrobným číslom
   ↓
2. Zadanie výrobného čísla pri vyskladnení
   ↓
3. Zápis do TCP
   ↓
4. Prepojenie s položkou DL (TCI)
   ↓
5. Synchronizácia (Sended)
```

## Business pravidlá

- Jedna položka DL môže mať viac výrobných čísel
- Výrobné číslo je unikátne pre daný tovar
- Umožňuje spätnú dohľadateľnosť zákazníka

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
