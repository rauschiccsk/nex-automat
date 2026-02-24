# LAB - Tlač cenovkových etikiet

## Popis modulu

Modul pre tlač cenovkových etikiet v NEX Genesis. Umožňuje naplnenie fronty etikiet z rôznych zdrojov (dodacie listy, interné doklady, cenník), úpravu počtu kusov a následnú tlač na etiketovú tlačiareň. Podporuje akciové ceny a zobrazenie minimálnej historickej ceny.

## Hlavný súbor

`NexModules\Lab_F.pas`

## Tabuľky modulu

| Tabuľka | Súbor | Popis | Polí | Indexov |
|---------|-------|-------|------|---------|
| LABITM | LABITM.BTR | Fronta tlače cenovkových etikiet | 22 | 4 |
| tLABPRN | (temp) | Dočasná tabuľka pre tlač | 35+ | 1 |
| APL_LOG | APL_LOG.BTR | Log vytlačených etikiet | - | - |

**Celkom: 1 perzistentná tabuľka, 22 polí, 4 indexy**

## Sub-moduly (5)

### Editácia
| Súbor | Popis |
|-------|-------|
| Lab_ItmAdd_F.pas | Pridanie položky do fronty |

### Tlač
| Súbor | Popis |
|-------|-------|
| Lab_PrnItm_F.pas | Alternatívne rozhranie tlače |
| LabPrn.pas | Trieda TLabPrn - jadro tlačového procesu |

### Filter
| Súbor | Popis |
|-------|-------|
| Lab_PlsFlt_F.pas | Filter cenníka podľa MgCode, FgCode, dátumu zmeny |

### Konfigurácia
| Súbor | Popis |
|-------|-------|
| LabKey.pas | Konfiguračné kľúče modulu |

## Trieda TLabPrn

Hlavná trieda pre spracovanie a tlač etikiet v `NexCommons\LabPrn.pas`:

### Metódy

| Metóda | Popis |
|--------|-------|
| Add(pLabItm) | Pridá položku do dočasnej tabuľky tLABPRN |
| Prn | Spustí tlač cez RepHand (výstup do gPath.RepPath+'LAB') |

### Obohatenie dát (v metóde Add)

```pascal
// Základné údaje z LABITM
tLABPRN.GsCode := pLabItm.GsCode;
tLABPRN.GsName := pLabItm.GsName;
tLABPRN.BarCode := pLabItm.BarCode;
...

// Akciové ceny z APLITM (ak existuje aktívna akcia)
If btAPLITM.Locate(GsCode) then begin
  tLABPRN.AcAPrice := btAPLITM.AcAPrice;  // Akciová cena bez DPH
  tLABPRN.AcBPrice := btAPLITM.AcBPrice;  // Akciová cena s DPH
  tLABPRN.BegDate := btAPLITM.BegDate;    // Začiatok akcie
  tLABPRN.EndDate := btAPLITM.EndDate;    // Koniec akcie
end;

// Minimálna cena z PLH histórie
tLABPRN.MinPrice := GetMinPrice(GsCode);  // Min BPrice za posledných N dní
```

## Štruktúra tLABPRN (dočasná tabuľka)

### Identifikácia

| Pole | Typ | Popis |
|------|-----|-------|
| ItmNum | longint | Poradové číslo položky |
| GsCode | longint | Tovarové číslo (PLU) |
| MgCode | longint | Tovarová skupina |
| FgCode | longint | Finančná skupina |
| GsName | Str30 | Názov tovaru |
| GaName | Str60 | Alternatívny názov |
| BarCode | Str15 | EAN kód |
| StkCode | Str15 | Skladový kód |
| MsName | Str10 | Merná jednotka |

### Mena

| Pole | Typ | Popis |
|------|-----|-------|
| InfDvz | Str3 | Informačná mena |
| AccDvz | Str3 | Účtovná mena |
| FixCrs | Str10 | Fixný kurz |

### Akciové ceny (Ac*)

| Pole | Typ | Popis |
|------|-----|-------|
| BegDate | DateTime | Začiatok akcie |
| EndDate | DateTime | Koniec akcie |
| AcAPrice | double | Akciová cena bez DPH |
| AcBPrice | double | Akciová cena s DPH |
| AcXPrice | double | Akciová cena v cudzej mene |
| AcBpcInt | Str6 | Celá časť ceny (pre veľký font) |
| AcBpcFrc | Str2 | Desatinná časť ceny |
| AcYPrice | Str15 | Formátovaná akciová cena |
| AcMPrice | Str15 | Akciová cena za MJ |
| AcMuName | Str10 | MJ pre akciovú cenu |

### Bežné ceny (Fg*)

