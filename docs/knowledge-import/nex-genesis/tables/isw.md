# ISW - História upomienok k dodávateľským faktúram

## Kľúčové slová / Aliases

ISW, ISW.BTR, príjemky zálohy, receipt advances, zálohové platby

## Popis

Tabuľka histórie upomienok prijatých od dodávateľov k neuhradenám faktúram. Sleduje priebeh upomienania a vystavené upomienky.

## Btrieve súbor

`ISWbbbbb.BTR` (bbbbb=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ISWbbbbb.BTR`

## Polia (13)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| IsdNum | Str12 | 13 | Interné číslo faktúry - **FK → ISH** |
| WrnNum | byte | 1 | Číslo upomienky |
| WrnVal | double | 8 | Hodnota, na ktorú bola vystavená upomienka |
| WrnDate | DateType | 4 | Dátum vystavenia upomienky |
| RegDate | DateType | 4 | Dátum zaevidovania |
| RegUser | Str10 | 11 | Používateľ, ktorý zaevidoval |
| RegName | Str30 | 31 | Meno a priezvisko používateľa |
| CrtUser | Str8 | 9 | Používateľ vytvorenia záznamu |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | IsdNum | IsdNum | Duplicit |
| 1 | IsdNum, WrnNum | InWn | Unique |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| IsdNum | ISH.DocNum | Hlavička faktúry |

## Workflow

```
1. Prijatie upomienky od dodávateľa
   ↓
2. Zaevidovanie do ISW
   ↓
3. Aktualizácia ISH.WrnNum, ISH.WrnDate
   ↓
4. Sledovanie histórie upomienok
```

## Business pravidlá

- Číslo upomienky sa zvyšuje s každou ďalšou upomienkou
- Hodnota WrnVal = zostatok k úhrade v čase upomienky
- Sleduje sa osoba, ktorá zaevidovala upomienku

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
