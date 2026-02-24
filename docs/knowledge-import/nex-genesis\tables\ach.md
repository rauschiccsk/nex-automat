# ACH - Hlavičky precenovacích dokladov

## Kľúčové slová / Aliases

ACH, ACH.BTR, hlavičky, precenovacích, dokladov

## Popis

Tabuľka hlavičiek precenovacích dokladov pre akciové precenenie tovaru. Obsahuje základné údaje o doklade vrátane obdobia akcie, stavu a počtu položiek. Každá kniha akciových precenení má vlastný súbor.

## Btrieve súbor

`ACHyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ACHyynnn.BTR`

## Štruktúra polí (19 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SerNum | longint | 4 | Poradové číslo precenovacieho dokladu |
| DocNum | Str12 | 13 | Interné číslo precenovacieho dokladu |
| Year | Str2 | 3 | Rok dokladu |

### Obdobie akcie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BegDate | DateType | 4 | Dátum zahájenia cenovej akcie |
| EndDate | DateType | 4 | Dátum ukončenia cenovej akcie |

### Popis

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Describe | Str30 | 31 | Popis dokladu |
| _Describe | Str30 | 31 | Vyhľadávacie pole popisu |

### Štatistika

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ItmQnt | longint | 4 | Počet položiek dokladu |
| WaiItmQnt | longint | 4 | Rezervované |
| ChgItmQnt | longint | 4 | Rezervované |

### Stav a typ

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocType | Str1 | 2 | Typ dokladu (A=akciové, Z=zmena cien) |
| DstLck | byte | 1 | Príznak uzatvorenia (1=uzatvorený, 9=rezervovaný) |
| Status | Str1 | 2 | Stav dokladu (N=pripravený, A=akcia, X=ukončená) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (5)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | Year, SerNum | YearSerNum | Unikátny |
| 1 | DocNum | DocNum | Duplicit |
| 2 | BegDate | BegDate | Duplicit |
| 3 | EndDate | EndDate | Duplicit |
| 4 | _Describe | Describe | Duplicit, Case-insensitive |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | ACI.DocNum | Položky dokladu |

## Typy dokladu (DocType)

| Hodnota | Typ | Popis |
|---------|-----|-------|
| A | Akciové precenenie | S označením tovaru ako akciový |
| Z | Zmena predajných cien | Bez označenia ako akcia |

## Stavy dokladu (Status)

| Hodnota | Stav | Farba | Popis |
|---------|------|-------|-------|
| N | Pripravený | Zelená | Nový doklad, možno upravovať |
| A | Akcia | Červená | Prebieha cenová akcia |
| X | Ukončená | Čierna | Ukončená akcia (typ Z) |
| E | Ukončená | Čierna | Ukončená akcia (typ A) |

## Použitie

- Evidencia precenovacích dokladov
- Správa cenových akcií
- Sledovanie stavu akcií
- Plánovanie obdobia akcií

## Business pravidlá

- Doklad možno zmazať len ak Status='N'
- Pri zahájení akcie sa Status mení na 'A' alebo 'X'
- Pri ukončení akcie sa Status mení na 'E'
- ItmQnt sa aktualizuje procedúrou AchRecalc

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
