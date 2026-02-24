# TCHOLE - Voľné poradové čísla ODL

## Kľúčové slová / Aliases

TCHOLE, TCHOLE.BTR, prázdne čísla DL, delivery number gaps

## Popis

Tabuľka voľných (uvoľnených) poradových čísel odberateľských dodacích listov. Vznikajú pri mazaní rozpracovaných DL a môžu byť znovu použité.

## Btrieve súbor

`TCHOLE.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\TCHOLE.BTR`

## Štruktúra polí (5 polí)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BookNum | Str5 | 6 | Číslo knihy ODL |
| SerNum | longint | 4 | Voľné poradové číslo |
| ModUser | Str8 | 9 | Používateľ uvoľnenia |
| ModDate | DateType | 4 | Dátum uvoľnenia |
| ModTime | TimeType | 4 | Čas uvoľnenia |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | BookNum, SerNum | BnSn | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| BookNum | TCBLST.BookNum | Kniha DL |

## Workflow

```
1. Vytvorenie DL → SerNum pridelené
   ↓
2. Zrušenie prázdneho DL
   ↓
3. Zápis do TCHOLE (SerNum uvoľnené)
   ↓
4. Nový DL → použije sa SerNum z TCHOLE
   ↓
5. Vymazanie záznamu z TCHOLE
```

## Business pravidlá

- Zabezpečuje súvislé číslovanie dokladov
- Voľné čísla sa využívajú prednostne
- Auditný záznam o uvoľnení čísla

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
