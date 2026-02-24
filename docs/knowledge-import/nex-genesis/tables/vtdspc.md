# VTDSPC - Špecifikácie dokladov pre DPH

## Kľúčové slová / Aliases

VTDSPC, VTDSPC.BTR, špecifikácie, dokladov, pre, dph

## Popis

Číselník špecifikácií dokladov z hľadiska DPH. Definuje pravidlá pre zaradenie dokladov do príslušných riadkov daňového priznania a podporu samozdanenia.

## Btrieve súbor

`VTDSPC.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\VTDSPC.BTR`

## Štruktúra polí (12 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VtdSpc | word | 2 | Kód špecifikácie dokladu - **PRIMARY KEY** |
| Describe | Str60 | 61 | Popis špecifikácie |

### Samozdanenie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SvtClc | byte | 1 | Samozdanenie (1=zapnuté) |
| SvtGrp | byte | 1 | Skupina DPH pre samozdanenie |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | VtdSpc | VtdSpc | Duplicit |

## Typické špecifikácie

| Kód | Popis | Samozdanenie |
|-----|-------|--------------|
| 0 | Štandardný doklad | Nie |
| 1 | Nadobudnutie tovaru z EÚ | Áno |
| 2 | Prijatie služby z EÚ | Áno |
| 3 | Tuzemské samozdanenie | Áno |
| 4 | Dovoz tovaru | Nie |
| 5 | Oslobodené plnenie | Nie |

## Samozdanenie (SvtClc)

Pri samozdanení systém automaticky:
1. Vytvára DPH na vstupe (odpočet)
2. Vytvára DPH na výstupe (povinnosť)
3. Používa skupinu DPH definovanú v SvtGrp

## Použitie

- Klasifikácia dokladov pre daňové priznanie
- Automatické samozdanenie pri EÚ obchodoch
- Správne zaradenie do riadkov výkazov

## Business pravidlá

- VtdSpc sa nastavuje na doklade (ISH, ICH)
- SvtClc=1 aktivuje mechanizmus samozdanenia
- SvtGrp určuje sadzbu DPH pre samozdanenie
- Používa sa v module VTR pre výpočet daňového priznania

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
