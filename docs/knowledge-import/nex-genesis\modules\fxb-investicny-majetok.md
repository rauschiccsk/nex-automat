# FXB - Evidencia investičného majetku (Fixed Assets)

## Prehľad modulu

- **Súbor**: `NexModules\Fxb_F.pas`
- **Účel**: Kompletná evidencia dlhodobého hmotného a nehmotného majetku s daňovými a účtovnými odpismi
- **Kategória**: Účtovníctvo / Majetok
- **Mark modulu**: FXB

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| FXBLST | FXBLST.BTR | Knihy investičného majetku | 23 | 2 |
| FXA | FXAyynnn.BTR | Evidenčné karty majetku | 43 | 12 |
| FXT | FXTyynnn.BTR | Daňové odpisy (ročné) | 21 | 5 |
| FXL | FXLyynnn.BTR | Účtovné odpisy (mesačné) | 21 | 5 |
| FXC | FXCyynnn.BTR | Technické zhodnotenie | 15 | 4 |
| FXM | FXMyynnn.BTR | Korekcia vstupnej ceny | 15 | 4 |
| FXN | FXNyynnn.BTR | Poznámky k majetku | 2 | 1 |
| FXTGRP | FXTGRP.BTR | Daňové odpisové skupiny | 21 | 3 |
| FXAGRP | FXAGRP.BTR | Účtovné skupiny majetku | ~15 | 2 |
| FXAASD | FXAASD.BTR | Údaje vyradenia majetku | 68 | 3 |

**Celkom: 10 tabuliek, ~244 polí, ~41 indexov**

## Sub-moduly (28)

### Hlavné obrazovky
| Súbor | Popis |
|-------|-------|
| Fxb_F.pas | Hlavný formulár - zoznam kariet majetku |
| Fxb_CrdEdit_F.pas | Editor evidenčnej karty majetku |
| Fxb_Book_F.pas | Správa kníh majetku |

### Odpisy
| Súbor | Popis |
|-------|-------|
| Fxb_FxtLst_F.pas / _V.pas | Zoznam daňových odpisov |
| Fxb_FxlLst_F.pas / _V.pas | Zoznam účtovných odpisov |
| Fxb_FxlDir_V.pas | Všetky účtovné odpisy |
| Fxb_Recalc.pas | Prepočet odpisov |
| Fxb_SulClc_F.pas | Prepočet sadzby účtovných odpisov |
| Fxb_SutClc_F.pas | Prepočet sadzby daňových odpisov |

### Skupiny
| Súbor | Popis |
|-------|-------|
| Fxb_FxaGrp_F.pas / _V.pas | Účtovné skupiny majetku |
| Fxb_FxtGrp_F.pas / _V.pas | Daňové odpisové skupiny |

### Zmeny a vyradenie
| Súbor | Popis |
|-------|-------|
| Fxb_FxcLst_F.pas / _V.pas | Technické zhodnotenie |
| Fxb_FxmLst_F.pas / _V.pas | Korekcia vstupnej ceny |
| Fxb_AsdFxa_F.pas | Vyradenie majetku z užívania |
| Fxb_Aside_F.pas | Protokol o vyradení |

### Tlač a export
| Súbor | Popis |
|-------|-------|
| Fxb_PrnCrd_F.pas | Tlač inventárnej karty |
| Fxb_ActSuPrn_F.pas | Tlač účtovných a daňových odpisov |
| Fxb_Info_F.pas | Informácie o module |

### Filtrovanie
| Súbor | Popis |
|-------|-------|
| Fxb_Filt_F.pas | Filter zoznamu majetku |
| Fxb_FxaFilt_V.pas | Výber filtra |

### Účtovanie
| Súbor | Popis |
|-------|-------|
| Fxb_Acc_F.pas | Zaúčtovanie majetku |
| Fxb_IntEdi_F.pas | Editor prerušenia odpisov |

### Pomocné
| Súbor | Popis |
|-------|-------|
| Fxb_Upgrade_F.pas | Upgrade štruktúr |

