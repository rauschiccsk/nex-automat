# PLH - História zmien predajných cien

## Kľúčové slová / Aliases

PLH, PLH.BTR, história, zmien, predajných, cien

## Popis

História zmien predajných cien. Zaznamenáva každú zmenu ceny tovaru v cenníku s pôvodnými a novými hodnotami, zdrojovým programom a používateľom.

## Btrieve súbor

`PLHnnnnn.BTR` (nnnnn = číslo cenníka)

## Umiestnenie

`C:\NEX\YEARACT\STK\PLHnnnnn.BTR`

## Štruktúra polí (14 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo (PLU) |

### Pôvodné hodnoty (O* = Old)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OProfit | double | 8 | Starý zisk v % |
| OAPrice | double | 8 | Stará predajná cena bez DPH |
| OBPrice | double | 8 | Stará predajná cena s DPH |

### Nové hodnoty (N* = New)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| NProfit | double | 8 | Nový zisk v % |
| NAPrice | double | 8 | Nová predajná cena bez DPH |
| NBPrice | double | 8 | Nová predajná cena s DPH |

### Údaje zmeny

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Status | Str1 | 2 | Príznak zmeny (A=akciové, E=ukončenie akcie) |
| ModPrg | Str3 | 4 | Skrátený názov programového modulu |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ zmeny |
| CrtDate | DateType | 4 | Dátum zmeny |
| CrtTime | TimeType | 4 | Čas zmeny |

## Indexy (5)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | GsCode | GsCode | Duplicit |
| 1 | CrtUser | CrtUser | Duplicit |
| 2 | CrtDate | CrtDate | Duplicit |
| 3 | Status | Status | Duplicit |
| 4 | ModPrg | ModPrg | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| GsCode | PLS.GsCode | Položka cenníka |

## Príklady Status

| Status | Popis |
|--------|-------|
| A | Akciové precenenie |
| E | Ukončenie akcie |
| (prázdny) | Bežná zmena ceny |

## Príklady ModPrg

| ModPrg | Popis |
|--------|-------|
| PLS | Predajné cenníky |
| ISB | Dodávateľské faktúry |
| TSB | Dodávateľské dodacie listy |
| IMB | Interné príjemky |

## Použitie

- Audit zmien predajných cien
- Sledovanie histórie cenových akcií
- Analýza cenotvorby podľa zdrojových modulov
- Prehľad zmien podľa používateľov

## Business pravidlá

- Každá zmena ceny v PLS vytvára záznam v PLH
- Status='A' pri začiatku akcie, 'E' pri ukončení
- ModPrg identifikuje modul, ktorý spôsobil zmenu
- Pre jedno GsCode môže existovať viac záznamov (história)

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
