# DMH - Hlavičky dokladov rozobrania

## Kľúčové slová / Aliases

DMH, DMH.BTR, hlavičky, dokladov, rozobrania

## Popis

Tabuľka hlavičiek dokladov rozobrania výrobkov. Obsahuje informácie o rozoberanom výrobku, skladoch pre výdaj a príjem, partnerovi a stavoch spracovania. Každá kniha má vlastný súbor.

## Btrieve súbor

`DMHyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\DMHyynnn.BTR`

## Štruktúra polí (34 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SerNum | longint | 4 | Poradové číslo dokladu |
| DocNum | Str12 | 13 | Interné číslo dokladu |
| DocDate | DateType | 4 | Dátum vystavenia dokladu |
| Year | Str2 | 3 | Rok dokladu |

### Sklady a pohyby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OuStkNum | word | 2 | Číslo skladu výdaja (výrobok) - **FK STKLST** |
| InStkNum | word | 2 | Číslo skladu príjmu (komponenty) - **FK STKLST** |
| OuSmCode | word | 2 | Kód skladového pohybu výdaja - **FK SMLST** |
| InSmCode | word | 2 | Kód skladového pohybu príjmu - **FK SMLST** |

### Partner

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Kód firmy (zákazník/reklamácia) - **FK PAB** |
| PaName | Str30 | 31 | Názov firmy |
| _PaName | Str20 | 21 | Vyhľadávacie pole názvu firmy |

### Výrobok

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| MgCode | word | 2 | Číslo tovarovej skupiny - **FK MGLST** |
| GsCode | longint | 4 | Tovarové číslo rozoberaného výrobku - **FK GSCAT** |
| GsName | Str30 | 31 | Názov rozoberaného výrobku |
| _GsName | Str20 | 21 | Názov výrobku - vyhľadávacie pole |
| BarCode | Str15 | 16 | Identifikačný kód výrobku (EAN) |
| GsQnt | double | 8 | Množstvo rozoberaného výrobku |
| MsName | Str10 | 11 | Merná jednotka výrobku |

### Cenové údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| VatPrc | byte | 1 | Sadzba DPH v % |
| CPrice | double | 8 | NC/MJ bez DPH výrobku |
| BPrice | double | 8 | PC/MJ s DPH výrobku |
| CValue | double | 8 | Hodnota v NC bez DPH výrobku |
| ItmVal | double | 8 | Hodnota položiek v NC bez DPH |
| RndVal | double | 8 | Hodnota cenového zaokrúhlenia |

### Väzby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OcdNum | Str12 | 13 | Číslo zákazky - **FK OCH** |

### Stav

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ItmQnt | word | 2 | Počet položiek dokladu |
| PrnCnt | byte | 1 | Počet vytlačených kópií |
| DstStk | Str1 | 2 | Stav výrobku (N=pripravený, S=vyskladnený) |
| StkStat | Str1 | 2 | Stav komponentov (N=zaevidované, S=naskladnené) |
| DstLck | byte | 1 | Príznak uzatvorenia (1=uzatvorený) |
| Sended | byte | 1 | Príznak odoslania (0=zmenený, 1=odoslaný) |
| SndStat | Str1 | 2 | Stav internetového prenosu |

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

## Indexy (12)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | Year, SerNum | YearSerNum | Unikátny |
| 1 | DocNum | DocNum | Duplicit |
| 2 | DocDate | DocDate | Duplicit |
| 3 | OuSmCode | OuSmCode | Duplicit |
| 4 | InSmCode | InSmCode | Duplicit |
| 5 | PaCode | PaCode | Duplicit |
| 6 | _PaName | PaName | Duplicit |
| 7 | GsCode | GsCode | Duplicit |
| 8 | _GsName | GsName | Duplicit |
| 9 | CValue | CValue | Duplicit |
| 10 | OcdNum | OcdNum | Duplicit |
| 11 | Sended | Sended | Duplicit |

## Stavy dokladu

### DstStk - Stav výrobku

| Hodnota | Farba | Popis |
|---------|-------|-------|
| N | Červená | Pripravený - výrobok ešte nie je vydaný |
| S | Čierna | Vyskladnený - výrobok vydaný na rozobranie |

### StkStat - Stav komponentov

| Hodnota | Popis |
|---------|-------|
| N | Zaevidované - komponenty ešte nie sú prijaté |
| S | Naskladnené - komponenty prijaté na sklad |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| OuStkNum | STKLST.StkNum | Sklad výdaja výrobku |
| InStkNum | STKLST.StkNum | Sklad príjmu komponentov |
| OuSmCode | SMLST.SmCode | Typ pohybu výdaja |
| InSmCode | SMLST.SmCode | Typ pohybu príjmu |
| PaCode | PAB.PaCode | Partner (zákazník) |
| GsCode | GSCAT.GsCode | Katalógová karta výrobku |
| MgCode | MGLST.MgCode | Tovarová skupina |
| OcdNum | OCH.DocNum | Zákazkový doklad |
| DocNum | DMI.DocNum | Položky dokladu |
| DocNum | DMN.DocNum | Poznámky |

## Použitie

- Evidencia dokladov rozobrania výrobkov
- Sledovanie stavu spracovania (výdaj výrobku, príjem komponentov)
- Väzba na zákazkové doklady
- Podklad pre skladové pohyby

## Business pravidlá

- Najprv sa vydá výrobok (DstStk='S'), potom prijmú komponenty (StkStat='S')
- ItmVal = súčet CValue všetkých položiek (komponentov)
- Doklad možno zmazať len ak ItmQnt=0 alebo FIFO karty nie sú použité
- DstLck=1 znamená uzatvorený doklad (nemožno meniť)

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
