# Príručka konfigurácie Windows Server 2025

**Pre slovenských používateľov a Delphi 6 aplikácie**

---

Táto príručka popisuje krok za krokom konfiguráciu Windows Server 2025 pre slovenských používateľov s obmedzeniami prístupu k súborovému systému. Obsahuje aj špecifické nastavenia pre aplikácie vytvorené v Delphi 6 a NEX Genesis ERP.

---

## 1. Vytvorenie používateľskej skupiny

Skupina slúži na centralizovanú správu oprávnení pre viacerých používateľov.

### 1.1 Manuálny postup

1. Otvorte **Computer Management** (Správa počítača) - pravý klik na tlačidlo Start alebo Win+X
2. Navigujte na **Local Users and Groups** (Lokálni používatelia a skupiny) → **Groups** (Skupiny)
3. Pravý klik → **New Group...** (Nová skupina)
4. Zadajte názov skupiny, napr. "**_Andros users_**"
5. Kliknite na **Create** (Vytvoriť)

---

## 2. Nastavenie obmedzení prístupu ku adresárom

Cieľom je zakázať skupine prístup k citlivým adresárom, pričom ostatné adresáre zostanú prístupné.

### 2.1 Zakázanie prístupu k citlivým adresárom

Pre každý citlivý adresár (napr. C:\Confidential, C:\Admin, atď.), ku ktorému chcete zakázať prístup, postupujte nasledovne:

1. Otvorte **File Explorer** (Prieskumník)
2. Pravý klik na citlivý adresár (napr. `C:\Confidential`) → **Properties** (Vlastnosti) → **Security** (Zabezpečenie) → **Advanced** (Rozšírené)
3. Kliknite na **Add** (Pridať) → **Select a principal** (Vybrať principal)
4. Zadajte názov skupiny (napr. "Andros users")
5. **Type** (Typ): **Deny** (Odmietnuť)
6. **Applies to** (Vzťahuje sa na): **This folder, subfolders and files** (Tento priečinok, podpriečinky a súbory)
7. Začiarknite všetky oprávnenia (Full control)
8. Kliknite na **OK** → **Apply** (Použiť) → **OK**

### 2.2 Povolenie prístupu k vlastnému profilu používateľa

Každý používateľ musí mať plný prístup k svojmu vlastnému adresáru `C:\Users\[username]`:

1. Pravý klik na `C:\Users\[meno_pouzivatela]` → **Properties** → **Security** → **Edit** (Upraviť)
2. Kliknite na **Add** (Pridať) → zadajte meno používateľa
3. Povoľte oprávnenia: **Modify, Read & Execute, List folder contents, Read, Write**

### 2.3 Poznámky k prístupu

- Skupina má predvolený prístup ku všetkým adresárom na C:, okrem tých, kde je nastavený **Deny**
- Systémové adresáre (C:\Windows, C:\Program Files, atď.) sú prístupné automaticky
- Deny oprávnenie má prednosť pred Allow - je najsilnejšie obmedzenie

---

## 3. Vytvorenie nového používateľa

### 3.1 Manuálny postup

1. Otvorte **Computer Management** → **Local Users and Groups** → **Users** (Používatelia)
2. Pravý klik → **New User...** (Nový používateľ)
3. Vyplňte používateľské meno a heslo
4. Kliknite na **Create** (Vytvoriť)
5. Otvorte **Local Users and Groups** → **Users**
6. Dvojitým kliknutím otvorte vytvorený používateľský účet
7. Prejdite na záložku **Member Of** (Člen skupín)
8. Kliknite na **Add...** (Pridať) → zadajte "Andros users" → **OK**
9. Odstráňte skupinu "Users" (voliteľné, ak chcete úplné obmedzenie)

---

## 4. Nastavenie slovenského jazyka

### 4.1 Manuálny postup

1. Prihláste sa ako vytvorený používateľ
2. Otvorte **Settings** (Nastavenia) → **Time & Language** (Čas a jazyk) → **Language & region** (Jazyk a oblasť)
3. Kliknite na **Add a language** (Pridať jazyk)
4. Vyhľadajte a vyberte **Slovak (slovenčina)**
5. Kliknite na tlačidlo s tromi bodkami (...) vedľa slovenčiny
6. Vyberte **Set as default** (Nastaviť ako predvolené)
7. Odhláste sa a znovu sa prihláste

#### Úprava formátu dátumu

1. Otvorte **Control Panel** (Ovládací panel) → **Clock and Region** (Hodiny a oblasť) → **Region** (Oblasť)
2. Kliknite na **Additional settings...** (Ďalšie nastavenia)
3. V záložke **Date** (Dátum) zmeňte **Short date** (Krátky dátum) na: `dd.MM.yyyy`
4. Kliknite na **OK**