## Typy majetku (FxaType)

| Hodnota | Typ | Popis |
|---------|-----|-------|
| 0 | DHM | Dlhodobý hmotný majetok |
| 1 | DNM | Dlhodobý nehmotný majetok |

## Spôsob obstarania (PrvMode)

| Hodnota | Spôsob | Popis |
|---------|--------|-------|
| 0 | Nákup | Obstaranie kúpou |
| 1 | Dar | Bezodplatné nadobudnutie |
| 2 | Vlastná výroba | Vytvorenie vlastnou činnosťou |

## Spôsob vyradenia (AsdMode)

| Hodnota | Spôsob | Popis |
|---------|--------|-------|
| 0 | - | Nevyradený |
| 1 | Predaj | Odpredaj majetku |
| 2 | Likvidácia | Fyzická likvidácia |
| 3 | Škoda | Vyradenie v dôsledku škody |
| 4 | Dar | Bezodplatný prevod |
| 5 | Manko | Zistené manko |

## Odpisové metódy

### Daňové odpisy (TsuMode)

| Hodnota | Metóda | Popis |
|---------|--------|-------|
| 0 | Rovnomerné | Lineárne odpisovanie |
| 1 | Zrýchlené | Degresívne odpisovanie |

### Odpisové skupiny podľa zákona o dani z príjmov

| Skupina | Doba | Príklady majetku |
|---------|------|------------------|
| 1 | 4 roky | Osobné automobily, kancelárska technika |
| 2 | 6 rokov | Nákladné vozidlá, stroje |
| 3 | 8 rokov | Technológie, lode |
| 4 | 12 rokov | Budovy (niektoré) |
| 5 | 20 rokov | Budovy (väčšina) |
| 6 | 40 rokov | Budovy trvalé, mosty |

### Sadzby rovnomerného odpisovania (FXTGRP)

| Pole | Popis |
|------|-------|
| LiPrcOne | Sadzba pre prvý rok |
| LiPrcNxt | Sadzba pre ďalšie roky |
| LiPrcInc | Sadzba pre zvýšenú cenu (TZ) |

### Koeficienty zrýchleného odpisovania (FXTGRP)

| Pole | Popis |
|------|-------|
| QcKfcOne | Koeficient pre prvý rok |
| QcKfcNxt | Koeficient pre ďalšie roky |
| QcKfcInc | Koeficient pre zvýšenú cenu (TZ) |

## Výpočet odpisov

### Rovnomerné odpisy

```
Prvý rok:    Odpis = VstupnáCena × LiPrcOne / 100
Ďalšie roky: Odpis = VstupnáCena × LiPrcNxt / 100
So zvýšením: Odpis = ZvýšenáCena × LiPrcInc / 100
```

### Zrýchlené odpisy

```
Prvý rok:    Odpis = VstupnáCena / QcKfcOne
Ďalšie roky: Odpis = (2 × Zostatková) / (QcKfcNxt - PočetOdpísanýchRokov + 1)
So zvýšením: Odpis = (2 × ZvýšenáZostatková) / (QcKfcInc - PočetOdZvýšenia + 1)
```

### Zostatkové hodnoty

```
TEndVal = PrvVal + ChgVal - ModVal - SuVal  // Daňová zostatková cena
LEndVal = PrvVal + ChgVal - ModVal - SuVal  // Účtovná zostatková cena
```

## Technické zhodnotenie (FXC)

Podmienky pre technické zhodnotenie:
- Od roku 2001: hodnota > 663.88 EUR (20 000 SKK)
- Od roku 2003: hodnota > 995.82 EUR (30 000 SKK)
- Aktuálne: hodnota > 1 700 EUR

Pri technickom zhodnotení sa zvyšuje vstupná cena a predlžuje sa doba odpisovania.

## Integrácie

### Zdrojové tabuľky

| Tabuľka | Použitie |
|---------|----------|
| WRILST | Prevádzkové jednotky |
| PARTNER | Dodávatelia majetku |
| JOURNAL | Zaúčtovanie odpisov |

