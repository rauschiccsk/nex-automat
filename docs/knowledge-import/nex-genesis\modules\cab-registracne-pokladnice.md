# CAB - Knihy registračných pokladníc (Cash Register Books)

## Prehľad modulu

- **Súbor**: `NexModules\Cab_F.pas`
- **Účel**: Konfigurácia a správa registračných pokladníc, spracovanie denných uzávierok
- **Kategória**: Maloobchod / POS

## Vzťah CAB vs SAB

| Modul | Účel | Tabuľky |
|-------|------|---------|
| CAB | Knihy/konfigurácia pokladníc (master data), denné uzávierky | CABLST, CAH, CAP |
| SAB | Skladové výdajky z pokladní (transakcie) | SAH, SAI, SAC, SAG |

## Tabuľky modulu

### Hlavné tabuľky

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| CABLST | CABLST.BTR | Zoznam kníh registračných pokladníc | 17 | 2 |
| CAH | CAHnnnnn.BTR | Denné uzávierkové údaje (Z-report) | 107 | 1 |
| CAP | CAPnnnnn.BTR | Register platidiel pokladne | 12 | 1 |
| CASLST | CASLST.BTR | Zoznam elektronických pokladníc | 6 | 1 |
| CASREG | CASREG.BTR | Globálny register platidiel | 8 | 1 |
| CAPDEF | CAPDEF.BTR | Definícia typov platidiel | 2 | 1 |
| CAPADV | CAPADV.BTR | Rozpis platidiel (stravovacie lístky) | 11 | 2 |
| CASORD | CASORD.BTR | Pokladničné objednávky (kuchyňa) | 16 | 7 |
| CAFSUM | CAFSUM.BTR | Kumulatívny stav podľa pokladníkov | 22 | 2 |
| CAFDOC | CAFDOC.BTR | Doklady podľa pokladníkov | 25 | 2 |
| CATLOG | CATLOG.BTR | Log prenosov do ERP | 70 | 2 |

**Celkom: 11 tabuliek**

## Sub-moduly

| Súbor | Popis |
|-------|-------|
| Cab_F.pas | Hlavný formulár - prehľad kníh pokladníc |
| Cab_SalProc_F.pas | Spracovanie pokladničného predaja (import T-súborov) |
| Sys_CasLst_F.pas | Editor konfigurácie pokladne |

## Dátový model

### Vzťahy

```
CABLST (Knihy pokladníc)
   │
   ├──→ CAHnnnnn (Denné uzávierky)
   │       ↓
   │    (10 typov platidiel: PayName0-9)
   │
   ├──→ CAPnnnnn (Register platidiel)
   │
   └──→ STKLST (Predvolený sklad)

CASLST (Elektronické pokladne)
   │
   └──→ CASORD (Objednávky)

CAPDEF (Definícia platidiel)
   │
   └──→ CAPADV (Rozpis - stravovacie lístky, cudzie meny)

CAFSUM + CAFDOC (Evidencia podľa pokladníkov)
```

## Štruktúra dennej uzávierky (CAH)

### Platobné prostriedky (10 typov)

```
┌─────────────────────────────────────────────────────────────────┐
│ Pre každý typ platidla (0-9):                                   │
│   PayNameX  = Názov platidla (Hotovosť, Karta, Strav.lístky...) │
│   BegValX   = Počiatočný stav                                   │
│   TrnValX   = Denná tržba                                       │
│   IncValX   = Príjem do pokladne                                │
│   ExpValX   = Odvod tržby                                       │
│   ChIValX   = Príjem - zmena platidla                           │
│   ChEValX   = Výdaj - zmena platidla                            │
│   EndVal    = Konečný stav (vypočítaný)                         │
└─────────────────────────────────────────────────────────────────┘
```

### DPH členenie (3 sadzby)

| Pole | Popis |
|------|-------|
| VatPrc1/VatVal1/BValue1 | Základná sadzba DPH |
| VatPrc2/VatVal2/BValue2 | Znížená sadzba DPH |
| VatPrc3/VatVal3/BValue3 | Nulová sadzba |

### Súhrnné hodnoty

| Pole | Popis |
|------|-------|
| GT1Val | Hrubý obrat |
| GT2Val | Čistý obrat |
| GT3Val | Záporný obrat |
| AValue | Celková hodnota bez DPH |
| VatVal | Celková hodnota DPH |
| BValue | Celková hodnota s DPH |
| ClmVal | Hodnota reklamácií |
| NegVal | Hodnota záporných položiek |
| DscVal | Hodnota zliav |
| CncVal | Hodnota stornovaných bločkov |

## Workflow spracovania predaja

```
1. ERP pokladňa vytvorí T-súbor (kontrolná páska)
   ┌─────────────────────────────────────────────────────────────┐
   │ Súbor: T{RRRRMMDD}.{nnn}                                    │
   │ Umiestnenie: {CasPath}\T20240115.001                        │
   │ Formát: Textový súbor s riadkami SB, SI, CI, SC, RB, RP...  │
   └─────────────────────────────────────────────────────────────┘
                           │
                           ▼
2. Spracovanie (Cab_SalProc_F.B_RunClick)
   ┌─────────────────────────────────────────────────────────────┐
   │ LoadTFile     - Načítanie kontrolnej pásky                  │
   │ LoadToCbh     - Načítanie hlavičkových údajov               │
   │ LoadToCbi     - Načítanie položiek predaja                  │
   │ LoadToSap     - Načítanie úhrad faktúr                      │
   │ LoadToSpd     - Načítanie príjmov/čerpaní záloh             │
   └─────────────────────────────────────────────────────────────┘
                           │
                           ▼
3. Vytvorenie skladových dokladov (SAH/SAI)
   ┌─────────────────────────────────────────────────────────────┐
   │ CollectSai    - Agregácia položiek do SAI                   │
   │ SaveToSai     - Uloženie do SAI                             │
   │ CpiToSacTmp   - Rozpad výrobkov na komponenty (SAC)         │
   │ ClcCpSuQnt    - Výpočet vyskladnených komponentov           │
   └─────────────────────────────────────────────────────────────┘
                           │
                           ▼
4. Skladové operácie
   ┌─────────────────────────────────────────────────────────────┐
   │ F_DocHand.OutputSaDoc - Výdaj zo skladu                     │
   │ SaiResSts     - Rezervácia nevysporiadaných položiek        │
   │ SahRecalc     - Prepočet hlavičky SAH                       │
   └─────────────────────────────────────────────────────────────┘
```

