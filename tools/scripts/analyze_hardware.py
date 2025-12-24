"""
Hardware Analyzer pre Windows Server
Kompletná analýza všetkých hardwarových komponentov.

Spustenie: python analyze_hardware.py
Pre vzdialený server: python analyze_hardware.py --remote SERVERNAME
"""

import subprocess
import argparse
from datetime import datetime


def run_powershell(script: str, remote_server: str = None) -> str:
    """Spustí PowerShell príkaz lokálne alebo vzdialene."""
    if remote_server:
        script = f"Invoke-Command -ComputerName {remote_server} -ScriptBlock {{ {script} }}"

    cmd = ["powershell", "-NoProfile", "-Command", script]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, encoding='utf-8', errors='replace')
        if result.returncode != 0 and result.stderr:
            return f"ERROR: {result.stderr}"
        return result.stdout
    except subprocess.TimeoutExpired:
        return "ERROR: Timeout pri pripojení"
    except Exception as e:
        return f"ERROR: {e}"


def section_header(title: str) -> str:
    return f"\n{'=' * 70}\n  {title}\n{'=' * 70}"


def parse_output(result: str) -> dict:
    """Parsuje key=value výstup."""
    data = {}
    for line in result.split('\n'):
        line = line.strip()
        if '=' in line:
            key, value = line.split('=', 1)
            data[key.strip()] = value.strip()
    return data


def get_system_info(remote: str = None) -> list:
    """Základné systémové informácie."""
    lines = [section_header("SYSTÉM")]

    ps = """
$cs = Get-CimInstance Win32_ComputerSystem
$bios = Get-CimInstance Win32_BIOS
$os = Get-CimInstance Win32_OperatingSystem
Write-Output "Manufacturer=$($cs.Manufacturer)"
Write-Output "Model=$($cs.Model)"
Write-Output "SystemType=$($cs.SystemType)"
Write-Output "Domain=$($cs.Domain)"
Write-Output "BIOSVersion=$($bios.SMBIOSBIOSVersion)"
Write-Output "BIOSDate=$($bios.ReleaseDate)"
Write-Output "SerialNumber=$($bios.SerialNumber)"
Write-Output "OSName=$($os.Caption)"
Write-Output "OSVersion=$($os.Version)"
Write-Output "OSBuild=$($os.BuildNumber)"
Write-Output "InstallDate=$($os.InstallDate)"
Write-Output "LastBoot=$($os.LastBootUpTime)"
"""
    data = parse_output(run_powershell(ps, remote))

    lines.append(f"  Výrobca:        {data.get('Manufacturer', 'N/A')}")
    lines.append(f"  Model:          {data.get('Model', 'N/A')}")
    lines.append(f"  Typ:            {data.get('SystemType', 'N/A')}")
    lines.append(f"  Doména:         {data.get('Domain', 'N/A')}")
    lines.append(f"  Sériové číslo:  {data.get('SerialNumber', 'N/A')}")
    lines.append(f"  BIOS:           {data.get('BIOSVersion', 'N/A')}")
    lines.append("")
    lines.append(f"  OS:             {data.get('OSName', 'N/A')}")
    lines.append(f"  Verzia:         {data.get('OSVersion', 'N/A')} (Build {data.get('OSBuild', 'N/A')})")
    lines.append(f"  Posledný boot:  {data.get('LastBoot', 'N/A')[:19] if data.get('LastBoot') else 'N/A'}")

    return lines


