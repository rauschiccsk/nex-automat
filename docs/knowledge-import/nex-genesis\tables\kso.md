# KSO - História pohybov konsignačného vyúčtovania

## Kľúčové slová / Aliases

KSO, KSO.BTR, história, pohybov, konsignačného, vyúčtovania

## Popis

Tabuľka histórie pohybov položiek konsignačného vyúčtovania. Zaznamenáva všetky súvisiace operácie vrátane predaja, zápožičky, vrátenky a nákupu. Slúži na kompletné sledovanie životného cyklu konsignačného tovaru. Každá kniha má vlastný súbor.

## Btrieve súbor

`KSOyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\KSOyynnn.BTR`

## Štruktúra polí (31 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo konsignačnej náhlásky - **FK KSH** |
| ItmNum | word | 2 | Poradové číslo položky dokladu |
| GsCode | longint | 4 | Tovarové číslo (PLU) - **FK GSCAT** |
| BPrice | double | 8 | Predajná cena s DPH |

### Predaj / Výdaj (Out)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| OutDoc | Str12 | 13 | Interné číslo dokladu predaja |
| OutItm | longint | 4 | Poradové číslo položky dokladu |
| OutQnt | double | 8 | Predané/vydané množstvo |
| OutVal | double | 8 | Hodnota predaja/výdaja |
| OutDat | DateType | 4 | Dátum predaja/výdaja |
| OutPac | longint | 4 | Číselný kód odberateľa |

### Konsignačná zápožička (Ren - Rental)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RenDoc | Str12 | 13 | Interné číslo dokladu konsignačnej zápožičky |
| RenItm | longint | 4 | Poradové číslo položky dokladu |
| RenFif | longint | 4 | FIFO karta konsignačnej zápožičky |
| RenVal | double | 8 | Hodnota konsignačnej zápožičky |
| RenDat | DateType | 4 | Dátum príjmu konsignačnej zápožičky |

### Konsignačná vrátenka (Ret - Return)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RetDoc | Str12 | 13 | Interné číslo dokladu konsignačnej vrátenky |
| RetItm | longint | 4 | Poradové číslo položky dokladu |
| RetDat | DateType | 4 | Dátum výdaja konsignačnej vrátenky |

### Konsignačný nákup (Buy)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BuyDoc | Str12 | 13 | Interné číslo dokladu konsignačného nákupu |
| BuyItm | longint | 4 | Poradové číslo položky dokladu |
| BuyFif | longint | 4 | FIFO karta konsignačného nákupu |
| BuyVal | double | 8 | Hodnota nakúpeného príjmu |
| BuyDat | DateType | 4 | Dátum príjmu konsignačného nákupu |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (4)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum, ItmNum, OutDoc, OutItm, RenFif | DoItOdOiRf | Unikátny |
| 1 | DocNum, ItmNum | DoIt | Duplicit |
| 2 | DocNum | DocNum | Duplicit |
| 3 | GsCode | GsCode | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | KSH.DocNum | Hlavička vyúčtovania |
| GsCode | GSCAT.GsCode | Katalógová karta produktu |
| OutDoc | TCH/ICH.DocNum | Doklad predaja |
| OutPac | PAB.PaCode | Odberateľ |
| RenDoc | TSH.DocNum | Doklad zápožičky |
| RenFif | FIF.FifNum | FIFO karta zápožičky |
| RetDoc | TSH.DocNum | Doklad vrátenky |
| BuyDoc | TSH.DocNum | Doklad nákupu |
| BuyFif | FIF.FifNum | FIFO karta nákupu |

## Životný cyklus záznamu

```
1. Zápožička (Ren)
   ┌─────────────────────────────────────────┐
   │ RenDoc, RenItm, RenFif, RenVal, RenDat │
   │ Príjem konsignačného tovaru             │
   └─────────────────────────────────────────┘
                    │
                    ▼
2. Predaj (Out)
   ┌─────────────────────────────────────────┐
   │ OutDoc, OutItm, OutQnt, OutVal, OutDat │
   │ OutPac = odberateľ                      │
   └─────────────────────────────────────────┘
                    │
                    ▼
3. Vyúčtovanie - Vrátenka (Ret)
   ┌─────────────────────────────────────────┐
   │ RetDoc, RetItm, RetDat                  │
   │ Konsignačné vysporiadanie (S)           │
   └─────────────────────────────────────────┘
                    │
                    ▼
4. Vyúčtovanie - Nákup (Buy)
   ┌─────────────────────────────────────────┐
   │ BuyDoc, BuyItm, BuyFif, BuyVal, BuyDat │
   │ Konsignačné vyúčtovanie (C)             │
   └─────────────────────────────────────────┘
```

## Použitie

- Kompletná história pohybov konsignačného tovaru
- Sledovanie od príjmu cez predaj po vyúčtovanie
- Kontrola správnosti vyúčtovania
- Audit a reporting

## Business pravidlá

- Jeden záznam pre každú kombináciu DocNum+ItmNum+OutDoc+OutItm+RenFif
- Ren* polia sa vyplnia pri konsignačnom príjme
- Out* polia sa vyplnia pri predaji
- Ret* polia sa vyplnia pri generovaní vrátenky
- Buy* polia sa vyplnia pri generovaní nákupu

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