### 4.2 Automatizovaný postup (PowerShell)

Vytvorte súbor `setup_slovak.bat` s nasledujúcim obsahom:

```batch
@echo off
echo Nastavuje sa slovenský jazyk a formát dátumu...
powershell.exe -ExecutionPolicy Bypass -Command "Set-WinUserLanguageList -LanguageList sk-SK -Force; Set-Culture -CultureInfo sk-SK"
reg add "HKCU\Control Panel\International" /v sShortDate /t REG_SZ /d "dd.MM.yyyy" /f
echo Hotovo. Odhláste sa a znovu sa prihláste pre aplikovanie zmien.
pause
```

Spustite tento súbor ako používateľ (nie ako administrátor). Po dokončení sa odhláste a znovu prihláste.

---

## 5. Nastavenie formátu čísiel (NOVÉ)

Pre správne zobrazovanie finančných hodnôt v NEX Genesis a Delphi aplikáciách.

### 5.1 Slovenský formát

| Položka | Hodnota | Príklad |
|---------|---------|---------|
| Desatinný oddeľovač | `,` (čiarka) | 1234,56 |
| Oddeľovač tisícov | ` ` (medzera) | 1 234 567 |
| Symbol meny | `€` | 1 234,56 € |
| Záporné číslo | `-1 234,56` | |

### 5.2 Manuálny postup

1. Otvorte **Control Panel** → **Clock and Region** → **Region**
2. Kliknite na **Additional settings...** (Ďalšie nastavenia)
3. V záložke **Numbers** (Čísla):
   - **Decimal symbol** (Desatinný symbol): `,`
   - **Digit grouping symbol** (Symbol zoskupovania číslic): ` ` (medzera)
   - **Negative number format** (Formát záporného čísla): `-1,1`
4. V záložke **Currency** (Mena):
   - **Currency symbol** (Symbol meny): `€`
   - **Positive currency format**: `1,1 €`
   - **Negative currency format**: `-1,1 €`
5. Kliknite na **OK**

### 5.3 Automatizovaný postup

Pridajte do `setup_slovak.bat`:

```batch
rem Formát čísiel
reg add "HKCU\Control Panel\International" /v sDecimal /t REG_SZ /d "," /f
reg add "HKCU\Control Panel\International" /v sThousand /t REG_SZ /d " " /f
reg add "HKCU\Control Panel\International" /v sCurrency /t REG_SZ /d "€" /f
reg add "HKCU\Control Panel\International" /v iCurrDigits /t REG_SZ /d "2" /f
```

---

## 6. Nastavenie klávesnice (NOVÉ)

### 6.1 Pridanie slovenskej klávesnice

1. Otvorte **Settings** → **Time & Language** → **Language & region**
2. Kliknite na **Slovak (slovenčina)** → **...** → **Language options**
3. V sekcii **Keyboards** kliknite na **Add a keyboard**
4. Vyberte **Slovak (QWERTZ)**
5. Voliteľne odstráňte **Slovak (QWERTY)** ak preferujete len QWERTZ

### 6.2 Automatizovaný postup (PowerShell)

```powershell
# Pridanie slovenskej QWERTZ klávesnice
$LangList = Get-WinUserLanguageList
$LangList.Add("sk-SK")
Set-WinUserLanguageList $LangList -Force

# Nastavenie QWERTZ ako predvolenej pre slovenčinu
Set-WinDefaultInputMethodOverride -InputTip "041B:0000041B"
```

### 6.3 Prepínanie klávesníc

- **Win + Space** - prepnutie medzi jazykmi
- **Alt + Shift** - alternatívne prepnutie
- Ikona klávesnice v systémovej lište zobrazuje aktuálny jazyk

---

## 7. Nastavenie časovej zóny

### 7.1 Manuálny postup

1. Otvorte **Settings** → **Time & Language** → **Date & time** (Dátum a čas)
2. V **Time zone** (Časové pásmo) vyberte: **(UTC+01:00) Bratislava, Budapest, Ljubljana, Prague, Warsaw**

### 7.2 Automatizovaný postup

Vytvorte súbor `set_timezone.bat` s obsahom:

```batch
@echo off
echo Nastavuje sa časová zóna...
powershell.exe -ExecutionPolicy Bypass -Command "Set-TimeZone -Id 'Central Europe Standard Time'"
echo Časová zóna nastavená na Central Europe (UTC+01:00).
pause
```

---

## 8. Nastavenie System Locale (KRITICKÉ pre Delphi 6)

**Toto nastavenie je nevyhnutné pre správne zobrazovanie slovenských diakritických znakov (ť, č, ľ, ň, atď.) v aplikáciách vytvorených v Delphi 6.**

