# PMI - Denník úhrad faktúr

## Kľúčové slová / Aliases

PMI, PMI.BTR, cenové ponuky položky, price quotes items, ponukové položky

## Popis

Denník úhrad dodávateľských a odberateľských faktúr. Obsahuje záznamy o jednotlivých úhradách s multi-menovými hodnotami.

## Btrieve súbor

`PMIyyyy.BTR` (yyyy=rok)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\PMIyyyy.BTR`

## Polia (27)

### Identifikácia úhrady

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo dokladu úhrady |
| ItmNum | word | 2 | Poradové číslo položky úhrady |
| ExtNum | Str12 | 13 | Variabilný symbol |
| PayDate | DateType | 4 | Dátum úhrady |
| Status | Str1 | 2 | Stav zápisu (D=zrušený) |

### Partner

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaName | Str30 | 31 | Názov firmy |
| _PaName | Str30 | 31 | Vyhľadávacie pole |
| PaCode | longint | 4 | Kód partnera |
| WriNum | word | 2 | Číslo prevádzky |

### Párovaná faktúra

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ConDoc | Str12 | 13 | Číslo uhradenej faktúry |

### Hodnoty v účtovnej mene

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| AcDvzName | Str3 | 4 | Účtovná mena (EUR) |
| AcPayVal | double | 8 | Hodnota úhrady v účtovnej mene |
| AcCrdVal | double | 8 | Kurzový rozdiel v účtovnej mene |

### Hodnoty v mene úhrady

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PyDvzName | Str3 | 4 | Mena úhrady |
| PyCourse | double | 8 | Kurz meny úhrady |
| PyPayVal | double | 8 | Hodnota úhrady v mene úhrady |
| PyPdfVal | double | 8 | Rozdiel úhrady v mene úhrady |

### Hodnoty v mene faktúry

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FgDvzName | Str3 | 4 | Mena faktúry |
| FgCourse | double | 8 | Kurz meny faktúry |
| FgPayVal | double | 8 | Hodnota úhrady v mene faktúry |
| FgPdfVal | double | 8 | Rozdiel úhrady v mene faktúry |

### Synchronizácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Sended | byte | 1 | Príznak odoslania (0=zmenený, 1=odoslaný) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |

## Indexy (10)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum, Status | DoItSt | Duplicit |
| 1 | PayDate | PayDate | Duplicit |
| 2 | _PaName | PaName | Duplicit |
| 3 | ExtNum | ExtNum | Case-insensitive, Duplicit |
| 4 | PyPayVal | PyPayVal | Duplicit |
| 5 | ConDoc | ConDoc | Case-insensitive, Duplicit |
| 6 | DocNum, ConDoc | DoCo | Case-insensitive, Duplicit |
| 7 | DocNum, ItmNum, ConDoc | DoItCd | Duplicit |
| 8 | Sended | Sended | Case-insensitive, Duplicit |
| 9 | DocNum | DocNum | Case-insensitive, Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| ConDoc | ISH.DocNum | Dodávateľská faktúra |
| ConDoc | ICH.DocNum | Odberateľská faktúra |
| PaCode | PAB.PaCode | Partner |

## Multi-mena architektúra

Úhrada môže prebiehať v troch rôznych menách:
1. **Účtovná mena (Ac*)** - EUR - mena účtovníctva
2. **Mena úhrady (Py*)** - mena, v ktorej sa platba uskutočnila
3. **Mena faktúry (Fg*)** - mena, v ktorej bola faktúra vystavená

## Workflow

```
1. Výber faktúry na úhradu
   ↓
2. Zadanie úhrady (plná/čiastočná)
   ↓
3. Vytvorenie záznamu PMI
   ↓
4. Aktualizácia zostatku faktúry
   ↓
5. Účtovanie úhrady
```

## Business pravidlá

- Jedna faktúra môže mať viac úhrad (čiastočné platby)
- Status = 'D' označuje zrušenú úhradu
- AcCrdVal obsahuje kurzový rozdiel pri rôznych kurzoch
- DocNum = číslo dokladu úhrady (napr. bankový výpis)

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
