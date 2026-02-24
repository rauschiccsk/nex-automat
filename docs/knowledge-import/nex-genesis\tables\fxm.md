# FXM - Korekcia vstupnej ceny majetku

## Kľúčové slová / Aliases

FXM, FXM.BTR, korekcia, vstupnej, ceny, majetku

## Popis

Tabuľka korekcií vstupnej ceny dlhodobého majetku. Slúži na evidenciu úprav obstarávacej ceny, ktoré nie sú technickým zhodnotením (napr. dodatočné náklady, opravy účtovných chýb, kurzové rozdiely).

## Btrieve súbor

`FXMyynnn.BTR` (yy=rok, nnn=číslo knihy z FXBLST)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\FXMyynnn.BTR`

## Štruktúra polí (15 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo karty majetku - **FK FXA** |
| DocDate | DateType | 4 | Dátum korekcie |
| DocYear | word | 2 | Rok, do ktorého patrí korekcia |
| DocMth | byte | 1 | Mesiac, do ktorého patrí korekcia |

### Údaje korekcie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Describ | Str30 | 31 | Textový popis - dôvod korekcie |
| DocVal | double | 8 | Hodnota korekcie (+ zvýšenie, - zníženie) |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtName | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Počet modifikácií |
| ModUser | Str8 | 9 | Používateľ zmeny |
| ModDate | DateType | 4 | Dátum zmeny |
| ModTime | TimeType | 4 | Čas zmeny |

## Indexy (4)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum | DocNum | Duplicit |
| 1 | DocDate | DocDate | Duplicit |
| 2 | DocNum, DocYear | DoDy | Duplicit |
| 3 | DocNum, DocYear, DocMth | DoDyDm | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | FXA.DocNum | Evidenčná karta majetku |

## Výpočtové pravidlá

### Vplyv na FXA

```
FXA.ModVal = SUM(FXM.DocVal) pre daný DocNum
```

### Vplyv na odpisy

```
VstupnáCena = PrvVal + ChgVal - ModVal
```

Korekcia znižuje alebo zvyšuje vstupnú cenu pre výpočet odpisov.

## Rozdiel FXM vs FXC

| Vlastnosť | FXM (Korekcia) | FXC (Tech. zhodnotenie) |
|-----------|----------------|-------------------------|
| Účel | Oprava ceny | Investícia do majetku |
| Doba odpisovania | Nemení sa | Môže sa predĺžiť |
| Typické prípady | Kurzové rozdiely, chyby | Rekonštrukcia, modernizácia |
| Limit hodnoty | Nie | Áno (1 700 EUR) |

## Typické dôvody korekcie

| Dôvod | DocVal | Popis |
|-------|--------|-------|
| Dodatočné náklady | + | Preprava, montáž objasnená neskôr |
| Oprava chyby | +/- | Nesprávna obstarávacia cena |
| Kurzový rozdiel | +/- | Majetok v cudzej mene |
| Zľava od dodávateľa | - | Dodatočná zľava |
| Dobropis | - | Reklamácia časti ceny |

## Použitie

- Evidencia zmien vstupnej ceny
- Opravy účtovných chýb
- Kurzové rozdiely pri zahraničnom majetku
- Dodatočné náklady obstarania

## Business pravidlá

- DocVal môže byť kladný (zvýšenie) aj záporný (zníženie)
- Korekcia ovplyvňuje výpočet odpisov od DocYear/DocMth
- Nemení dobu odpisovania (na rozdiel od tech. zhodnotenia)
- Musí byť vyplnený Describ s dôvodom

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