### Dátové toky

```
FXA (karta majetku)
    ↓
├→ FXT (daňové odpisy)
├→ FXL (účtovné odpisy)
├→ FXC (technické zhodnotenie)
├→ FXM (korekcia ceny)
└→ FXN (poznámky)
    ↓
├→ JOURNAL (účtovanie odpisov)
├→ Tlač (inventárne karty)
└→ FXAASD (vyradenie)
```

## Účtovanie odpisov

### Typické účtovné zápisy

| Operácia | MD | Dal |
|----------|----|----|
| Odpis DHM | 551 | 081,082 |
| Odpis DNM | 551 | 071,072 |
| Vyradenie - predaj | 541 | 08x,07x |
| Vyradenie - likvidácia | 549,551 | 08x,07x |
| Tržba z predaja | 641 | 311 |

## Tlačové zostavy

| Report | Popis |
|--------|-------|
| FXALST | Zoznam investičného majetku |
| FXACRD | Inventárna karta majetku |
| FXAASS | Protokol o vyradení majetku |
| FXTSUL | Odpisový plán (daňový) |
| FXLSUL | Odpisový plán (účtovný) |

## UI komponenty

| Komponent | Popis |
|-----------|-------|
| BL_Fxb | BookList - zoznam kníh majetku |
| TV_Fxb | TableView - karty majetku |
| E_FxaType | ComboBox - typ majetku |
| E_TsuGrp | ComboBox - daňová skupina |
| E_TsuMode | ComboBox - metóda odpisovania |
| E_PrvMode | ComboBox - spôsob obstarania |

### Menu štruktúra

- **Program** - Ukončenie, O programe
- **Úpravy** - Pridať/Zmazať kartu
- **Zobrazit** - Odpisy, Skupiny, Tech. zhodnotenie
- **Tlač** - Karty, Odpisové plány
- **Nástroje** - Prepočet odpisov, Zaúčtovanie
- **Údržba** - Prepočet sadzieb

## Business pravidlá

### Karta majetku

- SerNum je automatické poradové číslo
- DocNum = BookNum + SerNum (formátované)
- ExtNum = inventárne číslo (voliteľné)
- Majetok sa nedá zmazať ak má odpisy

### Odpisy

- Daňové odpisy sú ročné (FXT)
- Účtovné odpisy môžu byť mesačné (FXL)
- Status='L' znamená že účtovné = daňové
- Prerušenie odpisov ovplyvňuje dobu odpisovania

### Vyradenie

- Pri vyradení sa musí vyplniť FXAASD
- Vyradený majetok sa zobrazuje šedo
- Zostatkové hodnoty sa uplatnia daňovo/účtovne

### Slovenská legislatíva

- Odpisové skupiny podľa §26-27 Zákona o dani z príjmov
- Technické zhodnotenie podľa §29
- Prerušenie odpisov podľa §22 ods. 9
- Konverzia SKK→EUR (kurz 30.126) pre rok 2009

## Migračné poznámky

### Pre PostgreSQL migráciu

1. **Multi-book štruktúra** - FXAyynnn, FXTyynnn, FXLyynnn:
   ```sql
   CREATE TABLE fxa (
     id SERIAL PRIMARY KEY,
     book_num VARCHAR(5) NOT NULL,
     ser_num INTEGER NOT NULL,
     doc_num VARCHAR(12) NOT NULL,
     -- ostatné polia
     UNIQUE (book_num, ser_num)
   );
   ```

2. **Mesačné účtovné odpisy** (FXL) vs ročné daňové (FXT):
   - FXL má Year + Month
   - FXT má len Year

3. **Výpočet odpisov** - komplexná logika:
   - Rovnomerné vs zrýchlené
   - Technické zhodnotenie
   - Prerušenie odpisov

4. **FXTGRP** - závislosť na roku:
   - Sadzby sa menia podľa legislatívy
   - GrpYear ako súčasť kľúča

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
