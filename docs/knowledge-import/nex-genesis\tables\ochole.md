# OCHOLE - Voľné poradové čísla zákaziek

## Kľúčové slová / Aliases

OCHOLE, OCHOLE.BTR, prázdne čísla objednávok, order number gaps

## Popis

Tabuľka voľných (uvoľnených) poradových čísel zákaziek. Vznikajú pri mazaní rozpracovaných zákaziek a môžu byť znovu použité.

## Btrieve súbor

`OCHOLE.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OCHOLE.BTR`

## Štruktúra polí (7 polí)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Year | Str2 | 3 | Rok |
| BokNum | word | 2 | Číslo knihy |
| SerNum | longint | 4 | Voľné poradové číslo |
| DocNum | Str12 | 13 | Interné číslo dokladu |
| CrtUser | Str8 | 9 | Používateľ uvoľnenia |
| CrtDate | DateType | 4 | Dátum uvoľnenia |
| CrtTime | TimeType | 4 | Čas uvoľnenia |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | Year, BokNum, SerNum | YrBkSr | Unique |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| BokNum | OCBLST.BokNum | Kniha zákaziek |

## Workflow

```
1. Vytvorenie zákazky → SerNum pridelené
   ↓
2. Zrušenie prázdnej zákazky
   ↓
3. Zápis do OCHOLE (SerNum uvoľnené)
   ↓
4. Nová zákazka → použije sa SerNum z OCHOLE
   ↓
5. Vymazanie záznamu z OCHOLE
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
