"""
RAM Analyzer pre Windows Server
Získa detailné informácie o nainštalovaných pamäťových moduloch
pre účely objednávky kompatibilnej RAM.

Spustenie: python analyze_ram.py
Pre vzdialený server: python analyze_ram.py --remote SERVERNAME
"""

import subprocess
import sys
import argparse
from datetime import datetime


def run_powershell(script: str, remote_server: str = None) -> str:
    """Spustí PowerShell príkaz lokálne alebo vzdialene."""
    if remote_server:
        script = f"Invoke-Command -ComputerName {remote_server} -ScriptBlock {{ {script} }}"

    cmd = ["powershell", "-NoProfile", "-Command", script]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            encoding='utf-8',
            errors='replace'
        )
        if result.returncode != 0 and result.stderr:
            return f"ERROR: {result.stderr}"
        return result.stdout
    except subprocess.TimeoutExpired:
        return "ERROR: Timeout pri pripojení"
    except Exception as e:
        return f"ERROR: {e}"


def get_detailed_memory(remote_server: str = None) -> str:
    """Získa detailný výstup pre RAM analýzu."""
    target = remote_server if remote_server else "localhost"

    output_lines = []
    output_lines.append("=" * 70)
    output_lines.append(f"  RAM ANALÝZA - {target}")
    output_lines.append(f"  Čas: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output_lines.append("=" * 70)
    output_lines.append("")

    # 1. Fyzické pamäťové moduly - detailne
    output_lines.append("NAINŠTALOVANÉ PAMÄŤOVÉ MODULY:")
    output_lines.append("-" * 70)

    ps_script = """
$modules = Get-CimInstance -ClassName Win32_PhysicalMemory
$i = 0
foreach ($m in $modules) {
    $i++
    Write-Output "MODUL_START"
    Write-Output "Num=$i"
    Write-Output "DeviceLocator=$($m.DeviceLocator)"
    Write-Output "BankLabel=$($m.BankLabel)"
    Write-Output "Capacity=$($m.Capacity)"
    Write-Output "Speed=$($m.Speed)"
    Write-Output "ConfiguredClockSpeed=$($m.ConfiguredClockSpeed)"
    Write-Output "Manufacturer=$($m.Manufacturer)"
    Write-Output "PartNumber=$($m.PartNumber)"
    Write-Output "SerialNumber=$($m.SerialNumber)"
    Write-Output "FormFactor=$($m.FormFactor)"
    Write-Output "MemoryType=$($m.MemoryType)"
    Write-Output "SMBIOSMemoryType=$($m.SMBIOSMemoryType)"
    Write-Output "MODUL_END"
}
"""

    result = run_powershell(ps_script, remote_server)

    if "ERROR" in result:
        output_lines.append(f"  {result}")
    else:
        # Form Factor dekódovanie
        form_factors = {
            0: 'Unknown', 1: 'Other', 2: 'SIP', 3: 'DIP',
            4: 'ZIP', 5: 'SOJ', 6: 'Proprietary', 7: 'SIMM',
            8: 'DIMM', 9: 'TSOP', 10: 'PGA', 11: 'RIMM',
            12: 'SODIMM', 13: 'SRIMM', 14: 'SMD', 15: 'SSMP',
            16: 'QFP', 17: 'TQFP', 18: 'SOIC', 19: 'LCC',
            20: 'PLCC', 21: 'BGA', 22: 'FPBGA', 23: 'LGA'
        }

        # SMBIOS Memory Type (modernejšie)
        smbios_types = {
            0: 'Unknown', 1: 'Other', 2: 'DRAM', 3: 'Synchronous DRAM',
            4: 'Cache DRAM', 5: 'EDO', 6: 'EDRAM', 7: 'VRAM',
            8: 'SRAM', 9: 'RAM', 10: 'ROM', 11: 'Flash',
            12: 'EEPROM', 13: 'FEPROM', 14: 'EPROM', 15: 'CDRAM',
            16: '3DRAM', 17: 'SDRAM', 18: 'SGRAM', 19: 'RDRAM',
            20: 'DDR', 21: 'DDR2', 22: 'DDR2 FB-DIMM', 23: 'DDR3',
            24: 'FBD2', 25: 'DDR4', 26: 'LPDDR', 27: 'LPDDR2',
            28: 'LPDDR3', 29: 'LPDDR4', 30: 'Logical non-volatile',
            31: 'HBM', 32: 'HBM2', 33: 'DDR5', 34: 'LPDDR5'
        }

        current_module = {}
        total_capacity = 0
        module_count = 0

        for line in result.split('\n'):
            line = line.strip()
            if line == "MODUL_START":
                current_module = {}
            elif line == "MODUL_END" and current_module:
                module_count += 1
                output_lines.append(f"\n  Modul #{current_module.get('Num', module_count)}:")

                # Kapacita
                try:
                    capacity_bytes = int(current_module.get('Capacity', 0))
                    capacity_gb = capacity_bytes / (1024 ** 3)
                    total_capacity += capacity_bytes
                    output_lines.append(f"    Kapacita:       {capacity_gb:.0f} GB")
                except:
                    output_lines.append(f"    Kapacita:       N/A")

                output_lines.append(f"    Slot:           {current_module.get('DeviceLocator', 'N/A')}")
                output_lines.append(f"    Bank:           {current_module.get('BankLabel', 'N/A')}")
                output_lines.append(f"    Rýchlosť:       {current_module.get('Speed', 'N/A')} MHz")
                output_lines.append(f"    Výrobca:        {current_module.get('Manufacturer', 'N/A').strip()}")
                output_lines.append(f"    Part Number:    {current_module.get('PartNumber', 'N/A').strip()}")
                output_lines.append(f"    Sériové číslo:  {current_module.get('SerialNumber', 'N/A').strip()}")

                # Form Factor
                try:
                    ff = int(current_module.get('FormFactor', 0))
                    output_lines.append(f"    Form Factor:    {form_factors.get(ff, f'Unknown ({ff})')}")
                except:
                    output_lines.append(f"    Form Factor:    N/A")

                # Memory Type (SMBIOS je presnejší)
                try:
                    smbios = int(current_module.get('SMBIOSMemoryType', 0))
                    output_lines.append(f"    Typ pamäte:     {smbios_types.get(smbios, f'Unknown ({smbios})')}")
                except:
                    output_lines.append(f"    Typ pamäte:     N/A")

                current_module = {}
            elif '=' in line:
                key, value = line.split('=', 1)
                current_module[key] = value

        if module_count == 0:
            output_lines.append("  Žiadne moduly nenájdené!")

    # 2. Systémové informácie
    output_lines.append("")
    output_lines.append("")
    output_lines.append("SYSTÉMOVÉ INFORMÁCIE:")
    output_lines.append("-" * 70)

    ps_script = """
$cs = Get-CimInstance -ClassName Win32_ComputerSystem
Write-Output "Manufacturer=$($cs.Manufacturer)"
Write-Output "Model=$($cs.Model)"
Write-Output "TotalPhysicalMemory=$($cs.TotalPhysicalMemory)"
"""
    result = run_powershell(ps_script, remote_server)

    if "ERROR" not in result:
        for line in result.split('\n'):
            line = line.strip()
            if '=' in line:
                key, value = line.split('=', 1)
                if key == 'TotalPhysicalMemory' and value:
                    try:
                        total_bytes = int(value)
                        total_gb = total_bytes / (1024 ** 3)
                        output_lines.append(f"  Celková RAM:  {total_gb:.1f} GB")
                    except:
                        pass
                elif value:
                    output_lines.append(f"  {key}:  {value}")

    # 3. Motherboard info
    output_lines.append("")
    output_lines.append("")
    output_lines.append("ZÁKLADNÁ DOSKA:")
    output_lines.append("-" * 70)

    ps_script = """
$bb = Get-CimInstance -ClassName Win32_BaseBoard
Write-Output "Manufacturer=$($bb.Manufacturer)"
Write-Output "Product=$($bb.Product)"
Write-Output "Version=$($bb.Version)"
"""
    result = run_powershell(ps_script, remote_server)

    if "ERROR" not in result:
        for line in result.split('\n'):
            line = line.strip()
            if '=' in line:
                key, value = line.split('=', 1)
                if value:
                    output_lines.append(f"  {key}:  {value}")

    # 4. Maximálna podporovaná RAM
    output_lines.append("")
    output_lines.append("")
    output_lines.append("PAMÄŤOVÉ SLOTY A LIMITY:")
    output_lines.append("-" * 70)

    ps_script = """
$arrays = Get-CimInstance -ClassName Win32_PhysicalMemoryArray
foreach ($arr in $arrays) {
    Write-Output "MaxCapacity=$($arr.MaxCapacity)"
    Write-Output "MemoryDevices=$($arr.MemoryDevices)"
}
$modules = Get-CimInstance -ClassName Win32_PhysicalMemory
Write-Output "InstalledModules=$($modules.Count)"
"""
    result = run_powershell(ps_script, remote_server)

    if "ERROR" not in result:
        max_cap = 0
        total_slots = 0
        installed = 0
        for line in result.split('\n'):
            line = line.strip()
            if '=' in line:
                key, value = line.split('=', 1)
                if key == 'MaxCapacity' and value:
                    try:
                        max_cap = int(value) / (1024 ** 2)  # KB to GB
                    except:
                        pass
                elif key == 'MemoryDevices' and value:
                    try:
                        total_slots = int(value)
                    except:
                        pass
                elif key == 'InstalledModules' and value:
                    try:
                        installed = int(value)
                    except:
                        pass

        output_lines.append(f"  Max. kapacita:    {max_cap:.0f} GB")
        output_lines.append(f"  Celkom slotov:    {total_slots}")
        output_lines.append(f"  Obsadených:       {installed}")
        output_lines.append(f"  Voľných:          {total_slots - installed}")

    # 5. Aktuálne využitie
    output_lines.append("")
    output_lines.append("")
    output_lines.append("AKTUÁLNE VYUŽITIE RAM:")
    output_lines.append("-" * 70)

    ps_script = """
$os = Get-CimInstance -ClassName Win32_OperatingSystem
Write-Output "TotalVisible=$($os.TotalVisibleMemorySize)"
Write-Output "FreePhysical=$($os.FreePhysicalMemory)"
"""
    result = run_powershell(ps_script, remote_server)

    if "ERROR" not in result:
        values = {}
        for line in result.split('\n'):
            line = line.strip()
            if '=' in line:
                key, value = line.split('=', 1)
                values[key] = value

        if 'TotalVisible' in values and 'FreePhysical' in values:
            try:
                total_kb = int(values['TotalVisible'])
                free_kb = int(values['FreePhysical'])
                used_kb = total_kb - free_kb
                usage_pct = (used_kb / total_kb) * 100

                output_lines.append(f"  Celkom:     {total_kb / 1024 / 1024:.1f} GB")
                output_lines.append(f"  Využité:    {used_kb / 1024 / 1024:.1f} GB ({usage_pct:.1f}%)")
                output_lines.append(f"  Voľné:      {free_kb / 1024 / 1024:.1f} GB ({100 - usage_pct:.1f}%)")
            except:
                pass

    # Sumár
    output_lines.append("")
    output_lines.append("")
    output_lines.append("=" * 70)
    output_lines.append("  SÚHRN PRE OBJEDNÁVKU:")
    output_lines.append("=" * 70)
    output_lines.append("")
    output_lines.append("  Pri objednávke RAM zohľadni:")
    output_lines.append("  1. Part Number existujúceho modulu (pre identickú RAM)")
    output_lines.append("  2. Typ pamäte (DDR3/DDR4/DDR5) - MUSÍ sa zhodovať!")
    output_lines.append("  3. Rýchlosť (MHz) - optimálne rovnaká alebo vyššia")
    output_lines.append("  4. Form Factor (DIMM/SODIMM)")
    output_lines.append("  5. Počet voľných slotov")
    output_lines.append("")

    return '\n'.join(output_lines)


def main():
    parser = argparse.ArgumentParser(
        description='Analyzuje RAM pre účely objednávky kompatibilnej pamäte'
    )
    parser.add_argument(
        '--remote', '-r',
        help='Názov alebo IP vzdialeného servera (vyžaduje admin práva)'
    )
    parser.add_argument(
        '--output', '-o',
        help='Uložiť výstup do súboru'
    )

    args = parser.parse_args()

    # Spustenie analýzy
    report = get_detailed_memory(args.remote)

    # Výstup
    print(report)

    # Uloženie do súboru
    filename = args.output or f"ram_report_{args.remote or 'localhost'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\nReport uložený do: {filename}")


if __name__ == "__main__":
    main()