# CASORD - Pokladničné objednávky

## Kľúčové slová / Aliases

CASORD, CASORD.BTR, pokladničné, objednávky

## Popis

Tabuľka pokladničných objednávok. Používa sa v gastronómii pre tlač objednávok do kuchyne alebo baru. Obsahuje položky objednávky s informáciou o tlači. Globálny súbor.

## Btrieve súbor

`CASORD.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DATA\CASORD.BTR`

## Štruktúra polí (16 polí)

### Identifikácia objednávky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CsdName | Str10 | 11 | Názov pokladničnej účtenky (stôl) |
| OrdNum | longint | 4 | Poradové číslo objednávky |
| SubNum | word | 2 | Podčíslo objednávky |
| CsdNum | longint | 4 | Poradové číslo účtenky |

### Položka

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo - **FK GSCAT** |
| GsName | Str30 | 31 | Názov tovaru |
| _GsName | Str30 | 31 | Názov tovaru - vyhľadávacie pole |
| GsQnt | double | 8 | Objednané množstvo |
| BPrice | double | 8 | Predajná cena s DPH |

### Pokladník a tlač

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CasUsn | Str30 | 31 | Meno a priezvisko pokladníka |
| OrdPrn | byte | 1 | Port tlačiarne (oddelenie) |
| OrdDate | DateType | 4 | Dátum objednávky |
| OrdTime | TimeType | 4 | Čas objednávky |
| PrnStat | Str1 | 2 | Stav tlače (P=vytlačená) |

## Indexy (7)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | CsdName | CsdName | Duplicit |
| 1 | OrdNum | OrdNum | Duplicit |
| 2 | OrdNum, SubNum | OnSn | Duplicit |
| 3 | GsCode | GsCode | Duplicit |
| 4 | _GsName | GsName | Duplicit, Case-insensitive |
| 5 | CasUsn | CasUsn | Duplicit |
| 6 | PrnStat | PrnStat | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| GsCode | GSCAT.GsCode | Katalógová karta tovaru |

## Stavové hodnoty (PrnStat)

| Hodnota | Popis |
|---------|-------|
| (prázdne) | Nevytlačená |
| P | Vytlačená |

## Príklad použitia

```
Reštaurácia - Stôl 5
─────────────────────────────────────────────────────────────────
CsdName = "Stol_05"
OrdNum  = 1234
─────────────────────────────────────────────────────────────────
SubNum=1  GsName="Pivo 0.5l"    GsQnt=2  OrdPrn=1 (Bar)
SubNum=2  GsName="Grilované kura" GsQnt=1  OrdPrn=2 (Kuchyňa)
SubNum=3  GsName="Hranolky"     GsQnt=1  OrdPrn=2 (Kuchyňa)
─────────────────────────────────────────────────────────────────
CasUsn = "Ján Kováč"
OrdDate = 15.01.2024
OrdTime = 18:35:00
```

## Workflow

```
1. Čašník zadá objednávku na POS terminál
   ↓
2. Systém vytvorí záznamy v CASORD
   ↓
3. Objednávka sa vytlačí na príslušnej tlačiarni
   - OrdPrn=1 → Tlačiareň BAR
   - OrdPrn=2 → Tlačiareň KUCHYŇA
   ↓
4. PrnStat sa zmení na 'P'
   ↓
5. Po zaplatení sa položky presunú do SAI
```

## Použitie

- Gastronómia - objednávky do kuchyne/baru
- Sledovanie nevytlačených objednávok
- Identifikácia pokladníka
- Rozdelenie objednávok podľa oddelení (OrdPrn)

## Business pravidlá

- CsdName = identifikátor stola/účtenky
- OrdPrn = port tlačiarne podľa typu tovaru (bar, kuchyňa, gril...)
- Objednávky sa tlačia hneď po zadaní
- Po vytlačení sa nastaví PrnStat='P'

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
