# SAB - Skladové výdajky ERP predaja

## Popis modulu

Modul pre správu skladových výdajok z elektronických registračných pokladníc (ERP). Spracováva maloobchodný predaj, vrátenia tovaru, tržby podľa platobných prostriedkov a komponentov výrobkov (receptúry).

## Hlavný súbor

`NexModules\Sab_F.pas`

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| SAH | SAH$$.BTR | Hlavičky výdajok MO predaja | 65 | 6 |
| SAI | SAIyynnn.BTR | Položky výdajok MO predaja | 28 | 6 |
| SAC | SACnnnnn.BTR | Komponenty výrobkov (receptúry) | 31 | 7 |
| SAG | SAGyynnn.BTR | Tržby podľa tovarových skupín | 11 | 4 |
| SABLST | SABLST.BTR | Zoznam kníh ERP predaja | 18 | 1 |
| SAP | SAPyynnn.BTR | Hotovostné úhrady faktúr | 10 | 5 |
| SADMOD | SADMOD.BTR | Modifikované doklady na prepočet | 4 | 1 |

**Celkom: 7 tabuliek, 167 polí, 30 indexov**

## Sub-moduly (31)

### Zobrazenie
| Súbor | Popis |
|-------|-------|
| Sab_SaiLst_F.pas | Položky vybraného dokladu |
| Sab_SagLst_F.pas | Tržba podľa tovarových skupín |
| Sab_SacLst_F.pas | Zoznam výrobkov a komponentov |
| Sab_CasPay_F.pas | Tržba podľa platobných prostriedkov (form) |
| Sab_CasPay_V.pas | Tržba podľa platobných prostriedkov (view) |
| Sab_NsiLst_F.pas | Nevysporiadané položky MO predaja |
| Sab_NscLst_F.pas | Nevysporiadané komponenty |
| Sab_NsiSum_V.pas | Súhrn nevysporiadaných položiek |
| Sab_NscSum_V.pas | Súhrn nevysporiadaných komponentov |
| SabSac_F.pas | Komponenty výrobku (form) |
| SabSac_V.pas | Komponenty výrobku (view) |

### Tlač
| Súbor | Popis |
|-------|-------|
| Sab_SadPrn_F.pas | Tlač dokladov za obdobie |

### Nástroje
| Súbor | Popis |
|-------|-------|
| Sab_ReFund_F.pas | Výkaz predaného a vráteného tovaru |
| Sab_CadVer_F.pas | Porovnávanie s dennou uzávierkou |
| Sab_SabVer_F.pas | Porovnávanie kontrolných pások |
| Sab_SaiLos_F.pas | Položky so záporným ziskom |
| Sab_AccDoc_F.pas | Zaúčtovanie registračnej pokladne |

### Údržba
| Súbor | Popis |
|-------|-------|
| Sab_DocClc_F.pas | Prepočet dokladu podľa položiek |
| Sab_StmSad_F.pas | Porovnávanie dokladu s pohybmi |
| Sab_StmSaa_F.pas | Porovnávanie dokladov s pohybmi |
| Sab_StmSai_F.pas | Porovnávanie položiek s pohybmi |
| Sab_SagClc_F.pas | Prepočet podľa tovarových skupín |
| Sab_SaiSyn_F.pas | Synchronizácia základných údajov |
| Sab_DelOut_F.pas | Vrátiť všetko na sklad |
| Sab_TbiDel_F.pas | Vymazanie pohybov starého spracovania |
| SabAcv_F.pas | Kontrola zaúčtovania dokladov |

### Servis
| Súbor | Popis |
|-------|-------|
| Sab_DocDel_F.pas | Zmazanie celého dokladu |
| Sab_SaiRef_F.pas | Doplnenie údajov do položiek |
| Sab_MgcChg_F.pas | Zmena tovarovej skupiny |
| Sab_CpiVer_F.pas | Kontrola predaja podľa komponentov |

## Prístupové práva (gAfc.Sab.*)

### Úpravy
| Právo | Popis |
|-------|-------|
| DocAdd | Pridanie dokladu |
| DocDel | Zmazanie dokladu |
| DocMod | Úprava dokladu |
| DocLck | Uzatvorenie dokladu |
| DocUnl | Odomknutie dokladu |

### Položky
| Právo | Popis |
|-------|-------|
| ItmAdd | Pridanie položky |
| ItmDel | Zmazanie položky |
| ItmMod | Úprava položky |

### Zobrazenie
| Právo | Popis |
|-------|-------|
| SitLst | Položky dokladu |
| SagLst | Tržba podľa tovarových skupín |
| SacLst | Zoznam výrobkov a komponentov |
| NsiLst | Nevysporiadané položky |
| NscLst | Nevysporiadané komponenty |
| CasPay | Tržba podľa platobných prostriedkov |
| AccLst | Účtovné zápisy dokladu |
| SapLst | Zoznam hotovostných úhrad FA |

### Tlač
| Právo | Popis |
|-------|-------|
| DocPrn | Tlač dokladu |
| SadPrn | Tlač za obdobie |

