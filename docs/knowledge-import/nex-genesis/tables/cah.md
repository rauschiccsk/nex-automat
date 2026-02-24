# CAH - Denné uzávierkové údaje pokladne

## Kľúčové slová / Aliases

CAH, CAH.BTR, denné, uzávierkové, údaje, pokladne

## Popis

Tabuľka denných uzávierkových údajov registračnej pokladne (Z-report). Obsahuje tržby, platobné prostriedky, DPH a súhrnné hodnoty za jeden deň. Každá kniha má vlastný súbor.

## Btrieve súbor

`CAHnnnnn.BTR` (nnnnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\CAB\CAHnnnnn.BTR`

## Štruktúra polí (107 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocDate | DateType | 4 | Dátum uzávierky |

### Platobné prostriedky (10 typov, x=0-9)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayNameX | Str20 | 21 | Názov platidla |
| BegValX | double | 8 | Počiatočný stav |
| TrnValX | double | 8 | Denná tržba |
| IncValX | double | 8 | Príjem do pokladne |
| ExpValX | double | 8 | Odvod tržby |
| ChIValX | double | 8 | Príjem - zmena platidla |
| ChEValX | double | 8 | Výdaj - zmena platidla |

### DPH členenie (3 sadzby)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc1 | byte | 1 | Sadzba DPH 1 v % |
| VatPrc2 | byte | 1 | Sadzba DPH 2 v % |
| VatPrc3 | byte | 1 | Sadzba DPH 3 v % |
| VatVal1 | double | 8 | Hodnota DPH 1 |
| VatVal2 | double | 8 | Hodnota DPH 2 |
| VatVal3 | double | 8 | Hodnota DPH 3 |
| BValue1 | double | 8 | Hodnota predaja s DPH 1 |
| BValue2 | double | 8 | Hodnota predaja s DPH 2 |
| BValue3 | double | 8 | Hodnota predaja s DPH 3 |

### Súhrnné hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GT1Val | double | 8 | Hrubý obrat |
| GT2Val | double | 8 | Čistý obrat |
| GT3Val | double | 8 | Záporný obrat |
| AValue | double | 8 | Celková hodnota bez DPH |
| VatVal | double | 8 | Celková hodnota DPH |
| BValue | double | 8 | Celková hodnota s DPH |
| ClmVal | double | 8 | Hodnota reklamácií |
| NegVal | double | 8 | Hodnota záporných položiek |
| DscVal | double | 8 | Hodnota zliav |
| CncVal | double | 8 | Hodnota stornovaných bločkov |
| BegVal | double | 8 | Počiatočný stav všetkých platidiel |
| TrnVal | double | 8 | Tržba všetkých platidiel |
| ExpVal | double | 8 | Hodnota výdajov z pokladne |
| IncVal | double | 8 | Hodnota príjmov do pokladne |
| EndVal | double | 8 | Konečný stav všetkých platidiel |
| ChEVal | double | 8 | Výdaj - zmena platidla (súhrnný) |
| ChIVal | double | 8 | Príjem - zmena platidla (súhrnný) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Poradové číslo modifikácie |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocDate | DocDate | Duplicit |

## Výpočty

```
┌─────────────────────────────────────────────────────────────────┐
│ KONEČNÝ STAV PLATIDLA                                           │
│ EndValX = BegValX + TrnValX + IncValX - ExpValX                 │
│           + ChIValX - ChEValX                                   │
├─────────────────────────────────────────────────────────────────┤
│ SÚHRNNÁ TRŽBA                                                   │
│ TrnVal = Σ TrnValX (x=0..9)                                     │
├─────────────────────────────────────────────────────────────────┤
│ HODNOTA S DPH                                                   │
│ BValue = BValue1 + BValue2 + BValue3                            │
│ VatVal = VatVal1 + VatVal2 + VatVal3                            │
│ AValue = BValue - VatVal                                        │
└─────────────────────────────────────────────────────────────────┘
```

## Príklad

```
DocDate  = 15.01.2024
─────────────────────────────────────────────────────────────────
Platidlá:
  PayName0 = "Hotovosť"     TrnVal0 = 1250.00 EUR
  PayName1 = "Plat. karta"  TrnVal1 =  850.00 EUR
  PayName2 = "Strav. lístky" TrnVal2 =  420.00 EUR
─────────────────────────────────────────────────────────────────
DPH:
  VatPrc1=20%, VatVal1=350.00, BValue1=2100.00
  VatPrc2=10%, VatVal2= 38.18, BValue2= 420.00
─────────────────────────────────────────────────────────────────
Súhrn:
  BValue = 2520.00 EUR (s DPH)
  VatVal =  388.18 EUR
  AValue = 2131.82 EUR (bez DPH)
  TrnVal = 2520.00 EUR (celková tržba)
```

## Použitie

- Denné uzávierky (Z-report)
- Sledovanie tržieb podľa platidiel
- DPH evidencia
- Reklamácie a stornované bločky
- Zmeny platidiel (výmena meny)

## Business pravidlá

- Jeden záznam na deň (DocDate je kľúč)
- 10 typov platidiel (0-9)
- 3 sadzby DPH
- ChIVal/ChEVal = zmena platidla (napr. výmena EUR za CZK)
- EndVal = konečný stav pokladne

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