def get_cpu_info(remote: str = None) -> list:
    """Informácie o procesoroch."""
    lines = [section_header("PROCESOR (CPU)")]

    ps = """
$cpus = Get-CimInstance Win32_Processor
$i = 0
foreach ($cpu in $cpus) {
    $i++
    Write-Output "CPU_START"
    Write-Output "Num=$i"
    Write-Output "Name=$($cpu.Name)"
    Write-Output "Manufacturer=$($cpu.Manufacturer)"
    Write-Output "Cores=$($cpu.NumberOfCores)"
    Write-Output "LogicalProcessors=$($cpu.NumberOfLogicalProcessors)"
    Write-Output "MaxClockSpeed=$($cpu.MaxClockSpeed)"
    Write-Output "CurrentClockSpeed=$($cpu.CurrentClockSpeed)"
    Write-Output "L2CacheSize=$($cpu.L2CacheSize)"
    Write-Output "L3CacheSize=$($cpu.L3CacheSize)"
    Write-Output "Socket=$($cpu.SocketDesignation)"
    Write-Output "Status=$($cpu.Status)"
    Write-Output "LoadPercentage=$($cpu.LoadPercentage)"
    Write-Output "CPU_END"
}
"""
    result = run_powershell(ps, remote)
    current = {}

    for line in result.split('\n'):
        line = line.strip()
        if line == "CPU_START":
            current = {}
        elif line == "CPU_END" and current:
            lines.append(f"\n  CPU #{current.get('Num', '?')}:")
            lines.append(f"    Názov:          {current.get('Name', 'N/A')}")
            lines.append(f"    Socket:         {current.get('Socket', 'N/A')}")
            lines.append(f"    Jadrá:          {current.get('Cores', 'N/A')}")
            lines.append(f"    Logické proc.:  {current.get('LogicalProcessors', 'N/A')}")
            lines.append(f"    Max frekvencia: {current.get('MaxClockSpeed', 'N/A')} MHz")
            lines.append(f"    Akt. frekvencia:{current.get('CurrentClockSpeed', 'N/A')} MHz")
            lines.append(f"    L2 Cache:       {current.get('L2CacheSize', 'N/A')} KB")
            lines.append(f"    L3 Cache:       {current.get('L3CacheSize', 'N/A')} KB")
            lines.append(f"    Využitie:       {current.get('LoadPercentage', 'N/A')}%")
            current = {}
        elif '=' in line:
            k, v = line.split('=', 1)
            current[k] = v

    return lines


def get_memory_info(remote: str = None) -> list:
    """Informácie o pamäti."""
    lines = [section_header("PAMÄŤ (RAM)")]

    # Sumár
    ps = """
$arr = Get-CimInstance Win32_PhysicalMemoryArray
$mods = Get-CimInstance Win32_PhysicalMemory
$os = Get-CimInstance Win32_OperatingSystem
$total = ($mods | Measure-Object -Property Capacity -Sum).Sum
Write-Output "MaxCapacity=$($arr.MaxCapacity)"
Write-Output "TotalSlots=$($arr.MemoryDevices)"
Write-Output "UsedSlots=$($mods.Count)"
Write-Output "TotalInstalled=$total"
Write-Output "TotalVisible=$($os.TotalVisibleMemorySize)"
Write-Output "FreePhysical=$($os.FreePhysicalMemory)"
"""
    data = parse_output(run_powershell(ps, remote))

    try:
        max_gb = int(data.get('MaxCapacity', 0)) / (1024 ** 2)
        total_gb = int(data.get('TotalInstalled', 0)) / (1024 ** 3)
        visible_kb = int(data.get('TotalVisible', 0))
        free_kb = int(data.get('FreePhysical', 0))
        used_kb = visible_kb - free_kb
        usage_pct = (used_kb / visible_kb * 100) if visible_kb else 0

        lines.append(f"  Max. kapacita:    {max_gb:.0f} GB")
        lines.append(f"  Nainštalované:    {total_gb:.0f} GB")
        lines.append(f"  Sloty:            {data.get('UsedSlots', '?')}/{data.get('TotalSlots', '?')} obsadených")
        lines.append(
            f"  Využitie:         {used_kb / 1024 / 1024:.1f} GB / {visible_kb / 1024 / 1024:.1f} GB ({usage_pct:.1f}%)")
    except:
        lines.append("  Chyba pri načítaní súhrnu")

    # Jednotlivé moduly
    lines.append("\n  Moduly:")

    smbios_types = {
        0: 'Unknown', 20: 'DDR', 21: 'DDR2', 22: 'DDR2 FB-DIMM',
        23: 'DDR3', 24: 'FBD2', 25: 'DDR4', 26: 'LPDDR',
        33: 'DDR5', 34: 'LPDDR5'
    }

    ps = """
$mods = Get-CimInstance Win32_PhysicalMemory
foreach ($m in $mods) {
    Write-Output "MOD_START"
    Write-Output "Slot=$($m.DeviceLocator)"
    Write-Output "Capacity=$($m.Capacity)"
    Write-Output "Speed=$($m.Speed)"
    Write-Output "Manufacturer=$($m.Manufacturer)"
    Write-Output "PartNumber=$($m.PartNumber)"
    Write-Output "SMBIOSMemoryType=$($m.SMBIOSMemoryType)"
    Write-Output "MOD_END"
}
"""
    result = run_powershell(ps, remote)
    current = {}

    for line in result.split('\n'):
        line = line.strip()
        if line == "MOD_START":
            current = {}
        elif line == "MOD_END" and current:
            try:
                cap_gb = int(current.get('Capacity', 0)) / (1024 ** 3)
                mem_type = smbios_types.get(int(current.get('SMBIOSMemoryType', 0)), 'Unknown')
            except:
                cap_gb = 0
                mem_type = 'Unknown'
            lines.append(
                f"    {current.get('Slot', 'N/A'):10} {cap_gb:5.0f} GB  {current.get('Speed', 'N/A'):>5} MHz  {mem_type:8}  {current.get('Manufacturer', '').strip():20}  {current.get('PartNumber', '').strip()}")
            current = {}
        elif '=' in line:
            k, v = line.split('=', 1)
            current[k] = v

    return lines