| Pole | Typ | Popis |
|------|-----|-------|
| FgAPrice | double | Bežná cena bez DPH |
| FgBPrice | double | Bežná cena s DPH |
| FgXPrice | double | Bežná cena v cudzej mene |
| FgYPrice | Str15 | Formátovaná bežná cena |
| FgMPrice | Str15 | Bežná cena za MJ |
| FgMuName | Str10 | MJ pre bežnú cenu |

### Historická cena

| Pole | Typ | Popis |
|------|-----|-------|
| MinPrice | double | Minimálna historická cena (z PLH) |

### Poznámky

| Pole | Typ | Popis |
|------|-----|-------|
| Notice1-6 | Str60 | Textové poznámky na etiketu |

## Workflow

```
1. Naplnenie fronty (LABITM)
   ┌─────────────────────────────────────────────────────────────┐
   │ Zdroj A: TSI (položky príjemky) → Lab_F                    │
   │ Zdroj B: IMI (položky výdajky) → Lab_F                     │
   │ Zdroj C: PLS filter (cenník) → Lab_PlsFlt_F                │
   │ Zdroj D: Manuálne → Lab_ItmAdd_F                           │
   └─────────────────────────────────────────────────────────────┘
                           │
                           ▼
2. Úprava fronty (Lab_F)
   ┌─────────────────────────────────────────────────────────────┐
   │ TV_LabItm: Zobrazenie položiek vo fronte                   │
   │ LabQnt: Úprava počtu etikiet pre každú položku             │
   │ Delete: Odstránenie položiek z fronty                      │
   └─────────────────────────────────────────────────────────────┘
                           │
                           ▼
3. Príprava tlače (TLabPrn.Add)
   ┌─────────────────────────────────────────────────────────────┐
   │ Pre každú položku v LABITM:                                │
   │   → Vytvorenie záznamu v tLABPRN                           │
   │   → Doplnenie akciových cien z APLITM                      │
   │   → Výpočet MinPrice z PLH histórie                        │
   │   → Formátovanie cien (AcBpcInt, AcBpcFrc, YPrice)         │
   └─────────────────────────────────────────────────────────────┘
                           │
                           ▼
4. Tlač (TLabPrn.Prn)
   ┌─────────────────────────────────────────────────────────────┐
   │ RepHand.Output := gPath.RepPath + 'LAB'                    │
   │ Výstup na etiketovú tlačiareň                              │
   │ Zápis do APL_LOG (log vytlačených etikiet)                 │
   └─────────────────────────────────────────────────────────────┘
```

## Filter cenníka (Lab_PlsFlt_F)

| Parameter | Typ | Popis |
|-----------|-----|-------|
| MgCode | word | Filter podľa tovarovej skupiny |
| FgCode | word | Filter podľa finančnej skupiny |
| BegDate | date | Zmena ceny od dátumu (PLH) |
| EndDate | date | Zmena ceny do dátumu (PLH) |

## Konfigurácia (gKey.Lab)

| Parameter | Popis |
|-----------|-------|
| RepPath | Cesta k report šablónam (gPath.RepPath+'LAB') |
| MinPriceDays | Počet dní pre výpočet MinPrice |

## Prístupové práva

| Právo | Popis |
|-------|-------|
| gAfc.Lab.LabPrn | Tlač etikiet |
| gAfc.Lab.ItmAdd | Pridanie položky do fronty |
| gAfc.Lab.ItmDel | Odstránenie položky z fronty |
| gAfc.Lab.PlsFlt | Filter cenníka |

## Integrácie

| Závislosť | Popis |
|-----------|-------|
| LABITM | Fronta tlače |
| GSCAT | Katalóg produktov |
| PLS | Cenníková tabuľka |
| PLH | História zmien cien (MinPrice) |
| APLITM | Aktívne akciové ceny |
| APL_LOG | Log vytlačených etikiet |
| TSI | Položky dodacích listov |
| IMI | Položky interných dokladov |
| MGLST | Tovarové skupiny |
| RepHand | Report engine |

## Business pravidlá

- LABITM je perzistentná fronta - položky zostávajú aj po tlači
- tLABPRN je dočasná tabuľka vytvorená pred tlačou
- Akciové ceny sa zobrazujú len ak existuje aktívny záznam v APLITM
- MinPrice = minimálna BPrice z PLH za konfigurovateľný počet dní
- AcBpcInt/AcBpcFrc slúžia na formátovanie ceny veľkým fontom
- APL_LOG zaznamenáva každú tlač pre audit

## Formát etikety

Etiketa typicky obsahuje:
- GsName (názov produktu)
- BarCode (čiarový kód EAN)
- FgBPrice (bežná cena s DPH)
- AcBPrice (akciová cena, ak existuje)
- BegDate-EndDate (platnosť akcie)
- MinPrice (minimálna historická cena - legislatíva)

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
