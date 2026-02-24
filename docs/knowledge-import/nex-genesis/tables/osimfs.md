# OSIMFS - Výberový zoznam položiek MFS

## Kľúčové slová / Aliases

OSIMFS, OSIMFS.BTR, import objednávok, PO import

## Popis

Pracovná tabuľka pre výberový zoznam položiek systému MFS (Multi Filial System). Obsahuje agregované údaje o stave zásob a predajoch naprieč všetkými prevádzkami pre účely generovania objednávok.

## Btrieve súbor

`OSIMFS.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\OSIMFS.BTR`

## Štruktúra polí (79 polí)

### Identifikácia produktu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo (PLU) - **PRIMARY KEY** |
| MgCode | word | 2 | Tovarová skupina |
| GsName | Str30 | 31 | Názov tovaru |
| _GsName | Str30 | 31 | Vyhľadávacie pole |
| BarCode | Str15 | 16 | Čiarový kód |
| StkCode | Str15 | 16 | Skladový kód |
| VatPrc | byte | 1 | Sadzba DPH (%) |
| MsName | Str10 | 11 | Merná jednotka |

### Údaje za prevádzky 01-15

Pre každú prevádzku (01-15) existujú 4 polia:

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ActQntXX | double | 8 | Aktuálna skladová zásoba |
| BseQntXX | double | 8 | Celkový predaj v minulom roku |
| AseQntXX | double | 8 | Celkový predaj v aktuálnom roku |
| NsdQntXX | double | 8 | Nevysporiadané položky predaja |

### Súčty za všetky prevádzky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ActQnt | double | 8 | Celková aktuálna zásoba |
| BseQnt | double | 8 | Celkový predaj minulý rok |
| AseQnt | double | 8 | Celkový predaj aktuálny rok |
| NsdQnt | double | 8 | Celkové nevysporiadané |
| OsdQnt | double | 8 | Objednané množstvo od dodávateľa |
| OcdQnt | double | 8 | Rezervácie pre odberateľské objednávky |

### Ceny

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CPrice | double | 8 | NC bez DPH |
| BPrice | double | 8 | PC s DPH |

## Indexy (5)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | GsCode | GsCode | Unique |
| 1 | _GsName | GsName | Duplicit, Case insensitive |
| 2 | MgCode | MgCode | Duplicit |
| 3 | BarCode | BarCode | Duplicit |
| 4 | StkCode | StkCode | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| GsCode | GSCAT.GsCode | Tovar |
| MgCode | MGLST.MgCode | Tovarová skupina |

## Použitie

- Centrálny prehľad zásob naprieč prevádzkami
- Podklad pre automatické generovanie objednávok
- Analýza predajov a spotreby
- Optimalizácia zásobovania

## Business pravidlá

- Tabuľka sa pravidelne aktualizuje z dát jednotlivých prevádzok
- OsdQnt obsahuje už objednané množstvo (nezapočítané do novej objednávky)
- OcdQnt obsahuje rezervácie z odberateľských zákaziek

## Výpočet objednacieho množstva

```
Potreba = (PriemernýMesačnýVýdaj × ObjednacíKoeficient) + Rezervácie
Objednať = Potreba - AktuálnaZásoba - UžObjednané
```

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