def get_disk_info(remote: str = None) -> list:
    """Informácie o diskoch."""
    lines = [section_header("DISKY")]

    # Fyzické disky
    lines.append("\n  Fyzické disky:")

    ps = """
$disks = Get-CimInstance Win32_DiskDrive
foreach ($d in $disks) {
    Write-Output "DISK_START"
    Write-Output "Model=$($d.Model)"
    Write-Output "Size=$($d.Size)"
    Write-Output "InterfaceType=$($d.InterfaceType)"
    Write-Output "MediaType=$($d.MediaType)"
    Write-Output "SerialNumber=$($d.SerialNumber)"
    Write-Output "Partitions=$($d.Partitions)"
    Write-Output "Status=$($d.Status)"
    Write-Output "DISK_END"
}
"""
    result = run_powershell(ps, remote)
    current = {}
    disk_num = 0

    for line in result.split('\n'):
        line = line.strip()
        if line == "DISK_START":
            current = {}
        elif line == "DISK_END" and current:
            disk_num += 1
            try:
                size_gb = int(current.get('Size', 0)) / (1024 ** 3)
            except:
                size_gb = 0
            lines.append(f"\n    Disk #{disk_num}:")
            lines.append(f"      Model:      {current.get('Model', 'N/A')}")
            lines.append(f"      Veľkosť:    {size_gb:.0f} GB")
            lines.append(f"      Rozhranie:  {current.get('InterfaceType', 'N/A')}")
            lines.append(f"      Typ média:  {current.get('MediaType', 'N/A')}")
            lines.append(f"      Partície:   {current.get('Partitions', 'N/A')}")
            lines.append(f"      Sér. číslo: {current.get('SerialNumber', 'N/A').strip()}")
            current = {}
        elif '=' in line:
            k, v = line.split('=', 1)
            current[k] = v

    # Logické disky
    lines.append("\n  Logické disky (partície):")

    ps = """
$vols = Get-CimInstance Win32_LogicalDisk | Where-Object {$_.DriveType -eq 3}
foreach ($v in $vols) {
    Write-Output "VOL_START"
    Write-Output "DeviceID=$($v.DeviceID)"
    Write-Output "VolumeName=$($v.VolumeName)"
    Write-Output "Size=$($v.Size)"
    Write-Output "FreeSpace=$($v.FreeSpace)"
    Write-Output "FileSystem=$($v.FileSystem)"
    Write-Output "VOL_END"
}
"""
    result = run_powershell(ps, remote)
    current = {}

    for line in result.split('\n'):
        line = line.strip()
        if line == "VOL_START":
            current = {}
        elif line == "VOL_END" and current:
            try:
                size_gb = int(current.get('Size', 0)) / (1024 ** 3)
                free_gb = int(current.get('FreeSpace', 0)) / (1024 ** 3)
                used_pct = ((size_gb - free_gb) / size_gb * 100) if size_gb else 0
            except:
                size_gb = free_gb = used_pct = 0
            lines.append(
                f"    {current.get('DeviceID', '?'):3} {current.get('VolumeName', ''):15} {size_gb:8.1f} GB  Voľné: {free_gb:8.1f} GB ({100 - used_pct:5.1f}%)  {current.get('FileSystem', 'N/A')}")
            current = {}
        elif '=' in line:
            k, v = line.split('=', 1)
            current[k] = v

    return lines


