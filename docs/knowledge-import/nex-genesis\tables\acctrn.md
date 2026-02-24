# ACCTRN - Obratová predvaha analytických účtov

## Kľúčové slová / Aliases

ACCTRN, ACCTRN.BTR, obratová, predvaha, analytických, účtov

## Popis

Obratová predvaha analytických účtov s mesačnými obratmi. Tabuľka sa generuje prepočtom z denníka účtovných zápisov (JOURNAL) a obsahuje počiatočné stavy, mesačné obraty a konečné stavy pre každý analytický účet.

## Btrieve súbor

`ACCTRN.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ACCTRN.BTR`

## Štruktúra polí (43 polí)

### Identifikácia účtu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AccSnt | Str3 | 4 | Syntetický účet - **PK časť 1** |
| AccAnl | Str6 | 7 | Analytický účet - **PK časť 2** |
| AnlName | Str30 | 31 | Názov analytického účtu |
| _AnlName | Str30 | 31 | Vyhľadávacie pole názvu |

### Počiatočné stavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CBegVal | double | 8 | Počiatočný stav - MD (Má dať) |
| DBegVal | double | 8 | Počiatočný stav - Dal |

### Mesačné obraty - MD (Má dať)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CTrnVal01 | double | 8 | Obrat za mesiac 01 - MD |
| CTrnVal02 | double | 8 | Obrat za mesiac 02 - MD |
| CTrnVal03 | double | 8 | Obrat za mesiac 03 - MD |
| CTrnVal04 | double | 8 | Obrat za mesiac 04 - MD |
| CTrnVal05 | double | 8 | Obrat za mesiac 05 - MD |
| CTrnVal06 | double | 8 | Obrat za mesiac 06 - MD |
| CTrnVal07 | double | 8 | Obrat za mesiac 07 - MD |
| CTrnVal08 | double | 8 | Obrat za mesiac 08 - MD |
| CTrnVal09 | double | 8 | Obrat za mesiac 09 - MD |
| CTrnVal10 | double | 8 | Obrat za mesiac 10 - MD |
| CTrnVal11 | double | 8 | Obrat za mesiac 11 - MD |
| CTrnVal12 | double | 8 | Obrat za mesiac 12 - MD |

### Mesačné obraty - Dal

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DTrnVal01 | double | 8 | Obrat za mesiac 01 - Dal |
| DTrnVal02 | double | 8 | Obrat za mesiac 02 - Dal |
| DTrnVal03 | double | 8 | Obrat za mesiac 03 - Dal |
| DTrnVal04 | double | 8 | Obrat za mesiac 04 - Dal |
| DTrnVal05 | double | 8 | Obrat za mesiac 05 - Dal |
| DTrnVal06 | double | 8 | Obrat za mesiac 06 - Dal |
| DTrnVal07 | double | 8 | Obrat za mesiac 07 - Dal |
| DTrnVal08 | double | 8 | Obrat za mesiac 08 - Dal |
| DTrnVal09 | double | 8 | Obrat za mesiac 09 - Dal |
| DTrnVal10 | double | 8 | Obrat za mesiac 10 - Dal |
| DTrnVal11 | double | 8 | Obrat za mesiac 11 - Dal |
| DTrnVal12 | double | 8 | Obrat za mesiac 12 - Dal |

### Celkové obraty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CTrnVal | double | 8 | Celkový obrat - MD |
| DTrnVal | double | 8 | Celkový obrat - Dal |

### Konečné stavy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CEndVal | double | 8 | Konečný stav - MD |
| DEndVal | double | 8 | Konečný stav - Dal |
| DifVal | double | 8 | Rozdiel (CEndVal - DEndVal) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtName | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

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

### Celkový obrat
```
CTrnVal = SUM(CTrnVal01..CTrnVal12)
DTrnVal = SUM(DTrnVal01..DTrnVal12)
```

### Konečný stav
```
CEndVal = CBegVal + CTrnVal
DEndVal = DBegVal + DTrnVal
```

### Rozdiel
```
DifVal = CEndVal - DEndVal
```

### Bilančná rovnováha
Pre správne účtovníctvo musí platiť:
```
SUM(všetky účty: CBegVal) = SUM(všetky účty: DBegVal)
SUM(všetky účty: CTrnVal) = SUM(všetky účty: DTrnVal)
SUM(všetky účty: CEndVal) = SUM(všetky účty: DEndVal)
```

## Interpretácia DifVal

| DifVal | Typ účtu | Význam |
|--------|----------|--------|
| > 0 | Aktívny (A) | Zostatok na strane MD |
| < 0 | Pasívny (P) | Zostatok na strane D |
| = 0 | - | Vyrovnaný účet |

## Generovanie (Acc_ReCalc_F)

Tabuľka sa generuje prepočtom z JOURNAL:

```
1. TRUNCATE ACCTRN
2. FOR EACH (AccSnt, AccAnl) IN JOURNAL:
   a. PS: zápisy s BegRec=1 → CBegVal, DBegVal
   b. Obraty: zápisy s BegRec<>1,9 → CTrnVal[mth], DTrnVal[mth]
   c. INSERT INTO ACCTRN
3. CALCULATE: CTrnVal, DTrnVal, CEndVal, DEndVal, DifVal
```

## Použitie

- Zobrazenie obratovej predvahy
- Tlač účtovných výkazov
- Kontrola bilančnej rovnováhy
- Analýza účtov podľa mesiacov

## Business pravidlá

- Generovaná tabuľka (nie primárne dáta)
- Zdroj: JOURNAL účtovný denník
- AnlName sa preberá z ACCANL
- BegRec=9 zápisy (uzatvorenie) sa ignorujú
- Mazanie možné len pri nulových hodnotách

## Porovnanie s ACCANL

| Vlastnosť | ACCTRN | ACCANL |
|-----------|--------|--------|
| Zdroj | Prepočítaný | Primárny |
| Mesačné obraty | Áno (01-12) | Áno (Turn01-12) |
| Stredisko | Nie | Nie (viď ACCANLC) |
| Počiatočný stav | CBegVal, DBegVal | Beg* polia |
| Účel | Reporting | Evidencia |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