### Nástroje
| Právo | Popis |
|-------|-------|
| DocFlt | Filtrovanie dokladov |
| SalPro | Spracovanie pokladničného predaja |
| AccDoc | Zaúčtovanie dokladu |
| AccDel | Zrušenie zaúčtovania |
| AccBok | Hromadné zaúčtovanie knihy |
| RefRep | Výkaz predaného a vráteného tovaru |
| CadVer | Porovnávanie s dennou uzávierkou |
| SabVer | Porovnávanie kontrolných pások |
| SaiLos | Položky so záporným ziskom |
| OitSnd | Medziprevádzkový presun dokladu |
| SahDcl | Zápis údajov podľa DPH |

### Údržba a servis
| Právo | Popis |
|-------|-------|
| MntFnc | Údržbové funkcie |
| SrvFnc | Servisné funkcie |

## Stavové príznaky

### Hlavička (SAH)
| Pole | Hodnota | Popis |
|------|---------|-------|
| DstAcc | A | Doklad je zaúčtovaný |
| Sended | 1 | Zmeny odoslané |
| SndStat | . | Odoslaný |
| SndStat | O | Potvrdený |
| SndStat | E | Chybný prenos |

### Položky (SAI)
| Pole | Hodnota | Popis |
|------|---------|-------|
| StkStat | N | Neodpočítaný zo skladu |
| StkStat | S | Vyskladnený |
| StkStat | C | Rozdelený na komponenty |

### Komponenty (SAC)
| Pole | Hodnota | Popis |
|------|---------|-------|
| StkStat | N | Neodpočítaný |
| StkStat | S | Vyskladnený |
| ItmType | C | Komponent |
| ItmType | W | Práca |

## Väzby na iné moduly

| Modul | Popis väzby |
|-------|-------------|
| STK | Sklady - výdaj tovaru |
| GSCAT | Tovarový katalóg |
| MGLST | Tovarové skupiny |
| CSD | Hotovostná pokladňa - príjem tržby |
| ICD | Faktúry - hotovostné úhrady |
| CPI | Kalkulácie výrobkov (receptúry) |
| JRN | Hlavný denník - účtovné zápisy |

## Prepojenie na pokladničné doklady

### SAH obsahuje referencie na:
| Pole | Typ dokladu | Popis |
|------|-------------|-------|
| BvlDoc | Príjmový PD | Príjem dennej tržby v PC |
| CseDoc | Výdajový PD | Výdaj odvedenej hotovosti do HP |
| CsiDoc | Príjmový PD | Príjem odvedenej hotovosti do HP |
| SpiDoc | Príjmový PD | Príjem zálohy |
| SpeDoc | Výdajový PD | Výdaj použitej zálohy |
| SpvDoc | Interný ÚD | Zaúčtovanie DPH záloh |
| CrcDoc | Výdajový PD | Výdaj platobných kariet |
| IncCse | Výdajový PD | Výdaj hotovosti z HP do ERP |
| IncCsi | Príjmový PD | Príjem hotovosti z HP do ERP |

## Špecifické funkcie

### Nevysporiadané položky (NsiCnt)
Položky, ktoré ešte neboli odpočítané zo skladu. Červené zvýraznenie v zozname dokladov.

### Komponenty výrobkov (SAC)
Rozpad výrobkov na komponenty podľa receptúr (CPI). Umožňuje správne vyskladnenie surovín pri predaji hotových výrobkov.

### Tržba podľa tovarových skupín (SAG)
Agregované hodnoty predaja členené podľa tovarových skupín pre analytické účely.

### Hotovostné úhrady FA (SAP)
Evidencia úhrad faktúr v hotovosti priamo na ERP pokladni.

## DPH členenie

Modul podporuje 5 sadzieb DPH:
- VatPrc1/AValue1/VatVal1/BValue1
- VatPrc2/AValue2/VatVal2/BValue2
- VatPrc3/AValue3/VatVal3/BValue3
- VatPrc4/AValue4/VatVal4/BValue4
- VatPrc5/AValue5/VatVal5/BValue5

## Workflow

```
1. Import z ERP pokladne (Cab_SalProc_F)
   - Denná uzávierka pokladne
   - Vytvorenie SAH hlavičky
   - Import položiek do SAI
   ↓
2. Spracovanie komponentov (SAC)
   - Rozpad výrobkov na komponenty
   - Podľa receptúr z CPI
   ↓
3. Vysporiadanie skladu
   - Odpočítanie tovaru zo skladu (StkStat='S')
   - NsiCnt → 0
   ↓
4. Zaúčtovanie (DstAcc='A')
   - Vytvorenie pokladničných dokladov
   - Zápisy do JRN
```

## Použitie

- Maloobchodný predaj cez ERP pokladne
- Sledovanie denných tržieb
- Analýza predaja podľa tovarových skupín
- Správa komponentov výrobkov (gastronómia)
- Hotovostné úhrady faktúr

## Stav migrácie

- [x] Analýza modulu
- [x] BDF dokumentácia
- [ ] Btrieve modely (nexdata)
- [ ] PostgreSQL modely
- [ ] API endpointy
