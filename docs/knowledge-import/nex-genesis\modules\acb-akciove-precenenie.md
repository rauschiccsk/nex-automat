# ACB - Akciové precenenie tovaru

## Popis modulu

Modul pre hromadné precenenie tovaru v rámci cenových akcií. Umožňuje vytvárať precenovacie doklady s položkami, definovať akciové ceny, spúšťať a ukončovať cenové akcie s automatickou aktualizáciou predajného cenníka (PLS) a synchronizáciou do pokladní.

## Hlavný súbor

`NexModules\Acb_F.pas`

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| ACBLST | ACBLST.BTR | Zoznam kníh akciových precenení | 17 | 2 |
| ACH | ACHyynnn.BTR | Hlavičky precenovacích dokladov | 19 | 5 |
| ACI | ACIyynnn.BTR | Položky precenovacích dokladov | 28 | 7 |
| ACDTMP | ACDTMP.BTR | Dočasne uložený doklad | 14 | 1 |
| ACHOLE | ACHOLE.BTR | Voľné poradové čísla dokladov | 7 | 1 |
| ACPLST | ACPLST.BTR | Položky pre tlač akciových letákov | 19 | 4 |

**Celkom: 6 tabuliek, 104 polí, 20 indexov**

## Sub-moduly (12)

### Editácia
| Súbor | Popis |
|-------|-------|
| Acb_AchEdit_F.pas | Editor hlavičky precenovacieho dokladu |
| Acb_AciEdit_F.pas | Editor položky precenovacieho dokladu |
| Acb_AciLst_F.pas | Zoznam položiek vybraného dokladu |

### Zobrazenie
| Súbor | Popis |
|-------|-------|
| Acb_AcdLst_V.pas | Zoznam dočasných položiek |

### Tlač
| Súbor | Popis |
|-------|-------|
| Acb_DocPrn_F.pas | Tlač precenovacieho dokladu |
| Acb_PrnNew_F.pas | Tlač cenoviek s akciovými cenami |
| Acb_PrnAft_F.pas | Tlač cenoviek po ukončení akcie |

### Nástroje
| Súbor | Popis |
|-------|-------|
| Acb_ActRun_F.pas | Zahájenie cenovej akcie |
| Acb_ActEnd_F.pas | Ukončenie cenovej akcie |
| Acb_SndApl_F.pas | Odoslanie do akciového cenníka (APL) |
| Acb_ImpAci_F.pas | Import akciových cien |
| Acb_ReadTmp_F.pas | Načítanie dočasných údajov (deprecated) |

## Prístupové práva

Modul ACB používa štandardný mechanizmus kníh cez BOKLST:
- `gAfc.ACB.WriteData('ACB', I, True)` - nastavenie práv
- Práva sú nastavované pri vytvorení knihy

## Kľúčové vlastnosti

### Typy dokladov (DocType)
- **A** = Akciové precenenie (s akciou)
- **Z** = Zmena predajných cien (bez akcie)

### Stavy dokladu (Status)
- **N** = Pripravený (nový) - zelená farba
- **A** = Akcia prebieha - červená farba
- **X** = Ukončená akcia (pre typ Z)
- **E** = Ukončená akcia (pre typ A)

### Cenové údaje v položke (ACI)
- **StkCPrice** = nákupná cena bez DPH (zo skladu)
- **BefBPrice** = predajná cena s DPH pred precenením
- **NewBPrice** = akciová predajná cena s DPH
- **AftBPrice** = predajná cena s DPH po ukončení akcie
- **BefProfit** = zisk % pred precenením
- **NewProfit** = zisk % počas akcie
- **AftProfit** = zisk % po ukončení akcie

### Farebné rozlíšenie
- **Zelená** (clGreen) - pripravený doklad (Status='N')
- **Červená** (clRed) - prebiehajúca akcia (Status='A')
- **Čierna** (clBlack) - ukončená alebo bežná

## Workflow

