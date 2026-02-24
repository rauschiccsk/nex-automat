# TPC - Terminované ceny

## Kľúčové slová / Aliases

TPC, TPC.BTR, terminované, ceny

## Popis

Tabuľka položiek terminovaných (plánovaných) cien. Obsahuje budúce zmeny predajných cien s presným dátumom a časom platnosti. Každá kniha terminovaných cien má vlastný súbor.

## Btrieve súbor

`TPCnnnnn.BTR` (nnnnn=číslo knihy z BOKLST)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\TPCnnnnn.BTR`

## Štruktúra polí (21 polí)

### Identifikácia tovaru

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo (PLU) - **FK GSCAT** |
| GsName | Str30 | 31 | Názov tovaru |
| _GsName | Str20 | 21 | Vyhľadávacie pole názvu tovaru |
| BarCode | Str15 | 16 | Prvotný identifikačný kód tovaru (EAN) |

### Časové obdobie platnosti

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BegDate | DateType | 4 | Dátum začiatku platnosti ceny |
| BegTime | TimeType | 4 | Čas začiatku platnosti ceny |
| EndDate | DateType | 4 | Dátum ukončenia platnosti ceny |
| EndTime | TimeType | 4 | Čas ukončenia platnosti ceny |

### Cenové údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc | byte | 1 | Sadzba DPH v % |
| APrice | double | 8 | Terminovaná predajná cena bez DPH |
| BPrice | double | 8 | Terminovaná predajná cena s DPH |

### Stav a synchronizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SndNum | word | 2 | Číslo odoslania do pokladní |
| Status | Str1 | 2 | Stav položky (prázdne=aktívne, D=zrušené) |

### Audit - vytvorenie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |

### Audit - zmena

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

### Audit - zrušenie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DelUser | Str8 | 9 | Používateľ zrušenia |
| DelDate | DateType | 4 | Dátum zrušenia |
| DelTime | TimeType | 4 | Čas zrušenia |

## Indexy (5)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | GsCode | GsCode | Duplicit |
| 1 | _GsName | GsName | Duplicit, Case-insensitive |
| 2 | BarCode | BarCode | Duplicit, Case-insensitive |
| 3 | SndNum | SndNum | Duplicit |
| 4 | Status | Status | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| GsCode | GSCAT.GsCode | Katalógová karta produktu |
| BarCode | BARCODE.BarCode | Čiarový kód |

## Výpočtové pravidlá

### Cena bez DPH

```
APrice = BPrice / (1 + VatPrc / 100)
```

### Platnosť ceny

```
Cena je platná ak: BegDate ≤ aktuálny_dátum ≤ EndDate
                   AND BegTime ≤ aktuálny_čas ≤ EndTime
```

## Status položky

| Hodnota | Význam | Popis |
|---------|--------|-------|
| (prázdny) | Aktívna | Terminovaná cena čaká na aktiváciu |
| D | Zrušená | Položka bola zrušená používateľom |

## Použitie

- Plánovanie budúcich zmien predajných cien
- Príprava cenových zmien pred ich aktiváciou
- Synchronizácia plánovaných cien do pokladní
- Evidencia histórie cenových zmien

## Business pravidlá

- GsCode, GsName, BarCode, VatPrc sa načítavajú z PLS pri vytvorení
- BPrice zadáva používateľ, APrice sa vypočíta automaticky
- Položka so Status='D' nie je editovateľná
- Pri zrušení sa vyplnia DelUser, DelDate, DelTime
- Export prebieha iba pre aktívne položky (Status='')

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
