# ACT - Položky výkazu obratovej predvahy

## Kľúčové slová / Aliases

ACT, ACT.BTR, položky, výkazu, obratovej, predvahy

## Popis

Tabuľka položiek archívneho výkazu obratovej predvahy. Obsahuje súhrnné stavy a obraty pre každý analytický účet za definované obdobie. Každý výkaz má vlastný súbor ACTnnnnn.BTR kde nnnnn je SerNum z ACTLST.

## Btrieve súbor

`ACTnnnnn.BTR` (nnnnn = SerNum z ACTLST)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ACTnnnnn.BTR`

## Štruktúra polí (20 polí)

### Identifikácia účtu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AccSnt | Str3 | 4 | Syntetický účet - **PK časť 1** |
| AccAnl | Str6 | 7 | Analytický účet - **PK časť 2** |
| AnlName | Str30 | 31 | Názov analytického účtu |
| _AnlName | Str30 | 31 | Vyhľadávacie pole názvu (case-insensitive) |

### Počiatočné stavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CBegVal | double | 8 | Počiatočný stav - MD (Má dať) |
| DBegVal | double | 8 | Počiatočný stav - Dal |

### Kumulatív pred obdobím

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CPrvVal | double | 8 | Kumulatívny obrat do obdobia - MD |
| DPrvVal | double | 8 | Kumulatívny obrat do obdobia - Dal |

### Obraty za obdobie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CTrnVal | double | 8 | Celkový obrat za obdobie - MD |
| DTrnVal | double | 8 | Celkový obrat za obdobie - Dal |

### Kumulatív ku koncu obdobia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CSumVal | double | 8 | Kumulatívny obrat ku koncu obdobia - MD |
| DSumVal | double | 8 | Kumulatívny obrat ku koncu obdobia - Dal |

### Konečné stavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CEndVal | double | 8 | Konečný stav - MD |
| DEndVal | double | 8 | Konečný stav - Dal |
| DifVal | double | 8 | Zostatok na účte (CEndVal - DEndVal) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtName | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |

## Indexy (3)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | AccSnt, AccAnl | SnAn | Duplicit |
| 1 | _AnlName | AnlName | Duplicit, Case-insensitive |
| 2 | DifVal | DifVal | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| AccSnt | ACCSNT.AccSnt | Syntetický účet |
| AccSnt + AccAnl | ACCANL.AccSnt + AccAnl | Analytický účet |

## Výpočtové pravidlá

### Kumulatív ku koncu obdobia

```
CSumVal = CPrvVal + CTrnVal
DSumVal = DPrvVal + DTrnVal
```

### Konečný stav

```
CEndVal = CBegVal + CSumVal
DEndVal = DBegVal + DSumVal
```

### Zostatok

```
DifVal = CEndVal - DEndVal
```

## Interpretácia DifVal

| DifVal | Typ účtu | Význam |
|--------|----------|--------|
| > 0 | Aktívny (A) | Zostatok na strane MD |
| < 0 | Pasívny (P) | Zostatok na strane D |
| = 0 | - | Vyrovnaný účet |

## Algoritmus generovania (JrnCollect)

Položky výkazu sa generujú z JOURNAL takto:

```
Pre každý účet (AccSnt + AccAnl) v JOURNAL:
  1. BegRec=1 → CBegVal, DBegVal (počiatočný stav)
  2. DocDate < BegDate → CPrvVal, DPrvVal (predchádzajúce obdobie)
  3. BegDate <= DocDate <= EndDate → CTrnVal, DTrnVal (aktuálne obdobie)
  4. BegRec=9 sa ignoruje (uzatvorenie)

Filtrovanie:
  - WriNum musí byť v zozname WriNums (LongInInt funkcia)

Po generovaní:
  - NulItmDel odstráni položky kde:
    Abs(CBegVal) + Abs(DBegVal) + Abs(CSumVal) + Abs(DSumVal) = 0
```

## Rozdiel oproti ACCTRN

| Vlastnosť | ACT | ACCTRN |
|-----------|-----|--------|
| Mesačné obraty | Nie | Áno (CTrnVal01-12) |
| Predchádzajúce obdobie | CPrvVal/DPrvVal | Nie |
| Kumulatív ku koncu | CSumVal/DSumVal | Vypočítané |
| Počet súborov | Viac (archív) | Jeden (operatívny) |
| Regenerácia | Nie (trvalý) | Áno (prepočet) |
| Filter obdobia | BegDate/EndDate | Celý rok |

## Bilančná rovnováha

Pre správne účtovníctvo musí v každom výkaze platiť:

```
SUM(CBegVal) = SUM(DBegVal)  // Počiatočné stavy
SUM(CTrnVal) = SUM(DTrnVal)  // Obraty za obdobie
SUM(CEndVal) = SUM(DEndVal)  // Konečné stavy
```

## Použitie

- Archivácia výkazov obratovej predvahy
- Tlač historických výkazov
- Porovnávanie období
- Audit účtovných stavov

## Business pravidlá

- Každý výkaz má vlastný súbor (nie prepis)
- Nulové položky sa automaticky vymažú
- Názov účtu (AnlName) sa preberá z ACCANL
- Súbor sa vymaže pri zmazaní záznamu z ACTLST

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
