# CPBLST - Zoznam kníh kalkulácií výrobkov

## Kľúčové slová / Aliases

CPBLST, CPBLST.BTR, zoznam, kníh, kalkulácií, výrobkov

## Popis

Tabuľka zoznamu kníh kalkulácií výrobkov. Obsahuje konfiguráciu jednotlivých kníh vrátane nastavenia skladov, cenníka a spôsobu cenotvorby. Globálny súbor.

## Btrieve súbor

`CPBLST.BTR`

## Umiestnenie

`C:\NEX\YEARACT\DATA\CPBLST.BTR`

## Štruktúra polí (19 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CpbNum | longint | 4 | Číslo knihy kalkulácií |
| CpbName | Str30 | 31 | Názov knihy |
| WriNum | word | 2 | Číslo prevádzkovej jednotky |

### Konfigurácia skladov a cenníka

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PdStkNum | word | 2 | Sklad hotových výrobkov - **FK STKLST** |
| CpStkNum | word | 2 | Sklad komponentov výroby - **FK STKLST** |
| PdPlsNum | word | 2 | Predajný cenník hotových výrobkov - **FK PLSLST** |

### Nastavenia cenotvorby

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RndType | byte | 1 | Typ zaokrúhlenia predajnej ceny (0-6) |
| PlsSave | byte | 1 | Automaticky prenášať zmeny do cenníka (1=zapnuté) |
| AvgClc | byte | 1 | Spôsob cenotvorby (0=posledná NC, 1=priemerná NC) |
| FrmNum | byte | 1 | Číslo použitého formulára |

### Štatistika

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ItmQnt | word | 2 | Počet kalkulácií v danej knihe |

### Zdieľanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Shared | byte | 1 | Príznak zdieľania (1=zdieľaný cez FTP) |

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

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | CpbNum | CpbNum | Unikátny |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PdStkNum | STKLST.StkNum | Sklad hotových výrobkov |
| CpStkNum | STKLST.StkNum | Sklad komponentov |
| PdPlsNum | PLSLST.PlsNum | Predajný cenník |

## Typy zaokrúhlenia (RndType)

| Hodnota | Popis |
|---------|-------|
| 0 | Na 0.01 (centy) |
| 1 | Na 0.10 |
| 2 | Na 0.50 |
| 3 | Na 1.00 |
| 4 | Na 5.00 |
| 5 | Na 10.00 |
| 6 | Podľa tabuľky zaokrúhlenia |

## Spôsob cenotvorby (AvgClc)

| Hodnota | Popis | Použitie |
|---------|-------|----------|
| 0 | Posledná nákupná cena | CPI.CPrice = STK.LastPrice |
| 1 | Priemerná nákupná cena | CPI.CPrice = STK.AvgPrice |

## Príklad konfigurácie

```
Kniha: Kalkulácie - Pekáreň
─────────────────────────────────────────────────────────────────
CpbNum    = 1
CpbName   = "Pekárske výrobky"
PdStkNum  = 10 (Sklad hotových výrobkov)
CpStkNum  = 20 (Sklad surovín)
PdPlsNum  = 1  (Hlavný predajný cenník)
AvgClc    = 1  (Priemerná NC)
RndType   = 1  (Na 0.10)
PlsSave   = 1  (Automatický prenos do cenníka)
```

## Použitie

- Definícia kníh kalkulácií pre rôzne typy výroby
- Nastavenie zdrojových skladov pre komponenty a výrobky
- Konfigurácia automatického exportu cien do cenníka
- Voľba metódy oceňovania (posledná vs priemerná NC)

## Business pravidlá

- Knihu možno zmazať len ak ItmQnt=0 (neobsahuje kalkulácie)
- PdStkNum = sklad kam idú hotové výrobky
- CpStkNum = sklad odkiaľ sa čerpajú ceny komponentov
- PlsSave=1 automaticky aktualizuje PLS.BPrice pri uložení kalkulácie
- AvgClc určuje či sa použije LastPrice (0) alebo AvgPrice (1) zo STK

## Súvisiace súbory

Pre každú knihu (CpbNum=nnnnn) existujú:
- `CPHnnnnn.BTR` - hlavičky kalkulácií (výrobky)
- `CPInnnnn.BTR` - položky kalkulácií (komponenty)

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
