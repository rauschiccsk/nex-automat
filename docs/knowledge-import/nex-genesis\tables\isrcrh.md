# ISRCRH - Hlavičky koncoročného prekurzovania DF

## Kľúčové slová / Aliases

ISRCRH, ISRCRH.BTR, reklamácie hlavičky, claims header, reklamačné prípady

## Popis

Hlavičková tabuľka koncoročného prekurzovania dodávateľských faktúr v cudzej mene. Obsahuje sumárne hodnoty kurzových rozdielov podľa mien.

## Btrieve súbor

`ISRCRH.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ISRCRH.BTR`

## Polia (18)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DvzName | Str3 | 4 | Mena - **PRIMARY KEY** |
| NCourse | double | 8 | Nový (koncoročný) kurz |
| NAEndVal | double | 8 | Nový zostatok v tuzemskej mene |
| NFEndVal | double | 8 | Nový zostatok v zahraničnej mene |
| NCrdVal | double | 8 | Kurzový rozdiel aktuálny rok |
| OAEndVal | double | 8 | Starý zostatok v tuzemskej mene |
| OFEndVal | double | 8 | Starý zostatok v zahraničnej mene |
| OCrdVal | double | 8 | Kurzový rozdiel predchádzajúci rok |
| CrdVal | double | 8 | Celkový kurzový rozdiel |
| AccDoc | Str12 | 13 | Číslo účtovného dokladu |
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DvzName | DvzName | Duplicit |

## Výpočet kurzového rozdielu

```
Kurzový rozdiel = (Nový kurz - Starý kurz) × Zostatok v cudzej mene

CrdVal = NCrdVal - OCrdVal
kde:
- NCrdVal = NAEndVal - (NFEndVal × NCourse)
- OCrdVal = OAEndVal - (OFEndVal × OCourse)
```

## Workflow

```
1. Koniec účtovného roku
   ↓
2. Načítanie kurzov NBS k 31.12.
   ↓
3. Prepočet zostatok všetkých DF v cudzej mene
   ↓
4. Výpočet kurzových rozdielov
   ↓
5. Vytvorenie účtovného dokladu
   ↓
6. Zaúčtovanie kurzových rozdielov
```

## Business pravidlá

- Prekurzovanie sa robí k 31.12. každého roku
- Kurzové rozdiely sa účtujú na účty 563/663
- Každá mena má samostatný záznam

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
