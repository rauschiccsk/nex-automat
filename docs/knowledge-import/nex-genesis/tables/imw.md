# IMW - Váhové balíčky interných príjemok

## Kľúčové slová / Aliases

IMW, IMW.BTR, váhové, balíčky, interných, príjemok

## Popis

Tabuľka položkovitého zoznamu váhových balíčkov pri príjme váhového tovaru. Používa sa pre tovar s premenlivou hmotnosťou (mäso, zelenina, atď.).

## Btrieve súbor

`IMWnnnnn.BTR` (nnnnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\IMWnnnnn.BTR`

## Štruktúra polí (14 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo príjemky - **FK → IMH.DocNum** |
| ItmNum | word | 2 | Poradové číslo položky |
| RowNum | word | 2 | Poradové číslo váhového balíčka |

### Tovar

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo (PLU) |
| GsName | Str30 | 31 | Názov tovaru |
| BaCode | Str15 | 16 | Identifikačný kód tovaru |
| MsName | Str10 | 11 | Merná jednotka |

### Hodnoty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsQnt | double | 8 | Prijaté množstvo (váha) |
| CPrice | double | 8 | Nákupná cena bez DPH |
| CValue | double | 8 | Hodnota v NC bez DPH |

### Šarže

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RbaCod | Str30 | 31 | Kód výrobnej šarže |
| RbaDat | DateType | 4 | Dátum výrobnej šarže |

## Indexy (3)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum | DocNum | Duplicit |
| 1 | DocNum, ItmNum | DoIt | Duplicit |
| 2 | DocNum, ItmNum, RowNum | DoItRn | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | IMH.DocNum | Hlavička príjemky |
| GsCode | GSCAT.GsCode | Tovar |

## Workflow

```
1. Príjem váhového tovaru na elektronickej váhe
   ↓
2. Váženie jednotlivých balíčkov
   ↓
3. Zápis do IMW (jeden riadok = jeden balíček)
   ↓
4. Sumarizácia do IMI (celkové množstvo)
   ↓
5. Tlač etikiet na balíčky
```

## Použitie

- Evidencia jednotlivých váhových balíčkov
- Sledovanie šarží pri váhovom tovare
- Tlač cenových etikiet
- Traceability potravinárskeho tovaru

## Business pravidlá

- Jeden riadok = jeden fyzický balíček
- GsQnt v IMI = suma GsQnt zo všetkých IMW pre danú položku
- Používa sa pre váhový tovar (mäso, syry, ovocie, zelenina)

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
