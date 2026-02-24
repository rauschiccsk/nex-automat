# PAB - Hlavná tabuľka partnerov

## Kľúčové slová / Aliases

PAB, PAB.BTR, partneri, dodávatelia, odberatelia, firmy, partners, suppliers, customers, zákazníci, ügyfelek, beszállítók

## Popis

Hlavná tabuľka evidencie obchodných partnerov (dodávateľov a odberateľov). Obsahuje kompletné údaje o firmách vrátane adries, bankových spojení a obchodných podmienok.

## Btrieve súbor

`PABxxxxx.BTR` (x = číslo knihy partnerov, napr. PAB00001.BTR)

## Umiestnenie

`C:\NEX\YEARACT\FIRMS\PABxxxxx.BTR`

## Štruktúra polí (98 polí)

### Identifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Číselný kód partnera - **PRIMARY KEY** |
| PaName | Str30 | 31 | Pracovný názov firmy |
| _PaName | Str30 | 31 | Vyhľadávacie pole názvu (uppercase) |
| RegName | Str60 | 61 | Registrovaný názov firmy |
| SmlName | Str10 | 11 | Skrátený názov (pre rýchle vyhľadávanie) |
| IdCode | Str20 | 21 | Identifikačný kód (zákaznícka karta) |

### Registračné údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RegIno | Str15 | 16 | IČO partnera |
| RegTin | Str15 | 16 | DIČ partnera |
| RegVin | Str15 | 16 | IČ DPH partnera |
| OldTin | Str15 | 16 | Staré DIČ |
| VatPay | byte | 1 | Platiteľ DPH (1=platiteľ) |
| OrgType | byte | 1 | Typ (0=právnická, 1=fyzická osoba) |

### Registrovaná adresa (Reg*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| RegAddr | Str30 | 31 | Ulica a číslo |
| RegSta | Str2 | 3 | Kód štátu |
| RegCty | Str3 | 4 | Kód obce |
| RegCtn | Str30 | 31 | Názov mesta |
| RegZip | Str15 | 16 | PSČ |
| RegTel | Str20 | 21 | Telefón |
| RegFax | Str20 | 21 | Fax |
| RegEml | Str30 | 31 | Email |

### Korešpondenčná adresa (Crp*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrpAddr | Str30 | 31 | Ulica a číslo |
| CrpSta | Str2 | 3 | Kód štátu |
| CrpCty | Str3 | 4 | Kód obce |
| CrpCtn | Str30 | 31 | Názov mesta |
| CrpZip | Str15 | 16 | PSČ |
| CrpTel | Str20 | 21 | Telefón |
| CrpFax | Str20 | 21 | Fax |
| CrpEml | Str30 | 31 | Email |

### Fakturačná adresa (Ivc*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| IvcAddr | Str30 | 31 | Ulica a číslo |
| IvcSta | Str2 | 3 | Kód štátu |
| IvcCty | Str3 | 4 | Kód obce |
| IvcCtn | Str30 | 31 | Názov mesta |
| IvcZip | Str15 | 16 | PSČ |
| IvcTel | Str20 | 21 | Telefón |
| IvcFax | Str20 | 21 | Fax |
| IvcEml | Str30 | 31 | Email |

### Bankové spojenie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| ContoNum | Str30 | 31 | Hlavný bankový účet |
| BankCode | Str15 | 16 | Smerový kód banky |
| BankSeat | Str30 | 31 | Sídlo banky |
| IbanCode | Str34 | 35 | IBAN |
| SwftCode | Str20 | 21 | SWIFT kód |
| ContoQnt | byte | 1 | Počet bankových účtov |

### Obchodné podmienky - Dodávateľ (Is*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| IsDscPrc | double | 8 | Zľava % od dodávateľa |
| IsExpDay | word | 2 | Splatnosť došlých faktúr (dni) |
| IsPenPrc | double | 8 | Penále % pre došlé faktúry |
| IsPayCode | Str3 | 4 | Kód formy úhrady |
| IsPayName | Str20 | 21 | Názov formy úhrady |
| IsTrsCode | Str3 | 4 | Kód spôsobu dopravy |
| IsTrsName | Str20 | 21 | Názov spôsobu dopravy |

