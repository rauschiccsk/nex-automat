# CAPADV - Rozpis pokladničných platidiel

## Kľúčové slová / Aliases

CAPADV, CAPADV.BTR, rozpis, pokladničných, platidiel

## Popis

Tabuľka rozpisu platobných prostriedkov. Používa sa pre detailnú evidenciu stravovacích lístkov podľa emitenta a cudzích mien podľa typu. Globálny súbor.

## Btrieve súbor

`CAPADV.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DATA\CAPADV.BTR`

## Štruktúra polí (11 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PayNum | byte | 1 | Kód platidla (napr. 2=stravovacie lístky) |
| AdvName | Str10 | 11 | Typové označenie (DOXX, SODEXO, ...) |
| PayName | Str30 | 31 | Názov platobného prostriedku |

### Hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| IncVal | double | 8 | Prijaté množstvo (počet lístkov) |
| ChgCrs | double | 8 | Nominálna hodnota / prevodový kurz |
| PayVal | double | 8 | Zaplatená čiastka = IncVal × ChgCrs |

### Merné jednotky

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| IncMsu | Str10 | 11 | MJ prijatého množstva (ks, EUR, ...) |
| ChgMsu | Str10 | 11 | MJ prevodového kurzu |
| PayMsu | Str10 | 11 | MJ zaplatenej čiastky |

## Indexy (2)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | PayNum | PayNum | Duplicit |
| 1 | PayNum, AdvName | PnAn | Duplicit |

## Príklady použitia

### Stravovacie lístky

```
PayNum  = 2 (Stravovacie lístky)
─────────────────────────────────────────────────────────────────
AdvName = "DOXX"
PayName = "DOXX stravovacie lístky"
IncVal  = 15 (počet lístkov)
ChgCrs  = 5.00 (nominálna hodnota)
PayVal  = 75.00 EUR
IncMsu  = "ks"
ChgMsu  = "EUR/ks"
PayMsu  = "EUR"
─────────────────────────────────────────────────────────────────
AdvName = "SODEXO"
PayName = "Sodexo Gastro Pass"
IncVal  = 8
ChgCrs  = 4.50
PayVal  = 36.00 EUR
```

### Cudzia mena

```
PayNum  = 6 (Cudzia mena)
─────────────────────────────────────────────────────────────────
AdvName = "CZK"
PayName = "České koruny"
IncVal  = 500.00 (prijaté CZK)
ChgCrs  = 0.04 (kurz EUR/CZK)
PayVal  = 20.00 EUR
IncMsu  = "CZK"
ChgMsu  = "EUR/CZK"
PayMsu  = "EUR"
```

## Výpočet

```
PayVal = IncVal × ChgCrs

Príklad:
  15 lístkov × 5.00 EUR/lístok = 75.00 EUR
```

## Použitie

- Detailná evidencia stravovacích lístkov podľa emitenta
- Sledovanie cudzích mien
- Prepočet na EUR podľa kurzu/nominálnej hodnoty
- Reporting pre emitentov lístkov

## Business pravidlá

- PayNum odkazuje na CAPDEF.PayNum
- AdvName = skratka typu (DOXX, SODEXO, CHEQUE DEJEUNER, ...)
- Pre stravovacie lístky: IncVal = počet, ChgCrs = nominálna hodnota
- Pre cudzie meny: IncVal = čiastka v mene, ChgCrs = kurz

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
