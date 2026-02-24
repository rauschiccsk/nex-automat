# PLS - Predajné cenníky

## Popis modulu

Modul pre správu predajných cenníkov. Umožňuje tvorbu predajných cien, cenové hladiny (D1-D3), akcie, zľavy, históriu zmien cien, filtrovanie podľa tovarových skupín, tlač cenových etikiet a synchronizáciu s pokladňami/terminálmi.

## Hlavný súbor

`NexModules\Pls_F.pas`

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| PLS | PLSnnnnn.BTR | Položky predajného cenníka | 50 | 16 |
| PLSLST | PLSLST.BTR | Zoznam predajných cenníkov | 17 | 2 |
| PLSADD | PLSADD.BTR | Rozširujúce údaje cenníka | 5 | 3 |
| PLH | PLHnnnnn.BTR | História zmien predajných cien | 14 | 5 |
| PLD | PLDnnnnn.BTR | Zoznam zrušených položiek | 31 | 12 |
| DSCLST | DSCLST.BTR | Číselník typov zliav | 12 | 2 |

**Celkom: 6 tabuliek, 129 polí, 40 indexov**

## Sub-moduly (41)

### Editácia
| Súbor | Popis |
|-------|-------|
| Pls_PlcEdit_F.pas | Formulár na zadávanie predajnej ceny |
| Pls_LevEdi_F.pas | Karta tvorby predajnej ceny |
| Pls_ItmEdi_F.pas | Formulár cenotvorby a evidencie položky |
| Pls_Edit_F.pas | Základný editor položky |
| Pls_PlcEdi.pas | Editor cien |
| Pls_PlcLst.pas | Zoznam cien |
| Pls_EditBook_F.pas | Editor knihy cenníka |

### Zobrazenie
| Súbor | Popis |
|-------|-------|
| Pls_PlsLst_V.pas | Zoznam položiek cenníka |
| Pls_PlsHis_V.pas | História zmeny ceny |
| Pls_PlsMod_V.pas | História zmeny údajov |
| Pls_PlsDis_V.pas | Zoznam vyradených položiek |
| Pls_PlsDel_V.pas | Zoznam zrušených položiek |
| Pls_PlsPck_V.pas | Zoznam vratných obalov |
| Pls_PlsWgs_V.pas | Zoznam váhových tovarov |
| Pls_PlsPgs_V.pas | Zoznam obalových tovarov |
| Pls_PlsAct_V.pas | Zoznam akciových tovarov |
| Pls_PlcDif_V.pas | Porovnanie cien |
| Pls_GscDif_V.pas | Porovnanie s evidenciou tovaru |
| Pls_LapChg_V.pas | Zmeny nákupných cien |
| Pls_SapChg_V.pas | Zmeny predajných cien |

### Tlač
| Súbor | Popis |
|-------|-------|
| Pls_PrnFgc_F.pas | Tlač cenníka podľa finančných skupín |
| Pls_OrdPrn_F.pas | Tlač kuchynských objednávok |

### Nástroje
| Súbor | Popis |
|-------|-------|
| Pls_PlsFilt_F.pas | Filtrovanie položiek cenníka |
| Pls_PlsFilt_V.pas | Filtrovanie - pohľad |
| Pls_BcSrch_F.pas | Hľadať podľa čiarového kódu |
| Pls_NaSrch_F.pas | Hľadať podľa časti názvu |
| Pls_NusPls_F.pas | Nepoužité tovarové položky |
| Pls_PlsRef_F.pas | Obnova cenníka |
| Pls_ReCalc_F.pas | Prepočet cien |
| Pls_GsCopy_F.pas | Kopírovanie položiek |
| Pls_ApCalc_F.pas | Prepočet predajnej ceny bez DPH |
| Pls_LevClc_F.pas | Prepočet cenových hladín |
| Pls_RefGen_F.pas | Generovanie referencií |
| Pls_SetStk_F.pas | Nastavenie skladu |
| Pls_RndVer_F.pas | Kontrola zaokrúhlenia ceny/MJ |

### Údržba
| Súbor | Popis |
|-------|-------|
| Pls_Synchr_F.pas | Synchronizácia základných údajov |
| Pls_DifRef_F.pas | Kontrola rozdielov |
| Pls_PlcDif_F.pas | Rozdiel cien |
| Pls_GscDif_F.pas | Rozdiel s katalógom |
| Pls_LapChg_F.pas | Zmeny nákupných cien - formulár |
| Pls_DelSlc.pas | Zmazanie vybraných položiek |

## Prístupové práva

Modul PLS nepoužíva samostatný súbor Usd_AfcPls.pas. Prístupové práva sú spravované cez štandardný mechanizmus kníh pomocou funkcií:
- `BookInsert('PLS', PlsNum, TRUE)`
- `BookModify('PLS', PlsNum, TRUE)`
- `BookDelete('PLS', PlsNum, TRUE)`
- `BookProperty('PLS', PlsNum, TRUE)`

## Kľúčové vlastnosti

### Cenové hladiny (D1-D3)
- **APrice / BPrice** = základná cena (bez DPH / s DPH)
- **APrice1 / BPrice1** = cenová hladina D1
- **APrice2 / BPrice2** = cenová hladina D2
- **APrice3 / BPrice3** = cenová hladina D3
- **DscPrc1-3** = percentuálna zľava pre hladiny
- **PrfPrc1-3** = zisk pre hladiny

### Farebné rozlíšenie položiek
- **Červená** (clRed) - záporný zisk (Profit < 0)
- **Zelená** (clGreen) - akciový tovar (Action='A') alebo obal (GsType='P')
- **Modrá** (clBlue) - zmenená položka (ChgItm='X')
- **Šedá** (clGray) - vyradená položka (DisFlag=1)

### Typy položiek (GsType)
- **T** = riadny tovar
- **W** = váhový tovar
- **O** = obal

### Zdroj nákupnej ceny (CpcSrc)
- **A** = priemerná cena
- **L** = posledná cena
- **B** = GSCAT
- **P** = nákupné podmienky

## Integrácie

| Závislosť | Popis |
|-----------|-------|
| GSCAT | Katalóg produktov |
| BARCODE | Čiarové kódy |
| STKLST | Zoznam skladov |
| STK | Skladová karta |
| MGLST | Tovarové skupiny (stromová štruktúra) |
| FGLST | Finančné skupiny |
| SRCAT | Kategórie (pre NexStart) |
| PAB | Obchodní partneri (dodávatelia, odberatelia) |

## Business pravidlá

- BPrice = APrice * (1 + VatPrc/100) zaokrúhlené podľa RndType
- Profit = (APrice - NC) / NC * 100
- FixLevel v PLSADD určuje hladiny nepodliehajúce prepočtu (bitová maska 1+2+4+8)
- DelPls=1 povoľuje zrušenie cenníka
- Shared=1 aktivuje FTP synchronizáciu
- Master určuje hlavný cenník pre závislosť

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
