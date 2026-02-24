# SMLST - Zoznam skladových operácií

## Kľúčové slová / Aliases

SMLST, SMLST.BTR, merné jednotky, units of measure, jednotky, egységek

## Popis

Číselník typov skladových pohybov (operácií). Definuje, či ide o príjem alebo výdaj, a obsahuje účtovné predkontácie.

## Btrieve súbor

`STMLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\STORES\STMLST.BTR`

## Polia

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SmCode | longint | 4 | Kód skladového pohybu - **PRIMARY KEY** |
| SmName | Str30 | 31 | Názov skladového pohybu |
| _SmName | Str30 | 31 | Vyhľadávacie pole názvu |
| SmSign | Str1 | 2 | Znak pohybu (+príjem, -výdaj) |

### Účtovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AcSign | Str1 | 2 | Znak účtovného zápisu |
| CAccSnt | Str3 | 4 | Syntetický účet MD |
| CAccAnl | Str6 | 7 | Analytický účet MD |
| CAccStk | byte | 1 | Účtovanie podľa skladov (MD) |
| CAccWri | byte | 1 | Účtovanie podľa prevádzok (MD) |
| CAccCen | byte | 1 | Účtovanie podľa stredísk (MD) |
| DAccSnt | Str3 | 4 | Syntetický účet DAL |
| DAccAnl | Str6 | 7 | Analytický účet DAL |
| DAccStk | byte | 1 | Účtovanie podľa skladov (DAL) |
| DAccWri | byte | 1 | Účtovanie podľa prevádzok (DAL) |
| DAccCen | byte | 1 | Účtovanie podľa stredísk (DAL) |

### Synchronizácia a audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Sended | byte | 1 | Príznak odoslania zmien |
| ModNum | word | 2 | Poradové číslo modifikácie |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (3)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | SmCode | SmCode | Duplicit |
| 1 | _SmName | SmName | Case-insensitive, Duplicit |
| 2 | Sended | Sended | Duplicit |

## Typy pohybov

| SmSign | SmCode | SmName | Popis |
|--------|--------|--------|-------|
| + | 1 | Príjem od dodávateľa | Štandardný príjem |
| - | 2 | Výdaj na predaj | Výdaj do POS |
| + | 3 | Príjem z presunu | Presun z iného skladu |
| - | 4 | Výdaj na presun | Presun do iného skladu |
| + | 5 | Inventúrny prebytok | Inventúrny príjem |
| - | 6 | Inventúrny manko | Inventúrny výdaj |
| - | 7 | Spotreba | Interná spotreba |

## Účtovné predkontácie

Príklad pre príjem od dodávateľa:
```
MD: 132 (Sklad tovaru)    → CAccSnt="132"
DAL: 321 (Dodávatelia)    → DAccSnt="321"
```

## Business pravidlá

- SmSign="+" zvyšuje zásobu (STK.InQnt)
- SmSign="-" znižuje zásobu (STK.OutQnt)
- Predkontácie sa používajú pri účtovnej uzávierke
- Analytika môže byť dynamická podľa skladu/prevádzky

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
