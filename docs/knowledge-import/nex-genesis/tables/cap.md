# CAP - Register pokladničných platidiel

## Kľúčové slová / Aliases

CAP, CAP.BTR, register, pokladničných, platidiel

## Popis

Tabuľka registra platobných prostriedkov pokladne. Sleduje aktuálny stav jednotlivých typov platidiel (hotovosť, karty, stravovacie lístky). Každá pokladňa má vlastný súbor.

## Btrieve súbor

`CAPnnnnn.BTR` (nnnnn=číslo pokladne)

## Umiestnenie

`C:\NEX\YEARACT\CAB\CAPnnnnn.BTR`

## Štruktúra polí (12 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayNum | byte | 1 | Kód platidla (0-9) |
| PayName | Str30 | 31 | Názov platidla |

### Hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayVal | double | 8 | Aktuálna hodnota platidla |
| BegVal | double | 8 | Denný počiatočný stav |
| IncVal | double | 8 | Príjem do pokladne |
| TrnVal | double | 8 | Denná tržba |
| ExpVal | double | 8 | Denný odvod tržby |
| EndVal | double | 8 | Denný konečný stav |
| ChIVal | double | 8 | Príjem - zmena platidla |
| ChEVal | double | 8 | Výdaj - zmena platidla |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | PayNum | PayNum | Duplicit, Case-insensitive |

## Typické platidlá

| PayNum | PayName | Popis |
|--------|---------|-------|
| 0 | Hotovosť | Platba v hotovosti (EUR) |
| 1 | Platobná karta | Platba platobnou kartou |
| 2 | Stravovacie lístky | Gastro lístky, poukážky |
| 3 | Šek | Šeková platba |
| 4 | Preddavok | Záloha, depozit |
| 5 | Kredit | Platba na úver |
| 6 | CZK | Platba v cudzej mene |
| 7-9 | Ostatné | Podľa konfigurácie |

## Výpočet

```
EndVal = BegVal + TrnVal + IncVal - ExpVal + ChIVal - ChEVal
```

## Príklad

```
Pokladňa č. 1 (CAP00001.BTR)
─────────────────────────────────────────────────────────────────
PayNum=0  PayName="Hotovosť"
  BegVal  =   500.00 EUR (počiatočný stav)
  TrnVal  = 1,250.00 EUR (denná tržba)
  IncVal  =   200.00 EUR (vklad do pokladne)
  ExpVal  = 1,000.00 EUR (odvod tržby)
  ChIVal  =     0.00 EUR
  ChEVal  =     0.00 EUR
  EndVal  =   950.00 EUR (konečný stav)
─────────────────────────────────────────────────────────────────
PayNum=1  PayName="Platobná karta"
  TrnVal  =   850.00 EUR (denná tržba kartami)
```

## Použitie

- Sledovanie aktuálneho stavu platidiel
- Denná uzávierka
- Odvod tržby
- Vklady do pokladne
- Zmena platidiel (výmena meny)

## Business pravidlá

- Maximálne 10 typov platidiel (0-9)
- Každá pokladňa má vlastný register
- BegVal = EndVal z predchádzajúceho dňa
- ExpVal = odvod do hlavnej pokladne (CSB)

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
