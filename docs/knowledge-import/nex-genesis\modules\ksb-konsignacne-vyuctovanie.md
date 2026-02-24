# KSB - Konsignačné vyúčtovanie

## Popis modulu

Modul pre správu konsignačného (komisionálneho) vyúčtovania tovaru. Umožňuje evidenciu tovaru prijatého na konsignáciu od dodávateľa, sledovanie predaja a automatické generovanie vyúčtovacích dokladov. Konsignácia znamená, že tovar zostáva vo vlastníctve dodávateľa až do jeho predaja koncovému zákazníkovi.

## Hlavný súbor

`NexModules\Ksb_F.pas`

## Terminológia

| Pojem | Kód | Popis |
|-------|-----|-------|
| Konsignačné zapožičanie | K | Príjem konsignačného tovaru od dodávateľa |
| Konsignačné vrátenie | K | Výdaj (vrátenie) nepredaného tovaru dodávateľovi |
| Konsignačné vysporiadanie | S | Výdaj tovaru na vyúčtovanie (predaný tovar) |
| Konsignačné vyúčtovanie | C | Príjem vyúčtovaného tovaru (prevod vlastníctva) |

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| KSH | KSHyynnn.BTR | Hlavičky dokladov konsignačného vyúčtovania | 29 | 6 |
| KSI | KSIyynnn.BTR | Položky dokladov konsignačného vyúčtovania | 36 | 5 |
| KSN | KSNyynnn.BTR | Poznámky k dokladom | 6 | 2 |
| KSO | KSOyynnn.BTR | História pohybov položiek | 31 | 4 |

**Celkom: 4 tabuľky, 102 polí, 17 indexov**

## Sub-moduly (7)

### Editácia
| Súbor | Popis |
|-------|-------|
| Ksb_KsdAdd_F.pas | Pridanie nového dokladu vyúčtovania |
| Ksb_KsiEdi.pas | Editor položky dokladu |
| Ksb_KsiLst_F.pas | Zoznam položiek vybraného dokladu |

### Zobrazenie
| Súbor | Popis |
|-------|-------|
| Ksb_KsiDir_V.pas | Položky všetkých dokladov (servis) |

### Nástroje
| Súbor | Popis |
|-------|-------|
| Ksb_TsdGen_F.pas | Generovanie dodacích listov (vyúčtovanie) |

### Údržba
| Súbor | Popis |
|-------|-------|
| Ksb_KsdVer.pas | Kontrola konsignačného vyúčtovania |

### Konfigurácia
| Súbor | Popis |
|-------|-------|
| KsbKey.pas | Konfiguračné kľúče modulu |

## Prístupové práva

Modul KSB používa dedikovaný prístupový modul `AfcKsb.pas`:
- `gAfc.Ksb.DocAdd` - pridať doklad
- `gAfc.Ksb.DocDel` - zmazať doklad
- `gAfc.Ksb.SitLst` - zobraziť položky
- `gAfc.Ksb.MntFnc` - údržbové funkcie
- `gAfc.Ksb.SerFnc` - servisné funkcie
- `gAfc.Ksb.DocPrn` - tlač dokladu
- `gAfc.Ksb.TsdGen` - generovanie dodacích listov

## Kľúčové vlastnosti

### Farebné rozlíšenie
- **Čierna** (clBlack) - otvorený doklad (TsdNum='')
- **Šedá** (clGray) - uzavretý doklad (TsdNum<>''), vygenerovaný DL

### Cenové údaje
- **CValue** = nákupná cena bez DPH
- **EValue** = nákupná cena s DPH
- **AValue** = predajná cena bez DPH
- **BValue** = predajná cena s DPH
- **PrfPrc** = obchodná marža v %
- **PrfVal** = obchodná marža v EUR

### Obdobie vyúčtovania
- **BegDate** = začiatok dátumového intervalu
- **EndDate** = koniec dátumového intervalu

