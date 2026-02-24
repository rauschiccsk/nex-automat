# BARCODE - Druhotné identifikačné kódy

## Kľúčové slová / Aliases

BARCODE, BARCODE.BTR, čiarové kódy, EAN, barcodes, vonalkód, štítky, labels

## Popis
Tabuľka druhotných čiarových kódov. Každý tovar môže mať viacero čiarových kódov (EAN, Code128, interné, atď.). Prvotný kód je v GSCAT.BarCode, druhotné sú tu.

## Btrieve súbor
`BARCODE.BTR`

## Umiestnenie
`C:\NEX\YEARACT\STORES\BARCODE.BTR`

## Veľkosť záznamu
~50 bytes

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo (PLU) - **FK → GSCAT** |
| BarCode | Str15 | 16 | Druhotný identifikačný kód tovaru |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | GsCode | GsCode | Duplicit |
| 1 | BarCode | BarCode | Duplicit |
| 2 | GsCode, BarCode | GsBc | Unique (composite) |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| GsCode | GSCAT.GsCode | Tovarová položka |

## Business pravidlá

- Jeden tovar môže mať **viacero** druhotných kódov
- Kombinácia (GsCode + BarCode) musí byť **unikátna**
- BarCode môže byť **duplicitný** medzi rôznymi tovarmi (index 1 povoľuje duplicity)

## Použitie

Vyhľadanie tovaru podľa čiarového kódu:
1. Najprv hľadať v GSCAT.BarCode (prvotný kód)
2. Ak nenájdené, hľadať v BARCODE.BarCode (druhotné kódy)

## Stav migrácie

- [x] Model vytvorený (`packages/nexdata/nexdata/models/barcode.py`)
- [x] Kamenický dekódovanie
- [ ] PostgreSQL model
- [ ] API endpoint