## Formát kontrolnej pásky (T-súbor)

| Kód | Význam | Príklad |
|-----|--------|---------|
| SB | Začiatok bločku | SB;9;4;2;11.8.2024;7:13:05;... |
| SI | Položka predaja | SI;Názov;MgCode;GsCode;Množstvo;DPH;... |
| CI | Komponent | CI;Názov;MgCode;GsCode;Množstvo;... |
| SC | Koniec bločku | SC;... |
| RB | Úhrada faktúry | RB;...;IceNum;Hodnota;... |
| RP | Platba | RP;... |
| RC | Kreditná karta | RC;... |

## Typy platidiel

| Kód | Typický názov | Popis |
|-----|---------------|-------|
| 0 | Hotovosť | Platba v hotovosti |
| 1 | Platobná karta | Platba kartou |
| 2 | Stravovacie lístky | Gastro lístky, poukážky |
| 3 | Šek | Šeková platba |
| 4 | Preddavok | Záloha, depozit |
| 5 | Kredit | Na úver |
| 6-9 | Ostatné | Podľa konfigurácie |

## CAPADV - Rozpis platidiel

Pre stravovacie lístky a cudzie meny:

```
┌─────────────────────────────────────────────────────────────────┐
│ PayNum   = Kód platidla (napr. 2 = Stravovacie lístky)         │
│ AdvName  = Typové označenie (DOXX, CHEQUE DEJEUNER, ...)       │
│ PayName  = Názov platobného prostriedku                        │
│ IncVal   = Prijaté množstvo (počet lístkov)                    │
│ ChgCrs   = Nominálna hodnota lístku / Prevodový kurz           │
│ PayVal   = Zaplatená čiastka = IncVal × ChgCrs                 │
└─────────────────────────────────────────────────────────────────┘
```

## CATLOG - Evidencia prenosov

Sleduje prenosy údajov do ERP pokladníc:

| Typ | Popis |
|-----|-------|
| P | Predajné ceny |
| A | Akciové ceny |
| T | Terminované ceny |
| K | Zákaznícke karty |

Pre každú z 20 pokladníc eviduje:
- RcvDaXX - Dátum prijatia
- RcvTiXX - Čas prijatia
- RcvStXX - Stav (O=prijaté)

## Konfigurácia knihy (CABLST)

| Parameter | Popis |
|-----------|-------|
| BookNum | Číslo knihy (rrNNN) |
| BookName | Názov knihy |
| CasNum | Číslo pokladne |
| CasPath | Cesta k adresáru kontrolných pások |
| PlsNum | Číslo cenníka |
| StkNum | Predvolené číslo skladu |
| WriNum | Číslo prevádzkovej jednotky |
| CasStk | Zdroj čísla skladu (1=pokladňa, 0=kniha) |

## Väzby na iné moduly

| Modul | Popis väzby |
|-------|-------------|
| SAB | Skladové výdajky - transakcie predaja |
| STK | Sklady - výdaj tovaru |
| PLS | Cenníky - predajné ceny |
| GSCAT | Tovarový katalóg |
| CPI | Kalkulácie - rozpad na komponenty |
| ICD | Faktúry - hotovostné úhrady |
| PAB | Partneri - zákazníci |
| CRD | Kreditné karty |
| JRN | Hlavný denník - účtovanie |

## Migrácia z CASSAS

Modul obsahuje migračnú funkciu `CassasToCabLst`:
- Prekopíruje záznamy zo starej tabuľky CASSAS do novej CABLST
- Automaticky sa spustí ak CABLST je prázdna

## Business pravidlá

1. **Knihu možno zmazať** len ak neobsahuje denné uzávierky (CAH.RecordCount=0)
2. **Denná uzávierka** je identifikovaná dátumom (DocDate) - jeden záznam na deň
3. **Číslo dokladu** pre SAH: `CB{RRRRMMDD}{nnnn}` kde nnnn = číslo pokladne
4. **Spracovanie** kontroluje dátum uzávierky (gIni.GetSabClsDate)
5. **Nevysporiadané položky** - tovar ktorý nebol odpočítaný zo skladu

## UI komponenty

| Komponent | Popis |
|-----------|-------|
| BL_CabLst | BookList - výber knihy pokladníc |
| TV_Cah | TableView - zoznam denných uzávierok |
| P_CabEmpty | Panel - zobrazí sa ak nie sú žiadne knihy |

## eKasa poznámka

NEX Genesis bol vyvíjaný pred zavedením eKasa (2019). Modul CAB pracuje s tradičnými ERP pokladňami. Pre eKasa integráciu by bola potrebná rozsiahla úprava na:
- Online registráciu bločkov
- UUID dokladov
- Komunikáciu s FS SR

## Stav migrácie

- [x] Analýza modulu
- [x] BDF dokumentácia
- [ ] Btrieve modely (nexdata)
- [ ] PostgreSQL modely
- [ ] API endpointy
