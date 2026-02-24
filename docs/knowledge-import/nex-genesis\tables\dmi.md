# DMI - Položky dokladov rozobrania

## Kľúčové slová / Aliases

DMI, DMI.BTR, položky, dokladov, rozobrania

## Popis

Tabuľka položiek dokladov rozobrania. Obsahuje zoznam komponentov, ktoré vzniknú rozobraním výrobku. Každá kniha má vlastný súbor.

## Btrieve súbor

`DMIyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\DMIyynnn.BTR`

## Štruktúra polí (28 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo dokladu - **FK DMH** |
| ItmNum | word | 2 | Poradové číslo položky |
| DocDate | DateType | 4 | Dátum dokladu |

### Sklad a pohyb

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkNum | word | 2 | Číslo skladu príjmu - **FK STKLST** |
| SmCode | word | 2 | Číslo skladového pohybu - **FK SMLST** |

### Komponent

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| MgCode | word | 2 | Číslo tovarovej skupiny - **FK MGLST** |
| GsCode | longint | 4 | Tovarové číslo komponentu - **FK GSCAT** |
| GsName | Str30 | 31 | Názov komponentu |
| BarCode | Str15 | 16 | Identifikačný kód (EAN) |
| StkCode | Str15 | 16 | Skladový kód tovaru |
| MsName | Str10 | 11 | Merná jednotka |
| Notice | Str30 | 31 | Poznámka k položke |

### Množstvo a ceny

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsQnt | double | 8 | Prijaté množstvo komponentu |
| VatPrc | byte | 1 | Sadzba DPH v % |
| CPrice | double | 8 | Nákupná cena/MJ bez DPH |
| BPrice | double | 8 | Predajná cena/MJ s DPH |
| CValue | double | 8 | Hodnota položky v NC bez DPH |
| RndVal | double | 8 | Hodnota cenového zaokrúhlenia |

### Väzby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OcdNum | Str12 | 13 | Číslo zákazkového dokladu |

### Stav

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkStat | Str1 | 2 | Stav položky (N=zaevidované, S=naskladnené) |
| ClcStat | Str1 | 2 | Výpočet ceny (*=označený na výpočet) |

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

## Indexy (5)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum | DoIt | Unikátny |
| 1 | GsCode | GsCode | Duplicit |
| 2 | StkStat | StkStat | Duplicit, Case-insensitive |
| 3 | SmCode | SmCode | Duplicit |
| 4 | DocNum | DocNum | Duplicit |

## Stavy položky (StkStat)

| Hodnota | Farba | Popis |
|---------|-------|-------|
| N | Červená | Zaevidované - komponent ešte nie je prijatý na sklad |
| S | Čierna | Naskladnené - komponent prijatý na sklad |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | DMH.DocNum | Hlavička dokladu |
| GsCode | GSCAT.GsCode | Katalógová karta komponentu |
| StkNum | STKLST.StkNum | Sklad príjmu |
| SmCode | SMLST.SmCode | Typ skladového pohybu |
| MgCode | MGLST.MgCode | Tovarová skupina |

## Použitie

- Evidencia komponentov získaných rozobraním výrobku
- Podklad pre skladové príjmy
- Sledovanie stavu naskladnenia jednotlivých komponentov
- Výpočet cien komponentov z ceny výrobku

## Business pravidlá

- GsQnt = množstvo komponentu na celkové množstvo rozoberaného výrobku
- CValue = CPrice × GsQnt + RndVal
- Po príjme na sklad sa StkStat zmení na 'S'
- ClcStat='*' označuje položku na automatický výpočet ceny

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