### 8.1 Manuálny postup

1. Otvorte **Control Panel** → **Clock and Region** → **Region**
2. Kliknite na záložku **Administrative** (Správa)
3. Kliknite na **Change system locale...** (Zmeniť miestne nastavenie systému)
4. Vyberte **Slovak (Slovakia)**
5. **DÔLEŽITÉ:** _**NEZAŠKRTÁVAJTE**_ voľbu "Beta: Use Unicode UTF-8 for worldwide language support"
6. Kliknite na **OK**
7. **Reštartujte počítač (vyžaduje sa!)**

### 8.2 Overenie nastavenia

Po reštarte overte, že Code Page je nastavený na 1250:

```cmd
reg query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Nls\CodePage" /v ACP
```

Výsledok by mal byť: `ACP    REG_SZ    1250`

### 8.3 Automatizovaný postup

Vytvorte súbor `set_system_locale.bat` s obsahom (vyžaduje spustenie ako administrátor):

```batch
@echo off
echo Nastavuje sa System Locale na Slovak...
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Nls\CodePage" /v ACP /t REG_SZ /d "1250" /f
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Nls\CodePage" /v OEMCP /t REG_SZ /d "852" /f
powershell.exe -ExecutionPolicy Bypass -Command "Set-WinSystemLocale -SystemLocale sk-SK"
echo System Locale nastavený. REŠTART POČÍTAČA JE POVINNÝ!
echo Stlačte ľubovoľnú klávesu pre reštart alebo zatvorte toto okno pre manuálny reštart.
pause
shutdown /r /t 10
```

---

## 9. Konfigurácia pre NEX Genesis (NOVÉ)

### 9.1 Adresárová štruktúra

```
C:\NEX\                             # Hlavný adresár NEX
    ├── IMPORT\SUPPLIER-INVOICES\   # Prijaté PDF faktúry
    ├── IMPORT\SUPPLIER-STAGING\    # Staging pre spracovanie
    ├── IMPORT\SUPPLIER-ARCHIVE\    # Archív spracovaných
    └── YEARACT\STORES\             # Btrieve dátové súbory
```

### 9.2 Oprávnenia pre NEX adresáre

Skupina "Andros users" potrebuje:

| Adresár | Oprávnenie |
|---------|------------|
| `C:\NEX` | Read & Execute |
| `C:\NEX\IMPORT` | Modify (zápis faktúr) |
| `C:\NEX\YEARACT` | Modify (Btrieve prístup) |

### 9.3 Pervasive PSQL (Btrieve) nastavenia

1. Nainštalujte **Pervasive PSQL v11** alebo novší
2. Overte, že služba **Pervasive.SQL** beží:
   ```cmd
   sc query "Pervasive.SQL (relational)"
   ```
3. Nastavte prístup k databázovým súborom:
   - `C:\NEX\YEARACT\STORES\*.BTR` - dátové súbory
   - `C:\NEX\YEARACT\STORES\*.MK?` - indexové súbory

### 9.4 Delphi 6 runtime knižnice

Overte prítomnosť týchto súborov v `C:\Windows\System32` (32-bit) alebo `C:\Windows\SysWOW64` (64-bit OS):

| Súbor | Účel |
|-------|------|
| `borlndmm.dll` | Borland Memory Manager |
| `cc3260mt.dll` | C++ Runtime |
| `vcl60.bpl` | VCL Package |
| `rtl60.bpl` | RTL Package |

---

## 10. RDS Session Host konfigurácia (NOVÉ)

Pre multi-user prístup cez Remote Desktop.

### 10.1 Overenie RDS licencie

```powershell
# Kontrola RDS licenčného servera
Get-RDLicenseConfiguration
```

### 10.2 Nastavenie profilu pre nových používateľov

Aby mal každý nový RDS používateľ slovenské nastavenia:

1. Prihláste sa ako administrátor
2. Nakonfigurujte slovenské nastavenia podľa sekcií 4-8
3. Otvorte **Control Panel** → **Region** → záložka **Administrative**
4. Kliknite na **Copy settings...** (Kopírovať nastavenia)
5. Zaškrtnite:
   - **Welcome screen and system accounts**
   - **New user accounts**
6. Kliknite **OK** a reštartujte

### 10.3 Group Policy pre RDS používateľov (voliteľné)

Vytvorte GPO pre automatické nastavenia:

```powershell
# Nastavenie default locale pre nových používateľov
New-GPO -Name "Slovak Locale Settings"
Set-GPRegistryValue -Name "Slovak Locale Settings" `
    -Key "HKCU\Control Panel\International" `
    -ValueName "LocaleName" -Type String -Value "sk-SK"
```

---