def get_network_info(remote: str = None) -> list:
    """Informácie o sieti."""
    lines = [section_header("SIEŤ")]

    ps = """
$adapters = Get-CimInstance Win32_NetworkAdapterConfiguration | Where-Object {$_.IPEnabled -eq $true}
foreach ($a in $adapters) {
    Write-Output "NET_START"
    Write-Output "Description=$($a.Description)"
    Write-Output "MACAddress=$($a.MACAddress)"
    Write-Output "IPAddress=$($a.IPAddress -join ', ')"
    Write-Output "IPSubnet=$($a.IPSubnet -join ', ')"
    Write-Output "DefaultGateway=$($a.DefaultIPGateway -join ', ')"
    Write-Output "DNSServers=$($a.DNSServerSearchOrder -join ', ')"
    Write-Output "DHCPEnabled=$($a.DHCPEnabled)"
    Write-Output "NET_END"
}
"""
    result = run_powershell(ps, remote)
    current = {}
    adapter_num = 0

    for line in result.split('\n'):
        line = line.strip()
        if line == "NET_START":
            current = {}
        elif line == "NET_END" and current:
            adapter_num += 1
            lines.append(f"\n  Adaptér #{adapter_num}:")
            lines.append(f"    Popis:        {current.get('Description', 'N/A')}")
            lines.append(f"    MAC:          {current.get('MACAddress', 'N/A')}")
            lines.append(f"    IP:           {current.get('IPAddress', 'N/A')}")
            lines.append(f"    Maska:        {current.get('IPSubnet', 'N/A')}")
            lines.append(f"    Brána:        {current.get('DefaultGateway', 'N/A')}")
            lines.append(f"    DNS:          {current.get('DNSServers', 'N/A')}")
            lines.append(f"    DHCP:         {current.get('DHCPEnabled', 'N/A')}")
            current = {}
        elif '=' in line:
            k, v = line.split('=', 1)
            current[k] = v

    return lines


def get_gpu_info(remote: str = None) -> list:
    """Informácie o grafických kartách."""
    lines = [section_header("GRAFIKA (GPU)")]

    ps = """
$gpus = Get-CimInstance Win32_VideoController
foreach ($g in $gpus) {
    Write-Output "GPU_START"
    Write-Output "Name=$($g.Name)"
    Write-Output "AdapterRAM=$($g.AdapterRAM)"
    Write-Output "DriverVersion=$($g.DriverVersion)"
    Write-Output "DriverDate=$($g.DriverDate)"
    Write-Output "VideoProcessor=$($g.VideoProcessor)"
    Write-Output "CurrentResolution=$($g.CurrentHorizontalResolution)x$($g.CurrentVerticalResolution)"
    Write-Output "RefreshRate=$($g.CurrentRefreshRate)"
    Write-Output "Status=$($g.Status)"
    Write-Output "GPU_END"
}
"""
    result = run_powershell(ps, remote)
    current = {}
    gpu_num = 0

    for line in result.split('\n'):
        line = line.strip()
        if line == "GPU_START":
            current = {}
        elif line == "GPU_END" and current:
            gpu_num += 1
            try:
                vram_gb = int(current.get('AdapterRAM', 0)) / (1024 ** 3)
            except:
                vram_gb = 0
            lines.append(f"\n  GPU #{gpu_num}:")
            lines.append(f"    Názov:       {current.get('Name', 'N/A')}")
            lines.append(f"    VRAM:        {vram_gb:.1f} GB" if vram_gb > 0 else "    VRAM:        N/A")
            lines.append(f"    Driver:      {current.get('DriverVersion', 'N/A')}")
            lines.append(
                f"    Rozlíšenie:  {current.get('CurrentResolution', 'N/A')} @ {current.get('RefreshRate', 'N/A')} Hz")
            current = {}
        elif '=' in line:
            k, v = line.split('=', 1)
            current[k] = v

    return lines


def get_motherboard_info(remote: str = None) -> list:
    """Informácie o základnej doske."""
    lines = [section_header("ZÁKLADNÁ DOSKA")]

    ps = """
$bb = Get-CimInstance Win32_BaseBoard
$slots = Get-CimInstance Win32_SystemSlot
Write-Output "Manufacturer=$($bb.Manufacturer)"
Write-Output "Product=$($bb.Product)"
Write-Output "Version=$($bb.Version)"
Write-Output "SerialNumber=$($bb.SerialNumber)"
Write-Output "SlotCount=$($slots.Count)"
"""
    data = parse_output(run_powershell(ps, remote))

    lines.append(f"  Výrobca:        {data.get('Manufacturer', 'N/A')}")
    lines.append(f"  Model:          {data.get('Product', 'N/A')}")
    lines.append(f"  Verzia:         {data.get('Version', 'N/A')}")
    lines.append(f"  Sériové číslo:  {data.get('SerialNumber', 'N/A')}")
    lines.append(f"  Expanzné sloty: {data.get('SlotCount', 'N/A')}")

    return lines


