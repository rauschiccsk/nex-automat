# ANDROS RDS Licensing - Riešenie

**Zákazník:** ANDROS s.r.o.  
**Server:** Dell PowerEdge R740XD / Windows Server 2025 Standard  
**Hostname:** WIN-MGUUCR7DM2K  
**Dátum riešenia:** 2025-01-22

---

## Problém

Windows Server 2025 zobrazoval trial countdown a "No Remote Desktop license server is specified" (112 dní grace period), aj keď:
- Windows Server 2025 Standard bol aktivovaný
- RDS License Server bol aktivovaný
- 50 Device CAL licencie boli nainštalované

## Príčina

RD Session Host nevedel kde je License Server:
- `LicensingMode = 5` (Not Configured) namiesto 2 (Per Device)
- `LicenseServers` bol prázdny
- Pôvodne bol použitý nesprávny hostname `WIN-MGUUCR7D` namiesto `WIN-MGUUCR7DM2K`

## Riešenie

### 1. Overiť Windows aktiváciu
```cmd
slmgr /xpr
```
Výsledok: "The machine is permanently activated" ✓

### 2. Nakonfigurovať Session Host cez WMI
```powershell
$obj = Get-WmiObject -Namespace "root/cimv2/TerminalServices" -Class Win32_TerminalServiceSetting
$obj.SetSpecifiedLicenseServerList("WIN-MGUUCR7DM2K")
$obj.ChangeMode(2)
```

### 3. Nakonfigurovať cez Group Policy (gpedit.msc)
Cesta: Computer Configuration → Administrative Templates → Windows Components → Remote Desktop Services → Remote Desktop Session Host → Licensing

Nastavenia:
- **Use the specified Remote Desktop license servers** = Enabled, hodnota: `WIN-MGUUCR7DM2K`
- **Set the Remote Desktop licensing mode** = Enabled, hodnota: `Per Device`

### 4. Aplikovať zmeny
```powershell
gpupdate /force
Restart-Service -Name "TermService" -Force
```

### 5. Overiť konfiguráciu
```powershell
$obj = Get-WmiObject -Namespace "root/cimv2/TerminalServices" -Class Win32_TerminalServiceSetting
$obj.GetSpecifiedLicenseServerList()  # Očakávané: {WIN-MGUUCR7DM2K}
$obj.LicensingType                     # Očakávané: 2 (Per Device)
```

## Verifikácia

RD Licensing Diagnoser (lsdiag.msc) zobrazuje:
- ✅ Zelený status - žiadne problémy
- ✅ 49 licencií dostupných
- ✅ Licensing mode: Per Device
- ✅ License server: win-mguucr7dm2k - Available

## Diagnostické príkazy

```powershell
# Windows aktivácia
slmgr /xpr
slmgr /dlv

# RDS role status
Get-WindowsFeature -Name RDS* | Select-Object Name, InstallState

# License Server konfigurácia
Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\RCM\Licensing Core" | Select-Object LicensingMode, LicenseServers

# RD Licensing Manager
licmgr.exe

# RD Licensing Diagnoser
lsdiag.msc
```

## Licenčné informácie

- **Windows Server 2025 Standard:** KFYKN-WXVPX-8HDVJ-TMPPD-979YB
- **RDS CAL:** 50 Device CAL (Retail Purchase, Never expires)

## Dodatočné opravy Event Log chýb

### CertEnroll Error (ID 86) - SCEP Azure Attestation
Server sa snažil pripojiť k microsoftaik.azure.net (TPM attestation) bez Azure integrácie.

**Riešenie:**
```powershell
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WorkplaceJoin" -Name "autoWorkplaceJoin" -Value 0 -Type DWord -Force
```

### Security-SPP Error (ID 16398) - Grace Period Timer
Po konverzii z Evaluation zostal grace timer v registry.

**Riešenie:**
1. V regedit navigovať na: `HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\RCM\GracePeriod`
2. Pravý klik → Permissions → Advanced → Change Owner na Administrators
3. Dať Administrators Full Control
4. Vymazať GracePeriod key
5. Reštartovať TermService

## Poznámky

- Pri štarte servera sa môže na niekoľko sekúnd zobraziť "No Remote Desktop license server is specified" - toto je normálne počas inicializácie služieb
- LicensingMode hodnoty: 2 = Per Device, 4 = Per User, 5 = Not Configured
- Hostname musí presne zodpovedať - WIN-MGUUCR7DM2K (nie WIN-MGUUCR7D)