## 11. Kompletný setup script (NOVÉ)

Všetky nastavenia v jednom skripte:

### 11.1 Pre administrátora (globálne nastavenia)

Súbor: `setup_admin.bat` (spustiť ako Administrator)

```batch
@echo off
echo ========================================
echo Windows Server 2025 - Slovak Setup
echo Pre NEX Genesis a Delphi 6 aplikacie
echo ========================================
echo.

echo [1/3] Nastavujem System Locale na Slovak...
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Nls\CodePage" /v ACP /t REG_SZ /d "1250" /f
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Nls\CodePage" /v OEMCP /t REG_SZ /d "852" /f
powershell.exe -ExecutionPolicy Bypass -Command "Set-WinSystemLocale -SystemLocale sk-SK"

echo [2/3] Nastavujem casovu zonu...
powershell.exe -ExecutionPolicy Bypass -Command "Set-TimeZone -Id 'Central Europe Standard Time'"

echo [3/3] Nastavujem default pre novych pouzivatelov...
reg add "HKEY_USERS\.DEFAULT\Control Panel\International" /v LocaleName /t REG_SZ /d "sk-SK" /f
reg add "HKEY_USERS\.DEFAULT\Control Panel\International" /v sShortDate /t REG_SZ /d "dd.MM.yyyy" /f
reg add "HKEY_USERS\.DEFAULT\Control Panel\International" /v sDecimal /t REG_SZ /d "," /f
reg add "HKEY_USERS\.DEFAULT\Control Panel\International" /v sThousand /t REG_SZ /d " " /f

echo.
echo ========================================
echo HOTOVO! RESTARTUJTE SERVER!
echo ========================================
pause
shutdown /r /t 30
```

### 11.2 Pre používateľa (používateľské nastavenia)

Súbor: `setup_user.bat` (spustiť ako bežný používateľ)

```batch
@echo off
echo ========================================
echo Nastavenia pre pouzivatela
echo ========================================
echo.

echo [1/4] Slovensky jazyk...
powershell.exe -ExecutionPolicy Bypass -Command "Set-WinUserLanguageList -LanguageList sk-SK -Force"
powershell.exe -ExecutionPolicy Bypass -Command "Set-Culture -CultureInfo sk-SK"

echo [2/4] Format datumu...
reg add "HKCU\Control Panel\International" /v sShortDate /t REG_SZ /d "dd.MM.yyyy" /f
reg add "HKCU\Control Panel\International" /v sLongDate /t REG_SZ /d "d. MMMM yyyy" /f

echo [3/4] Format cisiel...
reg add "HKCU\Control Panel\International" /v sDecimal /t REG_SZ /d "," /f
reg add "HKCU\Control Panel\International" /v sThousand /t REG_SZ /d " " /f
reg add "HKCU\Control Panel\International" /v sCurrency /t REG_SZ /d "€" /f

echo [4/4] Klavesnica...
powershell.exe -ExecutionPolicy Bypass -Command "Set-WinDefaultInputMethodOverride -InputTip '041B:0000041B'"

echo.
echo ========================================
echo HOTOVO! Odhlaste sa a znovu prihlaste.
echo ========================================
pause
```

---

## Dôležité poznámky

- System Locale je **_globálne nastavenie_** - platí pre všetkých používateľov servera
- Jazykové nastavenia (Settings → Language) sú používateľsky špecifické a je potrebné ich nastaviť pre každého používateľa samostatne
- Po zmene System Locale je reštart servera povinný
- Code Page 1250 je nevyhnutný pre správne fungovanie Delphi 6 aplikácií so slovenskými znakmi
- Pri pridávaní nových používateľov do skupiny "Andros users" nezabudnite spustiť pre nich `setup_user.bat`
- Pre správne zobrazovanie menu v Delphi 6 aplikáciách pridajte do inicializácie programu: `Screen.MenuFont.Charset := EASTEUROPE_CHARSET;`
- **UTF-8 Beta NIKDY nezapínať** - rozbije Delphi 6 a Btrieve aplikácie

---

## Kontrolný zoznam po inštalácii

| Položka | Príkaz na overenie | Očakávaná hodnota |
|---------|-------------------|-------------------|
| Code Page | `chcp` | 852 |
| ACP Registry | `reg query "HKLM\...\CodePage" /v ACP` | 1250 |
| Časová zóna | `tzutil /g` | Central Europe Standard Time |
| Locale | `Get-Culture` | sk-SK |
| Klávesnica | `Get-WinUserLanguageList` | sk-SK |

---

_Koniec príručky_

Verzia dokumentu: 1.2  
Dátum vytvorenia: 19. január 2025  
Posledná aktualizácia: 20. január 2026  
Autor: ICC s.r.o.