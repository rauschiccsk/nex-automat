# PACNTC - Kontaktné osoby partnerov

## Kľúčové slová / Aliases

PACNTC, PACNTC.BTR, kontaktné osoby, contact persons, kontakty, kapcsolattartók

## Popis

Tabuľka kontaktných osôb obchodných partnerov. Obsahuje osobné údaje, kontakty a doklady totožnosti. Používa sa aj pre hotelový systém (HRS) na evidenciu hostí.

## Btrieve súbor

`PACNCT.BTR`

## Umiestnenie

`C:\NEX\YEARACT\FIRMS\PACNCT.BTR`

## Polia

### Základné údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Kód firmy - **FK → PAB** |
| PaName | Str30 | 31 | Názov firmy (cache) |
| _PaName | Str30 | 31 | Vyhľadávacie pole názvu firmy |

### Osobné údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| TitulBef | Str10 | 11 | Titul pred menom |
| FirstName | Str15 | 16 | Krstné meno |
| MidName | Str15 | 16 | Druhé krstné meno |
| LastName | Str15 | 16 | Priezvisko |
| FullName | Str30 | 31 | Celé meno |
| _FullName | Str30 | 31 | Vyhľadávacie pole mena |
| TitulAft | Str10 | 11 | Titul za menom |
| Function | Str30 | 31 | Funkcia/pozícia |
| SexMark | Str1 | 2 | Pohlavie (M=muž, W=žena) |
| Accost | Str30 | 31 | Oslovenie |

### Pracovné kontakty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WorkTel | Str20 | 21 | Pracovný telefón |
| WorkSec | Str5 | 6 | Telefónna klapka |
| WorkFax | Str20 | 21 | Pracovný fax |
| WorkEml | Str30 | 31 | Pracovný email |

### Súkromné kontakty

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| MobTel | Str20 | 21 | Mobilný telefón |
| PrivTel | Str20 | 21 | Súkromný telefón |
| PrivFax | Str20 | 21 | Súkromný fax |
| PrivEml | Str30 | 31 | Súkromný email |

### Adresa trvalého pobytu (Rsd*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RsdAddr | Str60 | 61 | Ulica a číslo |
| RsdCtc | Str3 | 4 | Kód mesta |
| RsdCtn | Str30 | 31 | Názov mesta |
| RsdZip | Str6 | 7 | PSČ |
| RsdStc | Str2 | 3 | Kód štátu |
| RsdStn | Str30 | 31 | Názov štátu |

### Doklady totožnosti (pre HRS)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| IdnType | Str1 | 2 | Typ dokladu (0=OP, 1=PAS) |
| IdnCard | Str30 | 31 | Číslo dokladu |
| BrtDate | DateType | 4 | Dátum narodenia |
| BrtPlac | Str30 | 31 | Miesto narodenia |
| Citizen | Str30 | 31 | Štátna príslušnosť |

### HRS (Hotelový systém)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VisNum | longint | 4 | Poradové číslo hosťa |
| VisType | Str1 | 2 | Typ hosťa (0=bežný, 1=VIP, 2=nežiaduci) |

### Ostatné

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Notice | Str30 | 31 | Poznámka |
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Poradové číslo modifikácie |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (7)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | PaCode | PaCode | Duplicit |
| 1 | _PaName | PaName | Duplicit |
| 2 | _FullName | FullName | Duplicit |
| 3 | WorkTel | WorkTel | Duplicit |
| 4 | PrivTel | PrivTel | Duplicit |
| 5 | MobTel | MobTel | Duplicit |
| 6 | VisNum | VisNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PaCode | PAB.PaCode | Partner |
| RsdStc | STALST.StaCode | Štát trvalého pobytu |
| RsdCtc | CTYLST.CtyCode | Mesto trvalého pobytu |

## Business pravidlá

- Partner môže mať viac kontaktných osôb
- FullName sa automaticky skladá z FirstName + LastName
- _FullName a _PaName sú uppercase pre case-insensitive vyhľadávanie
- Pre HRS systém: VisType=2 označuje nežiaduceho hosťa

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
