# OSGREM - Presun tovaru medzi skladmi

## Kľúčové slová / Aliases

OSGREM, OSGREM.BTR, pripomienky skupín objednávok, PO group reminders

## Popis

Tabuľka zoznamu tovarov, ktoré treba presunúť medzi skladmi v súvislosti s dodávateľskými objednávkami.

## Btrieve súbor

`OSGREM.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OSGREM.BTR`

## Štruktúra polí (11 polí)

### Identifikácia presunu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OutStk | word | 2 | Číslo skladu výdaja |
| IncStk | word | 2 | Číslo skladu príjmu |
| GsCode | longint | 4 | Tovarové číslo (PLU) |
| GsQnt | double | 8 | Množstvo na presun |

### Väzba na objednávku

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OsdNum | Str12 | 13 | Číslo dodávateľskej objednávky |
| OsdItm | word | 2 | Riadok objednávky |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |

## Indexy (3)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | OutStk | OutStk | Duplicit |
| 1 | IncStk | IncStk | Duplicit |
| 2 | OsdNum, OsdItm | OnOi | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| OutStk | STKLST.StkNum | Výdajový sklad |
| IncStk | STKLST.StkNum | Príjmový sklad |
| GsCode | GSCAT.GsCode | Tovar |
| OsdNum | OSHLST.DocNum | Objednávka |

## Workflow

```
1. Objednávka na centrálny sklad
   ↓
2. Identifikácia potreby na prevádzke
   ↓
3. Zápis do OSGREM (OutStk=centrála, IncStk=prevádzka)
   ↓
4. Príjem tovaru na centrálny sklad
   ↓
5. Generovanie medziskladového presunu
   ↓
6. Vymazanie záznamu z OSGREM
```

## Použitie

- Plánovanie medziskladových presunov
- Distribúcia tovaru z centrálneho skladu
- Optimalizácia zásobovania prevádzok

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
