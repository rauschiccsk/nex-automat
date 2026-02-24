# PDN - Správa výrobných čísiel (Serial Numbers)

## Popis modulu

Modul pre správu výrobných čísel (sériových čísel) tovaru. Umožňuje evidenciu individuálnych kusov tovaru od príjmu po výdaj, import sériových čísel z externých súborov a prepojenie s FIFO kartami pre kompletné sledovanie traceability.

## Hlavný súbor

`NexModules\Pdn_F.pas`

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| STKPDN | STKPDN.BTR | Evidencia výrobných čísiel | 15 | 5 |
| tIMPPDN | (temp) | Dočasná tabuľka importu | ~6 | 1 |
| tIMPPDG | (temp) | Sumarizácia podľa GsCode | ~8 | 1 |

**Celkom: 1 perzistentná tabuľka, 15 polí, 5 indexov**

## Sub-moduly (6)

### Zobrazenie
| Súbor | Popis |
|-------|-------|
| Pdn_F.pas | Hlavné okno - prezeranie a vyhľadávanie výrobných čísiel |

### Import
| Súbor | Popis |
|-------|-------|
| Imp_PdnLst.pas | Import výrobných čísiel zo súboru (CSV/XML) |
| Imp_PdnDef.pas | Definícia formátu importného súboru |
| Imp_PdnFif.pas | Prepojenie výrobných čísiel s FIFO kartami |

### Výdaj
| Súbor | Popis |
|-------|-------|
| Out_PdnLst.pas | Zoznam výrobných čísiel na výdajovom doklade |
| Out_PdnEdi.pas | Priradenie výrobného čísla k výdaju |

## Štruktúra STKPDN

### Identifikácia

| Pole | Typ | Popis |
|------|-----|-------|
| PrdNum | Str30 | Výrobné číslo tovaru (unikátne) |
| Status | Str1 | Stav: N=prijatý, S=vyskladnený |
| GsCode | longint | Tovarové číslo (PLU) - **FK GSCAT** |
| StkNum | word | Číslo skladu - **FK STKLST** |

### Príjem (Inp - Input)

| Pole | Typ | Popis |
|------|-----|-------|
| InpDoc | Str12 | Číslo príjmového dokladu - **FK TSH** |
| InpItm | word | Číslo položky príjmu |
| InpDat | DateType | Dátum príjmu |
| InpFif | longint | Číslo FIFO karty - **FK FIF** |

### Výdaj (Out - Output)

| Pole | Typ | Popis |
|------|-----|-------|
| OutDoc | Str12 | Číslo výdajového dokladu - **FK TCH** |
| OutItm | word | Číslo položky výdaja |
| OutDat | DateType | Dátum výdaja |

### Audit

| Pole | Typ | Popis |
|------|-----|-------|
| CrtUsr | Str8 | Používateľ vytvorenia |
| CrtDat | DateType | Dátum vytvorenia |
| CrtTim | TimeType | Čas vytvorenia |

## Indexy (5)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | PrdNum | PrdNum | Duplicit |
| 1 | PrdNum, Status | PnSt | Duplicit |
| 2 | PrdNum, Status, GsCode | PnStGc | Duplicit |
| 3 | GsCode | GsCode | Duplicit |
| 4 | OutDoc, OutItm | OdOi | Duplicit |

## Stavy výrobného čísla (Status)

| Status | Popis | Polia vyplnené |
|--------|-------|----------------|
| N | Prijatý (Nový) - na sklade | InpDoc, InpItm, InpDat, InpFif |
| S | Vyskladnený (Shipped) - vydaný | + OutDoc, OutItm, OutDat |

## Workflow

