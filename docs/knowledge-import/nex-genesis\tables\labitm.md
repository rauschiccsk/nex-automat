# LABITM - Fronta tlače cenovkových etikiet

## Kľúčové slová / Aliases

LABITM, LABITM.BTR, fronta, tlače, cenovkových, etikiet

## Popis

Tabuľka fronty tlače cenovkových etikiet. Obsahuje položky čakajúce na tlač cenoviek s informáciami o produkte, cenách a množstve. Globálny súbor zdieľaný celým systémom.

## Btrieve súbor

`LABITM.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DATA\LABITM.BTR`

## Štruktúra polí (22 polí)

### Identifikácia tovaru

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo (PLU) - **FK GSCAT** |
| MgCode | word | 2 | Číslo tovarovej skupiny - **FK MGLST** |
| FgCode | word | 2 | Finančná skupina |
| GsName | Str30 | 31 | Názov tovaru |
| _GsName | Str30 | 31 | Vyhľadávacie pole názvu (uppercase) |
| BarCode | Str15 | 16 | Identifikačný kód tovaru (EAN) |
| StkCode | Str15 | 16 | Skladový kód tovaru |
| MsName | Str10 | 11 | Merná jednotka tovaru |

### Cenové údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc | double | 8 | Sadzba DPH v % |
| APrice | double | 8 | Predajná cena bez DPH |
| BPrice | double | 8 | Predajná cena s DPH |

### Množstvo

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsQnt | double | 8 | Prijaté/vydané množstvo (zdroj: TSI/IMI) |
| GscKfc | double | 8 | Prepočítavací koeficient |
| LabQnt | double | 8 | Počet etikiet na tlač |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (4)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | GsCode | GsCode | Duplicit |
| 1 | _GsName | GsName | Duplicit, Case-insensitive |
| 2 | BarCode | BarCode | Duplicit, Case-insensitive |
| 3 | StkCode | StkCode | Duplicit, Case-insensitive |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| GsCode | GSCAT.GsCode | Katalógová karta produktu |
| MgCode | MGLST.MgCode | Tovarová skupina |

## Použitie

- Perzistentná fronta položiek na tlač etikiet
- Naplnenie z príjemky (TSI) alebo výdajky (IMI)
- Naplnenie z filtra cenníka (PLS)
- Manuálne pridanie položiek
- LabQnt určuje počet etikiet pre každú položku

## Zdroje dát

| Zdroj | Popis |
|-------|-------|
| TSI | Položky dodávateľského dodacieho listu (príjem) |
| IMI | Položky internej výdajky/prevodu |
| PLS | Filter z cenníka (podľa zmeny cien) |
| Manual | Ručné pridanie produktu |

## Business pravidlá

- GsQnt sa preberá z dokladu (TSI.GsQnt alebo IMI.GsQnt)
- LabQnt = počet etikiet, možno upraviť pred tlačou
- Po tlači sa záznamy z fronty nemažú automaticky
- _GsName slúži na vyhľadávanie bez diakritiky

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