def get_psu_thermal_info(remote: str = None) -> list:
    """Informácie o napájaní a teplotách (ak dostupné)."""
    lines = [section_header("NAPÁJANIE A TEPLOTY")]

    # Battery (pre notebooky/UPS)
    ps = """
$bat = Get-CimInstance Win32_Battery
if ($bat) {
    Write-Output "BatteryStatus=$($bat.BatteryStatus)"
    Write-Output "EstimatedChargeRemaining=$($bat.EstimatedChargeRemaining)"
    Write-Output "Name=$($bat.Name)"
}
"""
    data = parse_output(run_powershell(ps, remote))

    if data.get('Name'):
        lines.append(f"  Batéria:        {data.get('Name', 'N/A')}")
        lines.append(f"  Nabité:         {data.get('EstimatedChargeRemaining', 'N/A')}%")
    else:
        lines.append("  Batéria:        Nie je (desktop/server)")

    # Teploty (často nedostupné bez vendor nástrojov)
    ps = """
$temps = Get-CimInstance MSAcpi_ThermalZoneTemperature -Namespace root/wmi -ErrorAction SilentlyContinue
if ($temps) {
    foreach ($t in $temps) {
        $celsius = ($t.CurrentTemperature - 2732) / 10
        Write-Output "Temp=$celsius"
    }
}
"""
    result = run_powershell(ps, remote)
    if "Temp=" in result:
        for line in result.split('\n'):
            if line.strip().startswith("Temp="):
                temp = line.split('=')[1]
                lines.append(f"  Teplota:        {temp}°C")
    else:
        lines.append("  Teploty:        Nedostupné (vyžaduje vendor nástroje)")

    return lines


def get_usb_devices(remote: str = None) -> list:
    """Informácie o USB zariadeniach."""
    lines = [section_header("USB ZARIADENIA")]

    ps = """
$usb = Get-CimInstance Win32_USBHub
foreach ($u in $usb) {
    Write-Output "USB: $($u.Name)"
}
"""
    result = run_powershell(ps, remote)

    for line in result.split('\n'):
        line = line.strip()
        if line.startswith("USB:"):
            lines.append(f"  {line[4:].strip()}")

    if len(lines) == 1:
        lines.append("  Žiadne USB huby nenájdené")

    return lines


def get_hardware_report(remote_server: str = None) -> str:
    """Generuje kompletný hardwarový report."""
    target = remote_server if remote_server else "localhost"

    lines = []
    lines.append("#" * 70)
    lines.append(f"#  KOMPLETNÁ HARDWAROVÁ ANALÝZA")
    lines.append(f"#  Server: {target}")
    lines.append(f"#  Čas:    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("#" * 70)

    print(f"Analyzujem hardvér na {target}...")

    sections = [
        ("Systém", get_system_info),
        ("CPU", get_cpu_info),
        ("RAM", get_memory_info),
        ("Základná doska", get_motherboard_info),
        ("GPU", get_gpu_info),
        ("Disky", get_disk_info),
        ("Sieť", get_network_info),
        ("Napájanie/Teploty", get_psu_thermal_info),
        ("USB", get_usb_devices),
    ]

    for name, func in sections:
        print(f"  Zisťujem: {name}...")
        try:
            lines.extend(func(remote_server))
        except Exception as e:
            lines.append(f"\n  CHYBA pri {name}: {e}")

    lines.append("\n" + "=" * 70)
    lines.append("  KONIEC REPORTU")
    lines.append("=" * 70)

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Kompletná analýza hardvéru Windows servera')
    parser.add_argument('--remote', '-r', help='Názov alebo IP vzdialeného servera')
    parser.add_argument('--output', '-o', help='Uložiť výstup do súboru')

    args = parser.parse_args()

    report = get_hardware_report(args.remote)
    print(report)

    filename = args.output or f"hw_report_{args.remote or 'localhost'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\nReport uložený do: {filename}")


if __name__ == "__main__":
    main()