```
1. Import sériových čísel (Imp_PdnLst)
   ┌─────────────────────────────────────────────────────────────┐
   │ Načítanie CSV/XML súboru                                   │
   │ Formát: BaCode;PrdNum (konfigurovateľné pozície)           │
   │ Voliteľne: Transformácia BarCode cez BRGBAC                │
   └─────────────────────────────────────────────────────────────┘
                           │
                           ▼
2. Identifikácia produktu (GSI.Locate)
   ┌─────────────────────────────────────────────────────────────┐
   │ BarCode → GSCAT.GsCode                                     │
   │ Sumarizácia podľa GsCode do tIMPPDG                        │
   └─────────────────────────────────────────────────────────────┘
                           │
                           ▼
3. Prepojenie s FIFO (Imp_PdnFif)
   ┌─────────────────────────────────────────────────────────────┐
   │ Výber FIFO karty s nenulovou zásobou (OutQnt=0)            │
   │ Priradenie: InpDoc, InpItm, InpDat, InpFif                 │
   └─────────────────────────────────────────────────────────────┘
                           │
                           ▼
4. Uloženie do STKPDN (B_SavClick)
   ┌─────────────────────────────────────────────────────────────┐
   │ Status := 'N' (prijatý)                                    │
   │ Kontrola duplicity PrdNum                                  │
   │ Vytvorenie záznamu                                         │
   └─────────────────────────────────────────────────────────────┘
                           │
                           ▼
5. Výdaj tovaru (Out_PdnLst / Out_PdnEdi)
   ┌─────────────────────────────────────────────────────────────┐
   │ Vyhľadanie PrdNum podľa GsCode so Status='N'               │
   │ Priradenie k výdajovému dokladu                            │
   │ Status := 'S' (vyskladnený)                                │
   │ OutDoc, OutItm, OutDat                                     │
   └─────────────────────────────────────────────────────────────┘
```

## Import súboru (Imp_PdnDef)

### Parametre importu

| Parameter | Popis | Príklad |
|-----------|-------|---------|
| DirNam | Adresár s importným súborom | `C:\NEX\IMPORT\` |
| FilNam | Názov súboru | `Serialnummern.txt` |
| SepChr | Oddeľovač stĺpcov | `;` |
| DlmChr | Ohraničovač textu | `"` |
| FmtCsv | CSV formát | TRUE |
| FmtXml | XML formát | FALSE |
| SthFrm | Transformácia cez BRGBAC | FALSE |

### Pozície stĺpcov

| Parameter | Popis | Default |
|-----------|-------|---------|
| BacPos | Pozícia BarCode | 2 |
| PdnPos | Pozícia výrobného čísla | 1 |
| InvPos | Pozícia faktúry (nepoužívané) | 3 |

### Príklad CSV

```csv
SN12345678;4007249040169;INV001
SN12345679;4007249040169;INV001
SN12345680;4007249040176;INV002
```

## Traceability

### Forward tracing (Od príjmu k výdaju)

```
PrdNum → STKPDN.InpFif → FIF.FifNum → STM pohyby → OutDoc → Zákazník
```

### Backward tracing (Od zákazníka k príjmu)

```
OutDoc + OutItm → STKPDN.PrdNum → InpDoc → Dodávateľ
```

## Integrácie

| Závislosť | Popis |
|-----------|-------|
| GSCAT | Katalóg produktov (GsCode, BarCode) |
| FIF | FIFO karty (sledovanie pôvodu) |
| STM | Skladové pohyby |
| TSH/TSI | Príjmové doklady |
| TCH/TCI | Výdajové doklady |
| PAB | Obchodní partneri (dodávateľ/odberateľ) |
| STK | Skladová karta (ActSnQnt) |
| BRGBAC | Transformácia čiarových kódov |
| IMPDEF | Definície importu |
| STKLST | Zoznam skladov |

## Business pravidlá

- Každé výrobné číslo (PrdNum) je unikátne v rámci celého systému
- STK.PdnMust=1 → povinné zadanie výrobného čísla pri príjme/výdaji
- Počet záznamov so Status='N' pre GsCode = STK.ActSnQnt (aktuálna zásoba sériových čísel)
- Pri výdaji sa najprv vyhľadajú dostupné PrdNum (Status='N') pre daný GsCode
- Import kontroluje duplicitu PrdNum pred uložením
- Väzba na FIFO kartu umožňuje kompletné sledovanie pôvodu

## Použitie

- Evidencia sériových čísel elektroniky a zariadení
- Sledovanie záručných opráv
- Reklamačné konania (identifikácia dodávateľskej šarže)
- Inventúra podľa výrobných čísel
- Recall management (stiahnutie produktov)
- Compliance s legislatívou (napr. WEEE)

## UI komponenty

| Komponent | Popis |
|-----------|-------|
| Tv_StkPdn | TableView - zoznam výrobných čísiel |
| E_PrdNum | Vyhľadávanie podľa výrobného čísla |
| E_InpDoc/E_OutDoc | Informácie o príjme/výdaji |
| E_InpPan/E_OutPan | Názvy partnerov |

## Migračné poznámky

- STKPDN je globálna tabuľka (nie per-kniha)
- Import je konfigurovateľný (pozície stĺpcov, oddeľovače)
- Väzba na FIFO je kritická pre traceability
- Status prechody: '' → N → S (jednosmerné)
- Pri migrácii zachovať väzbu PrdNum → InpFif pre historické dáta

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
