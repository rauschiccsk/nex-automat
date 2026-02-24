# SYSTEM - Systémové údaje firmy

## Kľúčové slová / Aliases

SYSTEM, SYSTEM.BTR, systémové nastavenia, system settings, konfigurácia

## Popis

Tabuľka systémových údajov používateľskej firmy. Obsahuje základné identifikačné údaje, kontaktné informácie a globálne nastavenia systému. Globálny súbor - jeden záznam.

## Btrieve súbor

`SYSTEM.BTR`

## Umiestnenie

`C:\NEX\SYSTEM\SYSTEM.BTR`

## Štruktúra polí (32 polí)

### Identifikácia firmy

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| MyPaIno | Str15 | 16 | IČO používateľskej firmy |
| MyPaTin | Str15 | 16 | DIČ používateľskej firmy |
| MyPaVin | Str15 | 16 | IČ DPH používateľskej firmy |
| MyOldTin | Str15 | 16 | Starý DIČ (pre historické účely) |
| MyPaName | Str60 | 61 | Názov používateľskej firmy |

### Adresa sídla

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| MyPaAddr | Str30 | 31 | Registrovaná adresa firmy |
| MyStaCode | Str2 | 3 | Kód štátu sídla (SK, CZ, ...) |
| MyStaName | Str30 | 31 | Názov štátu sídla |
| MyCtyCode | Str3 | 4 | Kód obce sídla |
| MyCtyName | Str30 | 31 | Názov obce sídla |
| MyZipCode | Str10 | 11 | PSČ sídla |

### Kontaktné údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| MyWebSite | Str30 | 31 | Webová stránka firmy |
| MyTelNum | Str20 | 21 | Telefónne číslo firmy |
| MyFaxNum | Str20 | 21 | Faxové číslo firmy |
| MyEmail | Str30 | 31 | Elektronická adresa firmy |

### Bankové údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| MyBaConto | Str30 | 31 | Číslo predvoleného bankového účtu |
| MyBaName | Str30 | 31 | Názov banky |
| MyBaCity | Str30 | 31 | Sídlo banky |
| MyBaStat | Str30 | 31 | Štát banky |

### Prevádzkové údaje

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| MyWriNum | word | 2 | Číslo prevádzkovej jednotky |
| Register | Str90 | 91 | Záznam v obchodnom registri |

### Nastavenia systému

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| BegGsCode | longint | 4 | Počiatočné číslo tovaru v evidencii |
| EndGsCode | longint | 4 | Konečné číslo tovaru v evidencii |
| BegPaCode | longint | 4 | Počiatočné číslo partnera v evidencii |
| EndPaCode | longint | 4 | Konečné číslo partnera v evidencii |

### Internetové pripojenie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| DialHost | Str30 | 31 | Názov internetového pripojenia |
| DialUser | Str15 | 16 | Meno používateľa pre internet |
| DialPasw | Str15 | 16 | Heslo pre internet |

### FTP pripojenie

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| FtpHost | Str30 | 31 | Názov FTP servera |
| FtpUser | Str15 | 16 | Meno používateľa pre FTP |
| FtpPasw | Str15 | 16 | Heslo pre FTP |

## Indexy (1)

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | MyPaIno | MyPaIno | Duplicit, Case-insensitive |

## Príklad

```
MyPaIno   = "12345678"
MyPaTin   = "2023456789"
MyPaVin   = "SK2023456789"
MyPaName  = "ABC s.r.o."
MyPaAddr  = "Hlavná 123"
MyStaCode = "SK"
MyStaName = "Slovensko"
MyCtyCode = "BA1"
MyCtyName = "Bratislava"
MyZipCode = "81101"
MyTelNum  = "+421 2 12345678"
MyEmail   = "info@abc.sk"
MyWebSite = "www.abc.sk"
Register  = "Obchodný register Okresného súdu Bratislava I, oddiel: Sro, vložka č. 12345/B"
─────────────────────────────────────────────────────────────────
MyBaConto = "SK12 1100 0000 0012 3456 7890"
MyBaName  = "Tatra banka, a.s."
MyBaCity  = "Bratislava"
─────────────────────────────────────────────────────────────────
BegGsCode = 1
EndGsCode = 999999
BegPaCode = 1
EndPaCode = 99999
MyWriNum  = 1
```

## Použitie

- Hlavička tlačových zostáv a dokladov
- Identifikácia firmy v e-faktúrach
- Automatické vyplnenie údajov dodávateľa
- Nastavenie rozsahov číselníkov
- FTP prenos dát medzi prevádzkami

## Business pravidlá

- Tabuľka obsahuje vždy len jeden záznam
- MyPaIno musí byť platné IČO
- MyPaVin sa validuje proti formátu IČ DPH
- BegGsCode < EndGsCode
- BegPaCode < EndPaCode

## Načítanie do gvSys

```pascal
procedure LoadSystemData;
begin
  If dmSYS.btSYSTEM.RecordCount > 0 then begin
    dmSYS.btSYSTEM.First;
    gvSys.FirmaName := dmSYS.btSYSTEM.FieldByName('MyPaName').AsString;
    gvSys.WriNum := dmSYS.btSYSTEM.FieldByName('MyWriNum').AsInteger;
    gvSys.BegGsCode := dmSYS.btSYSTEM.FieldByName('BegGsCode').AsInteger;
    gvSys.EndGsCode := dmSYS.btSYSTEM.FieldByName('EndGsCode').AsInteger;
    gvSys.BegPaCode := dmSYS.btSYSTEM.FieldByName('BegPaCode').AsInteger;
    gvSys.EndPaCode := dmSYS.btSYSTEM.FieldByName('EndPaCode').AsInteger;
  end;
end;
```

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model (tenant settings)
- [ ] API endpoint