```
1. Vytvorenie dokladu (ACH)
   ┌─────────────────────────────────────────────────────────────┐
   │ Status='N', DocType='A' alebo 'Z'                          │
   │ BegDate, EndDate = obdobie akcie                           │
   └─────────────────────────────────────────────────────────────┘
                            │
                            ▼
2. Pridanie položiek (ACI)
   ┌─────────────────────────────────────────────────────────────┐
   │ GsCode, BefBPrice (aktuálna), NewBPrice (akciová)          │
   │ AftBPrice (cena po akcii)                                  │
   └─────────────────────────────────────────────────────────────┘
                            │
                            ▼
3. Zahájenie akcie (Acb_ActRun_F)
   ┌─────────────────────────────────────────────────────────────┐
   │ PLS.BPrice := ACI.NewBPrice                                │
   │ PLS.Action := 'A' (ak DocType='A')                         │
   │ PLH záznam s Status='A', ModPrg='ACB'                      │
   │ ACI.Status := 'A' alebo 'X'                                │
   │ Export do pokladní (PLSnnnnn.REF)                          │
   └─────────────────────────────────────────────────────────────┘
                            │
                            ▼
4. Ukončenie akcie (Acb_ActEnd_F)
   ┌─────────────────────────────────────────────────────────────┐
   │ PLS.BPrice := ACI.AftBPrice                                │
   │ PLS.Action := ''                                           │
   │ PLH záznam s Status='E', ModPrg='ACB'                      │
   │ ACI.Status := 'E'                                          │
   │ Export do pokladní                                         │
   └─────────────────────────────────────────────────────────────┘
```

## Rozdiel ACB vs APL vs TPC

| Vlastnosť | ACB (Precenenie) | APL (Akciové ceny) | TPC (Terminované) |
|-----------|------------------|--------------------|--------------------|
| Účel | Hromadná zmena cien | Definícia akciových cien | Plánovanie zmeny ceny |
| Aktivácia | Manuálna (ActRun) | Automatická podľa dátumu | Automatická v pokladni |
| Zmena PLS | Priama aktualizácia | Cez ACB alebo priamo | V pokladni |
| História PLH | Áno (Status='A','E') | Nie | Nie |
| Cena po akcii | AftBPrice | Pôvodná z PLS | Nie je |
| Periodicita | Nie | Áno (dni v týždni) | Nie |
| Export APL | Acb_SndApl_F | - | - |

## Integrácie

| Závislosť | Popis |
|-----------|-------|
| PLS | Predajný cenník - aktualizácia cien |
| PLH | História zmien cien - záznam zmien |
| STK | Skladová karta - nákupná cena pre výpočet zisku |
| GSCAT | Katalóg produktov |
| CABLST | Zoznam pokladní pre export |
| APLITM | Akciový cenník - export položiek |
| BOKLST | Zoznam kníh modulu |

## Business pravidlá

- Doklad možno zmazať len ak Status='N' (pripravený)
- Pri zahájení akcie sa zapisuje do PLH s ModPrg='ACB'
- Zisk sa prepočítava z LastPrice alebo AvgPrice podľa nastavenia
- Pri type 'A' sa nastavuje PLS.Action='A' (akciový príznak)
- Pri ukončení akcie sa PLS.Action vyprázdni
- Export prebieha do všetkých pokladní s príslušným PlsNum

## Konfigurácia knihy (ACBLST)

- **PlsNum** = číslo predajného cenníka pre knihu
- **RndType** = spôsob zaokrúhľovania predajnej ceny
- **LabPrn** = automatická tlač cenovkových etikiet

## Export do pokladní

Formát REF súboru (CSV):
```
M;GsCode;GsName;MgCode;FgCode;BarCode;StkCode;MsName;PackGs;StkNum;VatPrc;PdnMust;GrcMth;Profit;APrice;BPrice;OrdPrn;OpenGs
```

## UI komponenty

- **TV_Ach** - TableView so zoznamom dokladov
- **Nb_BokLst** - Zoznam kníh (TNxbLst)
- Farebné rozlíšenie podľa Status

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
