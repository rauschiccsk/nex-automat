"""
Check NEX Genesis connection method.
Search for database connection strings, ODBC DSN, Btrieve settings.
"""
import os
from pathlib import Path


def search_in_file(filepath: Path, keywords: list) -> list:
    """Search for keywords in file."""
    results = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                for keyword in keywords:
                    if keyword.upper() in line.upper():
                        results.append({
                            'line': line_num,
                            'text': line.strip()[:200],
                            'keyword': keyword
                        })
    except Exception:
        pass
    return results


def search_nex_genesis_config():
    """Search NEX Genesis for database configuration."""

    nex_dir = Path(r"C:\Development\nex-genesis-server")

    if not nex_dir.exists():
        print(f"❌ NEX Genesis directory not found: {nex_dir}")
        return

    print("\n" + "=" * 80)
    print("NEX GENESIS DATABASE CONNECTION ANALYSIS")
    print("=" * 80)
    print(f"Directory: {nex_dir}")
    print("=" * 80)

    # Keywords to search for
    connection_keywords = [
        'ODBC',
        'DSN',
        'ConnectionString',
        'Database',
        'BtrOpen',
        'BtrCall',
        'w3btrv7',
        'YEARACT',
        'STORES',
        'ServerName',
        'HostName',
    ]

    file_types = ['.pas', '.dpr', '.dfm', '.ini', '.cfg', '.conf', '.txt']

    all_findings = {}

    # Search recursively
    for filepath in nex_dir.rglob('*'):
        if not filepath.is_file():
            continue

        if filepath.suffix.lower() not in file_types:
            continue

        # Special interest in specific files
        interesting = any(x in filepath.name.upper() for x in [
            'BTRHAND', 'DATABASE', 'CONNECTION', 'CONFIG', 'MAIN', 'DATAMODULE'
        ])

        findings = search_in_file(filepath, connection_keywords)

        if findings:
            all_findings[filepath] = {
                'findings': findings,
                'interesting': interesting
            }

    # Print interesting files first
    print("\n🔍 HIGH PRIORITY FILES (Database/Connection related):")
    print("-" * 80)

    interesting_files = {k: v for k, v in all_findings.items() if v['interesting']}

    if interesting_files:
        for filepath, data in sorted(interesting_files.items()):
            print(f"\n📄 {filepath.relative_to(nex_dir)}")
            for finding in data['findings'][:10]:  # Max 10 per file
                print(f"   Line {finding['line']:4d}: {finding['text']}")
    else:
        print("   ❌ No high priority files found")

    # Print other files
    other_files = {k: v for k, v in all_findings.items() if not v['interesting']}

    if other_files:
        print("\n\n📋 OTHER FILES WITH DATABASE KEYWORDS:")
        print("-" * 80)

        for filepath, data in sorted(other_files.items()):
            print(f"\n📄 {filepath.relative_to(nex_dir)}")
            for finding in data['findings'][:5]:  # Max 5 per file
                print(f"   Line {finding['line']:4d}: {finding['text']}")

    # Summary
    print("\n\n" + "=" * 80)
    print("SUMMARY:")
    print("=" * 80)
    print(
        f"Total files searched: {len([f for f in nex_dir.rglob('*') if f.is_file() and f.suffix.lower() in file_types])}")
    print(f"Files with findings: {len(all_findings)}")
    print(f"High priority files: {len(interesting_files)}")

    if interesting_files:
        print("\n💡 NEXT STEPS:")
        print("   1. Check BtrHand.pas for Btrieve opening code")
        print("   2. Check DataModule files for connection settings")
        print("   3. Look for database registration or ODBC DSN")

    print("\n" + "=" * 80 + "\n")


def search_file_content(filepath: str):
    """Display specific file content."""
    path = Path(filepath)

    if not path.exists():
        print(f"❌ File not found: {filepath}")
        return

    print("\n" + "=" * 80)
    print(f"FILE CONTENT: {path.name}")
    print("=" * 80)
    print(f"Path: {filepath}")
    print("=" * 80 + "\n")

    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            print(content[:5000])  # First 5000 chars

            if len(content) > 5000:
                print("\n... (truncated) ...")
    except Exception as e:
        print(f"❌ Error reading file: {e}")

    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    search_nex_genesis_config()

    # Also check specific files if they exist
    specific_files = [
        r"C:\Development\nex-genesis-server\BtrHand.pas",
        r"C:\Development\nex-genesis-server\src\BtrHand.pas",
    ]

    print("\n\n" + "=" * 80)
    print("CHECKING SPECIFIC FILES:")
    print("=" * 80)

    for filepath in specific_files:
        if Path(filepath).exists():
            print(f"\n✅ Found: {filepath}")
            search_file_content(filepath)
        else:
            print(f"\n⚠️  Not found: {filepath}")