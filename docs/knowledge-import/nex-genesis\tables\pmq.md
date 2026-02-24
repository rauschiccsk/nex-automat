# PMQ - História prevodných príkazov

## Kľúčové slová / Aliases

PMQ, PMQ.BTR, cenové ponuky hlavičky, price quotes header, ponuky, árajánlatok

## Popis

Tabuľka histórie prevodných príkazov pre úhradu faktúr. Sleduje vystavené platobné príkazy a ich pripojenie k faktúram.

## Btrieve súbor

`PMQyyyy.BTR` (yyyy=rok)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\PMQyyyy.BTR`

## Polia (13)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo prevodného príkazu |
| ItmNum | word | 2 | Poradové číslo riadku |
| PayDate | DateType | 4 | Dátum vystavenia príkazu |
| ConDoc | Str12 | 13 | Číslo faktúry na úhradu |
| ConExt | Str12 | 13 | Variabilný symbol faktúry |
| DvzName | Str3 | 4 | Účtovná mena |
| PayVal | double | 8 | Hodnota úhrady |
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |

## Indexy (4)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum | DoIt | Duplicit (Composite PK) |
| 1 | PayDate | PayDate | Duplicit |
| 2 | ConDoc | ConDoc | Case-insensitive, Duplicit |
| 3 | ConExt | ConExt | Case-insensitive, Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| ConDoc | ISH.DocNum | Dodávateľská faktúra |

## Workflow

```
1. Výber faktúr na úhradu
   ↓
2. Generovanie prevodného príkazu
   ↓
3. Zápis do PMQ
   ↓
4. Aktualizácia ISH.PmqDate
   ↓
5. Export do banky (SEPA XML, ABO formát)
   ↓
6. Po potvrdení úhrady → PMI
```

## Rozdiel PMQ vs PMI

| Aspekt | PMQ | PMI |
|--------|-----|-----|
| Účel | Príkaz na úhradu | Realizovaná úhrada |
| Stav | Plánovaná platba | Skutočná platba |
| Zdroj | Generované systémom | Bankový výpis |
| Multi-mena | Jedna mena | Tri meny |

## Použitie

- Evidencia vystavených prevodných príkazov
- Kontrola plánovaných úhrad
- Export do bankových systémov
- Párovanie s bankovými výpismi

## Business pravidlá

- Jeden prevodný príkaz môže obsahovať viac faktúr
- DocNum = číslo príkazu (generované)
- PayDate = požadovaný dátum úhrady
- ConExt = variabilný symbol pre identifikáciu

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
