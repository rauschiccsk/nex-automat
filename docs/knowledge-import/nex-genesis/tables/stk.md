# STK - Skladové karty zásob

## Kľúčové slová / Aliases

STK, STK.BTR, skladové karty, zásoby, inventory, stock cards, raktár, készlet, sklad

## Popis

Hlavná tabuľka skladových kariet. Obsahuje informácie o zásobách, cenách, normatívoch a pohyboch pre každú tovarovú položku v danom sklade.

## Btrieve súbor

`STKxxxxx.BTR` (x = číslo skladu, napr. STK00001.BTR)

## Umiestnenie

`C:\NEX\YEARACT\STORES\STKxxxxx.BTR`

## Štruktúra polí (64 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo (PLU) - **FK → GSCAT** |
| MgCode | longint | 4 | Číslo hlavnej tovarovej skupiny |
| FgCode | longint | 4 | Číslo finančnej skupiny |
| GsName | Str30 | 31 | Názov tovaru |
| _GsName | Str15 | 16 | Vyhľadávacie pole názvu |
| BarCode | Str15 | 16 | Čiarový kód |
| StkCode | Str15 | 16 | Skladový kód |
| MsName | Str10 | 11 | Merná jednotka |
| GsType | Str1 | 2 | Typ položky (T=tovar, W=vážený, O=obal) |
| GaName | Str60 | 61 | Doplnkový názov |
| _GaName | Str60 | 61 | Vyhľadávacie pole doplnkového názvu |

### DPH a vlastnosti

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc | byte | 1 | Sadzba DPH % |
| DrbMust | byte | 1 | Povinné sledovanie trvanlivosti (0/1) |
| PdnMust | byte | 1 | Povinné sledovanie výrobných čísel (0/1) |
| GrcMth | word | 2 | Záručná doba (mesiace) |

### Množstvá - základné

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BegQnt | double | 8 | Počiatočné množstvo |
| InQnt | double | 8 | Celkový príjem od začiatku roka |
| OutQnt | double | 8 | Celkový výdaj od začiatku roka |
| ActQnt | double | 8 | Aktuálna skladová zásoba |
| FreQnt | double | 8 | Voľné množstvo (na predaj) |

### Množstvá - rezervácie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SalQnt | double | 8 | Predané, neodpočítané zo skladu |
| NrsQnt | double | 8 | Požiadavka na objednávku (nerezervované) |
| OcdQnt | double | 8 | Rezervácia pre odberateľské objednávky |
| OsdQnt | double | 8 | Objednané u dodávateľa |
| OsrQnt | double | 8 | Rezervácia z objednávky |
| FroQnt | double | 8 | Voľné množstvo z objednávky |
| ImrQnt | double | 8 | Rezervácia z príjemok (tovar na ceste) |
| PosQnt | double | 8 | Množstvo na pozičných miestach |
| OfrQnt | double | 8 | Ponúkané množstvo od dodávateľov |
| NsuQnt | double | 8 | Nevysporiadané položky |
| ActSnQnt | longint | 4 | Počet nevydaných výrobných čísel |

### Hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BegVal | double | 8 | Počiatočná hodnota |
| InVal | double | 8 | Hodnota celkového príjmu |
| OutVal | double | 8 | Hodnota celkového výdaja |
| ActVal | double | 8 | Aktuálna hodnota skladovej zásoby |

### Ceny

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AvgPrice | double | 8 | Priemerná NC (vážený priemer) |
| LastPrice | double | 8 | Posledná NC |
| ActPrice | double | 8 | Aktuálna NC (podľa aktívnej FIFO) |
| BPrice | double | 8 | Predajná cena s DPH |
| Profit | double | 8 | Obchodná marža |

### Normatívy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| MaxQnt | double | 8 | Maximálne množstvo (horná hranica) |
| MinQnt | double | 8 | Minimálne množstvo (dolná hranica) |
| OptQnt | double | 8 | Optimálne množstvo |
| MinMax | Str1 | 2 | Príznak prekročenia (X=max, N=min) |

### Dátumy a posledné pohyby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| InvDate | DateType | 4 | Dátum poslednej inventúry |
| LastIDate | DateType | 4 | Dátum posledného príjmu |
| LastODate | DateType | 4 | Dátum posledného výdaja |
| LastIQnt | double | 8 | Posledné množstvo príjmu |
| LastOQnt | double | 8 | Posledné množstvo výdaja |

### Štatistiky predaja

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ASaQnt | double | 8 | Predaj za aktuálny rok |
| AOuQnt | double | 8 | Výdaj za aktuálny rok |
| PSaQnt | double | 8 | Predaj za predošlý rok |
| POuQnt | double | 8 | Výdaj za predošlý rok |

### Stav a príznaky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DisFlag | byte | 1 | Vyradenie (1=vyradená karta) |
| Sended | byte | 1 | Príznak odoslania zmien (0/1) |
| Action | Str1 | 2 | Príznak cenovej akcie (A=akciový tovar) |
| LinPac | longint | 4 | Kód posledného dodávateľa |
| DefPos | Str15 | 16 | Hlavné pozičné miesto |
| OsdCode | Str15 | 16 | Objednávací kód tovaru |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (18)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | GsCode | GsCode | Duplicit |
| 1 | MgCode | MgCode | Duplicit |
| 2 | _GsName | GsName | Case-insensitive, Duplicit |
| 3 | BarCode | BarCode | Duplicit |
| 4 | StkCode | StkCode | Duplicit |
| 5 | ActQnt | ActQnt | Duplicit |
| 6 | ActVal | ActVal | Duplicit |
| 7 | MinMax | MinMax | Duplicit |
| 8 | AvgPrice | AvgPrice | Duplicit |
| 9 | LastPrice | LastPrice | Duplicit |
| 10 | LastIDate | LastIDate | Duplicit |
| 11 | LastODate | LastODate | Duplicit |
| 12 | Sended | Sended | Duplicit |
| 13 | Action | Action | Duplicit |
| 14 | LinPac | LinPac | Duplicit |
| 15 | _GaName | GaName | Case-insensitive, Duplicit |
| 16 | MgCode, StkCode | MgSc | Duplicit |
| 17 | OsdCode | OsdCode | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| GsCode | GSCAT.GsCode | Tovarová položka |
| MgCode | MGLST.MgCode | Tovarová skupina |
| FgCode | FGLST.FgCode | Finančná skupina |
| LinPac | PAB.PaCode | Posledný dodávateľ |

## Výpočtové vzťahy

```
ActQnt = BegQnt + InQnt - OutQnt
FreQnt = ActQnt - SalQnt - OcdQnt
ActVal = ActQnt * AvgPrice (aproximácia)
```

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