### Obchodné podmienky - Odberateľ (Ic*)

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| IcDscPrc | double | 8 | Trvalá zľava % pre odberateľa |
| IcExpDay | word | 2 | Splatnosť odoslaných faktúr (dni) |
| IcPenPrc | double | 8 | Penále % pre odoslané faktúry |
| IcPlsNum | word | 2 | Číslo predajného cenníka |
| IcAplNum | word | 2 | Číslo akciového cenníka |
| IcPayCode | Str3 | 4 | Kód formy úhrady |
| IcPayName | Str18 | 19 | Názov formy úhrady |
| IcPayMode | byte | 1 | Predvolená forma úhrady OF |
| IcPayBrm | byte | 1 | Bezhotovostný styk (0=zakázaný, 1=povolený) |
| IcTrsCode | Str3 | 4 | Kód spôsobu dopravy |
| IcTrsName | Str20 | 21 | Názov spôsobu dopravy |
| IcSalLim | double | 8 | Nákupný limit odberateľa |
| IcFacDay | word | 2 | Factoringová splatnosť (dni) |
| IcFacPrc | double | 8 | % zvýšenie cien pri Factoringu |
| IcExpPrm | word | 2 | Povolené dni omeškania |
| SpeLev | byte | 1 | Cenová hladina pre odberateľa |
| AdvPay | double | 8 | Prečerpanie záloh (0=nedovolí, -1=nedovolí+stop, >0=limit) |

### Blokovanie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BuDisStat | byte | 1 | Blokovanie nákupu (1=blokovaný) |
| BuDisDate | DateType | 4 | Dátum zablokovania nákupu |
| BuDisUser | Str8 | 9 | Používateľ, ktorý zablokoval |
| BuDisDesc | Str30 | 31 | Dôvod blokovania nákupu |
| SaDisStat | byte | 1 | Blokovanie predaja (1=blokovaný) |
| SaDisDate | DateType | 4 | Dátum zablokovania predaja |
| SaDisUser | Str8 | 9 | Používateľ, ktorý zablokoval |
| SaDisDesc | Str20 | 21 | Dôvod blokovania predaja |

### Klasifikácia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| SapType | byte | 1 | Je dodávateľ (1=áno) |
| CusType | byte | 1 | Je odberateľ (1=áno) |
| PagCode | word | 2 | Kód skupiny dodávateľov |
| PgcCode | word | 2 | Kód skupiny odberateľov |
| DlrCode | word | 2 | Kód obchodného zástupcu |
| OwnPac | longint | 4 | Kód vlastníckej firmy |
| BonClc | byte | 1 | Počítanie bonusov (1=zapnuté) |
| TrdType | byte | 1 | Forma obchodovania (1=MO, 2=VO, 3=oboje) |
| PasQnt | word | 2 | Počet prevádzok partnera |

### Ostatné

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| WebSite | Str30 | 31 | Webová stránka |
| HedName | Str30 | 31 | Meno majiteľa/konateľa |
| RegRec | Str60 | 61 | Záznam v obchodnom registri |
| SrCode | Str15 | 16 | Číslo povolenia na predaj liehovín |
| PrnLng | Str2 | 3 | Jazyk tlačových zostáv |

### Audit polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Poradové číslo modifikácie |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy (14)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | PaCode | PaCode | Duplicit |
| 1 | RegIno | RegIno | Duplicit |
| 2 | RegTin | RegTin | Duplicit |
| 3 | _PaName | PaName | Case-insensitive, Duplicit |
| 4 | SmlName | SmlName | Duplicit |
| 5 | ContoNum | ContoNum | Duplicit |
| 6 | IdCode | IdCode | Case-insensitive, Duplicit |
| 7 | RegSta | RegSta | Case-insensitive, Duplicit |
| 8 | RegCty | RegCty | Case-insensitive, Duplicit |
| 9 | PagCode | PagCode | Duplicit |
| 10 | PgcCode | PgcCode | Duplicit |
| 11 | DlrCode | DlrCode | Duplicit |
| 12 | OwnPac | OwnPac | Duplicit |
| 13 | BonClc | BonClc | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| RegSta | STALST.StaCode | Štát registrovanej adresy |
| RegCty | CTYLST.CtyCode | Mesto registrovanej adresy |
| CrpSta | STALST.StaCode | Štát korešpondenčnej adresy |
| CrpCty | CTYLST.CtyCode | Mesto korešpondenčnej adresy |
| IvcSta | STALST.StaCode | Štát fakturačnej adresy |
| IvcCty | CTYLST.CtyCode | Mesto fakturačnej adresy |
| IsPayCode | PAYLST.PayCode | Forma úhrady (dodávateľ) |
| IsTrsCode | TRSLST.TrsCode | Spôsob dopravy (dodávateľ) |
| IcPayCode | PAYLST.PayCode | Forma úhrady (odberateľ) |
| IcTrsCode | TRSLST.TrsCode | Spôsob dopravy (odberateľ) |
| PagCode | PAGLST.PagCode | Skupina dodávateľov |
| PgcCode | PAGLST.PagCode | Skupina odberateľov |
| BankCode | BANKLST.BankCode | Banka |

## Súvisiace tabuľky

| Tabuľka | Relácia | Popis |
|---------|---------|-------|
| PABACC | PaCode → PaCode | Bankové účty partnera |
| PACNTC | PaCode → PaCode | Kontaktné osoby |
| PASUBC | PaCode → PaCode | Prevádzkové jednotky |
| PANOTI | PaCode → PaCode | Poznámky |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