### Väzba na konsignačný príjem
- **KidNum** = číslo dokladu konsignačného príjmu
- **KidItm** = poradové číslo položky
- **KidDate** = dátum konsignačného príjmu
- **FifNum** = číslo FIFO karty konsignačného príjmu

## Workflow

```
1. Konsignačný príjem (TSB s typom K)
   ┌─────────────────────────────────────────────────────────────┐
   │ Tovar prijatý na konsignáciu → STK (AcqStat='K')           │
   │ FIFO karta s konsignačným príznakom                        │
   └─────────────────────────────────────────────────────────────┘
                            │
                            ▼
2. Predaj tovaru (TCB/ICB)
   ┌─────────────────────────────────────────────────────────────┐
   │ Výdaj zo skladu → STM pohyb z konsignačnej FIFO            │
   │ Tovar stále vo vlastníctve dodávateľa                      │
   └─────────────────────────────────────────────────────────────┘
                            │
                            ▼
3. Vyúčtovanie (KSB)
   ┌─────────────────────────────────────────────────────────────┐
   │ Výber obdobia BegDate - EndDate                            │
   │ Sumarizácia predaného tovaru                               │
   │ Vytvorenie dokladu KSH + KSI                               │
   └─────────────────────────────────────────────────────────────┘
                            │
                            ▼
4. Generovanie DL (Ksb_TsdGen_F)
   ┌─────────────────────────────────────────────────────────────┐
   │ RetGen: Konsignačná vrátenka (výdaj S)                     │
   │ BuyGen: Konsignačný nákup (príjem C)                       │
   │ RdcOut: Presmerovanie FIFO na vyúčtovanie                  │
   │ SmrGen: Vytvorenie pohybov vrátenky                        │
   │ RetVer + BuyVer + StmVer: Kontrola                         │
   └─────────────────────────────────────────────────────────────┘
                            │
                            ▼
5. Prevod vlastníctva
   ┌─────────────────────────────────────────────────────────────┐
   │ STM.AcqStat := 'C' (Consignment cleared)                   │
   │ Tovar je teraz vo vlastníctve firmy                        │
   │ TsdNum v KSH ukazuje na vygenerovaný DL                    │
   └─────────────────────────────────────────────────────────────┘
```

## Konfigurácia knihy (gKey.Ksb)

| Parameter | Popis |
|-----------|-------|
| TsoBok[BokNum] | Kniha pre konsignačnú vrátenku (výdaj) |
| TsiBok[BokNum] | Kniha pre konsignačný nákup (príjem) |
| TsoSmc[BokNum] | Skladový pohyb pre vrátenku |
| TsiSmc[BokNum] | Skladový pohyb pre nákup |

## Integrácie

| Závislosť | Popis |
|-----------|-------|
| TSB | Dodávateľské dodacie listy (generovanie DL) |
| TSH/TSI | Hlavičky a položky dodacích listov |
| STK | Skladová karta (stav zásob) |
| STM | Skladové pohyby (FIFO) |
| FIF | FIFO karty (sledovanie pôvodu tovaru) |
| PAB | Obchodní partneri (dodávatelia) |
| GSCAT | Katalóg produktov |
| BOKLST | Zoznam kníh modulu |

## Business pravidlá

- Doklad možno zmazať len ak ItmQnt=0
- Po vygenerovaní DL je doklad uzavretý (TsdNum<>'')
- TsdGen je dostupný len pre doklady bez TsdNum
- AcqStat='K' označuje konsignačný tovar v sklade
- AcqStat='C' označuje vyúčtovaný konsignačný tovar
- Kontrola zabezpečuje, že kumulatívna hodnota vyúčtovania = 0

## História pohybov (KSO)

Tabuľka KSO zaznamenáva všetky pohyby pre každú položku:
- **OutDoc/OutItm** - doklad predaja/výdaja
- **RenDoc/RenItm/RenFif** - konsignačná zápožička
- **RetDoc/RetItm** - konsignačná vrátenka
- **BuyDoc/BuyItm/BuyFif** - konsignačný nákup

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
