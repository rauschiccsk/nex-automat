# ACI - Položky precenovacích dokladov

## Kľúčové slová / Aliases

ACI, ACI.BTR, položky, precenovacích, dokladov

## Popis

Tabuľka položiek precenovacích dokladov pre akciové precenenie tovaru. Obsahuje údaje o tovare a cenách pred, počas a po cenovej akcii. Každá kniha akciových precenení má vlastný súbor.

## Btrieve súbor

`ACIyynnn.BTR` (yy=rok, nnn=číslo knihy)

## Umiestnenie

`C:\NEX\YEARACT\DOCS\ACIyynnn.BTR`

## Štruktúra polí (28 polí)

### Identifikácia dokladu

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DocNum | Str12 | 13 | Interné číslo precenovacieho dokladu - **FK ACH** |

### Identifikácia tovaru

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo (PLU) - **FK GSCAT** |
| MgCode | word | 2 | Číslo tovarovej skupiny |
| GsName | Str30 | 31 | Názov tovaru |
| _GsName | Str30 | 31 | Vyhľadávacie pole názvu |
| BarCode | Str15 | 16 | Identifikačný kód tovaru (EAN) |
| StkCode | Str15 | 16 | Skladový kód tovaru |
| MsName | Str10 | 11 | Názov mernej jednotky |

### Cenové údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| StkCPrice | double | 8 | Nákupná cena tovaru bez DPH |
| BefBPrice | double | 8 | Predajná cena s DPH pred precenením |
| NewBPrice | double | 8 | Akciová predajná cena s DPH |
| AftBPrice | double | 8 | Predajná cena s DPH po ukončení akcie |
| VatPrc | byte | 1 | Sadzba DPH v % |

### Zisk

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BefProfit | double | 8 | Zisk v % pred precenením |
| NewProfit | double | 8 | Zisk v % počas akciovej ceny |
| AftProfit | double | 8 | Zisk v % po ukončení akcie |

### Obdobie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BegDate | DateType | 4 | Dátum začiatku cenovej akcie |
| EndDate | DateType | 4 | Dátum ukončenia cenovej akcie |

### Stav

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| Status | Str1 | 2 | Stav riadku |
| ActPos | Str2 | 3 | Rezervované |

### Audit

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (7)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | DocNum | DocNum | Duplicit |
| 1 | DocNum, GsCode | DoGs | Duplicit |
| 2 | GsCode | GsCode | Duplicit |
| 3 | _GsName | GsName | Duplicit, Case-insensitive |
| 4 | BarCode | BarCode | Duplicit |
| 5 | StkCode | StkCode | Duplicit, Case-insensitive |
| 6 | Status | Status | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| DocNum | ACH.DocNum | Hlavička dokladu |
| GsCode | GSCAT.GsCode | Katalógová karta produktu |
| GsCode | PLS.GsCode | Položka predajného cenníka |
| GsCode | STK.GsCode | Skladová karta |

## Stavy položky (Status)

| Hodnota | Stav | Popis |
|---------|------|-------|
| (prázdny) | Nová | Položka čaká na spracovanie |
| N | Pripravená | Pripravená na zahájenie akcie |
| A | Aktívna | Prebieha cenová akcia |
| X | Ukončená | Ukončená zmena cien (typ Z) |
| E | Ukončená | Ukončená akcia (typ A) |

## Výpočtové pravidlá

### Zisk

```
Profit = (APrice / CPrice - 1) * 100

kde:
  APrice = BPrice / (1 + VatPrc/100)
  CPrice = LastPrice alebo AvgPrice zo STK
```

### Cena bez DPH

```
APrice = BPrice / (1 + VatPrc / 100)
```

## Použitie

- Evidencia tovarov v cenovej akcii
- Sledovanie cien pred/počas/po akcii
- Výpočet zisku pre rôzne fázy akcie
- Podklad pre tlač cenoviek

## Business pravidlá

- Pri zahájení akcie: PLS.BPrice := NewBPrice, Status := 'A' alebo 'X'
- Pri ukončení akcie: PLS.BPrice := AftBPrice, Status := 'E'
- Zisk sa prepočítava z aktuálnej nákupnej ceny
- BegDate/EndDate sa kopírujú z hlavičky ACH

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
